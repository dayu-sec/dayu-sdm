# dm_fired_alerts 字段映射与枚举候选

候选结果，未经标准注册审批。样本字段为源目录级证据；只有 WPL 规则块字段被归属到具体 log_type。

## `dm_fired_alerts`

- 状态：`partial`
- 证据：`sample_inferred`
- WPL 规则：dm_fired_alerts
- 样本：`log-model/examples/dm_fired_alerts/`，目录级非空行 1

| 来源字段 | SDM 候选目标 | 转换/保留策略 | 证据 |
|---|---|---|---|
| `CREATE_TIME` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `EARLIEST_TIME` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `LATEST_TIME` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `RECORDING_TIME` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `STATUS` | `outcome` | `candidate_identity` | `sample_inferred` |
| `UPDATE_TIME` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |

枚举/选择器信号：
- 字段 `warp_parse_table`（has）；候选值 FIRED_ALERTS；未知值策略：`preserve_raw_and_report`

开放问题：
- 未找到与该产品/格式直接对应的厂商字段文档
- FIRED_ALERTS 为平台安全审计表语义，缺厂商字段手册

