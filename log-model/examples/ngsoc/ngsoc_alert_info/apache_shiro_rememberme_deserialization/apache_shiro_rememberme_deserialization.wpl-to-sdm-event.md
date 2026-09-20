# WPL -> SDM Event 字段映射

> 样例：`apache_shiro_rememberme_deserialization.expected-sdm-event.behavior.json（现行）；旧 `*.expected-sdm-event.json` 为 55 列对照`；WPL 输出 18 个命名字段。

## 字段映射

| WPL 来源 | SDM 落位 | 转换/处理 | 说明 |
|---|---|---|---|
| `update_time` | `extensions.source_private.wpl_update_time` | 直接赋值或按说明投影 | Syslog 头缺少年份，WPL 按当前年份推断；仅保留原值，不参与事件时间 |
| `symbol` | `不落库` | 空值或无独立检索价值 | 固定解析标记，无独立检索价值 |
| `name` | `source_finding.title` | 直接赋值或按说明投影 | 来源告警标题 |
| `timestamp` | `occur_time` | 直接赋值或按说明投影 | 正文业务时间已由 WPL 转为毫秒时间戳 |
| `ruleCategoryName` | `source_finding.category.original.name` | 直接赋值或按说明投影 | 来源告警分类 |
| `srcIp` | `roles.source.endpoint.ip + source_ip` | 直接赋值或按说明投影 | 被观测网络行为的发起端；不代替 attackerContent |
| `dstIp` | `roles.target.endpoint.ip + target_ip` | 直接赋值或按说明投影 | 被观测网络行为的目标端；不代替 victimContent |
| `attentionValue` | `source_finding.attention.content` | 直接赋值或按说明投影 | 来源关注内容 |
| `severity` | `source_finding.severity` | 直接赋值或按说明投影 | 保留来源严重度，不覆盖顶层事件严重度 |
| `confidence` | `source_finding.confidence` | 直接赋值或按说明投影 | 保留来源置信度 |
| `compromiseState` | `不落库` | 空值或无独立检索价值 | 空值，不产生失陷状态 |
| `killchain` | `source_finding.killchain` | 受控枚举转换 | 突防利用归一为 exploitation |
| `attackResult` | `source_finding.attack_result + outcome` | 受控枚举转换 | 企图归一为 attempted；顶层 outcome 保守为 unknown |
| `ioc` | `不落库` | 空值或无独立检索价值 | 空数组，不构造 IOC |
| `domain` | `roles.related[].domain.name + extensions.source_private.domain_authority` | 解析单元素 JSON 数组和 host:port | 解析单元素 JSON 数组中的 host:port；没有 DNS 证据时不把端口挂到目标 IP |
| `url` | `不落库` | 空值或无独立检索价值 | 空数组，不构造 URL 或 HTTP 事实 |
| `attackerContent` | `source_finding.attacker.endpoint.ip` | 直接赋值或按说明投影 | NGSOC 检测声明中的攻击方；来源独立于 srcIp |
| `victimContent` | `source_finding.victim.endpoint.ip` | 直接赋值或按说明投影 | NGSOC 检测声明中的受害方；来源独立于 dstIp |

## 平台与派生字段

- `source_original_event_id` 使用完整原始 Syslog 的 SHA-256 确定性生成。
- `event_id` 由 `sha256(tenant_id + mapping_id + source_original_event_id)` 生成。
- `event_type=network_uncategorized`，因为只有端点证据，缺少协议、HTTP 请求和明确连接动作。

## 五、WPL/OML 编写规则

> WPL 只负责提取表中的 source 字段；Meta 和 Content 的赋值由 OML 按下表实现。
> `partial` 表示当前只有样例值或局部说明，不能视为完整厂商字典。

### 5.1 Meta 区

