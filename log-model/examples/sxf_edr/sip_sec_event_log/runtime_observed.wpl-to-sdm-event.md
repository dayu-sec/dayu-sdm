# sxf_edr / sip_sec_event_log 运行时观测候选映射

事件事实：深信服 SIP 安全事件（secevent）——主机 Asset1(198.51.100.25) 访问 Petya 勒索病毒通信域名，感染恶意文件。检测声明在 source_finding。

主体：受感染主机（source.host=branch_name/ip）；客体：Petya C2（source_finding，target=null）；载体：`none`；观察者：来源产品。

> 状态：candidate，未注册、未批准。WPL 解析事实与深信服 SIP 文档已确认；SR-062 人工复核结论见文末。

| WPL 字段 | 值 | SDM 候选路径 | 状态 |
|---|---|---|---|
| `time` | `2021-07-08 10:18:00` | `extensions_obj.source_private.time` | `source_private` |
| `symbol` | `secevent` | `extensions_obj.source_private.symbol` | `source_private` |
| `access_ip` | `192.0.2.103` | `extensions_obj.source_private.access_ip` | `source_private` |
| `asset_id` | `5` | `extensions_obj.source_private.asset_id` | `source_private` |
| `attachment` | `` | `extensions_obj.source_private.attachment` | `source_private` |
| `attack_count` | `0` | `extensions_obj.source_private.attack_count` | `source_private` |
| `attack_state` | `0` | `extensions_obj.source_private.attack_state` | `source_private` |
| `attack_time` | `` | `extensions_obj.source_private.attack_time` | `source_private` |
| `branchId` | `17` | `extensions_obj.source_private.branchId` | `source_private` |
| `branch_name` | `Asset1` | `roles_obj.source.host.name` | `confirmed` |
| `brief` | `主机访问了 Petya 勒索病毒通信域名` | `source_finding_obj.title` | `confirmed` |
| `classify1_id` | `` | `extensions_obj.source_private.classify1_id` | `source_private` |
| `classify_id` | `` | `extensions_obj.source_private.classify_id` | `source_private` |
| `count` | `2` | `extensions_obj.source_private.count` | `source_private` |
| `data_collection_size` | `` | `extensions_obj.source_private.data_collection_size` | `source_private` |
| `data_collection_time` | `` | `extensions_obj.source_private.data_collection_time` | `source_private` |
| `dealStatus` | `` | `extensions_obj.source_private.dealStatus` | `source_private` |
| `detectEngine` | `安全日志分析引擎` | `extensions_obj.source_private.detectEngine` | `source_private` |
| `directory_browsing` | `` | `extensions_obj.source_private.directory_browsing` | `source_private` |
| `domain_name` | `` | `extensions_obj.source_private.domain_name` | `source_private` |
| `downstream_traffic` | `` | `extensions_obj.source_private.downstream_traffic` | `source_private` |
| `dst_host` | `` | `extensions_obj.source_private.dst_host` | `source_private` |
| `dst_ip` | `198.51.100.25` | `target_ip` | `candidate` |
| `dst_mac_addr` | `` | `extensions_obj.source_private.dst_mac_addr` | `source_private` |
| `dst_port` | `0` | `target_port` | `candidate` |
| `email_from` | `` | `extensions_obj.source_private.email_from` | `source_private` |
| `email_to` | `` | `extensions_obj.source_private.email_to` | `source_private` |
| `emergency` | `emergent` | `source_finding_obj.severity` | `confirmed` |
| `eventKey` | `117830036` | `extensions_obj.source_private.eventKey` | `source_private` |
| `eventType` | `1` | `extensions_obj.source_private.eventType` | `source_private` |
| `event_content` | `主机访问了 Petya 勒索病毒通信域名` | `extensions_obj.source_private.event_content` | `source_private` |
| `event_evidence` | `` | `extensions_obj.source_private.event_evidence` | `source_private` |
| `firstTime` | `1625553809` | `extensions_obj.source_private.firstTime` | `source_private` |
| `hostName` | `` | `extensions_obj.source_private.hostName` | `source_private` |
| `hostRisk` | `198.51.100.25(Asset1)` | `extensions_obj.source_private.hostRisk` | `source_private` |
| `ip` | `198.51.100.25` | `roles_obj.source.host.ip` + `target_ip` | `confirmed` |
| `log_time` | `2021-07-06 06:43:29` | `extensions_obj.source_private.log_time` | `source_private` |
| `module_name` | `感染恶意文件` | `extensions_obj.source_private.module_name` | `source_private` |
| `msg_count` | `` | `extensions_obj.source_private.msg_count` | `source_private` |
| `msg_sub_type` | `4` | `extensions_obj.source_private.msg_sub_type` | `source_private` |
| `msg_type` | `209` | `extensions_obj.source_private.msg_type` | `source_private` |
| `multi_deal_status` | `0` | `extensions_obj.source_private.multi_deal_status` | `source_private` |
| `password_autofill` | `` | `extensions_obj.source_private.password_autofill` | `source_private` |
| `phishing_link` | `` | `extensions_obj.source_private.phishing_link` | `source_private` |
| `principle` | `Petya 勒索病毒釆用（CVE-2017-0199) RTF 漏洞进行钓鱼攻击，通过 EternalBlue（永恒之蓝）和 EternalRomance（永恒浪漫）漏洞横向传播，用户一旦感染，病毒会修改系统的 MBR 引导扇区，当电脑重启时，病毒代码会在 Windows 操作系统之前接管电脑，执行加密等恶意操作。当加密完成后，病毒要求受害者支付价值 300 美元的比特币之后，才会回复解密密钥。` | `extensions_obj.source_private.principle` | `source_private` |
| `recordDate` | `20210706` | `extensions_obj.source_private.recordDate` | `source_private` |
| `role` | `2` | `extensions_obj.source_private.role` | `source_private` |
| `rsp_email` | `` | `extensions_obj.source_private.rsp_email` | `source_private` |
| `ruleId` | `117830036` | `extensions_obj.source_private.ruleId` | `source_private` |
| `scan_count` | `0` | `extensions_obj.source_private.scan_count` | `source_private` |
| `scan_success` | `` | `extensions_obj.source_private.scan_success` | `source_private` |
| `scan_time` | `` | `extensions_obj.source_private.scan_time` | `source_private` |
| `server_sensative_directory` | `` | `extensions_obj.source_private.server_sensative_directory` | `source_private` |
| `session_token` | `` | `extensions_obj.source_private.session_token` | `source_private` |
| `solution` | `1、确认该主机是否为 DNS 服务器或域控服务器（DNS 代理），如果是请将该主机 IP 添加到失陷主机白名单即可；2、推荐使用深信服 EDR 专杀工具进行病毒查杀：<a href=\"http://edr.sangfor.com.cn/tool/SfabAntiBot.zip\"target=\"_blank\">http://edr.sangfor.com.cn/tool/SfabAntiBot.zip</a>3 、 如 以 上 推 荐 工 具 查 杀 不 出 来 ， 可 使 用 第 三 方 杀 毒 工 具 进 行 查 杀 ； 加 固 建 议 ： 1 、 下 载 安 装 补 丁 ： <a href=\"https://docs.microsoft.com/zh-cn/security-updates/securitybulletins/2017/ms17-010\" target=\"_blank\">https://docs.microsoft.com/zh-cn/security-updates/securitybulletins/2017/ms17-010</a> 日常维护：1、如无业务需要，建议关闭文件共享端口（139、445）；2、及时更新系统补丁，可以使用 windows 自动更新或采用腾讯管家等进行更新；3、对重要数据进行定期非本地备份；` | `extensions_obj.source_private.solution` | `source_private` |
| `src_host` | `` | `extensions_obj.source_private.src_host` | `source_private` |
| `src_ip` | `203.0.113.73` | `source_ip` | `candidate` |
| `src_mac_addr` | `` | `extensions_obj.source_private.src_mac_addr` | `source_private` |
| `src_port` | `0` | `source_port` | `candidate` |
| `stage` | `4` | `extensions_obj.source_private.stage` | `source_private` |
| `sub_attack_name` | `勒索` | `source_finding_obj.rule.name` | `confirmed` |
| `sub_attack_type` | `0` | `extensions_obj.source_private.sub_attack_type` | `source_private` |
| `sub_attack_type_name` | `` | `extensions_obj.source_private.sub_attack_type_name` | `source_private` |
| `suspect_level` | `2` | `severity` | `candidate` |
| `tampered_url` | `` | `extensions_obj.source_private.tampered_url` | `source_private` |
| `threat_level` | `3` | `severity` | `candidate` |
| `upstream_traffic` | `` | `extensions_obj.source_private.upstream_traffic` | `source_private` |
| `url` | `` | `extensions_obj.source_private.url` | `source_private` |
| `vulnerability_description` | `` | `extensions_obj.source_private.vulnerability_description` | `source_private` |
| `vulnerability_name` | `` | `extensions_obj.source_private.vulnerability_name` | `source_private` |

## 人工语义复核（SXF EDR，SR-062）

- 事件事实：深信服 SIP 记录安全事件，具体底层动作未由样本确认。
- `event_category=alert`，`event_type=network_connection`，`outcome=unknown`。
- 主体/客体/载体：受感染主机（source.host）/ Petya C2（source_finding，target=null）/ none
- 检测声明：`source_finding_obj`（title/severity/count/rule）
- 来源告警等级保留在 `source_finding`，不机械投影顶层 severity。
- 文档证据：深信服 SIP syslog 格式说明 77 版本；WPL 样本已命中。
