# sxf_firewall / fw_local_access_log 运行时观测候选映射

事件事实：深信服防火墙本地访问连接（本机安全）——源 198.51.100.66:1025 访问本地端口 762（SSL_HELLO），op_action=拒绝。

主体：访问源（source.endpoint=sip）；客体：本地目标（target.endpoint=dport，无目标 IP）；载体：`application`（facets.application）；观察者：来源产品。

> 状态：candidate，未注册、未批准。WPL 解析事实与深信服防火墙文档已确认；SR-067 人工复核结论见文末。

| WPL 字段 | 值 | SDM 候选路径 | 状态 |
|---|---|---|---|
| `time` | `2026-01-23 11:00:00` | `extensions_obj.source_private.time` | `source_private` |
| `domain` | `localhost` | `extensions_obj.source_private.domain` | `source_private` |
| `type` | `fwlog` | `extensions_obj.source_private.type` | `source_private` |
| `symbol` | `日志类型:本机安全` | `extensions_obj.source_private.symbol` | `source_private` |
| `logtype` | `本机安全` | `extensions_obj.source_private.logtype` | `source_private` |
| `policy_name` | `-` | `extensions_obj.source_private.policy_name` | `source_private` |
| `sip` | `198.51.100.66` | `roles_obj.source.endpoint.ip` + `source_ip` | `confirmed` |
| `sport` | `1025` | `roles_obj.source.endpoint.port` | `confirmed` |
| `dport` | `762` | `roles_obj.target.endpoint.port` | `confirmed` |
| `app_cat` | `SSL` | `facets_obj.application.name` | `confirmed` |
| `app_name` | `SSL_HELLO` | `extensions_obj.source_private.app_name` | `source_private` |
| `op_action` | `拒绝` | `extensions_obj.source_private.op_action`（来源处置，不映射 outcome） | `needs_review` |

## 人工语义复核（SXF Firewall，SR-067）

- 事件事实：深信服防火墙记录源端到目标端的本地访问连接。
- `event_category=network`
- `event_type=network_connection`
- `operation=empty`
- `outcome=unknown`；不将 `op_action` 或告警记录机械映射为动作结果。
- 主体/客体/载体：访问源（source.endpoint）/ 本地目标（target.endpoint）/ application（facets.application.name=SSL）
- `source_finding_obj=null`：访问连接审计非检测
- 文档证据：深信服防火墙 syslog 日志 8.0.50–8.0.95；样本字段已由 WPL 命中。