| SDM 字段 | 规则类型 | 输入/来源 | 赋值 | 未命中 | 状态与证据 |
|---|---|---|---|---|---|
| `source_original_event_id/source_finding.original_id` | `derived` | `derived.sha256(raw_input.original_payload)` | `'raw-' + sha256(raw_input.original_payload)` -> "raw-7c850c9422229d40da609862db250795f4a63e8b0d8988148ace827f89914984" | `—` | confirmed；原始日志没有 uuid/seq；完整载荷哈希避免同秒重复告警碰撞 |
| `event_id` | `derived` | `derived.sha256(tenant_id=''|mapping_id|source_original_event_id)` | `derived.sha256(tenant_id=''|mapping_id|source_original_event_id)` -> "evt-8caa2a17b230a7e635fcdf953893862d62a154d9993dc962318f9358ab1bfa03" | `—` | confirmed；确定性事件 ID |
| `record_kind` | `conditional` | `when wpl.name == "Apache Shiro RememberMe反序列化漏洞" && wpl.ruleCategoryName == "代码执行" && wpl.srcIp/wpl.dstIp nonempty` | `when wpl.name == "Apache Shiro RememberMe反序列化漏洞" && wpl.ruleCategoryName == "代码执行" && wpl.srcIp/wpl.dstIp nonempty then chars(finding) else no_match` -> "finding" | `no_match` | confirmed；NGSOC 来源告警 |
| `event_domain` | `conditional` | `when wpl.name == "Apache Shiro RememberMe反序列化漏洞" && wpl.ruleCategoryName == "代码执行" && wpl.srcIp/wpl.dstIp nonempty` | `when wpl.name == "Apache Shiro RememberMe反序列化漏洞" && wpl.ruleCategoryName == "代码执行" && wpl.srcIp/wpl.dstIp nonempty then chars(threat) else no_match` -> "threat" | `no_match` | confirmed；漏洞利用检测语义 |
| `event_type` | `conditional` | `when wpl.name == "Apache Shiro RememberMe反序列化漏洞" && wpl.ruleCategoryName == "代码执行" && wpl.srcIp/wpl.dstIp nonempty` | `when wpl.name == "Apache Shiro RememberMe反序列化漏洞" && wpl.ruleCategoryName == "代码执行" && wpl.srcIp/wpl.dstIp nonempty then chars(network_uncategorized) else no_match` -> "network_uncategorized" | `no_match` | confirmed；只有网络端点，缺少协议、连接动作和 HTTP 请求证据 |
| `operation` | `conditional` | `when event_type == 'network_uncategorized'` | `when event_type == 'network_uncategorized' then chars() else no_match` -> "" | `no_match` | confirmed；无可确认的标准操作 |
| `roles.source.ref_id` | `derived` | `derived.entity_ref(endpoint,exactly_one(wpl.srcIp))` | `derived.entity_ref(endpoint,exactly_one(wpl.srcIp))` -> "endpoint::198.51.100.128" | `drop_and_review` | confirmed；通信起点引用 |
| `roles.target.ref_id` | `derived` | `derived.entity_ref(endpoint,exactly_one(wpl.dstIp))` | `derived.entity_ref(endpoint,exactly_one(wpl.dstIp))` -> "endpoint::203.0.113.204" | `drop_and_review` | confirmed；通信终点引用；域名与目标 IP 无解析关系时不拼接端口 |
| `extensions.source_private.syslog_priority/syslog_host/syslog_header_time` | `derived` | `raw_syslog.header` | `parse_syslog_header(raw_input.original_payload)` | `—` | confirmed；保留优先级、上报主机和无年份头时间 |
| `roles.observer.product.name` | `constant` | `constant.observer_product_display_name` | "NGSOC" | `—` | confirmed；来源产品显示名 |
| `roles.observer.device.vendor` | `constant` | `constant.observer_vendor` | "qax" | `—` | confirmed；来源设备厂商 |
| `roles.observer.device.name` | `derived` | `raw_syslog.header.host` | `read(raw_syslog.header.host)` -> "host-456a5a37.sdm.example.internal" | `—` | confirmed；Syslog 上报主机 |
| `parse_time` | `context` | `platform_context.parse_time` | `read(parse_time)` | `—` | data_gap；真实平台上下文未随样例提供；当前为 null，运行时由接入层赋值 |
| `data_src_instance_id` | `context` | `platform_context.data_src_instance_id` | `read(data_src_instance_id)` | `—` | data_gap；真实平台上下文未随样例提供；当前为 null，运行时由接入层赋值 |
| `tenant_id` | `context` | `platform_context.tenant_id` | `read(tenant_id)` | `—` | data_gap；真实平台上下文未随样例提供；当前为 null，运行时由接入层赋值 |
| `log_id` | `context` | `platform_context.log_id` | `read(log_id)` | `—` | data_gap；真实平台上下文未随样例提供；当前为 null，运行时由接入层赋值 |
| `ingest_time` | `context` | `platform_context.ingest_time` | `read(ingest_time)` | `—` | data_gap；真实平台上下文未随样例提供；当前为 null，运行时由接入层赋值 |
| `data_src_product` | `constant` | `constant.data_src_product` | "ngsoc" | `—` | confirmed；日志类型级常量 |
| `log_type` | `constant` | `constant.log_type` | "ngsoc_alert_info" | `—` | confirmed；日志类型级常量 |
| `data_src_vendor` | `constant` | `constant.data_src_vendor` | "qax" | `—` | confirmed；日志类型级常量 |
| `mapping_id` | `constant` | `constant.mapping_id` | "qax.ngsoc.ngsoc_alert_info" | `—` | confirmed；日志类型级常量 |
| `schema_version` | `constant` | `constant.schema_version` | 2 | `—` | confirmed；日志类型级常量 |
| `observer_product` | `constant` | `constant.observer_product` | "ngsoc" | `—` | confirmed；日志类型级常量 |
| `observer_vendor` | `constant` | `constant.observer_vendor` | "qax" | `—` | confirmed；日志类型级常量 |
| `log_name` | `constant` | `constant.log_name` | "NGSOC告警信息" | `—` | confirmed；日志类型级常量 |
| `data_src_category` | `constant` | `constant.data_src_category` | "security_analytics" | `—` | confirmed；日志类型级常量 |
| `log_level` | `dictionary` | `derived.syslog_severity_code(raw_syslog.header.priority)` | 0 -> "emerg", 1 -> "alert", 2 -> "crit", 3 -> "error", 4 -> "warning", 5 -> "notice", 6 -> "info", 7 -> "debug" | `null_and_review` | confirmed；Syslog PRI 的低 3 位表示来源日志等级，不是 finding 安全严重度 |

