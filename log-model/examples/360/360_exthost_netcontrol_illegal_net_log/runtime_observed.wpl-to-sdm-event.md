# 360 / 360_exthost_netcontrol_illegal_net_log 运行时观测候选映射

事件事实：终端网络控制——非法 DNS 联网（illegal_type=dns），终端 zyykylin10（203.0.113.202）访问 www.baidu.com，deal_type=nothing。检测声明保存在 source_finding。

主体：`endpoint_host`（source.host=computername + source.endpoint=local_ip）；客体：`domain`（target.domain=server_ip）；载体：`dns`（illegal_type=dns）；观察者：来源产品。

> 状态：candidate，未注册、未批准。WPL 解析事实与 360 EPP 文档已确认；SR-045 人工复核结论见文末。

| WPL 字段 | 值 | SDM 候选路径 | 状态 |
|---|---|---|---|
| `asset_departmentname` | `test-asset_departmentname` | `extensions_obj.source_private.asset_departmentname` | `source_private` |
| `asset_username` | `hsakdjklas使用人` | `extensions_obj.source_private.asset_username` | `source_private` |
| `center_id` | `test-center_id` | `extensions_obj.source_private.center_id` | `source_private` |
| `clientip` | `203.0.113.37` | `extensions_obj.source_private.clientip` | `source_private` |
| `computername` | `zyykylin10` | `roles_obj.source.host.name` | `confirmed` |
| `ctime` | `2026-01-23 11:00:00` | `occur_time` | `candidate` |
| `deal_type` | `nothing` | `source_finding_obj.status` | `confirmed` |
| `duration` | `0` | `extensions_obj.source_private.duration` | `source_private` |
| `duration_num` | `1` | `extensions_obj.source_private.duration_num` | `source_private` |
| `event_id` | `b563ea44-abd9-43e8-b44e-793bd11f1804` | `extensions_obj.source_private.event_id` | `source_private` |
| `group_name` | `zyy` | `extensions_obj.source_private.group_name` | `source_private` |
| `id` | `116` | `extensions_obj.source_private.id` | `source_private` |
| `illegal_type` | `dns` | `source_finding_obj.rule.label` | `confirmed` |
| `inactivity` | `test-inactivity` | `extensions_obj.source_private.inactivity` | `source_private` |
| `is_xc` | `2` | `extensions_obj.source_private.is_xc` | `source_private` |
| `local_ip` | `203.0.113.202` | `roles_obj.source.endpoint.ip` + `source_ip` | `confirmed` |
| `type` | `360exthost_netcontrol_illegal_net_log` | `extensions_obj.source_private.type` | `source_private` |
| `ltime` | `2026-01-23 11:00:00` | `extensions_obj.source_private.ltime` | `source_private` |
| `m2` | `4e71c16981f112d16241a7b85a92a378de512959010b` | `extensions_obj.source_private.m2` | `source_private` |
| `mac_address` | `00:0c:29:8d:c6:74` | `roles_obj.source.endpoint.mac` | `confirmed` |
| `mtime` | `2026-01-23 11:00:00` | `extensions_obj.source_private.mtime` | `source_private` |
| `plat_id` | `5` | `extensions_obj.source_private.plat_id` | `source_private` |
| `public_ip` | `203.0.113.19` | `extensions_obj.source_private.public_ip` | `source_private` |
| `report_status` | `0` | `extensions_obj.source_private.report_status` | `source_private` |
| `reported_data_ide` | `test-reported_data_ide` | `extensions_obj.source_private.reported_data_ide` | `source_private` |
| `reported_to` | `test-reported_to` | `extensions_obj.source_private.reported_to` | `source_private` |
| `server_ip` | `www.baidu.com` | `roles_obj.target.domain.name` + `target_ip` | `confirmed` |
| `sysiplist` | `203.0.113.69;fe80::4b1f:a89:585b:e1a0%ens33` | `extensions_obj.source_private.sysiplist` | `source_private` |
| `sysmaclist` | `00:0C:29:8D:C6:74` | `extensions_obj.source_private.sysmaclist` | `source_private` |
| `username` | `root` | `extensions_obj.source_private.username` | `source_private` |

## 人工语义复核（360 EPP，SR-045）

- 事件事实：终端网络控制日志记录非法 DNS 联网；deal_type=nothing 不解释为允许或成功。
- **deal_type 枚举已确认**：nothing=不处理、isolate=隔离。本条 nothing。
- `event_category=alert`，`event_type=network_connection`，`operation=empty`，`outcome=unknown`（deal_type=nothing=不处理）。
- 主体/客体/载体：endpoint_host / domain / dns（illegal_type=dns）
- 检测声明：`source_finding_obj`（title/status=deal_type/count/rule.label=illegal_type）
- 文档证据：360《终端-EPP-SysLog文档》；当前 WPL 运行样本已命中。
- 未确认的数字枚举保留原值，未知值策略为 report。
