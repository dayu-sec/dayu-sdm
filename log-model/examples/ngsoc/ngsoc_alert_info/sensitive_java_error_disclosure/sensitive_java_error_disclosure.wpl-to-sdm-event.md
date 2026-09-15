# WPL -> SDM Event 字段映射

> 样例：`sensitive_java_error_disclosure.expected-sdm-event.json`。机器可读 JSON 记录全部 `67` 个 WPL 字段的处理结论。

## 核心字段

| WPL 来源 | SDM 落位 | 转换 | 说明 |
|---|---|---|---|
| `timestamp` | `occur_time` | 按 Asia/Shanghai 转毫秒 | WPL 输出仍为 chars，使用正文事件时间 |
| `seq` | `source_original_event_id`、`source_finding.original_id` | 直接赋值 | 来源告警序列 |
| `srcIp[0]` | `roles.source.endpoint.ip` | 取唯一值 | 通信主体 |
| `dstIp[0]` | `roles.target.endpoint` | 与唯一 `dport` 组合 | 代表客体，不表达主次 |
| `dstIp[1]` | `roles.related[relation_type=victim]` | 与唯一 `dport` 组合 | 第二个并列受害客体 |
| `victimContent` | `source_finding.entities.victims` | 建立两个 endpoint 引用 | 完整保留来源受害目标集合 |
| `uri` | `facets.http.request.path`、`roles.related[request_authority]` | 拆分 authority/path | 不绑定到两个 dstIp，不推断 scheme 或 method |
| `ruleName` | `source_finding.rules[].name` | 解析多值列表 | `ruleId` 为空也可保存 name-only 多规则 |
| `relevantRuleName` | `extensions.source_private.relevant_rule_name` | 直接赋值 | 关联规则名称，与检测规则名数组分开 |
| `attCk` | `extensions.unmapped.att_ck_original` | 原值保留 | 缺少来源 ATT&CK 技术 ID |

## 映射边界

- 不推断 HTTP 方法、scheme、传输协议、响应、阻断或信息实际泄露。
- 多目标完整保留；代表 target 只解决单值投影，不表达语义主次。
- Meta 和 Content 的逐字段赋值规则见下方生成表。

## 五、WPL/OML 编写规则

> WPL 只负责提取表中的 source 字段；Meta 和 Content 的赋值由 OML 按下表实现。
> `partial` 表示当前只有样例值或局部说明，不能视为完整厂商字典。

### 5.1 Meta 区

