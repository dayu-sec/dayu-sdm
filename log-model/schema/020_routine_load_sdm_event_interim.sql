-- 中间版日志 Routine Load：Kafka sdm_s4_events -> sdm2_log.sdm_event
-- 使用 OFFSET_END，避免把旧表已经消费过的历史积压重新写入新版表。
-- 先以新任务名运行，确认落库后再决定是否扩大消费范围。

USE sdm2_log;

CREATE ROUTINE LOAD sdm_events_load_interim_raw_msg
ON sdm_event
COLUMNS(
    event_id_raw,
    log_id,
    source_original_event_id,
    occur_time_ms,
    tenant_id_raw,
    log_type,
    event_type,
    event_category_raw,
    source_ip,
    source_port,
    source_user,
    source_host,
    target_ip,
    target_user,
    target_host,
    target_port,
    target_domain,
    target_url_raw,
    target_file_path,
    target_file_sha256,
    http_method,
    http_status,
    http_referer,
    http_user_agent,
    carrier_protocol,
    carrier_process_name,
    carrier_process_pid,
    carrier_process_guid,
    carrier_process_path,
    carrier_process_cmdline,
    carrier_session_id,
    observer_product,
    source_alert_name,
    source_alert_severity,
    source_alert_category,
    source_alert_signature_id,
    source_alert_action,
    source_alert_original_id,
    operation,
    outcome,
    severity,
    k8s_pod_name,
    k8s_namespace,
    raw_msg,
    log_content_raw,
    roles_obj,
    facets_obj,
    source_finding_obj,
    extension,
    event_id = TRIM(event_id_raw),
    tenant_id = IF(tenant_id_raw IS NULL OR TRIM(tenant_id_raw) = '', '', TRIM(tenant_id_raw)),
    occur_time = FROM_UNIXTIME(IF(occur_time_ms >= 100000000000, occur_time_ms / 1000, occur_time_ms)),
    ingest_time = NOW(3),
    parse_time = NOW(3),
    schema_version = 1,
    mapping_id = 'interim.sdm_event.v1',
    event_domain = CASE LOWER(TRIM(event_category_raw))
        WHEN 'auth' THEN 'identity'
        WHEN 'identity' THEN 'identity'
        WHEN 'network' THEN 'network'
        WHEN 'audit' THEN 'audit'
        WHEN 'process' THEN 'audit'
        WHEN 'file' THEN 'audit'
        WHEN 'config' THEN 'audit'
        WHEN 'system' THEN 'system'
        WHEN 'alert' THEN 'security'
        ELSE 'other'
    END,
    record_kind = CASE
        WHEN source_alert_name IS NOT NULL AND TRIM(source_alert_name) != '' THEN 'finding'
        ELSE 'activity'
    END,
    log_content = log_content_raw,
    network_protocol = carrier_protocol,
    network_session_id = carrier_session_id,
    source_finding_title = source_alert_name,
    source_finding_severity = source_alert_severity,
    source_finding_category = source_alert_category,
    source_finding_signature_id = source_alert_signature_id,
    source_finding_action = source_alert_action,
    source_finding_original_id = source_alert_original_id,
    extensions_obj = extension
)
PROPERTIES (
    "format" = "json",
    "jsonpaths" = "[\"$.event_id\",\"$.log_id\",\"$.source_original_event_id\",\"$.occur_time\",\"$.tenant_id\",\"$.log_type\",\"$.event_type\",\"$.event_category\",\"$.source_ip\",\"$.source_port\",\"$.source_user\",\"$.source_host\",\"$.target_ip\",\"$.target_user\",\"$.target_host\",\"$.target_port\",\"$.target_domain\",\"$.target_url\",\"$.target_file_path\",\"$.target_file_sha256\",\"$.http_method\",\"$.http_status\",\"$.http_referer\",\"$.http_user_agent\",\"$.carrier_protocol\",\"$.carrier_process_name\",\"$.carrier_process_pid\",\"$.carrier_process_guid\",\"$.carrier_process_path\",\"$.carrier_process_cmdline\",\"$.carrier_session_id\",\"$.observer_product\",\"$.source_alert_name\",\"$.source_alert_severity\",\"$.source_alert_category\",\"$.source_alert_signature_id\",\"$.source_alert_action\",\"$.source_alert_original_id\",\"$.operation\",\"$.outcome\",\"$.severity\",\"$.k8s_pod_name\",\"$.k8s_namespace\",\"$.raw_msg\",\"$.log_content\",\"$.roles\",\"$.facets\",\"$.source_finding\",\"$.extension\"]",
    "strip_outer_array" = "false",
    "max_filter_ratio" = "0.1"
)
FROM KAFKA (
    "kafka_broker_list" = "10.106.129.101:9092",
    "kafka_topic" = "sdm_s4_events",
    "kafka_partitions" = "0",
    "kafka_offsets" = "OFFSET_END"
);
