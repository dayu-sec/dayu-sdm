# tianqing 字段映射与枚举候选

候选结果，未经标准注册审批。样本字段为源目录级证据；只有 WPL 规则块字段被归属到具体 log_type。

## `cs_op_log`

- 状态：`reused_and_reviewed`
- 证据：`vendor_confirmed_and_observed`
- WPL 规则：cs_op_log
- 样本：`s4-doris/models/wpl/tianqing/sample.dat`，目录级非空行 54

| 来源字段 | SDM 候选目标 | 转换/保留策略 | 证据 |
|---|---|---|---|
| `asset_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `asset_oid` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `client_ip` | `source_ip` | `candidate_identity` | `vendor_confirmed_and_observed` |
| `create_time` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `entity_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `op_level` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `op_type` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `operator` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `operator_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `path` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `status` | `outcome` | `candidate_identity` | `vendor_confirmed_and_observed` |

开放问题：
- 已有天擎 examples 映射包（目录 edr_cs_op_log）；本目录仅记录复核状态，不重复生成样例

## `edr_account_change`

- 状态：`reused_and_reviewed`
- 证据：`vendor_confirmed_and_observed`
- WPL 规则：edr_account_change
- 样本：`s4-doris/models/wpl/tianqing/sample.dat`，目录级非空行 54

| 来源字段 | SDM 候选目标 | 转换/保留策略 | 证据 |
|---|---|---|---|
| `account_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `account_user` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `asset_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `asset_oid` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `client_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `client_info` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `client_ip` | `source_ip` | `candidate_identity` | `vendor_confirmed_and_observed` |
| `client_report_ip` | `source_ip` | `candidate_identity` | `vendor_confirmed_and_observed` |
| `computer_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `create_time` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `custom_group_paths` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `env_version` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `event_date_creation` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `event_type` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `gid` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `group_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `hostname` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `ip` | `source_ip` | `candidate_identity` | `vendor_confirmed_and_observed` |
| `logger` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `mac` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `mid` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `payload` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `pid` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `process_command_line` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `process_guid` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `process_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `process_internal_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `process_md5` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `process_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `process_original_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `process_parent_command_line` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `process_parent_internal_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `process_parent_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `process_parent_original_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `process_parent_path` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `process_parent_sign` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `process_path` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `process_sha1` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `process_sign` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `process_user` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `report_ip` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `sub_task_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `task_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `timestamp` | `occur_time` | `candidate_identity` | `vendor_confirmed_and_observed` |
| `type` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `uuid` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |

枚举/选择器信号：
- 字段 `type`（has）；候选值 account_change；未知值策略：`preserve_raw_and_report`

开放问题：
- 已有天擎 examples 映射包（目录 edr_account_change）；本目录仅记录复核状态，不重复生成样例

## `edr_alert_log`

- 状态：`reused_and_reviewed`
- 证据：`vendor_confirmed_and_observed`
- WPL 规则：edr_alert_log
- 样本：`s4-doris/models/wpl/tianqing/sample.dat`，目录级非空行 54

| 来源字段 | SDM 候选目标 | 转换/保留策略 | 证据 |
|---|---|---|---|
| `alert_id` | `event_id` | `candidate_identity` | `vendor_confirmed_and_observed` |
| `alert_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `asset_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `asset_oid` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `category_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `client_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `client_login_user` | `source_user` | `candidate_identity` | `vendor_confirmed_and_observed` |
| `compromise_status_cd` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `computer_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `custom_group_paths` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `description` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `gid` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `group_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `ioc_alerts` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `ioc_value` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `ip` | `source_ip` | `candidate_identity` | `vendor_confirmed_and_observed` |
| `log_type` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `mac` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `malicious_family` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `malicious_type` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `mid` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `origin_killchain` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `other_type` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `process_details` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `protocol` | `protocol` | `candidate_identity` | `vendor_confirmed_and_observed` |
| `report_ip` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `risky_source` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `rule_id` | `event_id` | `candidate_identity` | `vendor_confirmed_and_observed` |
| `severity` | `severity` | `candidate_identity` | `vendor_confirmed_and_observed` |
| `status` | `outcome` | `candidate_identity` | `vendor_confirmed_and_observed` |
| `tactic` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `technique` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |

枚举/选择器信号：
- 字段 `type`（has）；候选值 edr_alert；未知值策略：`preserve_raw_and_report`

开放问题：
- 已有天擎 examples 映射包（目录 edr_alert_log）；本目录仅记录复核状态，不重复生成样例

## `edr_antivirus_scan`

- 状态：`reused_and_reviewed`
- 证据：`vendor_confirmed_and_observed`
- WPL 规则：edr_antivirus_scan
- 样本：`s4-doris/models/wpl/tianqing/sample.dat`，目录级非空行 54

| 来源字段 | SDM 候选目标 | 转换/保留策略 | 证据 |
|---|---|---|---|
| `activation` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `build_version` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `client_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `client_info` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `computer_working_group` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `core_number` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `create_time` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `describe` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `domain` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `file_alarm_time` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `file_create_time` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `file_path` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `group_info` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `guid` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `ie_version` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `login_account` | `source_user` | `candidate_identity` | `vendor_confirmed_and_observed` |
| `mac` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `main` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `md5` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `memory_size` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `mid` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `name` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `need_reboot` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `nic_list` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `node_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `node_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `node_type` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `oid` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `os` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `os_bit` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `release_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `report_ip` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `report_ipv6` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `result` | `outcome` | `candidate_identity` | `vendor_confirmed_and_observed` |
| `scan_type` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `scanners` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `sha1` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `start_time` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `state` | `outcome` | `candidate_identity` | `vendor_confirmed_and_observed` |
| `sys_space` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `system_language` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `tree_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `trigger_mode` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `update_time` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `virus_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `virus_type` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |

枚举/选择器信号：
- 字段 `syslog_topic`（has）；候选值 antivirus_scan；未知值策略：`preserve_raw_and_report`

开放问题：
- 已有天擎 examples 映射包（目录 edr_antivirus_scan）；本目录仅记录复核状态，不重复生成样例

## `edr_antivirus_virus`

- 状态：`reused_and_reviewed`
- 证据：`vendor_confirmed_and_observed`
- WPL 规则：edr_antivirus_virus
- 样本：`s4-doris/models/wpl/tianqing/sample.dat`，目录级非空行 54

| 来源字段 | SDM 候选目标 | 转换/保留策略 | 证据 |
|---|---|---|---|
| `activation` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `build_version` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `client_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `client_info` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `computer_working_group` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `core_number` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `create_time` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `describe` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `domain` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `file_create_time` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `file_path` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `group_info` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `guid` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `ie_version` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `login_account` | `source_user` | `candidate_identity` | `vendor_confirmed_and_observed` |
| `mac` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `main` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `md5` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `memory_size` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `mid` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `name` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `need_reboot` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `nic_list` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `node_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `node_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `node_type` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `oid` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `os` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `os_bit` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `release_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `report_ip` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `report_ipv6` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `result` | `outcome` | `candidate_identity` | `vendor_confirmed_and_observed` |
| `scanners` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `severity` | `severity` | `candidate_identity` | `vendor_confirmed_and_observed` |
| `sha1` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `state` | `outcome` | `candidate_identity` | `vendor_confirmed_and_observed` |
| `sys_space` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `system_language` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `tree_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `trigger_mode` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `update_time` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `virus_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `virus_type` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |

枚举/选择器信号：
- 字段 `syslog_topic`（has）；候选值 antivirus_virus；未知值策略：`preserve_raw_and_report`

开放问题：
- 已有天擎 examples 映射包（目录 edr_antivirus_virus）；本目录仅记录复核状态，不重复生成样例

## `edr_attack_protection`

- 状态：`reused_and_reviewed`
- 证据：`vendor_confirmed_and_observed`
- WPL 规则：edr_attack_protection
- 样本：`s4-doris/models/wpl/tianqing/sample.dat`，目录级非空行 54

| 来源字段 | SDM 候选目标 | 转换/保留策略 | 证据 |
|---|---|---|---|
| `activation` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `attack_time` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `attack_type` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `build_version` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `client_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `client_info` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `computer_working_group` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `core_number` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `create_time` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `describe` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `domain` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `file_alarm_time` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `file_create_time` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `file_path` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `group_info` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `guid` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `ie_version` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `login_account` | `source_user` | `candidate_identity` | `vendor_confirmed_and_observed` |
| `mac` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `main` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `md5` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `memory_size` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `mid` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `name` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `need_reboot` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `nic_list` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `node_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `node_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `node_type` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `oid` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `os` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `os_bit` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `release_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `report_ip` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `report_ipv6` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `result` | `outcome` | `candidate_identity` | `vendor_confirmed_and_observed` |
| `scanners` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `sha1` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `state` | `outcome` | `candidate_identity` | `vendor_confirmed_and_observed` |
| `sys_space` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `system_language` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `tree_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `trigger_mode` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `update_time` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `virus_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `virus_type` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |

枚举/选择器信号：
- 字段 `syslog_topic`（has）；候选值 attack_protection_log；未知值策略：`preserve_raw_and_report`

开放问题：
- 已有天擎 examples 映射包（目录 edr_attack_protection）；本目录仅记录复核状态，不重复生成样例

## `edr_baseline_check_detail`

- 状态：`reused_and_reviewed`
- 证据：`vendor_confirmed_and_observed`
- WPL 规则：edr_baseline_check_detail
- 样本：`s4-doris/models/wpl/tianqing/sample.dat`，目录级非空行 54

| 来源字段 | SDM 候选目标 | 转换/保留策略 | 证据 |
|---|---|---|---|
| `activation` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `build_version` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `client_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `client_info` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `computer_working_group` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `core_number` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `create_time` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `describe` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `domain` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `file_alarm_time` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `file_create_time` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `file_path` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `group_info` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `guid` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `ie_version` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `login_account` | `source_user` | `candidate_identity` | `vendor_confirmed_and_observed` |
| `mac` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `main` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `md5` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `memory_size` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `mid` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `name` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `need_reboot` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `nic_list` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `node_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `node_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `node_type` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `oid` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `os` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `os_bit` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `release_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `report_ip` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `report_ipv6` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `result` | `outcome` | `candidate_identity` | `vendor_confirmed_and_observed` |
| `scanners` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `sha1` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `state` | `outcome` | `candidate_identity` | `vendor_confirmed_and_observed` |
| `sys_space` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `system_language` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `tree_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `trigger_mode` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `update_time` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `virus_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `virus_type` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |

枚举/选择器信号：
- 字段 `syslog_topic`（has）；候选值 baseline_check_detail；未知值策略：`preserve_raw_and_report`

开放问题：
- 已有天擎 examples 映射包（目录 edr_baseline_check_detail）；本目录仅记录复核状态，不重复生成样例

## `edr_baseline_check_result`

- 状态：`reused_and_reviewed`
- 证据：`vendor_confirmed_and_observed`
- WPL 规则：edr_baseline_check_result
- 样本：`s4-doris/models/wpl/tianqing/sample.dat`，目录级非空行 54

| 来源字段 | SDM 候选目标 | 转换/保留策略 | 证据 |
|---|---|---|---|
| `activation` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `build_version` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `client_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `client_info` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `computer_working_group` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `core_number` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `create_time` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `describe` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `domain` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `file_alarm_time` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `file_create_time` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `file_path` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `group_info` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `guid` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `ie_version` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `login_account` | `source_user` | `candidate_identity` | `vendor_confirmed_and_observed` |
| `mac` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `main` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `md5` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `memory_size` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `mid` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `name` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `need_reboot` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `nic_list` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `node_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `node_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `node_type` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `oid` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `op` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `os` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `os_bit` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `release_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `report_ip` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `report_ipv6` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `result` | `outcome` | `candidate_identity` | `vendor_confirmed_and_observed` |
| `scanners` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `sha1` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `state` | `outcome` | `candidate_identity` | `vendor_confirmed_and_observed` |
| `sys_space` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `system_language` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `tree_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `trigger_mode` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `update_time` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `virus_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `virus_type` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |

枚举/选择器信号：
- 字段 `syslog_topic`（has）；候选值 baseline_check_result；未知值策略：`preserve_raw_and_report`

开放问题：
- 已有天擎 examples 映射包（目录 edr_baseline_check_result）；本目录仅记录复核状态，不重复生成样例

## `edr_energy_manage_log`

- 状态：`reused_and_reviewed`
- 证据：`vendor_confirmed_and_observed`
- WPL 规则：edr_energy_manage_log
- 样本：`s4-doris/models/wpl/tianqing/sample.dat`，目录级非空行 54

| 来源字段 | SDM 候选目标 | 转换/保留策略 | 证据 |
|---|---|---|---|
| `action` | `outcome` | `candidate_identity` | `vendor_confirmed_and_observed` |
| `activation` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `build_version` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `client_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `client_info` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `computer_working_group` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `core_number` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `create_time` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `describe` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `domain` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `file_alarm_time` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `file_create_time` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `file_path` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `group_info` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `guid` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `ie_version` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `login_account` | `source_user` | `candidate_identity` | `vendor_confirmed_and_observed` |
| `mac` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `main` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `md5` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `memory_size` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `mid` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `name` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `need_reboot` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `nic_list` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `node_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `node_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `node_type` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `oid` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `os` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `os_bit` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `release_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `report_ip` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `report_ipv6` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `result` | `outcome` | `candidate_identity` | `vendor_confirmed_and_observed` |
| `scanners` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `sha1` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `state` | `outcome` | `candidate_identity` | `vendor_confirmed_and_observed` |
| `sys_space` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `system_language` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `tree_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `trigger_mode` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `update_time` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `virus_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `virus_type` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |

枚举/选择器信号：
- 字段 `syslog_topic`（has）；候选值 energy_manage_log；未知值策略：`preserve_raw_and_report`

开放问题：
- 已有天擎 examples 映射包（目录 edr_energy_manage_log）；本目录仅记录复核状态，不重复生成样例

## `edr_external_device_alarm`

- 状态：`reused_and_reviewed`
- 证据：`vendor_confirmed_and_observed`
- WPL 规则：edr_external_device_alarm
- 样本：`s4-doris/models/wpl/tianqing/sample.dat`，目录级非空行 54

| 来源字段 | SDM 候选目标 | 转换/保留策略 | 证据 |
|---|---|---|---|
| `action` | `outcome` | `candidate_identity` | `vendor_confirmed_and_observed` |
| `activation` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `build_version` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `client_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `client_info` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `computer_working_group` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `core_number` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `create_time` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `describe` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `domain` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `file_alarm_time` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `file_create_time` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `file_path` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `group_info` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `guid` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `host_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `ie_version` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `login_account` | `source_user` | `candidate_identity` | `vendor_confirmed_and_observed` |
| `mac` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `main` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `md5` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `memory_size` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `mid` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `name` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `need_reboot` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `nic_list` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `node_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `node_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `node_type` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `oid` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `os` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `os_bit` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `release_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `report_ip` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `report_ipv6` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `result` | `outcome` | `candidate_identity` | `vendor_confirmed_and_observed` |
| `scanners` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `sha1` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `state` | `outcome` | `candidate_identity` | `vendor_confirmed_and_observed` |
| `sys_space` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `system_language` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `tree_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `trigger_mode` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `update_time` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `virus_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `virus_type` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |

