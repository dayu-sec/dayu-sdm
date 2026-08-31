# qax_firewall / bh_session_share_log SDM2 候选样例

事件事实：堡垒机会话协同（logType=YAB_SESSION_SHARE_LOG）——用户 admin（192.xxx.xxx.20）将会话分享给 testUser，记录加入/退出时间。

- 主体：分享用户 → `roles.source.user{name=shareUser=admin}` + `source.endpoint(sourceIp)`
- 客体：协同用户 → `roles.target.user{name=user=testUser}`
- 载体：无 → `carriers=[]`
- 观察者：来源安全产品

## 证据与限制

- 原始样本：`log-model/examples/qax_firewall/` 第 11 个非空行。
- WPL 规则：`bh_session_share_log`，运行时解析成功。
- 字段映射和枚举为候选，未知枚举保留原值并报告。
- `outcome=unknown`；会话协同无动作结果字段。
- 顶层 `severity` 为空；来源严重度不机械投影。

## 人工语义复核（KB47750，SR-056）

- 事件事实：堡垒机用户发起会话协同并记录协同用户加入/退出时间。
- event_category：`audit`
- event_type：`user_resource_update_permissions`（会话分享=权限授予）
- operation：`share`
- outcome：`unknown`
- 主体/客体/载体：user（source.user=shareUser）/ collaborating_user（target.user=user）/ none
- 加入/退出时间（joinTime/exitTime）无标准路径，保留 source_private
- 证据：奇安信堡垒机 192.0.2.70 Syslog 格式说明 KB47750；对应 `logType` 为 `YAB_SESSION_SHARE_LOG`。
- 状态：`reviewed_candidate`

## 当前物理注册表迁移

- expected 已按当前 `sdm_event.yaml` 87 字段物理注册表收敛。
- 分享用户入 `roles.source.user+endpoint`；协同用户入 `roles.target.user`。
- 加入/退出时间保留在 `extensions.source_private`（无标准路径）。
