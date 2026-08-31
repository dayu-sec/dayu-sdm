# WPL → SDM Event 字段映射

> 样例：`data_export.expected-sdm-event.json`；WPL 字段 11 个；另有平台上下文、缺口补齐及结构字段。
> SDM 落位为逻辑路径；expected 位置为该样例中的实际物理 JSON 路径。

## 一、WPL 字段映射

| WPL 字段 | WPL 值 | SDM 落位 | expected 位置 | expected 值 | 说明 |
|---|---|---|---|---|---|
| `create_time` | 1670827544000 | `occur_time` | `occur_time` | 1670827544000 | 原始 `create_time=1670827544` 秒已由 WPL `time_timestamp` 转成毫秒，SDM 直接使用 WPL 毫秒值 |
| `client_ip` | "203.0.113.138" | `roles.source.endpoint.ip` | `roles_obj.source.endpoint.ip` | "203.0.113.138" | 操作来源 IP，投影 source_ip 标量 |
| `operator` | 2802480805320851645 | `roles.source.user.uid` | `roles_obj.source.user.uid` | "2802480805320851645" | 操作员账号 ID；19 位大整数转字符串保精度 |
| `operator_name` | "system001" | `roles.source.user.name` | `roles_obj.source.user.name` | "system001" | 操作员账号名，投影 source_user 标量 |
| `path` | "设置系统管理/系统设置/数据导出" | `extensions.source_private.path` | `extensions_obj.source_private.path` | 同左 | 控制台菜单路径；厂商、产品和日志类型由顶层来源字段表达 |
| `entity_id` | null | — | — | — | 空值不落库 |
| `status` | 3 | `extensions.source_private.status` + `outcome=success` | `outcome` | success | PDF §4.2.1 status=3 为成功 |
| `op_level` | 1 | `extensions.source_private.op_level` | `extensions_obj.source_private.op_level` | 1 | 操作级别 |
| `asset_id` | 2795221464750489887 | `extensions.source_private.asset_id` | `extensions_obj.source_private.asset_id` | 2795221464750489887 | 控制台关联资产上下文；非受管终端事件，语义待确认 |
| `asset_oid` | 2715229325145146394 | `extensions.source_private.asset_oid` | `extensions_obj.source_private.asset_oid` | 2715229325145146394 | 组织节点 ID，同上 |
| `op_type` | 106 | `extensions.source_private.op_type` | `extensions_obj.source_private.op_type` | 106 | 操作类型编码（106=数据导出，字典未确认） |

## 二、平台上下文与缺口补齐

| 来源 | SDM 落位 | expected 值 | 赋值责任 |
|---|---|---|---|
| `platform_context.tenant_id` | `tenant_id` | "" | 平台注入 |
| `platform_context.log_id` | `log_id` | "log-tianqing-cs-op-0001" | 平台上下文 |
| `raw_log.data_export.raw-log.json` | `raw_msg` | 原始日志串 | 接入层原样保存，不由平台富化生成 |
| `platform_context.source_original_event_id` | `source_original_event_id` | "607d65f6-…" | 平台保留原始 uuid（WPL 缺口，见 wpl-missing-fields） |
| `derived.sha256(tenant_id=''\|mapping_id\|source_original_event_id)` | `event_id` | "evt-e3f117d0…" | 确定性哈希，输入为 tenant_id、mapping_id、source_original_event_id |
| `platform_context.ingest_time` | `ingest_time` | 1670827545001 | 平台上下文 |
| `platform_context.parse_time` | `parse_time` | 1670827545120 | 平台上下文 |
| `constant` | `schema_version` / `extensions.schema_version` | 2 | 契约版本常量 |
| `constant` | `mapping_id` | "qax.tianqing.cs_op_log" | 映射契约常量 |
| `constant` | `data_src_vendor/product/category` | qax/tianqing/endpoint_security | 产品身份常量 |
| `platform_context.data_src_instance_id` | `data_src_instance_id` | "collector-tianqing-poc-01" | 平台上下文 |
| `constant` | `log_type` / `log_name` | cs_op_log / 天擎计算系统操作日志 | 日志身份常量 |
| `constant` | `record_kind` | activity | 审计活动记录 |
| `constant` | `event_domain` | system | 06 枚举：系统与系统审计活动 |
| `constant` | `event_type` | system_audit_log_uncategorized | 06 枚举 #88，cs_op 无更具体类型 |
| `constant` | `operation` / `outcome` / `severity` | null / success / info | 88 无动作；status=3 → success |
| `derived.entity_ref(user, wpl.operator)` | `roles.source.ref_id` | "user::2802480805320851645" | 三段式引用，tenant 段为空 |
| `constant` | `roles.source.entity_type` | user | 操作员为独立用户主体 |
| `constant` | `observer_vendor/product` | qax/tianqing | 产品身份常量 |
| `wpl.operator_name` | `source_user` | "system001" | 标量热检索投影（roles.source.user.name） |
| `wpl.client_ip` | `source_ip` | "203.0.113.138" | 标量热检索投影（roles.source.endpoint.ip） |

