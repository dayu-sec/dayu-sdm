# WPL → SDM Event 字段映射

> 样例：`usb_storage_connect.expected-sdm-event.json`；WPL 字段 45 个；另有平台上下文与结构字段。
> SDM 落位为逻辑路径；expected 位置为该样例中的实际物理 JSON 路径。

## 一、WPL 字段映射

| WPL 字段 | WPL 值 | SDM 落位 | expected 位置 | expected 值 | 说明 |
|---|---|---|---|---|---|
| `create_time` | 1779087140000 | `occur_time` | `occur_time` | 1779087140000 | 原始秒 1779087140 已由 WPL `time_timestamp` 转毫秒，SDM 直接使用 WPL 值；事件时间 |
| `eid` | "63D1BF90C975470FAF6ECA0FA6D2BE34" | `source_original_event_id` | `source_original_event_id` | 同左 | 设备唯一标识兜底（原始日志无事件 ID，见 wpl-missing-fields）；source_private 不重复保存 |
| `device_id` | "180E2001555223" | `roles.target.resource.id` | `roles_obj.target.resource.id` | 同左 | USB 存储设备 ID |
| `name` | "ic_recorder" | `roles.target.resource.name` | `roles_obj.target.resource.name` | 同左 | 设备登记名 |
| `supplier` | "sony" | `extensions.source_private.supplier` | `extensions_obj.source_private.supplier` | 同左 | 设备厂商 |
| `vid` / `pid` | "054C" / "0B6F" | `extensions.source_private.vid/pid` | `extensions_obj.source_private.vid/pid` | 同左 | USB VID/PID |
| `capacity` | 7161 | `extensions.source_private.capacity` | `extensions_obj.source_private.capacity` | 7161 | 容量 MB |
| `usb_type` | 1 | `extensions.source_private.usb_type` | `extensions_obj.source_private.usb_type` | 1 | 设备类型码，枚举待确认 |
| `usb_status` | 0 | `extensions.source_private.usb_status` | `extensions_obj.source_private.usb_status` | 0 | 设备状态码，枚举待确认 |
| `log_report_type` | 1 | `extensions.source_private.log_report_type` | `extensions_obj.source_private.log_report_type` | 1 | 上报类型（接入/拔出），枚举待确认 |
| `is_register` | 0 | `extensions.source_private.is_register` | `extensions_obj.source_private.is_register` | 0 | 是否登记设备 |
| `is_roam` / `is_intranet` / `out_permission` / `out_valid_day` | 0 / 0 / 2 / 0 | `extensions.source_private.*` | `extensions_obj.source_private.*` | 同左 | 外带管控属性 |
| `result` | 0 | `outcome`（间接） | — | observed | 操作结果码，枚举未确认；outcome 保守为 observed |
| `operation_time` | 1779087140 | — | — | — | 操作时间（秒），与 create_time 同秒；create_time 已作事件时间，不重复 |
| `client_id` | "3705108-…" | `extensions.profiles.endpoint_asset.agent.id` | `extensions_obj.profiles.endpoint_asset.agent.id` | 同左 | 终端 Agent ID |
| `client_mid` | "fc34fec0…" | `extensions.profiles.endpoint_asset.agent.fingerprint_id` | `extensions_obj.profiles.endpoint_asset.agent.fingerprint_id` | 同左 | 终端指纹 |
| `client_name` | "DESKTOP-R2UFGAO" | `roles.source.host.name` | `roles_obj.source.host.name` | 同左 | 投影 source_host 标量 |
| `client_ip` | "198.51.100.162" | `roles.source.host.ip` | `roles_obj.source.host.ip` | 同左 | 终端内网 IP |
| `client_report_ip` | "203.0.113.162" | — | — | — | 上报链路地址，非事件 IP，不落 |
| `client_mac` | "D0-F4-05-3D-DE-B7" | `roles.source.host.mac` | `roles_obj.source.host.mac` | "d0:f4:05:3d:de:b7" | 分隔符归一 |
| `asset_id`（衍生） | 2803747593140568836 | `roles.source.host.id` | `roles_obj.source.host.id` | "2803747593140568836" | 19 位大整数转字符串 |
| `group_node_name` / `group_node_id` | 规划发展部 / 2803769066869751831 | `extensions.profiles.endpoint_asset.ownership` | `extensions_obj.profiles.endpoint_asset.ownership` | group.id/name | 终端分组；organization.id=asset_oid |
| `src_log_type` | 1 | — | — | — | 规则内部路由，log_type 已表达 |
| `collect_time` | 1779087143498 | — | — | — | 采集侧时间，平台上下文 |
| `syslog_topic` | "mobile_storage_client_log" | — | — | — | WPL 路由标识，log_type 已表达 |
| `client_type`/`client_os_version_main`/`client_os_version_release_id`/`client_login_account`/`last_time`/`detail`/`label_name`/`server_id`/`user_name`/`user_number`/`source`/`destination`/`number` | 客户端/空值 | — | — | — | 资产画像或空值，不落库 |

