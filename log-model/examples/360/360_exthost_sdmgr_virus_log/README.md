# 360 / 360_exthost_sdmgr_virus_log SDM2 候选样例

事件事实：终端病毒检测——检出 Trojan.Win32.Emotet.BE（md5=787b03feb0bd3bbf3be3f5aeddf8c64d），路径 `C:\Users\qiushilong\Desktop\FD样本\...`，handle_result=未处理的病毒，handle_mode=manual。

- 主体：受感染终端 → `roles.source.host{name=qiushilong-PC}`
- 客体：恶意文件 → `roles.target.file{path, name, hashes.md5}`
- 载体：无 → `carriers=[]`
- 检测声明：`source_finding_obj{title=virus_name, status=handle_result, count, rule{name, label=virus_id}}`
- 观察者：来源安全产品

## 证据与限制

- 原始样本：`s4-doris/models/wpl/360/sample.dat` 第 4 个非空行。
- WPL 规则：`360_exthost_sdmgr_virus_log`，运行时解析成功。
- 字段映射和枚举为候选，未知枚举保留原值并报告。
- `outcome=unknown`；handle_result=未处理的病毒，不代表底层文件动作结果。
- 顶层 `severity` 为空；来源严重度不机械投影。

## 人工语义复核（360 EPP 文档，SR-046）

- 事件事实：终端病毒日志记录 Emotet 文件检测；样本明确为未处理，不代表底层文件动作结果。
- event_category：`alert`
- **event_type：`generic_event`**（06 无恶意软件检出类型；不是 file_read——检测事件无文件读取证据，与 SR-041 病毒样例一致）
- operation：`空`
- outcome：`unknown`（handle_result=未处理的病毒）
- 主体/客体/载体：endpoint_host / malware_file / none
- 检测声明：`source_finding_obj`（title/status/count/rule）
- 文档证据：360《终端-EPP-SysLog文档》；当前 WPL 运行样本已命中。

## 当前物理注册表迁移

- expected 已按当前 `sdm_event.yaml` 87 字段物理注册表收敛。
- 受感染终端入 `roles.source.host`；恶意文件入 `roles.target.file`。
- 检测声明入 `source_finding_obj`（title/status/count/rule）。
