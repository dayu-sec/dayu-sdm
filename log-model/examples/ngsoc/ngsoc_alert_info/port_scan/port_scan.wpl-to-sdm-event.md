# WPL -> SDM Event 字段映射

> 样例：`port_scan.expected-sdm-event.json`；WPL 输出 18 个命名字段。

## 字段映射

| WPL 来源 | SDM 落位 | 转换/处理 | 说明 |
|---|---|---|---|
| `update_time` | `extensions.source_private.wpl_update_time` | 解析或投影 | Syslog 头年份由 WPL 按当前年份推断，仅保留审计 |
| `symbol` | `不落库` | 空值或无独立价值 | 固定解析标记，无独立检索价值 |
| `name` | `source_finding.title` | 解析或投影 | 来源告警标题，不扩写为扫描成功 |
| `timestamp` | `occur_time` | 解析或投影 | WPL 已将正文时间转为毫秒时间戳 |
| `ruleCategoryName` | `source_finding.category.original.name` | 解析或投影 | 来源分类 |
| `srcIp` | `roles.source.endpoint.ip + source_ip` | 解析或投影 | 单一扫描发起端 |
| `dstIp` | `roles.target.endpoint.ip + roles.related[].endpoint.ip` | 解析或投影 | 数组第一项按来源顺序投影为代表 target，其余目标以 victim 关系保留；完整列表进入 source_finding.entities.victims |
| `attentionValue` | `source_finding.attention.content` | 解析或投影 | 来源关注内容 |
| `severity` | `source_finding.severity` | 解析或投影 | 来源严重度，不覆盖顶层 Syslog 严重度 |
| `confidence` | `source_finding.confidence` | 解析或投影 | 来源置信度 |
| `compromiseState` | `不落库` | 空值或无独立价值 | 空值，不产生失陷状态 |
| `killchain` | `source_finding.killchain` | 受控枚举转换 | 侦查跟踪归一为 reconnaissance |
| `attackResult` | `source_finding.attack_result` | 受控枚举转换 | 企图归一为 attempted，不驱动顶层 outcome |
| `ioc` | `不落库` | 空值或无独立价值 | 空数组，不构造 IOC |
| `domain` | `不落库` | 空值或无独立价值 | 空数组，不构造域名 |
| `url` | `不落库` | 空值或无独立价值 | 空数组，不构造 URL 或 HTTP 事实 |
| `attackerContent` | `source_finding.attacker.endpoint.ip` | 解析或投影 | 来源声明攻击方，独立于 srcIp |
| `victimContent` | `source_finding.entities.victims[].ref_id` | 解析或投影 | 保留两个并列受害目标；数组第一项仅按来源顺序投影至单值 source_finding.victim |

## 五、WPL/OML 编写规则

> WPL 只负责提取表中的 source 字段；Meta 和 Content 的赋值由 OML 按下表实现。
> `partial` 表示当前只有样例值或局部说明，不能视为完整厂商字典。

### 5.1 Meta 区

