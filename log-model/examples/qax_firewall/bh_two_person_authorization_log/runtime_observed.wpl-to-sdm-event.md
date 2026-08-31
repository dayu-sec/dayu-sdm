# qax_firewall / bh_two_person_authorization_log 运行时观测候选映射

事件事实：堡垒机双人授权（logType=YAB_DBL_AUTH_LOG）——用户 abc 申请访问「主机 1」，审批人 admin 参与审批。

主体：`source_user`（source.user=user + source.endpoint=sourceIP）；客体：`target_device_or_resource`（target.host=resource/targetIP）；审批人：`related[].user`（approver）；载体：`none`；观察者：来源产品。

> 状态：candidate，未注册、未批准。WPL 解析事实与 KB47750 已确认；SR-058 人工复核结论见文末。

| WPL 字段 | 值 | SDM 候选路径 | 状态 |
|---|---|---|---|
| `access_time` | `2026-02-03 16:55:13.733618` | `extensions_obj.source_private.access_time` | `source_private` |
| `logType` | `YAB_DBL_AUTH_LOG` | `extensions_obj.source_private.logType` | `source_private` |
| `time` | `2026-01-23 11:00:00` | `occur_time` | `candidate` |
| `user` | `abc` | `roles_obj.source.user.name` | `confirmed` |
| `sourceIP` | `192.xxx.xxx.20` | `roles_obj.source.endpoint.ip` + `source_ip` | `confirmed` |
| `resource` | `主机 1` | `roles_obj.target.host.name` | `confirmed` |
| `targetIP` | `192.xxx.xxx.40` | `roles_obj.target.host.ip` + `target_ip` | `confirmed` |
| `approver` | `admin` | `roles_obj.related[0].user.name` | `confirmed` |
| `prod_name` | `堡垒机` | `extensions_obj.source_private.prod_name` | `source_private` |
| `prod_id` | `f73b12355cd64a4ea36d42ed9c4d1e4e` | `extensions_obj.source_private.prod_id` | `source_private` |
| `prod_version` | `203.0.113.245` | `extensions_obj.source_private.prod_version` | `source_private` |
| `prod_ips` | `[FieldStorage { cur_name: None, value: Owned(Field { meta: Chars, name: "prod_ips/[0]", value: Chars("10.xxx.xxx.127") }) }, FieldStorage { cur_name: None, value: Owned(Field { meta: Chars, name: "prod_ips/[1]", value: Chars("192.xxx.xxx.55") }) }]` | `extensions_obj.source_private.prod_ips` | `source_private` |

## 人工语义复核（KB47750，SR-058）

- 事件事实：堡垒机记录用户访问目标资源前发起的双人授权流程，由管理员参与审批；日志未证明实际登录或持续权限变更。
- event_category：`auth`
- event_type：`user_login`（授权 preauth 流程）
- operation：`preauth`
- outcome：`unknown`（未证明实际登录）
- 主体/客体/载体：source_user / target_device_or_resource / none
- 审批人：`roles.related[].user{name=approver}`
- 证据：奇安信堡垒机 192.0.2.70 Syslog 格式说明 KB47750；对应 `logType` 为 `YAB_DBL_AUTH_LOG`。
- 状态：`reviewed_candidate`
