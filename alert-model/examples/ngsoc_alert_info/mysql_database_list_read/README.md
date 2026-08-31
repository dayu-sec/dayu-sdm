# MySQL 读取数据库列表

由 `log-model/examples/ngsoc/ngsoc_alert_info/mysql_database_list_read/mysql_database_list_read.expected-sdm-event.json` 导入为平台 `SOURCE_ALERT`。

| 项 | 值 |
|---|---|
| `alert_id` | `alert_27f4d1fc0d51dc727f3a9626` |
| `alert_display_id` | `ALT-20241129-94B0661F` |
| `category_code` | `ACL_VIOLATION` |
| `severity` | `MEDIUM` |
| 主对象 | `198.51.100.100` / `victim` |
| 证据行 | 2 |
| 实体行 | 3 |
| 分析行 | 3（GATE + 告警轮 AI + 案件轮 AI） |
| 告警轮 conclusion | `SUSPICIOUS` |
| GATE `next_hop` | `FULL_AGENT` |
| `case_id` | `case_f9e893941b133171fb567428` |
| 案件成员数 | 1 |
| `correlation_id` | `—` |

单独开案。`verdict` 仍为 `UNKNOWN`。
