# WPL -> SDM Event 字段映射

> 样例：`sensitive_java_source_leak.expected-sdm-event.json`；WPL 输出 18 个命名字段。

## 字段映射

| WPL 来源 | SDM 落位 | 转换/处理 | 说明 |
|---|---|---|---|
| `update_time` | `extensions.source_private.wpl_update_time` | 解析或投影 | Syslog 头缺少年份，WPL 按当前年份推断；仅保留审计，不参与事件时间 |
| `symbol` | `不落库` | 空值或无独立价值 | 固定解析标记，无独立检索价值 |
| `name` | `source_finding.title` | 解析或投影 | 来源告警标题；不是源码已被读取的客观事实 |
| `timestamp` | `occur_time` | 解析或投影 | 正文业务时间已由 WPL 转为毫秒时间戳 |
| `ruleCategoryName` | `source_finding.category.original.name` | 解析或投影 | 来源告警分类 |
| `srcIp` | `roles.source.endpoint.ip + source_ip` | 解析或投影 | 被观测网络行为的发起端；不代替 attackerContent |
| `dstIp` | `roles.target.endpoint.ip + target_ip` | 解析或投影 | 被观测网络行为的目标端；不代替 victimContent |
| `attentionValue` | `source_finding.attention.content` | 解析或投影 | 来源关注内容 |
| `severity` | `source_finding.severity` | 解析或投影 | 保留来源严重度，不覆盖顶层 Syslog 严重度 |
| `confidence` | `source_finding.confidence` | 解析或投影 | 保留来源置信度 |
| `compromiseState` | `不落库` | 空值或无独立价值 | 空值，不产生失陷状态 |
| `killchain` | `不落库` | 空值或无独立价值 | 空值，不产生杀伤链阶段 |
| `attackResult` | `不落库` | 空值或无独立价值 | 空值，不产生来源攻击结果；顶层 outcome 由 finding 事件语义确定 |
| `ioc` | `不落库` | 空值或无独立价值 | 空数组，不构造 IOC |
| `domain` | `roles.target.endpoint.port + target_port + extensions.source_private.domain_authority` | 解析或投影 | 解析 IP:port authority；host 与 dstIp 完全相同，因此提取目标端口并保留原值 |
| `url` | `不落库` | 空值或无独立价值 | 空数组，不构造 URL 或 HTTP 事实 |
| `attackerContent` | `source_finding.attacker.endpoint.ip` | 解析或投影 | NGSOC 检测声明中的攻击方；来源独立于 srcIp |
| `victimContent` | `source_finding.victim.endpoint.ip` | 解析或投影 | NGSOC 检测声明中的受害方；来源独立于 dstIp |

## 五、WPL/OML 编写规则

> WPL 只负责提取表中的 source 字段；Meta 和 Content 的赋值由 OML 按下表实现。
> `partial` 表示当前只有样例值或局部说明，不能视为完整厂商字典。

### 5.1 Meta 区

