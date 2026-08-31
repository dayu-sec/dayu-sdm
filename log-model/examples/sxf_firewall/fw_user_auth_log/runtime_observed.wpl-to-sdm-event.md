# sxf_firewall / fw_user_auth_log 运行时观测候选映射

事件事实：深信服防火墙用户认证日志——用户 192.0.2.131 注销（op_object=注销），登录时长 1569 秒。

主体：认证用户（source.user=user_name + source.endpoint=op_user_ip）；客体：`none`；载体：`none`；观察者：来源产品。

> 状态：candidate，未注册、未批准。WPL 解析事实与深信服防火墙文档已确认；SR-072 人工复核结论见文末。

| WPL 字段 | 值 | SDM 候选路径 | 状态 |
|---|---|---|---|
| `time` | `2026-01-23 11:00:00` | `extensions_obj.source_private.time` | `source_private` |
| `domain` | `localhost` | `extensions_obj.source_private.domain` | `source_private` |
| `type` | `fwlog` | `extensions_obj.source_private.type` | `source_private` |
| `symbol` | `日志类型:用户认证` | `extensions_obj.source_private.symbol` | `source_private` |
| `logtype` | `用户认证` | `extensions_obj.source_private.logtype` | `source_private` |
| `user_name` | `192.0.2.131` | `roles_obj.source.user.name` | `confirmed` |
| `op_user_ip` | `192.0.2.131` | `roles_obj.source.endpoint.ip` | `confirmed` |
| `op_object` | `注销` | `event_type=user_logout` | `confirmed` |
| `login_time` | `2026-01-23 11:00:00` | `extensions_obj.source_private.login_time` | `source_private` |
| `login_duration_time` | `1569` | `extensions_obj.source_private.login_duration_time` | `source_private` |
| `logoff_time` | `11:00:00` | `extensions_obj.source_private.logoff_time` | `source_private` |

## 人工语义复核（SXF Firewall，SR-072）

- 事件事实：深信服防火墙记录用户认证/注销事件；结果字段未提供。
- `event_category=auth`
- **`event_type=user_logout`**（op_object=注销；原 user_login+logon 是登录语义）
- `operation=empty`
- `outcome=unknown`；结果字段未提供，不机械映射。
- 主体/客体/载体：认证用户（source.user+endpoint）/ none / none
- 文档证据：深信服防火墙 syslog 日志 8.0.50–8.0.95；样本字段已由 WPL 命中。
