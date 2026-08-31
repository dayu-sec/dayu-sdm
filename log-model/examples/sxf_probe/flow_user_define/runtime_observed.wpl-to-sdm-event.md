# sxf_probe / flow_user_define 运行时观测候选映射

事件事实：探针 SMB 连接（logtype=smb）——用户 anonymous 访问 SMB 服务 192.0.2.211:445，command=6/status=0（字典未确认）。

主体：SMB 用户（source.user=username + source.endpoint=src_ip）；客体：SMB 服务（target.endpoint=dst_ip）；载体：`network_protocol` + `application`（facets）；观察者：来源产品。

> 状态：candidate，未注册、未批准。WPL 解析事实与深信服探针文档已确认；SR-077 人工复核结论见文末。

| WPL 字段 | 值 | SDM 候选路径 | 状态 |
|---|---|---|---|
| `appproto` | `SMB` | `facets_obj.application.name` | `confirmed` |
| `argument` | `{\"file_id\":171800789269}` | `extensions_obj.source_private.argument` | `source_private` |
| `command` | `6` | `extensions_obj.source_private.command` | `source_private` |
| `devname` | `SANGFOR STA` | `extensions_obj.source_private.devname` | `source_private` |
| `ds` | `20250522` | `extensions_obj.source_private.ds` | `source_private` |
| `dst_ip` | `192.0.2.211` | `roles_obj.target.endpoint.ip` + `target_ip` | `confirmed` |
| `dst_port` | `445` | `roles_obj.target.endpoint.port` | `confirmed` |
| `flags` | `0` | `extensions_obj.source_private.flags` | `source_private` |
| `flags2` | `0` | `extensions_obj.source_private.flags2` | `source_private` |
| `hh` | `10` | `extensions_obj.source_private.hh` | `source_private` |
| `iptype` | `4` | `extensions_obj.source_private.iptype` | `source_private` |
| `is_orig` | `true` | `extensions_obj.source_private.is_orig` | `source_private` |
| `logid` | `47881916615892` | `extensions_obj.source_private.logid` | `source_private` |
| `logtype` | `smb` | `extensions_obj.source_private.logtype` | `source_private` |
| `message_id` | `1142` | `extensions_obj.source_private.message_id` | `source_private` |
| `process_id` | `65279` | `extensions_obj.source_private.process_id` | `source_private` |
| `src_ip` | `198.51.100.194` | `roles_obj.source.endpoint.ip` + `source_ip` | `confirmed` |
| `src_port` | `50877` | `roles_obj.source.endpoint.port` | `confirmed` |
| `status` | `0` | `extensions_obj.source_private.status`（字典未确认，不映射 outcome） | `needs_review` |
| `sub_command` | `0` | `extensions_obj.source_private.sub_command` | `source_private` |
| `transproto` | `TCP` | `facets_obj.network.protocol.code` | `confirmed` |
| `tree` | `\u0000` | `extensions_obj.source_private.tree` | `source_private` |
| `tree_id` | `49` | `extensions_obj.source_private.tree_id` | `source_private` |
| `tree_service` | `\u0000` | `extensions_obj.source_private.tree_service` | `source_private` |
| `ts` | `2025-05-22 02:45:16` | `occur_time` | `candidate` |
| `uid` | `2729001902` | `extensions_obj.source_private.uid` | `source_private` |
| `user_id` | `87960930222193` | `extensions_obj.source_private.user_id` | `source_private` |
| `username` | `anonymous` | `roles_obj.source.user.name` | `confirmed` |
| `vendor` | `sangfor` | `extensions_obj.source_private.vendor` | `source_private` |
| `version` | `2` | `extensions_obj.source_private.version` | `source_private` |
| `word_count` | `0` | `extensions_obj.source_private.word_count` | `source_private` |

## 人工语义复核（SXF Probe，SR-077）

- 事件事实：探针记录一次 SMB 连接；command=6/status=0 的具体动作字典尚未确认。
- `event_category=network`，`event_type=network_connection`，`operation=empty`，`outcome=unknown`。
- 主体/客体/载体：SMB 用户（source.user+endpoint）/ SMB 服务（target.endpoint）/ network_protocol + application
- command=6/status=0 无标准路径，保留 `extensions.source_private`
- 文档证据：深信服《潜伏威胁探针数据接口对外说明 V2.0》；运行样本已命中。
- 未确认的协议数字/命令字典保留原值并 report。
