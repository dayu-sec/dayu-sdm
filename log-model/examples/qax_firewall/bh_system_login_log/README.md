# qax_firewall / bh_system_login_log SDM2 候选样例

事件事实：用户或管理员发起认证/登录相关操作。

- 主体：`source_user`
- 客体：`target_device_or_resource`
- 载体：`observer_product`
- 观察者：来源安全产品

## 证据与限制

- 原始样本：`s4-doris/models/wpl/qax_firewall/sample.dat` 第 1 个非空行。
- WPL 规则：`bh_system_login_log`，运行时解析成功。
- 字段映射和枚举为候选，未知枚举保留原值并报告。
- `outcome=unknown`；没有把 finding 或日志存在机械映射为 observed。
- 顶层 `severity` 为空；来源严重度不机械投影。
- logical/physical/projection 校验保持 partial，等待事件语义人工确认。

## 人工语义复核

- 事件事实：堡垒机管理员在 Web 等方式发起系统登录，日志给出操作和结果。
- event_category：`auth`
- event_type：`user_login`
- operation：`interactive`
- outcome：`success`
- 证据：奇安信堡垒机 192.0.2.70 Syslog 格式说明 KB47750；对应 `logType` 为 `YAB_SYSTEM_LOGIN_LOG`。
- 状态：`reviewed_candidate`
