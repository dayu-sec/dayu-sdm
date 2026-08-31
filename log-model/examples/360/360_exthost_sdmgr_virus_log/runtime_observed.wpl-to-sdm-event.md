# 360 / 360_exthost_sdmgr_virus_log 运行时观测候选映射

事件事实：终端病毒检测（recorder=360exthost_360sdmgr_virus_log）——检出 Trojan.Win32.Emotet.BE，handle_result=未处理。检测声明保存在 source_finding。

主体：`endpoint_host`（source.host=computername）；客体：`malware_file`（target.file=file_path/md5）；载体：`none`；观察者：来源产品。

> 状态：candidate，未注册、未批准。WPL 解析事实与 360 EPP 文档已确认；SR-046 人工复核结论见文末。

| WPL 字段 | 值 | SDM 候选路径 | 状态 |
|---|---|---|---|
| `asset_username` | `hsakdjklas使用人` | `extensions_obj.source_private.asset_username` | `source_private` |
| `clientip` | `203.0.113.37` | `extensions_obj.source_private.clientip` | `source_private` |
| `computername` | `TEST-PC-01` | `roles_obj.source.host.name` | `confirmed` |
| `content_type` | `1` | `extensions_obj.source_private.content_type` | `source_private` |
| `ctime` | `2026-01-23 11:00:00` | `occur_time` | `candidate` |
| `file_create_time` | `2026-01-23 11:00:00` | `extensions_obj.source_private.file_create_time` | `source_private` |
| `file_modify_time` | `2026-01-23 11:00:00` | `extensions_obj.source_private.file_modify_time` | `source_private` |
| `file_path` | `C:\\Users\\test-user\\Desktop\\FD样本\\FD样本\\Trojan..Win32.Emotet.BE\\787B03FEB0BD3BBF3BE3F5AEDDF8C64D` | `roles_obj.target.file.path` | `confirmed` |
| `found_time` | `2026-01-23 11:00:00` | `occur_time` | `candidate` |
| `handle_mode` | `manual` | `extensions_obj.source_private.handle_mode` | `source_private` |
| `handle_result` | `未处理的病毒` | `source_finding_obj.status` | `confirmed` |
| `handle_result_detail` | `未处理的病毒` | `extensions_obj.source_private.handle_result_detail` | `source_private` |
| `handle_time` | `2026-01-23 11:00:00` | `extensions_obj.source_private.handle_time` | `source_private` |
| `hit_layer` | `0` | `extensions_obj.source_private.hit_layer` | `source_private` |
| `id` | `1980` | `extensions_obj.source_private.id` | `source_private` |
| `inactivity` | `test-inactivity` | `extensions_obj.source_private.inactivity` | `source_private` |
| `is_xc` | `2` | `extensions_obj.source_private.is_xc` | `source_private` |
| `type` | `360exthost_360sdmgr_virus_log` | `extensions_obj.source_private.type` | `source_private` |
| `ltime` | `2026-01-23 11:00:00` | `extensions_obj.source_private.ltime` | `source_private` |
| `m2` | `a17f1890bb3e71a61d8be6fe71d71b73fa02c41e2914` | `extensions_obj.source_private.m2` | `source_private` |
| `md5` | `787b03feb0bd3bbf3be3f5aeddf8c64d` | `roles_obj.target.file.hashes.md5` | `confirmed` |
| `mtime` | `2026-01-23 11:00:00` | `extensions_obj.source_private.mtime` | `source_private` |
| `plat_id` | `1` | `extensions_obj.source_private.plat_id` | `source_private` |
| `scan_id` | `test-scan_id` | `extensions_obj.source_private.scan_id` | `source_private` |
| `scan_mode` | `18` | `extensions_obj.source_private.scan_mode` | `source_private` |
| `sysmaclist` | `00:00:5E:00:53:F4` | `extensions_obj.source_private.sysmaclist` | `source_private` |
| `trigger_type` | `2` | `extensions_obj.source_private.trigger_type` | `source_private` |
| `username` | `test-user` | `extensions_obj.source_private.username` | `source_private` |
| `virus_id` | `100` | `source_finding_obj.rule.label` | `confirmed` |
| `virus_name` | `Trojan.Win32.Emotet.BE` | `source_finding_obj.title` | `confirmed` |
| `virus_type` | `其它` | `extensions_obj.source_private.virus_type` | `source_private` |

## 人工语义复核（360 EPP，SR-046）

- 事件事实：终端病毒日志记录 Emotet 文件检测；样本明确为未处理，不代表底层文件动作结果。
- `event_category=alert`
- **`event_type=generic_event`**（06 无恶意软件检出类型；不是 file_read——检测事件无文件读取证据，与 SR-041 病毒样例一致）
- `operation=empty`
- `outcome=unknown`（handle_result=未处理的病毒）
- 主体/客体/载体：endpoint_host / malware_file / none
- 检测声明：`source_finding_obj`（title=virus_name/status=handle_result/count/rule）
- 文档证据：360《终端-EPP-SysLog文档》；当前 WPL 运行样本已命中。
- 未确认的数字枚举保留原值，未知值策略为 report。
