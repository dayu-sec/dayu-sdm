# WPL -> SDM Event 字段映射

> 样例：`slow_outbound_large_data_transfer.expected-sdm-event.behavior.json（现行）；旧 `*.expected-sdm-event.json` 为 55 列对照`。机器可读 JSON 记录全部 `67` 个 WPL 字段的处理结论。

## 核心字段

| WPL 来源 | SDM 落位 | 转换 | 说明 |
|---|---|---|---|
| `timestamp` | `occur_time` | 按 Asia/Shanghai 转毫秒 | 聚合 finding 时间 |
| `srcIp` | `roles.source.endpoint.ip`、`source_ip` | 取唯一 IP | 通信主体 |
| `dstIp/dport` | `roles.target.endpoint`、`target_ip/target_port` | 分别取唯一值 | 通信客体 |
| `protocol` | `facets.network.application_protocol` | `http` 小写归一 | 应用层协议，不写入传输协议 |
| `commDirection` | `facets.network.direction` | `内到外 -> L2W` | 局部字典并保留原值 |
| `sport` | `extensions.source_private.source_ports` | 解析整数列表 | 多值不投影单一 source_port |
| `name` | `source_finding.behavior`、`extensions.source_private.transfer_profile` | 定性标签 | 不生成 bytes、duration 或 rate |
| `sipGeo/dipGeo` | `roles.source.geo/roles.target.geo` | 按 IP 关联并规范化 | 来源 Geo，不是平台富化 |

## 映射边界

- 不把 source/target 自动解释为 attacker/victim。
- 不把 `times` 解释为传输字节数。
- 不把 `http` 写入表示 TCP/UDP 的 `network_protocol`。
- Meta 和 Content 的逐字段赋值规则见下方生成表。

## 五、WPL/OML 编写规则

> WPL 只负责提取表中的 source 字段；Meta 和 Content 的赋值由 OML 按下表实现。
> `partial` 表示当前只有样例值或局部说明，不能视为完整厂商字典。

### 5.1 Meta 区

