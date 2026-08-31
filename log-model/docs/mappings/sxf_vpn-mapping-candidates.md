# sxf_vpn 字段映射与枚举候选

候选结果，未经标准注册审批。样本字段为源目录级证据；只有 WPL 规则块字段被归属到具体 log_type。

## `sslvpn_manage_log`

- 状态：`candidate`
- 证据：`sample_inferred`
- WPL 规则：sslvpn_manage_log
- 样本：`log-model/examples/sxf_vpn/`，目录级非空行 16

| 来源字段 | SDM 候选目标 | 转换/保留策略 | 证据 |
|---|---|---|---|
| `time` | `occur_time` | `candidate_identity` | `sample_inferred` |
| `time_timestamp` | `occur_time` | `candidate_identity` | `sample_inferred` |

开放问题：
- 现有 AC XLSX 与 SVPN-USR/SYSTEM/ADMIN JSON 样本不完全匹配

## `sslvpn_manager_log`

- 状态：`candidate`
- 证据：`sample_inferred`
- WPL 规则：sslvpn_manager_log
- 样本：`log-model/examples/sxf_vpn/`，目录级非空行 16

| 来源字段 | SDM 候选目标 | 转换/保留策略 | 证据 |
|---|---|---|---|
| `time` | `occur_time` | `candidate_identity` | `sample_inferred` |
| `time_timestamp` | `occur_time` | `candidate_identity` | `sample_inferred` |

开放问题：
- 现有 AC XLSX 与 SVPN-USR/SYSTEM/ADMIN JSON 样本不完全匹配

## `sslvpn_user_log`

- 状态：`candidate`
- 证据：`sample_inferred`
- WPL 规则：sslvpn_user_log
- 样本：`log-model/examples/sxf_vpn/`，目录级非空行 16

| 来源字段 | SDM 候选目标 | 转换/保留策略 | 证据 |
|---|---|---|---|
| `groupId` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `groupPath` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `time` | `occur_time` | `candidate_identity` | `sample_inferred` |
| `time_timestamp` | `occur_time` | `candidate_identity` | `sample_inferred` |
| `userInfo` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |

开放问题：
- 现有 AC XLSX 与 SVPN-USR/SYSTEM/ADMIN JSON 样本不完全匹配

