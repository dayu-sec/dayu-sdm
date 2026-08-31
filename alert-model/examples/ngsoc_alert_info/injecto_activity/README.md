# Injecto远控木马活动事件

由 `log-model/examples/ngsoc/ngsoc_alert_info/injecto_activity/injecto_activity.expected-sdm-event.json` 导入为平台 `SOURCE_ALERT`。

| 项 | 值 |
|---|---|
| `alert_id` | `alert_1a516474aa7a7ec473833f34` |
| `alert_display_id` | `ALT-20241218-4CA6B469` |
| `category_code` | `NETWORK_COMMAND_AND_CONTROL` |
| `severity` | `HIGH` |
| 主对象 | `203.0.113.143` / `victim` |
| 证据行 | 2 |
| 实体行 | 4 |
| 分析行 | 3（GATE + 告警轮 AI + 案件轮 AI） |
| 告警轮 conclusion | `SUSPICIOUS` |
| GATE `next_hop` | `FULL_AGENT` |
| `case_id` | `case_c6f1a1b5ec84412f81739cf7` |
| 案件成员数 | 1 |
| `correlation_id` | `—` |

单独开案。`verdict` 仍为 `UNKNOWN`。