### 5.2 Content 区

| SDM 字段 | 规则类型 | WPL 字段 | 映射/赋值 | 未命中 | 状态与证据 |
|---|---|---|---|---|---|
| `extensions.source_private.wpl_update_time` | `projection` | `update_time` | "2026-11-28 14:37:53" | `—` | confirmed；Syslog 头无年份，WPL 推断值仅用于审计 |
| `occur_time` | `projection` | `timestamp` | 1732759249000 | `—` | confirmed；WPL 已完成正文时间转换 |
| `source_finding.title` | `projection` | `name` | "Apache Shiro RememberMe反序列化漏洞" | `—` | confirmed；来源告警标题 |
| `roles.source.endpoint.ip/source_ip` | `transform` | `srcIp` | `exactly_one(wpl.srcIp)` -> "198.51.100.128" | `drop_and_review` | confirmed；被观测网络行为的单一源 IP |
| `roles.target.endpoint.ip/target_ip` | `transform` | `dstIp` | `exactly_one(wpl.dstIp)` -> "203.0.113.204" | `drop_and_review` | confirmed；被观测网络行为的单一目标 IP |
| `source_finding.attacker.endpoint.ip` | `transform` | `attackerContent` | `exactly_one(wpl.attackerContent)` -> "198.51.100.128" | `drop_and_review` | confirmed；NGSOC 明确声明的攻击方 |
| `source_finding.victim.endpoint.ip` | `transform` | `victimContent` | `exactly_one(wpl.victimContent)` -> "203.0.113.204" | `drop_and_review` | confirmed；NGSOC 明确声明的受害方 |
| `roles.related[].domain.name` | `transform` | `domain` | `host(exactly_one(parse_json_array(wpl.domain)))` -> "ifisp.hnrcc.bank" | `drop_and_review` | confirmed；从 host:port 提取域名 |
| `extensions.source_private.domain_authority` | `transform` | `domain` | `exactly_one(parse_json_array(wpl.domain))` -> "ifisp.hnrcc.bank:8008" | `drop_and_review` | confirmed；保留来源 host:port；无 DNS 证据时不投影为 target_port |
| `source_finding.severity` | `projection` | `severity` | "高危" | `—` | confirmed；保留来源严重度 |
| `source_finding.confidence` | `projection` | `confidence` | "中" | `—` | confirmed；保留来源置信度 |
| `source_finding.category.original.name` | `projection` | `ruleCategoryName` | "代码执行" | `—` | confirmed；来源分类 |
| `source_finding.attention.content` | `projection` | `attentionValue` | "目的IP : 203.0.113.204" | `—` | confirmed；来源关注内容 |
| `source_finding.killchain` | `dictionary` | `killchain` | "突防利用" -> "exploitation" | `preserve_in_extension_and_review` | partial；当前样例值映射 |
| `source_alert_severity` | `transform` | `severity` | `string` -> "高危" | `—` | confirmed；保留来源 finding 原始严重度 |
| `severity` | `dictionary` | `severity` | "高危" -> "error" | `null_and_review` | partial；根据当前 NGSOC 样例分布推测的安全严重度交叉表，尚未经厂商确认 |
| `source_finding.attack_result` | `dictionary` | `attackResult` | "企图" -> "attempted" | `preserve_in_extension_and_review` | partial；检测到攻击尝试，但不声明动作成功 |
| `outcome` | `dictionary` | `attackResult` | "企图" -> "observed" | `unknown_and_review` | partial；检测到攻击尝试，但不声明动作成功 |

### 5.3 编写约束

- dictionary 仅包含当前样例能够证明的值，完整厂商字典仍需确认。
- 未知枚举不得静默映射为正常业务值。
- 现有 legacy adm.oml 的数字码字段不等同于本映射中的 SDM 语义枚举。
