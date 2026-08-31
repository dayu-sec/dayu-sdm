-- Analysis citations. evidence_id is tenant-unique; evidence_subject_type
-- plus alert_id/case_id are a frozen pointer to the evidence subject at
-- cite time (ADR-012 / ADR-014). Same XOR as sdm_evidence.

CREATE TABLE IF NOT EXISTS sdm2_log.sdm_analysis_citation (
    tenant_id                VARCHAR(128) NOT NULL,
    analysis_id              VARCHAR(128) NOT NULL,
    evidence_id              VARCHAR(128) NOT NULL,
    evidence_subject_type    VARCHAR(32) NOT NULL,
    alert_id                 VARCHAR(128) NULL,
    case_id                  VARCHAR(128) NULL,
    evidence_type            VARCHAR(64) NULL,
    evidence_role            VARCHAR(64) NULL,
    event_id                 VARCHAR(128) NULL,
    external_ref             VARCHAR(255) NULL,
    evidence_summary         TEXT NULL,
    cited_time               DATETIME(3) NOT NULL,

    INDEX idx_evidence_id (evidence_id) USING INVERTED,
    INDEX idx_evidence_subject_type (evidence_subject_type) USING INVERTED,
    INDEX idx_alert_id (alert_id) USING INVERTED,
    INDEX idx_case_id (case_id) USING INVERTED,
    INDEX idx_event_id (event_id) USING INVERTED
)
UNIQUE KEY(tenant_id, analysis_id, evidence_id)
DISTRIBUTED BY HASH(tenant_id, analysis_id) BUCKETS 4
PROPERTIES (
    "enable_unique_key_merge_on_write" = "true",
    "replication_num" = "1",
    "bloom_filter_columns" = "analysis_id,evidence_id,alert_id,case_id",
    "inverted_index_storage_format" = "V3",
    "light_schema_change" = "true"
);
