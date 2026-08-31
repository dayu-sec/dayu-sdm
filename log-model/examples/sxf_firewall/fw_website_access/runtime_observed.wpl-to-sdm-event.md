# sxf_firewall / fw_website_access 运行时观测候选映射

事件事实：深信服防火墙网站访问（网站访问日志）——源 203.0.113.113 访问 URL http://www.shenxinfu.com/simple.php（IT相关），op_action=被记录。

主体：访问源（source.endpoint=sip）；客体：Web 目标（target.endpoint=dip + target.domain=url）；载体：`http` + `application`（facets）；观察者：来源产品。

> 状态：candidate，未注册、未批准。WPL 解析事实与深信服防火墙文档已确认；SR-075 人工复核结论见文末。

| WPL 字段 | 值 | SDM 候选路径 | 状态 |
|---|---|---|---|
| `time` | `2026-01-23 11:00:00` | `extensions_obj.source_private.time` | `source_private` |
| `domain` | `localhost` | `extensions_obj.source_private.domain` | `source_private` |
| `type` | `fwlog` | `extensions_obj.source_private.type` | `source_private` |
| `symbol` | `日志类型:网站访问` | `extensions_obj.source_private.symbol` | `source_private` |
| `logtype` | `网站访问` | `extensions_obj.source_private.logtype` | `source_private` |
| `policy_name` | `web_access` | `extensions_obj.source_private.policy_name` | `source_private` |
| `user_name` | `(null)` | `source_user` | `candidate` |
| `sip` | `203.0.113.113` | `roles_obj.source.endpoint.ip` + `source_ip` | `confirmed` |
| `dip` | `203.0.113.118` | `roles_obj.target.endpoint.ip` + `target_ip` | `confirmed` |
| `app_name` | `IT相关` | `facets_obj.application.name` | `confirmed` |
| `op_action` | `被记录` | `extensions_obj.source_private.op_action`（审计动作，不映射 outcome） | `needs_review` |
| `url` | `http://www.shenxinfu.com/simple.php` | `roles_obj.target.domain.name` + `facets_obj.http.request.host` | `confirmed` |

## 人工语义复核（SXF Firewall，SR-075）

- 事件事实：深信服防火墙记录源端访问 Web 资源。
- `event_category=network`
- `event_type=network_http`
- `operation=empty`
- `outcome=unknown`；不将 `op_action`（被记录）或告警记录机械映射为动作结果。
- 主体/客体/载体：访问源（source.endpoint）/ Web 目标（target.endpoint+domain）/ http + application
- `source_finding_obj=null`：Web 访问审计非检测
- 文档证据：深信服防火墙 syslog 日志 8.0.50–8.0.95；样本字段已由 WPL 命中。
