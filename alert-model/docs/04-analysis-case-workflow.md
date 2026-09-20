# 04 研判、案件与流转

## 1. `sdm_analysis`

一次调查一行，只追加。告警轮、案件轮、重跑、人工都是新行。

主键：`UNIQUE KEY(tenant_id, analysis_id)`。`analysis_id` 每次调查新生成，禁止复用。  
`alert_id` 与 `case_id` 至少一个非空。`subject_type` 标明主体。

| 字段 | 类型 | 必要性 | 说明 |
|---|---|---|---|
| `analysis_id` | `VARCHAR(128)` | 必填 | |
| `tenant_id` | `VARCHAR(128)` | 必填 | |
| `alert_id` | `VARCHAR(128)` | 条件 | 告警轮必填 |
| `case_id` | `VARCHAR(128)` | 条件 | 案件轮必填 |
| `subject_type` | `VARCHAR(32)` | 必填 | ALERT / CASE |
| `analysis_type` | `VARCHAR(64)` | 必填 | GATE / RULE / AI / HUMAN / PLAYBOOK |
| `trigger_mode` | `VARCHAR(64)` | 必填 | ALERT / CASE / REPLAY / MANUAL |
| `conclusion` | `VARCHAR(64)` | 推荐 | 与 verdict 同枚举 |
| `analysis_confidence` | `INT` | 推荐 | 本次调查置信度 0–100 |
| `next_hop` | `VARCHAR(64)` | 条件 | GATE 必填：CLOSE_CANDIDATE / REUSE / FULL_AGENT / HUMAN |
| `noise_reason` | `VARCHAR(64)` | 可选 | EXCLUSION / KNOWN_FP / DUPLICATE / INSUFFICIENT_DATA / NONE |
| `reuses_analysis_id` | `VARCHAR(128)` | 可选 | 复用哪一次 |
| `reasoning_summary` | `TEXT` | 推荐 | ≤400 字 |
| `evidence_gaps` | `VARIANT` | 推荐 | 缺失项 |
| `recommended_actions` | `VARIANT` | 推荐 | |
| `accepted_status` | `VARCHAR(64)` | 推荐 | PENDING / ACCEPTED / REJECTED / SUPERSEDED |
| `accepted_by` | `VARCHAR(128)` | 可选 | 人或 policy_id |
| `policy_id` | `VARCHAR(128)` | 可选 | 允许回写 verdict 的策略 |
| `model_name` | `VARCHAR(128)` | 可选 | |
| `model_version` | `VARCHAR(64)` | 可选 | |
| `prompt_version` | `VARCHAR(64)` | 可选 | |
| `token_in` | `BIGINT` | 可选 | |
| `token_out` | `BIGINT` | 可选 | |
| `duration_ms` | `BIGINT` | 可选 | |
| `created_by` | `VARCHAR(128)` | 推荐 | system / gate / ai / user_id |
| `created_time` | `DATETIME(3)` | 必填 | DATETIME(3) UTC |

最新一行回写告警或案件上的 `latest_analysis_*`。`accepted_status=ACCEPTED` 且策略允许时才改 `verdict`。

闸门（`GATE`）也走本表，不另开状态机。引用过的证据写入 `sdm_analysis_citation`，不在本表存裸 `evidence_id` 列表。

## 2. `sdm_analysis_citation`

分析对证据的稳定引用，只追加。案件轮尤其必须走这里：`evidence_id` 在租户内唯一，并记下引用当时的主体快照与指针摘要。案件轮可以同时引用 Alert 证据和 Case 证据。

主键：`UNIQUE KEY(tenant_id, analysis_id, evidence_id)`。

cite 上的主体是**证据归属**，不是分析行自己的 `subject_type`。XOR 与证据表相同。

| 字段 | 类型 | 必要性 | 说明 |
|---|---|---|---|
| `analysis_id` | `VARCHAR(128)` | 必填 | |
| `tenant_id` | `VARCHAR(128)` | 必填 | |
| `evidence_id` | `VARCHAR(128)` | 必填 | 租户内唯一，见证据表 |
| `evidence_subject_type` | `VARCHAR(32)` | 必填 | 引用当时证据的主体：ALERT / CASE |
| `alert_id` | `VARCHAR(128)` | 条件 | 证据主体为 ALERT 时必填；不随案件合并改写 |
| `case_id` | `VARCHAR(128)` | 条件 | 证据主体为 CASE 时必填 |
| `evidence_type` | `VARCHAR(64)` | 推荐 | 引用时快照 |
| `evidence_role` | `VARCHAR(64)` | 推荐 | 引用时快照 |
| `event_id` | `VARCHAR(128)` | 可选 | 事实主键快照 |
| `external_ref` | `VARCHAR(255)` | 可选 | 非事件引用快照 |
| `evidence_summary` | `TEXT` | 推荐 | 引用时的一句摘要，证据行日后改了也不变 |
| `cited_time` | `DATETIME(3)` | 必填 | DATETIME(3) UTC |

