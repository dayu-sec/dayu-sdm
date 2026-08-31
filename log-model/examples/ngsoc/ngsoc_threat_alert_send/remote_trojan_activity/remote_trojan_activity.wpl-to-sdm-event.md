# WPL -> SDM Event 字段映射

> 样例：`remote_trojan_activity.expected-sdm-event.json`；WPL 输出 73 个顶层字段，机器可读文件逐字段记录映射或不落库结论。

## 核心字段

| WPL 来源 | SDM 落位 | 转换 | 说明 |
|---|---|---|---|
| `uuid` | `source_original_event_id`、`source_finding.original_id` | 直接赋值 | 来源告警 UUID |
| `log_id` | `log_id` | 直接赋值 | NGSOC 日志 ID |
| `occur_time` | `occur_time` | 毫秒时间戳直接使用 | 不使用生成时间 timestamp 替代发生时间 |
| `name` | `source_finding.title` | 直接赋值 | 来源检测标题 |
| `severity` | `source_finding.severity` | 保留 `3` | 不写入 syslog 枚举 `event.severity` |
| `confidence` | `source_finding.confidence` | 保留 `3` | NGSOC-4.13.1 厂商字典已确认 |
| `compromiseState` | `source_finding.compromise_status` | `true -> compromised` | NGSOC 失陷结论 |
| `attackResult` | `extensions.unmapped.attack_result` | 原值 `1` | 厂商数值字典未确认 |
| `killchain` | `source_finding.killchain` | `6 -> command_and_control` | 杀伤链归一 |
| `srcIp`、`extraFields.sport[0]`、`extraFields.smac[0]` | `roles.source.endpoint` | 组合 IP、端口与 MAC | 通信起点 |
| `dstIp`、`extraFields.dport[0]`、`extraFields.dmac[0]` | `roles.target.endpoint` | 组合 IP、端口与 MAC | 通信终点 |
| `attackerIp` | `source_finding.attacker.endpoint.ip` | 直接赋值 | NGSOC 检测主张攻击方 |
| `victimIp` | `source_finding.victim.endpoint.ip` | 直接赋值 | NGSOC 检测主张受害方 |
| `commDirection[0]` | `facets.network.direction` | `内到外 -> L2W` | 通信方向 |
| `ruleCategoryId/ruleCategoryName` | `source_finding.category.original` | 组合 code/name | 来源分类 |
| `relevantRuleId/relevantRuleName` | `source_finding.rule` | 组合 id/label | 关联规则 |
| `iocType/ioc` | `source_finding.ioc` | 组合 type/value | 命中 IOC |
| `sipGeo` | `source_finding.victim.geo` | 按 IP `192.0.2.254` 关联 | 不能机械认定为攻击方 |
| `dipGeo` | `source_finding.attacker.geo` | 按 IP `203.0.113.121` 关联 | 不能机械认定为受害方 |
| `solution` | `source_finding.remediation` | 直接赋值 | 来源处置建议 |
| `relevantLogsNum` | `source_finding.count`、`extensions.source_private.relevant_log_count` | 整数直接赋值 | 来源告警聚合数量 |
| `isFromExternal`、`attackerIp`、`victimIp`、`commDirection[0]` | `source_finding.attack_direction` | `true + 外部攻击方 + 内部受害方 + 内到外通信 -> W2L` | 攻击方向是检测语义，不等于连接方向 |

## 平台与派生字段

| 来源 | SDM 落位 | 说明 |
|---|---|---|
| `derived.sha256(tenant_id + mapping_id + uuid)` | `event_id` | 确定性事件 ID |
| `constant` | `record_kind/event_domain` | NGSOC 来源告警固定为 `finding/threat` |
| `name`、`alarmDesc`、`srcIp/dstIp`、`extraFields.sport/dport` | `event_type/operation` | 满足远控木马分类、通信描述和完整端点条件时归一为 `network_connection/traffic` |
| `constant.observer_product + name` | `source_finding.description` | 生成简短检测描述 `奇安信天眼流量传感器上报普通远控木马活动事件` |
| `platform_context.*` | 接入元数据 | 租户为空，使用 POC 采集实例 |

