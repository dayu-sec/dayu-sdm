# topas_ips 字段映射与枚举候选

候选结果，未经标准注册审批。样本字段为源目录级证据；只有 WPL 规则块字段被归属到具体 log_type。

## `topas_ips_attack`

- 状态：`candidate`
- 证据：`sample_inferred`
- WPL 规则：topas_ips_attack
- 样本：`log-model/examples/topas_ips/`，目录级非空行 9

| 来源字段 | SDM 候选目标 | 转换/保留策略 | 证据 |
|---|---|---|---|
| `app` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `app_pro` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `appendix` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `client` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `cve` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `ddev` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dev_ip` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dev_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dev_type` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dgeo` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dip` | `target_ip` | `candidate_identity` | `sample_inferred` |
| `dipv6` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `direction` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dmac` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dport` | `target_port` | `candidate_identity` | `sample_inferred` |
| `file` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `fingerprint` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `index` | `event_id` | `candidate_identity` | `sample_inferred` |
| `level` | `severity` | `candidate_identity` | `sample_inferred` |
| `method` | `http_method` | `candidate_identity` | `sample_inferred` |
| `msg` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `op` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `proto` | `protocol` | `candidate_identity` | `sample_inferred` |
| `recorder` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `repeat` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `req_body` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `req_header` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `resp_body` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `resp_header` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `response_code` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `result` | `outcome` | `candidate_identity` | `sample_inferred` |
| `rule` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `sdev` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `server` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `sgeo` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `sid` | `event_id` | `candidate_identity` | `sample_inferred` |
| `sip` | `source_ip` | `candidate_identity` | `sample_inferred` |
| `sipv6` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `smac` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `sport` | `source_port` | `candidate_identity` | `sample_inferred` |
| `sub_type` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `time` | `occur_time` | `candidate_identity` | `sample_inferred` |
| `type` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `vendor` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `vid` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `x_forwarded_for` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `x_real_ip` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |

枚举/选择器信号：
- 字段 `recorder`（has）；候选值 attack；未知值策略：`preserve_raw_and_report`

## `topas_ips_audit_db`

- 状态：`candidate`
- 证据：`sample_inferred`
- WPL 规则：topas_ips_audit_db
- 样本：`log-model/examples/topas_ips/`，目录级非空行 9

| 来源字段 | SDM 候选目标 | 转换/保留策略 | 证据 |
|---|---|---|---|
| `command` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dbname` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dbtype` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `ddev` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dev_ip` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dev_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dev_type` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dip` | `target_ip` | `candidate_identity` | `sample_inferred` |
| `dipv6` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dmac` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dport` | `target_port` | `candidate_identity` | `sample_inferred` |
| `index` | `event_id` | `candidate_identity` | `sample_inferred` |
| `password` | `REDACTED` | `preserve_raw_to_source_private` | `sample_inferred` |
| `proto` | `protocol` | `candidate_identity` | `sample_inferred` |
| `recorder` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `retcode` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `retmsg` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `sdev` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `sid` | `event_id` | `candidate_identity` | `sample_inferred` |
| `sip` | `source_ip` | `candidate_identity` | `sample_inferred` |
| `sipv6` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `smac` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `sport` | `source_port` | `candidate_identity` | `sample_inferred` |
| `time` | `occur_time` | `candidate_identity` | `sample_inferred` |
| `username` | `source_user` | `candidate_identity` | `sample_inferred` |
| `vendor` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `version` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `vid` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |

枚举/选择器信号：
- 字段 `recorder`（has）；候选值 audit_db；未知值策略：`preserve_raw_and_report`

## `topas_ips_audit_file`

- 状态：`candidate`
- 证据：`sample_inferred`
- WPL 规则：topas_ips_audit_file
- 样本：`log-model/examples/topas_ips/`，目录级非空行 9

| 来源字段 | SDM 候选目标 | 转换/保留策略 | 证据 |
|---|---|---|---|
| `application` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `ddev` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dev_ip` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dev_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dev_type` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dip` | `target_ip` | `candidate_identity` | `sample_inferred` |
| `dipv6` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `direction` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dmac` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dport` | `target_port` | `candidate_identity` | `sample_inferred` |
| `file` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `filesize` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `filetype` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `index` | `event_id` | `candidate_identity` | `sample_inferred` |
| `md5` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `proto` | `protocol` | `candidate_identity` | `sample_inferred` |
| `recorder` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `sdev` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `sid` | `event_id` | `candidate_identity` | `sample_inferred` |
| `sip` | `source_ip` | `candidate_identity` | `sample_inferred` |
| `sipv6` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `smac` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `sport` | `source_port` | `candidate_identity` | `sample_inferred` |
| `time` | `occur_time` | `candidate_identity` | `sample_inferred` |
| `vendor` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `vid` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |

