# WPL -> SDM Event 字段映射

> 样例：`injecto_activity.expected-sdm-event.behavior.json（现行）；旧 `*.expected-sdm-event.json` 为 55 列对照`。机器可读 JSON 记录全部 `67` 个 WPL 字段的处理结论。

## 核心字段

| WPL 来源 | SDM 落位 | 转换 | 说明 |
|---|---|---|---|
| `timestamp` | `occur_time` | 按 Asia/Shanghai 转毫秒 | WPL 实际输出仍为 chars，使用正文事件时间 |
| `seq` | `source_original_event_id`、`source_finding.original_id` | 直接赋值 | 来源告警序列 |
| `srcIp[0]` | `roles.source.endpoint.ip` | 取唯一值 | 通信主体 |
| `dstIp[0]` | `roles.target.endpoint.ip` | 取唯一值 | DNS 通信对端，无端口证据 |
| `victimContent` | `source_finding.victim.endpoint.ip` | 取唯一值 | 来源受害主机声明 |
| `domain` | `facets.dns.question.name`、`roles.related[].domain.name` | 解析单一域名 | DNS/IOC 域名 |
| `ioc/iocType` | `source_finding.ioc` | 分别取唯一值 | 来源 IOC |
| `maliciousFamily` | `source_finding.malware.name` | 取唯一值 | 恶意家族 |
| `sipGeo` | `source_finding.victim.geo` | 按 victim IP 取值 | 受害主机 Geo |
| `ruleName` | `source_finding.rule.label` | 取唯一值 | `ruleId` 为空，不伪造 ID |
| `relevantRuleName` | `extensions.source_private.relevant_rule_name` | 直接赋值 | 关联规则名称，不覆盖检测规则名称 |
| `attCk` | `extensions.unmapped.att_ck_original` | 原值保留 | 不是 ATT&CK 技术 ID |

## 映射边界

- 不推断 DNS 应答、TCP/UDP、阻断或远控连接成功。
- `domain/protocol/...` 虽呈括号列表文本，但必须按字段语义解析。
- Meta 和 Content 的逐字段赋值规则见下方生成表。

## 五、WPL/OML 编写规则

> WPL 只负责提取表中的 source 字段；Meta 和 Content 的赋值由 OML 按下表实现。
> `partial` 表示当前只有样例值或局部说明，不能视为完整厂商字典。

### 5.1 Meta 区