## 二、平台上下文与派生字段

| 来源 | SDM 落位 | expected 值 | 赋值责任 |
|---|---|---|---|
| `platform_context.tenant_id` | `tenant_id` | "" | 平台注入 |
| `platform_context.log_id` | `log_id` | "log-tianqing-mobile-storage-0001" | 平台上下文 |
| `raw_log.usb_storage_connect.raw-log.json` | `raw_msg` | 原始日志串 | 接入层原样保存 |
| `derived.sha256(tenant_id=''\|mapping_id\|source_original_event_id)` | `event_id` | "evt-40fd2684…" | 确定性哈希 |
| `platform_context.ingest_time` / `parse_time` | `ingest_time` / `parse_time` | 1779087141001 / 1779087141120 | 平台上下文 |
| `constant` | `schema_version` / `extensions.schema_version` | 2 | 契约版本常量 |
| `constant` | `mapping_id` | "qax.tianqing.edr_mobile_storage_client_log" | 映射契约常量 |
| `constant` | `data_src_vendor/product/category` | qax/tianqing/endpoint_security | 产品身份常量 |
| `platform_context.data_src_instance_id` | `data_src_instance_id` | "collector-tianqing-poc-01" | 平台上下文 |
| `constant` | `log_type` / `log_name` | edr_mobile_storage_client_log / 天擎移动存储客户端日志 | 日志身份常量 |
| `constant` | `record_kind` | activity | 行为活动记录 |
| `constant` | `event_domain` | endpoint | 06 推荐值：终端活动 |
| `constant` | `event_type` | generic_event | 06 #28；06 暂无 USB/外设事件类型（见未决 1） |
| `constant` | `operation` / `outcome` / `severity` | null / observed / info | generic_event 无动作；result 枚举未确认故 outcome 保守 |
| `derived.entity_ref(host, asset_id)` | `roles.source.ref_id` | "host::2803747593140568836" | 三段式引用 |
| `derived.entity_ref(resource, wpl.device_id)` | `roles.target.ref_id` | "resource::180E2001555223" | 三段式引用 |
| `platform_dictionary(wpl.usb_type)` | `roles.target.resource.type` | "usb_storage_device" | 受控枚举转换（值待 registry 确认） |
| `constant` | `observer_vendor/product` | qax/tianqing | 产品身份常量 |
| `wpl.client_name` | `source_host` | "DESKTOP-R2UFGAO" | 标量投影 |
| `constant` | `extensions.profiles.endpoint_asset.subject_ref.ref_id` | "host::2803747593140568836" | 指向 roles.source |

## 三、不落库字段

| WPL 字段 | WPL 值 | 原因 |
|---|---|---|
| `client_report_ip` | "203.0.113.162" | 上报链路地址，非事件 IP |
| `operation_time` | 1779087140 | 与 create_time 同秒，事件时间已由 create_time 表达 |
| `src_log_type` / `syslog_topic` | 1 / mobile_storage_client_log | WPL 路由标识，log_type 已表达 |
| `collect_time` | 1779087143498 | 采集侧时间，非事件时间 |
| `client_type`/`client_os_version_main`/`client_os_version_release_id`/`client_login_account`/`last_time` | 客户端元数据 | 资产画像，无检索价值 |
| `detail`/`label_name`/`server_id`/`user_name`/`user_number`/`source`/`destination`/`number` | null | 空值不落 |

## 四、未决问题

