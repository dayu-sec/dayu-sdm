# topas_ips / topas_ips_audit_file SDM2 候选样例

事件事实：文件审计（recorder=audit_file）——FTP 传输文件 04--csrss.exe（203.0.113.9:54454 → 198.51.100.249:54656，direction=s2c）。

- 主体：源端点 → `roles.source.endpoint(203.0.113.9:54454)`
- 客体：传输文件 → `roles.target.file{name=04--csrss.exe, size, extension=EXE, hashes.md5}` + `roles.target.endpoint(198.51.100.249:54656)`
- 载体：网络方向 → `facets.network.direction=s2c`；应用 → `facets.application.name=FTP`
- 观察者：来源安全产品

## 证据与限制

- 原始样本：`s4-doris/models/wpl/topas_ips/sample.dat` 第 3 个非空行。
- WPL 规则：`topas_ips_audit_file`，运行时解析成功。
- 字段映射和枚举为候选，未知枚举保留原值并报告。
- `outcome=unknown`；文件审计未提供明确动作结果。
- `source_finding_obj=null`：文件传输审计，非检测告警。

## 人工语义复核（TopIDP v3，SR-079）

- 事件事实：文件审计记录文件传输方向，但未提供明确动作结果。
- event_category：`network`
- event_type：`file_read`（文件传输方向）
- operation：`空`
- outcome：`unknown`
- 主体/客体/载体：源端点（source.endpoint）/ 传输文件（target.file+endpoint）/ application + network.direction
- 文件传输：`facets.application.name=FTP`；方向 `facets.network.direction=s2c`
- 文档证据：TopIDP 输出信息格式规范 v3；`recorder=audit_file`。

## 当前物理注册表迁移

- expected 已按当前 `sdm_event.yaml` 87 字段物理注册表收敛。
- 源端点入 `roles.source.endpoint`；传输文件入 `roles.target.file+endpoint`。
- 应用入 `facets.application.name`；方向入 `facets.network.direction`；source_finding_obj=null。
