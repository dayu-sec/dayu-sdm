# sxf_firewall / fw_nat_log SDM2 候选样例

事件事实：深信服防火墙 NAT 转换（NAT日志，snat）——源 192.0.2.44:52977 经 NAT 转换为 192.0.2.193:52977 访问目标 198.51.100.97:53（协议 17）。

- 主体：转换前源 → `roles.source.endpoint(192.0.2.44:52977)`
- 客体：目标 → `roles.target.endpoint(198.51.100.97:53)`
- 载体：NAT 转换 → `facets.network.nat{original.ip, translated.ip}` + `facets.network.protocol.code=17`
- 观察者：来源安全产品

## 证据与限制

- 原始样本：`log-model/examples/sxf_firewall/` 第 14 个非空行。
- WPL 规则：`fw_nat_log`，运行时解析成功。
- 字段映射和枚举为候选，未知枚举保留原值并报告。
- `outcome=unknown`；NAT 转换无动作结果。
- `source_finding_obj=null`：NAT 转换审计，非检测告警。

## 人工语义复核（深信服防火墙文档，SR-069）

- 事件事实：深信服防火墙记录 NAT 前后地址/端口转换关联。
- event_category：`network`
- event_type：`network_connection`
- operation：`空`
- outcome：`unknown`
- 主体/客体/载体：转换前源（source.endpoint）/ 目标（target.endpoint）/ network_protocol + nat（facets.network.nat）
- NAT 转换：`facets.network.nat{original.ip=192.0.2.44, translated.ip=192.0.2.193}`
- NAT 端口（转换前后）无标准路径，保留 source_private
- 文档证据：深信服防火墙 syslog 日志 8.0.50–8.0.95；样本字段已由 WPL 命中。

## 当前物理注册表迁移

- expected 已按当前 `sdm_event.yaml` 87 字段物理注册表收敛。
- 转换前源/目标入 `roles.source/target.endpoint`。
- NAT 转换入 `facets.network.nat{original, translated}`；协议入 `facets.network.protocol`；source_finding_obj=null。
