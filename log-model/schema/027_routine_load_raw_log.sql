-- Kafka hybrid-v1 原文 -> sdm2_log.raw_log
-- 与 026（sdm_event hybrid-v1）消费同一 topic；两表身份同构，按 (tenant_id, occur_time, event_id) upsert。
-- digest 由上游 wparse 计算后随消息写入（$.raw_msg_digest，sha256 十六进制小写），本作业不重算。
-- Placeholders: __DORIS_DB__ __KAFKA_BROKERS__ __KAFKA_TOPIC__ __KAFKA_OFFSETS__
-- 首次生产用 OFFSET_END。

USE __DORIS_DB__;

CREATE ROUTINE LOAD sdm_raw_logs_load_hybrid_v1
ON raw_log
COLUMNS(
    tenant_id_raw,
    occur_time_ms,
    event_id_raw,
    raw_msg,
    raw_msg_digest,
    tenant_id = TRIM(tenant_id_raw),
    event_id = TRIM(event_id_raw),
    occur_time = FROM_UNIXTIME(IF(CAST(occur_time_ms AS DOUBLE) >= 100000000000, CAST(occur_time_ms AS DOUBLE) / 1000, CAST(occur_time_ms AS DOUBLE))),
    digest_algo = 'sha256'
)
PROPERTIES (
    "format" = "json",
    "jsonpaths" = "[\"$.tenant_id\",\"$.occur_time\",\"$.event_id\",\"$.raw_msg\",\"$.raw_msg_digest\"]",
    "strip_outer_array" = "false",
    "max_filter_ratio" = "1",
    "max_error_number" = "1000000000",
    "timezone" = "Etc/UTC"
)
FROM KAFKA (
    "kafka_broker_list" = "__KAFKA_BROKERS__",
    "kafka_topic" = "__KAFKA_TOPIC__",
    "kafka_partitions" = "__KAFKA_PARTITIONS__",
    "kafka_offsets" = "__KAFKA_OFFSETS__"
);