1. 06 枚举无 USB/移动存储事件类型，暂用 generic_event（#28）兜底；建议后续扩展 `usb_storage_access` 或类似类型。
2. `usb_type`（1）、`usb_status`（0）、`log_report_type`（1）、`result`（0）枚举含义待天擎字典确认；outcome 保守为 observed。
3. `roles.target.resource.type="usb_storage_device"` 为样例自定受控值，待 registry 确认或扩展资源类型字典。
4. 原始日志无事件 ID，source_original_event_id 暂用 eid（设备标识）兜底；同一设备多条事件 eid 相同，跨事件去重需依赖 occur_time+asset_id 组合，建议采集层补事件 ID（见 wpl-missing-fields）。

## 五、WPL/OML 编写规则

> WPL 只负责提取表中的 source 字段；Meta 和 Content 的赋值由 OML 按下表实现。
> `partial` 表示当前只有样例值或局部说明，不能视为完整厂商字典。

### 5.1 Meta 区

| SDM 字段 | 规则类型 | 输入/来源 | 赋值 | 未命中 | 状态与证据 |
|---|---|---|---|---|---|
| `tenant_id` | `context` | `platform_context.tenant_id` | `platform_context.tenant_id` | `—` | confirmed；平台注入 |
| `log_id` | `context` | `platform_context.log_id` | `platform_context.log_id` | `—` | confirmed；平台上下文 |
| `event_id` | `derived` | `derived.sha256(tenant_id=''|mapping_id|source_original_event_id)` | `derived.sha256(tenant_id=''|mapping_id|source_original_event_id)` | `—` | confirmed；确定性哈希 |
| `schema_version` | `constant` | `constant` | 2 | `—` | confirmed；契约版本 |
| `extensions.schema_version` | `constant` | `constant` | 2 | `—` | confirmed；契约版本 |
| `mapping_id` | `derived` | `constant` | `constant` | `—` | confirmed；映射契约 |
| `data_src_vendor` | `constant` | `constant` | "qax" | `—` | confirmed；产品身份 |
| `data_src_product` | `constant` | `constant` | "tianqing" | `—` | confirmed；产品身份 |
| `category` | `constant` | `constant` | "endpoint_security" | `—` | confirmed；产品身份 |
| `data_src_instance_id` | `context` | `platform_context.data_src_instance_id` | `platform_context.data_src_instance_id` | `—` | confirmed；平台上下文 |
| `log_type` | `constant` | `constant` | "edr_mobile_storage_client_log" | `—` | confirmed；日志身份 |
| `log_name` | `constant` | `constant` | "天擎移动存储客户端日志" | `—` | confirmed；日志身份 |
| `record_kind` | `derived` | `constant` | `constant` | `—` | confirmed；行为活动 |
| `event_domain` | `derived` | `constant` | `constant` | `—` | confirmed；06 推荐值 |
| `event_type` | `derived` | `constant` | `constant` | `—` | confirmed；06 #28 兜底，06 无 USB 类型 |
| `event_category` | `constant` | `constant` | "audit" | `—` | confirmed；USB 设备接入活动，PDF §3.7.1 log_report_type=1=插拔日志 |
| `operation` | `constant` | `constant` | `chars(None)` | `—` | confirmed；generic_event 无动作；result 枚举未确认 |
| `outcome` | `constant` | `constant` | "observed" | `—` | confirmed；generic_event 无动作；result 枚举未确认 |
| `severity` | `constant` | `constant` | "info" | `—` | confirmed；generic_event 无动作；result 枚举未确认 |
| `roles.source.ref_id` | `derived` | `derived.entity_ref(host, asset_id)` | `derived.entity_ref(host, asset_id)` | `—` | confirmed；三段式引用 |
| `roles.target.ref_id` | `derived` | `derived.entity_ref(resource, wpl.device_id)` | `derived.entity_ref(resource, wpl.device_id)` | `—` | confirmed；三段式引用 |
| `observer_vendor` | `constant` | `constant` | "qax" | `—` | confirmed；产品身份 |
| `observer_product` | `constant` | `constant` | "tianqing" | `—` | confirmed；产品身份 |
| `extensions.profiles.endpoint_asset.subject_ref.ref_id` | `derived` | `constant` | `constant` | `—` | confirmed；指向 roles.source |
| `ingest_time` | `context` | `platform_context.ingest_time` | `read(ingest_time)` | `—` | confirmed；expected 事件中的平台上下文字段 |
| `parse_time` | `context` | `platform_context.parse_time` | `read(parse_time)` | `—` | confirmed；expected 事件中的平台上下文字段 |
| `data_src_category` | `constant` | `constant.data_src_category` | "endpoint_security" | `—` | confirmed；expected 事件确认的日志类型级常量 |