枚举/选择器信号：
- 字段 `syslog_topic`（has）；候选值 external_device_alarm；未知值策略：`preserve_raw_and_report`

开放问题：
- 已有天擎 examples 映射包（目录 edr_external_device_alarm）；本目录仅记录复核状态，不重复生成样例

## `edr_file_audit`

- 状态：`reused_and_reviewed`
- 证据：`vendor_confirmed_and_observed`
- WPL 规则：edr_file_audit
- 样本：`s4-doris/models/wpl/tianqing/sample.dat`，目录级非空行 54

| 来源字段 | SDM 候选目标 | 转换/保留策略 | 证据 |
|---|---|---|---|
| `asset_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `asset_oid` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `audit_type` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `behavior` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `client_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `client_ip` | `source_ip` | `candidate_identity` | `vendor_confirmed_and_observed` |
| `client_login_account` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `client_mac` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `client_mid` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `client_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `client_os_version_build_version` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `client_os_version_describe` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `client_os_version_main` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `client_os_version_release_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `client_report_ip` | `source_ip` | `candidate_identity` | `vendor_confirmed_and_observed` |
| `client_type` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `collect_time` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `create_time` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `file_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `file_size` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `group_node_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `group_node_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `group_node_path` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `handle` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `local_file_is_exists` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `local_file_path` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `operation_type` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `path_level1` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `path_level2` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `path_level3` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `path_level4` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `process_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `report_time` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `result` | `outcome` | `candidate_identity` | `vendor_confirmed_and_observed` |
| `syslog_topic` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `transfer_channel` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `transfer_method` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `upload_url` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `usb_type` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |

