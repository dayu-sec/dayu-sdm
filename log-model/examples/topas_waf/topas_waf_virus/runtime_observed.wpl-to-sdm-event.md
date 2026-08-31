# topas_waf / topas_waf_virus 运行时观测候选映射

事件事实：来源安全产品生成检测或防护记录；检测声明保存在 source_finding，具体 event_type 待按底层事件事实复核。

主体：`unknown`；客体：`unknown`；载体：`observer_product`；观察者：来源产品。

> 状态：candidate，未注册、未批准。仅 WPL 解析事实已确认，SDM 语义仍需人工复核。

| WPL 字段 | 值 | SDM 候选路径 | 状态 |
|---|---|---|---|
| `id` | `ngtos` | `event_id` | `candidate` |
| `version` | `2.1` | `extensions_obj.source_private.version` | `source_private` |
| `hiredate` | `2026-01-23 11:00:00` | `occur_time` | `candidate` |
| `dev` | `TopsecOS` | `extensions_obj.source_private.dev` | `source_private` |
| `pri` | `emergent` | `extensions_obj.source_private.pri` | `source_private` |
| `type` | `waf` | `extensions_obj.source_private.type` | `source_private` |
| `recorder` | `virus` | `extensions_obj.source_private.recorder` | `source_private` |
| `vsid` | `0` | `extensions_obj.source_private.vsid` | `source_private` |
| `client_ip` | `192.0.2.176` | `source_ip` | `candidate` |
| `sport` | `36285` | `source_port` | `candidate` |
| `server_ip` | `192.0.2.44` | `target_ip` | `candidate` |
| `dport` | `80` | `target_port` | `candidate` |
| `protocol` | `http` | `protocol` | `candidate` |
| `server` | `pro1` | `extensions_obj.source_private.server` | `source_private` |
| `host` | `` | `extensions_obj.source_private.host` | `source_private` |
| `url` | `/upload_file.php` | `extensions_obj.source_private.url` | `source_private` |
| `http_args` | `-` | `extensions_obj.source_private.http_args` | `source_private` |
| `http_method` | `POST` | `http_method` | `candidate` |
| `http_useragent` | `Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:11.0) Gecko/20100101 Firefox/11.0` | `extensions_obj.source_private.http_useragent` | `source_private` |
| `http_status` | `403` | `extensions_obj.source_private.http_status` | `source_private` |
| `http_referer` | `http://192.0.2.44/upload.html` | `extensions_obj.source_private.http_referer` | `source_private` |
| `real_ip` | `192.0.2.176` | `extensions_obj.source_private.real_ip` | `source_private` |
| `action` | `deny` | `outcome` | `candidate` |
| `action_data` | `-` | `extensions_obj.source_private.action_data` | `source_private` |
| `filename` | `/SE/waf/upload_cache/aaron.zip` | `extensions_obj.source_private.filename` | `source_private` |

## 人工语义复核（TopWAF 2.x）

- 事件事实：WAF 在 HTTP POST 上传流量中记录一次文件病毒防护事件；deny 是来源处置而非底层动作结果。
- `event_category=alert`
- `event_type=file_read`
- `operation=empty`
- `outcome=unknown`：不将来源处置或 HTTP 状态机械映射为底层动作结果。
- `log_level=emergent`：仅来自 `pri`，不作为安全严重度。
- 文档证据：天融信《waf2.0日志格式文档-v2.0》；`recorder=virus`，WPL 运行样本已命中。
