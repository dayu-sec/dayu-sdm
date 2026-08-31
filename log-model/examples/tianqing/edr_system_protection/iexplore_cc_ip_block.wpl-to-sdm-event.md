# WPL → SDM Event 字段映射

> 样例：`iexplore_cc_ip_block.expected-sdm-event.json`；WPL 字段 33 个。

## 一、WPL 字段映射

| WPL 字段 | WPL 值 | SDM 落位 | expected 位置 | 说明 |
|---|---|---|---|---|
| `event_time` | 1617354719000 | `occur_time` | `occur_time` | 纳秒→毫秒 |
| `name` | "Test-shifang-Win7" | `roles.source.host.name + source_host` | `roles_obj.source.host.name / source_host` | 承载终端 |
| `report_ip` | "192.0.2.71" | `roles.source.host.ip` | `roles_obj.source.host.ip` | 上报 IP |
| `mac` | "00-50-56-80-C8-49" | `roles.source.host.mac` | `roles_obj.source.host.mac` | 归一化 |
| `client_id` | "8863058-d816e136fa1a79d971206d99b1a1418 | `profiles.endpoint_asset.agent.id` | `extensions_obj.profiles.endpoint_asset.agent.id` | 客户端 ID |
| `mid` | "09d24a99dfe6f5d9bbf3e79865aa2d02a66158d | `profiles.endpoint_asset.agent.fingerprint_id` | `extensions_obj.profiles.endpoint_asset.agent.fingerprint_id` | 客户端指纹 |
| `node_name` | "CRH" | `profiles.endpoint_asset.ownership.group.name` | `extensions_obj…` | 分组名 |
| `node_id` | "2713465372446557376" | `profiles.endpoint_asset.ownership.group.id` | `extensions_obj…` | 分组 ID |
| `oid` | "100103" | `profiles.endpoint_asset.ownership.organization.id` | `extensions_obj…` | 组织 OID |

## 二、非 WPL 来源（规则缺口，raw_log 补齐）

| 来源 | SDM 落位 | 值 | 说明 |
|---|---|---|---|
| `data_gap.raw_log.subject_process` | `roles.source.process.name/path` | "iexplore.exe / C:\\Program Files\\Internet Explor | 原始日志存在但 WPL 未抽 |
| `data_gap.raw_log.object` | `roles.target.endpoint.ip` | "198.51.100.67" | 原始日志存在但 WPL 未抽 |
| `data_gap.raw_log.risk_detail` | `source_finding.title` | "拦截风险 IP 访问（DriveTheLife CC）" | 原始日志存在但 WPL 未抽 |
| `derived.entity_ref(process, raw_log.subject_process)` | `roles.source.ref_id` | "process::iexplore.exe" | 三段式 |
| `derived.entity_ref(endpoint, raw_log.object)` | `roles.target.ref_id` | "endpoint::198.51.100.67" | 三段式 |

## 三、未决问题

1. 06 枚举无系统防护事件类型，暂用 generic_event；建议扩展
2. action（21）/defend_action（1）/trigger_mode（5）枚举待确认
3. 原始日志无事件 ID，派生组合兜底

## 五、WPL/OML 编写规则

> WPL 只负责提取表中的 source 字段；Meta 和 Content 的赋值由 OML 按下表实现。
> `partial` 表示当前只有样例值或局部说明，不能视为完整厂商字典。

### 5.1 Meta 区