## 三、不落库字段

| WPL 字段 | WPL 值 | 原因 |
|---|---|---|
| `entity_id` | null | 空值不落 |

`roles.target` 空对象 `{}`、`roles.carriers` 空数组 `[]`：本样例没有可确认的标准客体实体，也没有可识别的会话、进程或协议载体，因此不虚构对象；菜单路径仅保留在 `source_private`。

## 四、未决问题

1. `status=3` 已确认成功；`op_type=106` 仍无业务名。
2. `path`（控制台菜单）与 `asset_id`/`asset_oid` 无标准审计模型路径，暂存 source_private；待 audit 事件模型扩展或确认 asset 语义后迁移。
3. `event_type` 使用 system_audit_log_uncategorized（#88）；若后续需区分具体操作，需 06 枚举扩展。

## 五、source_private 路径约定

私有扩展字段直接放在 `extensions.source_private.<field>` 下；来源厂商、产品、日志类型和映射契约已由顶层字段表达，仅存放标准模型无法表达且确有价值的数据。

## 五、WPL/OML 编写规则

> WPL 只负责提取表中的 source 字段；Meta 和 Content 的赋值由 OML 按下表实现。
> `partial` 表示当前只有样例值或局部说明，不能视为完整厂商字典。

### 5.1 Meta 区

