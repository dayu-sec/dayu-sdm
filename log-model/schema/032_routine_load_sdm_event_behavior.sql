-- sdm_event_behavior Routine Load（M4）。
-- Kafka 消息形态：sdm_event_behavior 信封单对象 JSON（strip_outer_array=false）。
-- 时间：meta.occur_time / ingest_time / parse_time 为 unix 毫秒整数（与旧 hybrid-v1 通道一致，
-- 写手零改动）；本任务侧 FROM_UNIXTIME 转 DATETIME(3)，秒/毫秒自适应，缺失时 ingest/parse 取 NOW(3)。
--   逻辑契约（07 Schema / 样例 / 校验器）中 occur_time 仍是 datetime 语义——unix ms 是 Kafka 物理编码。
-- carrier_role：D6 标量投影，jsonpaths 直取 $.carriers[0].carrier_role。
-- Placeholders: __DORIS_DB__ __KAFKA_BROKERS__ __KAFKA_BEHAVIOR_TOPIC__ __KAFKA_PARTITIONS__ __KAFKA_OFFSETS__
-- T0 canary 验收项（真实 Kafka）：时间转换正确、拒绝率、lag 归零，见评审文档 §五。
-- 首次生产用 OFFSET_END；重放场景按 offset 步骤执行，勿直接 RESUME。
USE __DORIS_DB__;

CREATE ROUTINE LOAD sdm_event_behavior_load_v1
ON sdm_event_behavior
COLUMNS(
    tenant_id_raw,
    occur_time_ms,
    event_id_raw,
    ingest_time_ms,
    parse_time_ms,
    schema_version,
    mapping_id,
    vendor,
    product,
    data_source_category,
    collector_instance_id,
    log_id,
    log_type,
    log_name,
    log_level,
    record_kind,
    behavior_layer,
    behavior_type,
    behavior_operation,
    behavior_outcome,
    behavior_message,
    subject_ref_id,
    subject_entity_type,
    object_ref_id,
    object_entity_type,
    observer_ref_id,
    observer_entity_type,
    observation_action,
    assertion_title,
    assertion_rule,
    assertion_conclusion,
    assertion_severity,
    subject_detail,
    object_detail,
    carriers,
    carrier_role,
    facets,
    observation_detail,
    extensions,
    tenant_id = TRIM(tenant_id_raw),
    occur_time = FROM_UNIXTIME(IF(CAST(occur_time_ms AS DOUBLE) >= 100000000000, CAST(occur_time_ms AS DOUBLE) / 1000, CAST(occur_time_ms AS DOUBLE))),
    event_id = TRIM(event_id_raw),
    ingest_time = IF(ingest_time_ms IS NULL, NOW(3), FROM_UNIXTIME(IF(CAST(ingest_time_ms AS DOUBLE) >= 100000000000, CAST(ingest_time_ms AS DOUBLE) / 1000, CAST(ingest_time_ms AS DOUBLE)))),
    parse_time = IF(parse_time_ms IS NULL, NOW(3), FROM_UNIXTIME(IF(CAST(parse_time_ms AS DOUBLE) >= 100000000000, CAST(parse_time_ms AS DOUBLE) / 1000, CAST(parse_time_ms AS DOUBLE))))
)
PROPERTIES (
    "format" = "json",
    "jsonpaths" = '["$.meta.tenant_id", "$.meta.occur_time", "$.meta.event_id", "$.meta.ingest_time", "$.meta.parse_time", "$.meta.schema_version", "$.meta.mapping_id", "$.meta.data_source.vendor", "$.meta.data_source.product", "$.meta.data_source.category", "$.meta.data_source.instance_id", "$.meta.source_record.log_id", "$.meta.source_record.log_type", "$.meta.source_record.log_name", "$.meta.source_record.log_level", "$.meta.source_record.record_kind", "$.behavior.layer", "$.behavior.type", "$.behavior.operation", "$.behavior.outcome", "$.behavior.message", "$.subject.ref_id", "$.subject.entity_type", "$.object.ref_id", "$.object.entity_type", "$.observation.observer.ref_id", "$.observation.observer.entity_type", "$.observation.action", "$.observation.assertion.title", "$.observation.assertion.rule", "$.observation.assertion.conclusion", "$.observation.assertion.severity", "$.subject", "$.object", "$.carriers", "$.carriers[0].carrier_role", "$.facets", "$.observation", "$.extensions"]',
    "strip_outer_array" = "false",
    "max_filter_ratio" = "0.01",
    "timezone" = "Etc/UTC"
)
FROM KAFKA (
    "kafka_broker_list" = "__KAFKA_BROKERS__",
    "kafka_topic" = "__KAFKA_BEHAVIOR_TOPIC__",
    "kafka_partitions" = "__KAFKA_PARTITIONS__",
    "kafka_offsets" = "__KAFKA_OFFSETS__"
);
