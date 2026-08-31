# WPL → SDM Event 字段映射

> 样例：`iexplore_attack_block.expected-sdm-event.json`；WPL 字段 44 个。

## 一、WPL 字段映射

| WPL 字段 | WPL 值 | SDM 落位 | expected 位置 | 说明 |
|---|---|---|---|---|
| `attack_time` | 1617357947536 | `occur_time` | `occur_time` | 纳秒 1617357947536497000 由 WPL 转毫秒 |
| `attack_type` | 2 | `extensions.source_private.attack_type` | 同左 | 攻击类型枚举（待确认） |
| `result` | 1 | `extensions.source_private.result` | 同左 | 拦截结果（待确认） |
| `trigger_mode` | 20 | `extensions.source_private.trigger_mode` | 同左 | 触发方式（待确认） |
| `name` | "Test-shifang-Win7" | `roles.related[].host.name`/`source_host` | 同左 | 行为执行终端；source_host 为热字段投影 |
| `report_ip` | "192.0.2.71" | `roles.related[].host.ip` | 同左 | 执行终端上报 IP |
| `mac` | "00-00-5E-00-53-64" | `roles.related[].host.mac` | "00:00:5E:00:53:17" | 归一化 |
| `client_id`/`mid`/`node_name`/`node_id`/`oid` | — | `profiles.endpoint_asset.*` | 同左 | 资产画像 |

## 二、非 WPL 来源（规则缺口，raw_log 补齐）

| 来源 | SDM 落位 | 值 | 说明 |
|---|---|---|---|
| `data_gap.raw_log.subject` | `roles.source.process.name` | "iexplore.exe" | 原始日志存在但 WPL 未抽，见 wpl-missing-fields |
| `data_gap.raw_log.object` | `roles.target.resource`、`facets.registry` | `registry_value/testkey/HKEY_LOCAL_MACHINE\…\run` | 原始日志存在但 WPL 未抽；纠正 JSON 反斜杠转义并拆分键路径、值名和新值 |
| `derived.entity_ref(process, raw_log.subject)` | `roles.source.ref_id` | "process::iexplore.exe" | 三段式引用 |
| `derived.entity_ref(resource, normalized_registry_path, value_name)` | `roles.target.ref_id` | "resource::hklm_run_testkey" | 由纠正后的注册表路径和值名派生 |
| `derived.sha256(…\|attack_time_ms\|subject)` | `event_id` | "evt-d8bd22a3…" | 无 uuid，派生组合兜底 |

## 三、未决问题

1. 厂商 `event_type=11`（脚本攻击）与 object=注册表不一致；以 object 为准。
2. `attack_type=2` / `trigger_mode=20` 业务名仍待字典确认。
3. 原始日志无事件 ID，source_original_event_id 用派生组合。

## 五、WPL/OML 编写规则

> WPL 只负责提取表中的 source 字段；Meta 和 Content 的赋值由 OML 按下表实现。
> `partial` 表示当前只有样例值或局部说明，不能视为完整厂商字典。

### 5.1 Meta 区

