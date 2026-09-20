# WPL -> SDM Event 字段映射

> 样例：`vpn_multi_mac_login.expected-sdm-event.behavior.json（现行）；旧 `*.expected-sdm-event.json` 为 55 列对照`。机器可读 JSON 记录全部 `67` 个 WPL 字段的处理结论。

## 核心字段

| WPL 来源 | SDM 落位 | 转换 | 说明 |
|---|---|---|---|
| `timestamp` | `occur_time` | 按 Asia/Shanghai 转毫秒 | 聚合 finding 的事件时间 |
| `userName` | `roles.source.user.name`、`source_user` | 解析唯一用户 | 登录行为主体 |
| `attackerContent/srcIp` | `roles.related[].endpoint` | 严格验证并配对交替 IP/MAC | 登录来源端点，不构造攻击方 |
| `sipGeo` | `roles.related[].geo` | 按来源 IP 关联 | 来源端点 Geo |
| `authType` | `facets.authentication.auth_type` | 取唯一组合值 | 来源认证方式，非闭合字典 |
| `name/eventType` | `facets.authentication.auth_result` | “登录成功”+`login` -> `success` | 局部字典，不驱动顶层 outcome |
| `devIp` | `roles.observer.device.ip_addresses[].address` | 解析 IP 列表 | 多个观察设备地址 |
| `relevantAssetsName` | `extensions.source_private.relevant_asset_names` | 解析列表 | 不选择唯一 VPN 目标 |

## 映射边界

- 不把 `attackerContent` 解释为攻击者列表。
- 不拆分两条登录 activity，不虚构每次登录时间或会话。
- 不把 `devIp` 或 `relevantAssetsName` 任意指定为登录目标。
- Meta 和 Content 的逐字段赋值规则见下方生成表。

## 五、WPL/OML 编写规则

> WPL 只负责提取表中的 source 字段；Meta 和 Content 的赋值由 OML 按下表实现。
> `partial` 表示当前只有样例值或局部说明，不能视为完整厂商字典。

### 5.1 Meta 区

