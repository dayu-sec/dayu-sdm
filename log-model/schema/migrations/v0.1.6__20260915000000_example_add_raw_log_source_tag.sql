-- Migration v0.1.6: example — raw_log source tag.
-- Idempotency contract applies (re-entrant on replay/force).
USE sdm2_log;

ALTER TABLE raw_log
    ADD COLUMN IF NOT EXISTS source_tag VARCHAR(64) NULL
    COMMENT "来源侧标签（示例迁移列）";
