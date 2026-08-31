-- Deferred design, not part of the MVP core table set (F3 / ADR-011).
-- When enabled, append-only membership events audit changes to alert.case_id.
-- Hash buckets must be a subset of the Unique Key; do not bucket by alert_id.

CREATE TABLE IF NOT EXISTS sdm2_log.sdm_case_membership (
    tenant_id            VARCHAR(128) NOT NULL,
    membership_id        VARCHAR(128) NOT NULL,
    alert_id             VARCHAR(128) NOT NULL,
    action_type          VARCHAR(64) NOT NULL,
    from_case_id         VARCHAR(128) NULL,
    to_case_id           VARCHAR(128) NULL,
    reason               VARCHAR(64) NOT NULL,
    comment              TEXT NULL,
    operator_id          VARCHAR(128) NULL,
    batch_id             VARCHAR(128) NULL,
    action_time          DATETIME(3) NOT NULL,

    INDEX idx_alert_id (alert_id) USING INVERTED,
    INDEX idx_from_case_id (from_case_id) USING INVERTED,
    INDEX idx_to_case_id (to_case_id) USING INVERTED,
    INDEX idx_action_type (action_type) USING INVERTED,
    INDEX idx_reason (reason) USING INVERTED,
    INDEX idx_batch_id (batch_id) USING INVERTED,
    INDEX idx_action_time (action_time) USING INVERTED
)
UNIQUE KEY(tenant_id, membership_id)
DISTRIBUTED BY HASH(tenant_id, membership_id) BUCKETS 4
PROPERTIES (
    "enable_unique_key_merge_on_write" = "true",
    "replication_num" = "1",
    "bloom_filter_columns" = "membership_id,alert_id,from_case_id,to_case_id,batch_id",
    "inverted_index_storage_format" = "V3",
    "light_schema_change" = "true"
);
