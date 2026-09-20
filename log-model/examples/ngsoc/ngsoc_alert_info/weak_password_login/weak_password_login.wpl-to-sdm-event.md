# WPL -> SDM Event 字段映射

> 样例：`weak_password_login.expected-sdm-event.behavior.json（现行）；旧 `*.expected-sdm-event.json` 为 55 列对照`；WPL 输出 18 个命名字段。

## 字段映射

| WPL 来源 | SDM 落位 | 转换 | 说明 |
|---|---|---|---|
| `timestamp` | `occur_time` | `2024-11-29 09:17:13` 转毫秒 | 使用正文业务时间 |
| `update_time` | `extensions.source_private.wpl_update_time` | 保留 WPL 值 | Syslog 头无年份，不能作为业务时间 |
| `name` | `source_finding.title` | 直接赋值 | 弱口令登录 |
| `ruleCategoryName` | `source_finding.category.original.name` | 直接赋值 | 弱口令 |
| `srcIp[0]` | `roles.source.endpoint.ip`、`source_ip` | 直接赋值 | 通信起点 |
| `dstIp[0]` | `roles.target.endpoint.ip`、`target_ip` | 直接赋值 | 通信终点 |
| `domain` | `roles.target.endpoint.port`、`target_port` | 从 `198.51.100.30:28080` 提取端口 | 该字段不是域名 |
| `attackerContent[0]` | `source_finding.attacker.endpoint.ip` | 直接赋值 | 来源检测主张攻击方 |
| `victimContent[0]` | `source_finding.victim.endpoint.ip` | 直接赋值 | 来源检测主张受害方 |
| `attentionValue` | `source_finding.attention.content` | 直接赋值 | 关注目标 IP |
| `severity` | `source_finding.severity` | 保留中危 | 不映射到 event.severity |
| `confidence` | `source_finding.confidence` | 保留高 | 来源置信度 |
| `attackResult` | `outcome`、`source_finding.attack_result`、`facets.authentication.auth_result` | 成功 -> success | 登录结果明确 |
| `compromiseState/killchain/ioc/url` | 不落库 | 空值或空数组 | 原始载荷保留在独立 raw_log 原文表（event_id 回查） |

## 派生字段

| 来源 | SDM 落位 | 说明 |
|---|---|---|
| `timestamp + name + srcIp + dstIp` | `source_original_event_id` | 原始日志没有 UUID 时的稳定组合 |
| `sha256(tenant_id + mapping_id + source_original_event_id)` | `event_id` | 确定性事件 ID |
| `raw_syslog.header` | `extensions.source_private.syslog_*` | 保留 priority、host 和无年份头时间 |

完整的逐字段机器映射见 `weak_password_login.wpl-to-sdm-event.json`。

## 五、WPL/OML 编写规则

> WPL 只负责提取表中的 source 字段；Meta 和 Content 的赋值由 OML 按下表实现。
> `partial` 表示当前只有样例值或局部说明，不能视为完整厂商字典。

### 5.1 Meta 区

| SDM 字段 | 规则类型 | 输入/来源 | 赋值 | 未命中 | 状态与证据 |
|---|---|---|---|---|---|
| `source_original_event_id/source_finding.original_id` | `derived` | `derived.source_original_event_id(wpl.timestamp,wpl.name,wpl.srcIp,wpl.dstIp)` | `derived.source_original_event_id(wpl.timestamp,wpl.name,wpl.srcIp,wpl.dstIp)` | `—` | confirmed；原始日志没有 uuid/seq |
| `event_id` | `derived` | `derived.sha256(tenant_id=""|mapping_id|source_original_event_id)` | `derived.sha256(tenant_id=""|mapping_id|source_original_event_id)` | `—` | confirmed；确定性事件 ID |
| `record_kind` | `constant` | `constant` | "finding" | `—` | confirmed；弱口令成功登录检测 |
| `event_domain` | `conditional` | `when wpl.name == "弱口令登录" && wpl.ruleCategoryName == "弱口令"` | `when wpl.name == "弱口令登录" && wpl.ruleCategoryName == "弱口令" then chars(identity) else no_match` -> "identity" | `no_match` | confirmed；仅弱口令登录告警命中，不能作为 ngsoc_alert_info 全局常量 |
| `event_type` | `conditional` | `when wpl.name == "弱口令登录" && wpl.ruleCategoryName == "弱口令"` | `when wpl.name == "弱口令登录" && wpl.ruleCategoryName == "弱口令" then chars(user_login) else no_match` -> "user_login" | `no_match` | confirmed；仅弱口令登录告警命中，其他告警进入各自语义分支 |
| `extensions.source_private.syslog_*` | `derived` | `raw_syslog.header` | `raw_syslog.header` | `—` | confirmed；保留接入头信息，不作为业务发生时间 |
| `parse_time` | `context` | `platform_context.parse_time` | `read(parse_time)` | `—` | confirmed；expected 事件中的平台上下文字段 |
| `data_src_instance_id` | `context` | `platform_context.data_src_instance_id` | `read(data_src_instance_id)` | `—` | confirmed；expected 事件中的平台上下文字段 |
| `tenant_id` | `context` | `platform_context.tenant_id` | `read(tenant_id)` | `—` | confirmed；expected 事件中的平台上下文字段 |
| `log_id` | `context` | `platform_context.log_id` | `read(log_id)` | `—` | confirmed；expected 事件中的平台上下文字段 |
| `ingest_time` | `context` | `platform_context.ingest_time` | `read(ingest_time)` | `—` | confirmed；expected 事件中的平台上下文字段 |
| `data_src_product` | `constant` | `constant.data_src_product` | "ngsoc" | `—` | confirmed；expected 事件确认的日志类型级常量 |
| `log_type` | `constant` | `constant.log_type` | "ngsoc_alert_info" | `—` | confirmed；expected 事件确认的日志类型级常量 |
| `data_src_vendor` | `constant` | `constant.data_src_vendor` | "qax" | `—` | confirmed；expected 事件确认的日志类型级常量 |
| `mapping_id` | `constant` | `constant.mapping_id` | "qax.ngsoc.ngsoc_alert_info" | `—` | confirmed；expected 事件确认的日志类型级常量 |
| `schema_version` | `constant` | `constant.schema_version` | 2 | `—` | confirmed；expected 事件确认的日志类型级常量 |
| `observer_product` | `constant` | `constant.observer_product` | "ngsoc" | `—` | confirmed；expected 事件确认的日志类型级常量 |
| `observer_vendor` | `constant` | `constant.observer_vendor` | "qax" | `—` | confirmed；expected 事件确认的日志类型级常量 |
| `log_name` | `constant` | `constant.log_name` | "NGSOC告警信息" | `—` | confirmed；expected 事件确认的日志类型级常量 |
| `data_src_category` | `constant` | `constant.data_src_category` | "security_analytics" | `—` | confirmed；expected 事件确认的日志类型级常量 |
| `log_level` | `dictionary` | `derived.syslog_severity_code(raw_syslog.header.priority)` | 0 -> "emerg", 1 -> "alert", 2 -> "crit", 3 -> "error", 4 -> "warning", 5 -> "notice", 6 -> "info", 7 -> "debug" | `null_and_review` | confirmed；Syslog PRI 的低 3 位表示来源日志等级，不是 finding 安全严重度 |

