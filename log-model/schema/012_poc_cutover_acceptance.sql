-- [HISTORICAL] ldm_alert no longer exists in current deliverables (feature/sdm2-alert-model);
-- acceptance queries below are kept as executed history.
-- POC 中间版结构验收。

SHOW CREATE TABLE sdm2_log.sdm_event;
SHOW CREATE TABLE sdm2_log.ldm_alert;

SELECT COUNT(*) AS new_event_row_count FROM sdm2_log.sdm_event;
SELECT COUNT(*) AS legacy_event_row_count FROM sdm2_log.sdm_event_legacy_20260804;
SELECT COUNT(*) AS ldm_alert_row_count FROM sdm2_log.ldm_alert;

SELECT TABLE_NAME, TABLE_TYPE
FROM information_schema.tables
WHERE TABLE_SCHEMA = 'sdm2_log'
  AND TABLE_NAME IN ('sdm_event', 'sdm_event_legacy_20260804', 'ldm_alert');
