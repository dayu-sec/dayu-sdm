# sxf_firewall / fw_web_threat SDM2 候选样例

事件事实：深信服防火墙 Web 威胁检测（WEB威胁日志）——用户 b（203.0.113.107）访问 URL http://203.0.113.107/repro/ss（p2p），op_action=拒绝。

- 主体：访问用户 → `roles.source.user{name=b}` + `source.endpoint(203.0.113.107)`
- 客体：Web 目标 → `roles.target.endpoint(198.51.100.123)` + `roles.target.domain(203.0.113.107)`
- 载体：HTTP + 应用 → `facets.http.request.host` + `facets.application.name=p2p`
- 检测声明：`source_finding_obj{title, status=op_action, count, rule{name, label=policy_name}}`
- 观察者：来源安全产品

## 证据与限制

- 原始样本：`s4-doris/models/wpl/sxf_firewall/sample.dat` 第 9 个非空行。
- WPL 规则：`fw_web_threat`，运行时解析成功。
- 字段映射和枚举为候选，未知枚举保留原值并报告。
- `outcome=unknown`；不将 `op_action`（拒绝）机械映射为动作结果。
- 顶层 `severity` 为空；来源严重度不机械投影。

## 人工语义复核（深信服防火墙文档，SR-074）

- 事件事实：深信服防火墙记录 Web 威胁检测；用户和 URL 作为来源证据。
- event_category：`alert`
- event_type：`network_http`
- operation：`空`
- outcome：`unknown`；不将 `op_action` 或告警记录机械映射为动作结果。
- 主体/客体/载体：访问用户（source.user+endpoint）/ Web 目标（target.endpoint+domain）/ http + application
- 检测声明：`source_finding_obj`（title/status/count/rule{name, label}）
- 文档证据：深信服防火墙 syslog 日志 8.0.50–8.0.95；样本字段已由 WPL 命中。

## 当前物理注册表迁移

- expected 已按当前 `sdm_event.yaml` 87 字段物理注册表收敛。
- 访问用户入 `roles.source.user+endpoint`；Web 目标入 `roles.target.endpoint+domain`。
- HTTP 请求入 `facets.http.request.host`；应用入 `facets.application.name`；检测声明入 `source_finding_obj`。
