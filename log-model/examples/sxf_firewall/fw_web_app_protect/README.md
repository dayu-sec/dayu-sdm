# sxf_firewall / fw_web_app_protect SDM2 候选样例

事件事实：深信服防火墙 Web 应用防护（WEB应用防护日志）——攻击 192.0.2.11:7224 → 192.0.2.15:80（URL http://www.sangfor.com/waf.jsp）命中跨站请求伪造，op_action=允许，severity=低。

- 主体：攻击源 → `roles.source.endpoint(192.0.2.11:7224)`
- 客体：Web 服务器 → `roles.target.endpoint(192.0.2.15:80)` + `roles.target.domain(www.sangfor.com)`
- 载体：HTTP 请求 → `facets.http.request.host=www.sangfor.com`
- 检测声明：`source_finding_obj{title, severity=低, status=op_action, count, rule{name, label=policy_name, signature_id}}`
- 观察者：来源安全产品

## 证据与限制

- 原始样本：`log-model/examples/sxf_firewall/` 第 1 个非空行。
- WPL 规则：`fw_web_app_protect`，运行时解析成功。
- 字段映射和枚举为候选，未知枚举保留原值并报告。
- `outcome=unknown`；不将 `op_action`（允许）机械映射为动作结果（允许的跨站请求仍可能已执行）。
- 顶层 `severity` 为空；来源严重度=低 保留在 source_finding.severity，不机械投影。

## 人工语义复核（深信服防火墙文档，SR-073）

- 事件事实：深信服防火墙记录 Web 应用防护命中；告警严重度保留 source_finding。
- event_category：`alert`
- event_type：`network_http`
- operation：`空`
- outcome：`unknown`；不将 `op_action` 或告警记录机械映射为动作结果。
- 主体/客体/载体：攻击源（source.endpoint）/ Web 服务器（target.endpoint+domain）/ http（facets.http.request）
- 检测声明：`source_finding_obj`（title/severity/status/count/rule{name, label, signature_id}）
- 文档证据：深信服防火墙 syslog 日志 8.0.50–8.0.95；样本字段已由 WPL 命中。

## 当前物理注册表迁移

- expected 已按当前 `sdm_event.yaml` 87 字段物理注册表收敛。
- 攻击源入 `roles.source.endpoint`；Web 服务器入 `roles.target.endpoint+domain`。
- HTTP 请求入 `facets.http.request.host`；检测声明入 `source_finding_obj`（title/severity/status/count/rule）。
