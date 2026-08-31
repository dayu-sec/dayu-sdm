# qax_firewall / bh_resource_login_log SDM2 候选样例

事件事实：堡垒机资源登录（logType=YAB_RESOURCE_LOGIN_LOG）——用户 admin（192.xxx.xxx.20）通过 SSH 登录目标资源「主机 1」(192.xxx.xxx.40) 的 root 账户。

- 主体：堡垒机用户 → `roles.source.user{name=admin}` + `source.endpoint(192.xxx.xxx.20)`
- 客体：目标资源 → `roles.target.host{name=主机 1, ip=192.xxx.xxx.40}` + `target.account{name=root}`
- 载体：SSH 认证 → `facets.authentication.auth_type=SSH`
- 观察者：来源安全产品

## 证据与限制

- 原始样本：`s4-doris/models/wpl/qax_firewall/sample.dat` 第 2 个非空行。
- WPL 规则：`bh_resource_login_log`，运行时解析成功。
- 字段映射和枚举为候选，未知枚举保留原值并报告。
- `outcome=unknown`；样本未提供登录结果字段。
- 顶层 `severity` 为空；来源严重度不机械投影。

## 人工语义复核（KB47750，SR-055）

- 事件事实：堡垒机用户发起到目标资源的 SSH 等资源登录；样本未提供结果。
- event_category：`auth`
- event_type：`user_login`
- operation：`remote_service`
- outcome：`unknown`（未提供结果）
- 主体/客体/载体：source_user / target_device_or_resource（target.host+account）/ none
- 认证方式：`facets.authentication.auth_type=SSH`
- 证据：奇安信堡垒机 192.0.2.70 Syslog 格式说明 KB47750；对应 `logType` 为 `YAB_RESOURCE_LOGIN_LOG`。
- 状态：`reviewed_candidate`

## 当前物理注册表迁移

- expected 已按当前 `sdm_event.yaml` 87 字段物理注册表收敛。
- 堡垒机用户入 `roles.source.user+endpoint`；目标资源入 `roles.target.host+account`。
- 认证方式入 `facets.authentication.auth_type`。
