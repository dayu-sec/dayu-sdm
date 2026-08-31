# topas_ips / topas_ips_audit_db SDM2 候选样例

事件事实：数据库审计——数据库用户 db2admin 对 DB2 库 SAMPLE（198.51.100.16:50000）执行 SQL 查询（`select current schema from sysibm.sysdummy1`），响应码 NP01F。recorder=audit_db。

- 主体：数据库用户 → `roles.source.user{name=db2admin}`；来源端点 → `roles.source.endpoint(192.0.2.104:49686)`
- 客体：数据库服务 → `roles.target.service{name=SAMPLE, port=50000}`
- 载体：网络协议 → `facets.network.protocol.code=proto`；数据库类型 → `facets.application.name=db2`
- 观察者：来源安全产品

## 证据与限制

- 原始样本：`log-model/examples/topas_ips/` 第 9 个非空行。
- WPL 规则：`topas_ips_audit_db`，运行时解析成功。
- 字段映射和枚举为候选，未知枚举保留原值并报告。
- `outcome=unknown`；retcode=NP01F 语义未确认，不机械映射。
- 顶层 `severity` 为空；来源严重度不机械投影。

## 人工语义复核（TopIDP v3，SR-038）

- 事件事实：数据库审计活动记录，非检测告警。
- event_category：`audit`
- event_type：`generic_event`（06 无数据库查询专用类型）
- operation：`空`
- outcome：`unknown`（retcode=NP01F 未确认）
- 主体/客体/载体：database_user（source.user） / database_service（target.service） / network_protocol（facets.network）
- 数据库类型：`facets.application.name=db2`
- **模型缺口**：registry 无 `facets.database` / `roles.target.database` 路径；SQL 事实（command/dbname/retcode/retmsg）在 `extensions.unmapped` 待扩展，未伪装成稳定 source_private 契约。
- 证据：TopIDP v3 §3.5.15 数据库审计，`recorder=audit_db`；WPL 运行样本已命中。

## 当前物理注册表迁移

- expected 已按当前 `sdm_event.yaml` 87 字段物理注册表收敛。
- 热字段 `source_ip/target_ip` 保留标量投影；完整端点/用户对象在 `roles_obj`。
- 协议与数据库类型入 `facets_obj`（registry 已注册路径）。
