# AsyncRAT远控木马活动事件

由 `log-model/examples/ngsoc/ngsoc_alert_info/asyncrat_activity/asyncrat_activity.expected-sdm-event.json` 导入为平台 `SOURCE_ALERT`。

| 项 | 值 |
|---|---|
| `alert_id` | `alert_427ccf5146ef6db645013d99` |
| `alert_display_id` | `ALT-20241218-FE7066C1` |
| `category_code` | `NETWORK_COMMAND_AND_CONTROL` |
| `severity` | `HIGH` |
| 主对象 | `192.0.2.38` / `victim` |
| 证据行 | 2 |
| 实体行 | 4 |
| 分析行 | 3（GATE + 告警轮 AI + 案件轮 AI） |
| 告警轮 conclusion | `SUSPICIOUS` |
| GATE `next_hop` | `FULL_AGENT` |
| `case_id` | `case_5624bff236402c87e964f6c0` |
| 案件成员数 | 1 |
| `correlation_id` | `—` |

单独开案。`verdict` 仍为 `UNKNOWN`。
