# topas_ips / topas_ips_virus 运行时观测候选映射

事件事实：恶意软件检测（recorder=virus）——FTP STOR 传输恶意 EXE。检测声明保存在 source_finding；op=alert 是来源处置，不是底层动作结果。

主体：`source_endpoint`（sip/sport）；客体：`malware_file`（related[].file）+ `target_endpoint`（dip/dport）；载体：`network_protocol`（facets.network）+ 应用 facets.application.name=ftp；观察者：来源产品。

> 状态：candidate，未注册、未批准。WPL 解析事实与 TopIDP v3 §3.4.4 已确认；SR-041 人工复核结论见文末。

| WPL 字段 | 值 | SDM 候选路径 | 状态 |
|---|---|---|---|
| `vendor` | `topsec` | `extensions_obj.source_private.vendor` | `source_private` |
| `dev_type` | `4` | `extensions_obj.source_private.dev_type` | `source_private` |
| `dev_name` | `` | `extensions_obj.source_private.dev_name` | `source_private` |
| `dev_ip` | `203.0.113.152` | `extensions_obj.source_private.dev_ip` | `source_private` |
| `time` | `2026-01-23 11:00:00` | `occur_time` | `candidate` |
| `index` | `302` | `event_id` | `candidate` |
| `recorder` | `virus` | `extensions_obj.source_private.recorder` | `source_private` |
| `type` | `11` | `extensions_obj.source_private.type` | `source_private` |
| `sub_type` | `11.1` | `extensions_obj.source_private.sub_type` | `source_private` |
| `level` | `4` | `severity` | `candidate` |
| `sid` | `5d89e577000015f` | `source_finding_obj.rule.signature_id` + `original_id` | `confirmed` |
| `proto` | `TCP` | `facets_obj.network.protocol.code` | `confirmed` |
| `sip` | `198.51.100.96` | `roles_obj.source.endpoint.ip` + `source_ip` | `confirmed` |
| `sport` | `20` | `roles_obj.source.endpoint.port` | `confirmed` |
| `dip` | `203.0.113.228` | `roles_obj.target.endpoint.ip` + `target_ip` | `confirmed` |
| `dport` | `49946` | `roles_obj.target.endpoint.port` | `confirmed` |
| `sipv6` | `` | `extensions_obj.source_private.sipv6` | `source_private` |
| `dipv6` | `` | `extensions_obj.source_private.dipv6` | `source_private` |
| `vid` | `` | `extensions_obj.source_private.vid` | `source_private` |
| `sdev` | `feth0` | `extensions_obj.source_private.sdev` | `source_private` |
| `ddev` | `feth1` | `extensions_obj.source_private.ddev` | `source_private` |
| `smac` | `00:0C:29:4D:04:B8` | `extensions_obj.source_private.smac` | `source_private` |
| `dmac` | `00:90:0B:3E:C0:DA` | `extensions_obj.source_private.dmac` | `source_private` |
| `op` | `alert` | `source_finding_obj.action` | `confirmed` |
| `rule` | `0` | `source_finding_obj.rule.label` | `confirmed` |
| `msg` | `13296f528d570e126b7671639f215745` | `source_finding_obj.title` | `confirmed` |
| `repeat` | `1` | `source_finding_obj.count` | `confirmed` |
| `file` | `code哼red2.exe` | `roles_obj.related[0].file.name` | `confirmed` |
| `filetype` | `EXE` | `roles_obj.related[0].file.extension` | `confirmed` |
| `filesize` | `8192` | `roles_obj.related[0].file.size` | `confirmed` |
| `md5` | `13296f528d570e126b7671639f21574` | `roles_obj.related[0].file.hashes.md5` | `confirmed` |
| `sha1` | `` | `roles_obj.related[0].file.hashes.sha1` | `confirmed` |
| `app_pro` | `FTP` | `facets_obj.application.name` | `confirmed` |
| `app` | `FTP` | `facets_obj.application.name` | `confirmed` |
| `method` | `STOR` | `extensions_obj.source_private.method` | `needs_review` |
| `appendix` | `` | `extensions_obj.source_private.appendix` | `source_private` |
| `direction` | `c2s` | `facets_obj.network.direction` | `confirmed` |
| `sgeo` | `美国` | `extensions_obj.source_private.sgeo` | `source_private` |
| `dgeo` | `美国` | `extensions_obj.source_private.dgeo` | `source_private` |


## 人工语义复核（TopIDP v3，SR-041）

- 事件事实：恶意软件检测日志是来源发现；op=alert 仅保留来源处置。
- event_category：`alert`
- event_type：`generic_event`（06 无恶意软件检测专用类型）
- operation：`空`
- outcome：`unknown`（op=alert 是来源处置，非底层动作结果）
- 主体/客体/载体：source_endpoint / malware_file（related）+ target_endpoint / network_protocol
- 检测声明：`source_finding_obj{original_id=sid, title=msg, count=repeat, action=op, rule{signature_id=sid, label=rule}}`
- 证据：TopIDP 输出信息格式规范 v3 §3.4.4，`recorder=virus`；WPL 运行样本已命中。
