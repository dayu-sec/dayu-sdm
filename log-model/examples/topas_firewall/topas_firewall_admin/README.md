# topas_firewall / topas_firewall_admin SDM2 候选样例

事件事实：防火墙管理员日志——用户 superman 通过串口（Serial）本地登录防火墙（TopsecOS，127.0.0.1），result=success，login success。

- 主体：管理员 → `roles.source.user{name=superman}` + `source.endpoint(127.0.0.1)`
- 客体：防火墙设备 → `roles.target.host{name=TopsecOS}`
- 载体：认证方式 → `facets.authentication.auth_type=Serial`
- 观察者：来源安全产品

## 证据与限制

- 原始样本：`log-model/examples/topas_firewall/` 第 1 个非空行。
- WPL 规则：`topas_firewall_admin`，运行时解析成功。
- 字段映射和枚举为候选，未知枚举保留原值并报告。
- `outcome=success`；result=success 明确登录成功。
- `pri=6` 仅进入 `log_level`。

## 人工语义复核（天融信防火墙文档，SR-078）

- 事件事实：防火墙管理员日志记录通过串口本地登录，result=success。
- event_category：`auth`
- event_type：`user_login`
- operation：`interactive`（本地串口登录）
- outcome：`success`（result=success）
- 主体/客体/载体：管理员（source.user+endpoint）/ 防火墙设备（target.host）/ authentication（facets.authentication.auth_type=Serial）
- `pri` 仅进入 `log_level`。
- 文档证据：天融信《防火墙日志规范 v23.2》对应 admin/ac 章节。

## 当前物理注册表迁移

- expected 已按当前 `sdm_event.yaml` 87 字段物理注册表收敛。
- 管理员入 `roles.source.user+endpoint`；防火墙设备入 `roles.target.host`。
- 认证方式入 `facets.authentication.auth_type`；source_finding_obj=null（登录活动）。