路由日志族由接入规则 `ngsoc_threat_alert_send*` 决定；载荷中的 `log_type=ngsoc_alert_info` 是上游载荷分类，单独保存在 `extensions.source_private.payload_log_type`，不能覆盖顶层路由 `log_type`。

## 不落库原则

- 空数组、空字符串和仅用于 NGSOC 内部展示的字段不单独落库。
- 完整原始 JSON 保存在独立 `raw_log` 原文表（`event_id` 回查）。
- `payload.packetData` 不复制进扩展，避免重复保存大体积证据。
- `relevantAssetsName` 没有稳定资产 ID 时不构造 host 或 resource。

## 五、WPL/OML 编写规则

> WPL 只负责提取表中的 source 字段；Meta 和 Content 的赋值由 OML 按下表实现。
> `partial` 表示当前只有样例值或局部说明，不能视为完整厂商字典。

### 5.1 Meta 区

| SDM 字段 | 规则类型 | 输入/来源 | 赋值 | 未命中 | 状态与证据 |
|---|---|---|---|---|---|
| `event_id` | `derived` | `derived.sha256(tenant_id=""|mapping_id|source_original_event_id)` | `derived.sha256(tenant_id=""|mapping_id|source_original_event_id)` | `—` | confirmed；确定性事件 ID |
| `record_kind` | `constant` | `constant` | "finding" | `—` | confirmed；NGSOC 来源告警 |
| `event_domain` | `constant` | `constant` | "threat" | `—` | confirmed；NGSOC 来源告警 |
| `event_type` | `conditional` | `when wpl.ruleCategoryName == "远控木马" && contains(wpl.alarmDesc, "网络通信") && wpl.srcIp/wpl.dstIp nonempty && exactly_one(wpl.extraFields.sport/dport) valid` | `when wpl.ruleCategoryName == "远控木马" && contains(wpl.alarmDesc, "网络通信") && wpl.srcIp/wpl.dstIp nonempty && exactly_one(wpl.extraFields.sport/dport) valid then chars(network_connection) else no_match` -> "network_connection" | `no_match` | confirmed；仅远控木马通信分支命中 |
| `operation` | `conditional` | `when event_type == "network_connection"` | `when event_type == "network_connection" then chars(traffic) else no_match` -> "traffic" | `no_match` | confirmed；与 event_type 绑定 |
| `roles.source.ref_id` | `derived` | `derived.entity_ref(endpoint,wpl.srcIp,to_int(exactly_one(wpl.extraFields.sport)))` | `derived.entity_ref(endpoint,wpl.srcIp,to_int(exactly_one(wpl.extraFields.sport)))` -> "endpoint::192.0.2.254:8857" | `drop_and_review` | confirmed；通信起点引用 |
| `roles.target.ref_id` | `derived` | `derived.entity_ref(endpoint,wpl.dstIp,to_int(exactly_one(wpl.extraFields.dport)))` | `derived.entity_ref(endpoint,wpl.dstIp,to_int(exactly_one(wpl.extraFields.dport)))` -> "endpoint::203.0.113.121:443" | `drop_and_review` | confirmed；通信终点引用 |
| `source_finding.description` | `derived` | `derived.finding_description(constant.observer_product,wpl.name)` | `derived.finding_description(constant.observer_product,wpl.name)` -> "奇安信天眼流量传感器上报普通远控木马活动事件" | `—` | confirmed；使用来源产品身份和告警名称生成简短描述 |
| `parse_time` | `context` | `platform_context.parse_time` | `read(parse_time)` | `—` | confirmed；expected 事件中的平台上下文字段 |
| `data_src_instance_id` | `context` | `platform_context.data_src_instance_id` | `read(data_src_instance_id)` | `—` | confirmed；expected 事件中的平台上下文字段 |
| `tenant_id` | `context` | `platform_context.tenant_id` | `read(tenant_id)` | `—` | confirmed；expected 事件中的平台上下文字段 |
| `log_id` | `context` | `platform_context.log_id` | `read(log_id)` | `—` | confirmed；expected 事件中的平台上下文字段 |
| `ingest_time` | `context` | `platform_context.ingest_time` | `read(ingest_time)` | `—` | confirmed；expected 事件中的平台上下文字段 |
| `data_src_product` | `constant` | `constant.data_src_product` | "ngsoc" | `—` | confirmed；expected 事件确认的日志类型级常量 |
| `log_type` | `constant` | `constant.log_type` | "ngsoc_threat_alert_send" | `—` | confirmed；expected 事件确认的日志类型级常量 |
| `data_src_vendor` | `constant` | `constant.data_src_vendor` | "qax" | `—` | confirmed；expected 事件确认的日志类型级常量 |
| `mapping_id` | `constant` | `constant.mapping_id` | "qax.ngsoc.ngsoc_threat_alert_send" | `—` | confirmed；expected 事件确认的日志类型级常量 |
| `schema_version` | `constant` | `constant.schema_version` | 2 | `—` | confirmed；expected 事件确认的日志类型级常量 |
| `observer_product` | `constant` | `constant.observer_product` | "ngsoc" | `—` | confirmed；expected 事件确认的日志类型级常量 |
| `observer_vendor` | `constant` | `constant.observer_vendor` | "qax" | `—` | confirmed；expected 事件确认的日志类型级常量 |
| `log_name` | `constant` | `constant.log_name` | "NGSOC威胁告警" | `—` | confirmed；expected 事件确认的日志类型级常量 |
| `data_src_category` | `constant` | `constant.data_src_category` | "security_analytics" | `—` | confirmed；expected 事件确认的日志类型级常量 |
| `log_level` | `gap` | `data_gap.no_source_log_level` | `null` | `—` | missing；来源没有独立日志等级字段 |

