# topas_waf / topas_waf_traffic 运行时观测候选映射

事件事实：来源安全产品生成检测或防护记录；检测声明保存在 source_finding，具体 event_type 待按底层事件事实复核。

主体：`unknown`；客体：`unknown`；载体：`observer_product`；观察者：来源产品。

> 状态：candidate，未注册、未批准。仅 WPL 解析事实已确认，SDM 语义仍需人工复核。

| WPL 字段 | 值 | SDM 候选路径 | 状态 |
|---|---|---|---|
| `id` | `ngtos` | `event_id` | `candidate` |
| `version` | `2.1` | `extensions_obj.source_private.version` | `source_private` |
| `time` | `2026-02-03 16:00:17` | `occur_time` | `candidate` |
| `dev` | `TopsecOS` | `extensions_obj.source_private.dev` | `source_private` |
| `pri` | `emergent` | `extensions_obj.source_private.pri` | `source_private` |
| `type` | `waf` | `extensions_obj.source_private.type` | `source_private` |
| `recorder` | `waf_traffic` | `extensions_obj.source_private.recorder` | `source_private` |
| `vsid` | `0` | `extensions_obj.source_private.vsid` | `source_private` |
| `client_ip` | `198.51.100.161` | `source_ip` | `candidate` |
| `sport` | `51954` | `source_port` | `candidate` |
| `server_ip` | `198.51.100.170` | `target_ip` | `candidate` |
| `dport` | `443` | `target_port` | `candidate` |
| `protocol` | `https` | `protocol` | `candidate` |
| `server` | `志愿献血者俱乐部` | `extensions_obj.source_private.server` | `source_private` |
| `host` | `mhssbc.shmh.gov.cn` | `extensions_obj.source_private.host` | `source_private` |
| `url` | `/login.action` | `extensions_obj.source_private.url` | `source_private` |
| `http_args` | `-` | `extensions_obj.source_private.http_args` | `source_private` |
| `http_method` | `GET` | `http_method` | `candidate` |
| `http_useragent` | `curl/7.29.0` | `extensions_obj.source_private.http_useragent` | `source_private` |
| `http_status` | `200` | `extensions_obj.source_private.http_status` | `source_private` |
| `http_referer` | `-` | `extensions_obj.source_private.http_referer` | `source_private` |
| `real_ip` | `203.0.113.62` | `extensions_obj.source_private.real_ip` | `source_private` |
| `upstream` | `181` | `extensions_obj.source_private.upstream` | `source_private` |
| `downstream` | `5382` | `extensions_obj.source_private.downstream` | `source_private` |

## 人工语义复核（TopWAF 2.x）

- 事件事实：WAF 记录客户端向受保护服务器发起的一次 HTTPS GET 请求及响应状态。
- `event_category=network`
- `event_type=network_http`
- `operation=empty`
- `outcome=unknown`：不将来源处置或 HTTP 状态机械映射为底层动作结果。
- `log_level=emergent`：仅来自 `pri`，不作为安全严重度。
- 文档证据：天融信《waf2.0日志格式文档-v2.0》；`recorder=waf_traffic`，WPL 运行样本已命中。
