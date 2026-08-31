# SQL注入攻击

由 `log-model/examples/ngsoc/ngsoc_alert_info/sql_injection_attempt/sql_injection_attempt.expected-sdm-event.json` 导入为平台 `SOURCE_ALERT`。

| 项 | 值 |
|---|---|
| `alert_id` | `alert_27d1706a8d1dbf0cfa17b465` |
| `alert_display_id` | `ALT-20241218-D74528BE` |
| `category_code` | `EXPLOIT` |
| `severity` | `HIGH` |
| 主对象 | `203.0.113.228` / `victim` |
| 证据行 | 3 |
| 实体行 | 5 |
| 分析行 | 3（GATE + 告警轮 AI + 案件轮 AI） |
| 告警轮 conclusion | `SUSPICIOUS` |
| GATE `next_hop` | `FULL_AGENT` |
| `case_id` | `case_59782e57543384097b85dcfc` |
| 案件成员数 | 4 |
| `correlation_id` | `corr_42aaea032af935ce` |

本条与同受害 IP、同时段的其他 SQL 注入共享一个 INVESTIGATION。

查询聚合见 [`alert.detail.json`](alert.detail.json)，只含告警轮分析；案件叙事见案件详情。
