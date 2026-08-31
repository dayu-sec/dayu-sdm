# topas_ips / topas_ips_audit_rdp SDM2 候选样例

事件事实：RDP 协议审计——用户 liuludan 连接远程主机（198.51.100.199:3389）。recorder=audit_rdp；未提供认证结果。

- 主体：RDP 用户 → `roles.source.user{name=liuludan}`；来源端点 → `roles.source.endpoint(192.0.2.122:47410)`
- 客体：被远程主机 → `roles.target.host{name/ip=198.51.100.199}`
- 载体：网络协议 → `facets.network.protocol.code=proto`；应用 → `facets.application.name=rdp`
- 观察者：来源安全产品

## 证据与限制

- 原始样本：`log-model/examples/topas_ips/` 第 8 个非空行。
- WPL 规则：`topas_ips_audit_rdp`，运行时解析成功。
- 字段映射和枚举为候选，未知枚举保留原值并报告。
- `outcome=unknown`；RDP 审计无认证结果字段，不机械映射。
- 顶层 `severity` 为空；来源严重度不机械投影。

## 人工语义复核（TopIDP v3，SR-040）

- 事件事实：RDP 协议审计活动记录，非检测告警。
- event_category：`audit`
- event_type：`generic_event`（06 无 RDP 审计专用类型）
- operation：`空`
- outcome：`unknown`（无认证结果字段）
- 主体/客体/载体：rdp_user（source.user） / rdp_host（target.host） / network_protocol（facets.network）
- 应用类型：`facets.application.name=rdp`
- 证据：TopIDP v3 §3.5.14 RDP 审计，`recorder=audit_rdp`；WPL 运行样本已命中。

## 当前物理注册表迁移

- expected 已按当前 `sdm_event.yaml` 87 字段物理注册表收敛。
- 热字段 `source_ip/target_ip` 保留标量投影；完整端点/用户/主机对象在 `roles_obj`。
- 协议与应用类型入 `facets_obj`（registry 已注册路径）。
- `dport=3389` 无 `roles.target.host.port` 路径，保留原值在 source_private（registry 无 host.port）。
