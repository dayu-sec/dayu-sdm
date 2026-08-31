# sxf_firewall / fw_local_access_log SDM2 候选样例

事件事实：深信服防火墙本地访问连接（本机安全日志）——源 198.51.100.66:1025 访问本地端口 762（SSL_HELLO），op_action=拒绝。

- 主体：访问源 → `roles.source.endpoint(198.51.100.66:1025)`
- 客体：本地目标 → `roles.target.endpoint(port=762)`（无目标 IP，本地访问）
- 载体：应用 → `facets.application.name=SSL`
- 观察者：来源安全产品

## 证据与限制

- 原始样本：`log-model/examples/sxf_firewall/` 第 21 个非空行。
- WPL 规则：`fw_local_access_log`，运行时解析成功。
- 字段映射和枚举为候选，未知枚举保留原值并报告。
- `outcome=unknown`；不将 `op_action`（拒绝）机械映射为动作结果。
- `source_finding_obj=null`：本地访问连接审计，非检测告警。

## 人工语义复核（深信服防火墙文档，SR-067）

- 事件事实：深信服防火墙记录源端到目标端的本地访问连接。
- event_category：`network`
- event_type：`network_connection`
- operation：`空`
- outcome：`unknown`；不将 `op_action` 或告警记录机械映射为动作结果。
- 主体/客体/载体：访问源（source.endpoint）/ 本地目标（target.endpoint，无目标 IP）/ application（facets.application.name=SSL）
- 文档证据：深信服防火墙 syslog 日志 8.0.50–8.0.95；样本字段已由 WPL 命中。

## 当前物理注册表迁移

- expected 已按当前 `sdm_event.yaml` 87 字段物理注册表收敛。
- 访问源入 `roles.source.endpoint`；本地目标入 `roles.target.endpoint`（无目标 IP）。
- 应用类型入 `facets.application.name`；source_finding_obj=null（访问连接审计）。
