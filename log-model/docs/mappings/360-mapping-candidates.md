# 360 字段映射与枚举候选

候选结果，未经标准注册审批。样本字段为源目录级证据；只有 WPL 规则块字段被归属到具体 log_type。

## `360_active_defense_log`

- 状态：`candidate`
- 证据：`sample_inferred`
- WPL 规则：360_active_defense_log
- 样本：`log-model/examples/360/`，目录级非空行 9

| 来源字段 | SDM 候选目标 | 转换/保留策略 | 证据 |
|---|---|---|---|
| `ctime` | `occur_time` | `candidate_identity` | `sample_inferred` |
| `hips_subtype` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `hips_type` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `intercept_time` | `occur_time` | `candidate_identity` | `sample_inferred` |
| `log_type` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `plat_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `record_tm` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `type` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |

枚举/选择器信号：
- 字段 `type`（has）；候选值 active_defense_log；未知值策略：`preserve_raw_and_report`

## `360_device_audit`

- 状态：`candidate`
- 证据：`sample_inferred`
- WPL 规则：360_device_audit
- 样本：`log-model/examples/360/`，目录级非空行 9

| 来源字段 | SDM 候选目标 | 转换/保留策略 | 证据 |
|---|---|---|---|
| `ctime` | `occur_time` | `candidate_identity` | `sample_inferred` |
| `log_type` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `plat_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `send_time` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `type` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |

枚举/选择器信号：
- 字段 `type`（has）；候选值 device_audit；未知值策略：`preserve_raw_and_report`

## `360_edr_hotpatch_intercept_log`

- 状态：`candidate`
- 证据：`sample_inferred`
- WPL 规则：360_edr_hotpatch_intercept_log
- 样本：`log-model/examples/360/`，目录级非空行 9

| 来源字段 | SDM 候选目标 | 转换/保留策略 | 证据 |
|---|---|---|---|
| `ctime` | `occur_time` | `candidate_identity` | `sample_inferred` |
| `log_type` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `mtime` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `plat_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `type` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |

枚举/选择器信号：
- 字段 `type`（has）；候选值 360edr_hotpatch_intercept_log；未知值策略：`preserve_raw_and_report`

## `360_exthost_device_violation_log`

- 状态：`candidate`
- 证据：`sample_inferred`
- WPL 规则：360_exthost_device_violation_log
- 样本：`log-model/examples/360/`，目录级非空行 9

| 来源字段 | SDM 候选目标 | 转换/保留策略 | 证据 |
|---|---|---|---|
| `ctime` | `occur_time` | `candidate_identity` | `sample_inferred` |
| `log_type` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `ltime` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `plat_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `type` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |

枚举/选择器信号：
- 字段 `type`（has）；候选值 360exthost_device_violation_log；未知值策略：`preserve_raw_and_report`

## `360_exthost_netcontrol_illegal_net_log`

- 状态：`candidate`
- 证据：`sample_inferred`
- WPL 规则：360_exthost_netcontrol_illegal_net_log
- 样本：`log-model/examples/360/`，目录级非空行 9

| 来源字段 | SDM 候选目标 | 转换/保留策略 | 证据 |
|---|---|---|---|
| `ctime` | `occur_time` | `candidate_identity` | `sample_inferred` |
| `log_type` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `ltime` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `mtime` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `plat_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `report_status` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `type` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |

枚举/选择器信号：
- 字段 `type`（has）；候选值 360exthost_netcontrol_illegal_net_log；未知值策略：`preserve_raw_and_report`

## `360_exthost_sdmgr_virus_log`

- 状态：`candidate`
- 证据：`sample_inferred`
- WPL 规则：360_exthost_sdmgr_virus_log
- 样本：`log-model/examples/360/`，目录级非空行 9

| 来源字段 | SDM 候选目标 | 转换/保留策略 | 证据 |
|---|---|---|---|
| `ctime` | `occur_time` | `candidate_identity` | `sample_inferred` |
| `file_create_time` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `file_modify_time` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `file_path` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `found_time` | `occur_time` | `candidate_identity` | `sample_inferred` |
| `handle_time` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `log_type` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `ltime` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `mtime` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `plat_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `type` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |

