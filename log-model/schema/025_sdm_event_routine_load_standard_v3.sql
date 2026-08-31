-- 标准结构 Routine Load v3：Kafka 天擎标准事件 -> sdm2_log.sdm_event
-- 与 023 v2 的差异：raw_msg 已拆分到 raw_log（006/024），本作业不再装载原文列。
-- 与 024（raw_log）消费同一 topic；两表身份同构，按 (tenant_id, occur_time, event_id) upsert。

USE sdm2_log;

CREATE ROUTINE LOAD sdm_events_load_standard_v3
ON sdm_event
COLUMNS(
    tenant_id_raw,
    occur_time_ms,
    event_id_raw,
    log_id,
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
    "jsonpaths" = "[\"$.tenant_id\",\"$.occur_time\",\"$.event_id\",\"$.log_id\",\"$.ingest_time\",\"$.parse_time\",\"$.schema_version\",\"$.mapping_id\",\"$.data_src_vendor\",\"$.data_src_product\",\"$.data_src_category\",\"$.data_src_instance_id\",\"$.log_type\",\"$.log_name\",\"$.source_original_event_id\",\"$.record_kind\",\"$.event_domain\",\"$.event_type\",\"$.operation\",\"$.outcome\",\"$.severity\",\"$.source_host\",\"$.observer_vendor\",\"$.observer_product\",\"$.roles_obj\",\"$.facets_obj\",\"$.source_finding_obj\",\"$.extensions_obj\"]",
    "strip_outer_array" = "false",
    "max_filter_ratio" = "0.1",
    "max_error_number" = "10000",
    "timezone" = "Etc/UTC"
)
FROM KAFKA (
    "kafka_broker_list" = "10.106.129.101:9092",
    "kafka_topic" = "sdm_s4_events",
    "kafka_partitions" = "0",
    "kafka_offsets" = "OFFSET_END"
);
