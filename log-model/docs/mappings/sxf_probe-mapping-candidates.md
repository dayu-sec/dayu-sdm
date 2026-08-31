# sxf_probe 字段映射与枚举候选

候选结果，未经标准注册审批。样本字段为源目录级证据；只有 WPL 规则块字段被归属到具体 log_type。

## `flow_dns`

- 状态：`candidate`
- 证据：`sample_inferred`
- WPL 规则：flow_dns
- 样本：`log-model/examples/sxf_probe/`，目录级非空行 8

| 来源字段 | SDM 候选目标 | 转换/保留策略 | 证据 |
|---|---|---|---|
| `Additional` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `Answers` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `Authority` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `Questions` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `aa` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `aclasses` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `ad` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `afver` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `ancnt` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `answers` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `appproto` | `protocol` | `candidate_identity` | `sample_inferred` |
| `arcnt` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `atypes` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `cd` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `cf` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `devname` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `ds` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dst_ip` | `target_ip` | `candidate_identity` | `sample_inferred` |
| `dst_port` | `target_port` | `candidate_identity` | `sample_inferred` |
| `dzone` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `hh` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `id` | `event_id` | `candidate_identity` | `sample_inferred` |
| `iptype` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `length` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `logid` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `logtype` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `nscnt` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `opcode` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `qclasses` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `qdcnt` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `qr` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `qtypes` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `queries` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `ra` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `rcode` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `rd` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `src_ip` | `source_ip` | `candidate_identity` | `sample_inferred` |
| `src_port` | `source_port` | `candidate_identity` | `sample_inferred` |
| `szone` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `tc` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `transproto` | `protocol` | `candidate_identity` | `sample_inferred` |
| `ts` | `occur_time` | `candidate_identity` | `sample_inferred` |
| `ttls` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `uid` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `vendor` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `z` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |

枚举/选择器信号：
- 字段 `logtype`（in）；候选值 dns_response, dns_request；未知值策略：`preserve_raw_and_report`

## `flow_mail`

- 状态：`candidate`
- 证据：`sample_inferred`
- WPL 规则：flow_mail
- 样本：`log-model/examples/sxf_probe/`，目录级非空行 8

| 来源字段 | SDM 候选目标 | 转换/保留策略 | 证据 |
|---|---|---|---|
| `appproto` | `protocol` | `candidate_identity` | `sample_inferred` |
| `bcc` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `cc` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `date` | `occur_time` | `candidate_identity` | `sample_inferred` |
| `devname` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `ds` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dst_ip` | `target_ip` | `candidate_identity` | `sample_inferred` |
| `dst_port` | `target_port` | `candidate_identity` | `sample_inferred` |
| `file_info` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `from` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `fuids` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `helo` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `helo_reply` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `hh` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `in_reply_to` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `iptype` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `last_command` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `last_reply_code` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `last_reply_msg` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `logid` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `logtype` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `mailfrom` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `mime_version` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `msg_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `rcptto` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `receiveds` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `reply_to` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `src_ip` | `source_ip` | `candidate_identity` | `sample_inferred` |
| `src_port` | `source_port` | `candidate_identity` | `sample_inferred` |
| `subject` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `to` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `trans_depth` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `transproto` | `protocol` | `candidate_identity` | `sample_inferred` |
| `ts` | `occur_time` | `candidate_identity` | `sample_inferred` |
| `uid` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `user` | `source_user` | `candidate_identity` | `sample_inferred` |
| `user_agent` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `vendor` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `x_originating_ip` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |

枚举/选择器信号：
- 字段 `logtype`（in）；候选值 imap, pop3, smtp；未知值策略：`preserve_raw_and_report`

## `flow_user_define`

- 状态：`candidate`
- 证据：`sample_inferred`
- WPL 规则：flow_user_define_smb, flow_user_define_net
- 样本：`log-model/examples/sxf_probe/`，目录级非空行 8

| 来源字段 | SDM 候选目标 | 转换/保留策略 | 证据 |
|---|---|---|---|
| `appproto` | `protocol` | `candidate_identity` | `sample_inferred` |
| `argument` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `attack_count` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `command` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `devname` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `ds` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dst_ip` | `target_ip` | `candidate_identity` | `sample_inferred` |
| `dst_port` | `target_port` | `candidate_identity` | `sample_inferred` |
| `flags` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `flags2` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `hh` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `iptype` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `is_orig` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `l3proto` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `l7proto` | `protocol` | `candidate_identity` | `sample_inferred` |
| `logid` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `logtype` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `message_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `nAppCrc` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `nNetAction` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `nPolicyId` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `nPrivateType` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `nProtocol` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `nServCrc` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `nType` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `process_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `request_flow` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `request_pack` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `response_flow` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `response_pack` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `session_start_time` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `session_state` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `session_time` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `src_ip` | `source_ip` | `candidate_identity` | `sample_inferred` |
| `src_port` | `source_port` | `candidate_identity` | `sample_inferred` |
| `status` | `outcome` | `candidate_identity` | `sample_inferred` |
| `sub_command` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `transproto` | `protocol` | `candidate_identity` | `sample_inferred` |
| `tree` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `tree_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `tree_service` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `ts` | `occur_time` | `candidate_identity` | `sample_inferred` |
| `uid` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `user_id` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `username` | `source_user` | `candidate_identity` | `sample_inferred` |
| `vendor` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `version` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `word_count` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |

枚举/选择器信号：
- 字段 `logtype`（has）；候选值 smb；未知值策略：`preserve_raw_and_report`
- 字段 `logtype`（has）；候选值 netflow；未知值策略：`preserve_raw_and_report`

## `flow_web`

- 状态：`candidate`
- 证据：`sample_inferred`
- WPL 规则：flow_web
- 样本：`log-model/examples/sxf_probe/`，目录级非空行 8

| 来源字段 | SDM 候选目标 | 转换/保留策略 | 证据 |
|---|---|---|---|
| `DSReq` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `DSRsp` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `HHReq` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `HHRsp` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `afver` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `appproto` | `protocol` | `candidate_identity` | `sample_inferred` |
| `cookie` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `devname` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `ds` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dst_ip` | `target_ip` | `candidate_identity` | `sample_inferred` |
| `dst_ip_req` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dst_ip_rsp` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dst_port` | `target_port` | `candidate_identity` | `sample_inferred` |
| `dst_port_req` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dst_port_rsp` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `duration` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `dzone` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `expires` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `hh` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `host` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `iptype` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `logid` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `logtype` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `method` | `http_method` | `candidate_identity` | `sample_inferred` |
| `referer` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `req_body` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `req_body_len` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `req_content_type` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `req_head` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `req_len` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `req_ts` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `rsp_body` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `rsp_body_len` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `rsp_content_type` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `rsp_head` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `rsp_len` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `rsp_ts` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `server` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `set_cookie` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `src_ip` | `source_ip` | `candidate_identity` | `sample_inferred` |
| `src_ip_req` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `src_ip_rsp` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `src_port` | `source_port` | `candidate_identity` | `sample_inferred` |
| `src_port_req` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `src_port_rsp` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `status_code` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `szone` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `transproto` | `protocol` | `candidate_identity` | `sample_inferred` |
| `ts` | `occur_time` | `candidate_identity` | `sample_inferred` |
| `uid` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `uri` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `user` | `source_user` | `candidate_identity` | `sample_inferred` |
| `user_agent` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `vendor` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |
| `x_forwarded_for` | `extensions.source_private` | `preserve_raw_to_source_private` | `sample_inferred` |

枚举/选择器信号：
- 字段 `logtype`（has）；候选值 http_session；未知值策略：`preserve_raw_and_report`

