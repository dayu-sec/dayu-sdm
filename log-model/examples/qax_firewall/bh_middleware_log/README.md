# qax_firewall / bh_middleware_log SDM2 候选样例

事件事实：系统用户 `root` 侧记录中间件 `redis` 的操作内容「start redis service」。

- 主体：`user`（系统用户 root，不是运维员）
- 客体：`middleware_service`（redis）
- 载体：`none`
- 观察者：来源安全产品

## 证据与限制

- 原始样本：`s4-doris/models/wpl/qax_firewall/sample.dat` 第 14 个非空行。
- WPL 规则：`bh_middleware_log`，运行时解析成功。
- `middleType` 文档无闭合枚举；样本值为 redis。
- `content` 是操作内容自由文本，不投影为 `service_start`，不推断 `outcome`。
- 无 `result`，`outcome=unknown`。
- 顶层 `severity` 为空。
- logical/physical/projection 校验保持 partial。

## 人工语义复核

- 事件事实：系统用户 root 侧记录中间件 redis 的操作内容「start redis service」。content 为自由文本，不升成 service_start；无结果字段，outcome=unknown。
- event_category：`system`
- event_type：`generic_event`
- operation：`空；无充分标准动作证据`
- outcome：`unknown`
- 证据：奇安信堡垒机 192.0.2.70 Syslog 格式说明 KB47750 §2.14；对应 `logType` 为 `YAB_MIDDLE_WARE_LOG`。
- 状态：`reviewed_candidate`