| SDM 字段 | 规则类型 | 输入/来源 | 赋值 | 未命中 | 状态与证据 |
|---|---|---|---|---|---|
| `source_original_event_id/source_finding.original_id` | `derived` | `derived.prefixed_sha256('raw-', raw_input.original_payload)` | `'raw-' + sha256(raw_input.original_payload)` -> "raw-4916493c45b107dc3e97d26d647c741ec618a71d8ef956d4931d2e84e7d1372f" | `—` | confirmed；原始日志无 uuid/seq；使用完整载荷哈希 |
| `event_id` | `derived` | `derived.prefixed_sha256('evt-', tenant_id + '|' + mapping_id + '|' + source_original_event_id)` | `'evt-' + sha256(tenant_id + '|' + mapping_id + '|' + source_original_event_id)` -> "evt-f31f8881a9a28bb2e3c44c040b312d761040ceadfe20a1f2992809faa2dcf45d" | `—` | confirmed；带 evt- 前缀的确定性事件 ID |
| `record_kind` | `conditional` | `when wpl.name == "敏感信息泄露_Java源码泄露" && wpl.ruleCategoryName == "信息泄露" && exactly_one_nonempty_ip(wpl.srcIp) && exactly_one_nonempty_ip(wpl.dstIp)` | `when wpl.name == "敏感信息泄露_Java源码泄露" && wpl.ruleCategoryName == "信息泄露" && exactly_one_nonempty_ip(wpl.srcIp) && exactly_one_nonempty_ip(wpl.dstIp) then chars(finding) else no_match` -> "finding" | `no_match` | confirmed；NGSOC 来源告警 |
| `event_domain` | `conditional` | `when wpl.name == "敏感信息泄露_Java源码泄露" && wpl.ruleCategoryName == "信息泄露" && exactly_one_nonempty_ip(wpl.srcIp) && exactly_one_nonempty_ip(wpl.dstIp)` | `when wpl.name == "敏感信息泄露_Java源码泄露" && wpl.ruleCategoryName == "信息泄露" && exactly_one_nonempty_ip(wpl.srcIp) && exactly_one_nonempty_ip(wpl.dstIp) then chars(threat) else no_match` -> "threat" | `no_match` | confirmed；来源声明敏感信息泄露风险 |
| `event_type` | `conditional` | `when wpl.name == "敏感信息泄露_Java源码泄露" && wpl.ruleCategoryName == "信息泄露" && exactly_one_nonempty_ip(wpl.srcIp) && exactly_one_nonempty_ip(wpl.dstIp)` | `when wpl.name == "敏感信息泄露_Java源码泄露" && wpl.ruleCategoryName == "信息泄露" && exactly_one_nonempty_ip(wpl.srcIp) && exactly_one_nonempty_ip(wpl.dstIp) then chars(network_uncategorized) else no_match` -> "network_uncategorized" | `no_match` | confirmed；缺少 HTTP 请求、文件路径和响应内容证据 |
| `operation` | `conditional` | `when event_type == 'network_uncategorized'` | `when event_type == 'network_uncategorized' then chars() else no_match` -> "" | `no_match` | confirmed；无可确认的标准操作 |
| `roles.source.ref_id` | `derived` | `derived.entity_ref(endpoint,exactly_one(wpl.srcIp))` | `derived.entity_ref(endpoint,exactly_one(wpl.srcIp))` -> "endpoint::192.0.2.52" | `drop_and_review` | confirmed；源端点引用 |
| `roles.source.entity_type` | `constant` | `constant.source_entity_type` | "endpoint" | `—` | confirmed；srcIp 装配为 endpoint |
| `roles.target.ref_id` | `derived` | `derived.entity_ref(endpoint,exactly_one(wpl.dstIp))` | `derived.entity_ref(endpoint,exactly_one(wpl.dstIp))` -> "endpoint::192.0.2.234" | `drop_and_review` | confirmed；目标引用只由 dstIp 生成；可选 authority 端口不改变实体引用 |
| `roles.target.entity_type` | `constant` | `constant.target_entity_type` | "endpoint" | `—` | confirmed；dstIp 装配为 endpoint |
| `roles.carriers` | `constant` | `constant.empty_carriers` | [] | `—` | confirmed；无可确认载体 |
| `roles.related` | `constant` | `constant.empty_related` | [] | `—` | confirmed；authority host 与目标 IP 重复，不创建关联域名 |
| `facets` | `constant` | `constant.empty_facets` | {} | `—` | confirmed；无协议、HTTP 请求、文件和响应事实 |
| `extensions.source_private.syslog_priority/syslog_host/syslog_header_time` | `derived` | `raw_syslog.header` | `parse_syslog_header(raw_input.original_payload)` | `—` | confirmed；保留 Syslog 头 |
| `extensions.schema_version` | `constant` | `constant.extensions_schema_version` | 1 | `—` | confirmed；当前 extensions 契约版本 |
| `extensions.profiles` | `constant` | `constant.empty_profiles` | {} | `—` | confirmed；无平台画像 |
| `extensions.enrichments` | `constant` | `constant.empty_enrichments` | {} | `—` | confirmed；无平台富化 |
| `extensions.unmapped` | `constant` | `constant.empty_unmapped` | {} | `—` | confirmed；全部字段已明确处理 |
| `roles.observer.product.name` | `constant` | `constant.observer_product_display_name` | "NGSOC" | `—` | confirmed；来源产品显示名 |
| `roles.observer.device.vendor` | `constant` | `constant.observer_vendor` | "qax" | `—` | confirmed；来源设备厂商 |
| `roles.observer.device.name` | `derived` | `raw_syslog.header.host` | `read(raw_syslog.header.host)` -> "host-2cfba8ce.sdm.example.internal" | `—` | confirmed；Syslog 上报主机 |
| `tenant_id` | `context` | `platform_context.tenant_id` | "" | `—` | data_gap；真实平台上下文未随样例提供；运行时赋值 |
| `log_id` | `context` | `platform_context.log_id` | `read(log_id)` | `—` | data_gap；真实平台上下文未随样例提供；运行时赋值 |
| `ingest_time` | `context` | `platform_context.ingest_time` | `read(ingest_time)` | `—` | data_gap；真实平台上下文未随样例提供；运行时赋值 |
| `parse_time` | `context` | `platform_context.parse_time` | `read(parse_time)` | `—` | data_gap；真实平台上下文未随样例提供；运行时赋值 |
| `data_src_instance_id` | `context` | `platform_context.data_src_instance_id` | `read(data_src_instance_id)` | `—` | data_gap；真实平台上下文未随样例提供；运行时赋值 |
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
| `extensions.source_private.wpl_update_time` | `projection` | `update_time` | "2026-11-29 09:17:05" | `—` | confirmed；WPL 推断值仅用于审计 |
| `occur_time` | `projection` | `timestamp` | 1732840688000 | `—` | confirmed；WPL 已完成正文时间转换 |
| `source_finding.title` | `projection` | `name` | "敏感信息泄露_Java源码泄露" | `—` | confirmed；来源告警标题 |
| `roles.source.endpoint.ip/source_ip` | `transform` | `srcIp` | `exactly_one(wpl.srcIp)` -> "192.0.2.52" | `drop_and_review` | confirmed；单一源 IP |
| `roles.target.endpoint.ip/target_ip` | `transform` | `dstIp` | `exactly_one(wpl.dstIp)` -> "192.0.2.234" | `drop_and_review` | confirmed；单一目标 IP |
| `roles.target.endpoint.port/target_port` | `transform` | `domain` | `when host(exactly_one(parse_json_array(wpl.domain))) == exactly_one(wpl.dstIp) then port(exactly_one(parse_json_array(wpl.domain))) else drop_and_review` -> 8080 | `drop_and_review` | confirmed；authority host 与 dstIp 完全相同时提取端口 |
| `extensions.source_private.domain_authority` | `transform` | `domain` | `exactly_one(parse_json_array(wpl.domain))` -> "192.0.2.234:8080" | `drop_and_review` | confirmed；保留来源 authority 原值 |
| `source_finding.attacker.endpoint.ip` | `transform` | `attackerContent` | `exactly_one(wpl.attackerContent)` -> "192.0.2.52" | `drop_and_review` | confirmed；来源声明攻击方 |
| `source_finding.victim.endpoint.ip` | `transform` | `victimContent` | `exactly_one(wpl.victimContent)` -> "192.0.2.234" | `drop_and_review` | confirmed；来源声明受害方 |
| `source_finding.severity` | `projection` | `severity` | "高危" | `—` | confirmed；来源严重度 |
| `source_finding.confidence` | `projection` | `confidence` | "高" | `—` | confirmed；来源置信度 |
| `source_finding.category.original.name` | `projection` | `ruleCategoryName` | "信息泄露" | `—` | confirmed；来源分类 |
| `source_finding.attention.content` | `projection` | `attentionValue` | "目的IP : 192.0.2.234" | `—` | confirmed；来源关注内容 |
| `source_alert_severity` | `transform` | `severity` | `string` -> "高危" | `—` | confirmed；保留来源 finding 原始严重度 |
| `severity` | `dictionary` | `severity` | "高危" -> "error" | `null_and_review` | partial；根据当前 NGSOC 样例分布推测的安全严重度交叉表，尚未经厂商确认 |
| `outcome` | `gap` | `data_gap.no_action_result` | "unknown" | `unknown` | missing；原始日志没有明确的底层动作结果字段或事件事实 |

### 5.3 编写约束

- 来源 killchain 和 attackResult 为空，不生成正常化值。
- Java 源码泄露是来源告警声明，不生成文件读取或实际泄露事实。
- authority host 必须与 dstIp 完全相同才能提取 target_port。
