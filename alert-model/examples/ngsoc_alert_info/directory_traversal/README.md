# 目录遍历攻击(通用)

由 `log-model/examples/ngsoc/ngsoc_alert_info/directory_traversal/directory_traversal.expected-sdm-event.json` 导入为平台 `SOURCE_ALERT`。

| 项 | 值 |
|---|---|
| `alert_id` | `alert_d0c60a293705a2c192edc258` |
| `alert_display_id` | `ALT-20241218-AA75E623` |
| `category_code` | `EXPLOIT` |
| `severity` | `MEDIUM` |
| 主对象 | `198.51.100.139` / `victim` |
| 证据行 | 2 |
| 实体行 | 4 |
| 分析行 | 3（GATE + 告警轮 AI + 案件轮 AI） |
| 告警轮 conclusion | `SUSPICIOUS` |
| GATE `next_hop` | `FULL_AGENT` |
| `case_id` | `case_03b1f02b5cff5a3fcfd6fc48` |
| 案件成员数 | 1 |
| `correlation_id` | `—` |

单独开案。`verdict` 仍为 `UNKNOWN`。
