# SDM2.0 hybrid-event contracts — live

The standards service and its release-control workflow are **retired (2026-08)**.

What remains here is the live 002 event contract:

| File | Purpose |
|---|---|
| `event_operation_dictionary.json` | Valid `(event_type, operation)` pairs (shared by five-layer and 87-col validators) |
| `schemas/sdm-event-logical.schema.json` | Five-layer logical event JSON Schema (Kafka message shape) |
| `hybrid-event/object-registry.v1.json` | Logical path inventory (`roles.source.endpoint.ip`, …) |
| `hybrid-event/projection-registry.v1.json` | Logical path → 002 physical column projection |
| `hybrid-event/table-metadata.v1.json` | Generated table metadata |
| `hybrid-event/profile-registry.v1.json` | Registered cross-source extension profiles |
| `hybrid-event/version-policy.v1.json` | Projection version and compatibility policy |

Consumers: `benchmark/converter`, `benchmark/doris/sdm2_doris_ddl.py`,
`benchmark/loader`, `.codex/skills/sdm2-map-log-fields/scripts/five_layer_contract.py`,
`scripts/render_hybrid_event_assets.py`, and
`log-model/`.

Physical shape: governed by `hybrid-event/projection-registry.v1.json` (the split-off raw
payload table `schema/006_raw_log.sql` is associated by `event_id`). The interim
`schema/002_sdm_event.sql` DDL (raw_msg inline column era) and the redundant
`metadata.raw_log_id` (always equal to `event_id`) were both retired 2026-08-26.
Validate with `scripts/check_hybrid_event_contract.py`; regenerate generated
assets with `scripts/render_hybrid_event_assets.py`.
