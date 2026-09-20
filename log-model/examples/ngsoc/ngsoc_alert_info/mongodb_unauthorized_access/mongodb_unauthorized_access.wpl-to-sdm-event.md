# WPL -> SDM Event 字段映射

> 样例：`mongodb_unauthorized_access.expected-sdm-event.behavior.json（现行）；旧 `*.expected-sdm-event.json` 为 55 列对照`；WPL 输出 67 个具名字段，机器可读文件记录完整逐字段处理结论。

## 核心字段

| WPL 来源 | SDM 落位 | 转换 | 说明 |
|---|---|---|---|
| `timestamp` | `occur_time` | WPL 已转换为毫秒时间戳 | 使用正文事件时间 |
| `seq` | `source_original_event_id`、`source_finding.original_id` | 直接赋值 | 来源告警序列 |
| `srcIp[0]` | `roles.source.endpoint.ip` | 直接赋值 | 通信起点 |
| `dstIp[0]`、`dport[0]` | `roles.target.endpoint` | 拆分并组合 IP/端口 | 通信终点 |
| `name`、`dport` | `roles.target.service.name` | 明确标题和 27017 共同归一为 `mongodb` | 不推断传输协议 |
| `sport` | `extensions.source_private.source_ports` | 数组字符串拆分为整数数组 | 聚合告警不投影单一源端口 |
| `name`、`ruleCategoryName` | `source_finding.title/category.original.name/behavior` | 行为归一为 `unauthorized_access` | 未授权是来源检测结论 |
| `attackResult` | `outcome`、`source_finding.attack_result` | `成功 -> success` | 来源明确声明成功 |
| `attackerContent/victimContent` | `source_finding.attacker/victim` | 使用设备明确声明 | 不与通信角色混用 |

## 派生字段

| 来源 | SDM 落位 | 说明 |
|---|---|---|
| `name/ruleCategoryName/dstIp/dport/relevantLogsType` | `record_kind/event_domain/event_type/operation` | 归一为 `finding/threat/network_connection/traffic` |
| `tenant_id + mapping_id + seq` | `event_id` | SHA-256 确定性事件 ID |

## 不落库原则

- 空字符串、空数组和仅供 NGSOC 展示的字段不单独落库，原值保留在独立 `raw_log` 原文表（`event_id` 回查）。
- 不根据“未授权访问”标题构造不存在的用户、认证会话或数据库资源。
- 不根据目标端口 27017 推断 TCP 等传输协议。

## 五、WPL/OML 编写规则

> WPL 只负责提取表中的 source 字段；Meta 和 Content 的赋值由 OML 按下表实现。
> `partial` 表示当前只有样例值或局部说明，不能视为完整厂商字典。

### 5.1 Meta 区

