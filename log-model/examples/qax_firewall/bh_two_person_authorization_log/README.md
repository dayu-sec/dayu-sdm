# qax_firewall / bh_two_person_authorization_log SDM2 候选样例

事件事实：堡垒机双人授权（logType=YAB_DBL_AUTH_LOG）——用户 abc（192.xxx.xxx.20）申请访问目标资源「主机 1」(192.xxx.xxx.40)，审批人 admin 参与审批。

- 主体：申请用户 → `roles.source.user{name=abc}` + `source.endpoint(192.xxx.xxx.20)`
- 客体：目标资源 → `roles.target.host{name=主机 1, ip=192.xxx.xxx.40}`
- 审批人 → `roles.related[].user{name=admin}`（approver）
- 载体：无 → `carriers=[]`
- 观察者：来源安全产品

## 证据与限制

- 原始样本：`log-model/examples/qax_firewall/` 第 5 个非空行。
- WPL 规则：`bh_two_person_authorization_log`，运行时解析成功。
- 字段映射和枚举为候选，未知枚举保留原值并报告。
- `outcome=unknown`；授权流程未证明实际登录或持续权限变更。
- 顶层 `severity` 为空；来源严重度不机械投影。

## 人工语义复核（KB47750，SR-058）

- 事件事实：堡垒机记录用户访问目标资源前发起的双人授权流程，由管理员参与审批；日志未证明实际登录或持续权限变更。
- event_category：`auth`
- event_type：`user_login`（授权 preauth 流程）
- operation：`preauth`
- outcome：`unknown`（未证明实际登录）
- 主体/客体/载体：source_user / target_device_or_resource / none
- 审批人：`roles.related[].user{name=approver}`
- 证据：奇安信堡垒机 192.0.2.70 Syslog 格式说明 KB47750；对应 `logType` 为 `YAB_DBL_AUTH_LOG`。
- 状态：`reviewed_candidate`

## 当前物理注册表迁移

- expected 已按当前 `sdm_event.yaml` 87 字段物理注册表收敛。
- 申请用户入 `roles.source.user+endpoint`；目标资源入 `roles.target.host`；审批人入 `roles.related[].user`。
