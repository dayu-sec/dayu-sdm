# WPL → SDM Event 字段映射

> 样例：`mirrordriver_transfer.expected-sdm-event.json`；WPL 字段 38 个。

## 一、WPL 字段映射

| WPL 字段 | WPL 值 | SDM 落位 | expected 位置 | 说明 |
|---|---|---|---|---|
| `params_id` | "4e3be01ab600001f00100000" | `source_original_event_id` | `source_original_event_id` | 会话参数 ID |
| `file_transfer_direction` | 1 | `extensions.source_private.file_transfer_direction` | `extensions_obj.source_private.file_transfer_direction` | 传输方向 |
| `file_transfer_result` | 1 | `extensions.source_private.file_transfer_result` | `extensions_obj.source_private.file_transfer_result` | 传输结果 |
| `name` | "WIN-EX01" | `roles.related.host.name + source_host` | `roles_obj.related[].host.name / source_host` | 传输会话关联终端；source_host 为热字段投影 |
| `report_ip` | "192.0.2.192" | `roles.related.host.ip` | `roles_obj.related[].host.ip` | 关联终端上报 IP |
| `mac` | "00-00-5E-00-53-A7" | `roles.related.host.mac` | `roles_obj.related[].host.mac` | 归一化 |
| `client_id` | "8424338-de7f6819c3625af3402bd64422d1400 | `profiles.endpoint_asset.agent.id` | `extensions_obj.profiles.endpoint_asset.agent.id` | 客户端 ID |
| `mid` | "1909aacaa9d3411b9237145b0bada7ee" | `profiles.endpoint_asset.agent.fingerprint_id` | `extensions_obj.profiles.endpoint_asset.agent.fingerprint_id` | 客户端指纹 |
| `node_name` | "hy" | `profiles.endpoint_asset.ownership.group.name` | `extensions_obj…` | 分组名 |
| `node_id` | "2814380010620583951" | `profiles.endpoint_asset.ownership.group.id` | `extensions_obj…` | 分组 ID |
| `oid` | "2811278348364284476" | `profiles.endpoint_asset.ownership.organization.id` | `extensions_obj…` | 组织 OID |

## 二、非 WPL 来源（规则缺口，raw_log 补齐）

| 来源 | SDM 落位 | 值 | 说明 |
|---|---|---|---|
| `data_gap.raw_log.admin_name` | `roles.source.user.name` | "admin" | 原始日志存在但 WPL 未抽 |
| `data_gap.raw_log.file_name/file_size` | `roles.target.file.name/size` | "MirrorDriver.7z / 348857" | 原始日志存在但 WPL 未抽 |
| `derived.entity_ref(user, raw_log.admin_name)` | `roles.source.ref_id` | "user::admin" | 三段式 |
| `derived.entity_ref(file, raw_log.file_name)` | `roles.target.ref_id` | "file::MirrorDriver.7z" | 三段式 |

## 三、未决问题

1. file_transfer_direction/file_transfer_result 枚举待确认（1=成功?）
2. file_copy 的 operation 枚举与传输方向映射待确认
3. 原始日志无事件 ID，params_id 兜底

## 五、WPL/OML 编写规则

> WPL 只负责提取表中的 source 字段；Meta 和 Content 的赋值由 OML 按下表实现。
> `partial` 表示当前只有样例值或局部说明，不能视为完整厂商字典。

### 5.1 Meta 区

