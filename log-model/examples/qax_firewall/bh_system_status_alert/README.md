# qax_firewall / bh_system_status_alert SDM2 候选样例

事件事实：堡垒机系统性能阈值告警（logType=YAB_SYSTEM_ALARM_LOG）——CPU 使用率超过 50%（alarmModule=系统性能，alarmLevel=低），告警消息「CPU使用率超过50%」。

- 主体：无（系统阈值告警，非用户操作）
- 客体：堡垒机自身 → `roles.target.host{name=堡垒机, id=prod_id}`
- 载体：无 → `carriers=[]`
- 观察者：来源安全产品

## 证据与限制

- 原始样本：`log-model/examples/qax_firewall/` 第 9 个非空行。
- WPL 规则：`bh_system_status_alert`，运行时解析成功。
- 字段映射和枚举为候选，未知枚举保留原值并报告。
- `outcome=unknown`；阈值告警无动作结果。
- 顶层 `severity` 为空；alarmLevel=低 仅保留来源私有，不映射 SDM severity。

## 人工语义复核（KB47750，SR-057）

- 事件事实：堡垒机生成系统性能阈值告警；alarmLevel 仅保留来源私有，不直接映射 SDM severity。
- event_category：`system`
- event_type：`status_update`
- operation：`空；无充分标准动作证据`
- outcome：`unknown`
- 主体/客体/载体：none / bastion_host（target.host）/ none
- 告警内容（alarmMsg/alarmModule/systemHardType/threshold/alarmLevel）无标准路径，保留 `extensions.source_private`
- 证据：奇安信堡垒机 192.0.2.70 Syslog 格式说明 KB47750；对应 `logType` 为 `YAB_SYSTEM_ALARM_LOG`。
- 状态：`reviewed_candidate`

## 当前物理注册表迁移

- expected 已按当前 `sdm_event.yaml` 87 字段物理注册表收敛。
- 堡垒机自身入 `roles.target.host{name, id=prod_id}`。
- 告警内容保留在 `extensions.source_private`（无标准路径）。
