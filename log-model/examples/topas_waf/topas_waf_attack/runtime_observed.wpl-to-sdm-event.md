# topas_waf / topas_waf_attack 运行时观测候选映射

事件事实：来源安全产品生成检测或防护记录；检测声明保存在 source_finding，具体 event_type 待按底层事件事实复核。

主体：`unknown`；客体：`unknown`；载体：`observer_product`；观察者：来源产品。

> 状态：candidate，未注册、未批准。仅 WPL 解析事实已确认，SDM 语义仍需人工复核。

| WPL 字段 | 值 | SDM 候选路径 | 状态 |
|---|---|---|---|
| `id` | `ngtos` | `event_id` | `candidate` |
| `version` | `2.1` | `extensions_obj.source_private.version` | `source_private` |
| `hiredate` | `2026-01-23 11:00:00` | `occur_time` | `candidate` |
| `dev` | `TopsecOS` | `extensions_obj.source_private.dev` | `source_private` |
| `pri` | `warning` | `extensions_obj.source_private.pri` | `source_private` |
| `type` | `waf` | `extensions_obj.source_private.type` | `source_private` |
| `recorder` | `waf_attack` | `extensions_obj.source_private.recorder` | `source_private` |
| `vsid` | `0` | `extensions_obj.source_private.vsid` | `source_private` |
| `client_ip` | `198.51.100.54` | `source_ip` | `candidate` |
| `sport` | `64544` | `source_port` | `candidate` |
| `server_ip` | `203.0.113.115` | `target_ip` | `candidate` |
| `dport` | `80` | `target_port` | `candidate` |
| `protocol` | `http` | `protocol` | `candidate` |
| `server` | `test` | `extensions_obj.source_private.server` | `source_private` |
| `host` | `203.0.113.115` | `extensions_obj.source_private.host` | `source_private` |
| `url` | `/ecshop/data/brandlogo/1240803412367015368.gif` | `extensions_obj.source_private.url` | `source_private` |
| `http_args` | `-` | `extensions_obj.source_private.http_args` | `source_private` |
| `http_method` | `GET` | `http_method` | `candidate` |
| `http_useragent` | `Mozilla/5.0 (Windows NT 6.1; WOW64; rv:48.0) Gecko/20100101 Firefox/48.0` | `extensions_obj.source_private.http_useragent` | `source_private` |
| `http_status` | `403` | `extensions_obj.source_private.http_status` | `source_private` |
| `http_referer` | `http://203.0.113.115/ecshop/?and%201=(select%20count(*)%20from%20master.dbo.sysobjects%20where%20xtype%20=%20%27x%27%20and%2...` | `extensions_obj.source_private.http_referer` | `source_private` |
| `real_ip` | `198.51.100.54` | `extensions_obj.source_private.real_ip` | `source_private` |
| `severity` | `High` | `severity` | `candidate` |
| `event_type` | `ATTACK_SQLI` | `extensions_obj.source_private.event_type` | `source_private` |
| `rule_id` | `1040020` | `event_id` | `candidate` |
| `action` | `deny` | `source_finding.status` | `candidate`；deny 是来源处置，不进顶层 outcome（SR-083 批准） |
| `action_data` | `-` | `extensions_obj.source_private.action_data` | `source_private` |
| `msg` | `SQL SELECT Statement Anomaly Detection Alert` | `extensions_obj.source_private.msg` | `source_private` |
| `http_detail` | `Matched Data:  http://203.0.113.115/ecshop/?and 1=(select count(*) from master.dbo.sysobjects where xtype = 'x' and name = '...` | `extensions_obj.source_private.http_detail` | `source_private` |
| `reqhdr` | `-` | `extensions_obj.source_private.reqhdr` | `source_private` |
| `rsphdr` | `-` | `extensions_obj.source_private.rsphdr` | `source_private` |

## 人工语义复核（TopWAF 2.x）

- 事件事实：WAF 记录一次 HTTP SQL 注入检测；客户端是观测来源，受保护服务器是观测目标。
- `event_category=alert`
- `event_type=network_http`
- `operation=empty`
- `outcome=unknown`：不将来源处置或 HTTP 状态机械映射为底层动作结果。
- `log_level=warning`：仅来自 `pri`，不作为安全严重度。
- 文档证据：天融信《waf2.0日志格式文档-v2.0》；`recorder=waf_attack`，WPL 运行样本已命中。
