# sxf_firewall / fw_mail_security_log SDM2 候选样例

事件事实：深信服防火墙邮件安全检测（邮件安全日志）——攻击 192.0.2.2:25 → 203.0.113.15:25（SMTP）命中撞库攻击（规则 6646），op_action=拒绝，severity=高。

- 主体：攻击源 → `roles.source.endpoint(192.0.2.2:25)`
- 客体：SMTP 服务器 → `roles.target.endpoint(203.0.113.15:25)`
- 载体：网络协议 → `facets.network.protocol.code=smtp`
- 检测声明：`source_finding_obj{title=origin_alert_cat_name, severity, status=op_action, count, rule{name, signature_id=rule_id}}`
- 观察者：来源安全产品

## 证据与限制

- 原始样本：`s4-doris/models/wpl/sxf_firewall/sample.dat` 第 19 个非空行。
- WPL 规则：`fw_mail_security_log`，运行时解析成功。
- 字段映射和枚举为候选，未知枚举保留原值并报告。
- `outcome=unknown`；不将 `op_action`（拒绝）机械映射为动作结果。
- 顶层 `severity` 为空；来源严重度=高 保留在 source_finding.severity，不机械投影。

## 人工语义复核（深信服防火墙文档，SR-068）

- 事件事实：深信服防火墙记录邮件安全检测；具体邮件动作未由样本确认。
- event_category：`alert`
- event_type：`network_smtp`
- operation：`空`
- outcome：`unknown`；不将 `op_action` 或告警记录机械映射为动作结果。
- 主体/客体/载体：攻击源（source.endpoint）/ SMTP 服务器（target.endpoint）/ network_protocol（facets.network.protocol=smtp）
- 检测声明：`source_finding_obj`（title/severity/status/count/rule{name, signature_id}）
- 文档证据：深信服防火墙 syslog 日志 8.0.50–8.0.95；样本字段已由 WPL 命中。

## 当前物理注册表迁移

- expected 已按当前 `sdm_event.yaml` 87 字段物理注册表收敛。
- 攻击源/SMTP 服务器入 `roles.source/target.endpoint`。
- 协议入 `facets.network.protocol`；检测声明入 `source_finding_obj`（title/severity/status/count/rule）。
