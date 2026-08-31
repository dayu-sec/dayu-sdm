# sxf_firewall 字段映射与枚举候选

候选结果，未经标准注册审批。样本字段为源目录级证据；只有 WPL 规则块字段被归属到具体 log_type。

## `ad_ddos_attack_log`

- 状态：`candidate`
- 证据：`sample_inferred`
- WPL 规则：ad_ddos_attack_log, ad_ddos_attack_log_v2
- 样本：`log-model/examples/sxf_firewall/`，目录级非空行 39

| 来源字段 | SDM 候选目标 | 转换/保留策略 | 证据 |
|---|---|---|---|
| `AttackType` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `PolicyName` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `ThreatSeverity` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `act` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `comm_direction` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dip` | `target_ip` | `candidate_identity` | `sample_inferred` |
| `direction` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dport` | `target_port` | `candidate_identity` | `sample_inferred` |
| `dst` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `logtype` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `op_action` | `outcome` | `candidate_identity` | `sample_inferred` |
| `origin_alert_cat_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `policy_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `protocol` | `protocol` | `candidate_identity` | `sample_inferred` |
| `severity` | `severity` | `candidate_identity` | `sample_inferred` |
| `sip` | `source_ip` | `candidate_identity` | `sample_inferred` |
| `sport` | `source_port` | `candidate_identity` | `sample_inferred` |
| `src` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |

## `fw_antivirus_virus`

- 状态：`candidate`
- 证据：`sample_inferred`
- WPL 规则：fw_antivirus_virus, fw_antivirus_virus_v2
- 样本：`log-model/examples/sxf_firewall/`，目录级非空行 39

| 来源字段 | SDM 候选目标 | 转换/保留策略 | 证据 |
|---|---|---|---|
| `PolicyName` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `Request` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `ThreatSeverity` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `URL` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `VirusName` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `act` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `app` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `app_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dip` | `target_ip` | `candidate_identity` | `sample_inferred` |
| `dport` | `target_port` | `candidate_identity` | `sample_inferred` |
| `dpt` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dst` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `logtype` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `op_action` | `outcome` | `candidate_identity` | `sample_inferred` |
| `origin_alert_cat_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `policy_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `severity` | `severity` | `candidate_identity` | `sample_inferred` |
| `sip` | `source_ip` | `candidate_identity` | `sample_inferred` |
| `sport` | `source_port` | `candidate_identity` | `sample_inferred` |
| `spt` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `src` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `suser` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `url` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `user_name` | `source_user` | `candidate_identity` | `sample_inferred` |
| `virus_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `virus_type` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |

## `fw_botnet_log`

- 状态：`candidate`
- 证据：`sample_inferred`
- WPL 规则：fw_botnet_log, fw_botnet_log_v2
- 样本：`log-model/examples/sxf_firewall/`，目录级非空行 39

| 来源字段 | SDM 候选目标 | 转换/保留策略 | 证据 |
|---|---|---|---|
| `AttackType` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `DeviceEventClassID` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `PolicyName` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `Request` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `ThreatSeverity` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `URL` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `act` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dip` | `target_ip` | `candidate_identity` | `sample_inferred` |
| `dport` | `target_port` | `candidate_identity` | `sample_inferred` |
| `dpt` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dst` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `logtype` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `op_action` | `outcome` | `candidate_identity` | `sample_inferred` |
| `origin_alert_cat_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `policy_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `protocol` | `protocol` | `candidate_identity` | `sample_inferred` |
| `risk_type` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `rule_id` | `event_id` | `candidate_identity` | `sample_inferred` |
| `severity` | `severity` | `candidate_identity` | `sample_inferred` |
| `sid` | `event_id` | `candidate_identity` | `sample_inferred` |
| `sip` | `source_ip` | `candidate_identity` | `sample_inferred` |
| `sport` | `source_port` | `candidate_identity` | `sample_inferred` |
| `spt` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `src` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `url` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |

## `fw_ips_protect_log`

- 状态：`candidate`
- 证据：`sample_inferred`
- WPL 规则：fw_ips_protect_log, fw_ips_protect_log_v2
- 样本：`log-model/examples/sxf_firewall/`，目录级非空行 39

