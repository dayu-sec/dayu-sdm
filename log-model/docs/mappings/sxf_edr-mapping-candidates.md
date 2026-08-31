# sxf_edr 字段映射与枚举候选

候选结果，未经标准注册审批。样本字段为源目录级证据；只有 WPL 规则块字段被归属到具体 log_type。

## `cs_attack_alert_log`

- 状态：`candidate`
- 证据：`sample_inferred`
- WPL 规则：cs_attack_alert_log/adv_threat_log, cs_attack_alert_log/anti_bfa, cs_attack_alert_log/botnet, cs_attack_alert_log/webshell, cs_attack_alert_log/nofile_attack
- 样本：`s4-doris/models/wpl/sxf_edr/sample.dat`，目录级非空行 17

| 来源字段 | SDM 候选目标 | 转换/保留策略 | 证据 |
|---|---|---|---|
| `alert_describe` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `alert_level` | `severity` | `candidate_identity` | `sample_inferred` |
| `att_src` | `source_ip` | `candidate_identity` | `sample_inferred` |
| `att_times` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `current_process` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `details` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `domain_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `event_risk_level` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `event_type` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `file_md5` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `file_path` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `file_size` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `found_time` | `occur_time` | `candidate_identity` | `sample_inferred` |
| `host_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `iplist` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `module_file` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `parent_process` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `risk_type` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `serv_type` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `state` | `outcome` | `candidate_identity` | `sample_inferred` |
| `threat_file` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `threat_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `threat_process` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `threat_process_params` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `user` | `source_user` | `candidate_identity` | `sample_inferred` |

## `cs_malware_alert_log`

- 状态：`candidate`
- 证据：`sample_inferred`
- WPL 规则：virus_event
- 样本：`s4-doris/models/wpl/sxf_edr/sample.dat`，目录级非空行 17

| 来源字段 | SDM 候选目标 | 转换/保留策略 | 证据 |
|---|---|---|---|
| `agent_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `file_md5` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `file_path` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `file_size` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `found_time` | `occur_time` | `candidate_identity` | `sample_inferred` |
| `host_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `iplist` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `risk_level` | `severity` | `candidate_identity` | `sample_inferred` |
| `state` | `outcome` | `candidate_identity` | `sample_inferred` |
| `virus_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `virus_type` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |

## `sip_atk_alarm_log`

- 状态：`candidate`
- 证据：`sample_inferred`
- WPL 规则：sip_atk_alarm_log, sip_atk_alarm_log_v2
- 样本：`s4-doris/models/wpl/sxf_edr/sample.dat`，目录级非空行 17

| 来源字段 | SDM 候选目标 | 转换/保留策略 | 证据 |
|---|---|---|---|
| `alert_id` | `event_id` | `candidate_identity` | `sample_inferred` |
| `analyze_suggest` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `asset_direction` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `attack_asset_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `attack_branch_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `attack_branch_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `attack_classify1_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `attack_classify1_id_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `attack_classify_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `attack_country` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `attack_direction` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `attack_ip` | `source_ip` | `candidate_identity` | `sample_inferred` |
| `attack_port` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `attack_province` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `attack_state` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `attack_type` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `attack_type_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `brief` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `count` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `created_at` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `damage` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dev_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dev_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dev_name_ori` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `emergency` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `engine` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `event_desc` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `event_evidence` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `first_time` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `hash_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `hole_ids` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `invasion_stage` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `ioc` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `is_read` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `is_white` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `last_time` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `linkage_status` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `log_ids` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `mining_stage` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `misreport` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `module_type` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `module_type_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `multi_deal_status` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `net_action` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `principle` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `record_date` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `relation` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `reliability` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `status_code` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `sub_attack_type` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `sub_attack_type_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `suffer_asset_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `suffer_branch_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `suffer_branch_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `suffer_classify1_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `suffer_classify1_id_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `suffer_classify_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `suffer_country` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `suffer_ip` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `suffer_port` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `suffer_province` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `suggest` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `tags` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `updated_at` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `url` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `x_forwarded_for` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |

## `sip_sec_event_log`

- 状态：`candidate`
- 证据：`sample_inferred`
- WPL 规则：sip_sec_event_log, sip_sec_event_log_v2
- 样本：`s4-doris/models/wpl/sxf_edr/sample.dat`，目录级非空行 17

| 来源字段 | SDM 候选目标 | 转换/保留策略 | 证据 |
|---|---|---|---|
| `alert_ids` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `attack_state` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `branchId` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `branch_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `brief` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `classify1_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `classify_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `count` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `data_collection_time` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dealStatus` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `detectEngine` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dst_branch_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dst_branch_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dst_host` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dst_ip` | `target_ip` | `candidate_identity` | `sample_inferred` |
| `dst_mac_addr` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dst_port` | `target_port` | `candidate_identity` | `sample_inferred` |
| `email_from` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `email_to` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `emergency` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `eventKey` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `eventType` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `event_content` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `event_evidence` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `hostName` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `hostRisk` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `ip` | `source_ip` | `candidate_identity` | `sample_inferred` |
| `log_time` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `module_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `msg_sub_type` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `msg_type` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `multi_deal_status` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `principle` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `recordDate` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `role` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `ruleId` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `scan_count` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `server_sensative_directory` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `session_token` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `solution` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `src_branch_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `src_branch_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `src_host` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `src_ip` | `source_ip` | `candidate_identity` | `sample_inferred` |
| `src_mac_addr` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `src_port` | `source_port` | `candidate_identity` | `sample_inferred` |
| `stage` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `sub_attack_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `sub_attack_type` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `sub_attack_type_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `suspect_level` | `severity` | `candidate_identity` | `sample_inferred` |
| `tag` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `threat_level` | `severity` | `candidate_identity` | `sample_inferred` |
| `url` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |

