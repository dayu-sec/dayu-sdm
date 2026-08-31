# topas_ips / topas_ips_attack 运行时观测候选映射

事件事实：IPS 攻击检测（recorder=attack，rule 95000 命中）。检测声明保存在 source_finding；op/result 是来源处置，不是已确认的底层动作结果。

主体：`source_endpoint`（sip/sport）；客体：`target_endpoint`（dip/dport）；载体：`network_protocol`（facets.network，proto/direction）；观察者：来源产品。

> 状态：candidate，未注册、未批准。WPL 解析事实与 TopIDP v3 文档章节已确认；SR-037 人工复核结论见文末。

| WPL 字段 | 值 | SDM 候选路径 | 状态 |
|---|---|---|---|
| `vendor` | `topsec` | `extensions_obj.source_private.vendor` | `source_private` |
| `dev_type` | `1` | `extensions_obj.source_private.dev_type` | `source_private` |
| `dev_name` | `TopsecOS` | `extensions_obj.source_private.dev_name` | `source_private` |
| `dev_ip` | `203.0.113.127` | `extensions_obj.source_private.dev_ip` | `source_private` |
| `time` | `2026-01-23 11:00:00` | `occur_time` | `candidate` |
| `index` | `301` | `event_id` | `candidate` |
| `recorder` | `attack` | `extensions_obj.source_private.recorder` | `source_private` |
| `type` | `17` | `extensions_obj.source_private.type` | `source_private` |
| `sub_type` | `` | `extensions_obj.source_private.sub_type` | `source_private` |
| `level` | `1` | `severity` | `candidate` |
| `sid` | `427299216830932575` | `source_finding_obj.rule.signature_id` + `original_id` | `confirmed` |
| `proto` | `2` | `facets_obj.network.protocol.code` | `confirmed` |
| `sip` | `203.0.113.143` | `roles_obj.source.endpoint.ip` + `source_ip` | `confirmed` |
| `sport` | `53490` | `roles_obj.source.endpoint.port` | `confirmed` |
| `dip` | `198.51.100.109` | `roles_obj.target.endpoint.ip` + `target_ip` | `confirmed` |
| `dport` | `80` | `roles_obj.target.endpoint.port` | `confirmed` |
| `sipv6` | `` | `extensions_obj.source_private.sipv6` | `source_private` |
| `dipv6` | `` | `extensions_obj.source_private.dipv6` | `source_private` |
| `vid` | `` | `extensions_obj.source_private.vid` | `source_private` |
| `sdev` | `feth1` | `extensions_obj.source_private.sdev` | `source_private` |
| `ddev` | `` | `extensions_obj.source_private.ddev` | `source_private` |
| `smac` | `00:00:00:00:00:01` | `extensions_obj.source_private.smac` | `source_private` |
| `dmac` | `00:00:00:00:00:02` | `extensions_obj.source_private.dmac` | `source_private` |
| `op` | `1` | `extensions_obj.source_private.op` | `source_private` |
| `rule` | `95000` | `source_finding_obj.rule.label`（原值保留 source_private） | `confirmed` |
| `msg` | `22222` | `extensions_obj.source_private.msg` | `source_private` |
| `repeat` | `1` | `source_finding_obj.count`（原值保留 source_private） | `confirmed` |
| `cve` | `` | `extensions_obj.source_private.cve` | `source_private` |
| `app_pro` | `1` | `extensions_obj.source_private.app_pro` | `source_private` |
| `app` | `HTTP` | `extensions_obj.source_private.app` | `source_private` |
| `method` | `POST` | `http_method` | `candidate` |
| `appendix` | `(URL=http://www.example.com/admbook/write.php)` | `extensions_obj.source_private.appendix` | `source_private` |
| `response_code` | `200 OK` | `extensions_obj.source_private.response_code` | `source_private` |
| `file` | `` | `extensions_obj.source_private.file` | `source_private` |
| `client` | `unknown,sun-tzu` | `extensions_obj.source_private.client` | `source_private` |
| `server` | `unknown` | `extensions_obj.source_private.server` | `source_private` |
| `sgeo` | `Private IP` | `extensions_obj.source_private.sgeo` | `source_private` |
| `dgeo` | `Private IP` | `extensions_obj.source_private.dgeo` | `source_private` |
| `result` | `0` | `outcome` | `candidate` |
| `x_forwarded_for` | `GUESS_WHAT:';if(isset(_GET[CMD])){ECHO'Hi .Master!';INI_SET('max_execution_time',0);PASSTHRU(_GET[CMD]);DIE;}echo'` | `extensions_obj.source_private.x_forwarded_for` | `source_private` |
| `x_real_ip` | `1::111` | `extensions_obj.source_private.x_real_ip` | `source_private` |
| `direction` | `c2s` | `facets_obj.network.direction`（原值保留 source_private） | `confirmed` |
| `fingerprint` | `2,474554#` | `extensions_obj.source_private.fingerprint` | `source_private` |
| `req_header` | `UE9TVCAvYWRtYm9vay93cml0ZS5waHAgSFRUUC8xLjENClJlZmVyZXI6IGh0dHA6Ly93d3cuc3RvbmVkY29kZXIub3JnL2FkbWJvb2svaW5kZXgucGhwDQpYLUZvcndhcmRlZC1Gb3I6IEdVRVNTX1dIQVQ6JztpZiAoaXNzZXQoJF9HRVRbQ01EXSkpe0VDSE8nSGkgLk1hc3RlciEnO0lOSV9TRVQoJ21heF9leGVjdXRpb25fdGltZScsMCk7UEFTU1RIUlUoJF9HRVRbQ01EXSk7RElFO31lY2hvJw0KQ29udGVudC1UeXBlOiBhcHBsaWNhdGlv` | `extensions_obj.source_private.req_header` | `source_private` |
| `req_body` | `cGFnZT0xJm5hbWU9d2hvYW1pJnVybD0mZW1haWw9d2hvYW1pQFNVTlRaVS5DT00maWNxPSZtZXNzYWdlPUklMjBsb3ZlJTIwaXRhbGlhbiUyMGd1eXNl` | `extensions_obj.source_private.req_body` | `source_private` |
| `resp_header` | `SFRUUC8xLjEgMjAwIE9LDQpTZXJ2ZXI6IEFwYWNoZQ0KTGFzdC1Nb2RpZmllZDogTW9uLCAwMiBGZWIgMjAwNCAxMTozMjo0MSBHTVQNCkVUYWc6ICJhODQo=` | `extensions_obj.source_private.resp_header` | `source_private` |
| `resp_body` | `UHduVCE=` | `extensions_obj.source_private.resp_body` | `source_private` |

## 人工语义复核（TopIDP v3，SR-037）

- 事件事实：IPS 攻击检测是来源发现；op/result 不是已确认的底层动作结果。
- event_category：`alert`
- event_type：`generic_event`（06 无攻击检测专用类型）
- operation：`空`
- outcome：`unknown`（op=1/result=0 保持来源私有，不机械映射）
- 检测声明：`source_finding_obj{original_id=sid, title=攻击检测（rule 95000）, count=repeat, rule{signature_id=sid, label=rule}}`
- 证据：TopIDP 输出信息格式规范 v3，`recorder=attack`；WPL 运行样本已命中。
