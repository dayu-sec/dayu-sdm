# sxf_firewall / fw_ips_protect_log 运行时观测候选映射

事件事实：深信服防火墙 IPS 防护（IPS防护日志）——攻击 203.0.113.113:80 → 203.0.113.118:80（tcp）命中 WebCalendar 漏洞，op_action=拒绝。检测声明在 source_finding。

主体：攻击源（source.endpoint=sip）；客体：受害目标（target.endpoint=dip）；载体：`network_protocol`（facets.network.protocol）；观察者：来源产品。

> 状态：candidate，未注册、未批准。WPL 解析事实与深信服防火墙文档已确认；SR-066 人工复核结论见文末。

| WPL 字段 | 值 | SDM 候选路径 | 状态 |
|---|---|---|---|
| `time` | `2026-01-23 11:00:00` | `extensions_obj.source_private.time` | `source_private` |
| `domain` | `localhost` | `extensions_obj.source_private.domain` | `source_private` |
| `type` | `fwlog` | `extensions_obj.source_private.type` | `source_private` |
| `symbol` | `日志类型:IPS防护日志` | `extensions_obj.source_private.symbol` | `source_private` |
| `logtype` | `IPS防护日志` | `extensions_obj.source_private.logtype` | `source_private` |
| `policy_name` | `ips2` | `source_finding_obj.rule.label` | `confirmed` |
| `vuln_id` | `1265` | `source_finding_obj.rule.signature_id` | `confirmed` |
| `vuln_name` | `WebCalendar本地文件包含和PHP代码注入漏洞` | `source_finding_obj.rule.name` | `confirmed` |
| `sip` | `203.0.113.113` | `roles_obj.source.endpoint.ip` + `source_ip` | `confirmed` |
| `sport` | `80` | `roles_obj.source.endpoint.port` | `confirmed` |
| `dip` | `203.0.113.118` | `roles_obj.target.endpoint.ip` + `target_ip` | `confirmed` |
| `dport` | `80` | `roles_obj.target.endpoint.port` | `confirmed` |
| `protocol` | `tcp` | `facets_obj.network.protocol.code` | `confirmed` |
| `origin_alert_cat_name` | `web漏洞攻击` | `source_finding_obj.title` | `confirmed` |
| `severity` | `高` | `source_finding_obj.severity` | `confirmed` |
| `op_action` | `拒绝` | `source_finding_obj.status`（来源处置，不映射 outcome） | `confirmed` |

## 人工语义复核（SXF Firewall，SR-066）

- 事件事实：深信服防火墙记录 IPS 防护命中；protocol 与源/目标地址支持网络连接事实。
- `event_category=alert`
- `event_type=network_connection`
- `operation=empty`
- `outcome=unknown`；不将 `op_action` 或告警记录机械映射为动作结果。
- 主体/客体/载体：攻击源（source.endpoint）/ 受害目标（target.endpoint）/ network_protocol
- 检测声明：`source_finding_obj`（title/severity/status/count/rule{name, label, signature_id}）
- 文档证据：深信服防火墙 syslog 日志 8.0.50–8.0.95；样本字段已由 WPL 命中。
