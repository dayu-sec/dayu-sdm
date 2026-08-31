# sxf_firewall / fw_system_op_log 运行时观测候选映射

事件事实：深信服防火墙系统操作日志——管理员 admin 从 198.51.100.54 启用 OSPF，op_info=OSPF 启用 成功。

主体：管理员（source.user=user_name + source.endpoint=op_user_ip）；客体：操作对象（target.service=op_object）；载体：`none`；观察者：来源产品。

> 状态：candidate，未注册、未批准。WPL 解析事实与深信服防火墙文档已确认；SR-071 人工复核结论见文末。

| WPL 字段 | 值 | SDM 候选路径 | 状态 |
|---|---|---|---|
| `time` | `2026-01-23 11:00:00` | `extensions_obj.source_private.time` | `source_private` |
| `domain` | `localhost` | `extensions_obj.source_private.domain` | `source_private` |
| `type` | `fwlog` | `extensions_obj.source_private.type` | `source_private` |
| `symbol` | `日志类型:系统操作` | `extensions_obj.source_private.symbol` | `source_private` |
| `logtype` | `系统操作` | `extensions_obj.source_private.logtype` | `source_private` |
| `user_name` | `admin` | `roles_obj.source.user.name` | `confirmed` |
| `op_user_ip` | `198.51.100.54` | `roles_obj.source.endpoint.ip` | `confirmed` |
| `op_object` | `启用禁用` | `roles_obj.target.service.name` | `confirmed` |
| `op_type` | `启用` | `extensions_obj.source_private.op_type` | `source_private` |
| `op_info` | `OSPF 启用 成功` | `outcome=success` | `confirmed` |

## 人工语义复核（SXF Firewall，SR-071）

- 事件事实：深信服防火墙记录管理员系统操作；具体动作语义保留来源字段。
- `event_category=audit`
- `event_type=status_update`（启用 OSPF 状态变更）
- `operation=empty`
- **`outcome=success`**（op_info=OSPF 启用 成功明确操作结果，同 SR-070）
- 主体/客体/载体：管理员（source.user+endpoint）/ 操作对象（target.service）/ none
- 文档证据：深信服防火墙 syslog 日志 8.0.50–8.0.95；样本字段已由 WPL 命中。
