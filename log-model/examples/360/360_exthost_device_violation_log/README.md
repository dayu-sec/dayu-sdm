# 360 / 360_exthost_device_violation_log SDM2 候选样例

事件事实：终端 WIN-EX02 尝试同时使用有线和无线网络，命中违规网络控制策略并执行 blockandalarm。

- 主体：终端 `WIN-EX02`（用户 `WIN-EX02\\Administrator`）
- 客体：违规网络控制策略 `wired_wifi_together_banned`
- 载体：无
- 观察者：来源安全产品

## 证据与限制

- 原始样本：`log-model/examples/360/` 第 5 个非空行。
- WPL 规则：`360_exthost_device_violation_log`，运行时解析成功。
- 字段映射和枚举为候选，未知枚举保留原值并报告。
- `outcome=unknown`；没有把 finding 或日志存在机械映射为 observed。
- 顶层 `severity` 为空；来源严重度不机械投影。
- 人工语义已确认；未提供独立逻辑事件，因此 projection 校验保持 partial。

## 人工语义复核

- 事件事实：终端 WIN-EX02 尝试同时使用有线和无线网络，命中违规网络控制策略并执行 blockandalarm。
- 对应文档：32. 违规网络控制审计（7000 及后续版本）；证据状态 `vendor_confirmed_and_observed`。
- 主体为终端 `WIN-EX02`（本机 IP `203.0.113.202`），用户上下文为 `WIN-EX02\\Administrator`。
- 客体为命中的违规网络控制策略 `wired_wifi_together_banned`；样本没有具体网卡标识，不构造虚假网卡对象。
- `deal_type=blockandalarm` 保留来源原值，并映射 `outcome=denied` 和策略动作 `block_and_alarm`。
- 当前标准没有专用违规网络控制 event_type，因此保留 `event_type=generic_event`、`operation=empty`。
- `clientip=203.0.113.37` 是客户端通讯 IP，投影设备管理地址；行为源 IP 使用文档定义的 `local_ip`。
