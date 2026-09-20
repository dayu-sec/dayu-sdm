# WPL -> SDM Event 字段映射

> 样例：`bastion_host_bypass_login.expected-sdm-event.behavior.json（现行）；旧 `*.expected-sdm-event.json` 为 55 列对照`；WPL 输出 18 个命名字段。

## 字段映射

| WPL 来源 | SDM 落位 | 转换/处理 | 说明 |
|---|---|---|---|
| `update_time` | `extensions.source_private.wpl_update_time` | 解析或投影 | Syslog 头年份由 WPL 按当前年份推断，仅保留审计 |
| `symbol` | `不落库` | 空值或无独立价值 | 固定解析标记，无独立检索价值 |
| `name` | `source_finding.title` | 解析或投影 | 来源告警标题；仅支持 user_login finding 分类，不证明实际登录 |
| `timestamp` | `occur_time` | 解析或投影 | WPL 已将正文时间转为毫秒时间戳 |
| `ruleCategoryName` | `source_finding.category.original.name` | 解析或投影 | 来源分类 |
| `srcIp` | `roles.source.endpoint.ip + source_ip` | 解析或投影 | 被观测行为发起端，不代替 attackerContent |
| `dstIp` | `roles.target.endpoint.ip + target_ip` | 解析或投影 | 被观测目标端，不代替 victimContent |
| `attentionValue` | `source_finding.attention.content + facets.application.name` | 解析或投影 | 完整保留关注内容，并从明确的协议标签提取 ssh 作为应用名称 |
| `severity` | `source_finding.severity` | 解析或投影 | 来源严重度，不覆盖顶层 Syslog 严重度 |
| `confidence` | `source_finding.confidence` | 解析或投影 | 来源置信度 |
| `compromiseState` | `不落库` | 空值或无独立价值 | 空值，不产生失陷状态 |
| `killchain` | `不落库` | 空值或无独立价值 | 空值，不产生杀伤链阶段 |
| `attackResult` | `不落库` | 空值或无独立价值 | 空值，不产生来源攻击结果；顶层 outcome 由 finding 语义确定 |
| `ioc` | `不落库` | 空值或无独立价值 | 空数组，不构造 IOC |
| `domain` | `不落库` | 空值或无独立价值 | 空数组，不构造域名 |
| `url` | `不落库` | 空值或无独立价值 | 空数组，不构造 URL |
| `attackerContent` | `source_finding.attacker.endpoint.ip` | 解析或投影 | 来源声明攻击方，独立于 srcIp |
| `victimContent` | `source_finding.victim.endpoint.ip` | 解析或投影 | 来源声明受害方，独立于 dstIp |

## 五、WPL/OML 编写规则

> WPL 只负责提取表中的 source 字段；Meta 和 Content 的赋值由 OML 按下表实现。
> `partial` 表示当前只有样例值或局部说明，不能视为完整厂商字典。

### 5.1 Meta 区

