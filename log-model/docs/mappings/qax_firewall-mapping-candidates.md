# qax_firewall 字段映射与枚举候选

候选结果，未经标准注册审批。样本字段为源目录级证据；只有 WPL 规则块字段被归属到具体 log_type。

## `bh_api_risk_log`

- 状态：`candidate`
- 证据：`sample_inferred`
- WPL 规则：bh_api_risk_log
- 样本：`s4-doris/models/wpl/qax_firewall/sample.dat`，目录级非空行 35

| 来源字段 | SDM 候选目标 | 转换/保留策略 | 证据 |
|---|---|---|---|
| `accessApi` | `roles.target.resource.name`、`facets.http.request.path` | `relative_api_path` | `vendor_confirmed_and_observed` |
| `content` | `source_finding.description` | `identity` | `vendor_confirmed_and_observed` |
| `ipStatus` | `source_finding.status`、`extensions.source_private.ipStatus` | `finding_status_and_preserve_raw` | `vendor_confirmed_and_observed` |
| `logType` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `prod_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `prod_ips` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `prod_version` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `result` | `source_finding.action` | `source_control_action` | `vendor_confirmed_and_observed` |
| `souceIp` | `roles.source.endpoint.ip`、`source_ip` | `identity` | `vendor_confirmed_and_observed` |
| `time` | `occur_time` | `candidate_identity` | `sample_inferred` |
| `user` | `roles.source.user.name`、`source_user` | `identity` | `vendor_confirmed_and_observed` |

事件语义：`event_category=alert`、`event_type=network_http`、`operation=empty`、`outcome=unknown`。`result=已拦截` 是来源安全控制结论，不直接映射底层 HTTP outcome。

枚举/选择器信号：
- 字段 `logType`（has）；候选值 YAB_API_RISK_LOG；未知值策略：`preserve_raw_and_report`

## `bh_command_operation_log`

- 状态：`candidate`
- 证据：`sample_inferred`
- WPL 规则：bh_command_operation_log
- 样本：`s4-doris/models/wpl/qax_firewall/sample.dat`，目录级非空行 35

| 来源字段 | SDM 候选目标 | 转换/保留策略 | 证据 |
|---|---|---|---|
| `filename` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `logType` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `operation` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `prod_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `prod_ips` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `prod_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `prod_version` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `resource` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `result` | `outcome` | `candidate_identity` | `sample_inferred` |
| `size` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `sourceIP` | `source_ip` | `candidate_identity` | `sample_inferred` |
| `sourcePath` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `targetIP` | `target_ip` | `candidate_identity` | `sample_inferred` |
| `targetPath` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `time` | `occur_time` | `candidate_identity` | `sample_inferred` |
| `user` | `source_user` | `candidate_identity` | `sample_inferred` |

枚举/选择器信号：
- 字段 `logType`（has）；候选值 YAB_FILE_OPS_LOG；未知值策略：`preserve_raw_and_report`

## `bh_file_operation_log`

- 状态：`candidate`
- 证据：`sample_inferred`
- WPL 规则：bh_file_operation_log
- 样本：`s4-doris/models/wpl/qax_firewall/sample.dat`，目录级非空行 35

| 来源字段 | SDM 候选目标 | 转换/保留策略 | 证据 |
|---|---|---|---|
| `action` | `outcome` | `candidate_identity` | `sample_inferred` |
| `command` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `logType` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `prod_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `prod_ips` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `prod_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `prod_version` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `protocol` | `protocol` | `candidate_identity` | `sample_inferred` |
| `resource` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `session_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `sourceIP` | `source_ip` | `candidate_identity` | `sample_inferred` |
| `targetIP` | `target_ip` | `candidate_identity` | `sample_inferred` |
| `time` | `occur_time` | `candidate_identity` | `sample_inferred` |
| `user` | `source_user` | `candidate_identity` | `sample_inferred` |

枚举/选择器信号：
- 字段 `logType`（has）；候选值 YAB_CMD_OPS_LOG；未知值策略：`preserve_raw_and_report`

## `bh_his_session_record_log`

