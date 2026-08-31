# topas_firewall 字段映射与枚举候选

候选结果，未经标准注册审批。样本字段为源目录级证据；只有 WPL 规则块字段被归属到具体 log_type。

## `topas_firewall_ac`

- 状态：`candidate`
- 证据：`sample_inferred`
- WPL 规则：topas_firewall_ac
- 样本：`s4-doris/models/wpl/topas_firewall/sample.dat`，目录级非空行 4

| 来源字段 | SDM 候选目标 | 转换/保留策略 | 证据 |
|---|---|---|---|
| `action` | `outcome` | `candidate_identity` | `sample_inferred` |
| `appname` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dev` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dport` | `target_port` | `candidate_identity` | `sample_inferred` |
| `dst` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `id` | `event_id` | `candidate_identity` | `sample_inferred` |
| `index` | `event_id` | `candidate_identity` | `sample_inferred` |
| `policyid` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `policyname` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `pri` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `protoname` | `protocol` | `candidate_identity` | `sample_inferred` |
| `recorder` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `sport` | `source_port` | `candidate_identity` | `sample_inferred` |
| `src` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `time` | `occur_time` | `candidate_identity` | `sample_inferred` |
| `type` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `user` | `source_user` | `candidate_identity` | `sample_inferred` |
| `version` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `vsid` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `vsys_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |

枚举/选择器信号：
- 字段 `recorder`（has）；候选值 ac；未知值策略：`preserve_raw_and_report`

## `topas_firewall_admin`

- 状态：`candidate`
- 证据：`sample_inferred`
- WPL 规则：topas_firewall_admin
- 样本：`s4-doris/models/wpl/topas_firewall/sample.dat`，目录级非空行 4

| 来源字段 | SDM 候选目标 | 转换/保留策略 | 证据 |
|---|---|---|---|
| `description` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dev` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `id` | `event_id` | `candidate_identity` | `sample_inferred` |
| `index` | `event_id` | `candidate_identity` | `sample_inferred` |
| `method` | `http_method` | `candidate_identity` | `sample_inferred` |
| `op` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `pri` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `recorder` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `result` | `outcome` | `candidate_identity` | `sample_inferred` |
| `src` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `time` | `occur_time` | `candidate_identity` | `sample_inferred` |
| `type` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `user` | `source_user` | `candidate_identity` | `sample_inferred` |
| `version` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `vsid` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |

枚举/选择器信号：
- 字段 `recorder`（has）；候选值 admin；未知值策略：`preserve_raw_and_report`

