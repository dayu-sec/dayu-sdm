# topas_ips / topas_ips_audit_file 运行时观测候选映射

事件事实：文件审计（recorder=audit_file）——FTP 传输文件 04--csrss.exe，203.0.113.9:54454 -> 198.51.100.249:54656。

主体：源端点（source.endpoint=sip）；客体：传输文件（target.file=file + target.endpoint=dip）；载体：`application` + `network.direction`（facets）；观察者：来源产品。

> 状态：candidate，未注册、未批准。WPL 解析事实与 TopIDP v3 已确认；SR-079 人工复核结论见文末。

| WPL 字段 | 值 | SDM 候选路径 | 状态 |
|---|---|---|---|
| `vendor` | `topsec` | `extensions_obj.source_private.vendor` | `source_private` |
| `dev_type` | `4` | `extensions_obj.source_private.dev_type` | `source_private` |
| `dev_name` | `` | `extensions_obj.source_private.dev_name` | `source_private` |
| `dev_ip` | `203.0.113.127` | `extensions_obj.source_private.dev_ip` | `source_private` |
| `time` | `2026-01-23 11:00:00` | `occur_time` | `candidate` |
| `index` | `404` | `event_id` | `candidate` |
| `recorder` | `audit_file` | `extensions_obj.source_private.recorder` | `source_private` |
| `sid` | `5d81a5380026851` | `event_id` | `candidate` |
| `proto` | `2` | `protocol` | `candidate` |
| `sip` | `203.0.113.9` | `roles_obj.source.endpoint.ip` + `source_ip` | `confirmed` |
| `sport` | `54454` | `roles_obj.source.endpoint.port` | `confirmed` |
| `dip` | `198.51.100.249` | `roles_obj.target.endpoint.ip` + `target_ip` | `confirmed` |
| `dport` | `54656` | `roles_obj.target.endpoint.port` | `confirmed` |
| `sipv6` | `` | `extensions_obj.source_private.sipv6` | `source_private` |
| `dipv6` | `` | `extensions_obj.source_private.dipv6` | `source_private` |
| `vid` | `` | `extensions_obj.source_private.vid` | `source_private` |
| `sdev` | `feth0` | `extensions_obj.source_private.sdev` | `source_private` |
| `ddev` | `` | `extensions_obj.source_private.ddev` | `source_private` |
| `smac` | `00:00:5E:00:53:F1` | `extensions_obj.source_private.smac` | `source_private` |
| `dmac` | `00:00:5E:00:53:8E` | `extensions_obj.source_private.dmac` | `source_private` |
| `application` | `FTP` | `facets_obj.application.name` | `confirmed` |
| `file` | `04--csrss.exe` | `roles_obj.target.file.name` | `confirmed` |
| `filesize` | `104470784514048` | `roles_obj.target.file.size` | `confirmed` |
| `filetype` | `EXE` | `roles_obj.target.file.extension` | `confirmed` |
| `md5` | `342271f6142e7c70805b8a81e1ba5f5c` | `roles_obj.target.file.hashes.md5` | `confirmed` |
| `direction` | `s2c` | `facets_obj.network.direction` | `confirmed` |


## 人工语义复核（TopIDP v3）

- 事件事实：文件审计记录文件传输方向，但未提供明确动作结果。
- event_category：`network`
- event_type：`file_read`
- operation：`空`
- outcome：`unknown`
- 证据：TopIDP 输出信息格式规范 v3，`recorder=audit_file`；WPL 运行样本已命中。


## 人工语义复核（TopIDP v3）

- 事件事实：文件审计记录文件传输方向，但未提供明确动作结果。
- event_category：`network`
- event_type：`file_read`
- operation：`空`
- outcome：`unknown`
- 证据：TopIDP 输出信息格式规范 v3，`recorder=audit_file`；WPL 运行样本已命中。


## 人工语义复核（TopIDP v3）

- 事件事实：文件审计记录文件传输方向，但未提供明确动作结果。
- event_category：`network`
- event_type：`file_read`
- operation：`空`
- outcome：`unknown`
- 证据：TopIDP 输出信息格式规范 v3，`recorder=audit_file`；WPL 运行样本已命中。