枚举/选择器信号：
- 字段 `syslog_topic`（has）；候选值 file_audit；未知值策略：`preserve_raw_and_report`

开放问题：
- 已有天擎 examples 映射包（目录 edr_file_audit）；本目录仅记录复核状态，不重复生成样例

## `edr_file_op`

- 状态：`reused_and_reviewed`
- 证据：`vendor_confirmed_and_observed`
- WPL 规则：edr_file_op
- 样本：`s4-doris/models/wpl/tianqing/sample.dat`，目录级非空行 54

| 来源字段 | SDM 候选目标 | 转换/保留策略 | 证据 |
|---|---|---|---|
| `asset_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `asset_oid` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `client_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `client_info` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `client_ip` | `source_ip` | `candidate_identity` | `vendor_confirmed_and_observed` |
| `client_report_ip` | `source_ip` | `candidate_identity` | `vendor_confirmed_and_observed` |
| `computer_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `create_time` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `custom_group_paths` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `env_version` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `event_date_creation` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `file_date_creation` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `file_md5` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `file_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `file_name_renamed` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `file_path` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `file_path_renamed` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `file_previous_date_creation` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `gid` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `group_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `hostname` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `ip` | `source_ip` | `candidate_identity` | `vendor_confirmed_and_observed` |
| `logger` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `mac` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `mid` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `payload` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `pid` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `process_command_line` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `process_guid` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `process_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `process_internal_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `process_md5` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `process_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `process_original_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `process_parent_command_line` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `process_parent_internal_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `process_parent_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `process_parent_original_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `process_parent_path` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `process_parent_sign` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `process_path` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `process_sha1` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `process_sign` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `process_user` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `removable_device` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `report_ip` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `sub_task_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `task_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `timestamp` | `occur_time` | `candidate_identity` | `vendor_confirmed_and_observed` |
| `type` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `uuid` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |

