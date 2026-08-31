# topas_ips / topas_ips_audit_nfs SDM2 候选样例

事件事实：NFS 审计（recorder=audit_nfs）——NFS 文件读取操作 SecureCRTPortable.exe（198.51.100.34:781 → 198.51.100.253:2049，nfs_op=read，deal_size=file_size=68836）。

- 主体：源端点 → `roles.source.endpoint(198.51.100.34:781)`
- 客体：读取文件 → `roles.target.file{name=SecureCRTPortable.exe, size=68836}` + `target.endpoint(198.51.100.253:2049)`
- 载体：应用 → `facets.application.name=NFS`
- 观察者：来源安全产品

## 证据与限制

- 原始样本：`log-model/examples/topas_ips/` 第 5 个非空行。
- WPL 规则：`topas_ips_audit_nfs`，运行时解析成功。
- 字段映射和枚举为候选，未知枚举保留原值并报告。
- `outcome=unknown`；result=0 数字字典未由 TopIDP 文档确认，不机械映射为成功。
- `source_finding_obj=null`：NFS 传输审计，非检测告警。

## 人工语义复核（TopIDP v3，SR-081）

- 事件事实：NFS nfs_op=read，支持文件读取活动候选；result 数字字典待确认。
- event_category：`network`
- event_type：`file_read`
- operation：`extended`
- outcome：`unknown`（result=0 字典未确认）
- 主体/客体/载体：源端点（source.endpoint）/ 读取文件（target.file+endpoint）/ application(NFS)
- NFS 应用：`facets.application.name=NFS`
- 文档证据：TopIDP 输出信息格式规范 v3；`recorder=audit_nfs`。

## 当前物理注册表迁移

- expected 已按当前 `sdm_event.yaml` 87 字段物理注册表收敛。
- 源端点入 `roles.source.endpoint`；读取文件入 `roles.target.file+endpoint`。
- 应用入 `facets.application.name`；result/operation 数字保留 source_private；source_finding_obj=null。
