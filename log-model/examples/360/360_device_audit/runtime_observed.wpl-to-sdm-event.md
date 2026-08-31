# 360 / 360_device_audit 运行时观测候选映射

事件事实：终端 TEST-PC-01 记录 Kingston 便携设备“新加卷”插入；文档 17 定义 operation_type=1 为插入。

主体：`endpoint_host`；客体：`peripheral_device`；载体：`none`；观察者：360 EPP。

> 状态：candidate，未注册、未批准。仅 WPL 解析事实已确认，SDM 语义仍需人工复核。

| WPL 字段 | 值 | SDM 候选路径 | 状态 |
|---|---|---|---|
| `asset_username` | `hsakdjklas#@$%阿利克水泥钉金卡三年` | `extensions_obj.source_private.asset_username` | `source_private` |
| `client_group_id` | `21` | `extensions_obj.source_private.client_group_id` | `source_private` |
| `client_group_name` | `qsl` | `extensions_obj.source_private.client_group_name` | `source_private` |
| `clientip` | `203.0.113.37` | `roles_obj.source.host.ip + source_ip` | `mapped` |
| `cmp_loginuser` | `test-user` | `roles_obj.source.user.name + source_user` | `mapped` |
| `computername` | `TEST-PC-01` | `roles_obj.source.host.name + source_host` | `mapped` |
| `ctime` | `2026-01-23 11:00:00` | `occur_time` | `candidate` |
| `device_id` | `test-device_id` | `roles_obj.target.resource.id` | `mapped` |
| `device_type` | `便携设备` | `roles_obj.target.resource.subtype` | `mapped` |
| `devicemodel` | `test-devicemodel` | `roles_obj.target.resource.product` | `mapped` |
| `id` | `09f054a8-aaa1-40d9-b545-57adc7786dcf` | `extensions_obj.source_private.id` | `source_private` |
| `is_xc` | `2` | `extensions_obj.source_private.is_xc` | `source_private` |
| `type` | `device_audit` | `extensions_obj.source_private.type` | `source_private` |
| `m2` | `a17f1890bb3e71a61d8be6fe71d71b73fa02c41e2914` | `extensions_obj.source_private.m2` | `source_private` |
| `mac` | `00:00:5E:00:53:F4` | `roles_obj.source.host.mac` | `mapped` |
| `manufacturer` | `Kingston` | `roles_obj.target.resource.vendor` | `mapped` |
| `operation_type` | `1` | `roles_obj.target.resource.action (1 → connect)` | `mapped` |
| `pid_value` | `test-pid_value` | `extensions_obj.source_private.pid_value` | `source_private` |
| `plant_id` | `1` | `extensions_obj.source_private.plant_id` | `source_private` |
| `plat_id` | `1` | `extensions_obj.source_private.plat_id` | `source_private` |
| `send_time` | `2026-01-23 03:00:00` | `extensions_obj.source_private.send_time` | `source_private` |
| `sysmaclist` | `00:00:5E:00:53:F4` | `extensions_obj.source_private.sysmaclist` | `source_private` |
| `typename` | `新加卷` | `roles_obj.target.resource.name` | `mapped` |
| `username` | `test-user` | `extensions_obj.source_private.username` | `source_private` |
| `vid_value` | `test-vid_value` | `extensions_obj.source_private.vid_value` | `source_private` |

## 人工语义复核（360 EPP）

- 事件事实：终端 TEST-PC-01 记录 Kingston 便携设备“新加卷”插入；文档 17 定义 operation_type=1 为插入。
- 对应文档：17. 外设使用审计日志（6230 及后续版本）；证据状态 `vendor_confirmed_and_observed`。
- `operation_type=1` 映射外设动作 `connect`；文档中的 `2=拔出` 登记为未观测候选 `disconnect`。
- 主体为终端 `TEST-PC-01`，登录用户上下文为 `test-user`；客体为 Kingston 便携设备“新加卷”；无独立载体。
- 当前标准无专用外设插拔 event_type，因此保留 `event_type=generic_event`、`operation=empty`；动作保存在目标资源。
- `outcome=unknown`，因为样本没有独立的成功/失败字段。
