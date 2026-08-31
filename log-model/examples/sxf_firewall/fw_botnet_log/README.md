# sxf_firewall / fw_botnet_log SDM2 候选样例

事件事实：深信服防火墙僵尸网络检测（僵尸网络日志）——源 192.0.2.163:4720 访问僵尸网络 C2 www.audi_log.org（192.0.2.220:80），特征 ID 34014989，op_action=拒绝，severity=低。

- 主体：僵尸主机 → `roles.source.endpoint(192.0.2.163:4720)`
- 客体：僵尸网络 C2 → `roles.target.domain(www.audi_log.org)` + `roles.target.endpoint(192.0.2.220:80)`
- 载体：HTTP 请求 → `facets.http.request.host=www.audi_log.org`
- 检测声明：`source_finding_obj{title, severity, status=op_action, count, rule{name, signature_id}}`
- 观察者：来源安全产品

## 证据与限制

- 原始样本：`log-model/examples/sxf_firewall/` 第 15 个非空行。
- WPL 规则：`fw_botnet_log`，运行时解析成功。
- 字段映射和枚举为候选，未知枚举保留原值并报告。
- `outcome=unknown`；不将 `op_action`（拒绝）机械映射为动作结果。
- 顶层 `severity` 为空；来源严重度=低 保留在 source_finding.severity，不机械投影。

## 人工语义复核（深信服防火墙文档，SR-065）

- 事件事实：深信服防火墙记录僵尸网络检测；检测结论保留 source_finding。
- event_category：`alert`
- event_type：`network_connection`
- operation：`空`
- outcome：`unknown`；不将 `op_action` 或告警记录机械映射为动作结果。
- 主体/客体/载体：僵尸主机（source.endpoint）/ 僵尸网络 C2（target.domain+endpoint）/ http（facets.http.request）
- 检测声明：`source_finding_obj`（title/severity/status/count/rule{name, signature_id}）
- 文档证据：深信服防火墙 syslog 日志 8.0.50–8.0.95；样本字段已由 WPL 命中。

## 当前物理注册表迁移

- expected 已按当前 `sdm_event.yaml` 87 字段物理注册表收敛。
- 僵尸主机入 `roles.source.endpoint`；C2 入 `roles.target.domain+endpoint`。
- HTTP 请求入 `facets.http.request.host`；检测声明入 `source_finding_obj`（title/severity/status/count/rule）。
