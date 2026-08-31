# topas_ips / topas_ips_audit_ftp 运行时观测候选映射

事件事实：FTP 审计——用户 anonymous 经 RETR 从 FTP 服务器(203.0.113.9:21)下载 04--csrss.exe，ret_code=226(Transfer complete)。

主体：FTP 用户（source.user=user + source.endpoint=sip）；客体：下载文件（target.file=file + target.endpoint=dip）；载体：`application`（facets）；观察者：来源产品。

> 状态：candidate，未注册、未批准。WPL 解析事实与 TopIDP v3 已确认；SR-080 人工复核结论见文末。

| WPL 字段 | 值 | SDM 候选路径 | 状态 |
|---|---|---|---|
| `vendor` | `topsec` | `extensions_obj.source_private.vendor` | `source_private` |
| `dev_type` | `4` | `extensions_obj.source_private.dev_type` | `source_private` |
| `dev_name` | `` | `extensions_obj.source_private.dev_name` | `source_private` |
| `dev_ip` | `203.0.113.127` | `extensions_obj.source_private.dev_ip` | `source_private` |
| `time` | `2026-01-23 11:00:00` | `occur_time` | `candidate` |
| `index` | `405` | `event_id` | `candidate` |
| `recorder` | `audit_ftp` | `extensions_obj.source_private.recorder` | `source_private` |
| `sid` | `5d81a5380026850` | `event_id` | `candidate` |
| `proto` | `2` | `protocol` | `candidate` |
| `sip` | `198.51.100.249` | `roles_obj.source.endpoint.ip` + `source_ip` | `confirmed` |
| `sport` | `54588` | `roles_obj.source.endpoint.port` | `confirmed` |
| `dip` | `203.0.113.9` | `roles_obj.target.endpoint.ip` + `target_ip` | `confirmed` |
| `dport` | `21` | `roles_obj.target.endpoint.port` | `confirmed` |
| `sipv6` | `` | `extensions_obj.source_private.sipv6` | `source_private` |
| `dipv6` | `` | `extensions_obj.source_private.dipv6` | `source_private` |
| `vid` | `` | `extensions_obj.source_private.vid` | `source_private` |
| `sdev` | `feth0` | `extensions_obj.source_private.sdev` | `source_private` |
| `ddev` | `` | `extensions_obj.source_private.ddev` | `source_private` |
| `smac` | `00:0C:29:DC:86:60` | `extensions_obj.source_private.smac` | `source_private` |
| `dmac` | `00:0C:29:05:1C:67` | `extensions_obj.source_private.dmac` | `source_private` |
| `user` | `anonymous` | `roles_obj.source.user.name` | `confirmed` |
| `cmd` | `RETR` | `extensions_obj.source_private.cmd` | `source_private` |
| `ret` | `Transfer complete` | `extensions_obj.source_private.ret` | `source_private` |
| `ret_code` | `226` | `outcome=success`（Transfer complete） | `confirmed` |
| `file` | `04--csrss.exe` | `roles_obj.target.file.name` | `confirmed` |


## 人工语义复核（TopIDP v3）

- 事件事实：FTP RETR 且 ret_code=226，支持文件读取成功候选。
- event_category：`network`
- event_type：`file_read`
- operation：`download`
- outcome：`unknown`
- 证据：TopIDP 输出信息格式规范 v3，`recorder=audit_ftp`；WPL 运行样本已命中。


## 人工语义复核（TopIDP v3）

- 事件事实：FTP RETR 且 ret_code=226，支持文件读取成功候选。
- event_category：`network`
- event_type：`file_read`
- operation：`download`
- outcome：`unknown`
- 证据：TopIDP 输出信息格式规范 v3，`recorder=audit_ftp`；WPL 运行样本已命中。


## 人工语义复核（TopIDP v3）

- 事件事实：FTP RETR 且 ret_code=226，支持文件读取成功候选。
- event_category：`network`
- event_type：`file_read`
- operation：`download`
- outcome：`unknown`
- 证据：TopIDP 输出信息格式规范 v3，`recorder=audit_ftp`；WPL 运行样本已命中。
