# topas_ips / topas_ips_attack SDM2 候选样例

事件事实：IPS 攻击检测——源 203.0.113.143:53490 向目标 198.51.100.109:80 发起 HTTP POST（rule 95000 命中，recorder=attack）。检测声明保存在 source_finding；op/result 是来源处置，不是已确认的底层动作结果。

- 主体：发起攻击的源端点 → `roles.source.endpoint`（sip/sport）
- 客体：被攻击的目标端点 → `roles.target.endpoint`（dip/dport）
- 载体：网络协议 → `facets.network.protocol{code=proto}` + `direction=c2s`；carriers 不构造实体
- 观察者：来源安全产品

## 证据与限制

- 原始样本：`log-model/examples/topas_ips/` 第 1 个非空行。
- WPL 规则：`topas_ips_attack`，运行时解析成功。
- 字段映射和枚举为候选，未知枚举保留原值并报告。
- `outcome=unknown`；没有把 finding 或日志存在机械映射为 observed。
- 顶层 `severity` 为空；来源严重度不机械投影。

## 人工语义复核（TopIDP v3，SR-037）

- 事件事实：攻击检测日志是来源发现；op/result 不是已确认的底层动作结果。
- event_category：`alert`
- event_type：`generic_event`（06 无攻击检测专用类型，检测事实已在 source_finding）
- operation：`空`
- outcome：`unknown`
- 主体/客体/载体：source_endpoint / target_endpoint / network_protocol（facets.network）
- 检测声明：`source_finding_obj{original_id=sid, title, count=repeat, rule{signature_id=sid, label=rule}}`
- 证据：TopIDP 输出信息格式规范 v3，`recorder=attack`；WPL 运行样本已命中。

## 当前物理注册表迁移

- expected 已按当前 `sdm_event.yaml` 87 字段物理注册表收敛。
- 热字段 `source_ip/target_ip` 保留标量投影；完整端点对象在 `roles_obj`。
- 协议与方向入 `facets_obj.network`（registry 已注册路径）。
