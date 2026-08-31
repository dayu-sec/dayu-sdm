# dm_terminal 字段映射与枚举候选

候选结果，未经标准注册审批。样本字段为源目录级证据；只有 WPL 规则块字段被归属到具体 log_type。

## `dm_terminal_log`

- 状态：`candidate`
- 证据：`sample_inferred`
- WPL 规则：dm_terminal_log
- 样本：`log-model/examples/dm_terminal/`，目录级非空行 6

| 来源字段 | SDM 候选目标 | 转换/保留策略 | 证据 |
|---|---|---|---|
| `action` | `outcome` | `candidate_identity` | `sample_inferred` |
| `alarm` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `auth_name` | `source_user` | `candidate_identity` | `sample_inferred` |
| `authtype` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `class` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `details` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `devid` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `devip` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `event` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `event_class_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `event_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `vendor_confirmed_and_observed` |
| `ip` | `source_ip` | `candidate_identity` | `sample_inferred` |
| `ipaddr` | `device_ip` | `identity_management_ip` | `vendor_confirmed_and_observed` |
| `level` | `source_finding.severity` | `identity_source_severity` | `vendor_confirmed_and_observed` |
| `log_id` | `event_id` | `candidate_identity` | `sample_inferred` |
| `macaddr` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `msg` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `name` | `device_name` | `identity` | `vendor_confirmed_and_observed` |
| `port_name` | `roles.target.resource.name` | `network_port_resource` | `vendor_confirmed_and_observed` |
| `result` | `outcome` | `candidate_identity` | `sample_inferred` |
| `time` | `occur_time` | `candidate_identity` | `sample_inferred` |
| `timestamp` | `occur_time` | `candidate_identity` | `sample_inferred` |
| `type` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `user` | `source_user` | `candidate_identity` | `sample_inferred` |

枚举/选择器信号：
- 字段 `event_class_id`（in）；候选值 0x0100, 0x0200, 0x0300, 0x0400, 0x0500, 0x0600；未知值策略：`preserve_raw_and_report`

## `dm_terminal_log` 人工语义复核

- 事件事实：思科交换机的端口 FastEthernet1/0/9 状态变为 DOWN；event_class_id=0x0100、event_id=0x0102 与厂商文档的设备事件/交换机端口 DOWN 枚举一致。
- 主体为交换机，客体为状态变化的端口；`ipaddr` 是设备管理 IP。
- 厂商事件代码保留在 `extensions.source_private.event_id`，SDM `event_id` 仍由原始载荷确定性生成。
- 证据：北信源《网络接入控制系统 SYSLOG 接口说明文档 V1.1》设备事件表：event_class_id=0x0100，交换机端口 DOWN 的 event_id=0x0102；样本已观测。
