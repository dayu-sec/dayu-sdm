# WPL → SDM Event 字段映射

> 样例：`ssid_test_protect.expected-sdm-event.json`；WPL 字段 36 个。

## 一、WPL 字段映射

| WPL 字段 | WPL 值 | SDM 落位 | expected 位置 | 说明 |
|---|---|---|---|---|
| `ssid_name` | "test" | `roles.target.resource.name/id` | `roles_obj.target.resource.name/id` | SSID 名称 |
| `protect_type` | 1 | `extensions.source_private.protect_type` | `extensions_obj.source_private.protect_type` | 保护类型 |
| `result` | 1 | `extensions.source_private.result` | `extensions_obj.source_private.result` | 管控结果 |
| `log_type` | 1 | `extensions.source_private.log_type` | `extensions_obj.source_private.log_type` | 日志类型 |
| `name` | "DESKTOP-3162Q7H" | `roles.source.host.name + source_host` | `roles_obj.source.host.name / source_host` | 承载终端 |
| `report_ip` | "198.51.100.63" | `roles.source.host.ip` | `roles_obj.source.host.ip` | 上报 IP |
| `mac` | null | `roles.source.host.mac` | `roles_obj.source.host.mac` | 归一化 |
| `client_id` | "8763344-22bf7c069ba34fd225ffbf178d46cbc | `profiles.endpoint_asset.agent.id` | `extensions_obj.profiles.endpoint_asset.agent.id` | 客户端 ID |
| `mid` | "f0322eabcfae08dd138fa7af42614ed25f03cfd | `profiles.endpoint_asset.agent.fingerprint_id` | `extensions_obj.profiles.endpoint_asset.agent.fingerprint_id` | 客户端指纹 |
| `node_name` | "testvbb" | `profiles.endpoint_asset.ownership.group.name` | `extensions_obj…` | 分组名 |
| `node_id` | "2701865912092360865" | `profiles.endpoint_asset.ownership.group.id` | `extensions_obj…` | 分组 ID |
| `oid` | "100103" | `profiles.endpoint_asset.ownership.organization.id` | `extensions_obj…` | 组织 OID |

## 二、非 WPL 来源（规则缺口，raw_log 补齐）

| 来源 | SDM 落位 | 值 | 说明 |
|---|---|---|---|
| `derived.entity_ref(resource, raw_log.ssid_name)` | `roles.target.ref_id` | "resource::test" | 三段式 |

## 三、未决问题

1. 06 枚举无 SSID/无线网络事件类型，暂用 generic_event；建议扩展
2. resource.type=ssid_network 待 registry 确认
3. log_type/protect_type 枚举已由 PDF §3.6.2 确认（protect_type 1=网卡防护/2=ssid管理；log_type 1=SSID连接）；result=1=放行 -> outcome=allowed
4. 原始日志无事件 ID，派生组合兜底

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
| `event_category` | `constant` | `constant` | "audit" | `—` | confirmed；无线网络管控活动，PDF §3.6.2 |
| `event_domain` | `constant` | `constant` | "network" | `—` | confirmed；见 README 决策 |
| `record_kind` | `constant` | `constant` | "activity" | `—` | confirmed；见 README 决策 |
| `outcome` | `constant` | `constant` | "allowed" | `—` | confirmed；PDF §3.6.2 result=1=放行 |
| `observer_vendor` | `constant` | `constant` | "qax" | `—` | confirmed；产品身份 |
| `observer_product` | `constant` | `constant` | "tianqing" | `—` | confirmed；产品身份 |
| `roles.target.ref_id` | `derived` | `derived.entity_ref(resource, raw_log.ssid_name)` | `derived.entity_ref(resource, raw_log.ssid_name)` | `—` | confirmed；三段式 |
| `log_id` | `context` | `platform_context.log_id` | `read(log_id)` | `—` | confirmed；expected 事件中的平台上下文字段 |
| `tenant_id` | `context` | `platform_context.tenant_id` | `read(tenant_id)` | `—` | confirmed；expected 事件中的平台上下文字段 |
| `ingest_time` | `context` | `platform_context.ingest_time` | `read(ingest_time)` | `—` | confirmed；expected 事件中的平台上下文字段 |
| `parse_time` | `context` | `platform_context.parse_time` | `read(parse_time)` | `—` | confirmed；expected 事件中的平台上下文字段 |
| `data_src_instance_id` | `context` | `platform_context.data_src_instance_id` | `read(data_src_instance_id)` | `—` | confirmed；expected 事件中的平台上下文字段 |
| `schema_version` | `constant` | `constant.schema_version` | 2 | `—` | confirmed；expected 事件确认的日志类型级常量 |
| `data_src_vendor` | `constant` | `constant.data_src_vendor` | "qax" | `—` | confirmed；expected 事件确认的日志类型级常量 |
| `mapping_id` | `constant` | `constant.mapping_id` | "qax.tianqing.edr_ssid_log" | `—` | confirmed；expected 事件确认的日志类型级常量 |
| `data_src_product` | `constant` | `constant.data_src_product` | "tianqing" | `—` | confirmed；expected 事件确认的日志类型级常量 |
| `log_type` | `constant` | `constant.log_type` | "edr_ssid_log" | `—` | confirmed；expected 事件确认的日志类型级常量 |
| `data_src_category` | `constant` | `constant.data_src_category` | "endpoint_security" | `—` | confirmed；expected 事件确认的日志类型级常量 |
| `log_name` | `constant` | `constant.log_name` | "天擎 SSID 无线日志" | `—` | confirmed；expected 事件确认的日志类型级常量 |
| `severity` | `constant` | `constant.log_semantics` | "info" | `—` | confirmed；当前日志类型的 expected 事件语义 |

### 5.2 Content 区

| SDM 字段 | 规则类型 | WPL 字段 | 映射/赋值 | 未命中 | 状态与证据 |
|---|---|---|---|---|---|
| `roles.target.resource.name/id` | `projection` | `ssid_name` | "test" | `—` | confirmed；SSID 名称 |
| `extensions.source_private.protect_type` | `projection` | `protect_type` | 1 | `—` | confirmed；保护类型 |
| `extensions.source_private.result` | `projection` | `result` | 1 | `—` | confirmed；管控结果 |
| `extensions.source_private.log_type` | `projection` | `log_type` | 1 | `—` | confirmed；日志类型 |
| `roles.source.host.name + source_host` | `projection` | `name` | "DESKTOP-3162Q7H" | `—` | confirmed；承载终端 |
| `roles.source.host.ip` | `projection` | `report_ip` | "198.51.100.63" | `—` | confirmed；上报 IP |
| `roles.source.host.mac` | `projection` | `mac` | `read(mac)` | `—` | confirmed；归一化 |
| `profiles.endpoint_asset.agent.id` | `projection` | `client_id` | "8763344-22bf7c069ba34fd225ffbf178d46cbcf" | `—` | confirmed；客户端 ID |
| `profiles.endpoint_asset.agent.fingerprint_id` | `projection` | `mid` | "f0322eabcfae08dd138fa7af42614ed25f03cfdbc0a0d65aeef0c0b575dc493e" | `—` | confirmed；客户端指纹 |
| `profiles.endpoint_asset.ownership.group.name` | `projection` | `node_name` | "testvbb" | `—` | confirmed；分组名 |
| `profiles.endpoint_asset.ownership.group.id` | `projection` | `node_id` | "2701865912092360865" | `—` | confirmed；分组 ID |
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
