# WPL -> SDM Event 字段映射

> 样例：`mssql_waitfor_delay_sql_injection.expected-sdm-event.behavior.json（现行）；旧 `*.expected-sdm-event.json` 为 55 列对照`。机器可读 JSON 记录全部 `67` 个 WPL 字段的处理结论。

## 核心字段

| WPL 来源 | SDM 落位 | 转换 | 说明 |
|---|---|---|---|
| `timestamp` | `occur_time` | 按 Asia/Shanghai 转毫秒 | WPL 实际输出仍为 chars，使用正文事件时间 |
| `seq` | `source_original_event_id`、`source_finding.original_id` | 直接赋值 | 来源告警序列 |
| `srcIp[0]` | `roles.source.endpoint.ip` | 取唯一值 | 通信主体 |
| `dstIp[0]+dport[0]` | `roles.target.endpoint` | 组合 IP/端口 | 通信客体 |
| `attackerContent/victimContent` | `source_finding.attacker/victim` | 分别取唯一值 | 来源设备的攻击方/受害方声明 |
| `sport` | `extensions.source_private.source_ports` | 校验端口数组 | 多源端口不生成 `source_port` |
| `uri` | `extensions.source_private.request_targets` | 解析字段专属括号列表 | 保留多值相对 URI |
| `domain` | `roles.related[].domain` | 解析并逐项建实体 | 不声明 DNS 绑定关系 |
| `dipGeo` | `source_finding.victim.geo` | JSON 解析并按 victim IP 取值 | 目标地理信息 |
| `ruleId` + `ruleName` | `source_finding.rule.id/label` | 分别取唯一值 | 同一检测规则的 ID 与名称，必须配对映射 |
| `relevantRuleName` | `extensions.source_private.relevant_rule_name` | 直接赋值 | 关联规则名称，不覆盖检测规则名称 |
| `attCk` | `extensions.unmapped.att_ck_original` | 原值保留 | 不是 ATT&CK 技术 ID |

## 映射边界

- 不推断 HTTP 方法、传输协议、响应、阻断或 SQL 执行成功。
- `uri/domain/...` 虽呈括号列表文本，但必须按字段语义解析；URI 内部可能含复杂载荷，不能使用全局逗号拆分规则。
- Meta 和 Content 的逐字段赋值规则见下方生成表。

## 五、WPL/OML 编写规则

> WPL 只负责提取表中的 source 字段；Meta 和 Content 的赋值由 OML 按下表实现。
> `partial` 表示当前只有样例值或局部说明，不能视为完整厂商字典。

### 5.1 Meta 区

