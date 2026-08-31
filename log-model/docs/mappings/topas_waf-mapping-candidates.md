# topas_waf 字段映射与枚举候选

候选结果，未经标准注册审批。样本字段为源目录级证据；只有 WPL 规则块字段被归属到具体 log_type。

## `topas_waf_ads_attack`

- 状态：`candidate`
- 证据：`sample_inferred`
- WPL 规则：topas_waf_ads_attack
- 样本：`log-model/examples/topas_waf/`，目录级非空行 5

| 来源字段 | SDM 候选目标 | 转换/保留策略 | 证据 |
|---|---|---|---|
| `action` | `outcome` | `candidate_identity` | `sample_inferred` |
| `attack_bytes` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `attack_msgs` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `attack_packets` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `attack_status` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `attack_type` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `cur_cfg_value` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `cur_time` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `defense_method` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dev` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `hiredate` | `occur_time` | `candidate_identity` | `sample_inferred` |
| `id` | `event_id` | `candidate_identity` | `sample_inferred` |
| `policy_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `pri` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `recorder` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `service` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `src_addr_list` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `total_bytes` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `total_packets` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `type` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `unit` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `version` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `vsid` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `zone_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |

枚举/选择器信号：
- 字段 `recorder`（has）；候选值 ads_attack；未知值策略：`preserve_raw_and_report`
- 字段 `type`（has）；候选值 waf；未知值策略：`preserve_raw_and_report`

## `topas_waf_attack`

- 状态：`candidate`
- 证据：`sample_inferred`
- WPL 规则：topas_waf_attack
- 样本：`log-model/examples/topas_waf/`，目录级非空行 5

| 来源字段 | SDM 候选目标 | 转换/保留策略 | 证据 |
|---|---|---|---|
| `action` | `outcome` | `candidate_identity` | `sample_inferred` |
| `action_data` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `client_ip` | `source_ip` | `candidate_identity` | `sample_inferred` |
| `dev` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dport` | `target_port` | `candidate_identity` | `sample_inferred` |
| `event_type` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `hiredate` | `occur_time` | `candidate_identity` | `sample_inferred` |
| `host` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `http_args` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `http_detail` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `http_method` | `http_method` | `candidate_identity` | `sample_inferred` |
| `http_referer` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `http_status` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `http_useragent` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `id` | `event_id` | `candidate_identity` | `sample_inferred` |
| `msg` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `pri` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `protocol` | `protocol` | `candidate_identity` | `sample_inferred` |
| `real_ip` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `recorder` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `reqhdr` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `rsphdr` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `rule_id` | `event_id` | `candidate_identity` | `sample_inferred` |
| `server` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `server_ip` | `target_ip` | `candidate_identity` | `sample_inferred` |
| `severity` | `severity` | `candidate_identity` | `sample_inferred` |
| `sport` | `source_port` | `candidate_identity` | `sample_inferred` |
| `type` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `url` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `version` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `vsid` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |

枚举/选择器信号：
- 字段 `recorder`（has）；候选值 waf_attack；未知值策略：`preserve_raw_and_report`
- 字段 `type`（has）；候选值 waf；未知值策略：`preserve_raw_and_report`

## `topas_waf_tamper`

- 状态：`candidate`
- 证据：`sample_inferred`
- WPL 规则：topas_waf_tamper
- 样本：`log-model/examples/topas_waf/`，目录级非空行 5

| 来源字段 | SDM 候选目标 | 转换/保留策略 | 证据 |
|---|---|---|---|
| `dev` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `domain` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `event` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `filename` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `hiredate` | `occur_time` | `candidate_identity` | `sample_inferred` |
| `id` | `event_id` | `candidate_identity` | `sample_inferred` |
| `pri` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `recorder` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `server_ip` | `target_ip` | `candidate_identity` | `sample_inferred` |
| `type` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `version` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `vsid` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |

枚举/选择器信号：
- 字段 `recorder`（has）；候选值 waf_tamper；未知值策略：`preserve_raw_and_report`
- 字段 `type`（has）；候选值 waf；未知值策略：`preserve_raw_and_report`

## `topas_waf_traffic`

- 状态：`candidate`
- 证据：`sample_inferred`
- WPL 规则：topas_waf_traffic
- 样本：`log-model/examples/topas_waf/`，目录级非空行 5

| 来源字段 | SDM 候选目标 | 转换/保留策略 | 证据 |
|---|---|---|---|
| `client_ip` | `source_ip` | `candidate_identity` | `sample_inferred` |
| `dev` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `downstream` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dport` | `target_port` | `candidate_identity` | `sample_inferred` |
| `host` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `http_args` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `http_method` | `http_method` | `candidate_identity` | `sample_inferred` |
| `http_referer` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `http_status` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `http_useragent` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `id` | `event_id` | `candidate_identity` | `sample_inferred` |
| `pri` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `protocol` | `protocol` | `candidate_identity` | `sample_inferred` |
| `real_ip` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `recorder` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `server` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `server_ip` | `target_ip` | `candidate_identity` | `sample_inferred` |
| `sport` | `source_port` | `candidate_identity` | `sample_inferred` |
| `time` | `occur_time` | `candidate_identity` | `sample_inferred` |
| `type` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `upstream` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `url` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `version` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `vsid` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |

枚举/选择器信号：
- 字段 `recorder`（has）；候选值 waf_traffic；未知值策略：`preserve_raw_and_report`
- 字段 `type`（has）；候选值 waf；未知值策略：`preserve_raw_and_report`

## `topas_waf_virus`

- 状态：`candidate`
- 证据：`sample_inferred`
- WPL 规则：topas_waf_virus
- 样本：`log-model/examples/topas_waf/`，目录级非空行 5

| 来源字段 | SDM 候选目标 | 转换/保留策略 | 证据 |
|---|---|---|---|
| `action` | `outcome` | `candidate_identity` | `sample_inferred` |
| `action_data` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `client_ip` | `source_ip` | `candidate_identity` | `sample_inferred` |
| `dev` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dport` | `target_port` | `candidate_identity` | `sample_inferred` |
| `filename` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `hiredate` | `occur_time` | `candidate_identity` | `sample_inferred` |
| `host` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `http_args` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `http_method` | `http_method` | `candidate_identity` | `sample_inferred` |
| `http_referer` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `http_status` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `http_useragent` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `id` | `event_id` | `candidate_identity` | `sample_inferred` |
| `pri` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `protocol` | `protocol` | `candidate_identity` | `sample_inferred` |
| `real_ip` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `recorder` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `server` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `server_ip` | `target_ip` | `candidate_identity` | `sample_inferred` |
| `sport` | `source_port` | `candidate_identity` | `sample_inferred` |
| `type` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `url` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `version` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `vsid` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |

枚举/选择器信号：
- 字段 `recorder`（has）；候选值 virus；未知值策略：`preserve_raw_and_report`
- 字段 `type`（has）；候选值 waf；未知值策略：`preserve_raw_and_report`

