# 定制-绕过堡垒机登录服务器

由 `log-model/examples/ngsoc/ngsoc_alert_info/bastion_host_bypass_login/bastion_host_bypass_login.expected-sdm-event.json` 导入为平台 `SOURCE_ALERT`。

| 项 | 值 |
|---|---|
| `alert_id` | `alert_cac6b6948ac0e4d7f34a8099` |
| `alert_display_id` | `ALT-20241128-C4C56EDE` |
| `category_code` | `AUTH_VIOLATION` |
| `severity` | `HIGH` |
| 主对象 | `192.0.2.115` / `victim` |
| 证据行 | 2 |
| 实体行 | 3 |
| 分析行 | 3（GATE + 告警轮 AI + 案件轮 AI） |
| 告警轮 conclusion | `SUSPICIOUS` |
| GATE `next_hop` | `FULL_AGENT` |
| `case_id` | `case_97aeb7833f170946650a8a9e` |
| 案件成员数 | 1 |
| `correlation_id` | `—` |

单独开案。`verdict` 仍为 `UNKNOWN`。