| SDM 字段 | 规则类型 | 输入/来源 | 赋值 | 未命中 | 状态与证据 |
|---|---|---|---|---|---|
| `event_id` | `derived` | `derived.sha256(tenant_id=''|mapping_id|source_original_event_id)` | `derived.sha256(tenant_id=''|mapping_id|source_original_event_id)` | `—` | confirmed；无 uuid，派生组合兜底（见 wpl-missing-fields） |
| `extensions.profiles.endpoint_asset.subject_ref.ref_id` | `derived` | `derived.entity_ref(host, platform_context.asset_id)` | `derived.entity_ref(host, platform_context.asset_id)` | `—` | confirmed；受管资产 |
| `roles.source.host.id(profiles.subject_ref)` | `context` | `platform_context.asset_id` | `platform_context.asset_id` | `—` | confirmed；缺口补齐 |
| `event_type` | `constant` | `constant` | "generic_event" | `—` | confirmed；见 README 决策 |
| `event_category` | `constant` | `constant` | "alert" | `—` | confirmed；系统防护检测告警，PDF §3.2.4 |
| `event_domain` | `constant` | `constant` | "threat" | `—` | confirmed；见 README 决策 |
| `record_kind` | `constant` | `constant` | "finding" | `—` | confirmed；见 README 决策 |
| `outcome` | `constant` | `constant` | "denied" | `—` | confirmed；见 README 决策 |
| `observer_vendor` | `constant` | `constant` | "qax" | `—` | confirmed；产品身份 |
| `observer_product` | `constant` | `constant` | "tianqing" | `—` | confirmed；产品身份 |
| `roles.source.ref_id` | `derived` | `derived.entity_ref(process, raw_log.subject_process)` | `derived.entity_ref(process, raw_log.subject_process)` | `—` | confirmed；三段式 |
| `roles.target.ref_id` | `derived` | `derived.entity_ref(endpoint, raw_log.object)` | `derived.entity_ref(endpoint, raw_log.object)` | `—` | confirmed；三段式 |
| `log_id` | `context` | `platform_context.log_id` | `read(log_id)` | `—` | confirmed；expected 事件中的平台上下文字段 |
| `tenant_id` | `context` | `platform_context.tenant_id` | `read(tenant_id)` | `—` | confirmed；expected 事件中的平台上下文字段 |
| `ingest_time` | `context` | `platform_context.ingest_time` | `read(ingest_time)` | `—` | confirmed；expected 事件中的平台上下文字段 |
| `parse_time` | `context` | `platform_context.parse_time` | `read(parse_time)` | `—` | confirmed；expected 事件中的平台上下文字段 |
| `data_src_instance_id` | `context` | `platform_context.data_src_instance_id` | `read(data_src_instance_id)` | `—` | confirmed；expected 事件中的平台上下文字段 |
| `schema_version` | `constant` | `constant.schema_version` | 2 | `—` | confirmed；expected 事件确认的日志类型级常量 |
| `data_src_vendor` | `constant` | `constant.data_src_vendor` | "qax" | `—` | confirmed；expected 事件确认的日志类型级常量 |
| `mapping_id` | `constant` | `constant.mapping_id` | "qax.tianqing.edr_system_protection" | `—` | confirmed；expected 事件确认的日志类型级常量 |
| `data_src_product` | `constant` | `constant.data_src_product` | "tianqing" | `—` | confirmed；expected 事件确认的日志类型级常量 |
| `log_type` | `constant` | `constant.log_type` | "edr_system_protection" | `—` | confirmed；expected 事件确认的日志类型级常量 |
| `data_src_category` | `constant` | `constant.data_src_category` | "endpoint_security" | `—` | confirmed；expected 事件确认的日志类型级常量 |
| `log_name` | `constant` | `constant.log_name` | "天擎系统防护日志" | `—` | confirmed；expected 事件确认的日志类型级常量 |
| `severity` | `constant` | `constant.log_semantics` | "info" | `—` | confirmed；当前日志类型的 expected 事件语义 |

### 5.2 Content 区

| SDM 字段 | 规则类型 | WPL 字段 | 映射/赋值 | 未命中 | 状态与证据 |
|---|---|---|---|---|---|
| `roles.source.process.name/path` | `gap` | `data_gap.raw_log.subject_process` | `data_gap.raw_log.subject_process` | `—` | missing；规则未抽 |
| `roles.target.endpoint.ip` | `gap` | `data_gap.raw_log.object` | `data_gap.raw_log.object` | `—` | missing；规则未抽 |
| `source_finding.title` | `gap` | `data_gap.raw_log.risk_detail` | `data_gap.raw_log.risk_detail` | `—` | missing；规则未抽 |
| `occur_time` | `projection` | `event_time` | 1617354719000 | `—` | confirmed；纳秒→毫秒 |
| `roles.source.host.name + source_host` | `projection` | `name` | "Test-shifang-Win7" | `—` | confirmed；承载终端 |
| `roles.source.host.ip` | `projection` | `report_ip` | "192.0.2.71" | `—` | confirmed；上报 IP |
| `roles.source.host.mac` | `projection` | `mac` | "00-50-56-80-C8-49" | `—` | confirmed；归一化 |
| `profiles.endpoint_asset.agent.id` | `projection` | `client_id` | "8863058-d816e136fa1a79d971206d99b1a1418f" | `—` | confirmed；客户端 ID |
| `profiles.endpoint_asset.agent.fingerprint_id` | `projection` | `mid` | "09d24a99dfe6f5d9bbf3e79865aa2d02a66158d59c1657d55a496cf15786df61" | `—` | confirmed；客户端指纹 |
| `profiles.endpoint_asset.ownership.group.name` | `projection` | `node_name` | "CRH" | `—` | confirmed；分组名 |
| `profiles.endpoint_asset.ownership.group.id` | `projection` | `node_id` | "2713465372446557376" | `—` | confirmed；分组 ID |
| `profiles.endpoint_asset.ownership.organization.id` | `projection` | `oid` | "100103" | `—` | confirmed；组织 OID |

### 5.3 编写约束

- dictionary 仅包含当前样例或已有说明能够证明的值；不是完整厂商字典时标记为 partial。
- WPL 负责提取 source 字段，OML 按 kind 和 source 实现赋值。
- 未知枚举不得静默映射为正常业务值；按 unmatched 策略保留、忽略或进入待确认项。

## 当前物理注册表迁移

- expected 已按当前 `sdm_event.yaml` 87 字段注册表收敛。
- 原始日志保存在同名 `raw-log.json`，expected 与 raw_log 的关联统一用 `event_id`（`raw_log_id` 已于 2026-08-26 退役）。
- `network_protocol/network_direction` 已迁移为 `carrier_protocol/carrier_direction`。
- 旧扁平 finding 热字段迁移为 `source_alert_*`；完整检测声明继续保存在 `source_finding_obj`。
- `schema_version/mapping_id/record_kind/event_domain` 不再作为当前 expected 顶层物理字段。