| SDM 字段 | 规则类型 | 输入/来源 | 赋值 | 未命中 | 状态与证据 |
|---|---|---|---|---|---|
| `event_id` | `derived` | `derived.sha256(tenant_id+'|'+mapping_id+'|'+wpl.seq)` | `'evt-' + sha256(tenant_id+'|'+mapping_id+'|'+wpl.seq)` -> "evt-68ab54deb295b1b964dfcd7f3bdd04e48bacae8935176e07b394447ac70b408e" | `—` | confirmed；来源序列驱动的确定性事件 ID |
| `record_kind` | `conditional` | `when wpl.name == "MSSQL Waitfor语句SQL注入攻击" && wpl.ruleCategoryName == "SQL注入" && any_all_contains(parse_uri_list(wpl.uri, entry_prefix="/"), ["waitfor", "delay"], case_insensitive=true)` | `when wpl.name == "MSSQL Waitfor语句SQL注入攻击" && wpl.ruleCategoryName == "SQL注入" && any_all_contains(parse_uri_list(wpl.uri, entry_prefix="/"), ["waitfor", "delay"], case_insensitive=true) then chars(finding) else no_match` -> "finding" | `no_match` | confirmed；NGSOC 来源告警 |
| `event_domain` | `conditional` | `when wpl.name == "MSSQL Waitfor语句SQL注入攻击" && wpl.ruleCategoryName == "SQL注入" && any_all_contains(parse_uri_list(wpl.uri, entry_prefix="/"), ["waitfor", "delay"], case_insensitive=true)` | `when wpl.name == "MSSQL Waitfor语句SQL注入攻击" && wpl.ruleCategoryName == "SQL注入" && any_all_contains(parse_uri_list(wpl.uri, entry_prefix="/"), ["waitfor", "delay"], case_insensitive=true) then chars(threat) else no_match` -> "threat" | `no_match` | confirmed；来源 SQL 注入检测声明 |
| `event_type` | `conditional` | `when wpl.name == "MSSQL Waitfor语句SQL注入攻击" && wpl.ruleCategoryName == "SQL注入" && any_all_contains(parse_uri_list(wpl.uri, entry_prefix="/"), ["waitfor", "delay"], case_insensitive=true) && exactly_one(parse_text_list(wpl.relevantLogsType)) == "天堤网页漏洞利用日志"` | `when wpl.name == "MSSQL Waitfor语句SQL注入攻击" && wpl.ruleCategoryName == "SQL注入" && any_all_contains(parse_uri_list(wpl.uri, entry_prefix="/"), ["waitfor", "delay"], case_insensitive=true) && exactly_one(parse_text_list(wpl.relevantLogsType)) == "天堤网页漏洞利用日志" then chars(network_http) else no_match` -> "network_http" | `no_match` | confirmed；网页漏洞利用日志与 URI 载荷共同支持 HTTP 请求上下文 |
| `operation` | `conditional` | `when wpl.name == "MSSQL Waitfor语句SQL注入攻击" && wpl.ruleCategoryName == "SQL注入" && any_all_contains(parse_uri_list(wpl.uri, entry_prefix="/"), ["waitfor", "delay"], case_insensitive=true) && exactly_one(parse_text_list(wpl.relevantLogsType)) == "天堤网页漏洞利用日志"` | `when wpl.name == "MSSQL Waitfor语句SQL注入攻击" && wpl.ruleCategoryName == "SQL注入" && any_all_contains(parse_uri_list(wpl.uri, entry_prefix="/"), ["waitfor", "delay"], case_insensitive=true) && exactly_one(parse_text_list(wpl.relevantLogsType)) == "天堤网页漏洞利用日志" then chars() else no_match` -> "" | `no_match` | confirmed；当前 HTTP 告警分支无方法或标准动作证据；不得影响同 mapping_id 的其他子类型 |
| `roles.source.ref_id` | `derived` | `derived.entity_ref(endpoint,exactly_one(parse_ip_list(wpl.srcIp)))` | `entity_ref(endpoint,exactly_one(parse_ip_list(wpl.srcIp)))` -> "endpoint::192.0.2.238" | `drop_and_review` | confirmed；源端点稳定引用 |
| `roles.target.ref_id` | `derived` | `derived.entity_ref(endpoint,exactly_one(parse_ip_list(wpl.dstIp)),exactly_one(parse_port_list(wpl.dport)))` | `entity_ref(endpoint,exactly_one(parse_ip_list(wpl.dstIp)),exactly_one(parse_port_list(wpl.dport)))` -> "endpoint::192.0.2.146:80" | `drop_and_review` | confirmed；目标端点稳定引用 |
| `roles.related[].ref_id` | `derived` | `derived.entity_ref(domain,parse_domain_list(wpl.domain)[])` | `map(entity_ref(domain,item),parse_domain_list(wpl.domain))` -> ["domain::host-349f2008.sdm.example.internal", "domain::host-5c568da6.sdm.example.internal"] | `drop_invalid_items_and_review` | confirmed；每个域名建立稳定关联引用 |
| `roles.observer.device.name` | `derived` | `raw_syslog.header.host` | `read(raw_syslog.header.host)` -> "host-2cfba8ce.sdm.example.internal" | `—` | confirmed；Syslog 上报主机名 |
| `extensions.source_private.syslog_host` | `derived` | `raw_syslog.header.host` | `read(raw_syslog.header.host)` -> "host-2cfba8ce.sdm.example.internal" | `—` | confirmed；Syslog 上报主机名审计值 |
| `extensions.source_private.syslog_priority` | `derived` | `raw_syslog.header.priority` | `read(raw_syslog.header.priority)` -> 14 | `—` | confirmed；Syslog PRI 审计值 |
| `extensions.source_private.syslog_header_time` | `derived` | `raw_syslog.header.time` | `read(raw_syslog.header.time)` -> "Dec 18 16:01:02" | `—` | confirmed；不含年份的 Syslog 头时间审计值 |
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
| `occur_time` | `transform` | `timestamp` | `parse_time_ms(wpl.timestamp,'Asia/Shanghai')` -> 1734506894000 | `drop_and_review` | confirmed；WPL 输出仍为 chars；SDM 装配转换为毫秒 |
| `source_original_event_id` | `projection` | `seq` | "12936312" | `—` | confirmed；来源告警序列热字段 |
| `source_finding.original_id` | `projection` | `seq` | "12936312" | `—` | confirmed；来源 finding 原始 ID |
| `roles.source.endpoint.ip` | `transform` | `srcIp` | `exactly_one(parse_ip_list(wpl.srcIp))` -> "192.0.2.238" | `drop_and_review` | confirmed；单一通信源 IP |
| `source_ip` | `projection` | `roles.source.endpoint.ip` | "192.0.2.238" | `—` | confirmed；从源端点投影热字段 |
| `roles.target.endpoint.ip` | `transform` | `dstIp` | `exactly_one(parse_ip_list(wpl.dstIp))` -> "192.0.2.146" | `drop_and_review` | confirmed；单一通信目标 IP |
| `target_ip` | `projection` | `roles.target.endpoint.ip` | "192.0.2.146" | `—` | confirmed；从目标端点投影热字段 |
| `roles.target.endpoint.port` | `transform` | `dport` | `exactly_one(parse_port_list(wpl.dport))` -> 80 | `drop_and_review` | confirmed；单一目标端口 |
| `target_port` | `projection` | `roles.target.endpoint.port` | 80 | `—` | confirmed；从目标端点投影热字段 |
| `source_finding.victim.endpoint.port` | `transform` | `dport` | `exactly_one(parse_port_list(wpl.dport))` -> 80 | `omit_and_review` | confirmed；来源受害方端口声明 |
| `extensions.source_private.source_ports` | `transform` | `sport` | `parse_port_list(wpl.sport)` -> [51572, 51598, 51586, 57786, 57788, 57800, 57798, 33312, 33276, 33294] | `drop_invalid_items_and_review` | confirmed；保留聚合源端口；不生成 source_port |
| `extensions.source_private.request_targets` | `transform` | `uri` | `parse_uri_list(wpl.uri,entry_prefix='/')` -> ["/login?url=http://host-5c568da6.sdm.example.internal//**/and(select/**/1)>0/**/waitfor/**/delay'0:0:5'/**/", "/login?url=http://host-5c568da6.sdm.example.internal/\"and(select/**/1)>0/**/waitfor/**/delay\"0:0:5", "/login?url=http://host-5c568da6.sdm.example.internal/'and(select/**/1)>0/**/waitfor/**/delay'0:0:5", "/apis/login", "/api/strategys?pageSize=10&pageNumber=1&type=2&query=123'\"and(select/**/1)>0/**/waitfor/**/delay\"0:0:5", "/api/strategys?pageSize=10&pageNumber=1&type=2&query=123'/**/and(select/**/1)>0/**/waitfor/**/delay'0:0:5'/**/", "/api/strategys?pageSize=10&pageNumber=1&type=2&query=123''and(select/**/1)>0/**/waitfor/**/delay'0:0:5", "/api/strategys/ME454286696117313536/components?pageSize=10&pageNumber=1&type=2&query=123\"and(select/**/1)>0/**/waitfor/**/delay\"0:0:5", "/api/strategys/ME454286696117313536/components?pageSize=10&pageNumber=1&type=2&query=123'and(select/**/1)>0/**/waitfor/**/delay'0:0:5", "/api/strategys/ME462186493725777920/managers?pageSize=10'and(select/**/1)>0/**/waitfor/**/delay'0:0:5&pageNumber=1"] | `preserve_raw_and_review` | confirmed；按条目前导斜杠识别边界；不拼造完整 URL |
| `roles.related[].domain.name` | `transform` | `domain` | `parse_domain_list(wpl.domain)` -> ["host-349f2008.sdm.example.internal", "host-5c568da6.sdm.example.internal"] | `drop_invalid_items_and_review` | confirmed；关联域名不声明与目标 IP 的 DNS 关系 |
| `roles.observer.device.ip` | `transform` | `devIp` | `exactly_one(parse_ip_list(wpl.devIp))` -> "192.0.2.37" | `omit_and_review` | confirmed；观测设备 IP |
| `source_finding.title` | `projection` | `name` | "MSSQL Waitfor语句SQL注入攻击" | `—` | confirmed；来源告警标题 |
| `source_finding.severity` | `projection` | `severity` | "高危" | `—` | confirmed；来源严重度 |
| `source_finding.status` | `projection` | `disposeState` | "待处置" | `—` | confirmed；来源处置状态；未做字典归一 |
| `source_finding.count` | `transform` | `times` | `to_int(wpl.times)` -> 17 | `omit_and_review` | confirmed；聚合命中次数 |
| `source_finding.confidence` | `projection` | `confidence` | "中" | `—` | confirmed；来源置信度 |
| `source_finding.category.original.name` | `projection` | `ruleCategoryName` | "SQL注入" | `—` | confirmed；来源分类 |
| `source_finding.attacker.endpoint.ip` | `transform` | `attackerContent` | `exactly_one(parse_ip_list(wpl.attackerContent))` -> "192.0.2.238" | `omit_and_review` | confirmed；来源攻击方声明，与通信角色分开 |
| `source_finding.victim.endpoint.ip` | `transform` | `victimContent` | `exactly_one(parse_ip_list(wpl.victimContent))` -> "192.0.2.146" | `omit_and_review` | confirmed；来源受害方声明，与通信角色分开 |
| `source_finding.victim.geo` | `transform` | `dipGeo` | `geo_by_ip(parse_json(wpl.dipGeo),exactly_one(parse_ip_list(wpl.victimContent)))` -> {"continent": {"name": "北美洲"}, "country": {"name": "美国"}, "region": {"name": "俄亥俄州"}, "city": {"name": "哥伦布"}, "coordinates": {"latitude": 39.96120071411133, "longitude": -82.9988021850586}} | `omit_and_review` | confirmed；目标 Geo 按受害方 IP 取值 |
| `source_finding.rule.id` | `transform` | `ruleId` | `string(exactly_one(parse_integer_list(wpl.ruleId)))` -> "310189" | `omit_and_review` | confirmed；来源规则 ID |
| `source_finding.rule.label` | `transform` | `ruleName` | `exactly_one(parse_text_list(wpl.ruleName))` -> "MSSQL Waitfor语句SQL注入攻击" | `omit_and_review` | confirmed；与 ruleId 配对的来源检测规则名称 |
| `extensions.source_private.relevant_rule_name` | `projection` | `relevantRuleName` | "调整-网络探针检测到SQL注入事件" | `—` | confirmed；触发告警的关联规则名称；不与检测规则 ID 配对 |
| `source_finding.attention.content` | `projection` | `attentionValue` | "目的IP : 192.0.2.146" | `—` | confirmed；来源关注内容 |
| `source_finding.behavior` | `conditional` | `name/ruleCategoryName/uri` | `when wpl.name == "MSSQL Waitfor语句SQL注入攻击" && wpl.ruleCategoryName == "SQL注入" && any_all_contains(parse_uri_list(wpl.uri, entry_prefix="/"), ["waitfor", "delay"], case_insensitive=true) then chars(sql_injection) else omit` -> "sql_injection" | `omit` | confirmed；SQL 注入来源声明及 WAITFOR/DELAY 载荷 |
| `extensions.source_private.sql_injection_variant` | `conditional` | `name/ruleCategoryName/uri` | `when wpl.name == "MSSQL Waitfor语句SQL注入攻击" && wpl.ruleCategoryName == "SQL注入" && any_all_contains(parse_uri_list(wpl.uri, entry_prefix="/"), ["waitfor", "delay"], case_insensitive=true) then chars(mssql_waitfor_delay) else omit` -> "mssql_waitfor_delay" | `omit` | confirmed；名称和同一 URI 内的 WAITFOR/DELAY 子串共同确认 MSSQL 时间盲注变体 |
| `source_finding.killchain` | `dictionary` | `killchain` | "突防利用" -> "exploitation" | `preserve_in_extension_and_review` | partial；当前样例值映射 |
| `facets.network.direction` | `dictionary` | `commDirection` | "内到内" -> "L2L" | `preserve_in_extension_and_review` | partial；当前样例值映射 |
| `extensions.unmapped.att_ck_original` | `projection` | `attCk` | "[端点拒绝服务：服务耗竭洪流]" | `—` | confirmed；来源文本不是 ATT&CK 技术编号 |
| `extensions.source_private.wpl_update_time` | `projection` | `update_time` | "2026-12-18 16:01:02" | `—` | confirmed；WPL 从无年份 Syslog 头推断，仅供审计 |
| `extensions.source_private.latest_timestamp` | `projection` | `latestTimestamp` | 1734508616000 | `—` | confirmed；WPL 已转毫秒 |
| `extensions.source_private.relevant_log_types` | `transform` | `relevantLogsType` | `parse_text_list(wpl.relevantLogsType)` -> ["天堤网页漏洞利用日志"] | `preserve_raw_and_review` | confirmed；来源关联日志类型 |
| `extensions.source_private.relevant_asset_names` | `transform` | `relevantAssetsName` | `parse_text_list(wpl.relevantAssetsName)` -> ["衡阳农商行快贷系统"] | `preserve_raw_and_review` | confirmed；来源关联资产名称 |
| `extensions.source_private.relevant_asset_groups` | `transform` | `relevantAssetsGroup` | `parse_text_list(wpl.relevantAssetsGroup)` -> ["互联网业务区", "已删除", "湖南省联社"] | `preserve_raw_and_review` | confirmed；来源关联资产组 |
| `extensions.source_private.relevant_network_segments` | `transform` | `relevantNetworkSegmentId` | `parse_text_list(wpl.relevantNetworkSegmentId)` -> ["衡阳市中心办公网", "互联网业务区", "运维管理区"] | `preserve_raw_and_review` | confirmed；来源关联网络分区 |
| `source_alert_severity` | `transform` | `severity` | `string` -> "高危" | `—` | confirmed；保留来源 finding 原始严重度 |
| `severity` | `dictionary` | `severity` | "高危" -> "error" | `null_and_review` | partial；根据当前 NGSOC 样例分布推测的安全严重度交叉表，尚未经厂商确认 |
| `source_finding.attack_result` | `dictionary` | `attackResult` | "企图" -> "attempted" | `preserve_in_extension_and_review` | partial；检测到攻击尝试，但不声明动作成功 |
| `outcome` | `dictionary` | `attackResult` | "企图" -> "observed" | `unknown_and_review` | partial；检测到攻击尝试，但不声明动作成功 |

### 5.3 编写约束

- 字典仅覆盖当前样例值，完整厂商字典仍需确认。
- 多源端口不投影 source_port；多 URI 不拼造单一 URL。
- attCk 不是技术 ID，必须保留原值并等待字典确认。
- 不推断 HTTP 方法、传输协议、响应、阻断或 SQL 执行成功。
