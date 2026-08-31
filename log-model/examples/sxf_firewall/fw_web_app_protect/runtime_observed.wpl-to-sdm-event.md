# sxf_firewall / fw_web_app_protect 运行时观测候选映射

事件事实：深信服防火墙 Web 应用防护（WEB应用防护日志）——攻击 192.0.2.11:7224 → 192.0.2.15:80 命中跨站请求伪造，op_action=允许。检测声明在 source_finding。

主体：攻击源（source.endpoint=sip）；客体：Web 服务器（target.endpoint=dip + target.domain=url）；载体：`http`（facets.http.request）；观察者：来源产品。

> 状态：candidate，未注册、未批准。WPL 解析事实与深信服防火墙文档已确认；SR-073 人工复核结论见文末。

| WPL 字段 | 值 | SDM 候选路径 | 状态 |
|---|---|---|---|
| `time` | `2026-01-23 11:00:00` | `extensions_obj.source_private.time` | `source_private` |
| `domain` | `localhost` | `extensions_obj.source_private.domain` | `source_private` |
| `type` | `fwlog` | `extensions_obj.source_private.type` | `source_private` |
| `symbol` | `日志类型:WEB应用防护` | `extensions_obj.source_private.symbol` | `source_private` |
| `logtype` | `WEB应用防护` | `extensions_obj.source_private.logtype` | `source_private` |
| `policy_name` | `waf1` | `source_finding_obj.rule.label` | `confirmed` |
| `rule_id` | `0` | `source_finding_obj.rule.signature_id` | `confirmed` |
| `sip` | `192.0.2.11` | `roles_obj.source.endpoint.ip` + `source_ip` | `confirmed` |
| `sport` | `7224` | `roles_obj.source.endpoint.port` | `confirmed` |
| `dip` | `192.0.2.15` | `roles_obj.target.endpoint.ip` + `target_ip` | `confirmed` |
| `dport` | `80` | `roles_obj.target.endpoint.port` | `confirmed` |
| `origin_alert_cat_name` | `跨站请求伪造` | `source_finding_obj.title` | `confirmed` |
| `severity` | `低` | `source_finding_obj.severity` | `confirmed` |
| `op_action` | `允许` | `source_finding_obj.status`（来源处置，不映射 outcome） | `confirmed` |
| `url` | `http://www.sangfor.com/waf.jsp` | `roles_obj.target.domain.name` + `facets_obj.http.request.host` | `confirmed` |

## 人工语义复核（SXF Firewall，SR-073）

- 事件事实：深信服防火墙记录 Web 应用防护命中；告警严重度保留 source_finding。
- `event_category=alert`
- `event_type=network_http`
- `operation=empty`
- `outcome=unknown`；不将 `op_action`（允许）或告警记录机械映射为动作结果。
- 主体/客体/载体：攻击源（source.endpoint）/ Web 服务器（target.endpoint+domain）/ http（facets.http.request）
- 检测声明：`source_finding_obj`（title/severity/status/count/rule{name, label, signature_id}）
- 文档证据：深信服防火墙 syslog 日志 8.0.50–8.0.95；样本字段已由 WPL 命中。
