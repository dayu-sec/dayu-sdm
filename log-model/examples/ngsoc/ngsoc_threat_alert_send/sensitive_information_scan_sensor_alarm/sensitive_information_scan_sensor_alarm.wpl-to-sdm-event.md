# WPL -> SDM Event 字段映射

详见同名 JSON 映射文件；Meta 与 Content 规则由 writer-facing 规则生成。

## 五、WPL/OML 编写规则

> WPL 只负责提取表中的 source 字段；Meta 和 Content 的赋值由 OML 按下表实现。
> `partial` 表示当前只有样例值或局部说明，不能视为完整厂商字典。

### 5.1 Meta 区

| SDM 字段 | 规则类型 | 输入/来源 | 赋值 | 未命中 | 状态与证据 |
|---|---|---|---|---|---|
| `event_id` | `derived` | `derived.sha256(tenant_id+'|'+mapping_id+'|'+wpl.uuid)` | `'evt-' + sha256(tenant_id+'|'+mapping_id+'|'+wpl.uuid)` -> "evt-dd2406481004afd4d1f5f79fc12ca0eb9b81b8593c39e631768bf6ba593d7e6e" | `—` | confirmed；来源 UUID 的确定性事件 ID |
| `record_kind` | `conditional` | `when wpl.name == "敏感信息扫描(机器学习)" && wpl.relevantLogsType[0] == "skyeye_platform_sensor_alarm"` | `when wpl.name == "敏感信息扫描(机器学习)" && wpl.relevantLogsType[0] == "skyeye_platform_sensor_alarm" then chars(finding) else no_match` -> "finding" | `no_match` | confirmed；NGSOC 来源告警 |
| `event_domain` | `conditional` | `when wpl.name == "敏感信息扫描(机器学习)" && wpl.relevantLogsType[0] == "skyeye_platform_sensor_alarm"` | `when wpl.name == "敏感信息扫描(机器学习)" && wpl.relevantLogsType[0] == "skyeye_platform_sensor_alarm" then chars(threat) else no_match` -> "threat" | `no_match` | confirmed；来源声明信息泄露风险 |
| `event_type` | `conditional` | `when wpl.name == "敏感信息扫描(机器学习)" && wpl.relevantLogsType[0] == "skyeye_platform_sensor_alarm"` | `when wpl.name == "敏感信息扫描(机器学习)" && wpl.relevantLogsType[0] == "skyeye_platform_sensor_alarm" then chars(network_http) else no_match` -> "network_http" | `no_match` | confirmed；payload 明确提供 HTTP 请求和响应 |
| `operation` | `constant` | `constant.empty_operation_for_network_http` | "" | `—` | confirmed；network_http 无可确认 subordinate operation |
| `roles.source.ref_id` | `derived` | `derived.entity_ref(endpoint,wpl.srcIp,extraFields.sport[0])` | `stable_endpoint_ref(wpl.srcIp,extraFields.sport[0])` -> "endpoint-6ca0b6362f653549e378f81f9f48dcf0" | `—` | confirmed；通信源端点稳定引用 |
| `roles.target.ref_id` | `derived` | `derived.entity_ref(endpoint,wpl.dstIp,extraFields.dport[0])` | `stable_endpoint_ref(wpl.dstIp,extraFields.dport[0])` -> "endpoint-9bc984e80bb20d13e7c8ed1ac918b4ad" | `—` | confirmed；通信目标端点稳定引用 |
| `roles.source.entity_type` | `constant` | `constant.roles_source_entity_type` | "endpoint" | `—` | confirmed；源 IP 与端口装配为 endpoint |
| `roles.target.entity_type` | `constant` | `constant.roles_target_entity_type` | "endpoint" | `—` | confirmed；目标 IP 与端口装配为 endpoint |
| `roles.carriers` | `constant` | `constant.roles_carriers` | [] | `—` | confirmed；没有进程或会话载体 |
| `roles.related` | `constant` | `constant.roles_related` | [] | `—` | confirmed；没有独立关联实体 |
| `roles.observer.product.name` | `constant` | `constant.roles_observer_product_name` | "NGSOC" | `—` | confirmed；来源产品 |
| `tenant_id` | `context` | `platform_context.tenant_id` | "" | `—` | data_gap；真实平台上下文未随样例提供；运行时由接入层赋值 |
| `ingest_time` | `context` | `platform_context.ingest_time` | `read(ingest_time)` | `—` | data_gap；真实平台上下文未随样例提供；运行时由接入层赋值 |
| `parse_time` | `context` | `platform_context.parse_time` | `read(parse_time)` | `—` | data_gap；真实平台上下文未随样例提供；运行时由接入层赋值 |
| `data_src_instance_id` | `context` | `platform_context.data_src_instance_id` | `read(data_src_instance_id)` | `—` | data_gap；真实平台上下文未随样例提供；运行时由接入层赋值 |
| `schema_version` | `constant` | `constant.schema_version` | 2 | `—` | confirmed；接入路由级常量 |
| `mapping_id` | `constant` | `constant.mapping_id` | "qax.ngsoc.ngsoc_threat_alert_send" | `—` | confirmed；接入路由级常量 |
| `data_src_vendor` | `constant` | `constant.data_src_vendor` | "qax" | `—` | confirmed；接入路由级常量 |
| `data_src_product` | `constant` | `constant.data_src_product` | "ngsoc" | `—` | confirmed；接入路由级常量 |
| `data_src_category` | `constant` | `constant.data_src_category` | "security_analytics" | `—` | confirmed；接入路由级常量 |
| `log_type` | `constant` | `constant.log_type` | "ngsoc_threat_alert_send" | `—` | confirmed；接入路由级常量 |
| `log_name` | `constant` | `constant.log_name` | "NGSOC告警信息" | `—` | confirmed；接入路由级常量 |
| `observer_vendor` | `constant` | `constant.observer_vendor` | "qax" | `—` | confirmed；接入路由级常量 |
| `observer_product` | `constant` | `constant.observer_product` | "ngsoc" | `—` | confirmed；接入路由级常量 |
| `log_level` | `gap` | `data_gap.no_source_log_level` | `null` | `—` | missing；来源没有独立日志等级字段 |

