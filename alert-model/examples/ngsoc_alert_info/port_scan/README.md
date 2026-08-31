# 端口扫描

由 `log-model/examples/ngsoc/ngsoc_alert_info/port_scan/port_scan.expected-sdm-event.json` 导入为平台 `SOURCE_ALERT`。

| 项 | 值 |
|---|---|
| `alert_id` | `alert_a1b535fb5a750c24a46e259c` |
| `alert_display_id` | `ALT-20241129-F99471DB` |
| `category_code` | `NETWORK_RECON` |
| `severity` | `MEDIUM` |
| 主对象 | `192.0.2.59` / `victim` |
| 证据行 | 2 |
| 实体行 | 4 |
| 分析行 | 3（GATE + 告警轮 AI + 案件轮 AI） |
| 告警轮 conclusion | `SUSPICIOUS` |
| GATE `next_hop` | `FULL_AGENT` |
| `case_id` | `case_c476fc8931245330069f89f5` |
| 案件成员数 | 1 |
| `correlation_id` | `—` |

单独开案。`verdict` 仍为 `UNKNOWN`。
