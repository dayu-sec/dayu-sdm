# SQL注入攻击_SLEEP休眠函数注入

由 `log-model/examples/ngsoc/ngsoc_alert_info/sql_injection_sleep_function/sql_injection_sleep_function.expected-sdm-event.json` 导入为平台 `SOURCE_ALERT`。

| 项 | 值 |
|---|---|
| `alert_id` | `alert_b8394e3bb27f24b31765a384` |
| `alert_display_id` | `ALT-20241218-A26FBA8B` |
| `category_code` | `EXPLOIT` |
| `severity` | `HIGH` |
| 主对象 | `192.0.2.146` / `victim` |
| 证据行 | 2 |
| 实体行 | 5 |
| 分析行 | 3（GATE + 告警轮 AI + 案件轮 AI） |
| 告警轮 conclusion | `SUSPICIOUS` |
| GATE `next_hop` | `FULL_AGENT` |
| `case_id` | `case_59782e57543384097b85dcfc` |
| 案件成员数 | 4 |
| `correlation_id` | `corr_42aaea032af935ce` |

本条与同受害 IP、同时段的其他 SQL 注入共享一个 INVESTIGATION。
