# 360 / 360_netconnect_audit 运行时观测候选映射

事件事实：网络连接审计（recorder=netconnect_audit）——进程 360hotfix.exe 从 192.0.2.65:50435 连接 203.0.113.233:8080 并统计流量。审计活动，非检测。

主体：`process`（source.process=processname + source.endpoint + source.user）；客体：`network_endpoint`（target.endpoint=object_ip/port）；载体：`none`（协议/流量入 facets.network）；观察者：来源产品。

> 状态：candidate，未注册、未批准。WPL 解析事实与 360 EPP 文档已确认；SR-048 人工复核结论见文末。

| WPL 字段 | 值 | SDM 候选路径 | 状态 |
|---|---|---|---|
| `asset_username` | `hsakdjklas#@$%阿利克水泥钉金卡三年` | `extensions_obj.source_private.asset_username` | `source_private` |
| `client_group_id` | `21` | `extensions_obj.source_private.client_group_id` | `source_private` |
| `client_group_name` | `qsl` | `extensions_obj.source_private.client_group_name` | `source_private` |
| `clientip` | `203.0.113.37` | `extensions_obj.source_private.clientip` | `source_private` |
| `cmp_loginuser` | `test-user` | `roles_obj.source.user.name` | `confirmed` |
| `computername` | `TEST-PC-01` | `extensions_obj.source_private.computername` | `source_private` |
| `count_byte` | `771` | `facets_obj.network.traffic.total_bytes` | `confirmed` |
| `ctime` | `2026-01-23 11:00:00` | `occur_time` | `candidate` |
| `id` | `3be31e6e-6159-4916-b4d2-fece4d8bf1ec` | `extensions_obj.source_private.id` | `source_private` |
| `incept_byte` | `211` | `facets_obj.network.traffic.bytes_in` | `confirmed` |
| `is_xc` | `2` | `extensions_obj.source_private.is_xc` | `source_private` |
| `type` | `netconnect_audit` | `extensions_obj.source_private.type` | `source_private` |
| `m2` | `a17f1890bb3e71a61d8be6fe71d71b73fa02c41e2914` | `extensions_obj.source_private.m2` | `source_private` |
| `mac` | `00:00:5E:00:53:F4` | `extensions_obj.source_private.mac` | `source_private` |
| `object_ip` | `203.0.113.233` | `roles_obj.target.endpoint.ip` + `target_ip` | `confirmed` |
| `object_port` | `8080` | `roles_obj.target.endpoint.port` | `confirmed` |
| `plant_id` | `1` | `extensions_obj.source_private.plant_id` | `source_private` |
| `plat_id` | `1` | `extensions_obj.source_private.plat_id` | `source_private` |
| `processname` | `360hotfix.exe` | `roles_obj.source.process.name` | `confirmed` |
| `processname_path` | `C:\\program files (x86)\\360\\360safe` | `roles_obj.source.process.path` | `confirmed` |
| `protocol` | `6` | `facets_obj.network.protocol.code` | `confirmed` |
| `send_byte` | `560` | `facets_obj.network.traffic.bytes_out` | `confirmed` |
| `send_time` | `2026-01-23 03:00:00` | `extensions_obj.source_private.send_time` | `source_private` |
| `send_time_end` | `2026-01-23 03:00:00` | `extensions_obj.source_private.send_time_end` | `source_private` |
| `source_ip` | `192.0.2.65` | `roles_obj.source.endpoint.ip` + `source_ip` | `confirmed` |
| `source_port` | `50435` | `roles_obj.source.endpoint.port` | `confirmed` |
| `sysmaclist` | `00:00:5E:00:53:F4` | `extensions_obj.source_private.sysmaclist` | `source_private` |
| `username` | `test-user` | `extensions_obj.source_private.username` | `source_private` |

## 人工语义复核（360 EPP，SR-048）

- 事件事实：网络连接审计记录进程从源地址端口连接目标地址端口并统计流量。
- `event_category=network`，`event_type=network_connection`，`operation=empty`，`outcome=unknown`（网络审计活动，非检测）。
- 主体/客体/载体：process / network_endpoint / none（协议/流量入 facets.network）
- 审计事实：roles.source.process+endpoint+user / target.endpoint / facets.network.protocol+traffic
- `source_finding_obj=null`：审计活动非检测。
- 文档证据：360《终端-EPP-SysLog文档》；当前 WPL 运行样本已命中。
- 未确认的数字枚举保留原值，未知值策略为 report。
