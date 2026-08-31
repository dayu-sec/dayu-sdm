# topas_firewall / topas_firewall_admin 运行时观测候选映射

事件事实：防火墙管理员日志——用户 superman 通过串口(Serial)本地登录防火墙(TopsecOS)，result=success。

主体：管理员（source.user=user + source.endpoint=src）；客体：防火墙设备（target.host=dev）；载体：`authentication`（facets.authentication.auth_type=Serial）；观察者：来源产品。

> 状态：candidate，未注册、未批准。WPL 解析事实与天融信防火墙文档已确认；SR-078 人工复核结论见文末。

| WPL 字段 | 值 | SDM 候选路径 | 状态 |
|---|---|---|---|
| `id` | `NGTOS` | `event_id` | `candidate` |
| `version` | `V3.2294.23037_NGFW.1_R` | `extensions_obj.source_private.version` | `source_private` |
| `time` | `2026-01-23 11:00:00` | `occur_time` | `candidate` |
| `dev` | `TopsecOS` | `extensions_obj.source_private.dev` | `source_private` |
| `pri` | `6` | `extensions_obj.source_private.pri` | `source_private` |
| `type` | `admin` | `extensions_obj.source_private.type` | `source_private` |
| `recorder` | `admin` | `extensions_obj.source_private.recorder` | `source_private` |
| `index` | `2010` | `event_id` | `candidate` |
| `vsid` | `0` | `extensions_obj.source_private.vsid` | `source_private` |
| `user` | `superman` | `roles_obj.source.user.name` | `confirmed` |
| `src` | `192.0.2.85` | `roles_obj.source.endpoint.ip` | `confirmed` |
| `op` | `local login` | `extensions_obj.source_private.op` | `source_private` |
| `method` | `Serial` | `facets_obj.authentication.auth_type` | `confirmed` |
| `result` | `success` | `outcome=success` | `confirmed` |
| `description` | `login success` | `extensions_obj.source_private.description` | `source_private` |

## 人工语义复核（Topas Firewall，SR-078）

- 事件事实：防火墙管理员日志记录通过串口本地登录，result=success。
- `event_category=auth`，`event_type=user_login`，`operation=interactive`，`outcome=success`（result=success）。
- 主体/客体/载体：管理员（source.user+endpoint）/ 防火墙设备（target.host）/ authentication（facets.authentication.auth_type=Serial）
- `pri` 仅进入 `log_level`。
- 文档证据：天融信《防火墙日志规范 v23.2》对应 admin/ac 章节。
