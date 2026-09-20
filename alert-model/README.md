# SDM2.0 告警模型

> 状态：**实验性 v0.2**。契约以本目录 ADR 与 schema 为准，尚未作为稳定发布。
> `sdm_event_behavior` 回答发生了什么；`sdm_alert` 是检出；`sdm_analysis` 是一次调查；`sdm_case` 是工作单元。AI 只追加分析行，正式 `verdict` 由策略或人写。

## 相对早期 55 列草案

- 主表去掉 12 列摊平实体、`evidences` 双写、未定稿的工单/处置状态、与 description 重复的 summary。
- 检出置信度/风险分与案件优先级分拆开。
- 实体、证据、分析、案件、流转分表；闸门配置不进 Finding 语义。

## 目录

| 路径 | 用途 |
|---|---|
| [docs/00-overview.md](docs/00-overview.md) | 分层与阅读顺序 |
| [docs/01-main-contract.md](docs/01-main-contract.md) | 键、状态、分数、写入 |
| [docs/02-alert-fields.md](docs/02-alert-fields.md) | `sdm_alert` |
| [docs/03-evidence-and-entity.md](docs/03-evidence-and-entity.md) | 证据、实体 |
| [docs/04-analysis-case-workflow.md](docs/04-analysis-case-workflow.md) | 分析、案件、流转 |
| [docs/05-enums.md](docs/05-enums.md) | 枚举 |
| [docs/06-runtime-pipeline.md](docs/06-runtime-pipeline.md) | 闸门与两轮研判 |
| [docs/decisions/](docs/decisions/) | 架构决策记录（ADR-001 … 014） |
| [schema/](schema/) | Doris DDL 010–017 |
| [standards/](standards/) | 枚举与表清单 |
| [examples/reverse_shell/](examples/reverse_shell/) | 规则引擎 DETECTION 写入样例 |
| [examples/ngsoc_alert_info/](examples/ngsoc_alert_info/) | 源 finding → 告警各表 |

## 表

`sdm_alert` · `sdm_evidence` · `sdm_alert_entity` · `sdm_analysis` · `sdm_analysis_citation` · `sdm_case` · `sdm_workflow_action`

后置：`sdm_case_membership`、`sdm_alert_attack_tag`、`sdm_alert_feedback`。服务配置：allowlist / FP 指纹 / 自动关单策略。

## 已关闭的开放问题

| 原问题 | 结论 |
|---|---|
| 宽表 vs 拆表 | 瘦主表 + 子表（ADR-001 / 004） |
| AI 能否改 verdict | 不能直接改（ADR-002） |
| 告警与 Case 边界 | Case 一等（ADR-005） |
| 证据双轨 | 只写证据表（ADR-008） |
| 闸门要不要小模型 | 第一版纯代码（ADR-006） |
| 90 天分区会不会删未结案 | 会；已改为无时间 RANGE + 按 `closed_time` 行级归档（ADR-009 / 010） |
| 物理 UK 是否含 created_time | 不含。UK = 业务身份；`alert_id` 由 `dedup_key` 派生（ADR-010） |
| Case 成员是否只是 alert.case_id | MVP 只保留当前快照；变更历史 `sdm_case_membership` 延后（ADR-011 / F3） |
| Case 分析如何引用跨告警证据 | `evidence_id` 租户内唯一；引用落 `sdm_analysis_citation`（ADR-012） |
| Incident 是不是 Case | 不是。Case 默认调查；`case_kind=INCIDENT` 才是事件，不另开表（ADR-013） |
| Case 能否直挂日志证据 | 能。`sdm_evidence.subject_type` 为 ALERT 或 CASE，二选一；不写 `event_ids` 也不回写 event（ADR-014） |

## 后续待办（v0.2 不改表）

| ID | 问题 | 拟定方向 |
|---|---|---|
| F1 | 分析只追加 vs 原行改 `accepted_status` | 接受也 insert；补 `accepts_analysis_id` / `accepted_time` |
| F2 | verdict 变化无法完整审计 | 只追加的 verdict 决策表 |
| F3 | Case 成员历史延后 | 启用 `sdm_case_membership` 时一并落地 CAS / Outbox / 对账 |