### 5.2 Content 区

| SDM 字段 | 规则类型 | WPL 字段 | 映射/赋值 | 未命中 | 状态与证据 |
|---|---|---|---|---|---|
| `roles.target.resource.type` | `dictionary` | `usb_type` | 1 -> "usb_storage_device" | `preserve_in_extension_and_review` | partial；受控枚举转换；值待 registry 确认 |
| `source_host` | `projection` | `client_name` | `wpl.client_name` | `—` | confirmed；标量投影 |
| `occur_time` | `projection` | `create_time` | 1779087140000 | `—` | confirmed；原始秒由 WPL time_timestamp 转毫秒，SDM 直接使用 WPL 值 |
| `source_original_event_id` | `projection` | `eid` | "63D1BF90C975470FAF6ECA0FA6D2BE34" | `—` | confirmed；设备标识兜底，原始日志无事件 ID |
| `roles.target.resource.id` | `projection` | `device_id` | "180E2001555223" | `—` | confirmed；USB 设备 ID |
| `roles.target.resource.name` | `projection` | `name` | "ic_recorder" | `—` | confirmed；设备登记名 |
| `extensions.source_private.supplier` | `projection` | `supplier` | "sony" | `—` | confirmed；设备厂商 |
| `extensions.source_private.vid` | `projection` | `vid` | "054C" | `—` | confirmed；USB VID |
| `extensions.source_private.pid` | `projection` | `pid` | "0B6F" | `—` | confirmed；USB PID |
| `extensions.source_private.capacity` | `projection` | `capacity` | 7161 | `—` | confirmed；容量 MB |
| `extensions.source_private.usb_type` | `projection` | `usb_type` | 1 | `—` | confirmed；设备类型码，枚举待确认 |
| `extensions.source_private.usb_status` | `projection` | `usb_status` | 0 | `—` | confirmed；状态码，枚举待确认 |
| `extensions.source_private.log_report_type` | `projection` | `log_report_type` | 1 | `—` | confirmed；上报类型，枚举待确认 |
| `extensions.source_private.is_register` | `projection` | `is_register` | 0 | `—` | confirmed；是否登记设备 |
| `extensions.source_private.is_roam` | `projection` | `is_roam` | 0 | `—` | confirmed；是否漫游 |
| `extensions.source_private.is_intranet` | `projection` | `is_intranet` | 0 | `—` | confirmed；是否内网 |
| `extensions.source_private.out_permission` | `projection` | `out_permission` | 2 | `—` | confirmed；外带权限 |
| `extensions.source_private.out_valid_day` | `projection` | `out_valid_day` | 0 | `—` | confirmed；外带有效天数 |
| `extensions.profiles.endpoint_asset.agent.id` | `projection` | `client_id` | "3705108-9a592f3c6d5b7223eeaa037169a45ee1" | `—` | confirmed；Agent ID |
| `extensions.profiles.endpoint_asset.agent.fingerprint_id` | `projection` | `client_mid` | "fc34fec09c1aefcf7de90f2181d04305fc9f4120a8d1a187ea6e99730507e073" | `—` | confirmed；终端指纹 |
| `roles.source.host.name` | `projection` | `client_name` | "DESKTOP-R2UFGAO" | `—` | confirmed；投影 source_host |
| `roles.source.host.ip` | `projection` | `client_ip` | "198.51.100.162" | `—` | confirmed；终端内网 IP |
| `roles.source.host.mac` | `projection` | `client_mac` | "d0:f4:05:3d:de:b7" | `—` | confirmed；分隔符归一 |
| `roles.source.host.id` | `projection` | `asset_id` | "2803747593140568836" | `—` | confirmed；19 位大整数转字符串 |
| `extensions.profiles.endpoint_asset.ownership.organization.id` | `projection` | `asset_oid` | "2715543661537396001" | `—` | confirmed；组织 ID |
| `extensions.profiles.endpoint_asset.ownership.group.name` | `projection` | `group_node_name` | "规划发展部" | `—` | confirmed；终端分组 |
| `extensions.profiles.endpoint_asset.ownership.group.id` | `projection` | `group_node_id` | "2803769066869751831" | `—` | confirmed；分组 ID |

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
