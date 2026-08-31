# WPL -> SDM Event 字段映射

详见同名 JSON 映射文件；Meta 与 Content 规则由 writer-facing 规则生成。

## 五、WPL/OML 编写规则

> WPL 只负责提取表中的 source 字段；Meta 和 Content 的赋值由 OML 按下表实现。
> `partial` 表示当前只有样例值或局部说明，不能视为完整厂商字典。

### 5.1 Meta 区

| SDM 字段 | 规则类型 | 输入/来源 | 赋值 | 未命中 | 状态与证据 |
|---|---|---|---|---|---|
| `event_id` | `derived` | `derived.sha256(tenant_id+'|'+mapping_id+'|'+wpl.uuid)` | `'evt-' + sha256(tenant_id+'|'+mapping_id+'|'+wpl.uuid)` -> "evt-db93ae606d498edfcbe1e160f8ed7cb62b0b2833f8efddf9b0b508a7d90ce52e" | `—` | confirmed；来源 UUID 的确定性事件 ID |
| `record_kind` | `conditional` | `when wpl.name == "发现黑客工具Nmap扫描行为" && wpl.relevantLogsType[0] == "flow_td_attack"` | `when wpl.name == "发现黑客工具Nmap扫描行为" && wpl.relevantLogsType[0] == "flow_td_attack" then chars(finding) else no_match` -> "finding" | `no_match` | confirmed；NGSOC 来源告警 |
| `event_domain` | `conditional` | `when wpl.name == "发现黑客工具Nmap扫描行为" && wpl.relevantLogsType[0] == "flow_td_attack"` | `when wpl.name == "发现黑客工具Nmap扫描行为" && wpl.relevantLogsType[0] == "flow_td_attack" then chars(threat) else no_match` -> "threat" | `no_match` | confirmed；来源网络扫描告警 |
| `event_type` | `conditional` | `when wpl.name == "发现黑客工具Nmap扫描行为" && wpl.relevantLogsType[0] == "flow_td_attack"` | `when wpl.name == "发现黑客工具Nmap扫描行为" && wpl.relevantLogsType[0] == "flow_td_attack" then chars(scan_network) else no_match` -> "scan_network" | `no_match` | confirmed；来源行为是网络扫描 |
| `operation` | `constant` | `constant.empty_operation_for_scan_network` | "" | `—` | confirmed；没有扫描生命周期动作证据 |
| `roles.source.ref_id` | `derived` | `derived.entity_ref(endpoint,wpl.srcIp,extraFields.sport[0])` | `stable_endpoint_ref(wpl.srcIp,extraFields.sport[0])` -> "endpoint-ccfbc9304839dd06828d23bb1e3a717d" | `—` | confirmed；源端点稳定引用 |
| `roles.target.ref_id` | `derived` | `derived.entity_ref(endpoint,wpl.dstIp,extraFields.dport[0])` | `stable_endpoint_ref(wpl.dstIp,extraFields.dport[0])` -> "endpoint-de1538c76c86c3a37ad4f9021c3779fb" | `—` | confirmed；目标端点稳定引用 |
| `roles.source.entity_type` | `constant` | `constant.roles_source_entity_type` | "endpoint" | `—` | confirmed；源 IP 与端口装配为 endpoint |
| `roles.target.entity_type` | `constant` | `constant.roles_target_entity_type` | "endpoint" | `—` | confirmed；目标 IP 与端口装配为 endpoint |
| `roles.carriers` | `constant` | `constant.roles_carriers` | [] | `—` | confirmed；无独立进程、会话或脚本载体 |
| `roles.related` | `constant` | `constant.roles_related` | [] | `—` | confirmed；无独立关联实体 |
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
| `log_id` | `projection` | `log_id` | "86da5a8ac01946968748414922c5f8b3" | `—` | confirmed；WPL 来源日志标识 |
| `source_original_event_id` | `projection` | `uuid` | "1a673139-914d-415b-8cfc-c53bee93231b" | `—` | confirmed；来源告警 UUID |
| `source_finding.original_id` | `projection` | `uuid` | "1a673139-914d-415b-8cfc-c53bee93231b" | `—` | confirmed；来源 finding 原始 ID |
| `occur_time` | `projection` | `occur_time` | 1733307762255 | `—` | confirmed；WPL 已解析毫秒时间 |
| `roles.source.endpoint.ip` | `projection` | `srcIp` | "192.0.2.140" | `—` | confirmed；通信源 IP |
| `source_ip` | `projection` | `roles.source.endpoint.ip` | "192.0.2.140" | `—` | confirmed；源 IP 热字段投影 |
| `roles.target.endpoint.ip` | `projection` | `dstIp` | "203.0.113.215" | `—` | confirmed；通信目标 IP |
| `target_ip` | `projection` | `roles.target.endpoint.ip` | "203.0.113.215" | `—` | confirmed；目标 IP 热字段投影 |
| `source_finding.attacker.endpoint.ip` | `projection` | `attackerContent` | "192.0.2.140" | `—` | confirmed；来源攻击方声明 |
| `source_finding.victim.endpoint.ip` | `projection` | `victimContent` | "203.0.113.215" | `—` | confirmed；来源受害方声明 |
| `roles.source.endpoint.port` | `transform` | `extraFields.sport[0]` | `digit(exactly_one(wpl.extraFields.sport))` -> 54128 | `omit_and_review` | confirmed；源端口字符串转整数 |
| `source_port` | `projection` | `roles.source.endpoint.port` | 54128 | `—` | confirmed；源端口热字段投影 |
| `roles.target.endpoint.port` | `transform` | `extraFields.dport[0]` | `digit(exactly_one(wpl.extraFields.dport))` -> 17854 | `omit_and_review` | confirmed；目标端口字符串转整数 |
| `target_port` | `projection` | `roles.target.endpoint.port` | 17854 | `—` | confirmed；目标端口热字段投影 |
| `source_finding.attacker.endpoint.port` | `transform` | `extraFields.sport[0]` | `digit(exactly_one(wpl.extraFields.sport))` -> 54128 | `omit_and_review` | confirmed；来源攻击方端口与通信源端口相同 |
| `source_finding.victim.endpoint.port` | `transform` | `extraFields.dport[0]` | `digit(exactly_one(wpl.extraFields.dport))` -> 17854 | `omit_and_review` | confirmed；来源受害方端口与通信目标端口相同 |
| `roles.source.endpoint.mac` | `projection` | `extraFields.smac[0]` | "00:0c:29:2f:93:bb" | `omit_and_review` | confirmed；源端 MAC |
| `roles.target.endpoint.mac` | `projection` | `extraFields.dmac[0]` | "5c:c9:99:bd:68:93" | `omit_and_review` | confirmed；目标端 MAC |
| `facets.network.protocol` | `transform` | `payload.packetData` | `uppercase(sip_via_transport(payload.packetData))` -> "TCP" | `omit_protocol_and_review` | confirmed；packetData 的 SIP Via 明确为 TCP |
| `network_protocol` | `projection` | `facets.network.protocol` | "TCP" | `—` | confirmed；网络协议热字段投影 |
| `facets.network.application_protocol` | `dictionary` | `sip_request_line(payload.packetData).protocol` | "SIP/2.0" -> "SIP" | `omit_application_protocol_and_review` | confirmed；packetData 请求行协议 SIP/2.0 归一为协议族 SIP |
| `application_name` | `projection` | `facets.network.application_protocol` | "SIP" | `—` | confirmed；应用名称热字段投影 |
| `extensions.unmapped.app_protocol_original` | `projection` | `extraFields.appProtocol[0]` | "UNKNOW" | `—` | confirmed；厂商哨兵值保留，不作为标准协议 |
| `facets.network.direction` | `dictionary` | `commDirection[0]` | "内到外" -> "L2W" | `extensions.unmapped.comm_direction=original_value_and_review` | confirmed；NGSOC-4.13.1 厂商字典映射 |
| `source_finding.title` | `projection` | `name` | "发现黑客工具Nmap扫描行为" | `—` | confirmed；来源告警标题 |
| `source_finding.severity` | `transform` | `severity` | `string(wpl.severity)` -> "1" | `—` | confirmed；WPL severity 为 digit；转字符串保留来源数值 |
| `source_finding.confidence` | `projection` | `confidence` | "2" | `—` | confirmed；保留来源数值置信度 |
| `extensions.unmapped.killchain` | `dictionary_candidate` | `killchain` | "1" | `preserve_original_value_and_review` | confirmed；厂商字典未确认 |
| `source_finding.victim.geo` | `transform` | `dipGeo[dstIp]` | `geoip_object(exactly_one(wpl.dipGeo[dstIp]))` -> {"continent": {"name": "亚洲"}, "country": {"name": "中国"}, "region": {"name": "内蒙古自治区"}, "city": {"name": "呼和浩特市"}, "coordinates": {"latitude": 40.8213005065918, "longitude": 111.64700317382812}} | `omit_geo_and_review` | confirmed；目标 GeoIP 经纬度转数值 |
| `source_finding.attention.content` | `transform` | `attentionValue` | `format_attention(exactly_one(wpl.attentionValue.目的IP))` -> "目的IP : 203.0.113.215" | `omit_and_review` | confirmed；来源关注内容 |
| `roles.observer.device.ip` | `projection` | `access_ip` | "192.0.2.30" | `—` | confirmed；WPL 观测设备 IP |
| `roles.observer.device.name` | `projection` | `extraFields.devName[0]` | "天眼流量传感器" | `omit_and_review` | confirmed；观测设备名称 |
| `roles.observer.device.vendor` | `dictionary` | `extraFields.devVendor[0]` | "奇安信" -> "qax" | `omit_vendor_and_review` | confirmed；设备厂商中文名归一为 qax |
| `source_finding.category.original.code` | `projection` | `ruleCategoryId` | "e3ec94c7-2bdc-49d0-8957-cef7a89696da" | `—` | confirmed；来源分类代码 |
| `source_finding.category.original.name` | `projection` | `ruleCategoryName` | "黑市工具" | `—` | confirmed；来源分类名称 |
| `source_finding.rule.id` | `projection` | `relevantRuleId` | "cb06eb0d-d1c9-4532-8074-fb640c8e2045" | `—` | confirmed；来源规则 ID |
| `source_finding.rule.label` | `projection` | `relevantRuleName` | "预置-网络探针检测到黑市工具事件" | `—` | confirmed；来源规则名称 |
| `source_finding.mitre.technique_id` | `projection` | `attCk` | "T1587.004" | `—` | confirmed；WPL 已将 raw attCk[0] 投影为标量 |
| `source_finding.count` | `projection` | `relevantLogsNum` | 1 | `—` | confirmed；关联日志数量 |
| `extensions.source_private.relevant_log_count` | `projection` | `relevantLogsNum` | 1 | `—` | confirmed；关联日志数量原值保留 |
| `extensions.source_private.relevant_log_types` | `projection` | `relevantLogsType` | ["flow_td_attack"] | `—` | confirmed；关联日志类型 |
| `extensions.source_private.log_start_time` | `projection` | `logStartTime` | 1733307658000 | `—` | confirmed；聚合窗口起点 |
| `extensions.source_private.log_end_time` | `projection` | `logEndTime` | 1733307658000 | `—` | confirmed；聚合窗口终点 |
| `extensions.source_private.merge_key` | `projection` | `mergeKey` | "b8cf1f0fe917e8c9c2535435a0dc167c" | `—` | confirmed；NGSOC 聚合键 |
| `extensions.source_private.source` | `projection` | `source` | 0 | `—` | confirmed；NGSOC 来源代码 |
| `extensions.source_private.payload_log_type` | `projection` | `type` | "ngsoc_alert_info" | `—` | confirmed；载荷日志类型 |
| `source_alert_severity` | `transform` | `severity` | `string` -> "1" | `—` | confirmed；保留来源 finding 原始严重度 |
| `severity` | `dictionary` | `severity` | 1 -> "notice" | `null_and_review` | confirmed；根据当前 NGSOC 样例分布推测的安全严重度交叉表，由 NGSOC-4.13.1 厂商文档确认 |
| `source_finding.attack_result` | `dictionary` | `attackResult` | "2" -> "attempted" | `preserve_in_extension_and_review` | confirmed；按当前设备类型候选字典推测攻击结果 |
| `outcome` | `dictionary` | `attackResult` | "2" -> "observed" | `unknown_and_review` | confirmed；按当前设备类型候选字典推测攻击结果 |
| `source_finding.compromise_status` | `dictionary` | `compromiseState` | "false" -> "not_compromised" | `preserve_in_extension_and_review` | confirmed；布尔值及中文值按当前样例语义推测，由 NGSOC-4.13.1 厂商文档确认 |

### 5.3 编写约束

- event_type 使用 scan_network；不把告警名称直接建模为 Nmap 进程。
- packetData 明确含 SIP/2.0 请求行和 Via SIP/2.0/TCP；SIP/2.0 通过协议族字典归一为 SIP，extraFields.appProtocol=UNKNOW 仅保留原值。
- sipGeo 的 保留IP 和 0,0 是私网 Geo 哨兵值，不写入标准 Geo。
- attackResult=2、killchain=1、compromiseState=false 未有厂商字典，原值保留，不驱动标准 outcome。
