-- Work object. Identity = (tenant_id, case_id). No time partition (ADR-010).
-- case_kind defaults to INVESTIGATION; INCIDENT is a promotion (ADR-013).

CREATE TABLE IF NOT EXISTS sdm2_log.sdm_case (
    tenant_id                      VARCHAR(128) NOT NULL,
    case_id                        VARCHAR(128) NOT NULL,
    created_time                   DATETIME(3) NOT NULL,
    case_name                      TEXT NOT NULL,
    description                    TEXT NULL,
    workflow_status                VARCHAR(64) NOT NULL,
    case_kind                      VARCHAR(32) NOT NULL,
    verdict                        VARCHAR(64) NOT NULL,
    closed_time                    DATETIME(3) NULL,
    promoted_time                  DATETIME(3) NULL,
    promoted_by                    VARCHAR(128) NULL,
    resolution_reason              VARCHAR(64) NULL,
    priority_score                 INT NULL,
    score_source                   VARCHAR(32) NULL,
    severity                       VARCHAR(32) NULL,
    primary_entity_id              VARCHAR(255) NULL,
    primary_entity_type            VARCHAR(64) NULL,
    primary_entity_value           TEXT NULL,
    alert_count                    INT NULL,
    correlation_id                 VARCHAR(128) NULL,
    assignee_id                    VARCHAR(128) NULL,
    ticket_id                      VARCHAR(128) NULL,
    latest_analysis_id             VARCHAR(128) NULL,
    latest_analysis_conclusion     VARCHAR(64) NULL,
    latest_analysis_summary        TEXT NULL,
    latest_analysis_time           DATETIME(3) NULL,
    first_seen                     DATETIME(3) NOT NULL,
    last_seen                      DATETIME(3) NOT NULL,
    updated_time                   DATETIME(3) NOT NULL,
    extensions                     VARIANT NULL,

    INDEX idx_workflow_status (workflow_status) USING INVERTED,
    INDEX idx_case_kind (case_kind) USING INVERTED,
    INDEX idx_verdict (verdict) USING INVERTED,
    INDEX idx_closed_time (closed_time) USING INVERTED,
    INDEX idx_primary_entity_id (primary_entity_id) USING INVERTED,
    INDEX idx_correlation_id (correlation_id) USING INVERTED,
    INDEX idx_created_time (created_time) USING INVERTED
)
UNIQUE KEY(tenant_id, case_id)
DISTRIBUTED BY HASH(tenant_id, case_id) BUCKETS 4
PROPERTIES (
    "enable_unique_key_merge_on_write" = "true",
    "function_column.sequence_col" = "updated_time",
    "replication_num" = "1",
    "bloom_filter_columns" = "case_id,correlation_id",
    "inverted_index_storage_format" = "V3",
    "light_schema_change" = "true"
);
