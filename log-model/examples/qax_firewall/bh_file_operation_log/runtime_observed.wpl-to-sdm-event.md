# qax_firewall / bh_file_operation_log 运行时观测候选映射

事件事实：堡垒机命令操作（logType=YAB_CMD_OPS_LOG）——用户 admin 对目标资源「主机1」(192.xxx.xxx.40) 执行命令 ls，action=disconnect。

主体：`source_user`（source.user=user + source.endpoint=sourceIP）；客体：`target_resource`（target.host=resource/targetIP）；载体：`none`；观察者：来源产品。

> 状态：candidate，未注册、未批准。WPL 解析事实与 KB47750 已确认；SR-053 人工复核结论见文末。

| WPL 字段 | 值 | SDM 候选路径 | 状态 |
|---|---|---|---|
| `access_time` | `2026-02-03 16:55:13.733618` | `extensions_obj.source_private.access_time` | `source_private` |
| `logType` | `YAB_CMD_OPS_LOG` | `extensions_obj.source_private.logType` | `source_private` |
| `time` | `2026-01-23 11:00:00` | `occur_time` | `candidate` |
| `user` | `admin` | `roles_obj.source.user.name` | `confirmed` |
| `sourceIP` | `192.xxx.xxx.20` | `roles_obj.source.endpoint.ip` + `source_ip` | `confirmed` |
| `resource` | `主机1` | `roles_obj.target.host.name` | `confirmed` |
| `targetIP` | `192.xxx.xxx.40` | `roles_obj.target.host.ip` + `target_ip` | `confirmed` |
| `command` | `ls` | `extensions_obj.source_private.command` | `source_private` |
| `action` | `disconnect` | `extensions_obj.source_private.action`（会话断开，非结果） | `needs_review` |
| `prod_name` | `堡垒机,prod_id=f73b12355cd64a4ea36d42ed9c4d1e4e` | `extensions_obj.source_private.prod_name` | `source_private` |
| `prod_version` | `203.0.113.245` | `extensions_obj.source_private.prod_version` | `source_private` |
| `prod_ips` | `[FieldStorage { cur_name: None, value: Owned(Field { meta: Chars, name: "prod_ips/[0]", value: Chars("10.xxx.xxx.127") }) }, FieldStorage { cur_name: None, value: Owned(Field { meta: Chars, name: "prod_ips/[1]", value: Chars("192.xxx.xxx.55") }) }]` | `extensions_obj.source_private.prod_ips` | `source_private` |

## 人工语义复核（KB47750，SR-053）

- 事件事实：堡垒机用户对目标资源执行命令操作（logType=YAB_CMD_OPS_LOG）。
- event_category：`audit`
- **event_type：`generic_event`**（命令执行无标准类型；user_resource_update_content 暗示内容更新不贴切）
- operation：`空；无充分标准动作证据`
- outcome：`unknown`
- 主体/客体/载体：source_user / target_resource（target.host）/ none
- `command=ls`、`action=disconnect`（断开连接）
- **目录名 bh_file_operation_log 与 logType=YAB_CMD_OPS_LOG 不符**（与 SR-006 同类）
- 证据：奇安信堡垒机 192.0.2.70 Syslog 格式说明 KB47750；对应 `logType` 为 `YAB_CMD_OPS_LOG`。
- 状态：`reviewed_candidate`
