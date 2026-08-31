# sxf_firewall / fw_antivirus_virus SDM2 候选样例

事件事实：深信服防火墙病毒查杀（病毒查杀日志）——用户 donnie（192.0.2.84:8271）访问邮件 URL（http://192.0.2.200/...pdf）检出 Backdoor.RmtBomb.2，op_action=拒绝，severity=高。

- 主体：访问用户 → `roles.source.user{name=donnie}` + `source.endpoint(192.0.2.84:8271)`
- 客体：邮件服务器 → `roles.target.endpoint(954f:2588:3600:::110)`
- 载体：HTTP 请求 → `facets.http.request.host=192.0.2.200`
- 检测声明：`source_finding_obj{title=virus_name, severity, status=op_action, count, rule{name, label=policy_name}, file{url}}`
- 观察者：来源安全产品

## 证据与限制

- 原始样本：`log-model/examples/sxf_firewall/` 第 7 个非空行。
- WPL 规则：`fw_antivirus_virus`，运行时解析成功。
- 字段映射和枚举为候选，未知枚举保留原值并报告。
- `outcome=unknown`；不将 `op_action`（拒绝）机械映射为动作结果。
- 顶层 `severity` 为空；来源严重度=高 保留在 source_finding.severity，不机械投影。

## 人工语义复核（深信服防火墙文档，SR-064）

- 事件事实：深信服防火墙记录上传/文件病毒检测；来源处置不等同底层 outcome。
- event_category：`alert`
- **event_type：`generic_event`**（06 无病毒查杀类型；不是 file_read——检测事件无文件读取证据，与 SR-046/060 一致）
- operation：`空`
- outcome：`unknown`；不将 `op_action` 或告警记录机械映射为动作结果。
- 主体/客体/载体：访问用户（source.user+endpoint）/ 邮件服务器（target.endpoint）/ http（facets.http.request）
- 检测声明：`source_finding_obj`（title/severity/status/count/rule/file{url}）
- 文档证据：深信服防火墙 syslog 日志 8.0.50–8.0.95；样本字段已由 WPL 命中。

## 当前物理注册表迁移

- expected 已按当前 `sdm_event.yaml` 87 字段物理注册表收敛。
- 访问用户入 `roles.source.user+endpoint`；邮件服务器入 `roles.target.endpoint`。
- HTTP 请求入 `facets.http.request.host`；检测声明入 `source_finding_obj`（title/severity/status/count/rule/file）。
