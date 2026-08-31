# topas_waf / topas_waf_tamper 运行时观测候选映射

事件事实：WAF 网页防篡改检测（recorder=waf_tamper，event=1）——受保护站点 test 的 /config 文件被删除。检测声明保存在 source_finding。

主体：`none`（防篡改检测无主动主体）；客体：`protected_web_resource`（target.host + target.file）；载体：`none`；观察者：来源产品。

> 状态：candidate，未注册、未批准。WPL 解析事实与 waf2.0 文档 TABLE 4 已确认；SR-042 人工复核结论见文末。

| WPL 字段 | 值 | SDM 候选路径 | 状态 |
|---|---|---|---|
| `id` | `ngtos` | `event_id` | `candidate` |
| `version` | `2.1` | `extensions_obj.source_private.version` | `source_private` |
| `hiredate` | `2026-01-23 11:00:00` | `occur_time` | `candidate` |
| `dev` | `TopsecOS` | `extensions_obj.source_private.dev` | `source_private` |
| `pri` | `warning` | `extensions_obj.source_private.pri` | `source_private` |
| `type` | `waf` | `extensions_obj.source_private.type` | `source_private` |
| `recorder` | `waf_tamper` | `extensions_obj.source_private.recorder` | `source_private` |
| `vsid` | `0` | `extensions_obj.source_private.vsid` | `source_private` |
| `event` | `1` | `source_finding_obj.action`（1=文件删除） | `confirmed` |
| `domain` | `test` | `source_finding_obj.rule.label` + `roles_obj.target.host.name` | `confirmed` |
| `ip` | `198.51.100.54` | `roles_obj.target.host.ip` | `confirmed` |
| `filename` | `/config` | `roles_obj.target.file.path` | `confirmed` |

## 人工语义复核（TopWAF 2.x，SR-042）

- 事件事实：WAF 记录受保护站点文件的网页防篡改检测事件。
- **event 枚举已确认**：waf 文档 TABLE 4 `event` 1=文件删除、2=文件添加、4=文件篡改、9=文件删除|恢复、12=文件篡改|恢复、16=签名错误、18=文件添加|签名错误。本条 event=1=文件删除。
- `event_category=alert`
- `event_type=generic_event`（06 无网页防篡改专用类型；file_deletion 候选待评估）
- `operation=empty`
- `outcome=unknown`：不将来源处置或 HTTP 状态机械映射为底层动作结果。
- `log_level=warning`：仅来自 `pri`，不作为安全严重度。
- 主体/客体/载体：none / protected_web_resource（target.host + target.file）/ none
- 检测声明：`source_finding_obj`（title/count/action=file_delete/rule.label=domain）
- 文档证据：天融信《waf2.0日志格式文档-v2.0》TABLE 4；`recorder=waf_tamper`，WPL 运行样本已命中。