| SDM 字段 | 规则类型 | 输入/来源 | 赋值 | 未命中 | 状态与证据 |
|---|---|---|---|---|---|
| `source_original_event_id/source_finding.original_id` | `derived` | `derived.prefixed_sha256('raw-', raw_input.original_payload)` | `'raw-' + sha256(raw_input.original_payload)` -> "raw-29250ea068ce567470bec49eed59ee4a4daebfdc764f6704e7fd1b6bce3b97f8" | `—` | confirmed；原始日志无 uuid/seq；完整载荷哈希 |
| `event_id` | `derived` | `derived.prefixed_sha256('evt-', tenant_id + '|' + mapping_id + '|' + source_original_event_id)` | `'evt-' + sha256(tenant_id + '|' + mapping_id + '|' + source_original_event_id)` -> "evt-9c397f78fabaf41d45ad09b3fcc963e6dbe2843ee6fd7cb6b556380635d3a639" | `—` | confirmed；确定性事件 ID |
| `record_kind` | `conditional` | `when wpl.name == "端口扫描" && wpl.ruleCategoryName == "端口扫描" && exactly_one_nonempty_ip(wpl.srcIp) && nonempty(wpl.dstIp)` | `when wpl.name == "端口扫描" && wpl.ruleCategoryName == "端口扫描" && exactly_one_nonempty_ip(wpl.srcIp) && nonempty(wpl.dstIp) then chars(finding) else no_match` -> "finding" | `no_match` | confirmed；NGSOC 来源告警 |
| `event_domain` | `conditional` | `when wpl.name == "端口扫描" && wpl.ruleCategoryName == "端口扫描" && exactly_one_nonempty_ip(wpl.srcIp) && nonempty(wpl.dstIp)` | `when wpl.name == "端口扫描" && wpl.ruleCategoryName == "端口扫描" && exactly_one_nonempty_ip(wpl.srcIp) && nonempty(wpl.dstIp) then chars(threat) else no_match` -> "threat" | `no_match` | confirmed；来源扫描风险 |
| `event_type` | `conditional` | `when wpl.name == "端口扫描" && wpl.ruleCategoryName == "端口扫描" && exactly_one_nonempty_ip(wpl.srcIp) && nonempty(wpl.dstIp)` | `when wpl.name == "端口扫描" && wpl.ruleCategoryName == "端口扫描" && exactly_one_nonempty_ip(wpl.srcIp) && nonempty(wpl.dstIp) then chars(scan_network) else no_match` -> "scan_network" | `no_match` | confirmed；标题与分类明确声明端口扫描 |
| `operation` | `conditional` | `when event_type == 'scan_network' && no_scan_lifecycle_state` | `when event_type == 'scan_network' && no_scan_lifecycle_state then chars() else no_match` -> "" | `no_match` | confirmed；缺少 started/completed 等扫描生命周期状态 |
| `roles.source.ref_id` | `derived` | `derived.entity_ref(endpoint,exactly_one(wpl.srcIp))` | `'endpoint-' + sha256(exactly_one(wpl.srcIp))[0:32]` -> "endpoint-07d4e40ca2920b225f65c24a7004b8ef" | `drop_and_review` | confirmed；源端点稳定引用 |
| `roles.target.ref_id` | `derived` | `derived.entity_ref(endpoint,first(wpl.dstIp))` | `'endpoint-' + sha256(first(wpl.dstIp))[0:32]` -> "endpoint-41fb5c95dfd58793e758f6de8d8b23c3" | `drop_and_review` | confirmed；target 单值槽位按来源数组顺序选择第一项作为代表目标，不表达主次 |
| `roles.related[0].ref_id` | `derived` | `derived.entity_ref(endpoint,second(wpl.dstIp))` | `derived.entity_ref(endpoint,second(wpl.dstIp))` -> "endpoint-33e6cfd6301e0e3f06497ef044103d72" | `drop_and_review` | confirmed；额外目标稳定引用 |
| `roles.source.entity_type/roles.target.entity_type/roles.related[0].entity_type` | `constant` | `constant.endpoint_entity_type` | "endpoint" | `—` | confirmed；三个 IP 对象均装配为 endpoint |
| `source_finding.entities.victims[].entity_type` | `constant` | `constant.endpoint_entity_type` | "endpoint" | `—` | confirmed；来源受害目标引用均为 endpoint |
| `roles.related[0].relation_type` | `constant` | `constant.victim_relation` | "victim" | `—` | confirmed；victimContent 明确声明第二个端点也是受害目标 |
| `roles.carriers` | `constant` | `constant.empty_carriers` | [] | `—` | confirmed；无协议、进程或会话 |
| `facets` | `constant` | `constant.empty_facets` | {} | `—` | confirmed；无端口、协议和扫描方法字段 |
| `extensions.source_private.syslog_priority/syslog_host/syslog_header_time` | `derived` | `raw_syslog.header` | `parse_syslog_header(raw_input.original_payload)` | `—` | confirmed；保留 Syslog 头 |
| `extensions.schema_version` | `constant` | `constant.extensions_schema_version` | 1 | `—` | confirmed；当前 extensions 契约版本 |
| `extensions.profiles/extensions.enrichments/extensions.unmapped` | `constant` | `constant.empty_extension_containers` | {} | `—` | confirmed；无平台画像、富化或未处理字段 |
| `roles.observer.product.name` | `constant` | `constant.observer_product_display_name` | "NGSOC" | `—` | confirmed；来源产品显示名 |
| `roles.observer.device.vendor` | `constant` | `constant.observer_vendor` | "qax" | `—` | confirmed；来源设备厂商 |
| `roles.observer.device.name` | `derived` | `raw_syslog.header.host` | `read(raw_syslog.header.host)` -> "host-2cfba8ce.sdm.example.internal" | `—` | confirmed；Syslog 上报主机 |
| `tenant_id` | `context` | `platform_context.tenant_id` | "" | `—` | data_gap；平台上下文未提供；运行时赋值 |
| `log_id` | `context` | `platform_context.log_id` | `read(log_id)` | `—` | data_gap；平台上下文未提供；运行时赋值 |
| `ingest_time` | `context` | `platform_context.ingest_time` | `read(ingest_time)` | `—` | data_gap；平台上下文未提供；运行时赋值 |
| `parse_time` | `context` | `platform_context.parse_time` | `read(parse_time)` | `—` | data_gap；平台上下文未提供；运行时赋值 |
| `data_src_instance_id` | `context` | `platform_context.data_src_instance_id` | `read(data_src_instance_id)` | `—` | data_gap；平台上下文未提供；运行时赋值 |
| `data_src_product` | `constant` | `constant.data_src_product` | "ngsoc" | `—` | confirmed；日志类型级常量 |
| `log_type` | `constant` | `constant.log_type` | "ngsoc_alert_info" | `—` | confirmed；日志类型级常量 |
| `data_src_vendor` | `constant` | `constant.data_src_vendor` | "qax" | `—` | confirmed；日志类型级常量 |
| `mapping_id` | `constant` | `constant.mapping_id` | "qax.ngsoc.ngsoc_alert_info" | `—` | confirmed；日志类型级常量 |
| `schema_version` | `constant` | `constant.schema_version` | 1 | `—` | confirmed；日志类型级常量 |
| `observer_product` | `constant` | `constant.observer_product` | "ngsoc" | `—` | confirmed；日志类型级常量 |
| `observer_vendor` | `constant` | `constant.observer_vendor` | "qax" | `—` | confirmed；日志类型级常量 |
| `log_name` | `constant` | `constant.log_name` | "NGSOC告警信息" | `—` | confirmed；日志类型级常量 |
| `data_src_category` | `constant` | `constant.data_src_category` | "security_analytics" | `—` | confirmed；日志类型级常量 |
| `log_level` | `dictionary` | `derived.syslog_severity_code(raw_syslog.header.priority)` | 0 -> "emerg", 1 -> "alert", 2 -> "crit", 3 -> "error", 4 -> "warning", 5 -> "notice", 6 -> "info", 7 -> "debug" | `null_and_review` | confirmed；Syslog PRI 的低 3 位表示来源日志等级，不是 finding 安全严重度 |

