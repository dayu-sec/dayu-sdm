# topas_ips / topas_ips_audit_ftp SDM2 候选样例

事件事实：FTP 审计（recorder=audit_ftp）——用户 anonymous 通过 RETR 从 FTP 服务器（203.0.113.9:21）下载文件 04--csrss.exe，ret_code=226（Transfer complete，成功）。

- 主体：FTP 用户 → `roles.source.user{name=anonymous}` + `source.endpoint(198.51.100.249:54588)`
- 客体：下载文件 → `roles.target.file{name=04--csrss.exe}` + `target.endpoint(203.0.113.9:21)`
- 载体：应用 → `facets.application.name=FTP`
- 观察者：来源安全产品

## 证据与限制

- 原始样本：`log-model/examples/topas_ips/` 第 4 个非空行。
- WPL 规则：`topas_ips_audit_ftp`，运行时解析成功。
- 字段映射和枚举为候选，未知枚举保留原值并报告。
- `outcome=success`；ret_code=226（Transfer complete）为 FTP 明确成功完成码，明确 RETR 下载成功。
- `source_finding_obj=null`：FTP 传输审计，非检测告警。

## 人工语义复核（TopIDP v3，SR-080）

- 事件事实：FTP RETR 且 ret_code=226（Transfer complete），文件读取成功。
- event_category：`network`
- event_type：`file_read`
- operation：`download`
- outcome：`success`（ret_code=226）
- 主体/客体/载体：FTP 用户（source.user+endpoint）/ 下载文件（target.file+endpoint）/ application(FTP)
- 文档证据：TopIDP 输出信息格式规范 v3；`recorder=audit_ftp`。

## 当前物理注册表迁移

- expected 已按当前 `sdm_event.yaml` 87 字段物理注册表收敛。
- FTP 用户入 `roles.source.user+endpoint`；下载文件入 `roles.target.file+endpoint`。
- 应用入 `facets.application.name`；ret_code=226 进 source_private（作为结果来源处置）；source_finding_obj=null。