| SDM 字段 | 规则类型 | 输入/来源 | 赋值 | 未命中 | 状态与证据 |
|---|---|---|---|---|---|
| `event_id` | `derived` | `derived.sha256(tenant_id+'|'+mapping_id+'|'+wpl.seq)` | `derived.sha256(tenant_id+'|'+mapping_id+'|'+wpl.seq)` | `—` | confirmed；确定性事件 ID |
| `record_kind` | `conditional` | `when wpl.name == "MongoDB未授权访问" && wpl.ruleCategoryName == "非授权访问/权限绕过"` | `when wpl.name == "MongoDB未授权访问" && wpl.ruleCategoryName == "非授权访问/权限绕过" then chars(finding) else no_match` -> "finding" | `no_match` | confirmed；未授权访问保留为来源检测结论 |
| `event_domain` | `conditional` | `when wpl.name == "MongoDB未授权访问" && wpl.ruleCategoryName == "非授权访问/权限绕过"` | `when wpl.name == "MongoDB未授权访问" && wpl.ruleCategoryName == "非授权访问/权限绕过" then chars(threat) else no_match` -> "threat" | `no_match` | confirmed；仅该告警语义分支命中 |
| `event_type` | `conditional` | `when wpl.name == "MongoDB未授权访问" && exactly_one(parse_bracket_list(wpl.dport)) == "27017" && wpl.srcIp nonempty && wpl.dstIp nonempty` | `when wpl.name == "MongoDB未授权访问" && exactly_one(parse_bracket_list(wpl.dport)) == "27017" && wpl.srcIp nonempty && wpl.dstIp nonempty then chars(network_connection) else no_match` -> "network_connection" | `no_match` | confirmed；端点和 MongoDB 目标端口共同证明网络通信 |
| `operation` | `conditional` | `when wpl.name == "MongoDB未授权访问" && exactly_one(parse_bracket_list(wpl.dport)) == "27017" && wpl.srcIp nonempty && wpl.dstIp nonempty` | `when wpl.name == "MongoDB未授权访问" && exactly_one(parse_bracket_list(wpl.dport)) == "27017" && wpl.srcIp nonempty && wpl.dstIp nonempty then chars(traffic) else no_match` -> "traffic" | `no_match` | confirmed；与 event_type 使用同一条件 |
| `roles.target.service.name` | `conditional` | `when contains(wpl.name, "MongoDB") && exactly_one(parse_bracket_list(wpl.dport)) == "27017"` | `when contains(wpl.name, "MongoDB") && exactly_one(parse_bracket_list(wpl.dport)) == "27017" then chars(mongodb) else no_match` -> "mongodb" | `no_match` | confirmed；名称和标准端口同时成立才赋值 |
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
| `source_finding.title` | `projection` | `name` | "MongoDB未授权访问" | `—` | confirmed；来源告警名称 |
| `source_finding.severity` | `projection` | `severity` | "高危" | `—` | confirmed；保留来源严重度 |
| `roles.source.endpoint.ip` | `projection` | `srcIp` | ["192.0.2.140"] | `—` | confirmed；通信起点 |
| `roles.target.endpoint.ip` | `projection` | `dstIp` | ["198.51.100.213"] | `—` | confirmed；通信终点 |
| `source_finding.count` | `transform` | `times` | `to_int(wpl.times)` -> 170 | `drop_and_review` | confirmed；十进制字符串转整数，非法或负数不落库 |
| `source_finding.original_id` | `projection` | `seq` | "12932948" | `—` | confirmed；来源告警序列 |
| `source_finding.attacker.endpoint.ip` | `projection` | `attackerContent` | ["192.0.2.140"] | `—` | confirmed；NGSOC 攻击方声明 |
| `source_finding.rule.label` | `projection` | `relevantRuleName` | "预置-网络探针检测到权限绕过事件" | `—` | confirmed；来源关联规则 |
| `roles.target.endpoint.port/target_port` | `transform` | `dport` | `to_int(exactly_one(parse_bracket_list(wpl.dport)))` -> 27017 | `drop_and_review` | confirmed；解析括号列表，必须恰好一个合法端口 |
| `occur_time` | `projection` | `timestamp` | 1734451233000 | `—` | confirmed；正文事件时间；WPL 已转换为毫秒时间戳 |
| `source_finding.victim.endpoint.ip` | `projection` | `victimContent` | ["198.51.100.213"] | `—` | confirmed；NGSOC 受害方声明 |
| `source_finding.category.original.name` | `projection` | `ruleCategoryName` | "非授权访问/权限绕过" | `—` | confirmed；来源分类 |
| `extensions.source_private.source_ports` | `projection` | `sport` | "[56339, 52086, 52579, 33985, 60581, 50214, 49677, 37970, 37971, 54760]" | `—` | confirmed；聚合告警含多个源端口，不投影单一 source_port |
| `source_finding.confidence` | `projection` | `confidence` | "高" | `—` | confirmed；保留来源置信度 |
| `source_finding.killchain` | `dictionary` | `killchain` | "突防利用" -> "exploitation" | `preserve_in_extension_and_review` | partial；突防利用归一为 exploitation |
| `facets.network.direction` | `dictionary` | `commDirection` | "[内到内]" -> "L2L" | `preserve_in_extension_and_review` | partial；内到内归一为 L2L |
| `source_alert_severity` | `transform` | `severity` | `string` -> "高危" | `—` | confirmed；保留来源 finding 原始严重度 |
| `severity` | `dictionary` | `severity` | "高危" -> "error" | `null_and_review` | partial；根据当前 NGSOC 样例分布推测的安全严重度交叉表，尚未经厂商确认 |
| `source_finding.attack_result` | `dictionary` | `attackResult` | "成功" -> "success" | `preserve_in_extension_and_review` | partial；中文值明确声明成功 |
| `outcome` | `dictionary` | `attackResult` | "成功" -> "success" | `unknown_and_review` | partial；中文值明确声明成功 |

### 5.3 编写约束

- dictionary 仅包含当前样例或已有说明能够证明的值；不是完整厂商字典时标记为 partial。
- WPL 负责提取 source 字段，OML 按 kind 和 source 实现赋值。
- 未知枚举不得静默映射为正常业务值；按 unmatched 策略保留、忽略或进入待确认项。
- 现有 legacy adm.oml 的数字码字段不等同于本映射中的 SDM 语义枚举；实现时必须按本表转换并单独做兼容验证。
