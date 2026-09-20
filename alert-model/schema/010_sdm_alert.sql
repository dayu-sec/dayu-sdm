-- Slim detection table. Business identity = (tenant_id, alert_id).
-- No RANGE(created_time): Doris Unique Key must include partition columns,
-- which would allow the same alert_id on two create days (ADR-010).
-- alert_id is derived from tenant_id + dedup_key so dedup is 1:1 with identity.
-- All instant columns are DATETIME(3) UTC, ms precision (Kafka unix ms; RL timezone=Etc/UTC).

CREATE TABLE IF NOT EXISTS __DORIS_DB__.sdm_alert (
    tenant_id                     VARCHAR(128) NOT NULL,
    alert_id                      VARCHAR(128) NOT NULL,
    created_time                  DATETIME(3) NOT NULL,
    alert_display_id              VARCHAR(128) NOT NULL,
    source_alert_id               VARCHAR(128) NULL,
    source_product                VARCHAR(128) NULL,
    alert_name                    TEXT NOT NULL,
    description                   TEXT NULL,
    alert_type                    VARCHAR(64) NOT NULL,
    category_code                 VARCHAR(64) NOT NULL,
    event_count                   BIGINT NULL,
    severity                      VARCHAR(32) NOT NULL,
    detection_confidence          INT NULL,
    detection_risk_score          INT NULL,
    workflow_status               VARCHAR(64) NOT NULL,
    verdict                       VARCHAR(64) NOT NULL,
    closed_time                   DATETIME(3) NULL,
    updated_time                  DATETIME(3) NOT NULL,
    first_seen                    DATETIME(3) NOT NULL,
    last_seen                     DATETIME(3) NOT NULL,
    rule_id                       VARCHAR(128) NULL,
    rule_name                     TEXT NULL,
    rule_version                  VARCHAR(64) NULL,
    rule_type                     VARCHAR(64) NULL,
    detection_engine              VARCHAR(128) NULL,
    dedup_key                     VARCHAR(255) NOT NULL,
    merge_id                      VARCHAR(128) NULL,
    correlation_id                VARCHAR(128) NULL,
    case_id                       VARCHAR(128) NULL,
    primary_entity_id             VARCHAR(255) NULL,
    primary_entity_type           VARCHAR(64) NULL,
    primary_entity_value          TEXT NULL,
    primary_entity_role           VARCHAR(64) NULL,
    primary_tactic_id             VARCHAR(64) NULL,
    primary_technique_id          VARCHAR(64) NULL,
    latest_analysis_id            VARCHAR(128) NULL,
    latest_analysis_conclusion    VARCHAR(64) NULL,
    latest_analysis_confidence    INT NULL,
    latest_analysis_summary       TEXT NULL,
    latest_analysis_time          DATETIME(3) NULL,
    assignee_id                   VARCHAR(128) NULL,
    ticket_id                     VARCHAR(128) NULL,
    extensions                    VARIANT NULL,

    INDEX idx_severity (severity) USING INVERTED,
    INDEX idx_workflow_status (workflow_status) USING INVERTED,
    INDEX idx_verdict (verdict) USING INVERTED,
    INDEX idx_closed_time (closed_time) USING INVERTED,
    INDEX idx_alert_type (alert_type) USING INVERTED,
    INDEX idx_category_code (category_code) USING INVERTED,
    INDEX idx_dedup_key (dedup_key) USING INVERTED,
    INDEX idx_created_time (created_time) USING INVERTED,
    INDEX idx_case_id (case_id) USING INVERTED,
    INDEX idx_primary_entity_id (primary_entity_id) USING INVERTED,
    INDEX idx_primary_entity_type (primary_entity_type) USING INVERTED,
    INDEX idx_rule_id (rule_id) USING INVERTED
)
UNIQUE KEY(tenant_id, alert_id)
DISTRIBUTED BY HASH(tenant_id, alert_id) BUCKETS 8
PROPERTIES (
    "enable_unique_key_merge_on_write" = "true",
    "function_column.sequence_col" = "updated_time",
    "replication_num" = "1",
    "bloom_filter_columns" = "alert_id,dedup_key,case_id",
    "inverted_index_storage_format" = "V3",
    "light_schema_change" = "true"
);
