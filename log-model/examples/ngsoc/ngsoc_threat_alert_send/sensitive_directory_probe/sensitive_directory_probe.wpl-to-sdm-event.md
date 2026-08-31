# WPL -> SDM Event 字段映射

详见同名 JSON 映射文件；Meta 与 Content 规则由后续 writer-facing 增强步骤生成。

## 五、WPL/OML 编写规则

> WPL 只负责提取表中的 source 字段；Meta 和 Content 的赋值由 OML 按下表实现。
> `partial` 表示当前只有样例值或局部说明，不能视为完整厂商字典。

### 5.1 Meta 区

| SDM 字段 | 规则类型 | 输入/来源 | 赋值 | 未命中 | 状态与证据 |
|---|---|---|---|---|---|
| `event_id` | `derived` | `derived.sha256(tenant_id+'|'+mapping_id+'|'+wpl.uuid)` | `'evt-' + sha256(tenant_id+'|'+mapping_id+'|'+wpl.uuid)` -> "evt-862d733b04071e1ad020396038d8410de44e4ab7762075e6d36da702ba9a80e2" | `—` | confirmed；来源 UUID 的确定性事件 ID |
| `record_kind` | `conditional` | `when wpl.name == "发现敏感目录/文件探测行为" && wpl.ruleCategoryName == "信息泄露"` | `when wpl.name == "发现敏感目录/文件探测行为" && wpl.ruleCategoryName == "信息泄露" then chars(finding) else no_match` -> "finding" | `no_match` | confirmed；NGSOC 来源告警 |
| `event_domain` | `conditional` | `when wpl.name == "发现敏感目录/文件探测行为" && wpl.ruleCategoryName == "信息泄露"` | `when wpl.name == "发现敏感目录/文件探测行为" && wpl.ruleCategoryName == "信息泄露" then chars(threat) else no_match` -> "threat" | `no_match` | confirmed；来源声明信息泄露风险 |
| `event_type` | `conditional` | `when wpl.name == "发现敏感目录/文件探测行为" && wpl.ruleCategoryName == "信息泄露"` | `when wpl.name == "发现敏感目录/文件探测行为" && wpl.ruleCategoryName == "信息泄露" then chars(network_http) else no_match` -> "network_http" | `no_match` | confirmed；存在结构化 HTTP 请求和响应证据 |
| `operation` | `constant` | `constant.empty_operation_for_network_http` | "" | `—` | confirmed；network_http 不配置 subordinate operation |
| `roles.source.ref_id/roles.target.ref_id` | `derived` | `derived.entity_ref(endpoint,wpl.srcIp,extraFields.sport[0])/derived.entity_ref(endpoint,wpl.dstIp,extraFields.dport[0])` | `stable_endpoint_refs(ip,port)` -> ["endpoint-0cde8cf840a4bbdd9e2eeab1c88eae98", "endpoint-9bc984e80bb20d13e7c8ed1ac918b4ad"] | `—` | confirmed；通信两端稳定引用 |
| `roles.source.entity_type/roles.target.entity_type` | `constant` | `constant.endpoint_entity_type` | "endpoint" | `—` | confirmed；IP 与端口装配为 endpoint |
| `roles.carriers/roles.related` | `constant` | `constant.empty_role_arrays` | [] | `—` | confirmed；没有进程、会话或独立关联实体 |
| `roles.observer.product.name` | `constant` | `constant.observer_product_display_name` | "NGSOC" | `—` | confirmed；来源产品 |
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
| `log_id` | `projection` | `log_id` | "4b8d855452b64a15b5c88084690d57f8" | `—` | confirmed；WPL 已解析来源日志标识；不是平台补充字段 |
| `source_original_event_id/source_finding.original_id` | `projection` | `uuid` | "c4d198b9-262b-49f0-81d3-3ecb694ecada" | `—` | confirmed；来源告警 UUID |
| `occur_time` | `projection` | `occur_time` | 1733307762257 | `—` | confirmed；WPL 已解析为毫秒时间戳 |
| `roles.source.endpoint.ip/source_ip` | `projection` | `srcIp` | "192.0.2.201" | `—` | confirmed；通信起点 |
| `roles.target.endpoint.ip/target_ip` | `projection` | `dstIp` | "198.51.100.157" | `—` | confirmed；通信终点 |
| `roles.source.endpoint.port/source_port` | `transform` | `extraFields.sport[0]` | `digit(exactly_one(wpl.extraFields.sport))` -> 34738 | `omit_port_and_review` | confirmed；唯一源端口字符串转整数 |
| `roles.target.endpoint.port` | `transform` | `extraFields.dport[0]` | `digit(exactly_one(wpl.extraFields.dport))` -> 80 | `omit_port_and_review` | confirmed；唯一目标端口字符串转整数 |
| `target_port` | `projection` | `roles.target.endpoint.port` | 80 | `—` | confirmed；目标端口热字段投影自 target endpoint |
| `source_finding.victim.endpoint.port` | `projection` | `extraFields.dport[0]` | 80 | `omit_port_and_review` | confirmed；来源受害端口与目标端口相同 |
| `facets.http.request.method` | `transform` | `extraFields.httpMethod[0]` | `uppercase(exactly_one(wpl.extraFields.httpMethod))` -> "GET" | `omit_and_review` | confirmed；结构化 HTTP 方法 |
| `facets.http.request.path` | `transform` | `extraFields.uriPath[0]` | `exactly_one(wpl.extraFields.uriPath)` -> "/old/swagger.json" | `omit_and_review` | confirmed；结构化请求路径 |
| `facets.http.request.user_agent` | `transform` | `extraFields.httpUserAgent[0]` | `exactly_one(wpl.extraFields.httpUserAgent)` -> "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.5481.38 Safari/537.36" | `omit_and_review` | confirmed；HTTP User-Agent |
| `facets.http.response.status_code` | `transform` | `extraFields.httpRspCode[0]` | `digit(exactly_one(wpl.extraFields.httpRspCode))` -> 503 | `omit_and_review` | confirmed；HTTP 响应码；503 不证明信息泄露 |
| `facets.network.direction` | `dictionary` | `commDirection[0]` | "内到外" -> "L2W" | `extensions.unmapped.comm_direction=original_value_and_review` | confirmed；NGSOC-4.13.1 厂商字典映射 |
| `source_finding.title` | `projection` | `name` | "发现敏感目录/文件探测行为" | `—` | confirmed；来源告警标题 |
| `source_finding.severity/source_finding.confidence` | `transform` | `severity/confidence` | `string(wpl.severity)/read(wpl.confidence)` -> ["1", "2"] | `—` | confirmed；保留来源数值枚举，不冒充顶层严重度 |
| `extensions.unmapped.killchain` | `dictionary_candidate` | `killchain` | "1" | `preserve_original_value_and_review` | confirmed；厂商数值字典未确认；候选含义仅供复核，不写标准字段 |
| `source_finding.attacker.endpoint.ip` | `projection` | `attackerContent` | "192.0.2.201" | `—` | confirmed；来源攻击方声明 |
| `source_finding.victim.endpoint.ip` | `projection` | `victimContent` | "198.51.100.157" | `—` | confirmed；来源受害方声明 |
| `source_finding.victim.geo` | `transform` | `dipGeo[dstIp]` | `geoip_object(exactly_one(wpl.dipGeo[dstIp]))` -> {"continent": {"name": "亚洲"}, "country": {"name": "新加坡"}, "region": {"name": "新加坡"}, "city": {"name": "新加坡"}, "coordinates": {"latitude": 1.2865300178527832, "longitude": 103.85399627685547}} | `omit_geo_and_review` | confirmed；目标 GeoIP 字段显式映射；经纬度字符串转数值，province_name 归一为 region.name |
| `source_finding.attention.content` | `transform` | `attentionValue` | `format_attention(exactly_one(wpl.attentionValue.目的IP))` -> "目的IP : 198.51.100.157" | `omit_and_review` | confirmed；WPL 保留 attentionValue 对象；仅将目的 IP 关注内容格式化为来源注意文本 |
| `roles.observer.device.ip` | `projection` | `access_ip` | "192.0.2.30" | `—` | confirmed；WPL 从 devIp[0] 提取的观测设备 IP |
| `roles.observer.device.name` | `projection` | `extraFields.devName[0]` | "天眼流量传感器" | `omit_and_review` | confirmed；观测设备显示名 |
| `roles.observer.device.vendor` | `dictionary` | `extraFields.devVendor[0]` | "奇安信" -> "qax" | `omit_vendor_and_review` | confirmed；设备厂商中文名按已确认接入厂商标识归一 |
| `source_finding.category.original.code/name` | `projection` | `ruleCategoryId/ruleCategoryName` | ["376b269e-ac3a-4759-9752-f2b30cb54d58", "信息泄露"] | `—` | confirmed；来源分类 |
| `source_finding.rule.id/label` | `projection` | `relevantRuleId/relevantRuleName` | ["0a94d36a-5c7e-439e-8fce-08e8c213d8ea", "预置-网络探针检测到信息泄露事件"] | `—` | confirmed；来源关联规则 |
| `source_finding.count` | `projection` | `relevantLogsNum` | 1 | `—` | confirmed；关联日志数量 |
| `extensions.source_private.relevant_log_count` | `projection` | `relevantLogsNum` | 1 | `—` | confirmed；关联日志数量原值保留 |
| `extensions.source_private.relevant_log_types` | `projection` | `relevantLogsType` | ["flow_td_webattack"] | `—` | confirmed；关联日志类型 |
| `extensions.source_private.log_start_time` | `projection` | `logStartTime` | 1733307681000 | `—` | confirmed；NGSOC 聚合窗口起点 |
| `extensions.source_private.log_end_time` | `projection` | `logEndTime` | 1733307681000 | `—` | confirmed；NGSOC 聚合窗口终点 |
| `extensions.source_private.merge_key` | `projection` | `mergeKey` | "42cbec74461f68614726e472bf586c8f" | `—` | confirmed；NGSOC 聚合键 |
| `extensions.source_private.source` | `projection` | `source` | 0 | `—` | confirmed；NGSOC 来源代码 |
| `extensions.source_private.payload_log_type` | `projection` | `type` | "ngsoc_alert_info" | `—` | confirmed；上游载荷分类，不覆盖顶层路由日志类型 |
| `source_alert_severity` | `transform` | `severity` | `string` -> "1" | `—` | confirmed；保留来源 finding 原始严重度 |
| `severity` | `dictionary` | `severity` | 1 -> "notice" | `null_and_review` | confirmed；根据当前 NGSOC 样例分布推测的安全严重度交叉表，由 NGSOC-4.13.1 厂商文档确认 |
| `source_finding.attack_result` | `dictionary` | `attackResult` | "2" -> "attempted" | `preserve_in_extension_and_review` | confirmed；按当前设备类型候选字典推测攻击结果 |
| `outcome` | `dictionary` | `attackResult` | "2" -> "observed" | `unknown_and_review` | confirmed；按当前设备类型候选字典推测攻击结果 |
| `source_finding.compromise_status` | `dictionary` | `compromiseState` | "false" -> "not_compromised" | `preserve_in_extension_and_review` | confirmed；布尔值及中文值按当前样例语义推测，由 NGSOC-4.13.1 厂商文档确认 |

### 5.3 编写约束

- attackResult=2 与 killchain=1 的厂商数值字典未确认，原值只进入 extensions.unmapped；候选标准含义不落库。
- 顶层 outcome 固定为 unknown，不读取 attackResult。
- HTTP 503 响应不证明敏感目录或文件已经泄露。