- 状态：`candidate`
- 证据：`sample_inferred`
- WPL 规则：bh_his_session_record_log
- 样本：`s4-doris/models/wpl/qax_firewall/sample.dat`，目录级非空行 35

| 来源字段 | SDM 候选目标 | 转换/保留策略 | 证据 |
|---|---|---|---|
| `account` | `source_user` | `candidate_identity` | `sample_inferred` |
| `endTime` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `historySession` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `logType` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `prod_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `prod_ips` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `prod_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `prod_version` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `protocol` | `protocol` | `candidate_identity` | `sample_inferred` |
| `resource` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `sourceIP` | `source_ip` | `candidate_identity` | `sample_inferred` |
| `startTime` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `targetIP` | `target_ip` | `candidate_identity` | `sample_inferred` |
| `user` | `source_user` | `candidate_identity` | `sample_inferred` |

枚举/选择器信号：
- 字段 `logType`（has）；候选值 YAB_HISTORY_SESSION_LOG；未知值策略：`preserve_raw_and_report`

## `bh_host_risk_log`

- 状态：`candidate`
- 证据：`sample_inferred`
- WPL 规则：bh_host_risk_log
- 样本：`s4-doris/models/wpl/qax_firewall/sample.dat`，目录级非空行 35

| 来源字段 | SDM 候选目标 | 转换/保留策略 | 证据 |
|---|---|---|---|
| `content` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `logType` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `prod_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `prod_ips` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `prod_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `prod_version` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `riskType` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `time` | `occur_time` | `candidate_identity` | `sample_inferred` |
| `user` | `source_user` | `candidate_identity` | `sample_inferred` |

枚举/选择器信号：
- 字段 `logType`（has）；候选值 YAB_HOST_RISK_LOG；未知值策略：`preserve_raw_and_report`

## `bh_middleware_log`

- 状态：`candidate`
- 证据：`sample_inferred`
- WPL 规则：bh_middleware_log
- 样本：`s4-doris/models/wpl/qax_firewall/sample.dat`，目录级非空行 35

| 来源字段 | SDM 候选目标 | 转换/保留策略 | 证据 |
|---|---|---|---|
| `content` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `logType` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `middleType` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `prod_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `prod_ips` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `prod_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `prod_version` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `time` | `occur_time` | `candidate_identity` | `sample_inferred` |
| `user` | `source_user` | `candidate_identity` | `sample_inferred` |

枚举/选择器信号：
- 字段 `logType`（has）；候选值 YAB_MIDDLE_WARE_LOG；未知值策略：`preserve_raw_and_report`

## `bh_ops_audit_log`

- 状态：`candidate`
- 证据：`sample_inferred`
- WPL 规则：bh_ops_audit_log
- 样本：`s4-doris/models/wpl/qax_firewall/sample.dat`，目录级非空行 35

| 来源字段 | SDM 候选目标 | 转换/保留策略 | 证据 |
|---|---|---|---|
| `content` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `cpu` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `eventType` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `logType` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `mem` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `operateModule` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `operationMsg` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `prod_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `prod_ips` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `prod_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `prod_version` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `read` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `result` | `outcome` | `candidate_identity` | `sample_inferred` |
| `sourceIP` | `source_ip` | `candidate_identity` | `sample_inferred` |
| `time` | `occur_time` | `candidate_identity` | `sample_inferred` |
| `user` | `source_user` | `candidate_identity` | `sample_inferred` |
| `write` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |

枚举/选择器信号：
- 字段 `logType`（in）；候选值 YAB_SYSTEM_STATUS_LOG, YAB_SYSTEM_OPERATE_LOG, YAB_SYSTEM_EVENT_LOG；未知值策略：`preserve_raw_and_report`

## `bh_resource_login_log`

- 状态：`candidate`
- 证据：`sample_inferred`
- WPL 规则：bh_resource_login_log
- 样本：`s4-doris/models/wpl/qax_firewall/sample.dat`，目录级非空行 35

