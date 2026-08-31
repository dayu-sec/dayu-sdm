# topas_ips / topas_ips_audit_nfs 运行时观测候选映射

事件事实：NFS 审计——NFS 文件读取操作 SecureCRTPortable.exe，198.51.100.34:781 -> 198.51.100.253:2049，nfs_op=read。

主体：源端点（source.endpoint=sip）；客体：读取文件（target.file=file_name + target.endpoint=dip）；载体：`application`（facets）；观察者：来源产品。

> 状态：candidate，未注册、未批准。WPL 解析事实与 TopIDP v3 已确认；SR-081 人工复核结论见文末。

| WPL 字段 | 值 | SDM 候选路径 | 状态 |
|---|---|---|---|
| `vendor` | `topsec` | `extensions_obj.source_private.vendor` | `source_private` |
| `dev_type` | `4` | `extensions_obj.source_private.dev_type` | `source_private` |
| `dev_name` | `` | `extensions_obj.source_private.dev_name` | `source_private` |
| `dev_ip` | `203.0.113.127` | `extensions_obj.source_private.dev_ip` | `source_private` |
| `time` | `2026-01-23 11:00:00` | `occur_time` | `candidate` |
| `index` | `412` | `event_id` | `candidate` |
| `recorder` | `audit_nfs` | `extensions_obj.source_private.recorder` | `source_private` |
| `sid` | `5d81a6ca0026855` | `event_id` | `candidate` |
| `proto` | `2` | `protocol` | `candidate` |
| `sip` | `198.51.100.34` | `roles_obj.source.endpoint.ip` + `source_ip` | `confirmed` |
| `sport` | `781` | `roles_obj.source.endpoint.port` | `confirmed` |
| `dip` | `198.51.100.253` | `roles_obj.target.endpoint.ip` + `target_ip` | `confirmed` |
| `dport` | `2049` | `roles_obj.target.endpoint.port` | `confirmed` |
| `sipv6` | `` | `extensions_obj.source_private.sipv6` | `source_private` |
| `dipv6` | `` | `extensions_obj.source_private.dipv6` | `source_private` |
| `vid` | `` | `extensions_obj.source_private.vid` | `source_private` |
| `sdev` | `feth0` | `extensions_obj.source_private.sdev` | `source_private` |
| `ddev` | `` | `extensions_obj.source_private.ddev` | `source_private` |
| `smac` | `00:0C:29:05:DF:E8` | `extensions_obj.source_private.smac` | `source_private` |
| `dmac` | `00:0C:29:20:09:CE` | `extensions_obj.source_private.dmac` | `source_private` |
| `nfs_version` | `0` | `extensions_obj.source_private.nfs_version` | `source_private` |
| `operation` | `1` | `extensions_obj.source_private.operation` | `source_private` |
| `result` | `0` | `extensions_obj.source_private.result`（字典未确认，不投影 outcome） | `source_private` |
| `nfs_proc` | `compound` | `extensions_obj.source_private.nfs_proc` | `source_private` |
| `nfs_op` | `read` | `extensions_obj.source_private.nfs_op` | `source_private` |
| `file_name` | `SecureCRTPortable.exe` | `roles_obj.target.file.name` | `confirmed` |
| `file_size` | `68836` | `roles_obj.target.file.size` | `confirmed` |
| `deal_size` | `68836` | `extensions_obj.source_private.deal_size` | `source_private` |


## 人工语义复核（TopIDP v3）

- 事件事实：NFS nfs_op=read，支持文件读取活动候选；result 数字字典待确认。
- event_category：`network`
- event_type：`file_read`
- operation：`extended`
- outcome：`unknown`
- 证据：TopIDP 输出信息格式规范 v3，`recorder=audit_nfs`；WPL 运行样本已命中。


## 人工语义复核（TopIDP v3）

- 事件事实：NFS nfs_op=read，支持文件读取活动候选；result 数字字典待确认。
- event_category：`network`
- event_type：`file_read`
- operation：`extended`
- outcome：`unknown`
- 证据：TopIDP 输出信息格式规范 v3，`recorder=audit_nfs`；WPL 运行样本已命中。


## 人工语义复核（TopIDP v3）

- 事件事实：NFS nfs_op=read，支持文件读取活动候选；result 数字字典待确认。
- event_category：`network`
- event_type：`file_read`
- operation：`extended`
- outcome：`unknown`
- 证据：TopIDP 输出信息格式规范 v3，`recorder=audit_nfs`；WPL 运行样本已命中。