枚举/选择器信号：
- 字段 `type`（has）；候选值 file_operations；未知值策略：`preserve_raw_and_report`

开放问题：
- 已有天擎 examples 映射包（目录 edr_file_op）；本目录仅记录复核状态，不重复生成样例

## `edr_firewall`

- 状态：`reused_and_reviewed`
- 证据：`vendor_confirmed_and_observed`
- WPL 规则：edr_firewall
- 样本：`s4-doris/models/wpl/tianqing/sample.dat`，目录级非空行 54

| 来源字段 | SDM 候选目标 | 转换/保留策略 | 证据 |
|---|---|---|---|
| `activation` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `build_version` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `client_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `client_info` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `computer_working_group` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `core_number` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `create_time` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `describe` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `domain` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `dst_ip` | `target_ip` | `candidate_identity` | `vendor_confirmed_and_observed` |
| `file_alarm_time` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `file_create_time` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `file_path` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `group_info` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `guid` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `ie_version` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `intercept_time` | `occur_time` | `candidate_identity` | `vendor_confirmed_and_observed` |
| `login_account` | `source_user` | `candidate_identity` | `vendor_confirmed_and_observed` |
| `mac` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `main` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `md5` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `memory_size` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `mid` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `name` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `need_reboot` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `nic_list` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `node_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `node_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `node_type` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `oid` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `os` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `os_bit` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `release_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `report_ip` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `report_ipv6` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `result` | `outcome` | `candidate_identity` | `vendor_confirmed_and_observed` |
| `scanners` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `sha1` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `src_ip` | `source_ip` | `candidate_identity` | `vendor_confirmed_and_observed` |
| `state` | `outcome` | `candidate_identity` | `vendor_confirmed_and_observed` |
| `sys_space` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `system_language` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `tree_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `trigger_mode` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `update_time` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `virus_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `virus_type` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |

