# qax_firewall / bh_resource_login_log 运行时观测候选映射

事件事实：堡垒机资源登录（logType=YAB_RESOURCE_LOGIN_LOG）——用户 admin 通过 SSH 登录目标资源「主机 1」的 root 账户。

主体：`source_user`（source.user=user + source.endpoint=sourceIP）；客体：`target_device_or_resource`（target.host=resource/targetIP + target.account=account）；载体：`none`（认证方式入 facets.authentication）；观察者：来源产品。

> 状态：candidate，未注册、未批准。WPL 解析事实与 KB47750 已确认；SR-055 人工复核结论见文末。

| WPL 字段 | 值 | SDM 候选路径 | 状态 |
|---|---|---|---|
| `access_time` | `2026-02-03 16:55:13.733618` | `extensions_obj.source_private.access_time` | `source_private` |
| `logType` | `YAB_RESOURCE_LOGIN_LOG` | `extensions_obj.source_private.logType` | `source_private` |
| `startTime` | `2026-01-23 11:00:00` | `extensions_obj.source_private.startTime` | `source_private` |
| `endTime` | `2026-01-23 11:00:00` | `extensions_obj.source_private.endTime` | `source_private` |
| `user` | `admin` | `roles_obj.source.user.name` | `confirmed` |
| `sourceIP` | `192.xxx.xxx.20` | `roles_obj.source.endpoint.ip` + `source_ip` | `confirmed` |
| `resource` | `主机 1` | `roles_obj.target.host.name` | `confirmed` |
| `targetIP` | `192.xxx.xxx.40` | `roles_obj.target.host.ip` + `target_ip` | `confirmed` |
| `protocol` | `SSH` | `facets_obj.authentication.auth_type` | `confirmed` |
| `account` | `root` | `roles_obj.target.account.name` | `confirmed` |
| `prod_name` | `堡垒机` | `extensions_obj.source_private.prod_name` | `source_private` |
| `prod_id` | `f73b12355cd64a4ea36d42ed9c4d1e4e` | `extensions_obj.source_private.prod_id` | `source_private` |
| `prod_version` | `203.0.113.245` | `extensions_obj.source_private.prod_version` | `source_private` |

## 人工语义复核（KB47750，SR-055）

- 事件事实：堡垒机用户发起到目标资源的 SSH 等资源登录；样本未提供结果。
- event_category：`auth`
- event_type：`user_login`
- operation：`remote_service`
- outcome：`unknown`
- 主体/客体/载体：source_user / target_device_or_resource（target.host+account）/ none
- 认证方式：`facets.authentication.auth_type=SSH`
- 证据：奇安信堡垒机 192.0.2.70 Syslog 格式说明 KB47750；对应 `logType` 为 `YAB_RESOURCE_LOGIN_LOG`。
- 状态：`reviewed_candidate`