| SDM 字段 | 规则类型 | 输入/来源 | 赋值 | 未命中 | 状态与证据 |
|---|---|---|---|---|---|
| `event_id` | `derived` | `derived.sha256(tenant_id=''|mapping_id|source_original_event_id)` | `derived.sha256(tenant_id=''|mapping_id|source_original_event_id)` | `—` | confirmed；source_original_event_id=attack_time_ms|subject 派生（无 uuid，见 wpl-missing-fields） |
| `roles.source.ref_id` | `derived` | `derived.entity_ref(process, raw_log.subject)` | `derived.entity_ref(process, raw_log.subject)` | `—` | confirmed；三段式引用 |
| `roles.related[].ref_id（profiles.subject_ref）` | `derived` | `derived.entity_ref(host, platform_context.asset_id)` | `derived.entity_ref(host, platform_context.asset_id)` | `—` | confirmed；受管资产 |
| `roles.target.ref_id` | `derived` | `derived.entity_ref(resource, normalized_registry_path, value_name)` | `derived.entity_ref(resource, normalized_registry_path, value_name)` | `—` | confirmed；注册表值稳定引用 |
| `roles.related[].ref_id` | `derived` | `derived.entity_ref(host, platform_context.asset_id)` | `derived.entity_ref(host, platform_context.asset_id)` | `—` | confirmed；行为执行终端关联实体 |
| `extensions.profiles.endpoint_asset.subject_ref.ref_id` | `context` | `platform_context.asset_id` | `platform_context.asset_id` | `—` | confirmed；缺口补齐 |
| `event_type` | `constant` | `constant` | "registry_modification" | `—` | confirmed；object 为注册表 set |
| `event_category` | `constant` | `constant` | "alert" | `—` | confirmed；攻击防护拦截 |
| `event_domain` | `constant` | `constant` | "threat" | `—` | confirmed；防护拦截为检测告警 |
| `record_kind` | `constant` | `constant` | "finding" | `—` | confirmed；防护拦截为检测告警 |
| `outcome` | `constant` | `constant` | "denied" | `—` | confirmed；PDF §3.2.3 result=1 已拦截 |
| `severity` | `constant` | `constant` | "info" | `—` | confirmed；防护拦截语义=拒绝；result 枚举待确认 |
| `source_finding_obj.title` | `derived` | `constant` | `constant` | `—` | confirmed；检测结论 |
| `observer_vendor` | `constant` | `constant` | "qax" | `—` | confirmed；产品身份 |
| `observer_product` | `constant` | `constant` | "tianqing" | `—` | confirmed；产品身份 |
| `log_id` | `context` | `platform_context.log_id` | `read(log_id)` | `—` | confirmed；expected 事件中的平台上下文字段 |
| `tenant_id` | `context` | `platform_context.tenant_id` | `read(tenant_id)` | `—` | confirmed；expected 事件中的平台上下文字段 |
| `ingest_time` | `context` | `platform_context.ingest_time` | `read(ingest_time)` | `—` | confirmed；expected 事件中的平台上下文字段 |
| `parse_time` | `context` | `platform_context.parse_time` | `read(parse_time)` | `—` | confirmed；expected 事件中的平台上下文字段 |
| `data_src_instance_id` | `context` | `platform_context.data_src_instance_id` | `read(data_src_instance_id)` | `—` | confirmed；expected 事件中的平台上下文字段 |
| `schema_version` | `constant` | `constant.schema_version` | 2 | `—` | confirmed；expected 事件确认的日志类型级常量 |
| `data_src_vendor` | `constant` | `constant.data_src_vendor` | "qax" | `—` | confirmed；expected 事件确认的日志类型级常量 |
| `mapping_id` | `constant` | `constant.mapping_id` | "qax.tianqing.edr_attack_protection" | `—` | confirmed；expected 事件确认的日志类型级常量 |
| `data_src_product` | `constant` | `constant.data_src_product` | "tianqing" | `—` | confirmed；expected 事件确认的日志类型级常量 |
| `log_type` | `constant` | `constant.log_type` | "edr_attack_protection" | `—` | confirmed；expected 事件确认的日志类型级常量 |
| `data_src_category` | `constant` | `constant.data_src_category` | "endpoint_security" | `—` | confirmed；expected 事件确认的日志类型级常量 |
| `log_name` | `constant` | `constant.log_name` | "天擎攻击防护日志" | `—` | confirmed；expected 事件确认的日志类型级常量 |

### 5.2 Content 区

| SDM 字段 | 规则类型 | WPL 字段 | 映射/赋值 | 未命中 | 状态与证据 |
|---|---|---|---|---|---|
| `roles.source.process.name` | `gap` | `data_gap.raw_log.subject` | `data_gap.raw_log.subject` | `—` | missing；规则未抽（见 wpl-missing-fields） |
| `roles.target.resource/facets.registry` | `gap` | `data_gap.raw_log.object` | `data_gap.raw_log.object` | `—` | missing；规则未抽；按注册表语义拆分键路径、值名和新值，并纠正原始 JSON 反斜杠转义异常 |
| `occur_time` | `projection` | `attack_time` | 1617357947536 | `—` | confirmed；WPL 纳秒→毫秒，SDM 直接用 |
| `extensions.source_private.attack_type` | `projection` | `attack_type` | 2 | `—` | confirmed；攻击类型枚举（2 待确认，私有暂存） |
| `extensions.source_private.result` | `projection` | `result` | 1 | `—` | confirmed；PDF 已拦截；不进 finding.status |
| `extensions.source_private.trigger_mode` | `projection` | `trigger_mode` | 20 | `—` | confirmed；触发方式（20 待确认） |
| `roles.related.host.name + source_host` | `projection` | `name` | "Test-shifang-Win7" | `—` | confirmed；承载终端 |
| `roles.related.host.ip` | `projection` | `report_ip` | "192.0.2.71" | `—` | confirmed；上报 IP |
| `roles.related.host.mac` | `projection` | `mac` | "00-00-5E-00-53-64" | `—` | confirmed；归一化 |
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
