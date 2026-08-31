# SDM2.0 hybrid-event contracts

权威物理契约是 `hybrid-event/projection-registry.v1.json`（hybrid-v1）。

| File | Purpose |
|---|---|
| `event_operation_dictionary.json` | 合法 `(event_type, operation)` 对 |
| `schemas/sdm-event-logical.schema.json` | 五层逻辑事件 JSON Schema（Kafka 消息形态） |
| `hybrid-event/object-registry.v1.json` | 逻辑路径清单（`roles.source.endpoint.ip`，…） |
| `hybrid-event/projection-registry.v1.json` | 逻辑路径 → 物理列投影（权威） |
| `hybrid-event/table-metadata.v1.json` | 生成的表元数据 |
| `hybrid-event/profile-registry.v1.json` | 跨来源扩展 profile |
| `hybrid-event/version-policy.v1.json` | 投影版本与兼容策略 |

原文在独立 `schema/006_raw_log.sql`，与 `sdm_event` 经 `event_id` 1:1 关联。校验：`scripts/check_hybrid_event_contract.py`；生成：`scripts/render_hybrid_event_assets.py`。