| SDM 字段 | 规则类型 | 输入/来源 | 赋值 | 未命中 | 状态与证据 |
|---|---|---|---|---|---|
| `event_id` | `derived` | `derived.sha256(tenant_id+'|'+mapping_id+'|'+wpl.seq)` | `'evt-' + sha256(tenant_id+'|'+mapping_id+'|'+wpl.seq)` -> "evt-5175f83843c873cab87682304fc49a09389c26b31b8fe4320a974835d0e2e662" | `—` | confirmed；来源序列驱动的确定性事件 ID |
| `record_kind` | `conditional` | `when wpl.name == "Injecto远控木马活动事件" && wpl.ruleCategoryName == "远控木马"` | `when wpl.name == "Injecto远控木马活动事件" && wpl.ruleCategoryName == "远控木马" then chars(finding) else no_match` -> "finding" | `no_match` | confirmed；NGSOC 来源告警 |
| `event_domain` | `conditional` | `when wpl.name == "Injecto远控木马活动事件" && wpl.ruleCategoryName == "远控木马"` | `when wpl.name == "Injecto远控木马活动事件" && wpl.ruleCategoryName == "远控木马" then chars(threat) else no_match` -> "threat" | `no_match` | confirmed；来源远控木马检测声明 |
| `event_type` | `conditional` | `when wpl.name == "Injecto远控木马活动事件" && wpl.ruleCategoryName == "远控木马" && exactly_one(parse_text_list(wpl.protocol)) == "DNS" && exactly_one(parse_domain_list(wpl.domain)) == "a-gwas-01.dyndns.org"` | `when wpl.name == "Injecto远控木马活动事件" && wpl.ruleCategoryName == "远控木马" && exactly_one(parse_text_list(wpl.protocol)) == "DNS" && exactly_one(parse_domain_list(wpl.domain)) == "a-gwas-01.dyndns.org" then chars(network_dns) else no_match` -> "network_dns" | `no_match` | confirmed；protocol=DNS 且 domain 提供单一域名 |
| `operation` | `conditional` | `when wpl.name == "Injecto远控木马活动事件" && wpl.ruleCategoryName == "远控木马" && exactly_one(parse_text_list(wpl.protocol)) == "DNS" && exactly_one(parse_domain_list(wpl.domain)) == "a-gwas-01.dyndns.org"` | `when wpl.name == "Injecto远控木马活动事件" && wpl.ruleCategoryName == "远控木马" && exactly_one(parse_text_list(wpl.protocol)) == "DNS" && exactly_one(parse_domain_list(wpl.domain)) == "a-gwas-01.dyndns.org" then chars(query) else no_match` -> "query" | `no_match` | confirmed；DNS 协议与单一 domain 字段共同支持域名查询语义 |
| `roles.source.ref_id` | `derived` | `derived.entity_ref(endpoint,exactly_one(parse_ip_list(wpl.srcIp)))` | `entity_ref(endpoint,exactly_one(parse_ip_list(wpl.srcIp)))` -> "endpoint::203.0.113.143" | `drop_and_review` | confirmed；源端点稳定引用 |
| `roles.target.ref_id` | `derived` | `derived.entity_ref(endpoint,exactly_one(parse_ip_list(wpl.dstIp)))` | `entity_ref(endpoint,exactly_one(parse_ip_list(wpl.dstIp)))` -> "endpoint::203.0.113.99" | `drop_and_review` | confirmed；无目标端口时按目标 IP 建立稳定引用 |
| `roles.related[].ref_id` | `derived` | `derived.entity_ref(domain,parse_domain_list(wpl.domain)[])` | `map(entity_ref(domain,item),parse_domain_list(wpl.domain))` -> ["domain::a-gwas-01.dyndns.org"] | `drop_invalid_items_and_review` | confirmed；每个域名建立稳定关联引用 |
| `roles.observer.device.name` | `derived` | `raw_syslog.header.host` | `read(raw_syslog.header.host)` -> "host-2cfba8ce.sdm.example.internal" | `—` | confirmed；Syslog 上报主机名 |
| `extensions.source_private.syslog_host` | `derived` | `raw_syslog.header.host` | `read(raw_syslog.header.host)` -> "host-2cfba8ce.sdm.example.internal" | `—` | confirmed；Syslog 上报主机名审计值 |
| `extensions.source_private.syslog_priority` | `derived` | `raw_syslog.header.priority` | `read(raw_syslog.header.priority)` -> 14 | `—` | confirmed；Syslog PRI 审计值 |
| `extensions.source_private.syslog_header_time` | `derived` | `raw_syslog.header.time` | `read(raw_syslog.header.time)` -> "Dec 18 16:01:31" | `—` | confirmed；不含年份的 Syslog 头时间审计值 |
| `roles.source.entity_type` | `constant` | `constant.roles_source_entity_type` | "endpoint" | `—` | confirmed；源 IP 装配为 endpoint |
| `roles.target.entity_type` | `constant` | `constant.roles_target_entity_type` | "endpoint" | `—` | confirmed；目标 IP/端口装配为 endpoint |
| `roles.related[].entity_type` | `constant` | `constant.roles_relateditems_entity_type` | "domain" | `—` | confirmed；domain 装配为关联域名 |
| `roles.carriers` | `constant` | `constant.roles_carriers` | [] | `—` | confirmed；无进程、会话或独立协议载体 |
| `roles.observer.product.name` | `constant` | `constant.roles_observer_product_name` | "NGSOC" | `—` | confirmed；来源产品显示名 |
| `roles.observer.device.vendor` | `constant` | `constant.roles_observer_device_vendor` | "qax" | `—` | confirmed；来源厂商 |
| `extensions.schema_version` | `constant` | `constant.extensions_schema_version` | 2 | `—` | confirmed；扩展契约版本 |
| `extensions.profiles` | `constant` | `constant.extensions_profiles` | {} | `—` | confirmed；无平台画像 |
| `extensions.enrichments` | `constant` | `constant.extensions_enrichments` | {} | `—` | confirmed；无平台富化 |
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
| `occur_time` | `transform` | `timestamp` | `parse_time_ms(wpl.timestamp,'Asia/Shanghai')` -> 1734483597000 | `drop_and_review` | confirmed；WPL 输出仍为 chars；SDM 装配转换为毫秒 |
| `source_original_event_id` | `projection` | `seq` | "12934380" | `—` | confirmed；来源告警序列热字段 |
| `source_finding.original_id` | `projection` | `seq` | "12934380" | `—` | confirmed；来源 finding 原始 ID |
| `roles.source.endpoint.ip` | `transform` | `srcIp` | `exactly_one(parse_ip_list(wpl.srcIp))` -> "203.0.113.143" | `drop_and_review` | confirmed；单一通信源 IP |
| `source_ip` | `projection` | `roles.source.endpoint.ip` | "203.0.113.143" | `—` | confirmed；从源端点投影热字段 |
| `roles.target.endpoint.ip` | `transform` | `dstIp` | `exactly_one(parse_ip_list(wpl.dstIp))` -> "203.0.113.99" | `drop_and_review` | confirmed；单一通信目标 IP |
| `target_ip` | `projection` | `roles.target.endpoint.ip` | "203.0.113.99" | `—` | confirmed；从目标端点投影热字段 |
| `roles.related[].domain.name` | `transform` | `domain` | `parse_domain_list(wpl.domain)` -> ["a-gwas-01.dyndns.org"] | `drop_invalid_items_and_review` | confirmed；关联域名不声明与目标 IP 的 DNS 关系 |
| `roles.observer.device.ip` | `transform` | `devIp` | `exactly_one(parse_ip_list(wpl.devIp))` -> "192.0.2.37" | `omit_and_review` | confirmed；观测设备 IP |
| `source_finding.title` | `projection` | `name` | "Injecto远控木马活动事件" | `—` | confirmed；来源告警标题 |
| `source_finding.severity` | `projection` | `severity` | "高危" | `—` | confirmed；来源严重度 |
| `source_finding.status` | `projection` | `disposeState` | "待处置" | `—` | confirmed；来源处置状态；未做字典归一 |
| `source_finding.count` | `transform` | `times` | `to_int(wpl.times)` -> 7 | `omit_and_review` | confirmed；聚合命中次数 |
| `source_finding.confidence` | `projection` | `confidence` | "高" | `—` | confirmed；来源置信度 |
| `source_finding.category.original.name` | `projection` | `ruleCategoryName` | "远控木马" | `—` | confirmed；来源分类 |
| `source_finding.victim.endpoint.ip` | `transform` | `victimContent` | `exactly_one(parse_ip_list(wpl.victimContent))` -> "203.0.113.143" | `omit_and_review` | confirmed；来源受害方声明对应通信主体 |
| `source_finding.victim.geo` | `transform` | `sipGeo` | `geo_by_ip(parse_json(wpl.sipGeo),exactly_one(parse_ip_list(wpl.victimContent)))` -> {"continent": {"name": "北美洲"}, "country": {"name": "美国"}, "region": {"name": "俄亥俄州"}, "city": {"name": "哥伦布"}, "coordinates": {"latitude": 39.96120071411133, "longitude": -82.9988021850586}} | `omit_and_review` | confirmed；受害方 Geo 按 victimContent IP 从 sipGeo 取值 |
| `extensions.source_private.communication_target_geo` | `transform` | `dipGeo` | `normalize_geo(geo_by_ip(parse_json(wpl.dipGeo),exactly_one(parse_ip_list(wpl.dstIp))))` -> {"continent": "北美洲", "country": "美国", "region": "俄亥俄州", "city": "哥伦布", "latitude": 39.96120071411133, "longitude": -82.9988021850586} | `preserve_raw_and_review` | confirmed；dipGeo 属于通信目标；清理空字段并将坐标转数值，不冒充来源攻击方 Geo |
| `source_finding.rule.label` | `transform` | `ruleName` | `exactly_one(parse_text_list(wpl.ruleName))` -> "Injecto远控木马活动事件" | `omit_and_review` | confirmed；ruleId 为空，仅保留来源检测规则名称 |
| `source_finding.ioc.type` | `transform` | `iocType` | `exactly_one(parse_text_list(wpl.iocType))` -> "域名" | `omit_and_review` | confirmed；来源 IOC 类型 |
| `source_finding.ioc.value` | `transform` | `ioc` | `exactly_one(parse_text_list(wpl.ioc))` -> "a-gwas-01.dyndns.org" | `omit_and_review` | confirmed；来源 IOC 域名 |
| `source_finding.malware.name` | `transform` | `maliciousFamily` | `exactly_one(parse_text_list(wpl.maliciousFamily))` -> "Injecto" | `omit_and_review` | confirmed；来源恶意家族名称 |
| `facets.dns.question.name` | `transform` | `domain` | `exactly_one(parse_domain_list(wpl.domain))` -> "a-gwas-01.dyndns.org" | `omit_and_review` | confirmed；DNS 查询域名；不推断应答 |
| `extensions.source_private.protocol_original` | `transform` | `protocol` | `parse_text_list(wpl.protocol)` -> ["DNS"] | `preserve_raw_and_review` | confirmed；保留来源协议原值 |
| `extensions.source_private.relevant_rule_name` | `projection` | `relevantRuleName` | "预置-网络探针检测到远控木马IOC命中事件" | `—` | confirmed；触发告警的关联规则名称；不与检测规则 ID 配对 |
| `source_finding.attention.content` | `projection` | `attentionValue` | "源IP : 203.0.113.143" | `—` | confirmed；来源关注内容 |
| `source_finding.behavior` | `conditional` | `name/ruleCategoryName` | `when wpl.name == "Injecto远控木马活动事件" && wpl.ruleCategoryName == "远控木马" then chars(remote_access_trojan) else omit` -> "remote_access_trojan" | `omit` | confirmed；来源名称和分类共同声明远控木马活动；恶意家族另行映射 |
| `source_finding.killchain` | `dictionary` | `killchain` | "通信控制" -> "command_and_control" | `preserve_in_extension_and_review` | partial；当前样例值映射；原值保留供完整字典复核 |
| `extensions.unmapped.attack_result_original` | `projection` | `attackResult` | "企图" | `—` | confirmed；字典仅覆盖当前样例值，保留厂商原文 |
| `extensions.unmapped.killchain_original` | `projection` | `killchain` | "通信控制" | `—` | confirmed；字典仅覆盖当前样例值，保留厂商原文 |
| `extensions.unmapped.compromise_state_original` | `projection` | `compromiseState` | "已失陷" | `—` | confirmed；字典仅覆盖当前样例值，保留厂商原文 |
| `facets.network.direction` | `dictionary` | `commDirection` | "内到内" -> "L2L" | `preserve_in_extension_and_review` | partial；当前样例值映射 |
| `extensions.source_private.wpl_update_time` | `projection` | `update_time` | "2026-12-18 16:01:31" | `—` | confirmed；WPL 从无年份 Syslog 头推断，仅供审计 |
| `extensions.source_private.latest_timestamp` | `projection` | `latestTimestamp` | 1734508604000 | `—` | confirmed；WPL 已转毫秒 |
| `extensions.source_private.relevant_log_types` | `transform` | `relevantLogsType` | `parse_text_list(wpl.relevantLogsType)` -> ["天堤威胁情报告警日志"] | `preserve_raw_and_review` | confirmed；来源关联日志类型 |
| `extensions.source_private.relevant_network_segments` | `transform` | `relevantNetworkSegmentId` | `parse_text_list(wpl.relevantNetworkSegmentId)` -> ["华容农商行业务网", "星沙上线环境业务网段", "运维管理区"] | `preserve_raw_and_review` | confirmed；来源关联网络分区 |
| `source_alert_severity` | `transform` | `severity` | `string` -> "高危" | `—` | confirmed；保留来源 finding 原始严重度 |
| `severity` | `dictionary` | `severity` | "高危" -> "error" | `null_and_review` | partial；根据当前 NGSOC 样例分布推测的安全严重度交叉表，尚未经厂商确认 |
| `source_finding.attack_result` | `dictionary` | `attackResult` | "企图" -> "attempted" | `preserve_in_extension_and_review` | partial；检测到攻击尝试，但不声明动作成功 |
| `outcome` | `dictionary` | `attackResult` | "企图" -> "observed" | `unknown_and_review` | partial；检测到攻击尝试，但不声明动作成功 |
| `source_finding.compromise_status` | `dictionary` | `compromiseState` | "已失陷" -> "compromised" | `preserve_in_extension_and_review` | partial；布尔值及中文值按当前样例语义推测，尚未经厂商确认 |

### 5.3 编写约束

- 字典仅覆盖当前样例值，完整厂商字典仍需确认。
- 通信 source/target 按观测方向保留；victim 按来源声明独立映射。
- attackerContent 和端口为空，不构造攻击方或端口事实。
- 不推断 DNS 应答、域名解析结果或远控连接成功。
