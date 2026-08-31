# 360 / 360_gtmaphenixdb_dlp_outfile_audit_log 运行时观测候选映射

事件事实：DLP 外发审计（recorder=gtmaphenixdb.dlp_outfile_audit_log）——用户 test-user 外发 syslog.zip 命中规则「手动添加1」，deal_type=1=阻止。审计声明在 source_finding。

主体：`endpoint_user`（source.user=cmp_loginuser）；客体：`outbound_file`（target.file=audit_filename/file_path）；载体：`none`；观察者：来源产品。

> 状态：candidate，未注册、未批准。WPL 解析事实与 360 EPP 文档已确认；SR-047 人工复核结论见文末。

| WPL 字段 | 值 | SDM 候选路径 | 状态 |
|---|---|---|---|
| `asset_username` | `hsakdjklas#@$%阿利克水泥钉金卡三年` | `extensions_obj.source_private.asset_username` | `source_private` |
| `audit_filename` | `syslog.zip` | `roles_obj.target.file.name` | `confirmed` |
| `client_name` | `TEST-PC-01` | `extensions_obj.source_private.client_name` | `source_private` |
| `clientip` | `203.0.113.37` | `extensions_obj.source_private.clientip` | `source_private` |
| `cmp_loginuser` | `test-user` | `roles_obj.source.user.name` | `confirmed` |
| `computername` | `TEST-PC-01` | `extensions_obj.source_private.computername` | `source_private` |
| `create_time` | `2026-01-23 11:00:00` | `extensions_obj.source_private.create_time` | `source_private` |
| `deal_type` | `1` | `outcome`（1=阻止 -> denied） | `confirmed` |
| `download_file` | `test-download_file` | `extensions_obj.source_private.download_file` | `source_private` |
| `download_flag` | `0` | `extensions_obj.source_private.download_flag` | `source_private` |
| `download_string` | `test-download_string` | `extensions_obj.source_private.download_string` | `source_private` |
| `file_path` | `test-file_path` | `roles_obj.target.file.path` | `confirmed` |
| `group_id` | `21` | `extensions_obj.source_private.group_id` | `source_private` |
| `group_name` | `qsl` | `extensions_obj.source_private.group_name` | `source_private` |
| `id` | `2` | `extensions_obj.source_private.id` | `source_private` |
| `ip` | `198.51.100.241` | `extensions_obj.source_private.ip` | `source_private` |
| `type` | `gtmaphenixdb.dlp_outfile_audit_log` | `extensions_obj.source_private.type` | `source_private` |
| `m2` | `a17f1890bb3e71a61d8be6fe71d71b73fa02c41e2914` | `extensions_obj.source_private.m2` | `source_private` |
| `opartion_details` | `[{\"detailcontextone\":\"syslog\",\"detailcontexttwo\":\"\",\"detailhitcount\":\"出现1次\",\"detailrule\":\"手动添加1\",\"detailtype\":\"关键字匹配\"}]` | `extensions_obj.source_private.opartion_details` | `source_private` |
| `opartion_detailsshow` | `[{\"showcontext\":\"syslog\",\"showrule\":\"手动添加1\",\"showtype\":\"关键字匹配\"}]` | `extensions_obj.source_private.opartion_detailsshow` | `source_private` |
| `operate_result` | `1` | `source_finding_obj.status`（1=未发送） | `confirmed` |
| `platform_id` | `1` | `extensions_obj.source_private.platform_id` | `source_private` |
| `platform_type` | `Windows` | `extensions_obj.source_private.platform_type` | `source_private` |
| `regular_name` | `手动添加1` | `source_finding_obj.rule.label` | `confirmed` |
| `scan_time` | `1769137200` | `extensions_obj.source_private.scan_time` | `source_private` |
| `secret_name` | `内部` | `extensions_obj.source_private.secret_name` | `source_private` |
| `send_time` | `2026-01-23 11:00:00` | `extensions_obj.source_private.send_time` | `source_private` |
| `username` | `q` | `extensions_obj.source_private.username` | `source_private` |

## 人工语义复核（360 EPP，SR-047）

- 事件事实：DLP 外发审计记录文件外发及规则命中。
- **deal_type 枚举已确认**：0=审计、1=阻止、2=用户确认。本条 1=阻止。
- **operate_result 枚举已确认**：0=已发送、1=未发送。本条 1=未发送。
- `event_category=audit`，`event_type=file_copy`，`operation=empty`
- **`outcome=denied`**（deal_type=1=阻止 + operate_result=1=未发送）
- 主体/客体/载体：endpoint_user / outbound_file / none
- 审计声明：`source_finding_obj`（title/count/rule.label=regular_name）
- 文档证据：360《终端-EPP-SysLog文档》；当前 WPL 运行样本已命中。
- 未确认的数字枚举保留原值，未知值策略为 report。
