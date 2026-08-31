# ADR-010 物理 Unique Key 等于业务身份

- 状态：已接受
- 日期：2026-08-17

## 背景

为迁就 Doris「分区列必须进入 Unique Key」，六张表把 `created_time` / `evidence_time` / `action_time` 写进主键。同一 `(tenant_id, alert_id)` 只要创建时间不同就可以落成两行。二次写入若没复用首次 `created_time`，会静默分叉。

`dedup_key` 本应是检出幂等键，但无法单独做 Unique：它既不是主键，时间分区又会把它拆到不同分区。

工作对象也不该按创建日 RANGE 分区（ADR-009）：分区裁剪换不来身份正确。

## 选项

1. 维持 `UNIQUE KEY(..., created_time, id)`，靠写入约定复用时间。
2. 继续 RANGE 分区，另加一张映射表承担 `dedup_key` 唯一。映射表在 Unique 模型下是后写覆盖，仍要写入约定保首次 `alert_id`。
3. 去掉时间分区。物理 UK = 业务身份。`alert_id` 由 `tenant_id + dedup_key` 稳定派生，使幂等键与主键 1:1。

## 决定

选 3。

| 表 | Unique Key |
|---|---|
| `sdm_alert` | `(tenant_id, alert_id)` |
| `sdm_evidence` | `(tenant_id, evidence_id)`（ADR-012 / ADR-014：租户内唯一；主体是 ALERT 或 CASE） |
| `sdm_alert_entity` | `(tenant_id, alert_id, entity_id, alert_entity_role)` |
| `sdm_analysis` | `(tenant_id, analysis_id)` |
| `sdm_analysis_citation` | `(tenant_id, analysis_id, evidence_id)` |
| `sdm_case` | `(tenant_id, case_id)` |
| `sdm_workflow_action` | `(tenant_id, workflow_id)` |

规则：

1. 工作对象表不做 `PARTITION BY RANGE(时间)`。时间列只做倒排索引，供列表筛选。
2. `alert_id = alert_` + `sha256(tenant_id || 0x1F || dedup_key)` 的前 24 位十六进制。禁止随机 UUID。同一 `dedup_key` 必然打到同一行。
3. Doris 一张表只能有一个 Unique Key。`dedup_key` 的幂等由派生 `alert_id` 承担，列本身保留倒排，供对账和规则回放。
4. 二次写入走同一 `alert_id`，刷新 `last_seen` / `event_count` / `updated_time`。`created_time` 以首次为准：部分列更新，或载荷带回首次值。`sequence_col = updated_time` 只解决谁更新，不保护 `created_time`。
5. 跨窗口同一现象用 `merge_id`，那是新的 `dedup_key` / `alert_id`，不是同一行。

## 后果

- 按 `created_time` 做分区裁剪不再可用；列表靠倒排 + `tenant_id` 分桶。
- ADR-009 的「不要按创建日 DROP PARTITION」自然成立：已经没有这类分区。
- 归档仍按 `closed_time` 行级删除。
