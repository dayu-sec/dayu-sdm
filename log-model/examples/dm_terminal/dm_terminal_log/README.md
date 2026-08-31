# dm_terminal / dm_terminal_log SDM2 候选样例

事件事实：思科交换机的端口 FastEthernet1/0/9 状态变为 DOWN；event_class_id=0x0100、event_id=0x0102 与厂商文档的设备事件/交换机端口 DOWN 枚举一致。

- 主体：`network_switch`（思科交换机）
- 客体：`network_port`（FastEthernet1/0/9）
- 载体：无
- 观察者：来源安全产品

## 证据与限制

- 原始样本：`s4-doris/models/wpl/dm_terminal/sample.dat` 第 1 个非空行。
- WPL 规则：`dm_terminal_log`，运行时解析成功。
- 字段映射和枚举为候选，未知枚举保留原值并报告。
- `outcome=unknown`；没有把 finding 或日志存在机械映射为 observed。
- 顶层 `severity` 为空；来源严重度不机械投影。
- 人工语义已确认；未提供独立逻辑事件，因此 logical_schema 未执行，projection_consistency 为 partial。

## 人工语义复核

- 事件事实：思科交换机的端口 FastEthernet1/0/9 状态变为 DOWN；event_class_id=0x0100、event_id=0x0102 与厂商文档的设备事件/交换机端口 DOWN 枚举一致。
- 主体：思科交换机；客体：状态变为 DOWN 的交换机端口；无独立载体。
- 当前 `roles.source` 不支持 `device` 类型，因此交换机按 `resource(type=network_switch)` 建模；端口按 `resource(type=network_port)` 建模并关联交换机。
- `ipaddr=198.51.100.228` 是交换机管理 IP，投影 `device_ip/device_ipv4`，不投影 `source_ip`。
- `event_category=alert`，`event_type=status_update`，`outcome=unknown`；DOWN 是状态，不是动作结果。
- `level=5` 保留在 `source_finding.severity`，顶层 `severity` 为空。
- 文档证据：北信源《网络接入控制系统 SYSLOG 接口说明文档 V1.1》设备事件表：event_class_id=0x0100，交换机端口 DOWN 的 event_id=0x0102；样本已观测。 证据状态 `vendor_confirmed_and_observed`。
