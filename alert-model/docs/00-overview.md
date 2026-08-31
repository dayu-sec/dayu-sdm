# SDM2.0 告警模型概览

> 版本：v0.2（相对 `s4-standards` 55 列主表草案的重设计）
> 状态：设计中
> 日期：2026-08-18

## 1. 回答什么问题

| 层 | 对象 | 回答 |
|---|---|---|
| 事实 | `sdm_event` | 发生了什么 |
| 检出 | `sdm_alert` | 哪条检测认为值得看 |
| 证据 | `sdm_evidence` | 依据哪些事实（主体是 ALERT 或 CASE；`evidence_id` 租户内唯一） |
| 实体 | `sdm_alert_entity` | 涉及谁、研判角色是什么 |
| 调查 | `sdm_analysis` | 这一次查下来结论是什么 |
| 案件 | `sdm_case` | 谁来处理这组告警（待办）；不是「已确认的攻击」 |
| 事件 | `sdm_case.case_kind=INCIDENT` | 是否正式安全事件；默认不是 |
| 流转 | `sdm_workflow_action` | 分派、关闭、工单做了哪些动作 |

`sdm_event.event_category='alert'` 只表示来源侧声称这是告警，**不是**平台 `sdm_alert`。

## 2. 相对 v0.1 / 55 列草案改了什么

1. **主表变瘦**：检出对象不再同时当实体库、证据库、工单和调查快照。
2. **删除主表权威的 12 列 `attacker_*` / `victim_*`**：列表只留 `primary_entity_*`；明细进实体表。
3. **删除主表 `evidences` VARIANT**：证据只存在证据表，避免双写。
4. **正式结论与检测分数拆开**：规则写 `detection_confidence` / `detection_risk_score`；AI 写分析行；`verdict` 仅策略或人回写。
5. **Case 成为一等对象**：不再用 `incident_ids` 数组冒充案件。
6. **分析只追加**：告警轮与 Case 轮各写一行，可重跑。
7. **闸门用代码**：排除、指纹、复用、缺字段、加塞不依赖小模型。
8. **拿掉未定稿状态列**：`disposition_status` / `ticket_status` 不进核心契约。
9. **分区不是生命周期**：未结案对象按 `closed_time` 行级归档（ADR-009）。
10. **物理 UK = 业务身份**：时间列不进主键；工作对象不做 RANGE 分区；`alert_id` 由 `dedup_key` 派生（ADR-010）。
11. **MVP 只保留 Case 快照**：`alert.case_id` 是当前主案件 ID；成员变更历史 `sdm_case_membership` 延后（ADR-011 / F3）。
12. **证据引用租户内唯一**：`evidence_id` 不按告警缩域；分析引用落 cite 表（ADR-012）。
13. **Case 不是 Incident**：建案默认调查；升级才是安全事件，不另开 `sdm_incident`（ADR-013）。
14. **证据按主体挂载**：`sdm_evidence.subject_type` 为 ALERT 或 CASE，二选一。触发日志挂 Alert；调查新增挂 Case。cite 表为 `sdm_analysis_citation`（ADR-014）。

## 3. 大宽表与分层模型

不走大禹 / QAX 那种单表几百列。检出主表只服务列表；证据、实体、分析、案件、流转分表。列表扫瘦主表；详情和 AI 走聚合，不把宽行当写模型。对照表见 [08 P3](08-review-presentation-outline.md#p3-大宽表与分层模型对比)。

```
sdm_event / raw_log / 外部引用
        ↑ 引用，不复制
sdm_evidence            subject_type = ALERT | CASE（二选一）
        ↑
sdm_alert           N:1  sdm_case     （case_id = 当前主案件 ID）
        ↓ 1:N
sdm_alert_entity
sdm_analysis      （alert_id 与/或 case_id）
sdm_analysis_citation       （任意 evidence_id + 当时主体快照）
sdm_workflow_action
```

```
Alert ──▶ Evidence ──▶ Event     检出触发 / 检出上下文
Case  ──▶ Evidence ──▶ Event     调查新增；不重复挂载成员告警已有事实
Case Analysis ──▶ Cite ──▶ 任意 Evidence
```

列表只查 `sdm_alert`（及需要时 `sdm_case`）。详情并行查子表。
`sdm_case_membership` 为后续设计，不在 MVP 建表和读写链路中。

## 4. 阅读顺序

| 文档 | 内容 |
|---|---|
| [01 主契约](01-main-contract.md) | 边界、键、状态机、写入原则 |
| [02 告警主表](02-alert-fields.md) | `sdm_alert` 字段 |
| [03 证据与实体](03-evidence-and-entity.md) | `sdm_evidence`、`sdm_alert_entity` |
| [04 研判、案件与流转](04-analysis-case-workflow.md) | analysis / case / workflow / 租户配置 |
| [05 枚举](05-enums.md) | 已定稿枚举 |
| [06 运行时流程](06-runtime-pipeline.md) | 闸门、两轮研判、限流 |
| [07 后续待办](07-follow-ups.md) | 接受流、verdict 账、成员并发 |
| [08 评审介绍会提纲](08-review-presentation-outline.md) | 会议目标、大宽表与分层对比、逐页讲述与决策清单 |
| [decisions/](decisions/) | 架构决策记录（ADR-001 … 014） |

机器可读层：`standards/`。DDL：`schema/`。
