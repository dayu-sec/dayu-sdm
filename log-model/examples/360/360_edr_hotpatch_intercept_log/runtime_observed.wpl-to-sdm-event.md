# 360 / 360_edr_hotpatch_intercept_log 运行时观测候选映射

事件事实：EDR 热补丁拦截远程代码执行攻击（recorder=360edr_hotpatch_intercept_log）——203.0.113.202:36938 -> 192.0.2.125:8080，action=阻断。检测声明保存在 source_finding。

主体：`source_endpoint`（src_ip/src_port）；客体：`protected_endpoint`（dst_ip/dst_port）；载体：`network_protocol`（facets.network.protocol=tcp）；观察者：来源产品。

> 状态：candidate，未注册、未批准。WPL 解析事实与 360 EPP 文档已确认；SR-044 人工复核结论见文末。

| WPL 字段 | 值 | SDM 候选路径 | 状态 |
|---|---|---|---|
| `action` | `阻断` | `source_finding_obj.action`（blocked）+ `outcome=denied` | `confirmed` |
| `action_time` | `01/23/26-11:00:00.000000` | `extensions_obj.source_private.action_time` | `source_private` |
| `clientip` | `203.0.113.37` | `extensions_obj.source_private.clientip` | `source_private` |
| `computername` | `kevintest的Mac` | `extensions_obj.source_private.computername` | `source_private` |
| `ctime` | `2026-01-23 11:00:00` | `occur_time` | `candidate` |
| `cve_id` | `test-cve_id` | `extensions_obj.source_private.cve_id` | `source_private` |
| `dst_ip` | `192.0.2.125` | `roles_obj.target.endpoint.ip` + `target_ip` | `confirmed` |
| `dst_port` | `8080` | `roles_obj.target.endpoint.port` | `confirmed` |
| `handle_result` | `0` | `extensions_obj.source_private.handle_result` | `source_private` |
| `id` | `14` | `extensions_obj.source_private.id` | `source_private` |
| `type` | `360edr_hotpatch_intercept_log` | `extensions_obj.source_private.type` | `source_private` |
| `m2` | `e56c345a91c17c571900b5c913da87229b14bf21059b` | `extensions_obj.source_private.m2` | `source_private` |
| `mtime` | `2026-01-23 11:00:00` | `extensions_obj.source_private.mtime` | `source_private` |
| `patchod` | `test-patchod` | `extensions_obj.source_private.patchod` | `source_private` |
| `process_id` | `test-process_id` | `extensions_obj.source_private.process_id` | `source_private` |
| `process_name` | `test-process_name` | `extensions_obj.source_private.process_name` | `source_private` |
| `process_path` | `process_path` | `extensions_obj.source_private.process_path` | `source_private` |
| `protocol` | `tcp` | `facets_obj.network.protocol.code` | `confirmed` |
| `rule_id` | `1000014` | `source_finding_obj.rule.signature_id` | `confirmed` |
| `rule_name` | `ApacheStruts2远程代码执行漏洞攻击(S2_057)` | `source_finding_obj.rule.name` | `confirmed` |
| `rule_version` | `01` | `extensions_obj.source_private.rule_version` | `source_private` |
| `src_ip` | `203.0.113.202` | `roles_obj.source.endpoint.ip` + `source_ip` | `confirmed` |
| `src_port` | `36938` | `roles_obj.source.endpoint.port` | `confirmed` |
| `sysmaclist` | `00:00:5E:00:53:78` | `extensions_obj.source_private.sysmaclist` | `source_private` |
| `threat_level` | `高危` | `extensions_obj.source_private.threat_level` | `source_private` |
| `threat_name` | `ApacheStruts2远程代码执行漏洞攻击(S2_057)` | `extensions_obj.source_private.threat_name` | `source_private` |
| `threat_type` | `远程代码执行` | `extensions_obj.source_private.threat_type` | `source_private` |
| `username` | `root` | `extensions_obj.source_private.username` | `source_private` |

## 人工语义复核（360 EPP，SR-044）

- 事件事实：EDR 热补丁日志明确记录远程代码执行攻击被阻断。
- `event_category=alert`，`event_type=network_connection`，`operation=empty`，`outcome=denied`（action=阻断）。
- 主体/客体/载体：source_endpoint / protected_endpoint / network_protocol
- 检测声明：`source_finding_obj`（title/severity=高危/count/action/rule）
- 文档证据：360《终端-EPP-SysLog文档》；当前 WPL 运行样本已命中。
- 未确认的数字枚举保留原值，未知值策略为 report。
