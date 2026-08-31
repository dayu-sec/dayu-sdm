# leadsec 字段映射与枚举候选

候选结果，未经标准注册审批。样本字段为源目录级证据；只有 WPL 规则块字段被归属到具体 log_type。

## `leadsec_av`

- 状态：`candidate`
- 证据：`sample_inferred`
- WPL 规则：leadsec_av
- 样本：`log-model/examples/leadsec/`，目录级非空行 18

| 来源字段 | SDM 候选目标 | 转换/保留策略 | 证据 |
|---|---|---|---|
| `act` | `roles.target.resource.action` | `normalize_add` | `vendor_confirmed_and_observed` |
| `date` | `occur_time` | `candidate_identity` | `sample_inferred` |
| `destaddr` | `target_ip` | `candidate_identity` | `sample_inferred` |
| `devid` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dname` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dsp_msg` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `from` | `source_ip` | `identity_admin_host_ip` | `vendor_confirmed_and_observed` |
| `fwlog` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `logtype` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `mod` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `name` | `roles.target.resource.name` | `identity_av_policy_name` | `vendor_confirmed_and_observed` |
| `obj` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `pri` | `log_level` | `identity_syslog_level` | `vendor_confirmed_and_observed` |
| `result` | `outcome` | `documented_result_0_to_success` | `vendor_confirmed_and_observed` |
| `type` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `user` | `source_user` | `identity_current_user` | `vendor_confirmed_and_observed` |

枚举/选择器信号：
- 字段 `logtype`（has）；候选值 9；未知值策略：`preserve_raw_and_report`

## `leadsec_ips`

- 状态：`candidate`
- 证据：`sample_inferred`
- WPL 规则：leadsec_ips
- 样本：`log-model/examples/leadsec/`，目录级非空行 18

| 来源字段 | SDM 候选目标 | 转换/保留策略 | 证据 |
|---|---|---|---|
| `action` | `outcome` | `candidate_identity` | `sample_inferred` |
| `app` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `date` | `occur_time` | `candidate_identity` | `sample_inferred` |
| `destaddr` | `target_ip` | `candidate_identity` | `sample_inferred` |
| `destport` | `target_port` | `candidate_identity` | `sample_inferred` |
| `destregion` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `devid` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dname` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dsp_msg` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `eventdetails` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `eventname` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `fwlog` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `if` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `logtype` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `pri` | `log_level` | `identity_syslog_level` | `vendor_confirmed_and_observed` |
| `protocol` | `protocol` | `candidate_identity` | `sample_inferred` |
| `repeated` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `severity` | `severity` | `candidate_identity` | `sample_inferred` |
| `srcaddr` | `source_ip` | `candidate_identity` | `sample_inferred` |
| `srcport` | `source_port` | `candidate_identity` | `sample_inferred` |
| `srcregion` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `user` | `source_user` | `identity_current_user` | `vendor_confirmed_and_observed` |

枚举/选择器信号：
- 字段 `logtype`（has）；候选值 16；未知值策略：`preserve_raw_and_report`

## `leadsec_vh`

- 状态：`candidate`
- 证据：`sample_inferred`
- WPL 规则：leadsec_vh
- 样本：`log-model/examples/leadsec/`，目录级非空行 18

| 来源字段 | SDM 候选目标 | 转换/保留策略 | 证据 |
|---|---|---|---|
| `date` | `occur_time` | `candidate_identity` | `sample_inferred` |
| `destaddr` | `target_ip` | `candidate_identity` | `sample_inferred` |
| `destport` | `target_port` | `candidate_identity` | `sample_inferred` |
| `devid` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dname` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `eventname` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `eventtype` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `fwlog` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `logtype` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `mod` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `pri` | `log_level` | `identity_syslog_level` | `vendor_confirmed_and_observed` |
| `protocol` | `protocol` | `candidate_identity` | `sample_inferred` |
| `srcaddr` | `source_ip` | `candidate_identity` | `sample_inferred` |
| `srcport` | `source_port` | `candidate_identity` | `sample_inferred` |
| `ver` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |

枚举/选择器信号：
- 字段 `logtype`（has）；候选值 15；未知值策略：`preserve_raw_and_report`

## `leadsec_vq`

- 状态：`candidate`
- 证据：`sample_inferred`
- WPL 规则：leadsec_vq
- 样本：`log-model/examples/leadsec/`，目录级非空行 18

| 来源字段 | SDM 候选目标 | 转换/保留策略 | 证据 |
|---|---|---|---|
| `date` | `occur_time` | `candidate_identity` | `sample_inferred` |
| `destaddr` | `target_ip` | `candidate_identity` | `sample_inferred` |
| `destport` | `target_port` | `candidate_identity` | `sample_inferred` |
| `devid` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dname` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `eventname` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `eventtype` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `fwlog` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `logtype` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `mod` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `pri` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `protocol` | `protocol` | `candidate_identity` | `sample_inferred` |
| `srcaddr` | `source_ip` | `candidate_identity` | `sample_inferred` |
| `srcport` | `source_port` | `candidate_identity` | `sample_inferred` |
| `ver` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |

枚举/选择器信号：
- 字段 `logtype`（has）；候选值 14；未知值策略：`preserve_raw_and_report`

## `leadsec_waf`

- 状态：`candidate`
- 证据：`sample_inferred`
- WPL 规则：leadsec_waf
- 样本：`log-model/examples/leadsec/`，目录级非空行 18

| 来源字段 | SDM 候选目标 | 转换/保留策略 | 证据 |
|---|---|---|---|
| `action` | `outcome` | `candidate_identity` | `sample_inferred` |
| `app` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `date` | `occur_time` | `candidate_identity` | `sample_inferred` |
| `destaddr` | `target_ip` | `candidate_identity` | `sample_inferred` |
| `destport` | `target_port` | `candidate_identity` | `sample_inferred` |
| `destregion` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `devid` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dname` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dsp_msg` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `eventdetails` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `eventname` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `fwlog` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `if` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `logtype` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `pri` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `protocol` | `protocol` | `candidate_identity` | `sample_inferred` |
| `repeated` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `severity` | `severity` | `candidate_identity` | `sample_inferred` |
| `srcaddr` | `source_ip` | `candidate_identity` | `sample_inferred` |
| `srcport` | `source_port` | `candidate_identity` | `sample_inferred` |
| `srcregion` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `user` | `source_user` | `identity_current_user` | `vendor_confirmed_and_observed` |

枚举/选择器信号：
- 字段 `logtype`（has）；候选值 29；未知值策略：`preserve_raw_and_report`

