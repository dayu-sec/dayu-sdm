# sxf_edr / cs_attack_alert_log SDM2 候选样例

事件事实：深信服 SIP 终端攻击告警（EDR adv_threat_log）——主机 WIN-EX03（203.0.113.70）上 powershell.exe 访问 lemonduck 挖矿通信域名，alert_level=4，attck_id=TA0011.T1071.004。

- 主体：受攻击终端 → `roles.source.host{name=WIN-EX03, ip=203.0.113.70}` + `roles.source.process(powershell.exe)`
- 客体：挖矿 C2 域名（无明确值，保留在 source_finding）→ `roles.target=null`
- 载体：无 → `carriers=[]`
- 检测声明：`source_finding_obj{title=alert_describe, severity=alert_level, count, rule{name, attck_id}}`
- 观察者：来源安全产品

## 证据与限制

- 原始样本：`log-model/examples/sxf_edr/` 第 2 个非空行。
- WPL 规则：`cs_attack_alert_log/adv_threat_log`，运行时解析成功。
- 字段映射和枚举为候选，未知枚举保留原值并报告。
- `outcome=unknown`；攻击告警无已确认的动作结果。
- 顶层 `severity` 为空；alert_level=4 保留在 source_finding.severity，不机械投影。

## 人工语义复核（深信服 SIP 文档，SR-059）

- 事件事实：深信服 SIP 记录终端攻击告警，攻击结论保留 source_finding。
- event_category：`alert`
- event_type：`network_connection`（挖矿域名通信语义）
- operation：`空`
- outcome：`unknown`
- 主体/客体/载体：受攻击终端（source.host+process）/ 挖矿 C2（source_finding，target=null）/ none
- 检测声明：`source_finding_obj`（title/severity/count/rule{name, attck_id}）
- 来源告警等级保留在 `source_finding`，不机械投影顶层 severity。
- 文档证据：深信服 SIP syslog 格式说明 77 版本；WPL 样本已命中。

## 当前物理注册表迁移

- expected 已按当前 `sdm_event.yaml` 87 字段物理注册表收敛。
- 受攻击终端入 `roles.source.host+process`。
- 挖矿攻击结论入 `source_finding_obj`（title/severity/count/rule{name, attck_id}）。
