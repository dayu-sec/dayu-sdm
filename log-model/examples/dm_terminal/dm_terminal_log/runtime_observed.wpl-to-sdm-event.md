# dm_terminal / dm_terminal_log 运行时观测候选映射

事件事实：思科交换机的端口 FastEthernet1/0/9 状态变为 DOWN；event_class_id=0x0100、event_id=0x0102 与厂商文档的设备事件/交换机端口 DOWN 枚举一致。

主体：`network_switch`；客体：`network_port`；载体：`none`；观察者：北信源准入产品。

> 状态：candidate，未注册、未批准。仅 WPL 解析事实已确认，SDM 语义仍需人工复核。

| WPL 字段 | 值 | SDM 候选路径 | 状态 |
|---|---|---|---|
| `devid` | `7bb0851bcb4cdfec3a5fcc662bdbad5e` | `roles_obj.source.resource.id` | `mapped` |
| `time` | `2026-01-23 03:00:00` | `occur_time` | `mapped` |
| `event_class_id` | `0x0100` | `extensions_obj.source_private.event_class_id` | `mapped` |
| `event_id` | `0x0102` | `extensions_obj.source_private.event_id` | `mapped` |
| `name` | `思科交换机` | `roles_obj.source.resource.name + device_name` | `mapped` |
| `ipaddr` | `198.51.100.228` | `roles_obj.source.resource.management_ip + device_ip/device_ipv4` | `mapped` |
| `port_name` | `FastEthernet1/0/9` | `roles_obj.target.resource.name` | `mapped` |
| `alarm` | `1` | `source_finding_obj.status` | `mapped` |
| `level` | `5` | `source_finding_obj.severity` | `mapped` |
| `details` | `交换机[198.51.100.228]的端口[FastEthernet1/0/9]发生DOWN操作` | `source_finding_obj.title` | `mapped` |

## 人工语义复核（DM Terminal）

- 事件事实：思科交换机的端口 FastEthernet1/0/9 状态变为 DOWN；event_class_id=0x0100、event_id=0x0102 与厂商文档的设备事件/交换机端口 DOWN 枚举一致。
- 主体：思科交换机；客体：状态变为 DOWN 的交换机端口；无独立载体。
- 当前 `roles.source` 不支持 `device` 类型，因此交换机按 `resource(type=network_switch)` 建模；端口按 `resource(type=network_port)` 建模并关联交换机。
- `ipaddr=198.51.100.228` 是交换机管理 IP，投影 `device_ip/device_ipv4`，不投影 `source_ip`。
- `event_category=alert`，`event_type=status_update`，`outcome=unknown`；DOWN 是状态，不是动作结果。
- `level=5` 保留在 `source_finding.severity`，顶层 `severity` 为空。
- 文档证据：北信源《网络接入控制系统 SYSLOG 接口说明文档 V1.1》设备事件表：event_class_id=0x0100，交换机端口 DOWN 的 event_id=0x0102；样本已观测。 证据状态 `vendor_confirmed_and_observed`。
