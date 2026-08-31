# 360 / 360_active_defense_log 运行时观测候选映射

事件事实：终端主动防御（HIPS）检测——局域网攻击来源 198.51.100.44（attack_process）对受保护终端 TEST-PC-01（risk_ip 203.0.113.19）的检测。hips_type=2=文件防护。检测声明保存在 source_finding。

主体：`attack_endpoint`（source.endpoint=attack_ip + source.process）；客体：`protected_host`（target.host=computername + target.endpoint=risk_ip）；载体：`none`；观察者：来源产品。

> 状态：candidate，未注册、未批准。WPL 解析事实与 360 EPP 文档已确认；SR-043 人工复核结论见文末。

| WPL 字段 | 值 | SDM 候选路径 | 状态 |
|---|---|---|---|
| `asset_username` | `hsakdjklas#@$%阿利克水泥钉金卡三年` | `extensions_obj.source_private.asset_username` | `source_private` |
| `attack_ip` | `198.51.100.44` | `roles_obj.source.endpoint.ip` + `source_ip` | `confirmed` |
| `attack_mac` | `test-101-mac` | `roles_obj.source.endpoint.mac` | `confirmed` |
| `attack_machine` | `test-attack_machine` | `extensions_obj.source_private.attack_machine` | `source_private` |
| `attack_process` | `cat ~/.ssh/` | `roles_obj.source.process.name` | `confirmed` |
| `clientip` | `192.0.2.180` | `extensions_obj.source_private.clientip` | `source_private` |
| `computername` | `TEST-PC-01` | `roles_obj.target.host.name` | `confirmed` |
| `ctime` | `2026-01-23 11:00:00` | `occur_time` | `candidate` |
| `dst_process` | `test-dst_process` | `extensions_obj.source_private.dst_process` | `source_private` |
| `hips_desc` | `360文档保护已经开启` | `source_finding_obj.title` | `confirmed` |
| `hips_result_type` | `0` | `source_finding_obj.outcome`（0=其他）+ `original_outcome` | `confirmed` |
| `hips_subtype` | `2` | `extensions_obj.source_private.hips_subtype` | `source_private` |
| `hips_type` | `2` | `extensions_obj.source_private.hips_type` | `source_private` |
| `id` | `71` | `extensions_obj.source_private.id` | `source_private` |
| `intercept_time` | `2026-01-23 11:00:00` | `occur_time` | `candidate` |
| `is_xc` | `2` | `extensions_obj.source_private.is_xc` | `source_private` |
| `lan_type` | `0` | `extensions_obj.source_private.lan_type` | `source_private` |
| `type` | `active_defense_log` | `extensions_obj.source_private.type` | `source_private` |
| `m2` | `a17f1890bb3e71a61d8be6fe71d71b73fa02c41e2914` | `extensions_obj.source_private.m2` | `source_private` |
| `plat_id` | `1` | `extensions_obj.source_private.plat_id` | `source_private` |
| `record_tm` | `2026-01-23 11:00:00` | `extensions_obj.source_private.record_tm` | `source_private` |
| `risk_file` | `test-risk_file` | `extensions_obj.source_private.risk_file` | `source_private` |
| `risk_ip` | `203.0.113.19` | `roles_obj.target.endpoint.ip` + `target_ip` | `confirmed` |
| `risk_opt` | `test-risk_opt` | `extensions_obj.source_private.risk_opt` | `source_private` |
| `risk_url` | `http://localhost:9090` | `extensions_obj.source_private.risk_url` | `source_private` |
| `src_process` | `test-src_process` | `extensions_obj.source_private.src_process` | `source_private` |
| `src_process_md5` | `test-src_process_md5` | `extensions_obj.source_private.src_process_md5` | `source_private` |
| `sysmaclist` | `00:00:5E:00:53:F4` | `extensions_obj.source_private.sysmaclist` | `source_private` |
| `username` | `test-user` | `extensions_obj.source_private.username` | `source_private` |

## 人工语义复核（360 EPP，SR-043）

- 事件事实：终端主动防御日志记录风险来源、攻击进程和受保护终端。
- **hips_result_type 枚举已确认**：0=其他、1=已阻止、2=已允许、3=自动允许、4=自动阻止、5=未处理、6=已清除。本条 0=其他。
- **hips_type 枚举已确认**：0=HIPS防护、1=进程防护、2=文件防护、3=注册表防护、4=网络防护、5=DNS防护、6=局域网防护、7=驱动防护。本条 2=文件防护。
- `event_category=alert`，`event_type=network_connection`（局域网攻击来源语义，候选），`operation=empty`，`outcome=unknown`（hips_result_type=0=其他）。
- 主体/客体/载体：attack_endpoint / protected_host / none
- 检测声明：`source_finding_obj`（title/count/outcome/original_outcome）
- 文档证据：360《终端-EPP-SysLog文档》；当前 WPL 运行样本已命中。
- 未确认的数字枚举保留原值，未知值策略为 report。
