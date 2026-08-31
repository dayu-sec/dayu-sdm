# 360 / 360_device_audit SDM2 候选样例

事件事实：终端 qiushilong-PC 记录 Kingston 便携设备“新加卷”插入；文档 17 定义 operation_type=1 为插入。

- 主体：终端 `qiushilong-PC`（登录用户 `qiushilong`）
- 客体：Kingston 便携设备“新加卷”
- 载体：无
- 观察者：来源安全产品

## 证据与限制

- 原始样本：`s4-doris/models/wpl/360/sample.dat` 第 2 个非空行。
- WPL 规则：`360_device_audit`，运行时解析成功。
- 字段映射和枚举为候选，未知枚举保留原值并报告。
- `outcome=unknown`；没有把 finding 或日志存在机械映射为 observed。
- 顶层 `severity` 为空；来源严重度不机械投影。
- 人工语义已确认；未提供独立逻辑事件，因此 projection 校验保持 partial。

## 人工语义复核

- 事件事实：终端 qiushilong-PC 记录 Kingston 便携设备“新加卷”插入；文档 17 定义 operation_type=1 为插入。
- 对应文档：17. 外设使用审计日志（6230 及后续版本）；证据状态 `vendor_confirmed_and_observed`。
- `operation_type=1` 映射外设动作 `connect`；文档中的 `2=拔出` 登记为未观测候选 `disconnect`。
- 主体为终端 `qiushilong-PC`，登录用户上下文为 `qiushilong`；客体为 Kingston 便携设备“新加卷”；无独立载体。
- 当前标准无专用外设插拔 event_type，因此保留 `event_type=generic_event`、`operation=empty`；动作保存在目标资源。
- `outcome=unknown`，因为样本没有独立的成功/失败字段。