| 来源字段 | SDM 候选目标 | 转换/保留策略 | 证据 |
|---|---|---|---|
| `account` | `source_user` | `candidate_identity` | `sample_inferred` |
| `endTime` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `logType` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `prod_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `prod_ips` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `prod_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `prod_version` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `protocol` | `protocol` | `candidate_identity` | `sample_inferred` |
| `resource` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `sourceIP` | `source_ip` | `candidate_identity` | `sample_inferred` |
| `startTime` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `targetIP` | `target_ip` | `candidate_identity` | `sample_inferred` |
| `user` | `source_user` | `candidate_identity` | `sample_inferred` |

枚举/选择器信号：
- 字段 `logType`（has）；候选值 YAB_RESOURCE_LOGIN_LOG；未知值策略：`preserve_raw_and_report`

## `bh_session_share_log`

- 状态：`candidate`
- 证据：`sample_inferred`
- WPL 规则：bh_session_share_log
- 样本：`s4-doris/models/wpl/qax_firewall/sample.dat`，目录级非空行 35

| 来源字段 | SDM 候选目标 | 转换/保留策略 | 证据 |
|---|---|---|---|
| `exitTime` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `joinTime` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `logType` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `prod_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `prod_ips` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `prod_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `prod_version` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `shareUser` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `sourceIp` | `source_ip` | `candidate_identity` | `sample_inferred` |
| `user` | `source_user` | `candidate_identity` | `sample_inferred` |

枚举/选择器信号：
- 字段 `logType`（has）；候选值 YAB_SESSION_SHARE_LOG；未知值策略：`preserve_raw_and_report`

## `bh_system_login_log`

- 状态：`candidate`
- 证据：`sample_inferred`
- WPL 规则：bh_system_login_log
- 样本：`s4-doris/models/wpl/qax_firewall/sample.dat`，目录级非空行 35

| 来源字段 | SDM 候选目标 | 转换/保留策略 | 证据 |
|---|---|---|---|
| `logType` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `logonType` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `operation` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `prod_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `prod_ips` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `prod_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `prod_version` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `result` | `outcome` | `candidate_identity` | `sample_inferred` |
| `sourceIp` | `source_ip` | `candidate_identity` | `sample_inferred` |
| `time` | `occur_time` | `candidate_identity` | `sample_inferred` |
| `user` | `source_user` | `candidate_identity` | `sample_inferred` |

枚举/选择器信号：
- 字段 `logType`（has）；候选值 YAB_SYSTEM_LOGIN_LOG；未知值策略：`preserve_raw_and_report`

## `bh_system_status_alert`

- 状态：`candidate`
- 证据：`sample_inferred`
- WPL 规则：bh_system_status_alert
- 样本：`s4-doris/models/wpl/qax_firewall/sample.dat`，目录级非空行 35

| 来源字段 | SDM 候选目标 | 转换/保留策略 | 证据 |
|---|---|---|---|
| `alarmLevel` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `alarmMsg` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `logType` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `prod_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `prod_ips` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `prod_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `prod_version` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `systemHardType` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `threshold` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `time` | `occur_time` | `candidate_identity` | `sample_inferred` |

枚举/选择器信号：
- 字段 `logType`（has）；候选值 YAB_SYSTEM_ALARM_LOG；未知值策略：`preserve_raw_and_report`

## `bh_two_person_authorization_log`

- 状态：`candidate`
- 证据：`sample_inferred`
- WPL 规则：bh_two_person_authorization_log
- 样本：`s4-doris/models/wpl/qax_firewall/sample.dat`，目录级非空行 35

| 来源字段 | SDM 候选目标 | 转换/保留策略 | 证据 |
|---|---|---|---|
| `approver` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `logType` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `prod_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `prod_ips` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `prod_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `prod_version` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `resource` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `sourceIP` | `source_ip` | `candidate_identity` | `sample_inferred` |
| `targetIP` | `target_ip` | `candidate_identity` | `sample_inferred` |
| `time` | `occur_time` | `candidate_identity` | `sample_inferred` |
| `user` | `source_user` | `candidate_identity` | `sample_inferred` |

枚举/选择器信号：
- 字段 `logType`（has）；候选值 YAB_DBL_AUTH_LOG；未知值策略：`preserve_raw_and_report`
