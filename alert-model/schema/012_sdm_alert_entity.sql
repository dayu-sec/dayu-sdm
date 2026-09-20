-- Identity = (tenant_id, alert_id, entity_id, alert_entity_role).
-- created_time is denormalized from the alert, not part of the unique key (ADR-010).

CREATE TABLE IF NOT EXISTS sdm2_log.sdm_alert_entity (
    tenant_id             VARCHAR(128) NOT NULL,
    alert_id              VARCHAR(128) NOT NULL,
    entity_id             VARCHAR(255) NOT NULL,
    alert_entity_role     VARCHAR(64) NOT NULL,
    created_time          DATETIME(3) NOT NULL,
    entity_type           VARCHAR(64) NOT NULL,
    event_role_hint       VARCHAR(64) NULL,
    entity_value          TEXT NULL,
    is_primary            BOOLEAN NULL,
    asset_id              VARCHAR(128) NULL,
    asset_name            VARCHAR(255) NULL,
    asset_type            VARCHAR(64) NULL,
    used_for_grouping     BOOLEAN NULL,
    grouping_weight       DOUBLE NULL,
    valid_until           DATETIME(3) NULL,
    risk_context          VARIANT NULL,

    INDEX idx_entity_id (entity_id) USING INVERTED,
    INDEX idx_entity_type (entity_type) USING INVERTED,
    INDEX idx_alert_entity_role (alert_entity_role) USING INVERTED
)
UNIQUE KEY(tenant_id, alert_id, entity_id, alert_entity_role)
DISTRIBUTED BY HASH(tenant_id, alert_id) BUCKETS 4
PROPERTIES (
    "enable_unique_key_merge_on_write" = "true",
    "replication_num" = "1",
    "bloom_filter_columns" = "alert_id,entity_id",
    "inverted_index_storage_format" = "V3",
    "light_schema_change" = "true"
);
