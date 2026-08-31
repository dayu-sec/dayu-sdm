# sxf_probe / flow_mail SDM2 候选样例

事件事实：探针邮件会话（logtype=imap）——用户 xjj_ser@sip.com（192.0.2.186:62687）访问 IMAP 服务 203.0.113.204:143，邮件 mail_3（发件人 xjj1@sip.com，Foxmail）。

- 主体：邮件用户 → `roles.source.user{name=xjj_ser@sip.com}` + `source.endpoint(192.0.2.186:62687)`
- 客体：IMAP 服务 → `roles.target.endpoint(203.0.113.204:143)`
- 载体：网络协议 → `facets.network.protocol.code=TCP`；应用 → `facets.application.name=IMAP`；邮件 → `facets.email{from, to, subject, message_id, cc}`
- 观察者：来源安全产品

## 证据与限制

- 原始样本：`s4-doris/models/wpl/sxf_probe/sample.dat` 第 6 个非空行。
- WPL 规则：`flow_mail`，运行时解析成功。
- 字段映射和枚举为候选，未知枚举保留原值并报告。
- `outcome=unknown`；样本没有明确会话结果。
- `source_finding_obj=null`：邮件会话审计，非检测告警。

## 人工语义复核（深信服探针文档，SR-076）

- 事件事实：探针记录客户端到 IMAP 服务的邮件会话；样本没有明确会话结果。
- event_category：`network`
- event_type：`network_connection`
- operation：`空`
- outcome：`unknown`（无明确会话结果）
- 主体/客体/载体：邮件用户（source.user+endpoint）/ IMAP 服务（target.endpoint）/ network_protocol + email
- 邮件会话：`facets.email{from, to, subject, message_id, cc}`；应用 `facets.application.name=IMAP`
- 文档证据：深信服《潜伏威胁探针数据接口对外说明 V2.0》；运行样本已命中。
- 未确认的协议数字/命令字典保留原值并 report。

## 当前物理注册表迁移

- expected 已按当前 `sdm_event.yaml` 87 字段物理注册表收敛。
- 邮件用户入 `roles.source.user+endpoint`；IMAP 服务入 `roles.target.endpoint`。
- 邮件会话入 `facets.email`；应用入 `facets.application.name`；协议入 `facets.network.protocol`；source_finding_obj=null。
