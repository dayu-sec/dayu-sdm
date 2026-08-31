USE sdm2_log;

SHOW ROUTINE LOAD FOR sdm_events_load_interim_raw_msg;

SELECT COUNT(*) AS event_rows,
       MIN(occur_time) AS min_occur_time,
       MAX(occur_time) AS max_occur_time
FROM sdm_event;

SELECT event_id, tenant_id, mapping_id, schema_version,
       record_kind, event_domain, event_type, log_id
FROM sdm_event
ORDER BY occur_time DESC
LIMIT 10;
