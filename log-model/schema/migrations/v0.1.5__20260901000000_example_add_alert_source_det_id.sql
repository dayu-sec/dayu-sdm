-- Migration v0.1.5: example — adds a nullable provenance column to sdm_alert.
-- Contract: every migration MUST be idempotent/re-entrant (script may replay
-- it after partial failure or across skipped versions).
-- Version prefix (v0.1.5) drives preflight pending-detection via sort -V.
USE sdm2_log;

ALTER TABLE sdm_alert
    ADD COLUMN IF NOT EXISTS source_det_id VARCHAR(128) NULL
    COMMENT "来源侧检测记录 ID（SOURCE_ALERT 路径回填）";
