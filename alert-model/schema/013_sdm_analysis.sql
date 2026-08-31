-- Append-only investigation history. Identity = (tenant_id, analysis_id).

CREATE TABLE IF NOT EXISTS sdm2_log.sdm_analysis (
    tenant_id                 VARCHAR(128) NOT NULL,
    analysis_id               VARCHAR(128) NOT NULL,
    created_time              DATETIME(3) NOT NULL,
    alert_id                  VARCHAR(128) NULL,
    case_id                   VARCHAR(128) NULL,
    subject_type              VARCHAR(32) NOT NULL,
    analysis_type             VARCHAR(64) NOT NULL,
    trigger_mode              VARCHAR(64) NOT NULL,
    conclusion                VARCHAR(64) NULL,
    analysis_confidence       INT NULL,
    next_hop                  VARCHAR(64) NULL,
    noise_reason              VARCHAR(64) NULL,
    reuses_analysis_id        VARCHAR(128) NULL,
    reasoning_summary         TEXT NULL,
    evidence_gaps             VARIANT NULL,
    recommended_actions       VARIANT NULL,
    accepted_status           VARCHAR(64) NULL,
    accepted_by               VARCHAR(128) NULL,
    policy_id                 VARCHAR(128) NULL,
    model_name                VARCHAR(128) NULL,
    model_version             VARCHAR(64) NULL,
    prompt_version            VARCHAR(64) NULL,
    token_in                  BIGINT NULL,
    token_out                 BIGINT NULL,
    duration_ms               BIGINT NULL,
    created_by                VARCHAR(128) NULL,

    INDEX idx_alert_id (alert_id) USING INVERTED,
    INDEX idx_case_id (case_id) USING INVERTED,
    INDEX idx_analysis_type (analysis_type) USING INVERTED,
    INDEX idx_trigger_mode (trigger_mode) USING INVERTED,
    INDEX idx_conclusion (conclusion) USING INVERTED,
    INDEX idx_created_time (created_time) USING INVERTED
)
UNIQUE KEY(tenant_id, analysis_id)
DISTRIBUTED BY HASH(tenant_id, analysis_id) BUCKETS 4
PROPERTIES (
    "enable_unique_key_merge_on_write" = "true",
    "replication_num" = "1",
    "bloom_filter_columns" = "analysis_id,alert_id,case_id",
    "inverted_index_storage_format" = "V3",
    "light_schema_change" = "true"
);