枚举/选择器信号：
- 字段 `syslog_topic`（has）；候选值 firewall；未知值策略：`preserve_raw_and_report`

开放问题：
- 已有天擎 examples 映射包（目录 edr_firewall）；本目录仅记录复核状态，不重复生成样例

## `edr_mobile_storage_client_log`

- 状态：`reused_and_reviewed`
- 证据：`vendor_confirmed_and_observed`
- WPL 规则：edr_mobile_storage_client_log
- 样本：`s4-doris/models/wpl/tianqing/sample.dat`，目录级非空行 54

| 来源字段 | SDM 候选目标 | 转换/保留策略 | 证据 |
|---|---|---|---|
| `activation` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `admin_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `asset_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `asset_oid` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `auth_node_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `capacity` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `client_activation` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `client_computer_working_group` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `client_core_number` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `client_create_time` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `client_domain` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `client_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `client_ie_version` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `client_info` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `client_ip` | `source_ip` | `candidate_identity` | `vendor_confirmed_and_observed` |
| `client_login_account` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `client_mac` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `client_memory_size` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `client_mid` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `client_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `client_nic_list` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `client_os` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `client_os_bit` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `client_os_version_build_version` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `client_os_version_describe` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `client_os_version_main` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `client_os_version_release_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `client_report_ip` | `source_ip` | `candidate_identity` | `vendor_confirmed_and_observed` |
| `client_report_ipv6` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `client_state` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `client_sys_space` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `client_system_language` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `client_tos_arch` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `client_tos_dist` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `client_tos_os` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `client_tos_version` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `client_type` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `client_update_time` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `collect_time` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `computer_working_group` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `core_number` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `create_time` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `destination` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `detail` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `device_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `domain` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `eid` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `f` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `group_info` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `group_node_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `group_node_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `group_node_path` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `group_node_type` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `group_oid` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `group_tree_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `ie_version` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `ip` | `source_ip` | `candidate_identity` | `vendor_confirmed_and_observed` |
| `is_intranet` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `is_register` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `is_roam` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `label_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `log_report_type` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `log_type` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `login_account` | `source_user` | `candidate_identity` | `vendor_confirmed_and_observed` |
| `login_user` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `mac` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `memory_size` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `mid` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `name` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `nic_list` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `node_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `node_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `node_type` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `number` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `oid` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `operation_time` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `os` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `os_bit` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `out_permission` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `out_valid_day` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `out_valid_max_times` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `path_level1` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `path_level10` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `path_level2` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `path_level3` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `path_level4` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `path_level5` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `path_level6` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `path_level7` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `path_level8` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `path_level9` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `pid` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `report_ip` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `report_ipv6` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `result` | `outcome` | `candidate_identity` | `vendor_confirmed_and_observed` |
| `search_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `server_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `source` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `src_log_type` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `state` | `outcome` | `candidate_identity` | `vendor_confirmed_and_observed` |
| `supplier` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `sys_space` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `syslog_topic` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `system_language` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `tree_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `update_time` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `usb_status` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `usb_type` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `user_create_time` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `user_email` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `user_group_info` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `user_group_names` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `user_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `user_info` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `user_mobile_phone_country_code` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `user_mobile_phone_number` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `user_name` | `source_user` | `candidate_identity` | `vendor_confirmed_and_observed` |
| `user_number` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `user_real_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `user_source_factor` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `user_source_factor_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `user_source_factor_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `user_state` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `user_third_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `user_update_time` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `vid` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |

枚举/选择器信号：
- 字段 `syslog_topic`（has）；候选值 mobile_storage_client_log；未知值策略：`preserve_raw_and_report`

开放问题：
- 已有天擎 examples 映射包（目录 edr_mobile_storage_client_log）；本目录仅记录复核状态，不重复生成样例

## `edr_net_out_log`

- 状态：`reused_and_reviewed`
- 证据：`vendor_confirmed_and_observed`
- WPL 规则：edr_net_out_log
- 样本：`s4-doris/models/wpl/tianqing/sample.dat`，目录级非空行 54

| 来源字段 | SDM 候选目标 | 转换/保留策略 | 证据 |
|---|---|---|---|
| `action` | `outcome` | `candidate_identity` | `vendor_confirmed_and_observed` |
| `activation` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `build_version` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `client_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `client_info` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `computer_working_group` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `core_number` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `create_time` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `describe` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `domain` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `file_alarm_time` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `file_create_time` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `file_path` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `group_info` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `guid` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `ie_version` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `login_account` | `source_user` | `candidate_identity` | `vendor_confirmed_and_observed` |
| `mac` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `main` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `md5` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `memory_size` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `mid` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `name` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `need_reboot` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `nic_list` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `node_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `node_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `node_type` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `oid` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `os` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `os_bit` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `release_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `report_ip` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `report_ipv6` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `result` | `outcome` | `candidate_identity` | `vendor_confirmed_and_observed` |
| `scanners` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `sha1` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `state` | `outcome` | `candidate_identity` | `vendor_confirmed_and_observed` |
| `sys_space` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `system_language` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `tree_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `trigger_mode` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `update_time` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `virus_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `virus_type` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |

枚举/选择器信号：
- 字段 `syslog_topic`（has）；候选值 net_out_log；未知值策略：`preserve_raw_and_report`

开放问题：
- 已有天擎 examples 映射包（目录 edr_net_out_log）；本目录仅记录复核状态，不重复生成样例

## `edr_powershell_cmd_exec`

- 状态：`reused_and_reviewed`
- 证据：`vendor_confirmed_and_observed`
- WPL 规则：edr_powershell_cmd_exec
- 样本：`s4-doris/models/wpl/tianqing/sample.dat`，目录级非空行 54

| 来源字段 | SDM 候选目标 | 转换/保留策略 | 证据 |
|---|---|---|---|
| `asset_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `asset_oid` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `client_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `client_info` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `client_ip` | `source_ip` | `candidate_identity` | `vendor_confirmed_and_observed` |
| `client_report_ip` | `source_ip` | `candidate_identity` | `vendor_confirmed_and_observed` |
| `computer_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `create_time` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `custom_group_paths` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `env_version` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `event_date_creation` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `event_id` | `event_id` | `candidate_identity` | `vendor_confirmed_and_observed` |
| `event_type` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `gid` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `group_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `hostname` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `ip` | `source_ip` | `candidate_identity` | `vendor_confirmed_and_observed` |
| `keywords` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `logger` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `mac` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `mid` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `payload` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `pid` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `powershell_create_time` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `powershell_payload` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `process_guid` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `process_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `process_internal_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `process_sign` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `process_user` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `report_ip` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `script_command` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `script_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `security_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `sub_task_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `task_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `thread_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `timestamp` | `occur_time` | `candidate_identity` | `vendor_confirmed_and_observed` |
| `type` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `user_data` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `uuid` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |

