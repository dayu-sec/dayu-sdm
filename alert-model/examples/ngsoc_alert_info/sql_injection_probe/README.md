# SQL注入攻击_注入点探测

由 `log-model/examples/ngsoc/ngsoc_alert_info/sql_injection_probe/sql_injection_probe.expected-sdm-event.json` 导入为平台 `SOURCE_ALERT`。

| 项 | 值 |
|---|---|
| `alert_id` | `alert_09dc366ac3646791d4455c0f` |
| `alert_display_id` | `ALT-20241217-638E07B5` |
| `category_code` | `EXPLOIT` |
| `severity` | `HIGH` |
| 主对象 | `198.51.100.102` / `victim` |
| 证据行 | 2 |
| 实体行 | 4 |
| 分析行 | 3（GATE + 告警轮 AI + 案件轮 AI） |
| 告警轮 conclusion | `SUSPICIOUS` |
| GATE `next_hop` | `FULL_AGENT` |
| `case_id` | `case_6954a2a63ce2db0fa14a40b3` |
| 案件成员数 | 1 |
| `correlation_id` | `corr_837f4d97259f70e2` |

单独开案。`verdict` 仍为 `UNKNOWN`。
