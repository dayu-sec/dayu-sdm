# SDM2.0 事件契约

现行逻辑契约是 `log-model/docs/main/07-sdm-event-behavior.schema.json`（`2.0`）。
现行物理表是 `log-model/schema/031_sdm_event_behavior.sql`。

| File | Purpose |
|---|---|
| `docs/main/07-sdm-event-behavior.schema.json` | 行为信封机器契约 |
| `docs/main/06-sdm-event-enum-catalog.md` | 闭合枚举 |
| `hybrid-event/object-fields.v1.json` | typed object 字段 |
| `hybrid-event/projection-registry.v1.json` | **旧** sdm_event 投影（退役，仅历史对照） |
| `hybrid-event/table-metadata.v1.json` | 旧表元数据（冻结） |
| `hybrid-event/object-registry.v1.json` | 旧五层路径清单（冻结） |
| `event_operation_dictionary.json` | 旧 `(event_type, operation)` 对照 |

原文在 `schema/006_raw_log.sql`，与行为事件经 `event_id` 1:1。校验：`scripts/validate_behavior_event.py`。

