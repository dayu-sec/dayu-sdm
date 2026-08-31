-- Append-only workflow action audit log. Identity = (tenant_id, workflow_id).
-- action_time is when the action happened, not part of the unique key (ADR-010).

CREATE TABLE IF NOT EXISTS sdm2_log.sdm_workflow_action (
    tenant_id            VARCHAR(128) NOT NULL,
    workflow_id          VARCHAR(128) NOT NULL,
    action_time          DATETIME(3) NOT NULL,
    subject_type         VARCHAR(32) NOT NULL,
    alert_id             VARCHAR(128) NULL,
    case_id              VARCHAR(128) NULL,
    action_type          VARCHAR(64) NOT NULL,
    from_status          VARCHAR(64) NULL,
    to_status            VARCHAR(64) NULL,
    resolution_reason    VARCHAR(64) NULL,
    operator_id          VARCHAR(128) NULL,
    assignee_id          VARCHAR(128) NULL,
    ticket_id            VARCHAR(128) NULL,
    comment              TEXT NULL,

    INDEX idx_alert_id (alert_id) USING INVERTED,
    INDEX idx_case_id (case_id) USING INVERTED,
    INDEX idx_action_type (action_type) USING INVERTED,
    INDEX idx_action_time (action_time) USING INVERTED
)
UNIQUE KEY(tenant_id, workflow_id)
DISTRIBUTED BY HASH(tenant_id, workflow_id) BUCKETS 4
PROPERTIES (
    "enable_unique_key_merge_on_write" = "true",
    "replication_num" = "1",
    "bloom_filter_columns" = "workflow_id,alert_id,case_id",
    "inverted_index_storage_format" = "V3",
    "light_schema_change" = "true"
);
