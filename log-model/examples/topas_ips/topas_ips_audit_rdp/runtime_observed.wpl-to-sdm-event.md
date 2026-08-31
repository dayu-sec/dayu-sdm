# topas_ips / topas_ips_audit_rdp 运行时观测候选映射

事件事实：RDP 协议审计活动记录（recorder=audit_rdp）——liuludan 连接远程主机 198.51.100.199:3389。未提供认证结果。

主体：`rdp_user`（source.user=liuludan + source.endpoint）；客体：`rdp_host`（target.host=198.51.100.199）；载体：`network_protocol`（facets.network.protocol）+ 应用 facets.application.name=rdp；观察者：来源产品。

> 状态：candidate，未注册、未批准。WPL 解析事实与 TopIDP v3 §3.5.14 已确认；SR-040 人工复核结论见文末。

| WPL 字段 | 值 | SDM 候选路径 | 状态 |
|---|---|---|---|
| `vendor` | `topsec` | `extensions_obj.source_private.vendor` | `source_private` |
| `dev_type` | `1` | `extensions_obj.source_private.dev_type` | `source_private` |
| `dev_name` | `TopsecOS` | `extensions_obj.source_private.dev_name` | `source_private` |
| `dev_ip` | `198.51.100.235` | `extensions_obj.source_private.dev_ip` | `source_private` |
| `time` | `2026-01-23 11:00:00` | `occur_time` | `candidate` |
| `index` | `417` | `event_id` | `candidate` |
| `recorder` | `audit_rdp` | `extensions_obj.source_private.recorder` | `source_private` |
| `sid` | `423755975380435122` | `event_id` | `candidate` |
| `proto` | `2` | `facets_obj.network.protocol.code` | `confirmed` |
| `sip` | `192.0.2.122` | `roles_obj.source.endpoint.ip` + `source_ip` | `confirmed` |
| `sport` | `47410` | `roles_obj.source.endpoint.port` | `confirmed` |
| `dip` | `198.51.100.199` | `roles_obj.target.host.ip` + `target_ip` | `confirmed` |
| `dport` | `3389` | `extensions_obj.source_private.dport` | `needs_review` |
| `sipv6` | `` | `extensions_obj.source_private.sipv6` | `source_private` |
| `dipv6` | `` | `extensions_obj.source_private.dipv6` | `source_private` |
| `vid` | `` | `extensions_obj.source_private.vid` | `source_private` |
| `sdev` | `feth1` | `extensions_obj.source_private.sdev` | `source_private` |
| `ddev` | `` | `extensions_obj.source_private.ddev` | `source_private` |
| `smac` | `00:00:5E:00:53:C0` | `extensions_obj.source_private.smac` | `source_private` |
| `dmac` | `00:00:5E:00:53:71` | `extensions_obj.source_private.dmac` | `source_private` |
| `username` | `liuludan` | `roles_obj.source.user.name` | `confirmed` |
| `password` | `REDACTED` | `extensions_obj.source_private.password` | `source_private` |


## 人工语义复核（TopIDP v3，SR-040）

- 事件事实：RDP 协议审计活动记录，非检测告警。
- event_category：`audit`
- event_type：`generic_event`（06 无 RDP 审计专用类型）
- operation：`空`
- outcome：`unknown`（无认证结果字段）
- 主体/客体/载体：rdp_user / rdp_host / network_protocol
- 应用类型：`facets.application.name=rdp`；`dport=3389` 无 host.port 路径，保留原值
- 证据：TopIDP 输出信息格式规范 v3 §3.5.14，`recorder=audit_rdp`；WPL 运行样本已命中。
