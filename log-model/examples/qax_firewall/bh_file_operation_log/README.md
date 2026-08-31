# qax_firewall / bh_file_operation_log SDM2 候选样例

事件事实：堡垒机命令操作（logType=YAB_CMD_OPS_LOG）——用户 admin 对目标资源「主机1」(192.xxx.xxx.40) 执行命令 ls，action=disconnect（断开连接）。

- 主体：堡垒机用户 → `roles.source.user{name=admin}` + `source.endpoint(192.xxx.xxx.20)`
- 客体：目标资源主机 → `roles.target.host{name=主机1, ip=192.xxx.xxx.40}`
- 载体：无 → `carriers=[]`
- 观察者：来源安全产品

## 证据与限制

- 原始样本：`s4-doris/models/wpl/qax_firewall/sample.dat` 第 3 个非空行。
- WPL 规则：`bh_file_operation_log`，运行时解析成功。
- 字段映射和枚举为候选，未知枚举保留原值并报告。
- `outcome=unknown`；action=disconnect 是会话断开，非命令执行结果。
- 顶层 `severity` 为空；来源严重度不机械投影。
- **目录名 `bh_file_operation_log` 与 logType=`YAB_CMD_OPS_LOG`（命令操作）不符**，与 SR-006 同类；不改目录名。

## 人工语义复核（KB47750，SR-053）

- 事件事实：堡垒机用户对目标资源执行命令操作（logType=YAB_CMD_OPS_LOG）。
- event_category：`audit`
- **event_type：`generic_event`**（命令执行无标准类型；user_resource_update_content 暗示内容更新不贴切，command=ls 是查看命令）
- operation：`空`（无充分标准动作证据）
- outcome：`unknown`
- 主体/客体/载体：source_user / target_resource（target.host）/ none
- `command=ls`、`action=disconnect`（断开连接）
- 证据：奇安信堡垒机 KB47750 §2.3 命令操作日志；对应 `logType` 为 `YAB_CMD_OPS_LOG`。
- 状态：`reviewed_candidate`

## 当前物理注册表迁移

- expected 已按当前 `sdm_event.yaml` 87 字段物理注册表收敛。
- 堡垒机用户入 `roles.source.user+endpoint`；目标资源入 `roles.target.host`。
- 命令/action 保留在 source_private（无标准路径）。
