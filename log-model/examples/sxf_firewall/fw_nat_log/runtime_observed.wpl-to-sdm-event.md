# sxf_firewall / fw_nat_log 运行时观测候选映射

事件事实：深信服防火墙 NAT 转换（NAT日志，snat）——源 192.0.2.44:52977 转换为 192.0.2.193 访问目标 198.51.100.97:53。

主体：转换前源（source.endpoint=sip）；客体：目标（target.endpoint=dip）；载体：`network_protocol` + nat（facets.network.nat）；观察者：来源产品。

> 状态：candidate，未注册、未批准。WPL 解析事实与深信服防火墙文档已确认；SR-069 人工复核结论见文末。

| WPL 字段 | 值 | SDM 候选路径 | 状态 |
|---|---|---|---|
| `time` | `2026-01-23 11:00:00` | `extensions_obj.source_private.time` | `source_private` |
| `domain` | `localhost` | `extensions_obj.source_private.domain` | `source_private` |
| `type` | `nat` | `extensions_obj.source_private.type` | `source_private` |
| `symbol` | `日志类型:NAT日志` | `extensions_obj.source_private.symbol` | `source_private` |
| `logtype` | `NAT日志` | `extensions_obj.source_private.logtype` | `source_private` |
| `nat_type` | `snat` | `extensions_obj.source_private.nat_type` | `source_private` |
| `sip` | `192.0.2.44` | `roles_obj.source.endpoint.ip` + `source_ip` + `facets_obj.network.nat.original.ip` | `confirmed` |
| `sport` | `52977` | `roles_obj.source.endpoint.port` | `confirmed` |
| `dip` | `198.51.100.97` | `roles_obj.target.endpoint.ip` + `target_ip` | `confirmed` |
| `dport` | `53` | `roles_obj.target.endpoint.port` | `confirmed` |
| `protocol` | `17` | `facets_obj.network.protocol.code` | `confirmed` |
| `nat_after_ip` | `192.0.2.193` | `facets_obj.network.nat.translated.ip` | `confirmed` |
| `nat_after_port` | `52977` | `extensions_obj.source_private.nat_after_port`（NAT 端口无标准路径） | `needs_review` |

## 人工语义复核（SXF Firewall，SR-069）

- 事件事实：深信服防火墙记录 NAT 前后地址/端口转换关联。
- `event_category=network`
- `event_type=network_connection`
- `operation=empty`
- `outcome=unknown`
- 主体/客体/载体：转换前源（source.endpoint）/ 目标（target.endpoint）/ network_protocol + nat（facets.network.nat）
- NAT 转换：`facets.network.nat{original.ip, translated.ip}`；NAT 端口无标准路径保留 source_private
- 文档证据：深信服防火墙 syslog 日志 8.0.50–8.0.95；样本字段已由 WPL 命中。
