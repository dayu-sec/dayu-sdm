# sxf_firewall / fw_antivirus_virus 运行时观测候选映射

事件事实：深信服防火墙病毒查杀（病毒查杀日志）——用户 donnie 访问邮件 URL 检出 Backdoor.RmtBomb.2，op_action=拒绝。检测声明在 source_finding。

主体：访问用户（source.user=user_name + source.endpoint=sip）；客体：邮件服务器（target.endpoint=dip）；载体：`http`（facets.http.request）；观察者：来源产品。

> 状态：candidate，未注册、未批准。WPL 解析事实与深信服防火墙文档已确认；SR-064 人工复核结论见文末。

| WPL 字段 | 值 | SDM 候选路径 | 状态 |
|---|---|---|---|
| `time` | `2026-01-23 11:00:00` | `extensions_obj.source_private.time` | `source_private` |
| `domain` | `localhost` | `extensions_obj.source_private.domain` | `source_private` |
| `type` | `fwlog` | `extensions_obj.source_private.type` | `source_private` |
| `symbol` | `日志类型:病毒查杀` | `extensions_obj.source_private.symbol` | `source_private` |
| `logtype` | `病毒查杀` | `extensions_obj.source_private.logtype` | `source_private` |
| `policy_name` | `virus22` | `extensions_obj.source_private.policy_name` | `source_private` |
| `user_name` | `donnie` | `roles_obj.source.user.name` | `confirmed` |
| `sip` | `192.0.2.84` | `roles_obj.source.endpoint.ip` + `source_ip` | `confirmed` |
| `sport` | `8271` | `roles_obj.source.endpoint.port` | `confirmed` |
| `dip` | `954f:2588:3600::` | `roles_obj.target.endpoint.ip` + `target_ip` | `confirmed` |
| `dport` | `110` | `roles_obj.target.endpoint.port` | `confirmed` |
| `virus_type` | `4160744368` | `extensions_obj.source_private.virus_type` | `source_private` |
| `virus_name` | `Backdoor.RmtBomb.2` | `source_finding_obj.title` | `confirmed` |
| `app_name` | `邮件` | `extensions_obj.source_private.app_name` | `source_private` |
| `severity` | `高` | `source_finding_obj.severity` | `confirmed` |
| `op_action` | `拒绝` | `source_finding_obj.status`（来源处置，不映射 outcome） | `confirmed` |
| `url` | `http://192.0.2.200/repro/adobe_pdf_embedded_exe_nojs.pdf` | `source_finding_obj.file.url` + `facets_obj.http.request.host` | `confirmed` |

## 人工语义复核（SXF Firewall，SR-064）

- 事件事实：深信服防火墙记录上传/文件病毒检测；来源处置不等同底层 outcome。
- `event_category=alert`
- **`event_type=generic_event`**（06 无病毒查杀类型；不是 file_read，与 SR-046/060 一致）
- `operation=empty`
- `outcome=unknown`；不将 `op_action` 或告警记录机械映射为动作结果。
- 主体/客体/载体：访问用户（source.user+endpoint）/ 邮件服务器（target.endpoint）/ http（facets.http.request）
- 检测声明：`source_finding_obj`（title/severity/status/count/rule/file{url}）
- 文档证据：深信服防火墙 syslog 日志 8.0.50–8.0.95；样本字段已由 WPL 命中。
