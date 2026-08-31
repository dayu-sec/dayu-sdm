# sxf_firewall / fw_ips_protect_log SDM2 候选样例

事件事实：深信服防火墙 IPS 防护（IPS防护日志）——攻击 203.0.113.113:80 → 203.0.113.118:80（tcp）命中 WebCalendar 本地文件包含和 PHP 代码注入漏洞（vuln_id=1265，策略 ips2），op_action=拒绝，severity=高。

- 主体：攻击源 → `roles.source.endpoint(203.0.113.113:80)`
- 客体：受害目标 → `roles.target.endpoint(203.0.113.118:80)`
- 载体：网络协议 → `facets.network.protocol.code=tcp`
- 检测声明：`source_finding_obj{title=origin_alert_cat_name, severity, status=op_action, count, rule{name=vuln_name, label=policy_name, signature_id=vuln_id}}`
- 观察者：来源安全产品

## 证据与限制

- 原始样本：`log-model/examples/sxf_firewall/` 第 3 个非空行。
- WPL 规则：`fw_ips_protect_log`，运行时解析成功。
- 字段映射和枚举为候选，未知枚举保留原值并报告。
- `outcome=unknown`；不将 `op_action`（拒绝）机械映射为动作结果。
- 顶层 `severity` 为空；来源严重度=高 保留在 source_finding.severity，不机械投影。

## 人工语义复核（深信服防火墙文档，SR-066）

- 事件事实：深信服防火墙记录 IPS 防护命中；protocol 与源/目标地址支持网络连接事实。
- event_category：`alert`
- event_type：`network_connection`
- operation：`空`
- outcome：`unknown`；不将 `op_action` 或告警记录机械映射为动作结果。
- 主体/客体/载体：攻击源（source.endpoint）/ 受害目标（target.endpoint）/ network_protocol（facets.network.protocol=tcp）
- 检测声明：`source_finding_obj`（title/severity/status/count/rule{name, label, signature_id}）
- 文档证据：深信服防火墙 syslog 日志 8.0.50–8.0.95；样本字段已由 WPL 命中。

## 当前物理注册表迁移

- expected 已按当前 `sdm_event.yaml` 87 字段物理注册表收敛。
- 攻击源/受害目标入 `roles.source/target.endpoint`。
- 协议入 `facets.network.protocol`；检测声明入 `source_finding_obj`（title/severity/status/count/rule）。
