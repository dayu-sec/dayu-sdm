# qax_firewall / bh_his_session_record_log SDM2 候选样例

事件事实：堡垒机登记用户 `admin` 对运维资源 `DefaultRegion_Linux_10.xxx.xxx.78_22` 的历史 SSH 会话（运维账户 `root`）及回放地址。

- 主体：`user`（admin / 10.xxx.xxx.30）
- 客体：`managed_resource`
- 载体：`recorded_session`（回放地址；不是当场 SSH 连接）
- 关联：运维账户 `root`
- 观察者：来源安全产品

## 证据与限制

- 原始样本：`log-model/examples/qax_firewall/` 第 6 个非空行。
- WPL 规则：`bh_his_session_record_log`，运行时解析成功。
- `occur_time` 来自 WPL `startTime`（文档：会话开始时间），不是缺失字段。
- `account=root` 是运维账户，禁止覆盖 `source_user=admin`。
- `protocol=SSH` 写入 `carrier_protocol`，不升成 `network_connection`。
- 样本 `historySession` 与 `prod_name` 之间缺逗号，WPL 把 `prod_name` 吞进回放字段；原样保留。
- 无 `result`，`outcome=unknown`。
- 顶层 `severity` 为空。
- logical/physical/projection 校验保持 partial。

## 人工语义复核

- 事件事实：堡垒机登记用户 admin 对运维资源 DefaultRegion_Linux_10.xxx.xxx.78_22 的历史 SSH 会话（运维账户 root）及回放地址；不把历史记录扩写成当场发生的网络连接。account 不是 source_user。
- event_category：`audit`
- event_type：`generic_event`
- operation：`空；无充分标准动作证据`
- outcome：`unknown`
- 证据：奇安信堡垒机 192.0.2.70 Syslog 格式说明 KB47750 §2.6；对应 `logType` 为 `YAB_HISTORY_SESSION_LOG`。
- 状态：`reviewed_candidate`
