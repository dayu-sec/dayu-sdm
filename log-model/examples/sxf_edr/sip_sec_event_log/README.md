# sxf_edr / sip_sec_event_log SDM2 候选样例

事件事实：深信服 SIP 安全事件（secevent）——主机 Asset1（198.51.100.25）访问 Petya 勒索病毒通信域名，命中安全日志分析引擎（tag=[Petya,勒索病毒]），emergency=emergent。

- 主体：受感染主机 → `roles.source.host{name=Asset1, ip=198.51.100.25}`
- 客体：Petya C2 域名（无字段值，保留在 source_finding）→ `roles.target=null`
- 载体：无 → `carriers=[]`
- 检测声明：`source_finding_obj{title=brief, severity=emergency, count, rule{name=sub_attack_name}}`
- 观察者：来源安全产品

## 证据与限制

- 原始样本：`s4-doris/models/wpl/sxf_edr/sample.dat` 第 9 个非空行。
- WPL 规则：`sip_sec_event_log`，运行时解析成功。
- 字段映射和枚举为候选，未知枚举保留原值并报告。
- `outcome=unknown`；具体底层动作未由样本确认。
- 顶层 `severity` 为空；emergency=emergent 保留在 source_finding.severity，不机械投影。

## 人工语义复核（深信服 SIP 文档，SR-062）

- 事件事实：深信服 SIP 记录安全事件，具体底层动作未由样本确认。
- event_category：`alert`
- event_type：`network_connection`（主机访问恶意域名语义）
- operation：`空`
- outcome：`unknown`（底层动作未确认）
- 主体/客体/载体：受感染主机（source.host）/ Petya C2（source_finding，target=null）/ none
- 检测声明：`source_finding_obj`（title/severity/count/rule）
- 来源告警等级保留在 `source_finding`，不机械投影顶层 severity。
- 文档证据：深信服 SIP syslog 格式说明 77 版本；WPL 样本已命中。

## 当前物理注册表迁移

- expected 已按当前 `sdm_event.yaml` 87 字段物理注册表收敛。
- 受感染主机入 `roles.source.host`。
- 攻击结论入 `source_finding_obj`（title/severity/count/rule）。
