# sxf_firewall / fw_mail_security_log 运行时观测候选映射

事件事实：深信服防火墙邮件安全检测（邮件安全日志）——攻击 192.0.2.2:25 → 203.0.113.15:25（SMTP）命中撞库攻击，op_action=拒绝。检测声明在 source_finding。

主体：攻击源（source.endpoint=sip）；客体：SMTP 服务器（target.endpoint=dip）；载体：`network_protocol`（facets.network.protocol）；观察者：来源产品。

> 状态：candidate，未注册、未批准。WPL 解析事实与深信服防火墙文档已确认；SR-068 人工复核结论见文末。

| WPL 字段 | 值 | SDM 候选路径 | 状态 |
|---|---|---|---|
| `time` | `2026-01-23 11:00:00` | `extensions_obj.source_private.time` | `source_private` |
| `domain` | `localhost` | `extensions_obj.source_private.domain` | `source_private` |
| `type` | `fwlog` | `extensions_obj.source_private.type` | `source_private` |
| `symbol` | `日志类型:邮件安全日志` | `extensions_obj.source_private.symbol` | `source_private` |
| `logtype` | `邮件安全日志` | `extensions_obj.source_private.logtype` | `source_private` |
| `policy_name` | `-` | `extensions_obj.source_private.policy_name` | `source_private` |
| `rule_id` | `6646` | `source_finding_obj.rule.signature_id` | `confirmed` |
| `sip` | `192.0.2.2` | `roles_obj.source.endpoint.ip` + `source_ip` | `confirmed` |
| `sport` | `25` | `roles_obj.source.endpoint.port` | `confirmed` |
| `dip` | `203.0.113.15` | `roles_obj.target.endpoint.ip` + `target_ip` | `confirmed` |
| `dport` | `25` | `roles_obj.target.endpoint.port` | `confirmed` |
| `origin_alert_cat_name` | `撞库攻击` | `source_finding_obj.title` | `confirmed` |
| `severity` | `高` | `source_finding_obj.severity` | `confirmed` |
| `op_action` | `拒绝` | `source_finding_obj.status`（来源处置，不映射 outcome） | `confirmed` |

## 人工语义复核（SXF Firewall，SR-068）

- 事件事实：深信服防火墙记录邮件安全检测；具体邮件动作未由样本确认。
- `event_category=alert`
- `event_type=network_smtp`
- `operation=empty`
- `outcome=unknown`；不将 `op_action` 或告警记录机械映射为动作结果。
- 主体/客体/载体：攻击源（source.endpoint）/ SMTP 服务器（target.endpoint）/ network_protocol
- 检测声明：`source_finding_obj`（title/severity/status/count/rule{name, signature_id}）
- 文档证据：深信服防火墙 syslog 日志 8.0.50–8.0.95；样本字段已由 WPL 命中。