| SDM 字段 | 规则类型 | 输入/来源 | 赋值 | 未命中 | 状态与证据 |
|---|---|---|---|---|---|
| `source_original_event_id/source_finding.original_id` | `derived` | `derived.prefixed_sha256('raw-', raw_input.original_payload)` | `'raw-' + sha256(raw_input.original_payload)` -> "raw-0c8ea5ceb90db923b263da0d8614ab5b6ea75ecefb7a2f97af219ad06e5417d6" | `—` | confirmed；原始日志无 uuid/seq；完整载荷哈希 |
| `event_id` | `derived` | `derived.prefixed_sha256('evt-', tenant_id + '|' + mapping_id + '|' + source_original_event_id)` | `'evt-' + sha256(tenant_id + '|' + mapping_id + '|' + source_original_event_id)` -> "evt-87aa2cb0b329377df9ebd74125f342f64cc2fd7c6300cb8c9bf0ec814a82a44a" | `—` | confirmed；确定性事件 ID |
| `record_kind` | `conditional` | `when wpl.name == "定制-绕过堡垒机登录服务器" && wpl.ruleCategoryName == "其它类攻击利用" && exactly_one_nonempty_ip(wpl.srcIp) && exactly_one_nonempty_ip(wpl.dstIp)` | `when wpl.name == "定制-绕过堡垒机登录服务器" && wpl.ruleCategoryName == "其它类攻击利用" && exactly_one_nonempty_ip(wpl.srcIp) && exactly_one_nonempty_ip(wpl.dstIp) then chars(finding) else no_match` -> "finding" | `no_match` | confirmed；NGSOC 来源告警 |
| `event_domain` | `conditional` | `when wpl.name == "定制-绕过堡垒机登录服务器" && wpl.ruleCategoryName == "其它类攻击利用" && exactly_one_nonempty_ip(wpl.srcIp) && exactly_one_nonempty_ip(wpl.dstIp)` | `when wpl.name == "定制-绕过堡垒机登录服务器" && wpl.ruleCategoryName == "其它类攻击利用" && exactly_one_nonempty_ip(wpl.srcIp) && exactly_one_nonempty_ip(wpl.dstIp) then chars(identity) else no_match` -> "identity" | `no_match` | confirmed；来源标题指向登录身份活动 |
| `event_type` | `conditional` | `when wpl.name == "定制-绕过堡垒机登录服务器" && wpl.ruleCategoryName == "其它类攻击利用" && exactly_one_nonempty_ip(wpl.srcIp) && exactly_one_nonempty_ip(wpl.dstIp)` | `when wpl.name == "定制-绕过堡垒机登录服务器" && wpl.ruleCategoryName == "其它类攻击利用" && exactly_one_nonempty_ip(wpl.srcIp) && exactly_one_nonempty_ip(wpl.dstIp) then chars(user_login) else no_match` -> "user_login" | `no_match` | confirmed；来源标题明确声明绕过堡垒机登录服务器风险 |
| `operation` | `conditional` | `when event_type == 'user_login' && no_auth_operation` | `when event_type == 'user_login' && no_auth_operation then chars() else no_match` -> "" | `no_match` | confirmed；缺少可确认的登录子类型与认证动作 |
| `roles.source.ref_id` | `derived` | `derived.entity_ref(endpoint,exactly_one(wpl.srcIp))` | `'endpoint-' + sha256(exactly_one(wpl.srcIp))[0:32]` -> "endpoint-fd899a7d94945bc9ed834886bdd5972f" | `drop_and_review` | confirmed；源端点稳定引用 |
| `roles.target.ref_id` | `derived` | `derived.entity_ref(endpoint,exactly_one(wpl.dstIp))` | `'endpoint-' + sha256(exactly_one(wpl.dstIp))[0:32]` -> "endpoint-fe8eb44d23bb5c034e292d57c979a1de" | `drop_and_review` | confirmed；目标端点稳定引用 |
| `roles.source.entity_type/roles.target.entity_type` | `constant` | `constant.endpoint_entity_type` | "endpoint" | `—` | confirmed；srcIp/dstIp 装配为 endpoint |
| `roles.carriers/roles.related` | `constant` | `constant.empty_role_arrays` | [] | `—` | confirmed；无进程、会话、独立服务实体或关联实体证据 |
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
| `extensions.source_private.wpl_update_time` | `projection` | `update_time` | "2026-11-29 09:16:21" | `—` | confirmed；WPL 推断值仅用于审计 |
| `occur_time` | `projection` | `timestamp` | 1732819726000 | `—` | confirmed；WPL 已完成时间转换 |
| `source_finding.title` | `projection` | `name` | "定制-绕过堡垒机登录服务器" | `—` | confirmed；来源告警标题 |
| `roles.source.endpoint.ip/source_ip` | `transform` | `srcIp` | `exactly_one(wpl.srcIp)` -> "203.0.113.60" | `drop_and_review` | confirmed；单一源 IP |
| `roles.target.endpoint.ip/target_ip` | `transform` | `dstIp` | `exactly_one(wpl.dstIp)` -> "203.0.113.11" | `drop_and_review` | confirmed；单一目标 IP |
| `source_finding.attention.content` | `projection` | `attentionValue` | "攻击者 : 203.0.113.60  , 协议 : ssh  , 受害者 : 203.0.113.11" | `—` | confirmed；完整保留来源关注内容 |
| `facets.application.name` | `transform` | `attentionValue` | `lower(trim(parse_labeled_attention(wpl.attentionValue)['协议']))` -> "ssh" | `omit_and_review` | confirmed；来源明确标注协议 ssh；按应用层名称落位，不写入传输协议 |
| `source_finding.attacker.endpoint.ip` | `transform` | `attackerContent` | `exactly_one(wpl.attackerContent)` -> "203.0.113.60" | `drop_and_review` | confirmed；来源声明攻击方 |
| `source_finding.victim.endpoint.ip` | `transform` | `victimContent` | `exactly_one(wpl.victimContent)` -> "203.0.113.11" | `drop_and_review` | confirmed；来源声明受害方 |
| `source_finding.severity` | `projection` | `severity` | "高危" | `—` | confirmed；来源严重度 |
| `source_finding.confidence` | `projection` | `confidence` | "高" | `—` | confirmed；来源置信度 |
| `source_finding.category.original.name` | `projection` | `ruleCategoryName` | "其它类攻击利用" | `—` | confirmed；来源分类 |
| `source_alert_severity` | `transform` | `severity` | `string` -> "高危" | `—` | confirmed；保留来源 finding 原始严重度 |
| `severity` | `dictionary` | `severity` | "高危" -> "error" | `null_and_review` | partial；根据当前 NGSOC 样例分布推测的安全严重度交叉表，尚未经厂商确认 |
| `outcome` | `gap` | `data_gap.no_action_result` | "unknown" | `unknown` | missing；原始日志没有明确的底层动作结果字段或事件事实 |

### 5.3 编写约束

- 登录和绕过均为来源告警声明；attackResult 为空，不生成登录成功、失败或绕过成功事实。
- attentionValue 中 ssh 是应用层协议，映射到 facets.application.name，不写入传输层 network_protocol。
- 没有堡垒机地址、账户、认证方式、会话或端口，不构造对应实体和认证 facet。
