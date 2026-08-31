# topas_ips / topas_ips_audit_db 运行时观测候选映射

事件事实：数据库审计活动记录（recorder=audit_db）——db2admin 对 DB2 库 SAMPLE 执行 SQL 查询。SQL 事实无标准数据库路径，待扩展；不是检测告警。

主体：`database_user`（source.user=db2admin + source.endpoint）；客体：`database_service`（target.service=SAMPLE:50000）；载体：`network_protocol`（facets.network.protocol）+ 数据库类型 facets.application.name=db2；观察者：来源产品。

> 状态：candidate，未注册、未批准。WPL 解析事实与 TopIDP v3 §3.5.15 已确认；SR-038 人工复核结论见文末。

| WPL 字段 | 值 | SDM 候选路径 | 状态 |
|---|---|---|---|
| `vendor` | `topsec` | `extensions_obj.source_private.vendor` | `source_private` |
| `dev_type` | `1` | `extensions_obj.source_private.dev_type` | `source_private` |
| `dev_name` | `TopsecOS` | `extensions_obj.source_private.dev_name` | `source_private` |
| `dev_ip` | `192.0.2.50` | `extensions_obj.source_private.dev_ip` | `source_private` |
| `time` | `2026-01-23 11:00:00` | `occur_time` | `candidate` |
| `index` | `418` | `event_id` | `candidate` |
| `recorder` | `audit_db` | `extensions_obj.source_private.recorder` | `source_private` |
| `sid` | `429073175226089477` | `event_id` | `candidate` |
| `proto` | `2` | `facets_obj.network.protocol.code` | `confirmed` |
| `sip` | `192.0.2.104` | `roles_obj.source.endpoint.ip` + `source_ip` | `confirmed` |
| `sport` | `49686` | `roles_obj.source.endpoint.port` | `confirmed` |
| `dip` | `198.51.100.16` | `roles_obj.target.service` + `target_ip` | `confirmed` |
| `dport` | `50000` | `roles_obj.target.service.port` | `confirmed` |
| `sipv6` | `` | `extensions_obj.source_private.sipv6` | `source_private` |
| `dipv6` | `` | `extensions_obj.source_private.dipv6` | `source_private` |
| `vid` | `` | `extensions_obj.source_private.vid` | `source_private` |
| `sdev` | `feth1` | `extensions_obj.source_private.sdev` | `source_private` |
| `ddev` | `` | `extensions_obj.source_private.ddev` | `source_private` |
| `smac` | `00:00:5E:00:53:74` | `extensions_obj.source_private.smac` | `source_private` |
| `dmac` | `00:00:5E:00:53:24` | `extensions_obj.source_private.dmac` | `source_private` |
| `dbtype` | `db2` | `facets_obj.application.name` | `confirmed` |
| `version` | `SQL11011` | `extensions_obj.source_private.version` | `source_private` |
| `username` | `db2admin` | `roles_obj.source.user.name` | `confirmed` |
| `password` | `REDACTED` | `extensions_obj.source_private.password` | `source_private` |
| `dbname` | `SAMPLE` | `roles_obj.target.service.name` | `confirmed` |
| `command` | `select current schema from sysibm.sysdummy1` | `extensions_obj.unmapped.command` | `needs_review` |
| `retcode` | `NP01F` | `extensions_obj.unmapped.retcode` | `needs_review` |
| `retmsg` | `` | `extensions_obj.unmapped.retmsg` | `needs_review` |


## 人工语义复核（TopIDP v3，SR-038）

- 事件事实：数据库审计活动记录，非检测告警。
- event_category：`audit`
- event_type：`generic_event`（06 无数据库查询专用类型）
- operation：`空`
- outcome：`unknown`（retcode=NP01F 未确认）
- 主体/客体/载体：database_user / database_service / network_protocol
- **模型缺口**：registry 无 `facets.database`/`roles.target.database` 路径；SQL 事实（command/dbname/retcode/retmsg）在 `extensions.unmapped` 待扩展。
- 证据：TopIDP 输出信息格式规范 v3 §3.5.15，`recorder=audit_db`；WPL 运行样本已命中。
