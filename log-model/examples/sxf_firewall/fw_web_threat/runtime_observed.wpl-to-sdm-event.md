# sxf_firewall / fw_web_threat 运行时观测候选映射

事件事实：深信服防火墙 Web 威胁检测（WEB威胁日志）——用户 b 访问 URL http://203.0.113.107/repro/ss（p2p），op_action=拒绝。检测声明在 source_finding。

主体：访问用户（source.user=user_name + source.endpoint=sip）；客体：Web 目标（target.endpoint=dip + target.domain=url）；载体：`http` + `application`（facets）；观察者：来源产品。

> 状态：candidate，未注册、未批准。WPL 解析事实与深信服防火墙文档已确认；SR-074 人工复核结论见文末。

| WPL 字段 | 值 | SDM 候选路径 | 状态 |
|---|---|---|---|
| `time` | `2026-01-23 11:00:00` | `extensions_obj.source_private.time` | `source_private` |
| `domain` | `localhost` | `extensions_obj.source_private.domain` | `source_private` |
| `type` | `fwlog` | `extensions_obj.source_private.type` | `source_private` |
| `symbol` | `日志类型:WEB威胁` | `extensions_obj.source_private.symbol` | `source_private` |
| `logtype` | `WEB威胁` | `extensions_obj.source_private.logtype` | `source_private` |
| `policy_name` | `web_threat` | `source_finding_obj.rule.label` | `confirmed` |
| `user_name` | `b` | `roles_obj.source.user.name` | `confirmed` |
| `sip` | `203.0.113.107` | `roles_obj.source.endpoint.ip` + `source_ip` | `confirmed` |
| `dip` | `198.51.100.123` | `roles_obj.target.endpoint.ip` + `target_ip` | `confirmed` |
| `app_name` | `p2p` | `facets_obj.application.name` | `confirmed` |
| `op_action` | `拒绝` | `source_finding_obj.status`（来源处置，不映射 outcome） | `confirmed` |
| `url` | `http://203.0.113.107/repro/ss` | `roles_obj.target.domain.name` + `facets_obj.http.request.host` | `confirmed` |

## 人工语义复核（SXF Firewall，SR-074）

- 事件事实：深信服防火墙记录 Web 威胁检测；用户和 URL 作为来源证据。
- `event_category=alert`
- `event_type=network_http`
- `operation=empty`
- `outcome=unknown`；不将 `op_action`（拒绝）或告警记录机械映射为动作结果。
- 主体/客体/载体：访问用户（source.user+endpoint）/ Web 目标（target.endpoint+domain）/ http + application
- 检测声明：`source_finding_obj`（title/status/count/rule{name, label}）
- 文档证据：深信服防火墙 syslog 日志 8.0.50–8.0.95；样本字段已由 WPL 命中。