| SDM 字段 | 规则类型 | 输入/来源 | 赋值 | 未命中 | 状态与证据 |
|---|---|---|---|---|---|
| `event_id` | `derived` | `derived.sha256(tenant_id+'|'+mapping_id+'|'+wpl.seq)` | `'evt-' + sha256(tenant_id+'|'+mapping_id+'|'+wpl.seq)` -> "evt-f5381df77f91df596587de91d075c5db65a251c67e32c6914926908ce61b12f2" | `—` | confirmed；来源序列驱动的确定性事件 ID |
| `record_kind` | `conditional` | `when wpl.name == "预置-网络探针检测到内部主机对外慢速传输大量数据" && wpl.ruleCategoryName == "流量异常" && exactly_one(parse_ip_list(wpl.srcIp)) != '' && exactly_one(parse_ip_list(wpl.dstIp)) != ''` | `when wpl.name == "预置-网络探针检测到内部主机对外慢速传输大量数据" && wpl.ruleCategoryName == "流量异常" && exactly_one(parse_ip_list(wpl.srcIp)) != '' && exactly_one(parse_ip_list(wpl.dstIp)) != '' then chars(finding) else no_match` -> "finding" | `no_match` | confirmed；NGSOC 来源聚合告警 |
| `event_domain` | `conditional` | `when wpl.name == "预置-网络探针检测到内部主机对外慢速传输大量数据" && wpl.ruleCategoryName == "流量异常" && exactly_one(parse_ip_list(wpl.srcIp)) != '' && exactly_one(parse_ip_list(wpl.dstIp)) != ''` | `when wpl.name == "预置-网络探针检测到内部主机对外慢速传输大量数据" && wpl.ruleCategoryName == "流量异常" && exactly_one(parse_ip_list(wpl.srcIp)) != '' && exactly_one(parse_ip_list(wpl.dstIp)) != '' then chars(network) else no_match` -> "network" | `no_match` | confirmed；来源为 TCP 流量聚合告警 |
| `event_type` | `conditional` | `when wpl.name == "预置-网络探针检测到内部主机对外慢速传输大量数据" && wpl.ruleCategoryName == "流量异常" && exactly_one(parse_ip_list(wpl.srcIp)) != '' && exactly_one(parse_ip_list(wpl.dstIp)) != ''` | `when wpl.name == "预置-网络探针检测到内部主机对外慢速传输大量数据" && wpl.ruleCategoryName == "流量异常" && exactly_one(parse_ip_list(wpl.srcIp)) != '' && exactly_one(parse_ip_list(wpl.dstIp)) != '' then chars(network_connection) else no_match` -> "network_connection" | `no_match` | confirmed；明确提供通信源、目标和端口 |
| `operation` | `conditional` | `when wpl.name == "预置-网络探针检测到内部主机对外慢速传输大量数据" && wpl.ruleCategoryName == "流量异常" && exactly_one(parse_ip_list(wpl.srcIp)) != '' && exactly_one(parse_ip_list(wpl.dstIp)) != ''` | `when wpl.name == "预置-网络探针检测到内部主机对外慢速传输大量数据" && wpl.ruleCategoryName == "流量异常" && exactly_one(parse_ip_list(wpl.srcIp)) != '' && exactly_one(parse_ip_list(wpl.dstIp)) != '' then chars(traffic) else no_match` -> "traffic" | `no_match` | confirmed；只确认发生流量传输，不推断连接建立或关闭 |
| `roles.source.ref_id` | `derived` | `derived.entity_ref(endpoint, exactly_one(parse_ip_list(wpl.srcIp)))` | `entity_ref(endpoint, exactly_one(parse_ip_list(wpl.srcIp)))` -> "endpoint::198.51.100.180" | `drop_and_review` | confirmed；源端点稳定引用 |
| `roles.target.ref_id` | `derived` | `derived.entity_ref(endpoint, exactly_one(parse_ip_list(wpl.dstIp)))` | `entity_ref(endpoint, exactly_one(parse_ip_list(wpl.dstIp)))` -> "endpoint::192.0.2.133" | `drop_and_review` | confirmed；目标端点稳定引用；端口不是实体身份 |
| `roles.observer.device.name` | `derived` | `raw_syslog.header.host` | `read(raw_syslog.header.host)` -> "host-2cfba8ce.sdm.example.internal" | `—` | confirmed；Syslog 上报主机 |
| `extensions.source_private.syslog_priority/syslog_host/syslog_header_time` | `derived` | `raw_syslog.header` | `parse_syslog_header(raw_input.original_payload)` -> {"priority": 14, "host": "host-2cfba8ce.sdm.example.internal", "time": "Dec 18 16:01:32"} | `—` | confirmed；保留 Syslog 头审计值 |
| `roles.source.entity_type` | `constant` | `constant.roles_source_entity_type` | "endpoint" | `—` | confirmed；源 IP 装配为 endpoint |
| `roles.target.entity_type` | `constant` | `constant.roles_target_entity_type` | "endpoint" | `—` | confirmed；目标 IP/端口装配为 endpoint |
| `roles.carriers` | `constant` | `constant.roles_carriers` | [] | `—` | confirmed；无进程、会话或独立载体实体 |
| `roles.related` | `constant` | `constant.roles_related` | [] | `—` | confirmed；无其他关联实体 |
| `roles.observer.product.name` | `constant` | `constant.roles_observer_product_name` | "NGSOC" | `—` | confirmed；来源产品显示名 |
| `roles.observer.device.vendor` | `constant` | `constant.roles_observer_device_vendor` | "qax" | `—` | confirmed；来源设备厂商 |
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
| `occur_time` | `transform` | `timestamp` | `parse_time_ms(wpl.timestamp,'Asia/Shanghai')` -> 1734481415000 | `drop_and_review` | confirmed；WPL 输出仍为 chars；SDM 装配转换为毫秒 |
| `source_original_event_id` | `projection` | `seq` | "12933976" | `—` | confirmed；来源告警序列热字段 |
| `source_finding.original_id` | `projection` | `seq` | "12933976" | `—` | confirmed；来源 finding 原始 ID |
| `roles.source.endpoint.ip` | `transform` | `srcIp` | `exactly_one(parse_ip_list(wpl.srcIp))` -> "198.51.100.180" | `drop_and_review` | confirmed；单一通信源 IP |
| `source_ip` | `projection` | `roles.source.endpoint.ip` | "198.51.100.180" | `—` | confirmed；从源端点投影热字段 |
| `roles.target.endpoint.ip` | `transform` | `dstIp` | `exactly_one(parse_ip_list(wpl.dstIp))` -> "192.0.2.133" | `drop_and_review` | confirmed；单一通信目标 IP |
| `target_ip` | `projection` | `roles.target.endpoint.ip` | "192.0.2.133" | `—` | confirmed；从目标端点投影热字段 |
| `roles.target.endpoint.port` | `transform` | `dport` | `exactly_one(parse_int_list(wpl.dport))` -> 8200 | `omit_and_review` | confirmed；唯一目标端口 |
| `target_port` | `projection` | `roles.target.endpoint.port` | 8200 | `—` | confirmed；从目标端点投影热字段 |
| `roles.source.geo` | `transform` | `sipGeo/srcIp` | `normalize_geo(geo_by_ip(parse_json(wpl.sipGeo), exactly_one(parse_ip_list(wpl.srcIp))))` -> {"continent": {"name": "北美洲"}, "country": {"name": "美国"}, "region": {"name": "俄亥俄州"}, "city": {"name": "哥伦布"}, "coordinates": {"latitude": 39.96120071411133, "longitude": -82.9988021850586}} | `omit_and_review` | confirmed；来源设备提供的源 Geo，不属于平台富化 |
| `roles.target.geo` | `transform` | `dipGeo/dstIp` | `normalize_geo(geo_by_ip(parse_json(wpl.dipGeo), exactly_one(parse_ip_list(wpl.dstIp))))` -> {"continent": {"name": "亚洲"}, "country": {"name": "中国"}, "region": {"name": "内蒙古自治区"}, "city": {"name": "呼和浩特市"}, "coordinates": {"latitude": 40.78160095214844, "longitude": 111.86299896240234}} | `omit_and_review` | confirmed；来源设备提供的目标 Geo |
| `roles.observer.device.ip` | `transform` | `devIp` | `exactly_one(parse_ip_list(wpl.devIp))` -> "192.0.2.37" | `omit_and_review` | confirmed；唯一观察设备 IP |
| `facets.network.application_protocol` | `transform` | `protocol` | `lower(exactly_one(parse_text_list(wpl.protocol)))` -> "http" | `preserve_raw_and_review` | confirmed；http 是应用层协议，不当作 TCP/UDP |
| `facets.network.direction` | `dictionary` | `commDirection` | "内到外" -> "L2W" | `preserve_in_extension_and_review` | partial；内到外归一 |
| `source_finding.title` | `projection` | `name` | "预置-网络探针检测到内部主机对外慢速传输大量数据" | `—` | confirmed；来源告警标题 |
| `source_finding.severity` | `projection` | `severity` | "中危" | `—` | confirmed；来源严重度 |
| `source_finding.status` | `projection` | `disposeState` | "待处置" | `—` | confirmed；来源处置状态；未做字典归一 |
| `source_finding.count` | `transform` | `times` | `to_int(wpl.times)` -> 16 | `omit_and_review` | confirmed；来源聚合命中次数；不是传输字节数 |
| `source_finding.confidence` | `projection` | `confidence` | "中" | `—` | confirmed；来源置信度 |
| `source_finding.category.original.name` | `projection` | `ruleCategoryName` | "流量异常" | `—` | confirmed；来源分类 |
| `source_finding.behavior` | `conditional` | `name/ruleCategoryName` | `when wpl.name == "预置-网络探针检测到内部主机对外慢速传输大量数据" && wpl.ruleCategoryName == "流量异常" then chars(outbound_large_data_transfer) else omit` -> "outbound_large_data_transfer" | `omit` | confirmed；厂商规则声明对外大量数据传输；无数值测量 |
| `source_finding.attention.content` | `projection` | `attentionValue` | "源IP : 198.51.100.180  , 目的IP : 192.0.2.133" | `—` | confirmed；完整保留来源关注内容 |
| `extensions.source_private.transfer_profile` | `conditional` | `name` | `when wpl.name == '预置-网络探针检测到内部主机对外慢速传输大量数据' then object(direction=outbound,speed=slow,volume=large) else omit` -> {"direction": "outbound", "speed": "slow", "volume": "large"} | `omit` | confirmed；标题定性标签；不是字节数或速率测量 |
| `extensions.source_private.source_ports` | `transform` | `sport` | `parse_int_list(wpl.sport)` -> [57194, 57186, 57106, 57060, 57044, 57012, 56924, 56994, 56910, 56928] | `preserve_raw_and_review` | confirmed；多个来源端口不任取一个投影 |
| `extensions.source_private.protocol_original` | `transform` | `protocol` | `parse_text_list(wpl.protocol)` -> ["http"] | `preserve_raw_and_review` | confirmed；保留来源应用协议列表原值 |
| `extensions.unmapped.comm_direction_original` | `transform` | `commDirection` | `exactly_one(parse_text_list(wpl.commDirection))` -> "内到外" | `omit_and_review` | confirmed；方向字典局部覆盖，保留厂商原文 |
| `extensions.source_private.wpl_update_time` | `projection` | `update_time` | "2026-12-18 16:01:32" | `—` | confirmed；WPL 从无年份 Syslog 头推断，仅供审计 |
| `extensions.source_private.latest_timestamp` | `projection` | `latestTimestamp` | 1734508602000 | `—` | confirmed；WPL 已转换为毫秒 |
| `extensions.source_private.finding_source` | `projection` | `source` | "关联规则" | `—` | confirmed；来源 finding 生成方式 |
| `extensions.source_private.relevant_rule_name` | `projection` | `relevantRuleName` | "预置-网络探针检测到内部主机对外慢速传输大量数据" | `—` | confirmed；关联规则名称；不冒充空 ruleName/ruleId |
| `extensions.source_private.relevant_log_types` | `transform` | `relevantLogsType` | `parse_text_list(wpl.relevantLogsType)` -> ["天堤TCP流量日志"] | `preserve_raw_and_review` | confirmed；来源关联日志类型 |
| `extensions.source_private.relevant_network_segments` | `transform` | `relevantNetworkSegmentId` | `parse_text_list(wpl.relevantNetworkSegmentId)` -> ["云业务区", "运维管理区"] | `preserve_raw_and_review` | confirmed；来源关联网络分区 |
| `source_alert_severity` | `transform` | `severity` | `string` -> "中危" | `—` | confirmed；保留来源 finding 原始严重度 |
| `severity` | `dictionary` | `severity` | "中危" -> "warning" | `null_and_review` | partial；根据当前 NGSOC 样例分布推测的安全严重度交叉表，尚未经厂商确认 |
| `outcome` | `conditional` | `name` | `chars(observed)` -> "observed" | `unknown` | partial；标题明确声明已检测到慢速传输大量数据行为 |

### 5.3 编写约束

- source/target 表示通信方向；attackerContent 和 victimContent 为空，不构造攻击方或受害方声明。
- 慢速和大量只作为厂商规则定性标签，不生成不存在的 bytes、duration 或 rate 数值。
- protocol=http 是应用层协议，写入 facets.network.application_protocol；不能据此写入 network_protocol。
- 多个 sport 只保存在扩展数组，不任取一个投影为 source_port。
- sipGeo/dipGeo 来自原始 NGSOC 字段，不属于平台 GeoIP 富化。
