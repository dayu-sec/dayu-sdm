# sxf_firewall / fw_user_auth_log SDM2 候选样例

事件事实：深信服防火墙用户认证日志——用户 192.0.2.131（192.0.2.131）注销，op_object=注销，登录时长 1569 秒。

- 主体：认证用户 → `roles.source.user{name=192.0.2.131}` + `source.endpoint(192.0.2.131)`
- 客体：无 → `roles.target=null`
- 载体：无 → `carriers=[]`
- 观察者：来源安全产品

## 证据与限制

- 原始样本：`log-model/examples/sxf_firewall/` 第 13 个非空行。
- WPL 规则：`fw_user_auth_log`，运行时解析成功。
- 字段映射和枚举为候选，未知枚举保留原值并报告。
- `outcome=unknown`；认证/注销结果字段未提供。
- 顶层 `severity` 为空；来源严重度不机械投影。

## 人工语义复核（深信服防火墙文档，SR-072）

- 事件事实：深信服防火墙记录用户认证/注销事件；结果字段未提供。
- event_category：`auth`
- **event_type：`user_logout`**（op_object=注销；原 user_login+logon 是登录语义，本样例为注销事件）
- operation：`空`
- outcome：`unknown`（结果字段未提供）
- 主体/客体/载体：认证用户（source.user+endpoint）/ none / none
- 文档证据：深信服防火墙 syslog 日志 8.0.50–8.0.95；样本字段已由 WPL 命中。

## 当前物理注册表迁移

- expected 已按当前 `sdm_event.yaml` 87 字段物理注册表收敛。
- 认证用户入 `roles.source.user+endpoint`。
- `source_finding_obj=null`（认证/注销活动，非检测）。