### 5.2 Content 区

| SDM 字段 | 规则类型 | WPL 字段 | 映射/赋值 | 未命中 | 状态与证据 |
|---|---|---|---|---|---|
| `extensions.source_private.relevant_log_types` | `projection` | `relevantLogsType` | ["flow_td_ioc"] | `—` | confirmed；关联日志类型 |
| `extensions.source_private.source` | `projection` | `source` | 0 | `—` | confirmed；NGSOC 来源代码 |
| `extensions.source_private.payload_log_type` | `projection` | `log_type` | "ngsoc_alert_info" | `—` | confirmed；保留载荷分类；顶层 log_type 由接入路由 ngsoc_threat_alert_send* 决定 |
| `source_original_event_id` | `projection` | `uuid` | "90ccc8c1-767a-4268-a49a-ca6adf39e70c" | `—` | confirmed；来源告警 UUID |
| `source_finding.remediation` | `projection` | `solution` | "对域名类IOC，需要在域名解析日志中查看解析到的A记录，若无A记录则说明外联不成功；若有A记录则需要根据A记录IP在TCP流量日志中查询有通信记录的源IP，并对这些源IP进行深入的调查分析，以确认是否为已失陷主机。对IP类IOC，需要在TCP流量日志中查询有通信记录的源IP，并对这些源IP进行深入的调查分析，以确认是否为已失陷主机。\n来自奇安信天眼流量传感器的告警描述为: 该家族是一个通用名，当引擎检出结果为恶意但是无法识别出具体的家族分类时(通常是由于病毒使用了一些加壳/混淆/免杀等去掉强特征的手段导致的)会使用这个名字。，处置建议为: 。" | `—` | confirmed；处置建议 |
| `extensions.source_private.merge_key` | `projection` | `mergeKey` | "e9762f36d08a471155d7bcfbf39e1cd2" | `—` | confirmed；NGSOC 聚合键 |
| `source_finding.count + extensions.source_private.relevant_log_count` | `projection` | `relevantLogsNum` | 1 | `—` | confirmed；关联日志数量同时作为来源告警计数 |
| `roles.source.endpoint.ip + source_ip` | `projection` | `srcIp` | "192.0.2.254" | `—` | confirmed；通信起点，不等同攻击方 |
| `source_finding.ioc.type` | `projection` | `iocType` | "dip:dport" | `—` | confirmed；IOC 类型 |
| `source_finding.victim.geo` | `projection` | `sipGeo` | {"192.0.2.254": {"continent_name": "保留IP", "city_name": "", "latitude": "0.0", "country_name": "", "county_name": "", "province_name": "", "longitude": "0.0"}} | `—` | confirmed；本样例 sip 是检测主张中的 victim |
| `source_finding.title` | `projection` | `name` | "普通远控木马活动事件" | `—` | confirmed；来源告警标题 |
| `source_finding.rule.id` | `projection` | `relevantRuleId` | "dcbd0462-4b2b-4003-b952-fdd34aeaab3f" | `—` | confirmed；关联规则 ID |
| `source_finding.category.original.code` | `projection` | `ruleCategoryId` | "cccfe07f-802d-4510-9b53-388faf6533d9" | `—` | confirmed；来源分类 ID |
| `extensions.source_private.log_start_time` | `projection` | `logStartTime` | 1733307673000 | `—` | confirmed；来源告警关联日志开始时间 |
| `extensions.source_private.log_end_time` | `projection` | `logEndTime` | 1733307673000 | `—` | confirmed；来源告警关联日志结束时间 |
| `occur_time` | `projection` | `occur_time` | 1733307762258 | `—` | confirmed；毫秒时间戳直接使用 |
| `source_finding.rule.label` | `projection` | `relevantRuleName` | "预置-远控木马IOC命中事件" | `—` | confirmed；关联规则名称 |
| `source_finding.severity` | `projection` | `severity` | 3 | `—` | confirmed；保留 NGSOC 原始等级 3 |
| `log_id` | `projection` | `log_id` | "207b443655fb4df2bf281fb121da4dae" | `—` | confirmed；来源日志 ID |
| `source_finding.attacker.endpoint.ip` | `projection` | `attackerIp` | "203.0.113.121" | `—` | confirmed；NGSOC 检测主张中的攻击方 |
| `source_finding.attacker.geo` | `projection` | `dipGeo` | {"203.0.113.121": {"continent_name": "亚洲", "city_name": "北京市", "latitude": "39.902801513671875", "country_name": "中国", "county_name": "", "province_name": "北京市", "longitude": "116.4010009765625"}} | `—` | confirmed；本样例 dip 是检测主张中的 attacker |
| `source_finding.confidence` | `projection` | `confidence` | 3 | `—` | confirmed；保留 NGSOC 原始置信度 3 |
| `source_finding.category.original.name` | `projection` | `ruleCategoryName` | "远控木马" | `—` | confirmed；来源分类名称 |
| `source_finding.victim.endpoint.ip` | `projection` | `victimIp` | "192.0.2.254" | `—` | confirmed；NGSOC 检测主张中的受害方 |
| `roles.target.endpoint.ip + target_ip` | `projection` | `dstIp` | "203.0.113.121" | `—` | confirmed；通信终点，不等同受害方 |
| `source_finding.ioc.value` | `projection` | `ioc` | "203.0.113.121:443" | `—` | confirmed；IOC 值 |
| `roles.source.endpoint.port/source_port` | `transform` | `extraFields.sport` | `to_int(exactly_one(wpl.extraFields.sport))` -> 8857 | `drop_and_review` | confirmed；必须恰好一个合法端口 |
| `roles.source.endpoint.mac` | `transform` | `extraFields.smac` | `normalize_mac(exactly_one(wpl.extraFields.smac))` -> "00:50:56:81:e3:8c" | `drop_and_review` | confirmed；必须恰好一个合法 MAC |
| `roles.target.endpoint.port/target_port` | `transform` | `extraFields.dport` | `to_int(exactly_one(wpl.extraFields.dport))` -> 443 | `drop_and_review` | confirmed；必须恰好一个合法端口 |
| `roles.target.endpoint.mac` | `transform` | `extraFields.dmac` | `normalize_mac(exactly_one(wpl.extraFields.dmac))` -> "cc:d8:1f:44:38:48" | `drop_and_review` | confirmed；必须恰好一个合法 MAC |
| `source_finding.malware.name` | `transform` | `extraFields.maliciousFamily` | `exactly_one(wpl.extraFields.maliciousFamily)` -> "Generic Trojan" | `drop_and_review` | confirmed；来源恶意家族名称 |
| `source_finding.killchain` | `dictionary` | `killchain` | 6 -> "command_and_control" | `preserve_in_extension_and_review` | confirmed；6 映射 command_and_control |
| `facets.network.direction` | `dictionary` | `commDirection` | ["内到外"] -> "L2W" | `preserve_in_extension_and_review` | confirmed；内到外归一为 L2W |
| `source_finding.attack_direction` | `conditional` | `when wpl.isFromExternal == true && wpl.attackerIp == wpl.dstIp && wpl.victimIp == wpl.srcIp && wpl.commDirection == ["内到外"]` | `when wpl.isFromExternal == true && wpl.attackerIp == wpl.dstIp && wpl.victimIp == wpl.srcIp && wpl.commDirection == ["内到外"] then chars(W2L) else preserve_in_extension_and_review` -> "W2L" | `preserve_in_extension_and_review` | confirmed；攻击方向表达检测主张，不能由通信方向单独推导 |
| `source_finding.status` | `transform` | `disposeState` | `string` -> "1" | `—` | confirmed；保留原始状态码 1 |
| `source_finding.severity` | `transform` | `severity` | `string` -> "3" | `—` | confirmed；保留 NGSOC 原始等级 3 |
| `source_finding.confidence` | `transform` | `confidence` | `string` -> "3" | `—` | confirmed；保留 NGSOC 原始置信度 3 |
| `source_alert_severity` | `transform` | `severity` | `string` -> "3" | `—` | confirmed；保留来源 finding 原始严重度 |
| `severity` | `dictionary` | `severity` | 3 -> "error" | `null_and_review` | confirmed；根据当前 NGSOC 样例分布推测的安全严重度交叉表，由 NGSOC-4.13.1 厂商文档确认 |
| `source_finding.attack_result` | `dictionary` | `attackResult` | 1 -> "success" | `preserve_in_extension_and_review` | confirmed；按当前设备类型候选字典推测攻击结果 |
| `outcome` | `dictionary` | `attackResult` | 1 -> "success" | `unknown_and_review` | confirmed；按当前设备类型候选字典推测攻击结果 |
| `source_finding.compromise_status` | `dictionary` | `compromiseState` | true -> "compromised" | `preserve_in_extension_and_review` | confirmed；布尔值及中文值按当前样例语义推测，由 NGSOC-4.13.1 厂商文档确认 |

### 5.3 编写约束

- dictionary 仅包含当前样例或已有说明能够证明的值；不是完整厂商字典时标记为 partial。
- WPL 负责提取 source 字段，OML 按 kind 和 source 实现赋值。
- 未知枚举不得静默映射为正常业务值；按 unmatched 策略保留、忽略或进入待确认项。
- 现有 legacy adm.oml 的数字码字段不等同于本映射中的 SDM 语义枚举；实现时必须按本表转换并单独做兼容验证。
