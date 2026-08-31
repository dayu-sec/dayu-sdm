# sxf_firewall / ad_ddos_attack_log 运行时观测候选映射

事件事实：深信服防火墙 DDoS 检测（DOS攻击日志）——源 203.0.113.164 对目的 192.0.2.220 发起 IP 宽松源路由攻击，op_action=拒绝。检测声明在 source_finding。

主体：攻击源（source.endpoint=sip）；客体：受害目标（target.endpoint=dip）；载体：`none`；观察者：来源产品。

> 状态：candidate，未注册、未批准。WPL 解析事实与深信服防火墙文档已确认；SR-063 人工复核结论见文末。

| WPL 字段 | 值 | SDM 候选路径 | 状态 |
|---|---|---|---|
| `time` | `2026-01-23 11:00:00` | `extensions_obj.source_private.time` | `source_private` |
| `domain` | `localhost` | `extensions_obj.source_private.domain` | `source_private` |
| `type` | `fwlog` | `extensions_obj.source_private.type` | `source_private` |
| `symbol` | `日志类型:DOS攻击日志` | `extensions_obj.source_private.symbol` | `source_private` |
| `logtype` | `DOS攻击日志` | `extensions_obj.source_private.logtype` | `source_private` |
| `policy_name` | `dos2` | `source_finding_obj.rule.label` | `confirmed` |
| `sip` | `203.0.113.164` | `roles_obj.source.endpoint.ip` + `source_ip` | `confirmed` |
| `dip` | `192.0.2.220` | `roles_obj.target.endpoint.ip` + `target_ip` | `confirmed` |
| `comm_direction` | `外网` | `extensions_obj.source_private.comm_direction` | `source_private` |
| `origin_alert_cat_name` | `IP宽松源路由选项报文` | `source_finding_obj.title` | `confirmed` |
| `severity` | `低` | `source_finding_obj.severity` | `confirmed` |
| `op_action` | `拒绝` | `source_finding_obj.status`（来源处置，不映射 outcome） | `confirmed` |

## 人工语义复核（SXF Firewall，SR-063）

- 事件事实：深信服防火墙记录 DDoS 检测告警；攻击结论保留 source_finding。
- `event_category=alert`
- `event_type=network_connection`
- `operation=empty`
- `outcome=unknown`；不将 `op_action` 或告警记录机械映射为动作结果。
- 主体/客体/载体：攻击源（source.endpoint）/ 受害目标（target.endpoint）/ none
- 检测声明：`source_finding_obj`（title/severity/status/count/rule{name, label=policy_name}）
- 文档证据：深信服防火墙 syslog 日志 8.0.50–8.0.95；样本字段已由 WPL 命中。