Agent 输出仍是短 JSON（`evidence_id` 列表）。写入服务按 ID 回查证据表，展开成本表行。禁止把主体内短名写进分析。

案件合并或成员迁移后，回查用本表的 `evidence_id` 与主体快照，不要在当前成员告警里按短名猜。

## 3. `sdm_case`

调查待办。人看的队列、优先级、案件叙事挂这里。
**不是**「已确认的同一场攻击」，也**不是**安全 Incident。是否同一故事线看 `correlation_id` / `merge_id`；是否 Incident 看 `case_kind`（ADR-013）。

主键：`UNIQUE KEY(tenant_id, case_id)`。无时间分区。

| 字段 | 类型 | 必要性 | 说明 |
|---|---|---|---|
| `case_id` | `VARCHAR(128)` | 必填 | |
| `tenant_id` | `VARCHAR(128)` | 必填 | |
| `case_name` | `TEXT` | 必填 | 稳定或系统生成的静态标题；**模型不得覆盖** |
| `description` | `TEXT` | 可选 | 静态描述，人可改 |
| `workflow_status` | `VARCHAR(64)` | 必填 | 与告警同一套流程枚举 |
| `case_kind` | `VARCHAR(32)` | 必填 | 默认 `INVESTIGATION`；`INCIDENT` 只能升上去 |
| `verdict` | `VARCHAR(64)` | 必填 | 默认 UNKNOWN |
| `promoted_time` | `DATETIME(3)` | 可选 | DATETIME(3) UTC；升为 INCIDENT 的时间；降级清空 |
| `promoted_by` | `VARCHAR(128)` | 可选 | 人或 policy_id |
| `closed_time` | `DATETIME(3)` | 可选 | DATETIME(3) UTC；进入 CLOSED/SUPPRESSED 时写入；REOPEN 清空 |
| `resolution_reason` | `VARCHAR(64)` | 可选 | 关闭原因 |
| `priority_score` | `INT` | 可选 | 0–100，案件服务计算 |
| `score_source` | `VARCHAR(32)` | 可选 | RULE / COMPUTED / MANUAL |
| `severity` | `VARCHAR(32)` | 推荐 | 案件展示紧急程度，可取成员告警最高值 |
| `primary_entity_id` | `VARCHAR(255)` | 推荐 | |
| `primary_entity_type` | `VARCHAR(64)` | 推荐 | |
| `primary_entity_value` | `TEXT` | 推荐 | |
| `alert_count` | `INT` | 可选 | |
| `correlation_id` | `VARCHAR(128)` | 可选 | 来源故事线 |
| `assignee_id` | `VARCHAR(128)` | 可选 | |
| `ticket_id` | `VARCHAR(128)` | 可选 | |
| `latest_analysis_id` | `VARCHAR(128)` | 可选 | |
| `latest_analysis_conclusion` | `VARCHAR(64)` | 可选 | |
| `latest_analysis_summary` | `TEXT` | 可选 | |
| `latest_analysis_time` | `DATETIME(3)` | 可选 | DATETIME(3) UTC |
| `first_seen` | `DATETIME(3)` | 必填 | DATETIME(3) UTC；成员告警最早 first_seen |
| `last_seen` | `DATETIME(3)` | 必填 | DATETIME(3) UTC |
| `created_time` | `DATETIME(3)` | 必填 | DATETIME(3) UTC |
| `updated_time` | `DATETIME(3)` | 必填 | DATETIME(3) UTC |
| `extensions` | `VARIANT` | 可选 | |

`sdm_alert.case_id` 是当前主案件 ID，一条告警当前至多一个。MVP 只维护这个快照，不保留成员变更历史；多案件并行引用第一版不做。成员是告警，不是 event；案件自有事实指针走 `sdm_evidence`（`subject_type=CASE`），不在本案上存 `event_ids`。

自动编组、误报复核、演练开的 Case 都是 `INVESTIGATION`。IR 队列筛 `case_kind=INCIDENT`。

AI 打开案件时的长叙事是计算视图，不覆盖 `case_name`（与 XSIAM 一致）。需要落库的调查写分析行 `subject_type=CASE`。

## 4. `sdm_case_membership`（后续待办）

