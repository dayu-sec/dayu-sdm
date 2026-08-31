# leadsec / leadsec_vq SDM2 候选样例

事件事实：病毒隔离——SMTP 流量（198.51.100.188:4026 → 203.0.113.5:25）中隔离邮件文件 email_2012_2_26_3_23_14_483926.eml。recorder=vq（病毒隔离），eventtype=病毒隔离。

- 主体：源端点 → `roles.source.endpoint(198.51.100.188:4026)`
- 客体：被隔离邮件文件 → `roles.target.file{name=email_2012_2_26_3_23_14_483926.eml, extension=eml}`
- 载体：网络协议 → `facets.network.protocol.code=SMTP`；邮件附件 → `facets.email.attachments[].name`
- 检测声明：`source_finding_obj{title=eventname, count, action=quarantine}`
- 观察者：来源安全产品

## 证据与限制

- 原始样本：`s4-doris/models/wpl/leadsec/sample.dat` 第 15 个非空行。
- WPL 规则：`leadsec_vq`，运行时解析成功。
- 字段映射和枚举为候选，未知枚举保留原值并报告。
- `outcome=unknown`；样本没有独立结果字段，不机械映射。
- 顶层 `severity` 为空；来源严重度不机械投影。

## 人工语义复核（Power-V 文档，SR-051）

- 事件事实：病毒文件隔离日志明确记录隔离邮件文件；样本没有独立结果字段。
- event_category：`alert`
- **event_type：`generic_event`**（06 无病毒隔离类型；隔离是来源处置，非文件修改动作，与 SR-046 病毒检测一致）
- operation：`空`
- outcome：`unknown`（无独立结果字段）
- 主体/客体/载体：source_endpoint / quarantined_file / smtp
- 检测声明：`source_finding_obj`（title=eventname/count/action=quarantine）
- `pri` 仅映射 `log_level`。
- 文档证据：Power-V 192.0.2.120 日志格式手册 VERSION 0.3.0；证据状态 `vendor_confirmed_and_observed`。

## 当前物理注册表迁移

- expected 已按当前 `sdm_event.yaml` 87 字段物理注册表收敛。
- 源端点入 `roles.source.endpoint`；被隔离邮件文件入 `roles.target.file`。
- 协议入 `facets.network.protocol`；邮件附件入 `facets.email.attachments`；检测声明入 `source_finding_obj`。
