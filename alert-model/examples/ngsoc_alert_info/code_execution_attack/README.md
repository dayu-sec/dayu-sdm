# 代码执行攻击

由 `log-model/examples/ngsoc/ngsoc_alert_info/code_execution_attack/code_execution_attack.expected-sdm-event.json` 导入为平台 `SOURCE_ALERT`。

| 项 | 值 |
|---|---|
| `alert_id` | `alert_15f1afd8bdbc1c9a59b8ce95` |
| `alert_display_id` | `ALT-20241128-E9FFF915` |
| `category_code` | `EXPLOIT` |
| `severity` | `HIGH` |
| 主对象 | `192.0.2.83` / `victim` |
| 证据行 | 2 |
| 实体行 | 4 |
| 分析行 | 3（GATE + 告警轮 AI + 案件轮 AI） |
| 告警轮 conclusion | `SUSPICIOUS` |
| GATE `next_hop` | `FULL_AGENT` |
| `case_id` | `case_41d8173dc2d82c2bcfee12cc` |
| 案件成员数 | 1 |
| `correlation_id` | `—` |

单独开案。`verdict` 仍为 `UNKNOWN`。