枚举/选择器信号：
- 字段 `type`（has）；候选值 powershell_execute；未知值策略：`preserve_raw_and_report`

开放问题：
- 已有天擎 examples 映射包（目录 edr_powershell_cmd_exec）；本目录仅记录复核状态，不重复生成样例

## `edr_process_event`

- 状态：`reused_and_reviewed`
- 证据：`vendor_confirmed_and_observed`
- WPL 规则：edr_process_event
- 样本：`s4-doris/models/wpl/tianqing/sample.dat`，目录级非空行 54

| 来源字段 | SDM 候选目标 | 转换/保留策略 | 证据 |
|---|---|---|---|
| `asset_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `asset_oid` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `client_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `client_info` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `client_ip` | `source_ip` | `candidate_identity` | `vendor_confirmed_and_observed` |
| `client_report_ip` | `source_ip` | `candidate_identity` | `vendor_confirmed_and_observed` |
| `computer_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `create_time` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `custom_group_paths` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `env_version` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `event_date_creation` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `event_type` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `gid` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `group_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `hostname` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `ip` | `source_ip` | `candidate_identity` | `vendor_confirmed_and_observed` |
| `logger` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `mac` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `mid` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `payload` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `pid` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `process_command_line` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `process_company` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `process_copyright` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `process_create_time` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `process_current_directory` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `process_description` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `process_guid` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `process_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `process_integrity_level` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `process_internal_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `process_md5` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `process_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `process_original_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `process_parent_command_line` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `process_parent_guid` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `process_parent_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `process_parent_internal_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `process_parent_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `process_parent_original_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `process_parent_path` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `process_parent_sign` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `process_path` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `process_pparent_command_line` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `process_pparent_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `process_pparent_path` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `process_product` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `process_root_guid` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `process_root_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `process_sha1` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `process_sign` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `process_terminate_time` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `process_user` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `process_version` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `report_ip` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `sub_task_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `task_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `timestamp` | `occur_time` | `candidate_identity` | `vendor_confirmed_and_observed` |
| `type` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `user_logon_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `user_session_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `uuid` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |

枚举/选择器信号：
- 字段 `type`（has）；候选值 process_details；未知值策略：`preserve_raw_and_report`

开放问题：
- 已有天擎 examples 映射包（目录 edr_process_event）；本目录仅记录复核状态，不重复生成样例

## `edr_process_log`

- 状态：`reused_and_reviewed`
- 证据：`vendor_confirmed_and_observed`
- WPL 规则：edr_process_log
- 样本：`s4-doris/models/wpl/tianqing/sample.dat`，目录级非空行 54

| 来源字段 | SDM 候选目标 | 转换/保留策略 | 证据 |
|---|---|---|---|
| `activation` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `build_version` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `client_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `client_info` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `computer_working_group` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `core_number` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `create_time` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `describe` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `domain` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `file_alarm_time` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `file_create_time` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `file_path` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `group_info` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `guid` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `ie_version` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `ip` | `source_ip` | `candidate_identity` | `vendor_confirmed_and_observed` |
| `login_account` | `source_user` | `candidate_identity` | `vendor_confirmed_and_observed` |
| `mac` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `main` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `md5` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `memory_size` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `mid` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `mode` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `name` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `need_reboot` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `nic_list` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `node_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `node_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `node_type` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `oid` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `os` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `os_bit` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `path` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `release_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `report_ip` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `report_ipv6` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `result` | `outcome` | `candidate_identity` | `vendor_confirmed_and_observed` |
| `scanners` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `sha1` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `state` | `outcome` | `candidate_identity` | `vendor_confirmed_and_observed` |
| `sys_space` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `system_language` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `tree_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `trigger_mode` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `update_time` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `virus_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `virus_type` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |

