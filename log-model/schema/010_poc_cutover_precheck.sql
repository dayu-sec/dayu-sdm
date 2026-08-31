-- POC 切换前只读检查。

SELECT COUNT(*) AS legacy_row_count,
       MIN(occur_time) AS legacy_min_occur_time,
       MAX(occur_time) AS legacy_max_occur_time
FROM sdm2_log.sdm_event;

SHOW ROUTINE LOAD FOR sdm_events_load;

SHOW FULL TABLES FROM sdm2_log;

SELECT TABLE_NAME, VIEW_DEFINITION
FROM information_schema.views
WHERE TABLE_SCHEMA = 'sdm2_log'
  AND LOWER(VIEW_DEFINITION) LIKE '%sdm_event%';
