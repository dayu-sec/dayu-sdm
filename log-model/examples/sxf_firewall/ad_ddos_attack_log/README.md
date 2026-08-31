# sxf_firewall / ad_ddos_attack_log SDM2 候选样例

事件事实：深信服防火墙 DDoS 检测（DOS攻击日志）——源 203.0.113.164 对目的 192.0.2.220 发起 IP 宽松源路由选项报文攻击（策略 dos2），系统动作=拒绝，severity=低。

- 主体：攻击源 → `roles.source.endpoint(203.0.113.164)`
- 客体：受害目标 → `roles.target.endpoint(192.0.2.220)`
- 载体：无 → `carriers=[]`
- 检测声明：`source_finding_obj{title=origin_alert_cat_name, severity, status=op_action, count, rule{name, label=policy_name}}`
- 观察者：来源安全产品

## 证据与限制

- 原始样本：`log-model/examples/sxf_firewall/` 第 5 个非空行。
- WPL 规则：`ad_ddos_attack_log`，运行时解析成功。
- 字段映射和枚举为候选，未知枚举保留原值并报告。
- `outcome=unknown`；不将 `op_action`（拒绝）机械映射为动作结果。
- 顶层 `severity` 为空；来源严重度=低 保留在 source_finding.severity，不机械投影。

## 人工语义复核（深信服防火墙文档，SR-063）

- 事件事实：深信服防火墙记录 DDoS 检测告警；攻击结论保留 source_finding。
- event_category：`alert`
- event_type：`network_connection`（DDoS 攻击网络语义）
- operation：`空`
- outcome：`unknown`；不将 `op_action` 或告警记录机械映射为动作结果。
- 主体/客体/载体：攻击源（source.endpoint）/ 受害目标（target.endpoint）/ none
- 检测声明：`source_finding_obj`（title/severity/status/count/rule{name, label=policy_name}）
- 文档证据：深信服防火墙 syslog 日志 8.0.50–8.0.95；样本字段已由 WPL 命中。

## 当前物理注册表迁移

- expected 已按当前 `sdm_event.yaml` 87 字段物理注册表收敛。
- 攻击源/受害目标入 `roles.source/target.endpoint`。
- 攻击结论入 `source_finding_obj`（title/severity/status/count/rule）。
