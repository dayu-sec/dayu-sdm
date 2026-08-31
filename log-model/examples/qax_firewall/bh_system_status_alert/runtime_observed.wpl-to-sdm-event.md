# qax_firewall / bh_system_status_alert 运行时观测候选映射

事件事实：堡垒机系统性能阈值告警（logType=YAB_SYSTEM_ALARM_LOG）——CPU 超 50%，alarmLevel=低。

主体：`none`（系统阈值告警）；客体：`bastion_host`（target.host=prod_name/prod_id）；载体：`none`；观察者：来源产品。

> 状态：candidate，未注册、未批准。WPL 解析事实与 KB47750 已确认；SR-057 人工复核结论见文末。

| WPL 字段 | 值 | SDM 候选路径 | 状态 |
|---|---|---|---|
| `access_time` | `2026-02-03 16:55:13.733618` | `extensions_obj.source_private.access_time` | `source_private` |
| `logType` | `YAB_SYSTEM_ALARM_LOG` | `extensions_obj.source_private.logType` | `source_private` |
| `prod_name` | `堡垒机` | `roles_obj.target.host.name` | `confirmed` |
| `prod_id` | `f73b12355cd64a4ea36d42ed9c4d1e4e` | `roles_obj.target.host.id` | `confirmed` |
| `prod_version` | `203.0.113.245` | `extensions_obj.source_private.prod_version` | `source_private` |
| `prod_ips` | `[FieldStorage { cur_name: None, value: Owned(Field { meta: Chars, name: "prod_ips/[0]", value: Chars("10.xxx.xxx.127") }) }, FieldStorage { cur_name: None, value: Owned(Field { meta: Chars, name: "prod_ips/[1]", value: Chars("192.xxx.xxx.55") }) }]` | `extensions_obj.source_private.prod_ips` | `source_private` |
| `time` | `2026-01-23 11:00:00` | `occur_time` | `candidate` |
| `user` | `admin` | `extensions_obj.source_private.user` | `source_private` |
| `alarmModule` | `系统性能` | `extensions_obj.source_private.alarmModule` | `source_private` |
| `systemHardType` | `CPU` | `extensions_obj.source_private.systemHardType` | `source_private` |
| `threshold` | `50` | `extensions_obj.source_private.threshold` | `source_private` |
| `msgType` | `系统消息` | `extensions_obj.source_private.msgType` | `source_private` |
| `alarmLevel` | `低` | `extensions_obj.source_private.alarmLevel` | `source_private` |
| `alarmMsg` | `CPU使用率超过50%` | `extensions_obj.source_private.alarmMsg` | `source_private` |

## 人工语义复核（KB47750，SR-057）

- 事件事实：堡垒机生成系统性能阈值告警；alarmLevel 仅保留来源私有，不直接映射 SDM severity。
- event_category：`system`
- event_type：`status_update`
- operation：`空；无充分标准动作证据`
- outcome：`unknown`
- 主体/客体/载体：none / bastion_host（target.host=prod_name/prod_id）/ none
- 告警内容（alarmMsg/alarmModule/systemHardType/threshold/alarmLevel）无标准路径，保留 `extensions.source_private`
- 证据：奇安信堡垒机 192.0.2.70 Syslog 格式说明 KB47750；对应 `logType` 为 `YAB_SYSTEM_ALARM_LOG`。
- 状态：`reviewed_candidate`