| SDM 字段 | 规则类型 | 输入/来源 | 赋值 | 未命中 | 状态与证据 |
|---|---|---|---|---|---|
| `tenant_id` | `context` | `platform_context.tenant_id` | `platform_context.tenant_id` | `—` | confirmed；平台注入 |
| `log_id` | `context` | `platform_context.log_id` | `platform_context.log_id` | `—` | confirmed；平台上下文 |
| `source_original_event_id` | `context` | `platform_context.source_original_event_id` | `platform_context.source_original_event_id` | `—` | confirmed；WPL 缺口补齐 |
| `event_id` | `derived` | `derived.sha256(tenant_id=''|mapping_id|source_original_event_id)` | `derived.sha256(tenant_id=''|mapping_id|source_original_event_id)` | `—` | confirmed；确定性哈希 |
| `schema_version` | `constant` | `constant` | 2 | `—` | confirmed；契约版本 |
| `extensions.schema_version` | `constant` | `constant` | 2 | `—` | confirmed；契约版本 |
| `mapping_id` | `derived` | `constant` | `constant` | `—` | confirmed；映射契约 |
| `data_src_vendor` | `constant` | `constant` | "qax" | `—` | confirmed；产品身份 |
| `data_src_product` | `constant` | `constant` | "tianqing" | `—` | confirmed；产品身份 |
| `category` | `constant` | `constant` | "endpoint_security" | `—` | confirmed；产品身份 |
| `data_src_instance_id` | `context` | `platform_context.data_src_instance_id` | `platform_context.data_src_instance_id` | `—` | confirmed；平台上下文 |
| `log_type` | `constant` | `constant` | "cs_op_log" | `—` | confirmed；日志身份 |
| `log_name` | `constant` | `constant` | "天擎计算系统操作日志" | `—` | confirmed；日志身份 |
| `record_kind` | `derived` | `constant` | `constant` | `—` | confirmed；审计活动 |
| `event_domain` | `derived` | `constant` | `constant` | `—` | confirmed；06 枚举 |
| `event_type` | `derived` | `constant` | `constant` | `—` | confirmed；06 枚举 #88 |
| `operation` | `constant` | `constant` | `chars(None)` | `—` | confirmed；88 无动作 |
| `outcome` | `constant` | `constant` | "success" | `—` | confirmed；PDF status=3 |
| `severity` | `constant` | `constant` | "info" | `—` | confirmed；88 无动作；status 未确认 |
| `roles.source.ref_id` | `derived` | `derived.entity_ref(user, wpl.operator)` | `derived.entity_ref(user, wpl.operator)` | `—` | confirmed；三段式引用 |
| `roles.source.entity_type` | `derived` | `constant` | `constant` | `—` | confirmed；独立用户主体 |
| `observer_vendor` | `constant` | `constant` | "qax" | `—` | confirmed；产品身份 |
| `observer_product` | `constant` | `constant` | "tianqing" | `—` | confirmed；产品身份 |
| `ingest_time` | `context` | `platform_context.ingest_time` | `read(ingest_time)` | `—` | confirmed；expected 事件中的平台上下文字段 |
| `parse_time` | `context` | `platform_context.parse_time` | `read(parse_time)` | `—` | confirmed；expected 事件中的平台上下文字段 |
| `data_src_category` | `constant` | `constant.data_src_category` | "endpoint_security" | `—` | confirmed；expected 事件确认的日志类型级常量 |

### 5.2 Content 区

| SDM 字段 | 规则类型 | WPL 字段 | 映射/赋值 | 未命中 | 状态与证据 |
|---|---|---|---|---|---|
| `source_user` | `projection` | `operator_name` | `wpl.operator_name` | `—` | confirmed；标量投影 |
| `source_ip` | `projection` | `client_ip` | `wpl.client_ip` | `—` | confirmed；标量投影 |
| `occur_time` | `projection` | `create_time` | 1670827544000 | `—` | confirmed；原始日志 create_time=1670827544 秒已由 WPL time_timestamp 转为毫秒；SDM 直接使用 WPL 毫秒值 |
| `roles.source.endpoint.ip` | `projection` | `client_ip` | "203.0.113.138" | `—` | confirmed；操作来源 IP，投影 source_ip |
| `roles.source.user.uid` | `projection` | `operator` | "2802480805320851645" | `—` | confirmed；操作员账号 ID；19 位大整数转字符串保精度 |
| `roles.source.user.name` | `projection` | `operator_name` | "system001" | `—` | confirmed；投影 source_user |
| `extensions.source_private.path` | `projection` | `path` | "设置系统管理/系统设置/数据导出" | `—` | confirmed；控制台菜单路径；厂商、产品和日志类型已由顶层来源字段表达 |
| `extensions.source_private.status` | `projection` | `status` | 3 | `—` | confirmed；操作状态码，枚举未确认 |
| `extensions.source_private.op_level` | `projection` | `op_level` | 1 | `—` | confirmed；操作级别 |
| `extensions.source_private.asset_id` | `projection` | `asset_id` | "2795221464750489887" | `—` | confirmed；控制台关联资产上下文，语义待确认；大整数转字符串保精度 |
| `extensions.source_private.asset_oid` | `projection` | `asset_oid` | "2715229325145146394" | `—` | confirmed；组织节点 ID；大整数转字符串保精度 |
| `extensions.source_private.op_type` | `projection` | `op_type` | 106 | `—` | confirmed；操作类型编码，字典未确认 |

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
