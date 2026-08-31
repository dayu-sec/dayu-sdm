# topas_ips / topas_ips_audit_smb 运行时观测候选映射

事件事实：SMB 审计——用户 topsec(主机 10232-SSG，198.51.100.201:51247)向 SMB 服务器(192.0.2.1:445)写入文件 CVE__2013-4123…pcap，smb_cmd=write。

主体：SMB 用户（source.user=user_name + source.host=host_name + source.endpoint=sip）；客体：写入文件（target.file=file_name + target.endpoint=dip）；载体：`application`（facets）；观察者：来源产品。

> 状态：candidate，未注册、未批准。WPL 解析事实与 TopIDP v3 已确认；SR-082 人工复核结论见文末。

| WPL 字段 | 值 | SDM 候选路径 | 状态 |
|---|---|---|---|
| `vendor` | `topsec` | `extensions_obj.source_private.vendor` | `source_private` |
| `dev_type` | `4` | `extensions_obj.source_private.dev_type` | `source_private` |
| `dev_name` | `` | `extensions_obj.source_private.dev_name` | `source_private` |
| `dev_ip` | `203.0.113.127` | `extensions_obj.source_private.dev_ip` | `source_private` |
| `time` | `2026-01-23 11:00:00` | `occur_time` | `candidate` |
| `index` | `413` | `event_id` | `candidate` |
| `recorder` | `audit_smb` | `extensions_obj.source_private.recorder` | `source_private` |
| `sid` | `5d81a9cb0000001` | `event_id` | `candidate` |
| `proto` | `2` | `protocol` | `candidate` |
| `sip` | `198.51.100.201` | `roles_obj.source.endpoint.ip` + `source_ip` | `confirmed` |
| `sport` | `51247` | `roles_obj.source.endpoint.port` | `confirmed` |
| `dip` | `192.0.2.1` | `roles_obj.target.endpoint.ip` + `target_ip` | `confirmed` |
| `dport` | `445` | `roles_obj.target.endpoint.port` | `confirmed` |
| `sipv6` | `` | `extensions_obj.source_private.sipv6` | `source_private` |
| `dipv6` | `` | `extensions_obj.source_private.dipv6` | `source_private` |
| `vid` | `` | `extensions_obj.source_private.vid` | `source_private` |
| `sdev` | `feth0` | `extensions_obj.source_private.sdev` | `source_private` |
| `ddev` | `` | `extensions_obj.source_private.ddev` | `source_private` |
| `smac` | `10:60:4B:6A:71:D7` | `extensions_obj.source_private.smac` | `source_private` |
| `dmac` | `64:51:06:5A:55:91` | `extensions_obj.source_private.dmac` | `source_private` |
| `smb_version` | `2` | `extensions_obj.source_private.smb_version` | `source_private` |
| `operation` | `0` | `extensions_obj.source_private.operation` | `source_private` |
| `result` | `0` | `extensions_obj.source_private.result`（字典未确认，不投影 outcome） | `source_private` |
| `smb_cmd` | `write` | `extensions_obj.source_private.smb_cmd` | `source_private` |
| `user_name` | `topsec` | `roles_obj.source.user.name` | `confirmed` |
| `host_name` | `10232-SSG` | `roles_obj.source.host.name` | `confirmed` |
| `session_id` | `4398046511149` | `extensions_obj.source_private.session_id` | `source_private` |
| `tree_id` | `9` | `extensions_obj.source_private.tree_id` | `source_private` |
| `file_name` | `CVE__2013-4123__CVE 2013-4123 __1.1.181.233.pcap` | `roles_obj.target.file.name` | `confirmed` |
| `file_size` | `3691` | `roles_obj.target.file.size` | `confirmed` |
| `deal_size` | `3691` | `extensions_obj.source_private.deal_size` | `source_private` |


## 人工语义复核（TopIDP v3）

- 事件事实：SMB smb_cmd=write，支持文件写入活动候选；result 数字字典待确认。
- event_category：`network`
- event_type：`file_modification`
- operation：`write`
- outcome：`unknown`
- 证据：TopIDP 输出信息格式规范 v3，`recorder=audit_smb`；WPL 运行样本已命中。


## 人工语义复核（TopIDP v3）

- 事件事实：SMB smb_cmd=write，支持文件写入活动候选；result 数字字典待确认。
- event_category：`network`
- event_type：`file_modification`
- operation：`write`
- outcome：`unknown`
- 证据：TopIDP 输出信息格式规范 v3，`recorder=audit_smb`；WPL 运行样本已命中。


## 人工语义复核（TopIDP v3）

- 事件事实：SMB smb_cmd=write，支持文件写入活动候选；result 数字字典待确认。
- event_category：`network`
- event_type：`file_modification`
- operation：`write`
- outcome：`unknown`
- 证据：TopIDP 输出信息格式规范 v3，`recorder=audit_smb`；WPL 运行样本已命中。
