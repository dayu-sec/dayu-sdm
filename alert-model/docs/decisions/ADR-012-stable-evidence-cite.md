# ADR-012 分析引用租户内唯一的证据

- 状态：已接受（归属规则由 [ADR-014](ADR-014-subject-evidence.md) 修订：证据主体改为 ALERT | CASE，表更名为 `sdm_evidence` / `sdm_analysis_citation`）
- 日期：2026-08-17

## 背景

`evidence_id` 曾只在 `(tenant_id, alert_id, evidence_id)` 内唯一。不同告警都可以叫 `evid_1`。案件分析把裸 ID 放进 `cited_evidence_ids`，合并或成员迁移后，按「当前案件里的 evid_1」回查会指到别的告警。引用不含 `alert_id`，也没有引用当时的指针快照。

证据行仍挂在原 `alert_id` 上，案件成员变化不会改证据归属。漂移来自**短名撞车**和**无归属的引用**，不是成员表。

## 选项

1. 维持裸 `cited_evidence_ids`，靠写入约定不撞名。
2. VARIANT 改成 `{alert_id, evidence_id}` 对象数组。能消歧，但不能稳定 join，证据摘要被改后分析仍无当时所见。
3. `evidence_id` 在租户内唯一；引用落到只追加的 cite 表，带来源主体和当时的指针摘要。

## 决定

选 3。

1. 证据表主键为 `UNIQUE KEY(tenant_id, evidence_id)`。主体 ID 不进主键。v0.2 前半主体只能是告警；[ADR-014](ADR-014-subject-evidence.md) 改为 `subject_type` + `alert_id` / `case_id` 二选一。
2. `evidence_id` 稳定派生，禁止 `evid_1` 这种主体内短名。哈希材料见 ADR-014（含 `subject_type` + `subject_id`）。

   `fact_key` 优先 `event_id`，否则 `raw_log_id` / `source_alert_original_id` / `external_ref` / `evidence_payload_ref`。都没有时用写入方提供的局部键（如 NEGATIVE 序号），仍须纳入哈希。
3. 删除分析表 `cited_evidence_ids`。引用写入 `sdm_analysis_citation`：`evidence_id` + 当时的主体快照（`evidence_subject_type` + `alert_id`/`case_id`）、`event_id`/`external_ref`、`evidence_role`、`evidence_summary`。分析行只追加，引用行只追加，不随证据后续更新而改。
4. 同一事件被两个主体引用，是两行、两个 `evidence_id`（哈希含主体）。案件分析可以同时引用它们。
5. 案件合并、成员迁移不改 `evidence_id` 或证据上的主体。回查用引用里的 `evidence_id`，不要在当前成员里按短名猜。

## 后果

- Agent 输出仍是短 JSON，由写入服务展开成 cite 行，不把裸 ID 当权威。
- 证据按行归档时，未归档分析若仍引用该 `evidence_id`，先留证据行或接受 cite 上的摘要自足。
