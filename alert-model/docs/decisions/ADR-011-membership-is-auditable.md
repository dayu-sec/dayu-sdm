# ADR-011 Case 成员关系可审计

- 状态：设计已接受，延后实施
- 日期：2026-08-17

## 背景

`sdm_alert.case_id` 只记录当前主案件。运行时却会创建、并入、合并、拆分案件。没有成员历史就无法回答：告警何时进入哪个案件、谁操作、为什么迁移。

`sdm_workflow_action` 管分派和关单，不是成员关系。把 MERGE/MOVE 塞进流转会把状态机和编组缠在一起。

一条告警当前仍只挂一个主案件；需要审计的是这条指针怎么变过来的。

## 选项

1. 只保留 `alert.case_id`，合并历史靠应用日志。
2. 扩 `sdm_workflow_action.action_type`，成员变更当流转动作。
3. 新增只追加的 `sdm_case_membership`。`alert.case_id` 仍是列表快照，任何改动必须同行写一条成员事件。

## 决定

目标设计选 3，但不纳入 MVP。MVP 只保留 `sdm_alert.case_id` 当前快照，不创建、不写入 `sdm_case_membership`，也不实施 MOVE / MERGE / SPLIT。启用条件与并发契约见 [F3](../07-follow-ups.md#f3-case-成员历史延后)。

| `action_type` | `from_case_id` | `to_case_id` |
|---|---|---|
| `ATTACH` | NULL | 新案件 |
| `DETACH` | 原案件 | NULL |
| `MOVE` | 原案件 | 目标案件 |
| `MERGE` | 被吸收案件 | 幸存案件 |
| `SPLIT` | 原案件 | 拆出的新案件 |

`reason`：`AUTO_GROUP` / `CORRELATION` / `MANUAL` / `MERGE` / `SPLIT` / `POLICY`。  
一次合并或拆分共用一个 `batch_id`，按告警各写一行。

后续启用后的写入契约：改 `sdm_alert.case_id` 必须同时 insert 成员行；`case_id` 等于该告警最新事件的 `to_case_id`。禁止只改快照。

当前成员查 `sdm_alert.case_id`；MVP 不提供历史查询。后续启用后，历史才查 `sdm_case_membership`。案件 `alert_count` 由服务按当前成员维护。

第一版仍是「当前一个主案件」。多案件并行引用另议，不靠改快照冒充。

## 后果

- 后续启用后，可以按告警拉完整入案轨迹，按 `batch_id` 回放一次合并。
- 后续归档约束：成员行随告警走；任一端案件仍未关闭则不得删。