| SDM 字段 | 规则类型 | 输入/来源 | 赋值 | 未命中 | 状态与证据 |
|---|---|---|---|---|---|
| `source_original_event_id/source_finding.original_id` | `derived` | `derived.prefixed_sha256('raw-', raw_input.original_payload)` | `'raw-' + sha256(raw_input.original_payload)` -> "raw-6e7c6fc43c4963d2657d282f775928dcebb43b9328e8fc7f13c11f6219b2f193" | `—` | confirmed；seq 为空，使用完整原始载荷哈希 |
| `event_id` | `derived` | `derived.prefixed_sha256('evt-', tenant_id+'|'+mapping_id+'|'+source_original_event_id)` | `'evt-' + sha256(tenant_id+'|'+mapping_id+'|'+source_original_event_id)` -> "evt-bc8efe2681d3672d7b59ae1cb8f0f08b1d2021dd148b9cad1f09a8fafe78d8b5" | `—` | confirmed；确定性事件 ID |
| `record_kind` | `conditional` | `when wpl.name == "定制-VPN12小时内不同物理地址登录成功(mac版)" && contains(parse_text_list(wpl.eventType), "login") && exactly_one(parse_text_list(wpl.userName)) != "" && length(parse_ip_list(wpl.srcIp)) >= 2 && valid_alternating_ip_mac_pairs(wpl.attackerContent, wpl.srcIp)` | `when wpl.name == "定制-VPN12小时内不同物理地址登录成功(mac版)" && contains(parse_text_list(wpl.eventType), "login") && exactly_one(parse_text_list(wpl.userName)) != "" && length(parse_ip_list(wpl.srcIp)) >= 2 && valid_alternating_ip_mac_pairs(wpl.attackerContent, wpl.srcIp) then chars(finding) else no_match` -> "finding" | `no_match` | confirmed；NGSOC 来源聚合告警 |
| `event_domain` | `conditional` | `when wpl.name == "定制-VPN12小时内不同物理地址登录成功(mac版)" && contains(parse_text_list(wpl.eventType), "login") && exactly_one(parse_text_list(wpl.userName)) != "" && length(parse_ip_list(wpl.srcIp)) >= 2 && valid_alternating_ip_mac_pairs(wpl.attackerContent, wpl.srcIp)` | `when wpl.name == "定制-VPN12小时内不同物理地址登录成功(mac版)" && contains(parse_text_list(wpl.eventType), "login") && exactly_one(parse_text_list(wpl.userName)) != "" && length(parse_ip_list(wpl.srcIp)) >= 2 && valid_alternating_ip_mac_pairs(wpl.attackerContent, wpl.srcIp) then chars(identity) else no_match` -> "identity" | `no_match` | confirmed；来源标题和 eventType 明确为登录身份活动 |
| `event_type` | `conditional` | `when wpl.name == "定制-VPN12小时内不同物理地址登录成功(mac版)" && contains(parse_text_list(wpl.eventType), "login") && exactly_one(parse_text_list(wpl.userName)) != "" && length(parse_ip_list(wpl.srcIp)) >= 2 && valid_alternating_ip_mac_pairs(wpl.attackerContent, wpl.srcIp)` | `when wpl.name == "定制-VPN12小时内不同物理地址登录成功(mac版)" && contains(parse_text_list(wpl.eventType), "login") && exactly_one(parse_text_list(wpl.userName)) != "" && length(parse_ip_list(wpl.srcIp)) >= 2 && valid_alternating_ip_mac_pairs(wpl.attackerContent, wpl.srcIp) then chars(user_login) else no_match` -> "user_login" | `no_match` | confirmed；VPN 登录聚合 finding |
| `operation` | `conditional` | `when wpl.name == "定制-VPN12小时内不同物理地址登录成功(mac版)" && contains(parse_text_list(wpl.eventType), "login") && exactly_one(parse_text_list(wpl.userName)) != "" && length(parse_ip_list(wpl.srcIp)) >= 2 && valid_alternating_ip_mac_pairs(wpl.attackerContent, wpl.srcIp)` | `when wpl.name == "定制-VPN12小时内不同物理地址登录成功(mac版)" && contains(parse_text_list(wpl.eventType), "login") && exactly_one(parse_text_list(wpl.userName)) != "" && length(parse_ip_list(wpl.srcIp)) >= 2 && valid_alternating_ip_mac_pairs(wpl.attackerContent, wpl.srcIp) then chars(remote) else no_match` -> "remote" | `no_match` | confirmed；VPN 登录属于远程登录；不细分交互式或服务登录 |
| `roles.source.ref_id` | `derived` | `derived.entity_ref(user, exactly_one(parse_text_list(wpl.userName)))` | `'user-' + sha256(exactly_one(parse_text_list(wpl.userName)))[0:32]` -> "user-0d2b05f4516aae5c6c9c9cc723197a36" | `drop_and_review` | confirmed；用户主体稳定引用 |
| `roles.target.ref_id` | `derived` | `derived.entity_ref(service, lower('VPN'))` | `'service-' + sha256(lower('VPN'))[0:32]` -> "service-ebf20cefc9169e0b714703d63d480c3e" | `—` | confirmed；标题明确的 VPN 服务；未绑定唯一网关资产 |
| `roles.related[].ref_id` | `derived` | `derived.entity_ref(endpoint, pair_alternating_ip_mac(wpl.attackerContent)[])` | `map('endpoint-' + sha256(item.ip+'|'+item.mac)[0:32], pair_alternating_ip_mac(wpl.attackerContent))` -> ["endpoint-a62e91ba4d5bceb486543711b0d75e10", "endpoint-52a87fb893ac8e809c53f06a7f74af9c"] | `drop_and_review` | confirmed；两个登录来源端点稳定引用 |
| `roles.observer.device.name` | `derived` | `raw_syslog.header.host` | `read(raw_syslog.header.host)` -> "host-2cfba8ce.sdm.example.internal" | `—` | confirmed；Syslog 上报主机 |
| `extensions.source_private.syslog_priority/syslog_host/syslog_header_time` | `derived` | `raw_syslog.header` | `parse_syslog_header(raw_input.original_payload)` -> {"priority": 14, "host": "host-2cfba8ce.sdm.example.internal", "time": "Dec 18 16:01:50"} | `—` | confirmed；保留 Syslog 头审计值 |
| `roles.source.entity_type` | `constant` | `constant.roles_source_entity_type` | "user" | `—` | confirmed；主体为登录用户 |
| `roles.target.entity_type` | `constant` | `constant.roles_target_entity_type` | "service" | `—` | confirmed；客体为 VPN 服务 |
| `roles.target.service.name` | `constant` | `constant.roles_target_service_name` | "VPN" | `—` | confirmed；标题明确 VPN 服务 |
| `roles.related[].entity_type` | `constant` | `constant.roles_relateditems_entity_type` | "endpoint" | `—` | confirmed；登录来源 IP/MAC 装配为 endpoint |
| `roles.related[].relation_type` | `constant` | `constant.roles_relateditems_relation_type` | "login_source" | `—` | confirmed；关联端点表示登录来源 |
| `roles.carriers` | `constant` | `constant.roles_carriers` | [] | `—` | confirmed；无会话、进程或独立载体实体 |
| `roles.observer.product.name` | `constant` | `constant.roles_observer_product_name` | "NGSOC" | `—` | confirmed；来源产品显示名 |
| `roles.observer.device.vendor` | `constant` | `constant.roles_observer_device_vendor` | "qax" | `—` | confirmed；来源设备厂商 |
| `facets.application.name` | `constant` | `constant.facets_application_name` | "VPN" | `—` | confirmed；标题明确 VPN 应用场景 |
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
| `occur_time` | `transform` | `timestamp` | `parse_time_ms(wpl.timestamp,'Asia/Shanghai')` -> 1734508540000 | `drop_and_review` | confirmed；WPL 输出仍为 chars；SDM 装配转换为毫秒 |
| `roles.source.user.name` | `transform` | `userName` | `exactly_one(parse_text_list(wpl.userName))` -> "秦锦" | `drop_and_review` | confirmed；同一用户是聚合行为主体 |
| `source_user` | `projection` | `roles.source.user.name` | "秦锦" | `—` | confirmed；从用户主体投影热字段 |
| `roles.related[].endpoint` | `transform` | `attackerContent/srcIp` | `pair_alternating_ip_mac(wpl.attackerContent, wpl.srcIp)` -> [{"ip": "203.0.113.8", "mac": "00:00:5E:00:53:EB"}, {"ip": "203.0.113.141", "mac": "00:00:5E:00:53:62"}] | `drop_and_review` | confirmed；只有严格交替且 IP 顺序与 srcIp 一致时才配对；不解释为攻击方 |
| `roles.related[].geo` | `transform` | `sipGeo/srcIp` | `map(normalize_geo(geo_by_ip(parse_json(wpl.sipGeo),ip)), parse_ip_list(wpl.srcIp))` -> [{"continent": {"name": "亚洲"}, "country": {"name": "中国"}, "region": {"name": "湖南省"}, "city": {"name": "娄底市"}, "coordinates": {"latitude": 27.738399505615234, "longitude": 111.98400115966797}}, {"continent": {"name": "亚洲"}, "country": {"name": "中国"}, "region": {"name": "湖南省"}, "city": {"name": "永州市"}, "coordinates": {"latitude": 26.433300018310547, "longitude": 111.60299682617188}}] | `omit_missing_items_and_review` | confirmed；按 IP 为两个登录来源端点关联来源 Geo |
| `roles.observer.device.ip_addresses[].address` | `transform` | `devIp` | `parse_ip_list(wpl.devIp)` -> ["192.0.2.91", "203.0.113.120"] | `drop_invalid_items_and_review` | confirmed；保留多个观察设备地址，不投影单一 device_ip |
| `facets.authentication.auth_type` | `transform` | `authType` | `exactly_one(parse_text_list(wpl.authType))` -> "auth_local_pass|auth_hid|auth_emm" | `omit_and_review` | confirmed；来源认证方式组合；当前不是闭合字典 |
| `facets.authentication.auth_result` | `dictionary` | `name/eventType` | {"name_contains": "登录成功", "eventType": "login"} -> "success" | `omit_and_review` | partial；标题明确登录成功且 eventType=login；认证结果不驱动顶层 finding outcome |
| `source_finding.title` | `projection` | `name` | "定制-VPN12小时内不同物理地址登录成功(mac版)" | `—` | confirmed；来源告警标题 |
| `source_finding.severity` | `projection` | `severity` | "中危" | `—` | confirmed；来源严重度 |
| `source_finding.status` | `projection` | `disposeState` | "待处置" | `—` | confirmed；来源处置状态；未做字典归一 |
| `source_finding.count` | `transform` | `times` | `to_int(wpl.times)` -> 1 | `omit_and_review` | confirmed；来源聚合命中次数 |
| `source_finding.confidence` | `projection` | `confidence` | "高" | `—` | confirmed；来源置信度 |
| `source_finding.category.original.name` | `projection` | `ruleCategoryName` | "其它类攻击利用" | `—` | confirmed；来源分类 |
| `source_finding.behavior` | `conditional` | `name/eventType` | `when wpl.name == "定制-VPN12小时内不同物理地址登录成功(mac版)" && contains(parse_text_list(wpl.eventType), "login") && exactly_one(parse_text_list(wpl.userName)) != "" && length(parse_ip_list(wpl.srcIp)) >= 2 && valid_alternating_ip_mac_pairs(wpl.attackerContent, wpl.srcIp) then chars(vpn_multiple_physical_address_login) else omit` -> "vpn_multiple_physical_address_login" | `omit` | confirmed；来源规则声明同一 VPN 用户从多个物理地址登录 |
| `source_finding.attention.content` | `projection` | `attentionValue` | "源IP : 203.0.113.8 ,  203.0.113.141  , 用户名 : 秦锦" | `—` | confirmed；完整保留来源关注内容 |
| `extensions.unmapped.comm_direction_original` | `transform` | `commDirection` | `exactly_one(parse_text_list(wpl.commDirection))` -> "未知" | `omit_and_review` | confirmed；未知方向不归一，保留原值 |
| `extensions.source_private.wpl_update_time` | `projection` | `update_time` | "2026-12-18 16:01:50" | `—` | confirmed；WPL 从无年份 Syslog 头推断，仅供审计 |
| `extensions.source_private.latest_timestamp` | `projection` | `latestTimestamp` | 1734508540000 | `—` | confirmed；WPL 已转换为毫秒 |
| `extensions.source_private.finding_source` | `projection` | `source` | "关联规则" | `—` | confirmed；来源 finding 生成方式 |
| `extensions.source_private.relevant_rule_name` | `projection` | `relevantRuleName` | "定制-VPN12小时内不同物理地址登录成功(mac版)" | `—` | confirmed；关联规则名称；不冒充 ruleName/ruleId |
| `extensions.source_private.relevant_log_types` | `transform` | `relevantLogsType` | `parse_text_list(wpl.relevantLogsType)` -> ["VPN日志"] | `preserve_raw_and_review` | confirmed；来源关联日志类型 |
| `extensions.source_private.relevant_network_segments` | `transform` | `relevantNetworkSegmentId` | `parse_text_list(wpl.relevantNetworkSegmentId)` -> ["运维管理区"] | `preserve_raw_and_review` | confirmed；来源关联网络分区 |
| `extensions.source_private.relevant_asset_names` | `transform` | `relevantAssetsName` | `parse_text_list(wpl.relevantAssetsName)` -> ["互联网业务区VPN-EMM-1", "互联网业务区VPN-EMM-2"] | `preserve_raw_and_review` | confirmed；来源关联资产，不选择唯一 VPN 目标 |
| `extensions.source_private.relevant_asset_groups` | `transform` | `relevantAssetsGroup` | `parse_text_list(wpl.relevantAssetsGroup)` -> ["运维管理区", "已删除", "湖南省联社"] | `preserve_raw_and_review` | confirmed；来源关联资产组 |
| `extensions.source_private.client_types` | `transform` | `clientType` | `parse_text_list(wpl.clientType)` -> ["ANDROID"] | `preserve_raw_and_review` | confirmed；客户端类型原值 |
| `extensions.source_private.event_types_original` | `transform` | `eventType` | `parse_text_list(wpl.eventType)` -> ["login"] | `preserve_raw_and_review` | confirmed；事件类型原值 |
| `extensions.source_private.auth_types_original` | `transform` | `authType` | `parse_text_list(wpl.authType)` -> ["auth_local_pass|auth_hid|auth_emm"] | `preserve_raw_and_review` | confirmed；认证方式列表原值 |
| `source_alert_severity` | `transform` | `severity` | `string` -> "中危" | `—` | confirmed；保留来源 finding 原始严重度 |
| `severity` | `dictionary` | `severity` | "中危" -> "warning" | `null_and_review` | partial；根据当前 NGSOC 样例分布推测的安全严重度交叉表，尚未经厂商确认 |
| `outcome` | `conditional` | `name + eventType` | `chars(success)` -> "success" | `unknown` | partial；标题明确声明登录成功，且 eventType=login |

### 5.3 编写约束

- 用户是登录主体；VPN 是标题明确的服务客体；两个 IP/MAC 是关联登录来源端点。
- attackerContent 在此日志类型中承载 IP/MAC 观察值，不代表来源声明攻击者。
- 只有 attackerContent 严格按 IP/MAC 交替且 IP 顺序与 srcIp 一致时才配对，否则整组进入 review。
- 认证成功来自标题和 eventType 的联合局部字典；顶层 finding outcome 保持 success。
- 两个 devIp 是观察设备地址；两个 relevantAssetsName 不足以确定唯一 VPN 目标。
