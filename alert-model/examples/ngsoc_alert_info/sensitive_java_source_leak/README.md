# 敏感信息泄露_Java源码泄露

由 `log-model/examples/ngsoc/ngsoc_alert_info/sensitive_java_source_leak/sensitive_java_source_leak.expected-sdm-event.json` 导入为平台 `SOURCE_ALERT`。

| 项 | 值 |
|---|---|
| `alert_id` | `alert_99fb41b9232512ff838abc32` |
| `alert_display_id` | `ALT-20241129-6D469083` |
| `category_code` | `DATA_AT_REST` |
| `severity` | `HIGH` |
| 主对象 | `192.0.2.234` / `victim` |
| 证据行 | 2 |
| 实体行 | 3 |
| 分析行 | 3（GATE + 告警轮 AI + 案件轮 AI） |
| 告警轮 conclusion | `SUSPICIOUS` |
| GATE `next_hop` | `FULL_AGENT` |
| `case_id` | `case_6a4f2e90e3c6118d2ae08d14` |
| 案件成员数 | 1 |
| `correlation_id` | `—` |

单独开案。`verdict` 仍为 `UNKNOWN`。
