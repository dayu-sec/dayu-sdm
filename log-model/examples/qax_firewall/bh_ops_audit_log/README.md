# qax_firewall / bh_ops_audit_log SDM2 候选样例

事件事实：堡垒机系统性能运行状态快照（logType=YAB_SYSTEM_STATUS_LOG）——cpu=5.06%、mem=61.84%、read=56681500、write=940099000。

- 主体：无（状态快照，非活动/检测）
- 客体：堡垒机自身 → `roles.target.host{name=堡垒机, id=prod_id}`
- 载体：无 → `carriers=[]`
- 观察者：来源安全产品

## 证据与限制

- 原始样本：`s4-doris/models/wpl/qax_firewall/sample.dat` 第 8 个非空行。
- WPL 规则：`bh_ops_audit_log`，运行时解析成功。
- 字段映射和枚举为候选，未知枚举保留原值并报告。
- `outcome=unknown`；状态快照无动作结果。
- 顶层 `severity` 为空；来源严重度不机械投影。

## 人工语义复核（KB47750，SR-054）

- 事件事实：堡垒机记录系统性能运行状态快照。
- event_category：`system`
- event_type：`status_update`
- operation：`空；无充分标准动作证据`
- outcome：`unknown`
- 主体/客体/载体：none / bastion_host（target.host）/ none
- 性能指标（cpu/mem/read/write）无标准路径，保留 `extensions.source_private`（受治理容器）
- 证据：奇安信堡垒机 192.0.2.70 Syslog 格式说明 KB47750；对应 `logType` 为 `YAB_SYSTEM_STATUS_LOG`。
- 状态：`reviewed_candidate`

## 当前物理注册表迁移

- expected 已按当前 `sdm_event.yaml` 87 字段物理注册表收敛。
- 堡垒机自身入 `roles.target.host{name, id=prod_id}`。
- 性能指标保留在 `extensions.source_private`（无标准路径）。
