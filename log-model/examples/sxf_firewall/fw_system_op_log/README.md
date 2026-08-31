# sxf_firewall / fw_system_op_log SDM2 候选样例

事件事实：深信服防火墙系统操作日志——管理员 admin（198.51.100.54）启用 OSPF，op_type=启用，op_info=OSPF 启用 成功。

- 主体：管理员 → `roles.source.user{name=admin}` + `source.endpoint(198.51.100.54)`
- 客体：操作对象 → `roles.target.service{name=启用禁用}`
- 载体：无 → `carriers=[]`
- 观察者：来源安全产品

## 证据与限制

- 原始样本：`log-model/examples/sxf_firewall/` 第 12 个非空行。
- WPL 规则：`fw_system_op_log`，运行时解析成功。
- 字段映射和枚举为候选，未知枚举保留原值并报告。
- **`outcome=success`**；op_info=OSPF 启用 成功明确操作结果。
- 顶层 `severity` 为空；来源严重度不机械投影。

## 人工语义复核（深信服防火墙文档，SR-071）

- 事件事实：深信服防火墙记录管理员系统操作；具体动作语义保留来源字段。
- event_category：`audit`
- event_type：`status_update`（启用 OSPF 状态变更）
- operation：`空`
- **outcome：`success`**（op_info=OSPF 启用 成功明确操作结果，同 SR-070）
- 主体/客体/载体：管理员（source.user+endpoint）/ 操作对象（target.service）/ none
- 文档证据：深信服防火墙 syslog 日志 8.0.50–8.0.95；样本字段已由 WPL 命中。

## 当前物理注册表迁移

- expected 已按当前 `sdm_event.yaml` 87 字段物理注册表收敛。
- 管理员入 `roles.source.user+endpoint`；操作对象入 `roles.target.service`。
- `source_finding_obj=null`（系统操作审计，非检测）。
