-- raw_log Routine Load：Kafka 天擎标准事件原文 -> sdm2_log.raw_log
-- 与 025（sdm_event v3）消费同一 topic，双表并行写入，身份同构保证 upsert 一致。
-- digest 由上游 wparse 计算后随消息写入（$.raw_msg_digest，sha256 十六进制小写），
-- 本作业不重算，仅透传。
-- 先以 OFFSET_END 跑通验收，确认后扩大消费范围。

USE sdm2_log;

CREATE ROUTINE LOAD sdm_raw_logs_load
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
