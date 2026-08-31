# leadsec / leadsec_ips 运行时观测候选映射

事件事实：IPS 入侵防护（recorder=ips）——攻击 203.0.113.206:56085 → 203.0.113.219:80，action=drop=丢弃。检测声明保存在 source_finding。

主体：`source_endpoint`（srcaddr/srcport）；客体：`target_endpoint`（destaddr/destport）；载体：`network_protocol`（facets.network.protocol=TCP）；观察者：来源产品。

> 状态：candidate，未注册、未批准。WPL 解析事实与 Power-V 文档已确认；SR-049 人工复核结论见文末。

| WPL 字段 | 值 | SDM 候选路径 | 状态 |
|---|---|---|---|
| `info` | `ips` | `extensions_obj.source_private.info` | `source_private` |
| `devid` | `0` | `extensions_obj.source_private.devid` | `source_private` |
| `date` | `2026-01-23 11:00:00` | `occur_time` | `candidate` |
| `dname` | `Themis` | `extensions_obj.source_private.dname` | `source_private` |
| `logtype` | `16` | `extensions_obj.source_private.logtype` | `source_private` |
| `pri` | `4` | `extensions_obj.source_private.pri` | `source_private` |
| `ver` | `0.3.0` | `extensions_obj.source_private.ver` | `source_private` |
| `user` | `` | `source_user` | `candidate` |
| `mod` | `ips` | `extensions_obj.source_private.mod` | `source_private` |
| `eventtype` | `IPS` | `extensions_obj.source_private.eventtype` | `source_private` |
| `eventname` | `UserDefine sina_alert` | `extensions_obj.source_private.eventname` | `source_private` |
| `severity` | `1` | `severity` | `candidate` |
| `dsp_msg` | `检测到攻击: sina_alert; 类型: UserDefine` | `extensions_obj.source_private.dsp_msg` | `source_private` |
| `protocol` | `TCP` | `facets_obj.network.protocol.code` | `confirmed` |
| `srcaddr` | `203.0.113.206` | `roles_obj.source.endpoint.ip` + `source_ip` | `confirmed` |
| `srcport` | `56085` | `roles_obj.source.endpoint.port` | `confirmed` |
| `destaddr` | `203.0.113.219` | `roles_obj.target.endpoint.ip` + `target_ip` | `confirmed` |
| `destport` | `80` | `roles_obj.target.endpoint.port` | `confirmed` |
| `srcregion` | `HOST` | `extensions_obj.source_private.srcregion` | `source_private` |
| `destregion` | `CN-中国` | `extensions_obj.source_private.destregion` | `source_private` |
| `app` | `HTTP` | `extensions_obj.source_private.app` | `source_private` |
| `repeated` | `1` | `extensions_obj.source_private.repeated` | `source_private` |
| `eventdetails` | `/1245758104/50/1300244013/0` | `extensions_obj.source_private.eventdetails` | `source_private` |
| `action` | `drop` | `outcome=denied` + `source_finding_obj.status` | `confirmed` |
| `if` | `市场部` | `extensions_obj.source_private.if` | `source_private` |
| `fwlog` | `0` | `extensions_obj.source_private.fwlog` | `source_private` |

## 人工语义复核（Leadsec Power-V，SR-049）

- 事件事实：入侵防护日志记录从源到目标的攻击检测，action=drop 的文档枚举含义为丢弃。
- `event_category=alert`，`event_type=network_connection`，`operation=empty`，**`outcome=denied`**（action=drop=丢弃）。
- 主体/客体/载体：source_endpoint / target_endpoint / network_protocol
- 检测声明：`source_finding_obj`（title/severity/status/count/rule）
- `pri` 仅映射 `log_level`；来源 severity 保留在 `source_finding`。
- 文档证据：Power-V 192.0.2.120 日志格式手册 VERSION 0.3.0；证据状态 `vendor_confirmed_and_observed`。
