# 360 / 360_edr_hotpatch_intercept_log SDM2 候选样例

事件事实：EDR 热补丁拦截——远程代码执行攻击（Apache Struts2 S2_057，高危）从 203.0.113.202:36938 对 192.0.2.125:8080 被阻断（action=阻断，protocol=tcp）。recorder=360edr_hotpatch_intercept_log。

- 主体：攻击源端点 → `roles.source.endpoint(203.0.113.202:36938)`
- 客体：被攻击端点 → `roles.target.endpoint(192.0.2.125:8080)`
- 载体：网络协议 → `facets.network.protocol.code=tcp`
- 检测声明：`source_finding_obj{title, severity=高危, count, action=blocked, rule{signature_id, name, version}}`
- 观察者：来源安全产品

## 证据与限制

- 原始样本：`s4-doris/models/wpl/360/sample.dat` 第 3 个非空行。
- WPL 规则：`360_edr_hotpatch_intercept_log`，运行时解析成功。
- 字段映射和枚举为候选，未知枚举保留原值并报告。
- `outcome=denied`；action=阻断，明确记录攻击被阻断。
- 顶层 `severity` 为空；来源严重度 `threat_level=高危` 保留在 source_finding.severity。

## 人工语义复核（360 EPP 文档，SR-044）

- 事件事实：EDR 热补丁日志明确记录远程代码执行攻击被阻断。
- event_category：`alert`
- event_type：`network_connection`（远程代码执行攻击的网络语义）
- operation：`空`
- outcome：`denied`（action=阻断）
- 主体/客体/载体：source_endpoint / protected_endpoint / network_protocol
- 检测声明：`source_finding_obj`（title/severity/count/action/rule）
- 文档证据：360《终端-EPP-SysLog文档》；当前 WPL 运行样本已命中。

## 当前物理注册表迁移

- expected 已按当前 `sdm_event.yaml` 87 字段物理注册表收敛。
- 攻击源/目标端点入 `roles.source/target.endpoint`。
- 协议入 `facets.network.protocol`；检测声明入 `source_finding_obj`。