### 5.2 Content 区

| SDM 字段 | 规则类型 | WPL 字段 | 映射/赋值 | 未命中 | 状态与证据 |
|---|---|---|---|---|---|
| `log_id` | `projection` | `log_id` | "6b7ce09b425b401cb22672faacb9c4c0" | `—` | confirmed；WPL 来源日志标识 |
| `source_original_event_id` | `projection` | `uuid` | "91ac201a-b694-455a-af70-d04acbc7b62e" | `—` | confirmed；来源告警 UUID |
| `source_finding.original_id` | `projection` | `uuid` | "91ac201a-b694-455a-af70-d04acbc7b62e" | `—` | confirmed；来源 finding 原始 ID |
| `occur_time` | `projection` | `occur_time` | 1733307762233 | `—` | confirmed；WPL 已解析毫秒时间 |
| `roles.source.endpoint.ip` | `projection` | `srcIp` | "192.0.2.201" | `—` | confirmed；通信起点 IP |
| `source_ip` | `projection` | `roles.source.endpoint.ip` | "192.0.2.201" | `—` | confirmed；源 IP 热字段投影 |
| `roles.target.endpoint.ip` | `projection` | `dstIp` | "198.51.100.157" | `—` | confirmed；通信终点 IP |
| `target_ip` | `projection` | `roles.target.endpoint.ip` | "198.51.100.157" | `—` | confirmed；目标 IP 热字段投影 |
| `roles.source.endpoint.port` | `transform` | `extraFields.sport[0]` | `digit(exactly_one(wpl.extraFields.sport))` -> 34162 | `omit_and_review` | confirmed；源端口字符串转整数 |
| `source_port` | `projection` | `roles.source.endpoint.port` | 34162 | `—` | confirmed；源端口热字段投影 |
| `roles.target.endpoint.port` | `transform` | `extraFields.dport[0]` | `digit(exactly_one(wpl.extraFields.dport))` -> 80 | `omit_and_review` | confirmed；目标端口字符串转整数 |
| `target_port` | `projection` | `roles.target.endpoint.port` | 80 | `—` | confirmed；目标端口热字段投影 |
| `source_finding.attacker.endpoint.port` | `transform` | `extraFields.sport[0]` | `digit(exactly_one(wpl.extraFields.sport))` -> 34162 | `omit_and_review` | confirmed；来源攻击方端口字符串转整数，与通信源端口相同 |
| `source_finding.victim.endpoint.port` | `transform` | `extraFields.dport[0]` | `digit(exactly_one(wpl.extraFields.dport))` -> 80 | `omit_and_review` | confirmed；来源受害方端口字符串转整数，与通信目标端口相同 |
| `facets.http.request.method` | `transform` | `payload.httpReqHeader` | `http_request_line(payload.httpReqHeader).method` -> "GET" | `omit_http_method_and_review` | confirmed；extraFields.httpMethod 为空，从请求行提取 |
| `facets.http.request.path` | `transform` | `extraFields.uri[0]` | `exactly_one(wpl.extraFields.uri)` -> "/WEB-INF/web.xml" | `omit_http_path_and_review` | confirmed；WPL 结构化 URI 路径 |
| `facets.http.request.host` | `transform` | `payload.httpReqHeader` | `http_header(payload.httpReqHeader,'Host')` -> "198.51.100.157" | `omit_http_host_and_review` | confirmed；请求头 Host |
| `http_host` | `projection` | `facets.http.request.host` | "198.51.100.157" | `—` | confirmed；HTTP Host 热字段投影 |
| `facets.http.request.user_agent` | `transform` | `payload.httpReqHeader` | `http_header(payload.httpReqHeader,'User-Agent')` -> "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.5481.38 Safari/537.36" | `omit_user_agent_and_review` | confirmed；extraFields.httpUserAgent 为空，从请求头提取 |
| `facets.http.response.status_code` | `transform` | `extraFields.httpRspCode[0]` | `digit(exactly_one(wpl.extraFields.httpRspCode))` -> 503 | `omit_and_review` | confirmed；HTTP 503 响应，不证明信息泄露 |
| `facets.network.application_protocol` | `transform` | `extraFields.appProtocol[0]` | `uppercase(exactly_one(wpl.extraFields.appProtocol))` -> "HTTP" | `omit_and_review` | confirmed；来源应用层协议归一为大写 HTTP |
| `application_name` | `projection` | `facets.network.application_protocol` | "HTTP" | `—` | confirmed；应用名称热字段投影 |
| `facets.network.direction` | `dictionary` | `commDirection[0]` | "内到外" -> "L2W" | `extensions.unmapped.comm_direction=original_value_and_review` | confirmed；NGSOC-4.13.1 厂商字典映射 |
| `source_finding.title` | `projection` | `name` | "敏感信息扫描(机器学习)" | `—` | confirmed；来源告警标题 |
| `source_finding.severity` | `transform` | `severity` | `string(wpl.severity)` -> "1" | `—` | confirmed；WPL severity 为 digit；转字符串保留来源数值，不覆盖顶层 severity |
| `source_finding.confidence` | `projection` | `confidence` | "3" | `—` | confirmed；保留来源数值置信度 |
| `extensions.unmapped.killchain` | `dictionary_candidate` | `killchain` | "1" | `preserve_original_value_and_review` | confirmed；厂商字典未确认 |
| `source_finding.attacker.geo` | `transform` | `sipGeo[srcIp]` | `geoip_object(exactly_one(wpl.sipGeo[srcIp]))` -> {"continent": {"name": "保留IP"}, "coordinates": {"latitude": 0.0, "longitude": 0.0}} | `omit_geo_and_review` | confirmed；攻击方 GeoIP；空地域名省略，经纬度字符串转数值 |
| `source_finding.victim.geo` | `transform` | `dipGeo[dstIp]` | `geoip_object(exactly_one(wpl.dipGeo[dstIp]))` -> {"continent": {"name": "亚洲"}, "country": {"name": "新加坡"}, "region": {"name": "新加坡"}, "city": {"name": "新加坡"}, "coordinates": {"latitude": 1.2865300178527832, "longitude": 103.85399627685547}} | `omit_geo_and_review` | confirmed；受害方 GeoIP 经纬度转数值 |
| `source_finding.attention.content` | `transform` | `attentionValue` | `format_attention(exactly_one(wpl.attentionValue.源IP))` -> "源IP : 192.0.2.201" | `omit_and_review` | confirmed；来源关注内容 |
| `roles.observer.device.ip` | `projection` | `access_ip` | "198.51.100.185" | `—` | confirmed；WPL 从 devIp[0] 提取设备 IP |
| `roles.observer.device.name` | `projection` | `extraFields.devName[0]` | "奇安信网神新一代威胁感知系统" | `omit_and_review` | confirmed；观测设备名称 |
| `roles.observer.device.vendor` | `dictionary` | `extraFields.devVendor[0]` | "奇安信" -> "qax" | `omit_vendor_and_review` | confirmed；设备厂商中文名归一为 qax |
| `source_finding.category.original.code` | `projection` | `ruleCategoryId` | "376b269e-ac3a-4759-9752-f2b30cb54d58" | `—` | confirmed；来源分类代码 |
| `source_finding.category.original.name` | `projection` | `ruleCategoryName` | "信息泄露" | `—` | confirmed；来源分类名称 |
| `source_finding.rule.id` | `projection` | `relevantRuleId` | "413e0032-268d-4b9d-b6e1-51ce20adc281" | `—` | confirmed；来源规则 ID |
| `source_finding.rule.label` | `projection` | `relevantRuleName` | "预置-天眼分析平台信息泄露事件" | `—` | confirmed；来源规则名称 |
| `source_finding.count` | `projection` | `relevantLogsNum` | 1 | `—` | confirmed；关联日志数量 |
| `extensions.source_private.relevant_log_count` | `projection` | `relevantLogsNum` | 1 | `—` | confirmed；关联日志数量原值保留 |
| `extensions.source_private.relevant_log_types` | `projection` | `relevantLogsType` | ["skyeye_platform_sensor_alarm"] | `—` | confirmed；关联日志类型 |
| `extensions.source_private.log_start_time` | `projection` | `logStartTime` | 1733307676000 | `—` | confirmed；聚合窗口起点 |
| `extensions.source_private.log_end_time` | `projection` | `logEndTime` | 1733307676000 | `—` | confirmed；聚合窗口终点 |
| `extensions.source_private.merge_key` | `projection` | `mergeKey` | "8229e4a5109144c3fc48c9522feec38f" | `—` | confirmed；NGSOC 聚合键 |
| `extensions.source_private.source` | `projection` | `source` | 0 | `—` | confirmed；NGSOC 来源代码 |
| `extensions.source_private.payload_log_type` | `projection` | `type` | "ngsoc_alert_info" | `—` | confirmed；载荷日志类型 |
| `source_finding.mitre.technique_id` | `projection` | `attCk` | "T1190" | `—` | confirmed；来源值符合 ATT&CK technique ID 格式 |
| `source_alert_severity` | `transform` | `severity` | `string` -> "1" | `—` | confirmed；保留来源 finding 原始严重度 |
| `severity` | `dictionary` | `severity` | 1 -> "notice" | `null_and_review` | confirmed；根据当前 NGSOC 样例分布推测的安全严重度交叉表，由 NGSOC-4.13.1 厂商文档确认 |
| `extensions.unmapped.attack_result` | `projection` | `attackResult` | "3" | `—` | confirmed；当前样例同时声明 compromiseState=false，不能推测为失陷或成功 |
| `outcome` | `gap` | `attackResult + compromiseState` | "unknown" | `unknown` | confirmed；当前样例同时声明 compromiseState=false，不能推测为失陷或成功 |
| `source_finding.compromise_status` | `dictionary` | `compromiseState` | "false" -> "not_compromised" | `preserve_in_extension_and_review` | confirmed；布尔值及中文值按当前样例语义推测，由 NGSOC-4.13.1 厂商文档确认 |

### 5.3 编写约束

- HTTP 方法从 payload 请求行提取，路径优先使用 extraFields.uri，Host/User-Agent 从请求头提取；响应码来自 extraFields。
- extraFields.appProtocol=HTTP 仅表示应用层协议，传输协议仍未知。
- `attackResult=3` 由 NGSOC-4.13.1 厂商字典确认，归一为 `source_finding.attack_result=failed`。
- HTTP 503 不证明敏感信息已经泄露。
