# WPL -> SDM Event 字段映射

> 样例：`mysql_database_list_read.expected-sdm-event.json`；WPL 输出 18 个命名字段。

## 字段映射

| WPL 来源 | SDM 落位 | 转换/处理 | 说明 |
|---|---|---|---|
| `update_time` | `extensions.source_private.wpl_update_time` | 解析或投影 | Syslog 头年份由 WPL 按当前年份推断，仅保留审计 |
| `symbol` | `不落库` | 空值或无独立价值 | 固定解析标记，无独立检索价值 |
| `name` | `source_finding.title` | 解析或投影 | 来源告警标题；不构造实际数据库列表读取事实 |
| `timestamp` | `occur_time` | 解析或投影 | WPL 已将正文时间转为毫秒时间戳 |
| `ruleCategoryName` | `source_finding.category.original.name` | 解析或投影 | 来源分类 |
| `srcIp` | `roles.source.endpoint.ip + source_ip` | 解析或投影 | 被观测行为发起端，不代替 attackerContent |
| `dstIp` | `roles.target.endpoint.ip + target_ip` | 解析或投影 | 被观测目标端，不代替 victimContent |
| `attentionValue` | `source_finding.attention.content` | 解析或投影 | 来源关注内容 |
| `severity` | `source_finding.severity` | 解析或投影 | 来源严重度，不覆盖顶层 Syslog 严重度 |
| `confidence` | `source_finding.confidence` | 解析或投影 | 来源置信度 |
| `compromiseState` | `不落库` | 空值或无独立价值 | 空值，不产生失陷状态 |
| `killchain` | `source_finding.killchain` | 受控枚举转换 | 突防利用归一为 exploitation |
| `attackResult` | `source_finding.attack_result` | 受控枚举转换 | 成功归一为 success；仅表示来源声明，不驱动顶层 outcome |
| `ioc` | `不落库` | 空值或无独立价值 | 空数组，不构造 IOC |
| `domain` | `不落库` | 空值或无独立价值 | 空数组，不构造域名或数据库服务 |
| `url` | `不落库` | 空值或无独立价值 | 空数组，不构造 URL |
| `attackerContent` | `source_finding.attacker.endpoint.ip` | 解析或投影 | 来源声明攻击方，独立于 srcIp |
| `victimContent` | `source_finding.victim.endpoint.ip` | 解析或投影 | 来源声明受害方，独立于 dstIp |

## 五、WPL/OML 编写规则

> WPL 只负责提取表中的 source 字段；Meta 和 Content 的赋值由 OML 按下表实现。
> `partial` 表示当前只有样例值或局部说明，不能视为完整厂商字典。

### 5.1 Meta 区