| SDM 字段 | 规则类型 | 输入/来源 | 赋值 | 未命中 | 状态与证据 |
|---|---|---|---|---|---|
| `event_id` | `derived` | `derived.sha256(tenant_id+'|'+mapping_id+'|'+wpl.seq)` | `'evt-' + sha256(tenant_id+'|'+mapping_id+'|'+wpl.seq)` -> "evt-7b7e7c9b64acef175fbb40ac9f55e1f255bdcc987f0d8b8c23f2eec82adfd8c6" | `—` | confirmed；来源序列驱动的确定性事件 ID |
| `record_kind` | `conditional` | `when wpl.name == "敏感信息泄露_Java报错信息" && wpl.ruleCategoryName == "信息泄露" && exactly_one(parse_text_list(wpl.srcIp)) == exactly_one(parse_text_list(wpl.attackerContent))` | `when wpl.name == "敏感信息泄露_Java报错信息" && wpl.ruleCategoryName == "信息泄露" && exactly_one(parse_text_list(wpl.srcIp)) == exactly_one(parse_text_list(wpl.attackerContent)) then chars(finding) else no_match` -> "finding" | `no_match` | confirmed；NGSOC 来源告警 |
| `event_domain` | `conditional` | `when wpl.name == "敏感信息泄露_Java报错信息" && wpl.ruleCategoryName == "信息泄露" && exactly_one(parse_text_list(wpl.srcIp)) == exactly_one(parse_text_list(wpl.attackerContent))` | `when wpl.name == "敏感信息泄露_Java报错信息" && wpl.ruleCategoryName == "信息泄露" && exactly_one(parse_text_list(wpl.srcIp)) == exactly_one(parse_text_list(wpl.attackerContent)) then chars(threat) else no_match` -> "threat" | `no_match` | confirmed；来源声明信息泄露风险 |
| `event_type` | `conditional` | `when wpl.name == "敏感信息泄露_Java报错信息" && wpl.ruleCategoryName == "信息泄露" && exactly_one(parse_text_list(wpl.srcIp)) == exactly_one(parse_text_list(wpl.attackerContent)) && exactly_one(parse_text_list(wpl.relevantLogsType)) == "Web入侵事件日志" && exactly_one(parse_authority_path_list(wpl.uri)).path != ""` | `when wpl.name == "敏感信息泄露_Java报错信息" && wpl.ruleCategoryName == "信息泄露" && exactly_one(parse_text_list(wpl.srcIp)) == exactly_one(parse_text_list(wpl.attackerContent)) && exactly_one(parse_text_list(wpl.relevantLogsType)) == "Web入侵事件日志" && exactly_one(parse_authority_path_list(wpl.uri)).path != "" then chars(network_http) else no_match` -> "network_http" | `no_match` | confirmed；Web 入侵日志类型及 authority/path 共同支持 HTTP 请求上下文 |
| `operation` | `conditional` | `when wpl.name == "敏感信息泄露_Java报错信息" && wpl.ruleCategoryName == "信息泄露" && exactly_one(parse_text_list(wpl.srcIp)) == exactly_one(parse_text_list(wpl.attackerContent)) && exactly_one(parse_text_list(wpl.relevantLogsType)) == "Web入侵事件日志" && exactly_one(parse_authority_path_list(wpl.uri)).path != ""` | `when wpl.name == "敏感信息泄露_Java报错信息" && wpl.ruleCategoryName == "信息泄露" && exactly_one(parse_text_list(wpl.srcIp)) == exactly_one(parse_text_list(wpl.attackerContent)) && exactly_one(parse_text_list(wpl.relevantLogsType)) == "Web入侵事件日志" && exactly_one(parse_authority_path_list(wpl.uri)).path != "" then chars() else no_match` -> "" | `no_match` | confirmed；无 HTTP 方法或标准动作证据；仅限当前子类型 |
| `roles.source.ref_id` | `derived` | `derived.entity_ref(endpoint,exactly_one(parse_ip_list(wpl.srcIp)))` | `entity_ref(endpoint,exactly_one(parse_ip_list(wpl.srcIp)))` -> "endpoint-e7a994bd5e80346636e6fe5205280208" | `drop_and_review` | confirmed；源端点稳定引用 |
| `roles.target.ref_id` | `derived` | `derived.entity_ref(endpoint,first(parse_ip_list(wpl.dstIp)),exactly_one(parse_port_list(wpl.dport)))` | `entity_ref(endpoint,first(parse_ip_list(wpl.dstIp)),exactly_one(parse_port_list(wpl.dport)))` -> "endpoint-c98cb08e7b6ff00c661b4b7cf7acead6" | `drop_and_review` | confirmed；首个来源目标作为代表 target，不表达主次 |
| `roles.related[0].ref_id` | `derived` | `derived.entity_ref(endpoint,second(parse_ip_list(wpl.dstIp)),exactly_one(parse_port_list(wpl.dport)))` | `entity_ref(endpoint,second(parse_ip_list(wpl.dstIp)),exactly_one(parse_port_list(wpl.dport)))` -> "endpoint-39cad19f7f3403286bf165961f0b40c0" | `drop_and_review` | confirmed；第二个并列受害目标引用 |
| `roles.related[1].ref_id` | `derived` | `derived.entity_ref(endpoint,authority_ip(wpl.uri),authority_port(wpl.uri))` | `entity_ref(endpoint,authority_ip(wpl.uri),authority_port(wpl.uri))` -> "endpoint-ac47dabbc538bc80b65ee0046fc1df89" | `drop_and_review` | confirmed；URI authority 独立引用 |
| `roles.observer.device.name` | `derived` | `raw_syslog.header.host` | `read(raw_syslog.header.host)` -> "host-2cfba8ce.sdm.example.internal" | `—` | confirmed；Syslog 上报主机 |
| `extensions.source_private.syslog_host` | `derived` | `raw_syslog.header.host` | `read(raw_syslog.header.host)` -> "host-2cfba8ce.sdm.example.internal" | `—` | confirmed；Syslog 主机审计值 |
| `extensions.source_private.syslog_priority` | `derived` | `raw_syslog.header.priority` | `read(raw_syslog.header.priority)` -> 14 | `—` | confirmed；Syslog PRI 审计值 |
| `extensions.source_private.syslog_header_time` | `derived` | `raw_syslog.header.time` | `read(raw_syslog.header.time)` -> "Dec 18 16:01:04" | `—` | confirmed；无年份 Syslog 头时间审计值 |
| `roles.source.entity_type` | `constant` | `constant.roles_source_entity_type` | "endpoint" | `—` | confirmed；源 IP 装配为 endpoint |
| `roles.target.entity_type` | `constant` | `constant.roles_target_entity_type` | "endpoint" | `—` | confirmed；代表目标装配为 endpoint |
| `roles.related[0].entity_type` | `constant` | `constant.roles_related[0]_entity_type` | "endpoint" | `—` | confirmed；额外受害目标装配为 endpoint |
| `roles.related[0].relation_type` | `constant` | `constant.roles_related[0]_relation_type` | "victim" | `—` | confirmed；来源明确声明为受害目标 |
| `roles.related[1].entity_type` | `constant` | `constant.roles_related[1]_entity_type` | "endpoint" | `—` | confirmed；URI authority 装配为 endpoint |
| `roles.related[1].relation_type` | `constant` | `constant.roles_related[1]_relation_type` | "request_authority" | `—` | confirmed；URI authority 与受害 IP 不同 |
| `roles.carriers` | `constant` | `constant.roles_carriers` | [] | `—` | confirmed；无进程、会话或独立协议载体 |
| `roles.observer.product.name` | `constant` | `constant.roles_observer_product_name` | "NGSOC" | `—` | confirmed；来源产品显示名 |
| `roles.observer.device.vendor` | `constant` | `constant.roles_observer_device_vendor` | "qax" | `—` | confirmed；来源厂商 |
| `extensions.schema_version` | `constant` | `constant.extensions_schema_version` | 2 | `—` | confirmed；扩展契约版本 |
| `extensions.profiles` | `constant` | `constant.extensions_profiles` | {} | `—` | confirmed；无平台画像 |
| `extensions.enrichments` | `constant` | `constant.extensions_enrichments` | {} | `—` | confirmed；无平台富化 |
| `source_finding.entities.victims[].entity_type` | `constant` | `constant.source_finding_entities_victimsitems_entity_type` | "endpoint" | `—` | confirmed；受害实体引用类型 |
| `tenant_id` | `context` | `platform_context.tenant_id` | "" | `—` | data_gap；真实平台上下文未提供；运行时赋值 |
| `log_id` | `context` | `platform_context.log_id` | `read(log_id)` | `—` | data_gap；真实平台上下文未提供；运行时赋值 |
| `ingest_time` | `context` | `platform_context.ingest_time` | `read(ingest_time)` | `—` | data_gap；真实平台上下文未提供；运行时赋值 |
| `parse_time` | `context` | `platform_context.parse_time` | `read(parse_time)` | `—` | data_gap；真实平台上下文未提供；运行时赋值 |
| `data_src_instance_id` | `context` | `platform_context.data_src_instance_id` | `read(data_src_instance_id)` | `—` | data_gap；真实平台上下文未提供；运行时赋值 |
| `schema_version` | `constant` | `constant.schema_version` | 2 | `—` | confirmed；日志类型级常量 |
| `mapping_id` | `constant` | `constant.mapping_id` | "qax.ngsoc.ngsoc_alert_info" | `—` | confirmed；日志类型级常量 |
| `data_src_vendor` | `constant` | `constant.data_src_vendor` | "qax" | `—` | confirmed；日志类型级常量 |
| `data_src_product` | `constant` | `constant.data_src_product` | "ngsoc" | `—` | confirmed；日志类型级常量 |
| `data_src_category` | `constant` | `constant.data_src_category` | "security_analytics" | `—` | confirmed；日志类型级常量 |
| `log_type` | `constant` | `constant.log_type` | "ngsoc_alert_info" | `—` | confirmed；日志类型级常量 |
| `log_name` | `constant` | `constant.log_name` | "NGSOC告警信息" | `—` | confirmed；日志类型级常量 |
| `observer_vendor` | `constant` | `constant.observer_vendor` | "qax" | `—` | confirmed；日志类型级常量 |
| `observer_product` | `constant` | `constant.observer_product` | "ngsoc" | `—` | confirmed；日志类型级常量 |
| `log_level` | `dictionary` | `derived.syslog_severity_code(raw_syslog.header.priority)` | 0 -> "emerg", 1 -> "alert", 2 -> "crit", 3 -> "error", 4 -> "warning", 5 -> "notice", 6 -> "info", 7 -> "debug" | `null_and_review` | confirmed；Syslog PRI 的低 3 位表示来源日志等级，不是 finding 安全严重度 |

