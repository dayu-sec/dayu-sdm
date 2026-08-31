# sxf_edr / sip_atk_alarm_log SDM2 候选样例

事件事实：深信服 SIP 攻击告警（口令暴力破解/Telnet 账号爆破）——攻击源（attack_ip=0.0.0.0 占位）对受害资产 Asset1（suffer_ip=198.51.100.25:58669）发起攻击，命中自定义威胁情报（IOC=www.61house.com），severity=important。

- 主体：攻击源 → `roles.source.endpoint(0.0.0.0)`（attack_ip 占位，真实攻击 IP 未知）
- 客体：受害资产 → `roles.target.host{name=suffer_branch_name=Asset1, ip=suffer_ip=198.51.100.25}` + `roles.target.endpoint(198.51.100.25:58669)`
- 载体：无 → `carriers=[]`
- 检测声明：`source_finding_obj{title=brief, severity=emergency, count, rule{name=sub_attack_type_name, label=module_type_name}}`
- 观察者：来源安全产品

## 证据与限制

- 原始样本：`log-model/examples/sxf_edr/` 第 8 个非空行。
- WPL 规则：`sip_atk_alarm_log`，运行时解析成功。
- 字段映射和枚举为候选，未知枚举保留原值并报告。
- `outcome=unknown`；攻击告警无已确认的动作结果。
- 顶层 `severity` 为空；emergency=important 保留在 source_finding.severity，不机械投影。
- `attack_ip=0.0.0.0` 为占位值（真实攻击 IP 未知，IOC 为域名），roles.source.endpoint 仅作候选。

## 人工语义复核（深信服 SIP 文档，SR-061）

- 事件事实：深信服 SIP 记录攻击告警，攻击源与受害资产支持网络连接观察。
- event_category：`alert`
- event_type：`network_connection`
- operation：`空`
- outcome：`unknown`
- 主体/客体/载体：攻击源（source.endpoint）/ 受害资产（target.host+endpoint）/ none
- 检测声明：`source_finding_obj`（title/severity/count/rule）
- 来源告警等级保留在 `source_finding`，不机械投影顶层 severity。
- 文档证据：深信服 SIP syslog 格式说明 77 版本；WPL 样本已命中。

## 当前物理注册表迁移

- expected 已按当前 `sdm_event.yaml` 87 字段物理注册表收敛。
- 攻击源入 `roles.source.endpoint`；受害资产入 `roles.target.host+endpoint`。
- 攻击结论入 `source_finding_obj`（title/severity/count/rule）。