枚举/选择器信号：
- 字段 `type`（has）；候选值 360exthost_360sdmgr_virus_log；未知值策略：`preserve_raw_and_report`

## `360_gtmaphenixdb_dlp_outfile_audit_log`

- 状态：`candidate`
- 证据：`sample_inferred`
- WPL 规则：360_gtmaphenixdb_dlp_outfile_audit_log
- 样本：`log-model/examples/360/`，目录级非空行 9

| 来源字段 | SDM 候选目标 | 转换/保留策略 | 证据 |
|---|---|---|---|
| `create_time` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `log_type` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `plat_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `send_time` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `type` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |

枚举/选择器信号：
- 字段 `type`（has）；候选值 gtmaphenixdb.dlp_outfile_audit_log；未知值策略：`preserve_raw_and_report`

## `360_leakfix_system_log`

- 状态：`reviewed_candidate`
- 证据：`vendor_confirmed_and_observed`
- WPL 规则：360_leakfix_system_log
- 样本：`log-model/examples/360/`，目录级非空行 9
- 事件事实：终端 DESKTOP-41B7VL6 的漏洞修复状态结果显示 KB5012170 未修复；这是来源漏洞发现，不扩写为扫描完成或补丁安装动作。
- 角色：主体 `none`；客体 `affected_endpoint_host`；载体 `none`；观察者 `source_product`。

| 来源字段 | SDM 候选目标 | 转换/保留策略 | 证据 |
|---|---|---|---|
| `clientip` | `roles.target.host.ip` | `identity` | `vendor_confirmed_and_observed` |
| `computername` | `roles.target.host.name` | `identity` | `vendor_confirmed_and_observed` |
| `id` | `source_finding.original_id` | `identity` | `vendor_confirmed_and_observed` |
| `kbid` | `source_finding.vulnerabilities[0].id` | `identity`；KBID 不冒充 CVE | `vendor_confirmed_and_observed` |
| `type` | `source_finding.status` | `unrepaired` 投影漏洞状态 | `vendor_confirmed_and_observed` |
| `name` | `source_finding.title` | `identity` | `vendor_confirmed_and_observed` |
| `repair_suggestions` | `source_finding.vulnerabilities[0].remediation` | `identity` | `vendor_confirmed_and_observed` |
| `severitylevel` | `source_finding.severity` | `identity`；不提升到顶层 severity | `vendor_confirmed_and_observed` |
| `status` | `extensions.source_private.status_raw` | `preserve_conflicted_raw`；不映射 outcome | `conflicted` |
| `summary` | `source_finding.vulnerabilities[0].description` | `identity` | `vendor_confirmed_and_observed` |
| `sysmaclist` | `roles.target.host.mac` | `identity` | `vendor_confirmed_and_observed` |
| `username` | `roles.target.user.name` | `identity` | `vendor_confirmed_and_observed` |

枚举/选择器信号：
- `type=unrepaired`：投影 `source_finding.status` 和漏洞 `type`，证据为 `vendor_confirmed_and_observed`。
- `status=unrepaired`：不在厂商文档列出的 status 操作状态枚举内，原值保留至 `extensions.source_private.status_raw`，证据为 `conflicted`。

## `360_netconnect_audit`

- 状态：`candidate`
- 证据：`sample_inferred`
- WPL 规则：360_netconnect_audit
- 样本：`log-model/examples/360/`，目录级非空行 9

| 来源字段 | SDM 候选目标 | 转换/保留策略 | 证据 |
|---|---|---|---|
| `ctime` | `occur_time` | `candidate_identity` | `sample_inferred` |
| `log_type` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `send_time` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `send_time_end` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `type` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |

枚举/选择器信号：
- 字段 `type`（has）；候选值 netconnect_audit；未知值策略：`preserve_raw_and_report`
