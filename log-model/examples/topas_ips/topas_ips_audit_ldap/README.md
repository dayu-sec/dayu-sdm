# topas_ips / topas_ips_audit_ldap SDM2 候选样例

事件事实：LDAP 协议审计——用户 user1 连接 LDAP 服务（192.0.2.54:389，协议版本 3）。recorder=audit_ldap；未提供认证结果。

- 主体：LDAP 用户 → `roles.source.user{name=user1}`；来源端点 → `roles.source.endpoint(203.0.113.205:36587)`
- 客体：LDAP 服务 → `roles.target.service{name=192.0.2.54, port=389}`
- 载体：网络协议 → `facets.network.protocol.code=proto`；应用 → `facets.application.name=ldap`
- 观察者：来源安全产品

## 证据与限制

- 原始样本：`log-model/examples/topas_ips/` 第 7 个非空行。
- WPL 规则：`topas_ips_audit_ldap`，运行时解析成功。
- 字段映射和枚举为候选，未知枚举保留原值并报告。
- `outcome=unknown`；LDAP 审计无认证结果字段，不机械映射。
- 顶层 `severity` 为空；来源严重度不机械投影。

## 人工语义复核（TopIDP v3，SR-039）

- 事件事实：LDAP 协议审计活动记录，非检测告警。
- event_category：`audit`
- event_type：`generic_event`（06 无 LDAP 审计专用类型）
- operation：`空`
- outcome：`unknown`（无认证结果字段）
- 主体/客体/载体：ldap_user（source.user） / ldap_service（target.service） / network_protocol（facets.network）
- 应用类型：`facets.application.name=ldap`
- 证据：TopIDP v3 §3.5.13 LDAP 审计，`recorder=audit_ldap`；WPL 运行样本已命中。

## 当前物理注册表迁移

- expected 已按当前 `sdm_event.yaml` 87 字段物理注册表收敛。
- 热字段 `source_ip/target_ip` 保留标量投影；完整端点/用户对象在 `roles_obj`。
- 协议与应用类型入 `facets_obj`（registry 已注册路径）。
