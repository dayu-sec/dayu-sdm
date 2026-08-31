# topas_firewall / topas_firewall_ac SDM2 候选样例

事件事实：记录源端到目标端的网络连接或访问控制活动。

- 主体：`source_host_or_ip`
- 客体：`target_host_or_ip`
- 载体：`network_protocol_or_session`
- 观察者：来源安全产品

## 证据与限制

- 原始样本：`log-model/examples/topas_firewall/` 第 3 个非空行。
- WPL 规则：`topas_firewall_ac`，运行时解析成功。
- 字段映射和枚举为候选，未知枚举保留原值并报告。
- `outcome=unknown`；没有把 finding 或日志存在机械映射为 observed。
- 顶层 `severity` 为空；来源严重度不机械投影。
- logical/physical/projection 校验保持 partial，等待事件语义人工确认。

## 人工语义复核

- 事件事实：防火墙访问控制日志记录 UDP 会话命中策略，action=accept 的厂商枚举含义为允许。
- `event_category=network`，`event_type=network_connection`，`operation=empty`，`outcome=allowed`。
- `pri` 仅进入 `log_level`。
- 文档证据：天融信《防火墙日志规范 v23.2》对应 admin/ac 章节。
