# WPL → SDM Event 字段映射

> 样例：`check_item_disabled.expected-sdm-event.json`；WPL 字段 36 个。

## 一、WPL 字段映射

| WPL 字段 | WPL 值 | SDM 落位 | expected 位置 | 说明 |
|---|---|---|---|---|
| `task` | "{9546E589-97EA-42FF-BCDD-6FD76A1C7D9B}" | `source_original_event_id` | `source_original_event_id` | 去花括号 |
| `result` | 0 | `extensions.source_private.result` | `extensions_obj.source_private.result` | PDF §3.4.2 不通过；不进 outcome/finding.status |
| `score` | 1 | `extensions.source_private.score` | `extensions_obj.source_private.score` | 检查项评分 |
| `name` | "A003076-PC01" | `roles.target.host.name + source_host` | `roles_obj.target.host.name / source_host` | 被检查终端；source_host 为热字段投影 |
| `report_ip` | "198.51.100.114" | `roles.target.host.ip` | `roles_obj.target.host.ip` | 被检查终端上报 IP |
| `mac` | "4C-CC-6A-E9-D6-3D" | `roles.target.host.mac` | `roles_obj.target.host.mac` | 归一化 |
| `client_id` | "0500428-c2d3492c62cff604846b34c4f648c3c | `profiles.endpoint_asset.agent.id` | `extensions_obj.profiles.endpoint_asset.agent.id` | 客户端 ID |
| `mid` | "c735212406352838244575b95f07f07f5fc5d41 | `profiles.endpoint_asset.agent.fingerprint_id` | `extensions_obj.profiles.endpoint_asset.agent.fingerprint_id` | 客户端指纹 |
| `node_name` | "创新BG" | `profiles.endpoint_asset.ownership.group.name` | `extensions_obj…` | 分组名 |
| `node_id` | "z_2727659524106813897" | `profiles.endpoint_asset.ownership.group.id` | `extensions_obj…` | 分组 ID |
| `oid` | "100231" | `profiles.endpoint_asset.ownership.organization.id` | `extensions_obj…` | 组织 OID |

## 二、非 WPL 来源（规则缺口，raw_log 补齐）

| 来源 | SDM 落位 | 值 | 说明 |
|---|---|---|---|
| `data_gap.raw_log.scope/check_std/reject/user_name/user_real_name` | `extensions.source_private.*` | "9005/已禁用/0/qinxin/秦鑫" | 原始日志存在但 WPL 未抽 |

## 三、未决问题

1. 06 枚举无基线检查项类型，保持 generic_event
2. 检查项 `name=1015` 业务名未见
3. 用户 qinxin 是否为检查执行人未确认

## 五、WPL/OML 编写规则

> WPL 只负责提取表中的 source 字段；Meta 和 Content 的赋值由 OML 按下表实现。
> `partial` 表示当前只有样例值或局部说明，不能视为完整厂商字典。

### 5.1 Meta 区

