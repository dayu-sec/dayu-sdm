-- 029_routine_load_sdm_evidence.sql: Routine Load for sdm_evidence.
-- 从现场 RL 沉淀（告警三表，字段与 DDL 对齐）。
-- __KAFKA_BROKERS__ / __KAFKA_OFFSETS__ 由 apply_prod_schema.sh 注入；topic=sdm_evidence 固定。
-- 时间：Unix 毫秒/秒自适应，timezone=Etc/UTC（与 145 行为表写入一致），num_as_string=true。

CREATE ROUTINE LOAD sdm_evidence_load_v1 ON sdm_evidence
WITH APPEND
COLUMNS(
  tenant_id_raw, evidence_id_raw, subject_type, alert_id, case_id,
  evidence_time_raw, event_occur_time_raw, evidence_type, event_id, log_id,
  raw_log_id, source_alert_original_id, external_ref, evidence_payload_ref,
  evidence_role, event_type, evidence_summary, chain_id, sequence_no,
  parent_evidence_id, phase, weight, confidence,
  tenant_id=trim(tenant_id_raw), evidence_id=trim(evidence_id_raw),
  evidence_time=from_unixtime(cast(if(cast(evidence_time_raw AS double) >= 100000000000, cast(evidence_time_raw AS double) / 1000, cast(evidence_time_raw AS double)) AS decimal(18,6))),
  event_occur_time=from_unixtime(cast(if(cast(event_occur_time_raw AS double) >= 100000000000, cast(event_occur_time_raw AS double) / 1000, cast(event_occur_time_raw AS double)) AS decimal(18,6)))
)
PROPERTIES(
  "desired_concurrent_number"="1", "max_error_number"="10000", "max_filter_ratio"="1.0",
  "max_batch_interval"="10", "max_batch_rows"="200000", "max_batch_size"="104857600",
  "format"="json",
  "jsonpaths"="[\"$.tenant_id\",\"$.evidence_id\",\"$.subject_type\",\"$.alert_id\",\"$.case_id\",\"$.evidence_time\",\"$.event_occur_time\",\"$.evidence_type\",\"$.event_id\",\"$.log_id\",\"$.raw_log_id\",\"$.source_alert_original_id\",\"$.external_ref\",\"$.evidence_payload_ref\",\"$.evidence_role\",\"$.event_type\",\"$.evidence_summary\",\"$.chain_id\",\"$.sequence_no\",\"$.parent_evidence_id\",\"$.phase\",\"$.weight\",\"$.confidence\"]",
  "strip_outer_array"="false", "num_as_string"="true", "strict_mode"="false",
  "timezone"="Etc/UTC", "exec_mem_limit"="2147483648"
)
FROM KAFKA(
  "kafka_broker_list"="__KAFKA_BROKERS__", "kafka_topic"="sdm_evidence",
  "property.group.id"="sdm_evidence_load_v1", "property.kafka_default_offsets"="__KAFKA_OFFSETS__"
);
