# leadsec / leadsec_av SDM2 候选样例

事件事实：管理员 administrator 从 198.51.100.25 新增名为 test 的 AV 策略，result=0 表示操作正常。

- 主体：`administrator`（操作端 IP `198.51.100.25`）
- 客体：AV 策略资源 `test`
- 载体：无
- 观察者：来源安全产品

## 证据与限制

- 原始样本：`s4-doris/models/wpl/leadsec/sample.dat` 第 2 个非空行。
- WPL 规则：`leadsec_av`，运行时解析成功。
- 字段映射和枚举为候选，未知枚举保留原值并报告。
- `result=0` 由文档确认表示正常，映射 `outcome=success`。
- 顶层 `severity` 为空；来源严重度不机械投影。
- 人工语义已确认；未提供独立逻辑事件，因此 projection 校验保持 partial。

## 人工语义复核

- 事件事实：管理员 administrator 从 198.51.100.25 新增名为 test 的 AV 策略，result=0 表示操作正常。
- `event_category=audit`，`event_type=device_config_update`，`operation=empty`，`outcome=success`。
- `pri` 仅映射 `log_level`；来源 severity 保留在 `source_finding`。
- 文档证据：Power-V 192.0.2.120 日志格式手册 VERSION 0.3.0；证据状态 `vendor_confirmed_and_observed`。
- 对应章节：192.0.2.62「添加一条 av 策略」；`logtype=9` 是设备管理日志，`result=0` 表示正常。
- 主体为当前管理员 `administrator`（操作端 IP `198.51.100.25`）；客体为 AV 策略资源 `test`；无独立载体。
- 2.7.9 的 `logtype=7` 是另一种病毒告警格式，不适用于本样本。
