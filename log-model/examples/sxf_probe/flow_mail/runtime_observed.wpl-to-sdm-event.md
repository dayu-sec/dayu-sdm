# sxf_probe / flow_mail 运行时观测候选映射

事件事实：探针邮件会话（logtype=imap）——用户 user-7289a435@example.com 访问 IMAP 服务 203.0.113.204:143，邮件 mail_3。

主体：邮件用户（source.user=user + source.endpoint=src_ip）；客体：IMAP 服务（target.endpoint=dst_ip）；载体：`network_protocol` + `email`（facets）；观察者：来源产品。

> 状态：candidate，未注册、未批准。WPL 解析事实与深信服探针文档已确认；SR-076 人工复核结论见文末。

| WPL 字段 | 值 | SDM 候选路径 | 状态 |
|---|---|---|---|
| `appproto` | `IMAP` | `facets_obj.application.name` | `confirmed` |
| `cc` | `` | `facets_obj.email.cc` | `confirmed` |
| `date` | `Tue, 18 Sep 2018 19:46:22 +0800` | `occur_time` | `candidate` |
| `devname` | `SANGFOR STA` | `extensions_obj.source_private.devname` | `source_private` |
| `ds` | `20250522` | `extensions_obj.source_private.ds` | `source_private` |
| `dst_ip` | `203.0.113.204` | `roles_obj.target.endpoint.ip` + `target_ip` | `confirmed` |
| `dst_port` | `143` | `roles_obj.target.endpoint.port` | `confirmed` |
| `file_info` | `[{\"charset\":\"us-ascii\",\"depth\":2,\"extract_bytes\":23,\"file_type\":\"body\",\"fuid\":\"L88K1PGfQeJ96UuJ3QbMMNa\",\"is_orig\":false,\"mime_type\":\"text/plain\",\"seen_bytes\":23},{\"charset\":\"us-ascii\",\"depth\":3,\"extract_bytes\":475,\"file_type\":\"body\",\"fuid\":\"L20zB61iepX5Vk1RyXf6F25\",\"is_orig\":false,\"mime_type\":\"text/html\",\"seen_bytes\":475}]` | `extensions_obj.source_private.file_info` | `source_private` |
| `from` | `\"user-a0a2f9f0@example.com\" <user-a0a2f9f0@example.com>` | `facets_obj.email.from` | `confirmed` |
| `fuids` | `L88K1PGfQeJ96UuJ3QbMMNa\|L20zB61iepX5Vk1RyXf6F25` | `extensions_obj.source_private.fuids` | `source_private` |
| `hh` | `09` | `extensions_obj.source_private.hh` | `source_private` |
| `in_reply_to` | `` | `extensions_obj.source_private.in_reply_to` | `source_private` |
| `iptype` | `4` | `extensions_obj.source_private.iptype` | `source_private` |
| `logid` | `47878108509752` | `extensions_obj.source_private.logid` | `source_private` |
| `logtype` | `imap` | `extensions_obj.source_private.logtype` | `source_private` |
| `mime_version` | `1.0` | `extensions_obj.source_private.mime_version` | `source_private` |
| `msg_id` | `<user-adee23e7@example.com>` | `facets_obj.email.message_id` | `confirmed` |
| `receiveds` | `from pc-PC ([192.0.2.186])\t(envelope-sender <user-a0a2f9f0@example.com>)\tby 203.0.113.204 with ESMTP\tfor <user-7289a435@example.com>; Tue, 18 Sep 2018 19:46:26 +0800` | `extensions_obj.source_private.receiveds` | `source_private` |
| `reply_to` | `` | `extensions_obj.source_private.reply_to` | `source_private` |
| `src_ip` | `192.0.2.186` | `roles_obj.source.endpoint.ip` + `source_ip` | `confirmed` |
| `src_port` | `62687` | `roles_obj.source.endpoint.port` | `confirmed` |
| `subject` | `mail_3` | `facets_obj.email.subject` | `confirmed` |
| `to` | `xjj_ser <user-7289a435@example.com>` | `facets_obj.email.to` | `confirmed` |
| `trans_depth` | `1` | `extensions_obj.source_private.trans_depth` | `source_private` |
| `transproto` | `TCP` | `facets_obj.network.protocol.code` | `confirmed` |
| `ts` | `2025-05-22 01:41:48` | `occur_time` | `candidate` |
| `uid` | `3038827477` | `extensions_obj.source_private.uid` | `source_private` |
| `user` | `user-7289a435@example.com` | `roles_obj.source.user.name` | `confirmed` |
| `user_agent` | `Foxmail 7, 2, 6, 40[cn]` | `extensions_obj.source_private.user_agent` | `source_private` |
| `vendor` | `sangfor` | `extensions_obj.source_private.vendor` | `source_private` |
| `x_originating_ip` | `` | `extensions_obj.source_private.x_originating_ip` | `source_private` |

## 人工语义复核（SXF Probe，SR-076）

- 事件事实：探针记录客户端到 IMAP 服务的邮件会话；样本没有明确会话结果。
- `event_category=network`，`event_type=network_connection`，`operation=empty`，`outcome=unknown`。
- 主体/客体/载体：邮件用户（source.user+endpoint）/ IMAP 服务（target.endpoint）/ network_protocol + email
- 邮件会话：`facets.email{from, to, subject, message_id, cc}`；应用 `facets.application.name=IMAP`
- 文档证据：深信服《潜伏威胁探针数据接口对外说明 V2.0》；运行样本已命中。
- 未确认的协议数字/命令字典保留原值并 report。