枚举/选择器信号：
- 字段 `recorder`（has）；候选值 audit_file；未知值策略：`preserve_raw_and_report`

## `topas_ips_audit_ftp`

- 状态：`candidate`
- 证据：`sample_inferred`
- WPL 规则：topas_ips_audit_ftp
- 样本：`log-model/examples/topas_ips/`，目录级非空行 9

| 来源字段 | SDM 候选目标 | 转换/保留策略 | 证据 |
|---|---|---|---|
| `cmd` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `ddev` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dev_ip` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dev_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dev_type` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dip` | `target_ip` | `candidate_identity` | `sample_inferred` |
| `dipv6` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dmac` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dport` | `target_port` | `candidate_identity` | `sample_inferred` |
| `file` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `index` | `event_id` | `candidate_identity` | `sample_inferred` |
| `proto` | `protocol` | `candidate_identity` | `sample_inferred` |
| `recorder` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `ret` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `ret_code` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `sdev` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `sid` | `event_id` | `candidate_identity` | `sample_inferred` |
| `sip` | `source_ip` | `candidate_identity` | `sample_inferred` |
| `sipv6` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `smac` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `sport` | `source_port` | `candidate_identity` | `sample_inferred` |
| `time` | `occur_time` | `candidate_identity` | `sample_inferred` |
| `user` | `source_user` | `candidate_identity` | `sample_inferred` |
| `vendor` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `vid` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |

枚举/选择器信号：
- 字段 `recorder`（has）；候选值 audit_ftp；未知值策略：`preserve_raw_and_report`

## `topas_ips_audit_ldap`

- 状态：`candidate`
- 证据：`sample_inferred`
- WPL 规则：topas_ips_audit_ldap
- 样本：`log-model/examples/topas_ips/`，目录级非空行 9

| 来源字段 | SDM 候选目标 | 转换/保留策略 | 证据 |
|---|---|---|---|
| `ddev` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dev_ip` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dev_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dev_type` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dip` | `target_ip` | `candidate_identity` | `sample_inferred` |
| `dipv6` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dmac` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dport` | `target_port` | `candidate_identity` | `sample_inferred` |
| `index` | `event_id` | `candidate_identity` | `sample_inferred` |
| `password` | `REDACTED` | `preserve_raw_to_source_private` | `sample_inferred` |
| `proto` | `protocol` | `candidate_identity` | `sample_inferred` |
| `recorder` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `sdev` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `sid` | `event_id` | `candidate_identity` | `sample_inferred` |
| `sip` | `source_ip` | `candidate_identity` | `sample_inferred` |
| `sipv6` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `smac` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `sport` | `source_port` | `candidate_identity` | `sample_inferred` |
| `time` | `occur_time` | `candidate_identity` | `sample_inferred` |
| `username` | `source_user` | `candidate_identity` | `sample_inferred` |
| `vendor` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `version` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `vid` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |

枚举/选择器信号：
- 字段 `recorder`（has）；候选值 audit_ldap；未知值策略：`preserve_raw_and_report`

## `topas_ips_audit_nfs`

- 状态：`candidate`
- 证据：`sample_inferred`
- WPL 规则：topas_ips_audit_nfs
- 样本：`log-model/examples/topas_ips/`，目录级非空行 9

| 来源字段 | SDM 候选目标 | 转换/保留策略 | 证据 |
|---|---|---|---|
| `ddev` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `deal_size` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dev_ip` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dev_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dev_type` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dip` | `target_ip` | `candidate_identity` | `sample_inferred` |
| `dipv6` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dmac` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dport` | `target_port` | `candidate_identity` | `sample_inferred` |
| `file_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `file_size` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `index` | `event_id` | `candidate_identity` | `sample_inferred` |
| `nfs_op` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `nfs_proc` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `nfs_version` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `operation` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `proto` | `protocol` | `candidate_identity` | `sample_inferred` |
| `recorder` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `result` | `outcome` | `candidate_identity` | `sample_inferred` |
| `sdev` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `sid` | `event_id` | `candidate_identity` | `sample_inferred` |
| `sip` | `source_ip` | `candidate_identity` | `sample_inferred` |
| `sipv6` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `smac` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `sport` | `source_port` | `candidate_identity` | `sample_inferred` |
| `time` | `occur_time` | `candidate_identity` | `sample_inferred` |
| `vendor` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `vid` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |

枚举/选择器信号：
- 字段 `recorder`（has）；候选值 audit_nfs；未知值策略：`preserve_raw_and_report`

## `topas_ips_audit_rdp`