| 来源字段 | SDM 候选目标 | 转换/保留策略 | 证据 |
|---|---|---|---|
| `AttackType` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `DeviceEventClassID` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `PolicyName` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `Request` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `ThreatSeverity` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `VulnerabilityName` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `act` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `app` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dip` | `target_ip` | `candidate_identity` | `sample_inferred` |
| `dport` | `target_port` | `candidate_identity` | `sample_inferred` |
| `dpt` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dst` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `logtype` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `op_action` | `outcome` | `candidate_identity` | `sample_inferred` |
| `origin_alert_cat_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `policy_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `protocol` | `protocol` | `candidate_identity` | `sample_inferred` |
| `severity` | `severity` | `candidate_identity` | `sample_inferred` |
| `sip` | `source_ip` | `candidate_identity` | `sample_inferred` |
| `sport` | `source_port` | `candidate_identity` | `sample_inferred` |
| `spt` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `src` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `url` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `vuln_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `vuln_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |

## `fw_local_access_log`

- 状态：`candidate`
- 证据：`sample_inferred`
- WPL 规则：fw_local_access_log, fw_local_access_log_v2
- 样本：`log-model/examples/sxf_firewall/`，目录级非空行 39

| 来源字段 | SDM 候选目标 | 转换/保留策略 | 证据 |
|---|---|---|---|
| `PolicyName` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `act` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `app` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `app_cat` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `app_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dip` | `target_ip` | `candidate_identity` | `sample_inferred` |
| `domain` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dport` | `target_port` | `candidate_identity` | `sample_inferred` |
| `dpt` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dst` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `logtype` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `msg` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `op_action` | `outcome` | `candidate_identity` | `sample_inferred` |
| `policy_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `sip` | `source_ip` | `candidate_identity` | `sample_inferred` |
| `sport` | `source_port` | `candidate_identity` | `sample_inferred` |
| `spt` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `src` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |

## `fw_mail_security_log`

- 状态：`candidate`
- 证据：`sample_inferred`
- WPL 规则：fw_mail_security_log, fw_mail_security_log_v2
- 样本：`log-model/examples/sxf_firewall/`，目录级非空行 39

| 来源字段 | SDM 候选目标 | 转换/保留策略 | 证据 |
|---|---|---|---|
| `AttackType` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `DeviceEventClassID` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `PolicyName` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `ThreatSeverity` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `act` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dip` | `target_ip` | `candidate_identity` | `sample_inferred` |
| `dport` | `target_port` | `candidate_identity` | `sample_inferred` |
| `dpt` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dst` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `logtype` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `op_action` | `outcome` | `candidate_identity` | `sample_inferred` |
| `origin_alert_cat_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `policy_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `rule_id` | `event_id` | `candidate_identity` | `sample_inferred` |
| `severity` | `severity` | `candidate_identity` | `sample_inferred` |
| `sip` | `source_ip` | `candidate_identity` | `sample_inferred` |
| `sport` | `source_port` | `candidate_identity` | `sample_inferred` |
| `spt` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `src` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |

## `fw_nat_log`

- 状态：`candidate`
- 证据：`sample_inferred`
- WPL 规则：fw_nat_log, fw_nat_log_v2
- 样本：`log-model/examples/sxf_firewall/`，目录级非空行 39

| 来源字段 | SDM 候选目标 | 转换/保留策略 | 证据 |
|---|---|---|---|
| `NAT` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `NATType` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `TranslatedAddress` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `TranslatedPort` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `destinationTranslatedAddress` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `destinationTranslatedPort` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dip` | `target_ip` | `candidate_identity` | `sample_inferred` |
| `dip_asset_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dip_asset_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dport` | `target_port` | `candidate_identity` | `sample_inferred` |
| `dpt` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dst` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `logtype` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `nat_after_ip` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `nat_after_port` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `nat_type` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `proto` | `protocol` | `candidate_identity` | `sample_inferred` |
| `protocol` | `protocol` | `candidate_identity` | `sample_inferred` |
| `sip` | `source_ip` | `candidate_identity` | `sample_inferred` |
| `sip_asset_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `sip_asset_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `sourceTranslatedAddress` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `sourceTranslatedPort` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `sport` | `source_port` | `candidate_identity` | `sample_inferred` |
| `spt` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `src` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |

## `fw_ssl_vpn_user_log`

- 状态：`candidate`
- 证据：`sample_inferred`
- WPL 规则：fw_ssl_vpn_user_log, fw_ssl_vpn_user_log_v2
- 样本：`log-model/examples/sxf_firewall/`，目录级非空行 39

| 来源字段 | SDM 候选目标 | 转换/保留策略 | 证据 |
|---|---|---|---|
| `IP` | `source_ip` | `candidate_identity` | `sample_inferred` |
| `act` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `login_time` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `logtype` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `msg` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `op_info` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `op_object` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `op_type` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `op_user_ip` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `src` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `start` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `suser` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `target` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `user_name` | `source_user` | `candidate_identity` | `sample_inferred` |

## `fw_system_op_log`

- 状态：`candidate`
- 证据：`sample_inferred`
- WPL 规则：fw_system_op_log, fw_system_op_log_v2
- 样本：`log-model/examples/sxf_firewall/`，目录级非空行 39

| 来源字段 | SDM 候选目标 | 转换/保留策略 | 证据 |
|---|---|---|---|
| `IP` | `source_ip` | `candidate_identity` | `sample_inferred` |
| `act` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `logtype` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `msg` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `op_info` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `op_object` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `op_type` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `op_user_ip` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `src` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `suser` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `target` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `user_name` | `source_user` | `candidate_identity` | `sample_inferred` |

## `fw_user_auth_log`

- 状态：`candidate`
- 证据：`sample_inferred`
- WPL 规则：fw_user_auth_log, fw_user_auth_log_v2
- 样本：`log-model/examples/sxf_firewall/`，目录级非空行 39

| 来源字段 | SDM 候选目标 | 转换/保留策略 | 证据 |
|---|---|---|---|
| `IP` | `source_ip` | `candidate_identity` | `sample_inferred` |
| `OnlineDuration` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `end` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `login_duration_time` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `login_time` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `logoff_time` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `logtype` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `op_object` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `op_user_ip` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `src` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `start` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `suser` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `target` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `user_name` | `source_user` | `candidate_identity` | `sample_inferred` |

## `fw_web_app_protect`

- 状态：`candidate`
- 证据：`sample_inferred`
- WPL 规则：fw_web_app_protect, fw_web_app_protect_v2
- 样本：`log-model/examples/sxf_firewall/`，目录级非空行 39

| 来源字段 | SDM 候选目标 | 转换/保留策略 | 证据 |
|---|---|---|---|
| `AttackType` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `DeviceEventClassID` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `PolicyName` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `Request` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `ThreatSeverity` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `URL` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `act` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dip` | `target_ip` | `candidate_identity` | `sample_inferred` |
| `dport` | `target_port` | `candidate_identity` | `sample_inferred` |
| `dpt` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dst` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `logtype` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `op_action` | `outcome` | `candidate_identity` | `sample_inferred` |
| `origin_alert_cat_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `policy_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `rule_id` | `event_id` | `candidate_identity` | `sample_inferred` |
| `severity` | `severity` | `candidate_identity` | `sample_inferred` |
| `sip` | `source_ip` | `candidate_identity` | `sample_inferred` |
| `sport` | `source_port` | `candidate_identity` | `sample_inferred` |
| `spt` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `src` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `url` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |

## `fw_web_threat`

- 状态：`candidate`
- 证据：`sample_inferred`
- WPL 规则：fw_web_threat, fw_web_threat_v2
- 样本：`log-model/examples/sxf_firewall/`，目录级非空行 39

| 来源字段 | SDM 候选目标 | 转换/保留策略 | 证据 |
|---|---|---|---|
| `PolicyName` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `Request` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `ThreatSeverity` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `URL` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `act` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `app_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dip` | `target_ip` | `candidate_identity` | `sample_inferred` |
| `dport` | `target_port` | `candidate_identity` | `sample_inferred` |
| `dst` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `logtype` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `op_action` | `outcome` | `candidate_identity` | `sample_inferred` |
| `policy_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `severity` | `severity` | `candidate_identity` | `sample_inferred` |
| `sip` | `source_ip` | `candidate_identity` | `sample_inferred` |
| `sport` | `source_port` | `candidate_identity` | `sample_inferred` |
| `src` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `suser` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `url` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `user_name` | `source_user` | `candidate_identity` | `sample_inferred` |

## `fw_website_access`

- 状态：`candidate`
- 证据：`sample_inferred`
- WPL 规则：fw_website_access, fw_website_access_v2
- 样本：`log-model/examples/sxf_firewall/`，目录级非空行 39

| 来源字段 | SDM 候选目标 | 转换/保留策略 | 证据 |
|---|---|---|---|
| `PolicyName` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `Request` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `ThreatSeverity` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `URL` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `act` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `app` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `app_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dip` | `target_ip` | `candidate_identity` | `sample_inferred` |
| `dport` | `target_port` | `candidate_identity` | `sample_inferred` |
| `dst` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `logtype` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `op_action` | `outcome` | `candidate_identity` | `sample_inferred` |
| `policy_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `severity` | `severity` | `candidate_identity` | `sample_inferred` |
| `sip` | `source_ip` | `candidate_identity` | `sample_inferred` |
| `sport` | `source_port` | `candidate_identity` | `sample_inferred` |
| `src` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `suser` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `url` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `user_name` | `source_user` | `candidate_identity` | `sample_inferred` |

