-- 标准结构 Routine Load v2：Kafka 天擎标准事件 -> sdm2_log.sdm_event
-- 适配 process_creation/process_terminate.expected-sdm-event.json 结构（2026-08-05）
-- 时间约定（用户裁决 2026-08-05）：所有时间字段统一 Unix 毫秒，按 UTC 落库（timezone=Etc/UTC）
-- 与 020 的差异：jsonpaths 换标准结构字段名；时间不再 NOW(3)，直接用消息毫秒；
--   record_kind/event_domain/schema_version/mapping_id 用消息值，不再 CASE/固定。
-- 先以 OFFSET_END 跑通验收（021 同款 SQL 复用），确认后扩大消费范围。

USE sdm2_log;

CREATE ROUTINE LOAD sdm_events_load_standard_v2
ON sdm_event
COLUMNS(
    tenant_id_raw,
    occur_time_ms,
    event_id_raw,
    log_id,
    raw_msg,
    ingest_time_ms,
    parse_time_ms,
    schema_version,
    mapping_id,
    data_src_vendor,
    data_src_product,
    data_src_category,
    data_src_instance_id,
    log_type,
    log_name,
    source_original_event_id,
    record_kind,
    event_domain,
    event_type,
    operation,
    outcome,
    severity,
    source_host,
    observer_vendor,
    observer_product,
    roles_obj,
    facets_obj,
    source_finding_obj,
    extensions_obj,
    tenant_id = TRIM(tenant_id_raw),
    event_id = TRIM(event_id_raw),
    occur_time = FROM_UNIXTIME(IF(CAST(occur_time_ms AS DOUBLE) >= 100000000000, CAST(occur_time_ms AS DOUBLE) / 1000, CAST(occur_time_ms AS DOUBLE))),
    ingest_time = FROM_UNIXTIME(IF(CAST(ingest_time_ms AS DOUBLE) >= 100000000000, CAST(ingest_time_ms AS DOUBLE) / 1000, CAST(ingest_time_ms AS DOUBLE))),
    parse_time = FROM_UNIXTIME(IF(CAST(parse_time_ms AS DOUBLE) >= 100000000000, CAST(parse_time_ms AS DOUBLE) / 1000, CAST(parse_time_ms AS DOUBLE)))
)
PROPERTIES (
    "format" = "json",
    "jsonpaths" = "[\"$.tenant_id\",\"$.occur_time\",\"$.event_id\",\"$.log_id\",\"$.raw_msg\",\"$.ingest_time\",\"$.parse_time\",\"$.schema_version\",\"$.mapping_id\",\"$.data_src_vendor\",\"$.data_src_product\",\"$.data_src_category\",\"$.data_src_instance_id\",\"$.log_type\",\"$.log_name\",\"$.source_original_event_id\",\"$.record_kind\",\"$.event_domain\",\"$.event_type\",\"$.operation\",\"$.outcome\",\"$.severity\",\"$.source_host\",\"$.observer_vendor\",\"$.observer_product\",\"$.roles_obj\",\"$.facets_obj\",\"$.source_finding_obj\",\"$.extensions_obj\"]",
    "strip_outer_array" = "false",
    "max_filter_ratio" = "0.1",
    "timezone" = "Etc/UTC"
)
FROM KAFKA (
    "kafka_broker_list" = "10.106.129.101:9092",
    "kafka_topic" = "sdm_s4_events",
    "kafka_partitions" = "0",
    "kafka_offsets" = "OFFSET_END"
);
