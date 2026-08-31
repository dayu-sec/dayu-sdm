# sxf_probe / flow_user_define SDM2 候选样例

事件事实：探针 SMB 连接（logtype=smb）——用户 anonymous（198.51.100.194:50877）访问 SMB 服务 192.0.2.211:445，command=6/status=0（字典未确认）。

- 主体：SMB 用户 → `roles.source.user{name=anonymous}` + `source.endpoint(198.51.100.194:50877)`
- 客体：SMB 服务 → `roles.target.endpoint(192.0.2.211:445)`
- 载体：网络协议 → `facets.network.protocol.code=TCP`；应用 → `facets.application.name=SMB`
- 观察者：来源安全产品

## 证据与限制

- 原始样本：`s4-doris/models/wpl/sxf_probe/sample.dat` 第 1 个非空行。
- WPL 规则：`flow_user_define_smb`，运行时解析成功。
- 字段映射和枚举为候选，未知枚举保留原值并报告。
- `outcome=unknown`；command=6/status=0 具体动作字典尚未确认。
- `source_finding_obj=null`：SMB 连接审计，非检测告警。

## 人工语义复核（深信服探针文档，SR-077）

- 事件事实：探针记录一次 SMB 连接；command=6/status=0 的具体动作字典尚未确认。
- event_category：`network`
- event_type：`network_connection`
- operation：`空`
- outcome：`unknown`（command/status 字典未确认）
- 主体/客体/载体：SMB 用户（source.user+endpoint）/ SMB 服务（target.endpoint）/ network_protocol + application
- command=6/status=0 无标准路径，保留 `extensions.source_private`
- 文档证据：深信服《潜伏威胁探针数据接口对外说明 V2.0》；运行样本已命中。
- 未确认的协议数字/命令字典保留原值并 report。

## 当前物理注册表迁移

- expected 已按当前 `sdm_event.yaml` 87 字段物理注册表收敛。
- SMB 用户入 `roles.source.user+endpoint`；SMB 服务入 `roles.target.endpoint`。
- 应用入 `facets.application.name=SMB`；协议入 `facets.network.protocol`；source_finding_obj=null。