| SDM 字段 | 规则类型 | 输入/来源 | 赋值 | 未命中 | 状态与证据 |
|---|---|---|---|---|---|
| `source_original_event_id/source_finding.original_id` | `derived` | `derived.prefixed_sha256('raw-', raw_input.original_payload)` | `'raw-' + sha256(raw_input.original_payload)` -> "raw-50066c030b57ac43c66ad919639af3dbe5c491b576b9be2b450b0753fc7ff043" | `—` | confirmed；原始日志无 uuid/seq；完整载荷哈希 |
| `event_id` | `derived` | `derived.prefixed_sha256('evt-', tenant_id + '|' + mapping_id + '|' + source_original_event_id)` | `'evt-' + sha256(tenant_id + '|' + mapping_id + '|' + source_original_event_id)` -> "evt-ca168be73c9bdb9a6a6d51addf1ef04f6b05d5bba2dd7e0964017f66f9f0c372" | `—` | confirmed；确定性事件 ID |
| `record_kind` | `conditional` | `when wpl.name == "MySQL 读取数据库列表" && wpl.ruleCategoryName == "敏感操作"` | `when wpl.name == "MySQL 读取数据库列表" && wpl.ruleCategoryName == "敏感操作" then chars(finding) else no_match` -> "finding" | `no_match` | confirmed；NGSOC 来源告警 |
| `event_domain` | `conditional` | `when wpl.name == "MySQL 读取数据库列表" && wpl.ruleCategoryName == "敏感操作"` | `when wpl.name == "MySQL 读取数据库列表" && wpl.ruleCategoryName == "敏感操作" then chars(threat) else no_match` -> "threat" | `no_match` | confirmed；来源声明敏感数据库操作风险 |
| `event_type` | `conditional` | `when wpl.name == "MySQL 读取数据库列表" && wpl.ruleCategoryName == "敏感操作"` | `when wpl.name == "MySQL 读取数据库列表" && wpl.ruleCategoryName == "敏感操作" then chars(network_uncategorized) else no_match` -> "network_uncategorized" | `no_match` | confirmed；缺少端口、协议、SQL、数据库名和响应证据 |
| `operation` | `conditional` | `when event_type == 'network_uncategorized'` | `when event_type == 'network_uncategorized' then chars() else no_match` -> "" | `no_match` | confirmed；无可确认标准操作 |
| `roles.source.ref_id/roles.source.entity_type` | `conditional` | `when exactly_one_nonempty_ip(wpl.srcIp)` | `when exactly_one_nonempty_ip(wpl.srcIp) then endpoint_ref(exactly_one(wpl.srcIp)) else omit_role_and_review` -> {"ref_id": "endpoint-80989d22612183ad18bdbed1eb41bd6b", "entity_type": "endpoint"} | `omit_role_and_review` | confirmed；源角色装配独立于日志类型命中；多值或缺失时不丢弃事件 |
| `roles.target.ref_id/roles.target.entity_type` | `conditional` | `when exactly_one_nonempty_ip(wpl.dstIp)` | `when exactly_one_nonempty_ip(wpl.dstIp) then endpoint_ref(exactly_one(wpl.dstIp)) else omit_role_and_review` -> {"ref_id": "endpoint-611cf4a4c76313caaecc8cb0b321e9c4", "entity_type": "endpoint"} | `omit_role_and_review` | confirmed；目标角色装配独立于日志类型命中；多值或缺失时不丢弃事件 |
| `roles.carriers/roles.related` | `constant` | `constant.empty_role_arrays` | [] | `—` | confirmed；无进程、协议、会话、服务或关联实体证据 |
| `facets` | `constant` | `constant.empty_facets` | {} | `—` | confirmed；无 SQL、数据库对象、协议或响应内容 |
| `extensions.source_private.syslog_priority/syslog_host/syslog_header_time` | `derived` | `raw_syslog.header` | `parse_syslog_header(raw_input.original_payload)` | `—` | confirmed；保留 Syslog 头 |
| `extensions.schema_version` | `constant` | `constant.extensions_schema_version` | 1 | `—` | confirmed；当前 extensions 契约版本 |
| `extensions.profiles/extensions.enrichments` | `constant` | `constant.empty_extension_containers` | {} | `—` | confirmed；无平台画像或富化字段 |
| `extensions.unmapped` | `derived` | `derived.unmatched_enum_values(wpl.killchain,wpl.attackResult)` | `object(killchain=unknown(wpl.killchain), attack_result=unknown(wpl.attackResult))` -> {} | `—` | confirmed；仅保留未命中字典的非空原值；当前样例均命中，所以为空对象 |
| `roles.observer.product.name` | `constant` | `constant.observer_product_display_name` | "NGSOC" | `—` | confirmed；来源产品显示名 |
| `roles.observer.device.vendor` | `constant` | `constant.observer_vendor` | "qax" | `—` | confirmed；来源设备厂商 |
| `roles.observer.device.name` | `derived` | `raw_syslog.header.host` | `read(raw_syslog.header.host)` -> "ngsoc94.qax.cn" | `—` | confirmed；Syslog 上报主机 |
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
| `extensions.source_private.wpl_update_time` | `projection` | `update_time` | "2026-11-29 09:15:56" | `—` | confirmed；WPL 推断值仅用于审计 |
| `occur_time` | `projection` | `timestamp` | 1732842946000 | `—` | confirmed；WPL 已完成时间转换 |
| `source_finding.title` | `projection` | `name` | "MySQL 读取数据库列表" | `—` | confirmed；来源告警标题 |
| `roles.source.endpoint.ip/source_ip` | `transform` | `srcIp` | `exactly_one(wpl.srcIp)` -> "203.0.113.91" | `omit_role_and_review` | confirmed；单一源 IP；多值或缺失只跳过源角色，不影响日志类型命中 |
| `roles.target.endpoint.ip/target_ip` | `transform` | `dstIp` | `exactly_one(wpl.dstIp)` -> "198.51.100.100" | `omit_role_and_review` | confirmed；单一目标 IP；多值或缺失只跳过目标角色，不影响日志类型命中 |
| `source_finding.attacker.endpoint.ip` | `transform` | `attackerContent` | `exactly_one(wpl.attackerContent)` -> "203.0.113.91" | `drop_and_review` | confirmed；来源声明攻击方 |
| `source_finding.victim.endpoint.ip` | `transform` | `victimContent` | `exactly_one(wpl.victimContent)` -> "198.51.100.100" | `drop_and_review` | confirmed；来源声明受害方 |
| `source_finding.severity` | `projection` | `severity` | "中危" | `—` | confirmed；来源严重度 |
| `source_finding.confidence` | `projection` | `confidence` | "中" | `—` | confirmed；来源置信度 |
| `source_finding.category.original.name` | `projection` | `ruleCategoryName` | "敏感操作" | `—` | confirmed；来源分类 |
| `source_finding.attention.content` | `projection` | `attentionValue` | "源IP : 203.0.113.91" | `—` | confirmed；来源关注内容 |
| `source_finding.killchain` | `dictionary` | `killchain` | "突防利用" -> "exploitation" | `extensions.unmapped.killchain=original_value_and_review` | partial；当前样例值映射；未知非空值保留原文 |
| `source_alert_severity` | `transform` | `severity` | `string` -> "中危" | `—` | confirmed；保留来源 finding 原始严重度 |
| `severity` | `dictionary` | `severity` | "中危" -> "warning" | `null_and_review` | partial；根据当前 NGSOC 样例分布推测的安全严重度交叉表，尚未经厂商确认 |
| `source_finding.attack_result` | `dictionary` | `attackResult` | "成功" -> "success" | `preserve_in_extension_and_review` | partial；中文值明确声明成功 |
| `outcome` | `dictionary` | `attackResult` | "成功" -> "success" | `unknown_and_review` | partial；中文值明确声明成功 |

### 5.3 编写约束

- MySQL 与读取数据库列表均为来源告警声明；没有 SQL、数据库名、列表内容或响应证据，不生成数据库读取事实。
- attackResult=成功只映射 source_finding.attack_result=success，顶层 outcome 保持 success。
- 日志类型命中不依赖 IP 基数；srcIp/dstIp 多值或缺失时仅跳过对应角色并进入 review。
- killchain/attackResult 的未知非空值分别保留到 extensions.unmapped.killchain/attack_result。
- 没有端口、协议、会话或服务证据，carriers/related/facets 均为空。
