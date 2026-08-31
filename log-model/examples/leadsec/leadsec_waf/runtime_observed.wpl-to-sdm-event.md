# leadsec / leadsec_waf 运行时观测候选映射

事件事实：WAF 跨站脚本攻击（recorder=event，Web应用防护）——HTTP 请求 203.0.113.206:3746 → 203.0.113.192:80，action=丢弃。检测声明在 source_finding。

主体：`http_client`（source.endpoint=srcaddr/srcport）；客体：`web_server`（target.endpoint=destaddr/destport）；载体：`http`（facets.network.protocol=TCP + facets.http.request）；观察者：来源产品。

> 状态：candidate，未注册、未批准。WPL 解析事实与 Power-V 文档已确认；SR-052 人工复核结论见文末。

| WPL 字段 | 值 | SDM 候选路径 | 状态 |
|---|---|---|---|
| `info` | `event` | `extensions_obj.source_private.info` | `source_private` |
| `devid` | `0` | `extensions_obj.source_private.devid` | `source_private` |
| `date` | `2026-01-23 11:00:00` | `occur_time` | `candidate` |
| `dname` | `themis` | `extensions_obj.source_private.dname` | `source_private` |
| `logtype` | `29` | `extensions_obj.source_private.logtype` | `source_private` |
| `pri` | `4` | `extensions_obj.source_private.pri` | `source_private` |
| `ver` | `0.3.0` | `extensions_obj.source_private.ver` | `source_private` |
| `user` | `` | `source_user` | `candidate` |
| `mod` | `Web应用防护` | `extensions_obj.source_private.mod` | `source_private` |
| `eventtype` | `WAF` | `extensions_obj.source_private.eventtype` | `source_private` |
| `eventname` | `跨站脚本攻击` | `source_finding_obj.title` | `confirmed` |
| `severity` | `中` | `severity` | `candidate` |
| `dsp_msg` | `检测到攻击:跨站脚本攻击` | `extensions_obj.source_private.dsp_msg` | `source_private` |
| `protocol` | `TCP` | `facets_obj.network.protocol.code` | `confirmed` |
| `srcaddr` | `203.0.113.206` | `roles_obj.source.endpoint.ip` + `source_ip` | `confirmed` |
| `srcport` | `3746` | `roles_obj.source.endpoint.port` | `confirmed` |
| `destaddr` | `203.0.113.192` | `roles_obj.target.endpoint.ip` + `target_ip` | `confirmed` |
| `destport` | `80` | `roles_obj.target.endpoint.port` | `confirmed` |
| `srcregion` | `HOST` | `extensions_obj.source_private.srcregion` | `source_private` |
| `destregion` | `CN-中国` | `extensions_obj.source_private.destregion` | `source_private` |
| `app` | `HTTP` | `extensions_obj.source_private.app` | `source_private` |
| `repeated` | `1` | `extensions_obj.source_private.repeated` | `source_private` |
| `eventdetails` | `/?yyy=zz%0aand%0dxxx=1` | `facets_obj.http.request.query` | `confirmed` |
| `action` | `丢弃` | `outcome=denied` + `source_finding_obj.status` | `confirmed` |
| `if` | `` | `extensions_obj.source_private.if` | `source_private` |
| `fwlog` | `0` | `extensions_obj.source_private.fwlog` | `source_private` |

## 人工语义复核（Leadsec Power-V，SR-052）

- 事件事实：WAF 日志记录跨站脚本攻击，action=丢弃与文档 drop 枚举共同支持拒绝处置。
- `event_category=alert`，`event_type=network_http`，`operation=empty`，**`outcome=denied`**（action=丢弃）。
- 主体/客体/载体：http_client / web_server / http
- 检测声明：`source_finding_obj`（title/severity/status/count/rule.name=WAF）
- `pri` 仅映射 `log_level`；来源 severity 保留在 `source_finding`。
- 文档证据：Power-V 192.0.2.120 日志格式手册 VERSION 0.3.0；证据状态 `vendor_confirmed_and_observed`。
