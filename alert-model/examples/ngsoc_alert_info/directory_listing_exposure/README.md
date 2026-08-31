# 目录列表泄露

由 `log-model/examples/ngsoc/ngsoc_alert_info/directory_listing_exposure/directory_listing_exposure.expected-sdm-event.json` 导入为平台 `SOURCE_ALERT`。

| 项 | 值 |
|---|---|
| `alert_id` | `alert_6cf9d627adf89e598ede56a4` |
| `alert_display_id` | `ALT-20241129-F3A14C40` |
| `category_code` | `DATA_AT_REST` |
| `severity` | `HIGH` |
| 主对象 | `198.51.100.178` / `victim` |
| 证据行 | 2 |
| 实体行 | 3 |
| 分析行 | 3（GATE + 告警轮 AI + 案件轮 AI） |
| 告警轮 conclusion | `SUSPICIOUS` |
| GATE `next_hop` | `FULL_AGENT` |
| `case_id` | `case_2ea8e3f29f54c357ba7e58fc` |
| 案件成员数 | 1 |
| `correlation_id` | `—` |

单独开案。`verdict` 仍为 `UNKNOWN`。
