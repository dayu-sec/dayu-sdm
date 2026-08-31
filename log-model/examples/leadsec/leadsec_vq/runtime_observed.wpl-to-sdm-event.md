# leadsec / leadsec_vq 运行时观测候选映射

事件事实：病毒隔离（recorder=vq）——SMTP 流量隔离邮件文件 email_2012_2_26_3_23_14_483926.eml。检测声明在 source_finding。

主体：`source_endpoint`（srcaddr/srcport）；客体：`quarantined_file`（target.file=eventname 文件 + facets.email）；载体：`smtp`（facets.network.protocol=SMTP）；观察者：来源产品。

> 状态：candidate，未注册、未批准。WPL 解析事实与 Power-V 文档已确认；SR-051 人工复核结论见文末。

| WPL 字段 | 值 | SDM 候选路径 | 状态 |
|---|---|---|---|
| `info` | `asdeamon` | `extensions_obj.source_private.info` | `source_private` |
| `devid` | `0` | `extensions_obj.source_private.devid` | `source_private` |
| `date` | `2026-01-23 11:00:00` | `occur_time` | `candidate` |
| `dname` | `Themis` | `extensions_obj.source_private.dname` | `source_private` |
| `logtype` | `14` | `extensions_obj.source_private.logtype` | `source_private` |
| `pri` | `4` | `extensions_obj.source_private.pri` | `source_private` |
| `ver` | `0.3.0` | `extensions_obj.source_private.ver` | `source_private` |
| `eventtype` | `病毒隔离` | `extensions_obj.source_private.eventtype` | `source_private` |
| `eventname` | `隔离文件 : email_2012_2_26_3_23_14_483926.eml` | `source_finding_obj.title` | `confirmed` |
| `mod` | `vq` | `extensions_obj.source_private.mod` | `source_private` |
| `protocol` | `SMTP` | `facets_obj.network.protocol.code` + `facets_obj.email.attachments[].name` | `confirmed` |
| `srcaddr` | `198.51.100.188` | `roles_obj.source.endpoint.ip` + `source_ip` | `confirmed` |
| `srcport` | `4026` | `roles_obj.source.endpoint.port` | `confirmed` |
| `destaddr` | `203.0.113.5` | `extensions_obj.source_private.destaddr` + `target_ip` | `needs_review` |
| `destport` | `25` | `extensions_obj.source_private.destport` | `needs_review` |
| `fwlog` | `0` | `extensions_obj.source_private.fwlog` | `source_private` |

## 人工语义复核（Leadsec Power-V，SR-051）

- 事件事实：病毒文件隔离日志明确记录隔离邮件文件；样本没有独立结果字段。
- `event_category=alert`
- **`event_type=generic_event`**（06 无病毒隔离类型；隔离是来源处置，非文件修改动作，与 SR-046 一致）
- `operation=empty`，`outcome=unknown`（无独立结果字段）。
- 主体/客体/载体：source_endpoint / quarantined_file / smtp
- 检测声明：`source_finding_obj`（title=eventname/count/action=quarantine）
- `pri` 仅映射 `log_level`。
- 文档证据：Power-V 192.0.2.120 日志格式手册 VERSION 0.3.0；证据状态 `vendor_confirmed_and_observed`。
