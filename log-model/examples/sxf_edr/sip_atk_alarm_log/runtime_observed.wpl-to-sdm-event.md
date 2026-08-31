# sxf_edr / sip_atk_alarm_log 运行时观测候选映射

事件事实：深信服 SIP 攻击告警（口令暴力破解/账号攻击）——攻击源对受害资产 Asset1(198.51.100.25) 发起攻击，命中自定义威胁情报。检测声明在 source_finding。

主体：攻击源（source.endpoint=attack_ip）；客体：受害资产（target.host=suffer_branch_name/suffer_ip + target.endpoint）；载体：`none`；观察者：来源产品。

> 状态：candidate，未注册、未批准。WPL 解析事实与深信服 SIP 文档已确认；SR-061 人工复核结论见文末。

| WPL 字段 | 值 | SDM 候选路径 | 状态 |
|---|---|---|---|
| `time` | `2022-01-26 10:11:18.468356` | `extensions_obj.source_private.time` | `source_private` |
| `time2` | `2022-01-26 10:12:15` | `extensions_obj.source_private.time2` | `source_private` |
| `symbol` | `alarm` | `extensions_obj.source_private.symbol` | `source_private` |
| `access_ip` | `192.0.2.8` | `extensions_obj.source_private.access_ip` | `source_private` |
| `alert_id` | `2141000061` | `event_id` | `candidate` |
| `analyze_suggest` | `1.通过深信服威胁情报中心（https://sec.sangfor.com.cn/analysis-platform）查看情报详情。\\2.如已部署深信服终端安全产品（深信服>终端安全 EDR），推荐配置联动功能，EDR 产品病毒检测日志可上报到 SIP 平台进行处置响应，并可对终端下发联动扫描，https://edr.sangfor.com.cn/#/introduction/edr，如未部署深信服终端安全产品>（深信服终端安全 EDR），推荐使用深信服病毒专杀工具进行病毒查杀，https://edr.sangfor.com.cn/#/introduction/bot_net。\\3.如果 EDR以及其他杀软没有排查到可疑文件，可以通过内存分析工具定位到请求恶意情报的进程并进一步分析进程是否可疑。` | `extensions_obj.source_private.analyze_suggest` | `source_private` |
| `asset_direction` | `1` | `extensions_obj.source_private.asset_direction` | `source_private` |
| `attack_asset_id` | `0` | `extensions_obj.source_private.attack_asset_id` | `source_private` |
| `attack_branch_id` | `0` | `extensions_obj.source_private.attack_branch_id` | `source_private` |
| `attack_branch_name` | `` | `extensions_obj.source_private.attack_branch_name` | `source_private` |
| `attack_classify1_id` | `0` | `extensions_obj.source_private.attack_classify1_id` | `source_private` |
| `attack_classify1_id_name` | `未知` | `extensions_obj.source_private.attack_classify1_id_name` | `source_private` |
| `attack_classify_id` | `0` | `extensions_obj.source_private.attack_classify_id` | `source_private` |
| `attack_country` | `未知` | `extensions_obj.source_private.attack_country` | `source_private` |
| `attack_direction` | `2` | `extensions_obj.source_private.attack_direction` | `source_private` |
| `attack_ip` | `0.0.0.0` | `roles_obj.source.endpoint.ip` + `source_ip` | `confirmed` |
| `attack_port` | `0` | `extensions_obj.source_private.attack_port` | `source_private` |
| `attack_province` | `未知` | `extensions_obj.source_private.attack_province` | `source_private` |
| `attack_state` | `3` | `extensions_obj.source_private.attack_state` | `source_private` |
| `attack_type` | `2` | `extensions_obj.source_private.attack_type` | `source_private` |
| `attack_type_name` | `账号爆破` | `extensions_obj.source_private.attack_type_name` | `source_private` |
| `brief` | `自定义威胁情报` | `source_finding_obj.title` | `confirmed` |
| `count` | `1` | `extensions_obj.source_private.count` | `source_private` |
| `created_at` | `1643163099` | `extensions_obj.source_private.created_at` | `source_private` |
| `damage` | `` | `extensions_obj.source_private.damage` | `source_private` |
| `dev_id` | `1740D4E7` | `extensions_obj.source_private.dev_id` | `source_private` |
| `dev_name_ori` | `感知平台数据构造平台(198.51.100.179)` | `extensions_obj.source_private.dev_name_ori` | `source_private` |
| `emergency` | `important` | `source_finding_obj.severity` | `confirmed` |
| `engine` | `自定义威胁情报库` | `extensions_obj.source_private.engine` | `source_private` |
| `event_desc` | `命中自定义威胁情报指标` | `extensions_obj.source_private.event_desc` | `source_private` |
| `event_evidence` | `具体情报: www.61house.com 解析 IP: - 情报标签: [u'\\u81ea\\u5b9a\\u4e49-Telnet\\u8d26\\u53f7\\u7206\\u7834']` | `extensions_obj.source_private.event_evidence` | `source_private` |
| `first_time` | `2022-01-26 02:11:29` | `extensions_obj.source_private.first_time` | `source_private` |
| `hash_id` | `81b896841bbefd342beb3706ae0d0a14` | `extensions_obj.source_private.hash_id` | `source_private` |
| `invasion_stage` | `6` | `extensions_obj.source_private.invasion_stage` | `source_private` |
| `ioc` | `[FieldStorage { cur_name: None, value: Owned(Field { meta: Chars, name: "ioc", value: Chars("www.61house.com") }) }]` | `extensions_obj.source_private.ioc` | `source_private` |
| `is_read` | `0` | `extensions_obj.source_private.is_read` | `source_private` |
| `is_white` | `0` | `extensions_obj.source_private.is_white` | `source_private` |
| `last_time` | `1643163089` | `extensions_obj.source_private.last_time` | `source_private` |
| `linkage_status` | `0` | `extensions_obj.source_private.linkage_status` | `source_private` |
| `mining_stage` | `0` | `extensions_obj.source_private.mining_stage` | `source_private` |
| `misreport` | `0` | `extensions_obj.source_private.misreport` | `source_private` |
| `module_type` | `204` | `extensions_obj.source_private.module_type` | `source_private` |
| `module_type_name` | `账号攻击` | `extensions_obj.source_private.module_type_name` | `source_private` |
| `multi_deal_status` | `0` | `extensions_obj.source_private.multi_deal_status` | `source_private` |
| `net_action` | `0` | `extensions_obj.source_private.net_action` | `source_private` |
| `principle` | `` | `extensions_obj.source_private.principle` | `source_private` |
| `record_date` | `20220126` | `extensions_obj.source_private.record_date` | `source_private` |
| `relation` | `{\"cond\":{\"hole_id\":\"${hole_ids}\",\"src_asset_id\":\"${suffer_asset_id}\"},\"from\":\"ngfw.security\",\"type\":\"es\"}` | `extensions_obj.source_private.relation` | `source_private` |
| `reliability` | `3` | `extensions_obj.source_private.reliability` | `source_private` |
| `sub_attack_type` | `1` | `extensions_obj.source_private.sub_attack_type` | `source_private` |
| `sub_attack_type_name` | `口令暴力破解` | `source_finding_obj.rule.name` | `confirmed` |
| `suffer_asset_id` | `5` | `extensions_obj.source_private.suffer_asset_id` | `source_private` |
| `suffer_branch_id` | `16` | `extensions_obj.source_private.suffer_branch_id` | `source_private` |
| `suffer_branch_name` | `Asset1` | `roles_obj.target.host.name` | `confirmed` |
| `suffer_classify1_id` | `1` | `extensions_obj.source_private.suffer_classify1_id` | `source_private` |
| `suffer_classify1_id_name` | `服务器` | `extensions_obj.source_private.suffer_classify1_id_name` | `source_private` |
| `suffer_classify_id` | `10000` | `extensions_obj.source_private.suffer_classify_id` | `source_private` |
| `suffer_country` | `未知` | `extensions_obj.source_private.suffer_country` | `source_private` |
| `suffer_ip` | `198.51.100.25` | `roles_obj.target.host.ip` + `target_ip` | `confirmed` |
| `suffer_port` | `58669` | `roles_obj.target.endpoint.port` | `confirmed` |
| `suffer_province` | `未知` | `extensions_obj.source_private.suffer_province` | `source_private` |
| `suggest` | `1、确认该主机是否是正常业务需要，如果是，将该主机 IP 添加到全局白名单即可；\\2、确认该行为是否内部同事人为操作，如果是，根据组织内部规章制度进行处理；\\3、排除以上两种情况，则该主机可能已被黑客控制沦为肉鸡，可参考以下方法处理：\\（1）不要打开来自未知或未经证明的发件人的电子邮件，不要运行邮件中的附件文件；\\（2）不要点击电子邮件中的不明链接，用户访问之前可以先检查网站信誉；\\（3）请注意备份重要文档。备份的最佳做法是采取 3-2-1 规则，即至少做三个副本，用两种不同格式保存，并将副本放在异地存储。\\推荐杀毒软件：\\<ahref=\"http://edr.sangfor.com.cn/tool/SfabAntiBot.zip\"target=\"_blank\">http://edr.sangfor.com.cn/tool/SfabAntiBot.zip</a>；` | `extensions_obj.source_private.suggest` | `source_private` |
| `tags` | `命中自定义威胁情报指标` | `extensions_obj.source_private.tags` | `source_private` |
| `updated_at` | `1643163099` | `extensions_obj.source_private.updated_at` | `source_private` |

## 人工语义复核（SXF EDR，SR-061）

- 事件事实：深信服 SIP 记录攻击告警，攻击源与受害资产支持网络连接观察。
- `event_category=alert`，`event_type=network_connection`，`outcome=unknown`。
- 主体/客体/载体：攻击源（source.endpoint）/ 受害资产（target.host+endpoint）/ none
- 检测声明：`source_finding_obj`（title/severity/count/rule）
- 来源告警等级保留在 `source_finding`，不机械投影顶层 severity。
- 文档证据：深信服 SIP syslog 格式说明 77 版本；WPL 样本已命中。
