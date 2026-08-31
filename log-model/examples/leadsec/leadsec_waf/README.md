# leadsec / leadsec_waf SDM2 候选样例

事件事实：WAF 跨站脚本攻击——HTTP 请求 203.0.113.206:3746 → 203.0.113.192:80（`/?yyy=zz%0aand%0dxxx=1`），action=丢弃。recorder=event（Web应用防护），eventname=跨站脚本攻击。

- 主体：HTTP 客户端端点 → `roles.source.endpoint(203.0.113.206:3746)`
- 客体：Web 服务器端点 → `roles.target.endpoint(203.0.113.192:80)`
- 载体：HTTP → `facets.network.protocol.code=TCP` + `facets.http.request{host, query}`
- 检测声明：`source_finding_obj{title, severity=中, status=丢弃, count, rule.name=WAF}`
- 观察者：来源安全产品

## 证据与限制

- 原始样本：`log-model/examples/leadsec/` 第 14 个非空行。
- WPL 规则：`leadsec_waf`，运行时解析成功。
- 字段映射和枚举为候选，未知枚举保留原值并报告。
- `outcome=denied`；action=丢弃与文档 drop 枚举共同支持拒绝处置。
- 顶层 `severity` 为空；来源 severity=中 保留在 source_finding.severity。

## 人工语义复核（Power-V 文档，SR-052）

- 事件事实：WAF 日志记录跨站脚本攻击，action=丢弃与文档 drop 枚举共同支持拒绝处置。
- event_category：`alert`
- event_type：`network_http`
- operation：`空`
- **outcome：`denied`**（action=丢弃=drop）
- 主体/客体/载体：http_client / web_server / http
- 检测声明：`source_finding_obj`（title/severity/status/count/rule.name=WAF）
- `pri` 仅映射 `log_level`；来源 severity 保留在 `source_finding`。
- 文档证据：Power-V 192.0.2.120 日志格式手册 VERSION 0.3.0；证据状态 `vendor_confirmed_and_observed`。

## 当前物理注册表迁移

- expected 已按当前 `sdm_event.yaml` 87 字段物理注册表收敛。
- HTTP 客户端/服务器端点入 `roles.source/target.endpoint`。
- 协议入 `facets.network.protocol`；HTTP 请求入 `facets.http.request`；检测声明入 `source_finding_obj`。