- 状态：`candidate`
- 证据：`sample_inferred`
- WPL 规则：topas_ips_audit_rdp
- 样本：`log-model/examples/topas_ips/`，目录级非空行 9

| 来源字段 | SDM 候选目标 | 转换/保留策略 | 证据 |
|---|---|---|---|
| `ddev` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dev_ip` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dev_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dev_type` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dip` | `target_ip` | `candidate_identity` | `sample_inferred` |
| `dipv6` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dmac` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dport` | `target_port` | `candidate_identity` | `sample_inferred` |
| `index` | `event_id` | `candidate_identity` | `sample_inferred` |
| `password` | `REDACTED` | `preserve_raw_to_source_private` | `sample_inferred` |
| `proto` | `protocol` | `candidate_identity` | `sample_inferred` |
| `recorder` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `sdev` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `sid` | `event_id` | `candidate_identity` | `sample_inferred` |
| `sip` | `source_ip` | `candidate_identity` | `sample_inferred` |
| `sipv6` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `smac` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `sport` | `source_port` | `candidate_identity` | `sample_inferred` |
| `time` | `occur_time` | `candidate_identity` | `sample_inferred` |
| `username` | `source_user` | `candidate_identity` | `sample_inferred` |
| `vendor` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `vid` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |

枚举/选择器信号：
- 字段 `recorder`（has）；候选值 audit_rdp；未知值策略：`preserve_raw_and_report`

## `topas_ips_audit_smb`

- 状态：`candidate`
- 证据：`sample_inferred`
- WPL 规则：topas_ips_audit_smb
- 样本：`log-model/examples/topas_ips/`，目录级非空行 9

| 来源字段 | SDM 候选目标 | 转换/保留策略 | 证据 |
|---|---|---|---|
| `ddev` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `deal_size` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dev_ip` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dev_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dev_type` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dip` | `target_ip` | `candidate_identity` | `sample_inferred` |
| `dipv6` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dmac` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dport` | `target_port` | `candidate_identity` | `sample_inferred` |
| `file_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `file_size` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `host_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `index` | `event_id` | `candidate_identity` | `sample_inferred` |
| `operation` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `proto` | `protocol` | `candidate_identity` | `sample_inferred` |
| `recorder` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `result` | `outcome` | `candidate_identity` | `sample_inferred` |
| `sdev` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `session_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `sid` | `event_id` | `candidate_identity` | `sample_inferred` |
| `sip` | `source_ip` | `candidate_identity` | `sample_inferred` |
| `sipv6` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `smac` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `smb_cmd` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `smb_version` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `sport` | `source_port` | `candidate_identity` | `sample_inferred` |
| `time` | `occur_time` | `candidate_identity` | `sample_inferred` |
| `tree_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `user_name` | `source_user` | `candidate_identity` | `sample_inferred` |
| `vendor` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `vid` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |

枚举/选择器信号：
- 字段 `recorder`（has）；候选值 audit_smb；未知值策略：`preserve_raw_and_report`

## `topas_ips_virus`

- 状态：`candidate`
- 证据：`sample_inferred`
- WPL 规则：topas_ips_virus
- 样本：`log-model/examples/topas_ips/`，目录级非空行 9

| 来源字段 | SDM 候选目标 | 转换/保留策略 | 证据 |
|---|---|---|---|
| `app` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `app_pro` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `appendix` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `ddev` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dev_ip` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dev_name` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dev_type` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dgeo` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dip` | `target_ip` | `candidate_identity` | `sample_inferred` |
| `dipv6` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `direction` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dmac` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dport` | `target_port` | `candidate_identity` | `sample_inferred` |
| `file` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `filesize` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `filetype` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `index` | `event_id` | `candidate_identity` | `sample_inferred` |
| `level` | `severity` | `candidate_identity` | `sample_inferred` |
| `md5` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `method` | `http_method` | `candidate_identity` | `sample_inferred` |
| `msg` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `op` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `proto` | `protocol` | `candidate_identity` | `sample_inferred` |
| `recorder` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `repeat` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `rule` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `sdev` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `sgeo` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `sha1` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `sid` | `event_id` | `candidate_identity` | `sample_inferred` |
| `sip` | `source_ip` | `candidate_identity` | `sample_inferred` |
| `sipv6` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `smac` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `sport` | `source_port` | `candidate_identity` | `sample_inferred` |
| `sub_type` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `time` | `occur_time` | `candidate_identity` | `sample_inferred` |
| `type` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `vendor` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `vid` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |

枚举/选择器信号：
- 字段 `recorder`（has）；候选值 virus；未知值策略：`preserve_raw_and_report`
- 字段 `type`（has）；候选值 11；未知值策略：`preserve_raw_and_report`

