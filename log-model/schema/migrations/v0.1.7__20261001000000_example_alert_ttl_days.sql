-- Migration v0.1.7: example — alert retention hint.
USE sdm2_log;

ALTER TABLE sdm_alert
    ADD COLUMN IF NOT EXISTS ttl_days INT NULL
    COMMENT "告警保留天数提示（示例迁移列）";
