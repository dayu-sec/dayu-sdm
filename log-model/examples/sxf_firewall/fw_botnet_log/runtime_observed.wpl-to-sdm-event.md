# sxf_firewall / fw_botnet_log 运行时观测候选映射

事件事实：深信服防火墙僵尸网络检测（僵尸网络日志）——源 192.0.2.163 访问 C2 www.audi_log.org，op_action=拒绝。检测声明在 source_finding。

主体：僵尸主机（source.endpoint=sip）；客体：僵尸网络 C2（target.domain=url + target.endpoint=dip）；载体：`http`（facets.http.request）；观察者：来源产品。

> 状态：candidate，未注册、未批准。WPL 解析事实与深信服防火墙文档已确认；SR-065 人工复核结论见文末。

| WPL 字段 | 值 | SDM 候选路径 | 状态 |
|---|---|---|---|
| `time` | `2026-01-23 11:00:00` | `extensions_obj.source_private.time` | `source_private` |
| `domain` | `localhost` | `extensions_obj.source_private.domain` | `source_private` |
| `type` | `fwlog` | `extensions_obj.source_private.type` | `source_private` |
| `symbol` | `日志类型:僵尸网络日志` | `extensions_obj.source_private.symbol` | `source_private` |
| `logtype` | `僵尸网络日志` | `extensions_obj.source_private.logtype` | `source_private` |
| `policy_name` | `-` | `extensions_obj.source_private.policy_name` | `source_private` |
| `sid` | `34014989` | `source_finding_obj.rule.signature_id` | `confirmed` |
| `sip` | `192.0.2.163` | `roles_obj.source.endpoint.ip` + `source_ip` | `confirmed` |
| `sport` | `4720` | `roles_obj.source.endpoint.port` | `confirmed` |
| `dip` | `192.0.2.220` | `roles_obj.target.endpoint.ip` + `target_ip` | `confirmed` |
| `dport` | `80` | `roles_obj.target.endpoint.port` | `confirmed` |
| `origin_alert_cat_name` | `僵尸网络` | `source_finding_obj.title` | `confirmed` |
| `severity` | `低` | `source_finding_obj.severity` | `confirmed` |
| `op_action` | `拒绝` | `source_finding_obj.status`（来源处置，不映射 outcome） | `confirmed` |
| `url` | `www.audi_log.org/test.html` | `roles_obj.target.domain.name` + `facets_obj.http.request.host` | `confirmed` |

## 人工语义复核（SXF Firewall，SR-065）

- 事件事实：深信服防火墙记录僵尸网络检测；检测结论保留 source_finding。
- `event_category=alert`
- `event_type=network_connection`
- `operation=empty`
- `outcome=unknown`；不将 `op_action` 或告警记录机械映射为动作结果。
- 主体/客体/载体：僵尸主机（source.endpoint）/ C2（target.domain+endpoint）/ http（facets.http.request）
- 检测声明：`source_finding_obj`（title/severity/status/count/rule{name, signature_id}）
- 文档证据：深信服防火墙 syslog 日志 8.0.50–8.0.95；样本字段已由 WPL 命中。
