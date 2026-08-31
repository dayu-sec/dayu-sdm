-- Subject evidence refs. Identity = (tenant_id, evidence_id) — unique in
-- the tenant, not inside one alert or case (ADR-012 / ADR-014).
-- subject_type is ALERT | CASE (exactly one). Application enforces XOR:
-- ALERT => alert_id NOT NULL and case_id NULL;
-- CASE  => case_id NOT NULL and alert_id NULL.

CREATE TABLE IF NOT EXISTS sdm2_log.sdm_evidence (
    tenant_id                   VARCHAR(128) NOT NULL,
    evidence_id                 VARCHAR(128) NOT NULL,
    subject_type                VARCHAR(32) NOT NULL,
    alert_id                    VARCHAR(128) NULL,
    case_id                     VARCHAR(128) NULL,
    evidence_time               DATETIME(3) NOT NULL,
    event_occur_time            DATETIME(3) NULL,
    evidence_type               VARCHAR(64) NOT NULL,
    event_id                    VARCHAR(128) NULL,
    log_id                      VARCHAR(128) NULL,
    raw_log_id                  VARCHAR(128) NULL,
    source_alert_original_id    VARCHAR(128) NULL,
    external_ref                VARCHAR(255) NULL,
    evidence_payload_ref        VARCHAR(255) NULL,
    evidence_role               VARCHAR(64) NULL,
    event_type                  VARCHAR(128) NULL,
    evidence_summary            TEXT NULL,
    chain_id                    VARCHAR(128) NULL,
    sequence_no                 INT NULL,
    parent_evidence_id          VARCHAR(128) NULL,
    phase                       VARCHAR(128) NULL,
    weight                      DOUBLE NULL,
    confidence                  INT NULL,

    INDEX idx_subject_type (subject_type) USING INVERTED,
    INDEX idx_alert_id (alert_id) USING INVERTED,
    INDEX idx_case_id (case_id) USING INVERTED,
    INDEX idx_evidence_type (evidence_type) USING INVERTED,
    INDEX idx_event_id (event_id) USING INVERTED,
    INDEX idx_evidence_role (evidence_role) USING INVERTED,
    INDEX idx_evidence_time (evidence_time) USING INVERTED
)
UNIQUE KEY(tenant_id, evidence_id)
DISTRIBUTED BY HASH(tenant_id, evidence_id) BUCKETS 4
PROPERTIES (
    "enable_unique_key_merge_on_write" = "true",
    "replication_num" = "1",
    "bloom_filter_columns" = "evidence_id,alert_id,case_id,event_id",
    "inverted_index_storage_format" = "V3",
    "light_schema_change" = "true"
);