枚举/选择器信号：
- 字段 `syslog_topic`（has）；候选值 process_log；未知值策略：`preserve_raw_and_report`

开放问题：
- 已有天擎 examples 映射包（目录 edr_process_log）；本目录仅记录复核状态，不重复生成样例

## `edr_remote_assistance_file_transfer`

- 状态：`reused_and_reviewed`
- 证据：`vendor_confirmed_and_observed`
- WPL 规则：edr_remote_assistance_file_transfer
- 样本：`s4-doris/models/wpl/tianqing/sample.dat`，目录级非空行 54

| 来源字段 | SDM 候选目标 | 转换/保留策略 | 证据 |
|---|---|---|---|
| `action` | `outcome` | `candidate_identity` | `vendor_confirmed_and_observed` |
| `activation` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `build_version` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `client_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `client_info` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `computer_working_group` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `core_number` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `create_time` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `describe` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `domain` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `file_alarm_time` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `file_create_time` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `file_path` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `group_info` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `guid` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `ie_version` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `login_account` | `source_user` | `candidate_identity` | `vendor_confirmed_and_observed` |
| `mac` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `main` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `md5` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `memory_size` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `mid` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `name` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `need_reboot` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `nic_list` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `node_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `node_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `node_type` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `oid` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `os` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `os_bit` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `release_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `report_ip` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `report_ipv6` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `report_time` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `result` | `outcome` | `candidate_identity` | `vendor_confirmed_and_observed` |
| `scanners` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `sha1` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `state` | `outcome` | `candidate_identity` | `vendor_confirmed_and_observed` |
| `sys_space` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `system_language` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `tree_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `trigger_mode` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `update_time` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `virus_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `virus_type` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |

枚举/选择器信号：
- 字段 `syslog_topic`（has）；候选值 remote_assistance_file_transfer；未知值策略：`preserve_raw_and_report`

开放问题：
- 已有天擎 examples 映射包（目录 edr_remote_assistance_file_transfer）；本目录仅记录复核状态，不重复生成样例

## `edr_remote_assistance_log`

- 状态：`reused_and_reviewed`
- 证据：`vendor_confirmed_and_observed`
- WPL 规则：edr_remote_assistance_log
- 样本：`s4-doris/models/wpl/tianqing/sample.dat`，目录级非空行 54

| 来源字段 | SDM 候选目标 | 转换/保留策略 | 证据 |
|---|---|---|---|
| `action` | `outcome` | `candidate_identity` | `vendor_confirmed_and_observed` |
| `activation` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `build_version` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `client_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `client_info` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `computer_working_group` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `core_number` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `create_time` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `describe` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `domain` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `file_alarm_time` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `file_create_time` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `file_path` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `group_info` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `guid` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `ie_version` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `login_account` | `source_user` | `candidate_identity` | `vendor_confirmed_and_observed` |
| `mac` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `main` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `md5` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `memory_size` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `mid` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `name` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `need_reboot` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `nic_list` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `node_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `node_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `node_type` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `oid` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `os` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `os_bit` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `release_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `report_ip` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `report_ipv6` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `report_time` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `result` | `outcome` | `candidate_identity` | `vendor_confirmed_and_observed` |
| `scanners` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `sha1` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `state` | `outcome` | `candidate_identity` | `vendor_confirmed_and_observed` |
| `sys_space` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `system_language` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `tree_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `trigger_mode` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `update_time` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `virus_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `virus_type` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |

枚举/选择器信号：
- 字段 `syslog_topic`（has）；候选值 remote_assistance_log；未知值策略：`preserve_raw_and_report`

开放问题：
- 已有天擎 examples 映射包（目录 edr_remote_assistance_log）；本目录仅记录复核状态，不重复生成样例

## `edr_ssid_log`

- 状态：`reused_and_reviewed`
- 证据：`vendor_confirmed_and_observed`
- WPL 规则：edr_ssid_log
- 样本：`s4-doris/models/wpl/tianqing/sample.dat`，目录级非空行 54

| 来源字段 | SDM 候选目标 | 转换/保留策略 | 证据 |
|---|---|---|---|
| `action` | `outcome` | `candidate_identity` | `vendor_confirmed_and_observed` |
| `activation` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `build_version` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `client_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `client_info` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `client_mac` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `computer_working_group` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `core_number` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `create_time` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `describe` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `domain` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `file_alarm_time` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `file_create_time` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `file_path` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `group_info` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `guid` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `ie_version` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `log_type` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `login_account` | `source_user` | `candidate_identity` | `vendor_confirmed_and_observed` |
| `mac` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `main` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `md5` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `memory_size` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `mid` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `name` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `need_reboot` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `nic_list` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `node_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `node_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `node_type` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `oid` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `os` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `os_bit` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `release_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `report_ip` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `report_ipv6` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `result` | `outcome` | `candidate_identity` | `vendor_confirmed_and_observed` |
| `scanners` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `sha1` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `ssid_log_type` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `state` | `outcome` | `candidate_identity` | `vendor_confirmed_and_observed` |
| `sys_space` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `system_language` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `tree_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `trigger_mode` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `update_time` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `virus_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `virus_type` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |

