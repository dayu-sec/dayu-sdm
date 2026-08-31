# topas_ips / topas_ips_audit_smb SDM2 候选样例

事件事实：SMB 审计（recorder=audit_smb）——用户 topsec（主机 10232-SSG，198.51.100.201:51247）向 SMB 服务器（192.0.2.1:445）写入文件 CVE__2013-4123__CVE 2013-4123 __1.1.181.233.pcap（smb_cmd=write，deal_size=file_size=3691）。

- 主体：SMB 用户 → `roles.source.user{name=topsec}` + `source.host{name=10232-SSG}` + `source.endpoint(198.51.100.201:51247)`
- 客体：写入文件 → `roles.target.file{name=CVE__2013-4123…pcap, size=3691}` + `target.endpoint(192.0.2.1:445)`
- 载体：应用 → `facets.application.name=SMB`
- 观察者：来源安全产品

## 证据与限制

- 原始样本：`log-model/examples/topas_ips/` 第 6 个非空行。
- WPL 规则：`topas_ips_audit_smb`，运行时解析成功。
- 字段映射和枚举为候选，未知枚举保留原值并报告。
- `outcome=unknown`；result=0 数字字典未由 TopIDP 文档确认，不机械映射为成功。
- `source_finding_obj=null`：SMB 传输审计，非检测告警。

## 人工语义复核（TopIDP v3，SR-082）

- 事件事实：SMB smb_cmd=write，支持文件写入活动候选；result 数字字典待确认。
- event_category：`network`
- event_type：`file_modification`
- operation：`write`
- outcome：`unknown`（result=0 字典未确认）
- 主体/客体/载体：SMB 用户（source.user+host+endpoint）/ 写入文件（target.file+endpoint）/ application(SMB)
- SMB 应用：`facets.application.name=SMB`
- 文档证据：TopIDP 输出信息格式规范 v3；`recorder=audit_smb`。

## 当前物理注册表迁移

- expected 已按当前 `sdm_event.yaml` 87 字段物理注册表收敛。
- SMB 用户入 `roles.source.user+host+endpoint`；写入文件入 `roles.target.file+endpoint`。
- 应用入 `facets.application.name`；result/operation 数字保留 source_private；source_finding_obj=null。
