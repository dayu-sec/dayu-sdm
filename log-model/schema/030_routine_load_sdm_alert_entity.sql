-- 030_routine_load_sdm_alert_entity.sql: Routine Load for sdm_alert_entity.
-- 从现场 RL 沉淀（告警三表，字段与 DDL 对齐）。
-- __KAFKA_BROKERS__ / __KAFKA_OFFSETS__ 由 apply_prod_schema.sh 注入；topic=sdm_alert_entity 固定。
-- 时间：Unix 毫秒/秒自适应，timezone=Etc/UTC（与 145 行为表写入一致），num_as_string=true。

CREATE ROUTINE LOAD sdm_alert_entity_load_v1 ON sdm_alert_entity
WITH APPEND
COLUMNS(
  tenant_id_raw, alert_id_raw, entity_id_raw, alert_entity_role_raw,
  created_time_raw, entity_type, event_role_hint, entity_value, is_primary,
  asset_id, asset_name, asset_type, used_for_grouping, grouping_weight, valid_until_raw, risk_context,
  tenant_id=trim(tenant_id_raw), alert_id=trim(alert_id_raw),
  entity_id=trim(entity_id_raw), alert_entity_role=trim(alert_entity_role_raw),
  created_time=from_unixtime(cast(if(cast(created_time_raw AS double) >= 100000000000, cast(created_time_raw AS double) / 1000, cast(created_time_raw AS double)) AS decimal(18,6))),
  valid_until=from_unixtime(cast(if(cast(valid_until_raw AS double) >= 100000000000, cast(valid_until_raw AS double) / 1000, cast(valid_until_raw AS double)) AS decimal(18,6)))
)
PROPERTIES(
  "desired_concurrent_number"="1", "max_error_number"="10000", "max_filter_ratio"="1.0",
  "max_batch_interval"="10", "max_batch_rows"="200000", "max_batch_size"="104857600",
  "format"="json",
  "jsonpaths"="[\"$.tenant_id\",\"$.alert_id\",\"$.entity_id\",\"$.alert_entity_role\",\"$.created_time\",\"$.entity_type\",\"$.event_role_hint\",\"$.entity_value\",\"$.is_primary\",\"$.asset_id\",\"$.asset_name\",\"$.asset_type\",\"$.used_for_grouping\",\"$.grouping_weight\",\"$.valid_until\",\"$.risk_context\"]",
  "strip_outer_array"="false", "num_as_string"="true", "strict_mode"="false",
  "timezone"="Etc/UTC", "exec_mem_limit"="2147483648"
)
FROM KAFKA(
  "kafka_broker_list"="__KAFKA_BROKERS__", "kafka_topic"="sdm_alert_entity",
  "property.group.id"="sdm_alert_entity_load_v1", "property.kafka_default_offsets"="__KAFKA_OFFSETS__"
);
