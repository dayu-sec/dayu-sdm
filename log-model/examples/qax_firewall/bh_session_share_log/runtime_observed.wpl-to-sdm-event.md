# qax_firewall / bh_session_share_log 运行时观测候选映射

事件事实：堡垒机会话协同（logType=YAB_SESSION_SHARE_LOG）——用户 admin 将会话分享给 testUser，记录加入/退出时间。

主体：`user`（source.user=shareUser + source.endpoint=sourceIp）；客体：`collaborating_user`（target.user=user）；载体：`none`；观察者：来源产品。

> 状态：candidate，未注册、未批准。WPL 解析事实与 KB47750 已确认；SR-056 人工复核结论见文末。

| WPL 字段 | 值 | SDM 候选路径 | 状态 |
|---|---|---|---|
| `access_time` | `2026-02-03 16:55:13.733618` | `extensions_obj.source_private.access_time` | `source_private` |
| `logType` | `YAB_SESSION_SHARE_LOG` | `extensions_obj.source_private.logType` | `source_private` |
| `shareUser` | `admin` | `roles_obj.source.user.name` | `confirmed` |
| `user` | `testUser` | `roles_obj.target.user.name` | `confirmed` |
| `prod_name` | `堡垒机` | `extensions_obj.source_private.prod_name` | `source_private` |
| `prod_id` | `f73b12355cd64a4ea36d42ed9c4d1e4e` | `extensions_obj.source_private.prod_id` | `source_private` |
| `prod_version` | `203.0.113.245` | `extensions_obj.source_private.prod_version` | `source_private` |
| `prod_ips` | `[FieldStorage { cur_name: None, value: Owned(Field { meta: Chars, name: "prod_ips/[0]", value: Chars("10.xxx.xxx.127") }) }, FieldStorage { cur_name: None, value: Owned(Field { meta: Chars, name: "prod_ips/[1]", value: Chars("192.xxx.xxx.55") }) }]` | `extensions_obj.source_private.prod_ips` | `source_private` |
| `joinTime` | `2026-01-23 11:00:00` | `extensions_obj.source_private.joinTime` | `source_private` |
| `exitTime` | `2026-01-23 11:00:00` | `extensions_obj.source_private.exitTime` | `source_private` |
| `sourceIp` | `192.xxx.xxx.20` | `roles_obj.source.endpoint.ip` + `source_ip` | `confirmed` |

## 人工语义复核（KB47750，SR-056）

- 事件事实：堡垒机用户发起会话协同并记录协同用户加入/退出时间。
- event_category：`audit`
- event_type：`user_resource_update_permissions`（会话分享=权限授予）
- operation：`share`
- outcome：`unknown`
- 主体/客体/载体：user（source.user=shareUser）/ collaborating_user（target.user=user）/ none
- 加入/退出时间（joinTime/exitTime）无标准路径，保留 source_private
- 证据：奇安信堡垒机 192.0.2.70 Syslog 格式说明 KB47750；对应 `logType` 为 `YAB_SESSION_SHARE_LOG`。
- 状态：`reviewed_candidate`
