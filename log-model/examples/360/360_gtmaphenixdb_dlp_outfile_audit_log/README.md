# 360 / 360_gtmaphenixdb_dlp_outfile_audit_log SDM2 候选样例

事件事实：DLP 外发审计——用户 test-user（TEST-PC-01）外发文件 syslog.zip 命中关键字规则「手动添加1」（secret_name=内部），deal_type=1=阻止、operate_result=1=未发送。

- 主体：外发用户 → `roles.source.user{name=cmp_loginuser=test-user}`
- 客体：外发文件 → `roles.target.file{name=audit_filename=syslog.zip, path=file_path}`
- 载体：无 → `carriers=[]`
- 检测/审计声明：`source_finding_obj{title, count, rule.label=regular_name}`
- 观察者：来源安全产品

## 证据与限制

- 原始样本：`log-model/examples/360/` 第 7 个非空行。
- WPL 规则：`360_gtmaphenixdb_dlp_outfile_audit_log`，运行时解析成功。
- 字段映射和枚举为候选，未知枚举保留原值并报告。
- `outcome=denied`；deal_type=1=阻止、operate_result=1=未发送。
- 顶层 `severity` 为空；来源严重度不机械投影。

## 人工语义复核（360 EPP 文档，SR-047）

- 事件事实：DLP 外发审计记录文件外发及规则命中。
- **deal_type 枚举已确认**：0=审计、1=阻止、2=用户确认。本条 1=阻止。
- **operate_result 枚举已确认**：0=已发送、1=未发送。本条 1=未发送。
- event_category：`audit`
- event_type：`file_copy`（文件外发复制语义）
- operation：`空`
- **outcome：`denied`**（deal_type=1=阻止 + operate_result=1=未发送）
- 主体/客体/载体：endpoint_user / outbound_file / none
- 审计声明：`source_finding_obj`（title/count/rule.label=regular_name）
- 文档证据：360《终端-EPP-SysLog文档》；当前 WPL 运行样本已命中。

## 当前物理注册表迁移

- expected 已按当前 `sdm_event.yaml` 87 字段物理注册表收敛。
- 外发用户入 `roles.source.user`；外发文件入 `roles.target.file`。
- 审计声明入 `source_finding_obj`（title/count/rule.label）。
