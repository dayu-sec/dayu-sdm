# sxf_firewall / fw_ssl_vpn_user_log 运行时观测候选映射

事件事实：深信服防火墙 SSL VPN 用户行为日志——用户 wjj 从 198.51.100.109 登录 SSL VPN，op_info=登录成功。

主体：VPN 用户（source.user=user_name + source.endpoint=op_user_ip）；客体：SSL VPN 服务（target.service=op_object）；载体：`none`；观察者：来源产品。

> 状态：candidate，未注册、未批准。WPL 解析事实与深信服防火墙文档已确认；SR-070 人工复核结论见文末。

| WPL 字段 | 值 | SDM 候选路径 | 状态 |
|---|---|---|---|
| `time` | `2026-01-23 11:00:00` | `extensions_obj.source_private.time` | `source_private` |
| `domain` | `localhost` | `extensions_obj.source_private.domain` | `source_private` |
| `type` | `fwlog` | `extensions_obj.source_private.type` | `source_private` |
| `symbol` | `日志类型:SSL VPN用户行为日志` | `extensions_obj.source_private.symbol` | `source_private` |
| `logtype` | `SSL VPN用户行为日志` | `extensions_obj.source_private.logtype` | `source_private` |
| `user_name` | `wjj` | `roles_obj.source.user.name` | `confirmed` |
| `op_user_ip` | `198.51.100.109` | `roles_obj.source.endpoint.ip` | `confirmed` |
| `op_object` | `SSL VPN` | `roles_obj.target.service.name` | `confirmed` |
| `op_type` | `登录` | `extensions_obj.source_private.op_type` | `source_private` |
| `login_time` | `2026-01-23 11:00:00` | `extensions_obj.source_private.login_time` | `source_private` |
| `op_info` | `登录成功` | `outcome=success` | `confirmed` |

## 人工语义复核（SXF Firewall，SR-070）

- 事件事实：深信服防火墙记录 SSL VPN 用户操作/登录相关事件。
- `event_category=auth`
- `event_type=user_login`
- `operation=remote_service`
- **`outcome=success`**（op_info=登录成功明确认证结果）
- 主体/客体/载体：VPN 用户（source.user+endpoint）/ SSL VPN 服务（target.service）/ none
- 文档证据：深信服防火墙 syslog 日志 8.0.50–8.0.95；样本字段已由 WPL 命中。
