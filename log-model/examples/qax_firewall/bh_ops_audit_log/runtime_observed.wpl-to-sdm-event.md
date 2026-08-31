# qax_firewall / bh_ops_audit_log 运行时观测候选映射

事件事实：堡垒机系统性能运行状态快照（logType=YAB_SYSTEM_STATUS_LOG）——cpu/mem/read/write 指标。

主体：`none`（状态快照）；客体：`bastion_host`（target.host=prod_name/prod_id）；载体：`none`；观察者：来源产品。

> 状态：candidate，未注册、未批准。WPL 解析事实与 KB47750 已确认；SR-054 人工复核结论见文末。

| WPL 字段 | 值 | SDM 候选路径 | 状态 |
|---|---|---|---|
| `access_time` | `2026-02-03 16:55:13.733618` | `extensions_obj.source_private.access_time` | `source_private` |
| `logType` | `YAB_SYSTEM_STATUS_LOG` | `extensions_obj.source_private.logType` | `source_private` |
| `prod_name` | `堡垒机` | `roles_obj.target.host.name` | `confirmed` |
| `prod_id` | `f73b12355cd64a4ea36d42ed9c4d1e4e` | `roles_obj.target.host.id` | `confirmed` |
| `prod_version` | `203.0.113.245` | `extensions_obj.source_private.prod_version` | `source_private` |
| `prod_ips` | `[FieldStorage { cur_name: None, value: Owned(Field { meta: Chars, name: "prod_ips/[0]", value: Chars("10.xxx.xxx.127") }) }, FieldStorage { cur_name: None, value: Owned(Field { meta: Chars, name: "prod_ips/[1]", value: Chars("192.xxx.xxx.55") }) }]` | `extensions_obj.source_private.prod_ips` | `source_private` |
| `time` | `2026-01-23 11:00:00` | `occur_time` | `candidate` |
| `cpu` | `5.06` | `extensions_obj.source_private.cpu` | `source_private` |
| `mem` | `61.84` | `extensions_obj.source_private.mem` | `source_private` |
| `read` | `56681500` | `extensions_obj.source_private.read` | `source_private` |
| `write` | `940099000` | `extensions_obj.source_private.write` | `source_private` |

## 人工语义复核（KB47750，SR-054）

- 事件事实：堡垒机记录系统性能运行状态快照。
- event_category：`system`
- event_type：`status_update`
- operation：`空；无充分标准动作证据`
- outcome：`unknown`
- 主体/客体/载体：none / bastion_host（target.host=prod_name/prod_id）/ none
- 性能指标（cpu/mem/read/write）无标准路径，保留 `extensions.source_private`
- 证据：奇安信堡垒机 192.0.2.70 Syslog 格式说明 KB47750；对应 `logType` 为 `YAB_SYSTEM_STATUS_LOG`。
- 状态：`reviewed_candidate`