### 5.2 Content 区

| SDM 字段 | 规则类型 | WPL 字段 | 映射/赋值 | 未命中 | 状态与证据 |
|---|---|---|---|---|---|
| `extensions.source_private.wpl_update_time` | `projection` | `update_time` | "2026-11-29 09:17:20" | `—` | confirmed；Syslog 头无年份，WPL 推断成 2026，不参与事件时间 |
| `source_finding.title` | `projection` | `name` | "弱口令登录" | `—` | confirmed；来源告警标题 |
| `occur_time` | `projection` | `timestamp` | 1732843033000 | `—` | confirmed；正文时间转毫秒；优先于无年份 Syslog 头时间 |
| `source_finding.category.original.name` | `projection` | `ruleCategoryName` | "弱口令" | `—` | confirmed；来源告警分类 |
| `roles.source.endpoint.ip/source_finding.attacker.endpoint.ip/source_ip` | `projection` | `srcIp` | ["192.0.2.28"] | `—` | confirmed；通信起点与检测主张攻击方一致 |
| `roles.target.endpoint.ip/source_finding.victim.endpoint.ip/target_ip` | `projection` | `dstIp` | ["198.51.100.30"] | `—` | confirmed；通信终点与检测主张受害方一致 |
| `source_finding.attention.content` | `projection` | `attentionValue` | "目的IP : 198.51.100.30" | `—` | confirmed；关注内容 |
| `source_finding.severity` | `projection` | `severity` | "中危" | `—` | confirmed；保留中危 |
| `source_finding.confidence` | `projection` | `confidence` | "高" | `—` | confirmed；保留高 |
| `roles.target.endpoint.port/target_port` | `transform` | `domain` | `to_int(port(exactly_one(parse_json_array(wpl.domain))))` -> 28080 | `drop_and_review` | confirmed；解析单元素 JSON 数组和 IP:port，校验 IP 与 wpl.dstIp 一致后提取端口；不构造 domain |
| `source_finding.attacker.endpoint.ip` | `projection` | `attackerContent` | ["192.0.2.28"] | `—` | confirmed；NGSOC 检测主张攻击方 |
| `source_finding.victim.endpoint.ip` | `projection` | `victimContent` | ["198.51.100.30"] | `—` | confirmed；NGSOC 检测主张受害方 |
| `source_alert_severity` | `transform` | `severity` | `string` -> "中危" | `—` | confirmed；保留来源 finding 原始严重度 |
| `severity` | `dictionary` | `severity` | "中危" -> "warning" | `null_and_review` | partial；根据当前 NGSOC 样例分布推测的安全严重度交叉表，尚未经厂商确认 |
| `source_finding.attack_result` | `dictionary` | `attackResult` | "成功" -> "success" | `preserve_in_extension_and_review` | partial；中文值明确声明成功 |
| `outcome` | `dictionary` | `attackResult` | "成功" -> "success" | `unknown_and_review` | partial；中文值明确声明成功 |

### 5.3 编写约束

- dictionary 仅包含当前样例或已有说明能够证明的值；不是完整厂商字典时标记为 partial。
- WPL 负责提取 source 字段，OML 按 kind 和 source 实现赋值。
- 未知枚举不得静默映射为正常业务值；按 unmatched 策略保留、忽略或进入待确认项。
- 现有 legacy adm.oml 的数字码字段不等同于本映射中的 SDM 语义枚举；实现时必须按本表转换并单独做兼容验证。