### 5.2 Content 区

| SDM 字段 | 规则类型 | WPL 字段 | 映射/赋值 | 未命中 | 状态与证据 |
|---|---|---|---|---|---|
| `occur_time` | `transform` | `timestamp` | `parse_time_ms(wpl.timestamp,'Asia/Shanghai')` -> 1734483774000 | `drop_and_review` | confirmed；WPL 输出仍为 chars；SDM 装配转换为毫秒 |
| `source_original_event_id` | `projection` | `seq` | "12934417" | `—` | confirmed；来源告警序列热字段 |
| `source_finding.original_id` | `projection` | `seq` | "12934417" | `—` | confirmed；来源 finding 原始 ID |
| `roles.source.endpoint.ip` | `transform` | `srcIp` | `exactly_one(parse_ip_list(wpl.srcIp))` -> "192.0.2.203" | `drop_and_review` | confirmed；单一通信源 IP |
| `source_ip` | `projection` | `roles.source.endpoint.ip` | "192.0.2.203" | `—` | confirmed；源 IP 热字段 |
| `roles.target.endpoint.ip` | `transform` | `dstIp[0]` | `first(parse_ip_list(wpl.dstIp))` -> "192.0.2.238" | `drop_and_review` | confirmed；来源顺序首项作为代表目标，不表达主次 |
| `target_ip` | `projection` | `roles.target.endpoint.ip` | "192.0.2.238" | `—` | confirmed；代表目标热字段 |
| `roles.related[0].endpoint.ip` | `transform` | `dstIp[1]` | `second(parse_ip_list(wpl.dstIp))` -> "203.0.113.108" | `drop_and_review` | confirmed；第二个并列受害目标 |
| `roles.target.endpoint.port` | `transform` | `dport` | `exactly_one(parse_port_list(wpl.dport))` -> 9090 | `drop_and_review` | confirmed；唯一目标端口 |
| `target_port` | `projection` | `roles.target.endpoint.port` | 9090 | `—` | confirmed；代表目标端口热字段 |
| `roles.related[0].endpoint.port` | `transform` | `dport` | `exactly_one(parse_port_list(wpl.dport))` -> 9090 | `omit_and_review` | confirmed；并列受害目标共用来源唯一目标端口 |
| `roles.related[1].endpoint.ip` | `transform` | `uri` | `authority_ip(exactly_one(parse_authority_path_list(wpl.uri)))` -> "192.0.2.169" | `omit_and_review` | confirmed；URI authority 与 dstIp 分开 |
| `roles.related[1].endpoint.port` | `transform` | `uri` | `authority_port(exactly_one(parse_authority_path_list(wpl.uri)))` -> 9090 | `omit_and_review` | confirmed；URI authority 端口 |
| `facets.http.request.path` | `transform` | `uri` | `path(exactly_one(parse_authority_path_list(wpl.uri)))` -> "/service/api/resopencard/updateResOpenCradStatu" | `omit_and_review` | confirmed；只提取路径，不推断 scheme 或 method |
| `extensions.source_private.request_targets` | `transform` | `uri` | `parse_text_list(wpl.uri)` -> ["192.0.2.169:9090/service/api/resopencard/updateResOpenCradStatu"] | `preserve_raw_and_review` | confirmed；保留来源完整请求目标 |
| `extensions.source_private.source_ports` | `transform` | `sport` | `parse_port_list(wpl.sport)` -> [60940, 32792, 57288, 36068, 59824, 38876, 33244, 40248, 35512, 36076] | `drop_invalid_items_and_review` | confirmed；保留聚合源端口；不生成 source_port |
| `source_finding.title` | `projection` | `name` | "敏感信息泄露_Java报错信息" | `—` | confirmed；来源告警标题 |
| `source_finding.severity` | `projection` | `severity` | "高危" | `—` | confirmed；来源严重度 |
| `source_finding.status` | `projection` | `disposeState` | "待处置" | `—` | confirmed；来源处置状态；未做字典归一 |
| `source_finding.count` | `transform` | `times` | `to_int(wpl.times)` -> 121 | `omit_and_review` | confirmed；聚合命中次数 |
| `source_finding.confidence` | `projection` | `confidence` | "高" | `—` | confirmed；来源置信度 |
| `source_finding.category.original.name` | `projection` | `ruleCategoryName` | "信息泄露" | `—` | confirmed；来源分类 |
| `source_finding.attacker.endpoint.ip` | `transform` | `attackerContent` | `exactly_one(parse_ip_list(wpl.attackerContent))` -> "192.0.2.203" | `omit_and_review` | confirmed；来源攻击方声明，与通信角色分开 |
| `source_finding.victim.endpoint.ip` | `transform` | `victimContent[0]` | `first(parse_ip_list(wpl.victimContent))` -> "192.0.2.238" | `omit_and_review` | confirmed；单值 victim 使用首个来源目标，不表达主次 |
| `source_finding.victim.endpoint.port` | `transform` | `dport` | `exactly_one(parse_port_list(wpl.dport))` -> 9090 | `omit_and_review` | confirmed；来源受害方端口 |
| `source_finding.entities.victims[].ref_id` | `transform` | `victimContent/dport` | `map(entity_ref(endpoint,item,exactly_one(parse_port_list(wpl.dport))),parse_ip_list(wpl.victimContent))` -> ["endpoint-c98cb08e7b6ff00c661b4b7cf7acead6", "endpoint-39cad19f7f3403286bf165961f0b40c0"] | `drop_invalid_items_and_review` | confirmed；完整保留两个并列受害目标 |
| `source_finding.attention.content` | `projection` | `attentionValue` | "目的IP : 192.0.2.238 ,  203.0.113.108" | `—` | confirmed；来源关注内容 |
| `source_finding.behavior` | `conditional` | `name/ruleCategoryName` | `when wpl.name == "敏感信息泄露_Java报错信息" && wpl.ruleCategoryName == "信息泄露" && exactly_one(parse_text_list(wpl.srcIp)) == exactly_one(parse_text_list(wpl.attackerContent)) then chars(information_disclosure) else omit` -> "information_disclosure" | `omit` | confirmed；来源明确声明信息泄露检测，不表示实际泄露 |
| `extensions.source_private.information_disclosure_variant` | `conditional` | `name` | `when wpl.name == "敏感信息泄露_Java报错信息" && wpl.ruleCategoryName == "信息泄露" && exactly_one(parse_text_list(wpl.srcIp)) == exactly_one(parse_text_list(wpl.attackerContent)) then chars(java_error_message) else omit` -> "java_error_message" | `omit` | confirmed；告警标题确认 Java 报错信息变体 |
| `source_finding.rules[].name` | `transform` | `ruleName` | `map(name,parse_text_list(wpl.ruleName))` -> ["敏感信息泄露_Java报错信息", "敏感信息泄露_Oracle_SQL错误信息"] | `drop_invalid_items_and_review` | confirmed；ruleId 为空但规则名为多值，建立标准多规则数组 |
| `extensions.source_private.relevant_rule_name` | `projection` | `relevantRuleName` | "预置-WEB安全事件-敏感信息泄露" | `—` | confirmed；关联规则名与检测规则名数组分开 |
| `facets.network.direction` | `dictionary` | `commDirection` | "内到内" -> "L2L" | `preserve_in_extension_and_review` | partial；当前样例值映射 |
| `extensions.unmapped.att_ck_original` | `projection` | `attCk` | "[利用面向公众的应用程序]" | `—` | confirmed；来源没有 ATT&CK 技术 ID，不根据中文名称推断编号 |
| `extensions.source_private.wpl_update_time` | `projection` | `update_time` | "2026-12-18 16:01:04" | `—` | confirmed；WPL 从无年份 Syslog 头推断，仅供审计 |
| `extensions.source_private.latest_timestamp` | `projection` | `latestTimestamp` | 1734508620000 | `—` | confirmed；WPL 已转毫秒 |
| `extensions.source_private.occur_days` | `transform` | `occurDays` | `to_int(wpl.occurDays)` -> 3 | `—` | confirmed；来源持续天数 |
| `extensions.source_private.relevant_log_types` | `transform` | `relevantLogsType` | `parse_text_list(wpl.relevantLogsType)` -> ["Web入侵事件日志"] | `preserve_raw_and_review` | confirmed；来源关联日志类型 |
| `extensions.source_private.relevant_asset_names` | `transform` | `relevantAssetsName` | `parse_text_list(wpl.relevantAssetsName)` -> ["示例集团移动银行系统", "天清Web应用网关（WAF1）"] | `preserve_raw_and_review` | confirmed；来源关联资产名称 |
| `extensions.source_private.relevant_asset_groups` | `transform` | `relevantAssetsGroup` | `parse_text_list(wpl.relevantAssetsGroup)` -> ["互联网业务区", "已删除", "示例集团", "运维管理区"] | `preserve_raw_and_review` | confirmed；来源关联资产组 |
| `extensions.source_private.relevant_network_segments` | `transform` | `relevantNetworkSegmentId` | `parse_text_list(wpl.relevantNetworkSegmentId)` -> ["互联网业务区", "运维管理区"] | `preserve_raw_and_review` | confirmed；来源关联网络分区 |
| `source_alert_severity` | `transform` | `severity` | `string` -> "高危" | `—` | confirmed；保留来源 finding 原始严重度 |
| `severity` | `dictionary` | `severity` | "高危" -> "error" | `null_and_review` | partial；根据当前 NGSOC 样例分布推测的安全严重度交叉表，尚未经厂商确认 |
| `outcome` | `gap` | `data_gap.no_action_result` | "unknown" | `unknown` | missing；原始日志没有明确的底层动作结果字段或事件事实 |

### 5.3 编写约束

- roles.target 按来源数组顺序选择第一个受害 IP 作为代表目标，不表达主次；第二个进入 related，完整列表进入 source_finding.entities.victims。
- URI authority 192.0.2.169:9090 与两个 dstIp 均不同，作为 request_authority 关联端点只建一次，不建立未经证实的绑定。
- ruleId 为空且 ruleName 有两个值，使用 source_finding.rules[].name 保存标准多规则数组；relevantRuleName 单独保存在 source_private。
- 不推断 HTTP method、scheme、传输协议、响应、阻断或信息实际泄露。
