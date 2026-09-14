# SDM2.0 事件契约

现行逻辑契约是 `../docs/main/07-sdm-event-behavior.schema.json`（`2.0`）。
现行物理表是 `../schema/031_sdm_event_behavior.sql`。

| File | Purpose |
|---|---|
| `../docs/main/07-sdm-event-behavior.schema.json` | 行为信封机器契约 |
| `../docs/main/07-sdm-event-behavior-kafka.schema.json` | Kafka 行为消息（07 同树，三时间为 unix ms） |
| `../docs/main/06-sdm-event-enum-catalog.md` | 闭合枚举 |
| `hybrid-event/object-fields.v1.json` | typed object 字段 |
| `hybrid-event/object-registry.v2.json` | 行为信封对象与 related 路由 |
| `hybrid-event/behavior-cutover-allowlist.v1.json` | 切流准入 |
| `hybrid-event/projection-registry.v1.json` | **旧** sdm_event 投影（冻结） |
| `hybrid-event/table-metadata.v1.json` | 旧表元数据（冻结） |
| `hybrid-event/object-registry.v1.json` | 旧五层路径清单（冻结） |
| `event_operation_dictionary.json` | 旧 `(event_type, operation)` 对照 |

原文在 `../schema/006_raw_log.sql`，与行为事件经 `event_id` 1:1。校验：`../scripts/validate_behavior_event.py`。