| SDM 字段 | 规则类型 | 输入/来源 | 赋值 | 未命中 | 状态与证据 |
|---|---|---|---|---|---|
| `event_id` | `derived` | `derived.sha256(tenant_id=''|mapping_id|source_original_event_id)` | `derived.sha256(tenant_id=''|mapping_id|source_original_event_id)` | `—` | confirmed；无 uuid，派生组合兜底（见 wpl-missing-fields） |
| `extensions.profiles.endpoint_asset.subject_ref.ref_id` | `derived` | `derived.entity_ref(host, platform_context.asset_id)` | `derived.entity_ref(host, platform_context.asset_id)` | `—` | confirmed；受管资产 |
| `roles.target.host.id(profiles.subject_ref)` | `context` | `platform_context.asset_id` | `platform_context.asset_id` | `—` | confirmed；缺口补齐 |
| `event_type` | `constant` | `constant` | "generic_event" | `—` | confirmed；06 无基线检查项类型 |
| `event_category` | `constant` | `constant` | "system" | `—` | confirmed；系统配置核查项 |
| `event_domain` | `constant` | `constant` | "system" | `—` | confirmed；见 README 决策 |
| `record_kind` | `constant` | `constant` | "finding" | `—` | confirmed；见 README 决策 |
| `outcome` | `constant` | `constant` | "observed" | `—` | confirmed；见 README 决策 |
| `observer_vendor` | `constant` | `constant` | "qax" | `—` | confirmed；产品身份 |
| `observer_product` | `constant` | `constant` | "tianqing" | `—` | confirmed；产品身份 |
| `log_id` | `context` | `platform_context.log_id` | `read(log_id)` | `—` | confirmed；expected 事件中的平台上下文字段 |
| `tenant_id` | `context` | `platform_context.tenant_id` | `read(tenant_id)` | `—` | confirmed；expected 事件中的平台上下文字段 |
| `ingest_time` | `context` | `platform_context.ingest_time` | `read(ingest_time)` | `—` | confirmed；expected 事件中的平台上下文字段 |
| `parse_time` | `context` | `platform_context.parse_time` | `read(parse_time)` | `—` | confirmed；expected 事件中的平台上下文字段 |
| `data_src_instance_id` | `context` | `platform_context.data_src_instance_id` | `read(data_src_instance_id)` | `—` | confirmed；expected 事件中的平台上下文字段 |
| `schema_version` | `constant` | `constant.schema_version` | 2 | `—` | confirmed；expected 事件确认的日志类型级常量 |
| `data_src_vendor` | `constant` | `constant.data_src_vendor` | "qax" | `—` | confirmed；expected 事件确认的日志类型级常量 |
| `mapping_id` | `constant` | `constant.mapping_id` | "qax.tianqing.edr_baseline_check_detail" | `—` | confirmed；expected 事件确认的日志类型级常量 |
| `data_src_product` | `constant` | `constant.data_src_product` | "tianqing" | `—` | confirmed；expected 事件确认的日志类型级常量 |
| `log_type` | `constant` | `constant.log_type` | "edr_baseline_check_detail" | `—` | confirmed；expected 事件确认的日志类型级常量 |
| `data_src_category` | `constant` | `constant.data_src_category` | "endpoint_security" | `—` | confirmed；expected 事件确认的日志类型级常量 |
| `log_name` | `constant` | `constant.log_name` | "天擎基线检查详情日志" | `—` | confirmed；expected 事件确认的日志类型级常量 |
| `severity` | `constant` | `constant.log_semantics` | "info" | `—` | confirmed；当前日志类型的 expected 事件语义 |

### 5.2 Content 区

| SDM 字段 | 规则类型 | WPL 字段 | 映射/赋值 | 未命中 | 状态与证据 |
|---|---|---|---|---|---|
| `extensions.source_private.*` | `gap` | `data_gap.raw_log.scope/check_std/reject/user_name/user_real_name` | `data_gap.raw_log.scope/check_std/reject/user_name/user_real_name` | `—` | missing；规则未抽 |
| `source_original_event_id` | `projection` | `task` | "{9546E589-97EA-42FF-BCDD-6FD76A1C7D9B}" | `—` | confirmed；去花括号 |
| `extensions.source_private.result` | `projection` | `result` | 0 | `—` | confirmed；结果枚举 |
| `extensions.source_private.score` | `projection` | `score` | 1 | `—` | confirmed；检查项评分 |
| `roles.target.host.name + source_host` | `projection` | `name` | "A003076-PC01" | `—` | confirmed；承载终端 |
| `roles.target.host.ip` | `projection` | `report_ip` | "198.51.100.114" | `—` | confirmed；上报 IP |
| `roles.target.host.mac` | `projection` | `mac` | "4C-CC-6A-E9-D6-3D" | `—` | confirmed；归一化 |
| `profiles.endpoint_asset.agent.id` | `projection` | `client_id` | "0500428-c2d3492c62cff604846b34c4f648c3c9" | `—` | confirmed；客户端 ID |
| `profiles.endpoint_asset.agent.fingerprint_id` | `projection` | `mid` | "c735212406352838244575b95f07f07f5fc5d4127d55862a8ee13ec46a049442" | `—` | confirmed；客户端指纹 |
| `profiles.endpoint_asset.ownership.group.name` | `projection` | `node_name` | "创新BG" | `—` | confirmed；分组名 |
| `profiles.endpoint_asset.ownership.group.id` | `projection` | `node_id` | "z_2727659524106813897" | `—` | confirmed；分组 ID |
| `profiles.endpoint_asset.ownership.organization.id` | `projection` | `oid` | "100231" | `—` | confirmed；组织 OID |

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