| SDM 字段 | 规则类型 | 输入/来源 | 赋值 | 未命中 | 状态与证据 |
|---|---|---|---|---|---|
| `event_id` | `derived` | `derived.sha256(tenant_id=''|mapping_id|source_original_event_id)` | `derived.sha256(tenant_id=''|mapping_id|source_original_event_id)` | `—` | confirmed；无 uuid，派生组合兜底（见 wpl-missing-fields） |
| `extensions.profiles.endpoint_asset.subject_ref.ref_id` | `derived` | `derived.entity_ref(host, platform_context.asset_id)` | `derived.entity_ref(host, platform_context.asset_id)` | `—` | confirmed；受管资产 |
| `roles.related.host.id(profiles.subject_ref)` | `context` | `platform_context.asset_id` | `platform_context.asset_id` | `—` | confirmed；缺口补齐 |
| `event_type` | `constant` | `constant` | "file_copy" | `—` | confirmed；见 README 决策 |
| `event_category` | `constant` | `constant` | "audit" | `—` | confirmed；远程协助文件传输，PDF §3.6.7 |
| `event_domain` | `constant` | `constant` | "endpoint" | `—` | confirmed；见 README 决策 |
| `record_kind` | `constant` | `constant` | "activity" | `—` | confirmed；见 README 决策 |
| `outcome` | `constant` | `constant` | "observed" | `—` | confirmed；见 README 决策 |
| `observer_vendor` | `constant` | `constant` | "qax" | `—` | confirmed；产品身份 |
| `observer_product` | `constant` | `constant` | "tianqing" | `—` | confirmed；产品身份 |
| `roles.source.ref_id` | `derived` | `derived.entity_ref(user, raw_log.admin_name)` | `derived.entity_ref(user, raw_log.admin_name)` | `—` | confirmed；三段式 |
| `roles.target.ref_id` | `derived` | `derived.entity_ref(file, raw_log.file_name)` | `derived.entity_ref(file, raw_log.file_name)` | `—` | confirmed；三段式 |
| `log_id` | `context` | `platform_context.log_id` | `read(log_id)` | `—` | confirmed；expected 事件中的平台上下文字段 |
| `tenant_id` | `context` | `platform_context.tenant_id` | `read(tenant_id)` | `—` | confirmed；expected 事件中的平台上下文字段 |
| `ingest_time` | `context` | `platform_context.ingest_time` | `read(ingest_time)` | `—` | confirmed；expected 事件中的平台上下文字段 |
| `parse_time` | `context` | `platform_context.parse_time` | `read(parse_time)` | `—` | confirmed；expected 事件中的平台上下文字段 |
| `data_src_instance_id` | `context` | `platform_context.data_src_instance_id` | `read(data_src_instance_id)` | `—` | confirmed；expected 事件中的平台上下文字段 |
| `schema_version` | `constant` | `constant.schema_version` | 2 | `—` | confirmed；expected 事件确认的日志类型级常量 |
| `data_src_vendor` | `constant` | `constant.data_src_vendor` | "qax" | `—` | confirmed；expected 事件确认的日志类型级常量 |
| `mapping_id` | `constant` | `constant.mapping_id` | "qax.tianqing.edr_remote_assistance_file_transfer" | `—` | confirmed；expected 事件确认的日志类型级常量 |
| `data_src_product` | `constant` | `constant.data_src_product` | "tianqing" | `—` | confirmed；expected 事件确认的日志类型级常量 |
| `log_type` | `constant` | `constant.log_type` | "edr_remote_assistance_file_transfer" | `—` | confirmed；expected 事件确认的日志类型级常量 |
| `data_src_category` | `constant` | `constant.data_src_category` | "endpoint_security" | `—` | confirmed；expected 事件确认的日志类型级常量 |
| `log_name` | `constant` | `constant.log_name` | "天擎远程协助文件传输日志" | `—` | confirmed；expected 事件确认的日志类型级常量 |
| `severity` | `constant` | `constant.log_semantics` | "info" | `—` | confirmed；当前日志类型的 expected 事件语义 |

### 5.2 Content 区

| SDM 字段 | 规则类型 | WPL 字段 | 映射/赋值 | 未命中 | 状态与证据 |
|---|---|---|---|---|---|
| `roles.source.user.name` | `gap` | `data_gap.raw_log.admin_name` | `data_gap.raw_log.admin_name` | `—` | missing；规则未抽 |
| `roles.target.file.name/size` | `gap` | `data_gap.raw_log.file_name/file_size` | `data_gap.raw_log.file_name/file_size` | `—` | missing；规则未抽 |
| `source_original_event_id` | `projection` | `params_id` | "4e3be01ab600001f00100000" | `—` | confirmed；会话参数 ID |
| `extensions.source_private.file_transfer_direction` | `projection` | `file_transfer_direction` | 1 | `—` | confirmed；传输方向 |
| `extensions.source_private.file_transfer_result` | `projection` | `file_transfer_result` | 1 | `—` | confirmed；传输结果 |
| `roles.related.host.name + source_host` | `projection` | `name` | "WIN-EX01" | `—` | confirmed；承载终端 |
| `roles.related.host.ip` | `projection` | `report_ip` | "192.0.2.192" | `—` | confirmed；上报 IP |
| `roles.related.host.mac` | `projection` | `mac` | "00-00-5E-00-53-A7" | `—` | confirmed；归一化 |
| `profiles.endpoint_asset.agent.id` | `projection` | `client_id` | "8424338-de7f6819c3625af3402bd64422d1400a" | `—` | confirmed；客户端 ID |
| `profiles.endpoint_asset.agent.fingerprint_id` | `projection` | `mid` | "1909aacaa9d3411b9237145b0bada7ee" | `—` | confirmed；客户端指纹 |
| `profiles.endpoint_asset.ownership.group.name` | `projection` | `node_name` | "hy" | `—` | confirmed；分组名 |
| `profiles.endpoint_asset.ownership.group.id` | `projection` | `node_id` | "2814380010620583951" | `—` | confirmed；分组 ID |
| `profiles.endpoint_asset.ownership.organization.id` | `projection` | `oid` | "2811278348364284476" | `—` | confirmed；组织 OID |

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
