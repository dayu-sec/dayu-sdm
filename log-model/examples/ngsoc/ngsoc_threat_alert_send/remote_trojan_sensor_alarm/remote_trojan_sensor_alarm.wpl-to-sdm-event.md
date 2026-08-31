# WPL -> SDM Event 字段映射

详见同名 JSON 映射文件。

## 五、WPL/OML 编写规则

> WPL 只负责提取表中的 source 字段；Meta 和 Content 的赋值由 OML 按下表实现。
> `partial` 表示当前只有样例值或局部说明，不能视为完整厂商字典。

### 5.1 Meta 区

| SDM 字段 | 规则类型 | 输入/来源 | 赋值 | 未命中 | 状态与证据 |
|---|---|---|---|---|---|
| `event_id` | `derived` | `derived.sha256(tenant_id+'|'+mapping_id+'|'+wpl.uuid)` | `'evt-' + sha256(tenant_id+'|'+mapping_id+'|'+wpl.uuid)` -> "evt-cad901546e8641c198fe031669a089f7de4b4541a18ed896f4d70f492ee5a872" | `—` | confirmed；来源 UUID 的确定性事件 ID |
| `record_kind` | `conditional` | `when wpl.name == "普通远控木马活动事件" && wpl.relevantLogsType[0] == "skyeye_platform_sensor_alarm"` | `when wpl.name == "普通远控木马活动事件" && wpl.relevantLogsType[0] == "skyeye_platform_sensor_alarm" then chars(finding) else no_match` -> "finding" | `—` | confirmed；NGSOC 来源告警 |
| `event_domain` | `conditional` | `when wpl.name == "普通远控木马活动事件" && wpl.relevantLogsType[0] == "skyeye_platform_sensor_alarm"` | `when wpl.name == "普通远控木马活动事件" && wpl.relevantLogsType[0] == "skyeye_platform_sensor_alarm" then chars(threat) else no_match` -> "threat" | `—` | confirmed；来源威胁告警 |
| `event_type` | `conditional` | `when wpl.name == "普通远控木马活动事件" && wpl.relevantLogsType[0] == "skyeye_platform_sensor_alarm"` | `when wpl.name == "普通远控木马活动事件" && wpl.relevantLogsType[0] == "skyeye_platform_sensor_alarm" then chars(network_connection) else no_match` -> "network_connection" | `—` | confirmed；只有网络端点和端口，无 HTTP/协议载体 |
| `operation` | `constant` | `constant.network_connection_traffic` | "traffic" | `—` | confirmed；告警描述声明网络通信 |
| `roles.source.ref_id` | `derived` | `derived.entity_ref(endpoint,wpl.srcIp,extraFields.sport[0])` | `stable_endpoint_ref(wpl.srcIp,extraFields.sport[0])` -> "endpoint-4c06508fc66e2c0fc536ddefc30db973" | `—` | confirmed；源端点引用 |
| `roles.target.ref_id` | `derived` | `derived.entity_ref(endpoint,wpl.dstIp,extraFields.dport[0])` | `stable_endpoint_ref(wpl.dstIp,extraFields.dport[0])` -> "endpoint-eff82c96501dd8a5ad7f68852311e61c" | `—` | confirmed；目标端点引用 |
| `roles.source.entity_type` | `constant` | `constant.endpoint_entity_type` | "endpoint" | `—` | confirmed；源端点类型 |
| `roles.target.entity_type` | `constant` | `constant.endpoint_entity_type` | "endpoint" | `—` | confirmed；目标端点类型 |
| `roles.carriers` | `constant` | `constant.empty_carriers` | [] | `—` | confirmed；无进程、会话或协议载体 |
| `roles.related` | `constant` | `constant.empty_related` | [] | `—` | confirmed；无独立关联实体 |
| `roles.observer.product.name` | `constant` | `constant.observer_product_display_name` | "NGSOC" | `—` | confirmed；来源产品 |
| `tenant_id` | `context` | `platform_context.tenant_id` | "" | `—` | data_gap；真实平台上下文未提供；运行时赋值 |
| `ingest_time` | `context` | `platform_context.ingest_time` | `read(ingest_time)` | `—` | data_gap；真实平台上下文未提供；运行时赋值 |
| `parse_time` | `context` | `platform_context.parse_time` | `read(parse_time)` | `—` | data_gap；真实平台上下文未提供；运行时赋值 |
| `data_src_instance_id` | `context` | `platform_context.data_src_instance_id` | `read(data_src_instance_id)` | `—` | data_gap；真实平台上下文未提供；运行时赋值 |
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
| `log_id` | `projection` | `log_id` | "7a74297cb35c48208e135a2f72158bf2" | `—` | confirmed；WPL 来源日志标识 |
| `source_original_event_id` | `projection` | `uuid` | "4c1ea437-f21b-4a0e-8b4f-7181ae7c7c5e" | `—` | confirmed；来源 UUID |
| `source_finding.original_id` | `projection` | `uuid` | "4c1ea437-f21b-4a0e-8b4f-7181ae7c7c5e" | `—` | confirmed；来源 finding 原始 ID |
| `occur_time` | `projection` | `occur_time` | 1733307762233 | `—` | confirmed；WPL 毫秒事件时间 |
| `roles.source.endpoint.ip` | `projection` | `srcIp` | "192.0.2.254" | `—` | confirmed；通信源 IP |
| `source_ip` | `projection` | `roles.source.endpoint.ip` | "192.0.2.254" | `—` | confirmed；源 IP 热字段 |
| `roles.target.endpoint.ip` | `projection` | `dstIp` | "203.0.113.121" | `—` | confirmed；通信目标 IP |
| `target_ip` | `projection` | `roles.target.endpoint.ip` | "203.0.113.121" | `—` | confirmed；目标 IP 热字段 |
| `roles.source.endpoint.port` | `transform` | `extraFields.sport[0]` | `digit(exactly_one(wpl.extraFields.sport))` -> 24617 | `omit_and_review` | confirmed；源端口字符串转整数 |
| `source_port` | `projection` | `roles.source.endpoint.port` | 24617 | `—` | confirmed；源端口热字段 |
| `roles.target.endpoint.port` | `transform` | `extraFields.dport[0]` | `digit(exactly_one(wpl.extraFields.dport))` -> 443 | `omit_and_review` | confirmed；目标端口字符串转整数 |
| `target_port` | `projection` | `roles.target.endpoint.port` | 443 | `—` | confirmed；目标端口热字段 |
| `source_finding.attacker.endpoint.port` | `transform` | `extraFields.dport[0]` | `digit(exactly_one(wpl.extraFields.dport))` -> 443 | `omit_and_review` | confirmed；攻击方端口来自通信目标端口 |
| `source_finding.victim.endpoint.port` | `transform` | `extraFields.sport[0]` | `digit(exactly_one(wpl.extraFields.sport))` -> 24617 | `omit_and_review` | confirmed；受害方端口来自通信源端口 |
| `roles.source.endpoint.mac` | `projection` | `extraFields.smac[0]` | "00:50:56:81:e3:8c" | `omit_and_review` | confirmed；源端 MAC |
| `roles.target.endpoint.mac` | `projection` | `extraFields.dmac[0]` | "cc:d8:1f:44:38:48" | `omit_and_review` | confirmed；目标端 MAC |
| `facets.network.direction` | `dictionary` | `commDirection[0]` | "内到外" -> "L2W" | `preserve_original_value_and_review` | confirmed；当前样例网络方向 |
| `source_finding.title` | `projection` | `name` | "普通远控木马活动事件" | `—` | confirmed；告警标题 |
| `source_finding.severity` | `transform` | `severity` | `string(wpl.severity)` -> "3" | `—` | confirmed；来源数字严重度转字符串 |
| `source_finding.confidence` | `projection` | `confidence` | "3" | `—` | confirmed；来源置信度 |
| `source_finding.attacker.endpoint.ip` | `projection` | `attackerContent` | "203.0.113.121" | `—` | confirmed；来源攻击方声明 |
| `source_finding.victim.endpoint.ip` | `projection` | `victimContent` | "192.0.2.254" | `—` | confirmed；来源受害方声明 |
| `source_finding.attacker.geo` | `transform` | `dipGeo[dstIp]` | `geoip_object(exactly_one(wpl.dipGeo[dstIp]))` -> {"continent": {"name": "亚洲"}, "country": {"name": "中国"}, "region": {"name": "北京市"}, "city": {"name": "北京市"}, "coordinates": {"latitude": 39.902801513671875, "longitude": 116.4010009765625}} | `—` | confirmed；攻击方 GeoIP |
| `source_finding.victim.geo` | `transform` | `sipGeo[srcIp]` | `geoip_object(exactly_one(wpl.sipGeo[srcIp]))` -> {"continent": {"name": "保留IP"}, "coordinates": {"latitude": 0.0, "longitude": 0.0}} | `—` | confirmed；受害方 GeoIP 来自 sipGeo；空地域名省略，经纬度字符串转数值 |
| `source_finding.ioc.value` | `projection` | `ioc` | "203.0.113.121:443" | `—` | confirmed；来源 IOC 值 |
| `source_finding.ioc.type` | `projection` | `iocType` | "dip:dport" | `—` | confirmed；来源 IOC 类型 |
| `source_finding.malware.name` | `projection` | `extraFields.maliciousFamily[0]` | "Generic Trojan" | `—` | confirmed；恶意家族 |
| `roles.observer.device.ip` | `projection` | `access_ip` | "198.51.100.185" | `—` | confirmed；观测设备 IP |
| `roles.observer.device.name` | `projection` | `extraFields.devName[0]` | "奇安信网神新一代威胁感知系统" | `omit_and_review` | confirmed；观测设备名称 |
| `roles.observer.device.vendor` | `dictionary` | `extraFields.devVendor[0]` | "奇安信" -> "qax" | `omit_vendor_and_review` | confirmed；设备厂商中文名归一为 qax |
| `source_finding.attention.content` | `transform` | `attentionValue` | `format_attention(exactly_one(wpl.attentionValue.源IP))` -> "源IP : 192.0.2.254" | `—` | confirmed；来源关注内容 |
| `source_finding.attack_direction` | `constant` | `constant.W2L_from_attacker_victim` | "W2L" | `—` | confirmed；来源 attacker/victim 明确外部攻击方、内部受害方 |
| `extensions.unmapped.killchain` | `dictionary_candidate` | `killchain` | "6" | `preserve_original_value_and_review` | confirmed；厂商数值字典未确认 |
| `source_finding.category.original.code` | `projection` | `ruleCategoryId` | "cccfe07f-802d-4510-9b53-388faf6533d9" | `—` | confirmed；分类代码 |
| `source_finding.category.original.name` | `projection` | `ruleCategoryName` | "远控木马" | `—` | confirmed；分类名称 |
| `source_finding.rule.id` | `projection` | `relevantRuleId` | "0862f5ae-d906-4336-931b-7be358dd0905" | `—` | confirmed；规则 ID |
| `source_finding.rule.label` | `projection` | `relevantRuleName` | "预置-天眼分析平台远控木马事件" | `—` | confirmed；规则名称 |
| `source_finding.count` | `projection` | `relevantLogsNum` | 1 | `—` | confirmed；关联日志数量 |
| `extensions.source_private.relevant_log_count` | `projection` | `relevantLogsNum` | 1 | `—` | confirmed；关联日志数量原值保留 |
| `extensions.source_private.relevant_log_types` | `projection` | `relevantLogsType` | ["skyeye_platform_sensor_alarm"] | `—` | confirmed；关联日志类型 |
| `extensions.source_private.log_start_time` | `projection` | `logStartTime` | 1733307658000 | `—` | confirmed；聚合窗口起点 |
| `extensions.source_private.log_end_time` | `projection` | `logEndTime` | 1733307658000 | `—` | confirmed；聚合窗口终点 |
| `extensions.source_private.merge_key` | `projection` | `mergeKey` | "1c5cd18ecd09c89a15f281c823b5f54c" | `—` | confirmed；聚合键 |
| `extensions.source_private.source` | `projection` | `source` | 0 | `—` | confirmed；来源代码 |
| `extensions.source_private.payload_log_type` | `projection` | `type` | "ngsoc_alert_info" | `—` | confirmed；载荷类型 |
| `source_finding.mitre.technique_id` | `projection` | `attCk` | "T1587.001" | `—` | confirmed；来源值符合 ATT&CK technique/sub-technique ID 格式 |
| `source_alert_severity` | `transform` | `severity` | `string` -> "3" | `—` | confirmed；保留来源 finding 原始严重度 |
| `severity` | `dictionary` | `severity` | 3 -> "error" | `null_and_review` | confirmed；根据当前 NGSOC 样例分布推测的安全严重度交叉表，由 NGSOC-4.13.1 厂商文档确认 |
| `source_finding.attack_result` | `dictionary` | `attackResult` | "1" -> "success" | `preserve_in_extension_and_review` | confirmed；按当前设备类型候选字典推测攻击结果 |
| `outcome` | `dictionary` | `attackResult` | "1" -> "success" | `unknown_and_review` | confirmed；按当前设备类型候选字典推测攻击结果 |
| `source_finding.compromise_status` | `dictionary` | `compromiseState` | "false" -> "not_compromised" | `preserve_in_extension_and_review` | confirmed；布尔值及中文值按当前样例语义推测，由 NGSOC-4.13.1 厂商文档确认 |

### 5.3 编写约束

- 通信 source/target 按观测方向保留；attacker/victim 按来源声明独立投影。
- `attackResult=1` 由 NGSOC-4.13.1 厂商字典确认，归一为 `source_finding.attack_result=success`。
- payload 无 HTTP 请求证据，不生成 HTTP facet。
