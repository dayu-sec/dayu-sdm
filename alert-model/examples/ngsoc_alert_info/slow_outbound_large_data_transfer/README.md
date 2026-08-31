# 预置-网络探针检测到内部主机对外慢速传输大量数据

由 `log-model/examples/ngsoc/ngsoc_alert_info/slow_outbound_large_data_transfer/slow_outbound_large_data_transfer.expected-sdm-event.json` 导入为平台 `SOURCE_ALERT`。

| 项 | 值 |
|---|---|
| `alert_id` | `alert_362aa7cd2f01b49e683459d3` |
| `alert_display_id` | `ALT-20241218-F12D3BC6` |
| `category_code` | `DATA_EXFILTRATION` |
| `severity` | `MEDIUM` |
| 主对象 | `198.51.100.180` / `affected` |
| 证据行 | 2 |
| 实体行 | 3 |
| 分析行 | 3（GATE + 告警轮 AI + 案件轮 AI） |
| 告警轮 conclusion | `SUSPICIOUS` |
| GATE `next_hop` | `FULL_AGENT` |
| `case_id` | `case_5c70827c010f9e3efee5b1dc` |
| 案件成员数 | 1 |
| `correlation_id` | `—` |

单独开案。`verdict` 仍为 `UNKNOWN`。