枚举/选择器信号：
- 字段 `syslog_topic`（has）；候选值 ssid_log；未知值策略：`preserve_raw_and_report`

开放问题：
- 已有天擎 examples 映射包（目录 edr_ssid_log）；本目录仅记录复核状态，不重复生成样例

## `edr_system_protection`

- 状态：`reused_and_reviewed`
- 证据：`vendor_confirmed_and_observed`
- WPL 规则：edr_system_protection
- 样本：`s4-doris/models/wpl/tianqing/sample.dat`，目录级非空行 54

| 来源字段 | SDM 候选目标 | 转换/保留策略 | 证据 |
|---|---|---|---|
| `activation` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `build_version` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `client_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `client_info` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `computer_working_group` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `core_number` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `create_time` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `describe` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `domain` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `event_time` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `file_alarm_time` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `file_create_time` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `file_path` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `group_info` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `guid` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `ie_version` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `login_account` | `source_user` | `candidate_identity` | `vendor_confirmed_and_observed` |
| `mac` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `main` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `md5` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `memory_size` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `mid` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `name` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `need_reboot` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `nic_list` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `node_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `node_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `node_type` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `oid` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `os` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `os_bit` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `release_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `report_ip` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `report_ipv6` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `result` | `outcome` | `candidate_identity` | `vendor_confirmed_and_observed` |
| `scanners` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `sha1` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `state` | `outcome` | `candidate_identity` | `vendor_confirmed_and_observed` |
| `sys_space` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `system_language` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `tree_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `trigger_mode` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `update_time` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `virus_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `virus_type` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |

枚举/选择器信号：
- 字段 `syslog_topic`（has）；候选值 system_protection_log；未知值策略：`preserve_raw_and_report`

开放问题：
- 已有天擎 examples 映射包（目录 edr_system_protection）；本目录仅记录复核状态，不重复生成样例

## `edr_webpage_protection`

- 状态：`reused_and_reviewed`
- 证据：`vendor_confirmed_and_observed`
- WPL 规则：edr_webpage_protection
- 样本：`s4-doris/models/wpl/tianqing/sample.dat`，目录级非空行 54

| 来源字段 | SDM 候选目标 | 转换/保留策略 | 证据 |
|---|---|---|---|
| `activation` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `build_version` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `client_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `client_info` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `computer_working_group` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `core_number` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `create_time` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `describe` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `domain` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `event_time` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `file_alarm_time` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `file_create_time` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `file_path` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `group_info` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `guid` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `ie_version` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `login_account` | `source_user` | `candidate_identity` | `vendor_confirmed_and_observed` |
| `mac` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `main` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `md5` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `memory_size` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `mid` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `name` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `need_reboot` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `nic_list` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `node_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `node_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `node_type` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `oid` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `os` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `os_bit` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `release_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `report_ip` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `report_ipv6` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `result` | `outcome` | `candidate_identity` | `vendor_confirmed_and_observed` |
| `scanners` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `sha1` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `state` | `outcome` | `candidate_identity` | `vendor_confirmed_and_observed` |
| `sys_space` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `system_language` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `tree_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `trigger_mode` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `update_time` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `virus_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `virus_type` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `visit_ip` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |

枚举/选择器信号：
- 字段 `syslog_topic`（has）；候选值 webpage_protection_log；未知值策略：`preserve_raw_and_report`

开放问题：
- 已有天擎 examples 映射包（目录 edr_webpage_protection）；本目录仅记录复核状态，不重复生成样例

## `edr_wmi_event`

- 状态：`reused_and_reviewed`
- 证据：`vendor_confirmed_and_observed`
- WPL 规则：edr_wmi_event
- 样本：`s4-doris/models/wpl/tianqing/sample.dat`，目录级非空行 54

| 来源字段 | SDM 候选目标 | 转换/保留策略 | 证据 |
|---|---|---|---|
| `asset_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `asset_oid` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `client_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `client_info` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `client_ip` | `source_ip` | `candidate_identity` | `vendor_confirmed_and_observed` |
| `client_report_ip` | `source_ip` | `candidate_identity` | `vendor_confirmed_and_observed` |
| `computer_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `custom_group_paths` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `event_date_creation` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `event_type` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `gid` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `group_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `ip` | `source_ip` | `candidate_identity` | `vendor_confirmed_and_observed` |
| `mac` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `mid` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `payload` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `process_command_line` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `process_guid` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `process_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `process_internal_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `process_md5` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `process_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `process_original_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `process_parent_command_line` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `process_parent_internal_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `process_parent_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `process_parent_original_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `process_parent_path` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `process_parent_sign` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `process_path` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `process_sha1` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `process_sign` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `process_user` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `report_ip` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `sub_task_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `task_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `timestamp` | `occur_time` | `candidate_identity` | `vendor_confirmed_and_observed` |
| `type` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `uuid` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `wmi_consumer_destination` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `wmi_consumer_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `wmi_consumer_type` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `wmi_filter_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `wmi_filter_wql` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `wmi_namespace` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `wmi_operation` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |

枚举/选择器信号：
- 字段 `type`（has）；候选值 wmi_event；未知值策略：`preserve_raw_and_report`

开放问题：
- 已有天擎 examples 映射包（目录 edr_wmi_event）；本目录仅记录复核状态，不重复生成样例

