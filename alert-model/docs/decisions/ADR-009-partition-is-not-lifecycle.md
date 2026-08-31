# ADR-009 分区删除不是业务生命周期

- 状态：已接受（分区形态由 [ADR-010](ADR-010-unique-key-is-business-identity.md) 改为无时间 RANGE；本条的生命周期规则仍有效）
- 日期：2026-08-17

## 背景

六张告警表都按不可变时间列分区（告警/案件/证据/实体/分析用 `created_time` 或与其对齐的时间，流转用 `action_time`），并曾设置 `dynamic_partition.start = -90`。

Doris Unique Key 必须包含分区列，因此分区键不可变。`updated_time` 只作 merge-on-write 的 sequence 列，**不会把行迁到新分区**。日历删分区会物理删除该创建日（或动作日）的全部行，包括仍打开的 Alert/Case，以及未结案对象的早期 workflow / analysis。

同一天的分区里开单与关单混在一起，无法「只丢掉已关闭的」。

## 选项

1. 维持 `-90`，接受超 90 天的未结案对象消失。
2. 把 `start` 改成更大的负数（如 `-400` / `-1095`）。仍是按创建日一刀切，长案、法律留存、MSS 年报仍会误删。
3. 不设 `dynamic_partition.start`（历史分区不自动删）。清理按 `workflow_status` + `closed_time` 做行级归档，禁止对工作对象 `DROP PARTITION`。

## 决定

选 3。

1. 六张核心表只自动**创建**未来分区（`end=3`）。`history_partition_num=90` 仅表示建表时预建多少天历史分区，不是保留期。
2. `sdm_alert`、`sdm_case` 增加 `closed_time`：进入 `CLOSED` / `SUPPRESSED` 时写入，`REOPEN` 时清空。
3. 物理删除只能由归档作业按行执行，且必须同时满足：
   - 主体 `workflow_status` 为 `CLOSED` 或 `SUPPRESSED`；
   - `closed_time` 早于租户保留期；
   - 告警若仍挂在**未关闭**的 `case_id` 上，即使自身已关单也不得删。
4. 子表随主体归档，不得按自己的时间列单独删。`sdm_evidence` 按 `subject_type` 走：ALERT 证据随告警，CASE 证据随案件。未归档分析仍引用的证据行先留，或接受 cite 摘要自足（ADR-012 / ADR-014）。entity / analysis / workflow 仍随各自主体。
5. 事件表可以继续 90 天日历淘汰；证据只引用事件，事件过期不构成删除告警的理由。

## 后果

- 未结案对象可以跨年存在；存储随未归档历史增长，要用作业而不是分区 TTL 控量。
- 查询仍可按 `created_time` 裁剪分区；列表「活跃」用 `workflow_status` 与 `closed_time IS NULL`。
- 禁止把事件表的 `-90` 抄到告警/案件表。
