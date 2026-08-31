# sxf_firewall / fw_website_access SDM2 候选样例

事件事实：深信服防火墙网站访问（网站访问日志）——源 203.0.113.113 访问 URL http://www.shenxinfu.com/simple.php（IT相关），op_action=被记录。

- 主体：访问源 → `roles.source.endpoint(203.0.113.113)`
- 客体：Web 目标 → `roles.target.endpoint(203.0.113.118)` + `roles.target.domain(www.shenxinfu.com)`
- 载体：HTTP + 应用 → `facets.http.request.host` + `facets.application.name=IT相关`
- 观察者：来源安全产品

## 证据与限制

- 原始样本：`s4-doris/models/wpl/sxf_firewall/sample.dat` 第 10 个非空行。
- WPL 规则：`fw_website_access`，运行时解析成功。
- 字段映射和枚举为候选，未知枚举保留原值并报告。
- `outcome=unknown`；op_action=被记录是审计动作，非结果。
- `source_finding_obj=null`：Web 访问审计，非检测告警。

## 人工语义复核（深信服防火墙文档，SR-075）

- 事件事实：深信服防火墙记录源端访问 Web 资源。
- event_category：`network`
- event_type：`network_http`
- operation：`空`
- outcome：`unknown`；不将 `op_action`（被记录）机械映射为动作结果。
- 主体/客体/载体：访问源（source.endpoint）/ Web 目标（target.endpoint+domain）/ http + application
- 文档证据：深信服防火墙 syslog 日志 8.0.50–8.0.95；样本字段已由 WPL 命中。

## 当前物理注册表迁移

- expected 已按当前 `sdm_event.yaml` 87 字段物理注册表收敛。
- 访问源入 `roles.source.endpoint`；Web 目标入 `roles.target.endpoint+domain`。
- HTTP 请求入 `facets.http.request.host`；应用入 `facets.application.name`；source_finding_obj=null。
