# leadsec / leadsec_ips SDM2 候选样例

事件事实：IPS 入侵防护——攻击 203.0.113.206:56085 → 203.0.113.219:80（protocol=TCP），事件 UserDefine sina_alert，action=drop=丢弃。recorder=ips。

- 主体：攻击源端点 → `roles.source.endpoint(203.0.113.206:56085)`
- 客体：被攻击端点 → `roles.target.endpoint(203.0.113.219:80)`
- 载体：网络协议 → `facets.network.protocol.code=TCP`
- 检测声明：`source_finding_obj{title, severity=1, status=drop, count, rule{name, label}}`
- 观察者：来源安全产品

## 证据与限制

- 原始样本：`log-model/examples/leadsec/` 第 1 个非空行。
- WPL 规则：`leadsec_ips`，运行时解析成功。
- 字段映射和枚举为候选，未知枚举保留原值并报告。
- `outcome=denied`；action=drop=丢弃，明确记录攻击被阻断。
- 顶层 `severity` 为空；`pri` 仅映射 `log_level`；来源 severity=1 保留在 source_finding.severity。

## 人工语义复核（Power-V 文档，SR-049）

- 事件事实：入侵防护日志记录从源到目标的攻击检测，action=drop 的文档枚举含义为丢弃。
- event_category：`alert`
- event_type：`network_connection`
- operation：`空`
- **outcome：`denied`**（action=drop=丢弃）
- 主体/客体/载体：source_endpoint / target_endpoint / network_protocol
- 检测声明：`source_finding_obj`（title/severity/status/count/rule）
- `pri` 仅映射 `log_level`；来源 severity 保留在 `source_finding`。
- 文档证据：Power-V 192.0.2.120 日志格式手册 VERSION 0.3.0；证据状态 `vendor_confirmed_and_observed`。

## 当前物理注册表迁移

- expected 已按当前 `sdm_event.yaml` 87 字段物理注册表收敛。
- 攻击源/目标端点入 `roles.source/target.endpoint`。
- 协议入 `facets.network.protocol`；检测声明入 `source_finding_obj`。
