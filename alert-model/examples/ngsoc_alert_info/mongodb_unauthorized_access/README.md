# MongoDB未授权访问

由 `log-model/examples/ngsoc/ngsoc_alert_info/mongodb_unauthorized_access/mongodb_unauthorized_access.expected-sdm-event.json` 导入为平台 `SOURCE_ALERT`。

| 项 | 值 |
|---|---|
| `alert_id` | `alert_39777e7a0aedfe871287b575` |
| `alert_display_id` | `ALT-20241217-ED11D883` |
| `category_code` | `ACL_VIOLATION` |
| `severity` | `HIGH` |
| 主对象 | `198.51.100.213` / `victim` |
| 证据行 | 3 |
| 实体行 | 3 |
| 分析行 | 3（GATE + 告警轮 AI + 案件轮 AI） |
| 告警轮 conclusion | `SUSPICIOUS` |
| GATE `next_hop` | `FULL_AGENT` |
| `case_id` | `case_9d02c452eafb220f6a76e014` |
| 案件成员数 | 1 |
| `correlation_id` | `—` |

单独开案。`verdict` 仍为 `UNKNOWN`。
