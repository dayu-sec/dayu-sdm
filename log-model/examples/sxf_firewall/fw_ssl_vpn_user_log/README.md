# sxf_firewall / fw_ssl_vpn_user_log SDM2 候选样例

事件事实：深信服防火墙 SSL VPN 用户行为日志——用户 wjj（198.51.100.109）登录 SSL VPN，op_type=登录，op_info=登录成功。

- 主体：VPN 用户 → `roles.source.user{name=wjj}` + `source.endpoint(198.51.100.109)`
- 客体：SSL VPN 服务 → `roles.target.service{name=SSL VPN}`
- 载体：无 → `carriers=[]`
- 观察者：来源安全产品

## 证据与限制

- 原始样本：`log-model/examples/sxf_firewall/` 第 18 个非空行。
- WPL 规则：`fw_ssl_vpn_user_log`，运行时解析成功。
- 字段映射和枚举为候选，未知枚举保留原值并报告。
- **`outcome=success`**；op_info=登录成功明确认证结果。
- 顶层 `severity` 为空；来源严重度不机械投影。

## 人工语义复核（深信服防火墙文档，SR-070）

- 事件事实：深信服防火墙记录 SSL VPN 用户操作/登录相关事件。
- event_category：`auth`
- event_type：`user_login`
- operation：`remote_service`
- **outcome：`success`**（op_info=登录成功明确认证结果；区别于 SR-055 未提供结果的 unknown）
- 主体/客体/载体：VPN 用户（source.user+endpoint）/ SSL VPN 服务（target.service）/ none
- 文档证据：深信服防火墙 syslog 日志 8.0.50–8.0.95；样本字段已由 WPL 命中。

## 当前物理注册表迁移

- expected 已按当前 `sdm_event.yaml` 87 字段物理注册表收敛。
- VPN 用户入 `roles.source.user+endpoint`；SSL VPN 服务入 `roles.target.service`。
- `source_finding_obj=null`（登录活动，非检测）。