本表不在 MVP 建表和读写链路中。以下仅保留为后续设计：启用后作为成员关系的只追加权威历史，回答告警何时进入哪个案件、谁操作、为什么迁移。启用条件和并发契约见 [07 F3](07-follow-ups.md#f3-case-成员历史延后)。

主键：`UNIQUE KEY(tenant_id, membership_id)`。

| 字段 | 类型 | 必要性 | 说明 |
|---|---|---|---|
| `membership_id` | `VARCHAR(128)` | 必填 | 事件主键，禁止复用 |
| `tenant_id` | `VARCHAR(128)` | 必填 | |
| `alert_id` | `VARCHAR(128)` | 必填 | |
| `action_type` | `VARCHAR(64)` | 必填 | ATTACH / DETACH / MOVE / MERGE / SPLIT |
| `from_case_id` | `VARCHAR(128)` | 条件 | ATTACH 为空；其余为变更前案件 |
| `to_case_id` | `VARCHAR(128)` | 条件 | DETACH 为空；其余为变更后案件 |
| `reason` | `VARCHAR(64)` | 必填 | AUTO_GROUP / CORRELATION / MANUAL / MERGE / SPLIT / POLICY |
| `comment` | `TEXT` | 可选 | 人写的迁移说明 |
| `operator_id` | `VARCHAR(128)` | 推荐 | 人或 `agent:case-service` |
| `batch_id` | `VARCHAR(128)` | 条件 | 一次合并/拆分/批量并入共用；单条 ATTACH 可空 |
| `action_time` | `DATETIME(3)` | 必填 | DATETIME(3) UTC |

```
ATTACH  无案件 → A
DETACH  A → 无案件
MOVE    A → B          （人工改挂）
MERGE   B → A          （B 并入幸存的 A，本行是随迁的告警）
SPLIT   A → C          （从 A 拆出到新案件 C）
```

当前 MVP 成员：仅查 `sdm_alert.case_id`。启用本表后，才按 `alert_id` + `action_time` 查入案轨迹、按 `batch_id` 回放批量变更。

## 5. `sdm_workflow_action`

分派、关闭、工单、评论。可作用于告警或案件（`subject_type` + 对应 ID）。

| 字段 | 类型 | 必要性 | 说明 |
|---|---|---|---|
| `workflow_id` | `VARCHAR(128)` | 必填 | |
| `tenant_id` | `VARCHAR(128)` | 必填 | |
| `subject_type` | `VARCHAR(32)` | 必填 | ALERT / CASE |
| `alert_id` | `VARCHAR(128)` | 条件 | |
| `case_id` | `VARCHAR(128)` | 条件 | |
| `action_type` | `VARCHAR(64)` | 必填 | ASSIGN / COMMENT / CONFIRM / CLOSE / SUPPRESS / ESCALATE / CREATE_TICKET / REOPEN / PROMOTE_INCIDENT / DEMOTE_INCIDENT |
| `from_status` | `VARCHAR(64)` | 可选 | |
| `to_status` | `VARCHAR(64)` | 推荐 | |
| `resolution_reason` | `VARCHAR(64)` | 条件 | CLOSE 时推荐 |
| `operator_id` | `VARCHAR(128)` | 推荐 | 可以是 `agent:…` |
| `assignee_id` | `VARCHAR(128)` | 可选 | |
| `ticket_id` | `VARCHAR(128)` | 可选 | |
| `comment` | `TEXT` | 可选 | |
| `action_time` | `DATETIME(3)` | 必填 | DATETIME(3) UTC |

告警流程：

```
NEW → IN_PROGRESS → CONFIRMED → CLOSED
  ↘ SUPPRESSED ↗
CLOSED → REOPEN → IN_PROGRESS
```

`FALSE_POSITIVE` / `BENIGN` 写在 `verdict` 或 `resolution_reason`，不写进 `workflow_status`。

CLOSE / SUPPRESS 同时写主体 `closed_time`。REOPEN 清空。流转行本身只追加，不因案件仍打开而被日历淘汰（ADR-009）。

成员变更不写本表。本表只记录分派、关单、工单。

## 6. `sdm_alert_attack_tag`（可后置）

ATT&CK 多标签。主表已有 primary tactic/technique 供列表。子表第一版可不上。

## 7. 租户配置（非告警语义表）

闸门依赖，但不进 Finding 语义：

| 表 | 用途 |
|---|---|
| `sdm_alert_allowlist` | 租户允许的 IP / 用户 / hash / 路径 / 规则 |
| `sdm_alert_fp_fingerprint` | `tenant + rule_id + 规范化指纹` → 历史 FP |
| `sdm_alert_policy` | 自动回写 verdict 的阈值与类型白名单 |

`sdm_alert_feedback`（lesson / Context Memory）第二阶段再加，不阻塞 MVP。