### 5.2 Content 区

| SDM 字段 | 规则类型 | WPL 字段 | 映射/赋值 | 未命中 | 状态与证据 |
|---|---|---|---|---|---|
| `extensions.source_private.wpl_update_time` | `projection` | `update_time` | "2026-11-29 09:16:26" | `—` | confirmed；WPL 推断值仅用于审计 |
| `occur_time` | `projection` | `timestamp` | 1732838634000 | `—` | confirmed；WPL 已完成时间转换 |
| `source_finding.title` | `projection` | `name` | "端口扫描" | `—` | confirmed；来源告警标题 |
| `roles.source.endpoint.ip/source_ip` | `transform` | `srcIp` | `exactly_one(wpl.srcIp)` -> "203.0.113.69" | `drop_and_review` | confirmed；单一源 IP |
| `roles.target.endpoint.ip/target_ip` | `transform` | `dstIp[0]` | `first(wpl.dstIp)` -> "198.51.100.151" | `drop_and_review` | confirmed；数组第一项按来源顺序投影为代表 target，不表达主次 |
| `roles.related[0].endpoint.ip` | `transform` | `dstIp[1]` | `second(wpl.dstIp)` -> "203.0.113.23" | `drop_and_review` | confirmed；第二个并列受害目标使用 victim 关系保留 |
| `source_finding.attacker.endpoint.ip` | `transform` | `attackerContent` | `exactly_one(wpl.attackerContent)` -> "203.0.113.69" | `drop_and_review` | confirmed；来源声明攻击方 |
| `source_finding.victim.endpoint.ip` | `transform` | `victimContent[0]` | `first(wpl.victimContent)` -> "198.51.100.151" | `drop_and_review` | confirmed；单值 victim 投影使用首个来源受害目标 |
| `source_finding.entities.victims[].ref_id` | `transform` | `victimContent` | `map(derived.entity_ref(endpoint, item), wpl.victimContent)` -> ["endpoint-41fb5c95dfd58793e758f6de8d8b23c3", "endpoint-33e6cfd6301e0e3f06497ef044103d72"] | `drop_and_review` | confirmed；完整保留两个来源声明受害目标 |
| `source_finding.severity` | `projection` | `severity` | "中危" | `—` | confirmed；来源严重度 |
| `source_finding.confidence` | `projection` | `confidence` | "高" | `—` | confirmed；来源置信度 |
| `source_finding.category.original.name` | `projection` | `ruleCategoryName` | "端口扫描" | `—` | confirmed；来源分类 |
| `source_finding.attention.content` | `projection` | `attentionValue` | "源IP : 203.0.113.69" | `—` | confirmed；来源关注内容 |
| `source_finding.killchain` | `dictionary` | `killchain` | "侦查跟踪" -> "reconnaissance" | `preserve_in_extension_and_review` | partial；当前样例值映射 |
| `source_alert_severity` | `transform` | `severity` | `string` -> "中危" | `—` | confirmed；保留来源 finding 原始严重度 |
| `severity` | `dictionary` | `severity` | "中危" -> "warning" | `null_and_review` | partial；根据当前 NGSOC 样例分布推测的安全严重度交叉表，尚未经厂商确认 |
| `source_finding.attack_result` | `dictionary` | `attackResult` | "企图" -> "attempted" | `preserve_in_extension_and_review` | partial；检测到攻击尝试，但不声明动作成功 |
| `outcome` | `dictionary` | `attackResult` | "企图" -> "observed" | `unknown_and_review` | partial；检测到攻击尝试，但不声明动作成功 |

### 5.3 编写约束

- 多目标字段完整保存在 source_finding.entities.victims；roles.target 按来源数组顺序选择第一项作为代表目标，不表达主次，第二目标使用 victim 关系。
- dictionary 仅包含当前样例值，完整厂商字典仍需确认。
- 没有端口、协议、扫描方法或响应证据，不生成 network scan facet。
