-- 028_routine_load_sdm_alert.sql: Routine Load for sdm_alert.
-- 从现场 RL 沉淀（告警三表，字段与 DDL 对齐）。
-- __KAFKA_BROKERS__ / __KAFKA_OFFSETS__ 由 apply_prod_schema.sh 注入；topic=sdm_alert 固定。
-- 时间：Unix 毫秒/秒自适应，timezone=Etc/UTC（与 145 行为表写入一致），num_as_string=true。

CREATE ROUTINE LOAD sdm_alert_load_v1 ON sdm_alert
WITH APPEND
COLUMNS(
  tenant_id_raw, alert_id_raw, created_time_raw, alert_display_id,
  source_alert_id, source_product, alert_name, description, alert_type,
  category_code, event_count, severity, detection_confidence, detection_risk_score,
  workflow_status, verdict, closed_time_raw, updated_time_raw, first_seen_raw, last_seen_raw,
  rule_id, rule_name, rule_version, rule_type, detection_engine, dedup_key, merge_id,
  correlation_id, case_id, primary_entity_id, primary_entity_type, primary_entity_value,
  primary_entity_role, primary_tactic_id, primary_technique_id, latest_analysis_id,
  latest_analysis_conclusion, latest_analysis_confidence, latest_analysis_summary,
  latest_analysis_time_raw, assignee_id, ticket_id, extensions,
  tenant_id=trim(tenant_id_raw), alert_id=trim(alert_id_raw),
  created_time=from_unixtime(cast(if(cast(created_time_raw AS double) >= 100000000000, cast(created_time_raw AS double) / 1000, cast(created_time_raw AS double)) AS decimal(18,6))),
  closed_time=from_unixtime(cast(if(cast(closed_time_raw AS double) >= 100000000000, cast(closed_time_raw AS double) / 1000, cast(closed_time_raw AS double)) AS decimal(18,6))),
  updated_time=from_unixtime(cast(if(cast(updated_time_raw AS double) >= 100000000000, cast(updated_time_raw AS double) / 1000, cast(updated_time_raw AS double)) AS decimal(18,6))),
  first_seen=from_unixtime(cast(if(cast(first_seen_raw AS double) >= 100000000000, cast(first_seen_raw AS double) / 1000, cast(first_seen_raw AS double)) AS decimal(18,6))),
  last_seen=from_unixtime(cast(if(cast(last_seen_raw AS double) >= 100000000000, cast(last_seen_raw AS double) / 1000, cast(last_seen_raw AS double)) AS decimal(18,6))),
  latest_analysis_time=from_unixtime(cast(if(cast(latest_analysis_time_raw AS double) >= 100000000000, cast(latest_analysis_time_raw AS double) / 1000, cast(latest_analysis_time_raw AS double)) AS decimal(18,6)))
)
PROPERTIES(
  "desired_concurrent_number"="1", "max_error_number"="10000", "max_filter_ratio"="1.0",
  "max_batch_interval"="10", "max_batch_rows"="200000", "max_batch_size"="104857600",
  "format"="json",
  "jsonpaths"="[\"$.tenant_id\",\"$.alert_id\",\"$.created_time\",\"$.alert_display_id\",\"$.source_alert_id\",\"$.source_product\",\"$.alert_name\",\"$.description\",\"$.alert_type\",\"$.category_code\",\"$.event_count\",\"$.severity\",\"$.detection_confidence\",\"$.detection_risk_score\",\"$.workflow_status\",\"$.verdict\",\"$.closed_time\",\"$.updated_time\",\"$.first_seen\",\"$.last_seen\",\"$.rule_id\",\"$.rule_name\",\"$.rule_version\",\"$.rule_type\",\"$.detection_engine\",\"$.dedup_key\",\"$.merge_id\",\"$.correlation_id\",\"$.case_id\",\"$.primary_entity_id\",\"$.primary_entity_type\",\"$.primary_entity_value\",\"$.primary_entity_role\",\"$.primary_tactic_id\",\"$.primary_technique_id\",\"$.latest_analysis_id\",\"$.latest_analysis_conclusion\",\"$.latest_analysis_confidence\",\"$.latest_analysis_summary\",\"$.latest_analysis_time\",\"$.assignee_id\",\"$.ticket_id\",\"$.extensions\"]",
  "strip_outer_array"="false", "num_as_string"="true", "strict_mode"="false",
  "timezone"="Etc/UTC", "exec_mem_limit"="2147483648"
)
FROM KAFKA(
  "kafka_broker_list"="__KAFKA_BROKERS__", "kafka_topic"="sdm_alert",
  "property.group.id"="sdm_alert_load_v1", "property.kafka_default_offsets"="__KAFKA_OFFSETS__"
);
