# topas_ips / topas_ips_audit_ldap 运行时观测候选映射

事件事实：LDAP 协议审计活动记录（recorder=audit_ldap）——user1 连接 LDAP 服务（192.0.2.54:389，协议版本 3）。未提供认证结果。

主体：`ldap_user`（source.user=user1 + source.endpoint）；客体：`ldap_service`（target.service=192.0.2.54:389）；载体：`network_protocol`（facets.network.protocol）+ 应用 facets.application.name=ldap；观察者：来源产品。

> 状态：candidate，未注册、未批准。WPL 解析事实与 TopIDP v3 §3.5.13 已确认；SR-039 人工复核结论见文末。

| WPL 字段 | 值 | SDM 候选路径 | 状态 |
|---|---|---|---|
| `vendor` | `topsec` | `extensions_obj.source_private.vendor` | `source_private` |
| `dev_type` | `1` | `extensions_obj.source_private.dev_type` | `source_private` |
| `dev_name` | `TopsecOS` | `extensions_obj.source_private.dev_name` | `source_private` |
| `dev_ip` | `198.51.100.235` | `extensions_obj.source_private.dev_ip` | `source_private` |
| `time` | `2026-01-23 11:00:00` | `occur_time` | `candidate` |
| `index` | `416` | `event_id` | `candidate` |
| `recorder` | `audit_ldap` | `extensions_obj.source_private.recorder` | `source_private` |
| `sid` | `423755985044111606` | `event_id` | `candidate` |
| `proto` | `2` | `facets_obj.network.protocol.code` | `confirmed` |
| `sip` | `203.0.113.205` | `roles_obj.source.endpoint.ip` + `source_ip` | `confirmed` |
| `sport` | `36587` | `roles_obj.source.endpoint.port` | `confirmed` |
| `dip` | `192.0.2.54` | `roles_obj.target.service.name` + `target_ip` | `confirmed` |
| `dport` | `389` | `roles_obj.target.service.port` | `confirmed` |
| `sipv6` | `` | `extensions_obj.source_private.sipv6` | `source_private` |
| `dipv6` | `` | `extensions_obj.source_private.dipv6` | `source_private` |
| `vid` | `` | `extensions_obj.source_private.vid` | `source_private` |
| `sdev` | `feth1` | `extensions_obj.source_private.sdev` | `source_private` |
| `ddev` | `` | `extensions_obj.source_private.ddev` | `source_private` |
| `smac` | `00:00:5E:00:53:D0` | `extensions_obj.source_private.smac` | `source_private` |
| `dmac` | `00:00:5E:00:53:EF` | `extensions_obj.source_private.dmac` | `source_private` |
| `username` | `user1` | `roles_obj.source.user.name` | `confirmed` |
| `password` | `REDACTED` | `extensions_obj.source_private.password` | `source_private` |
| `version` | `3` | `extensions_obj.source_private.version` | `source_private` |


## 人工语义复核（TopIDP v3，SR-039）

- 事件事实：LDAP 协议审计活动记录，非检测告警。
- event_category：`audit`
- event_type：`generic_event`（06 无 LDAP 审计专用类型）
- operation：`空`
- outcome：`unknown`（无认证结果字段）
- 主体/客体/载体：ldap_user / ldap_service / network_protocol
- 应用类型：`facets.application.name=ldap`
- 证据：TopIDP 输出信息格式规范 v3 §3.5.13，`recorder=audit_ldap`；WPL 运行样本已命中。
