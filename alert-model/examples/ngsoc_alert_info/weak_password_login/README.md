# 弱口令登录

由 `log-model/examples/ngsoc/ngsoc_alert_info/weak_password_login/weak_password_login.expected-sdm-event.json` 导入为平台 `SOURCE_ALERT`。

| 项 | 值 |
|---|---|
| `alert_id` | `alert_8c471fee2c74c8eec947663d` |
| `alert_display_id` | `ALT-20241129-84B83D74` |
| `category_code` | `AUTH_VIOLATION` |
| `severity` | `MEDIUM` |
| 主对象 | `203.0.113.28` / `victim` |
| 证据行 | 3 |
| 实体行 | 3 |
| 分析行 | 3（GATE + 告警轮 AI + 案件轮 AI） |
| 告警轮 conclusion | `SUSPICIOUS` |
| GATE `next_hop` | `FULL_AGENT` |
| `case_id` | `case_51f38564698851cacc521ada` |
| 案件成员数 | 1 |
| `correlation_id` | `—` |

单独开案。`verdict` 仍为 `UNKNOWN`。
