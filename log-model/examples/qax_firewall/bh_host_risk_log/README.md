# qax_firewall / bh_host_risk_log SDM2 候选样例

事件事实：堡垒机报告主机风险：`riskType=risk_user`，`content=system risk account:yabroot`。

- 主体：`none`
- 客体：`host`（堡垒机自身；无单独目标 IP）
- 载体：`none`
- 关联：系统用户 `root`（不是主体）
- 观察者：来源安全产品
- 发现：`source_finding` = risk_user / system risk account:yabroot

## 证据与限制

- 原始样本：`log-model/examples/qax_firewall/` 第 12 个非空行。
- WPL 规则：`bh_host_risk_log`，运行时解析成功。
- `riskType`：文档表 USER/PRODCESS/NET_CONNECT，示例与样本为 `risk_user`，`conflicted`；expected 保留观测值。
- 不从 `content` 抽取 `yabroot` 作为独立用户客体。
- `user=root` 不写 `source_user`。
- `outcome=unknown`；finding 存在不映射 `observed`。
- 顶层 `severity` 为空。
- logical/physical/projection 校验保持 partial。

## 人工语义复核

- 事件事实：堡垒机报告主机风险：riskType=risk_user，content=system risk account:yabroot。这是来源发现，不是已完成处置。文档字段表写 USER/PRODCESS/NET_CONNECT，示例与样本为 risk_user，枚举 conflicted。user=root 是系统用户名，不是主体。
- event_category：`alert`
- event_type：`generic_event`
- operation：`空；无充分标准动作证据`
- outcome：`unknown`
- 证据：奇安信堡垒机 192.0.2.70 Syslog 格式说明 KB47750 §2.12；对应 `logType` 为 `YAB_HOST_RISK_LOG`。
- 状态：`reviewed_candidate`
