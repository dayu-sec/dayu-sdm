# WPL → SDM Event 字段映射

> 样例：`adware_detection.expected-sdm-event.json`；WPL 字段 39 个；另有平台上下文与结构字段。
> SDM 落位为逻辑路径；expected 位置为该样例中的实际物理 JSON 路径。

## 一、WPL 字段映射

| WPL 字段 | WPL 值 | SDM 落位 | expected 位置 | expected 值 | 说明 |
|---|---|---|---|---|---|
| `file_alarm_time` | 1732493003000 | `occur_time` | `occur_time` | 1732493003000 | 原始 19 位纳秒已由 WPL `time_timestamp` 转毫秒，SDM 直接使用 WPL 毫秒值；事件时间 |
| `guid` | "sddguidD288505E-…" | `source_original_event_id` | `source_original_event_id` | 同左 | 病毒记录唯一标识（非标准 GUID，含 sddguid 前缀）；确定性 event_id 输入 |
| `virus_name` | "Adware.Agent.30f0fd07" | `source_finding.title` | `source_finding_obj.title` | "检出广告软件 Adware.Agent.30f0fd07" | 检出结论，title 加"检出"前缀 |
| `virus_type` | "adware" | `source_finding.category.original` | `source_finding_obj.category.original.code` | "adware" | 病毒类型映射原始分类 code，name="广告软件" |
| `file_path` | "C:\\Users\\…\\出品部门牌_Key.vbs" | `roles.target.file.path` | `roles_obj.target.file.path` | 同左 | 检出文件路径，投影 target_file_path 标量 |
| `file_create_time` | 1731897537000 | `roles.target.file.created_time` | `roles_obj.target.file.created_time` | 1731897537000 | 19 位纳秒由 WPL `time_timestamp` 转毫秒；05 目录 `roles.target.file.created_time` 已注册 |
| `md5` | "b4b7b2baf26fc319ef817cb95d33ab59" | `roles.target.file.hashes.md5` | `roles_obj.target.file.hashes.md5` | 同左 | 检出文件 MD5 |
| `sha1` | "bf629dd7792044c8701d6939e66fe1e40fcba43d" | `roles.target.file.hashes.sha1` | `roles_obj.target.file.hashes.sha1` | 同左 | 检出文件 SHA1 |
| `severity` | "0" | `source_finding.severity` | `source_finding_obj.severity` | "0" | 原始严重度（chars 转换），0 不在 06 顶层 severity 枚举，保留原始值 |
| `result` | 1 | `extensions.source_private.result` | `extensions_obj.source_private.result` | 1 | PDF §3.2.1 删除成功；不进 outcome/finding.status |
| `trigger_mode` | 2 | `extensions.source_private.trigger_mode` | `extensions_obj.source_private.trigger_mode` | 2 | 触发方式编码（实时监控/手动），枚举待确认 |
| `need_reboot` | 0 | `extensions.source_private.need_reboot` | `extensions_obj.source_private.need_reboot` | 0 | 是否需重启 |
| `scanners` | "qce" | `extensions.source_private.scanners` | `extensions_obj.source_private.scanners` | "qce" | 查杀引擎标识 |
| `client_id` | "8424338-…" | `extensions.profiles.endpoint_asset.agent.id` | `extensions_obj.profiles.endpoint_asset.agent.id` | 同左 | 终端 Agent ID |
| `mid` | "1909aacaa9d3411b9237145b0bada7ee" | `extensions.profiles.endpoint_asset.agent.fingerprint_id` | `extensions_obj.profiles.endpoint_asset.agent.fingerprint_id` | 同左 | 终端指纹 |
| `name` | "WIN-UMAG4B1GGKV" | `roles.source.host.name` | `roles_obj.source.host.name` | 同左 | 终端主机名，投影 source_host 标量 |
| `report_ip` | "192.0.2.192" | `roles.source.host.ip` | `roles_obj.source.host.ip` | 同左 | 终端上报 IP（规则抽取；原始 client_info.ip 未抽） |
| `mac` | "00-00-5E-00-53-A7" | `roles.source.host.mac` | `roles_obj.source.host.mac` | "00:00:5E:00:53:AC" | 分隔符归一 |
| `domain` | "clinetsdddomain" | `roles.source.host.domain` | `roles_obj.source.host.domain` | 同左 | 主机域 |
| `asset_id`（衍生） | 2811278348364284476 | `roles.source.host.id` | `roles_obj.source.host.id` | "2811278348364284476" | 19 位大整数转字符串；来自原始日志顶层 asset_id（规则未直接抽取，平台按 WPL 上下文提供，见未决 3） |
| `group_info` | [{node_name:"hy",…}] | `extensions.profiles.endpoint_asset.ownership` | `extensions_obj.profiles.endpoint_asset.ownership` | group.id/name | 终端分组（node_id/node_name），organization.id=asset_oid |
| `create_time`/`update_time`/`os`/`release_id`/`build_version`/`main`/`describe`/`sys_space`/`core_number`/`login_account`/`memory_size`/`ie_version`/`computer_working_group`/`os_bit`/`nic_list`/`report_ipv6`/`state`/`activation`/`system_language` | 客户端元数据 | — | — | — | 终端资产画像类元数据，无检索价值，不落库；原值保留 raw_msg |

## 二、平台上下文与派生字段

| 来源 | SDM 落位 | expected 值 | 赋值责任 |
|---|---|---|---|
| `platform_context.tenant_id` | `tenant_id` | "" | 平台注入 |
| `platform_context.log_id` | `log_id` | "log-tianqing-antivirus-virus-0001" | 平台上下文 |
| `raw_log.adware_detection.raw-log.json` | `raw_msg` | 原始日志串 | 接入层原样保存 |
| `derived.sha256(tenant_id=''\|mapping_id\|source_original_event_id)` | `event_id` | "evt-2acb19ee…" | 确定性哈希 |
| `platform_context.ingest_time` / `parse_time` | `ingest_time` / `parse_time` | 1732493004001 / 1732493004120 | 平台上下文 |
| `constant` | `schema_version` / `extensions.schema_version` | 2 | 契约版本常量 |
| `constant` | `mapping_id` | "qax.tianqing.edr_antivirus_virus" | 映射契约常量 |
| `constant` | `data_src_vendor/product/category` | qax/tianqing/endpoint_security | 产品身份常量 |
| `platform_context.data_src_instance_id` | `data_src_instance_id` | "collector-tianqing-poc-01" | 平台上下文 |
| `constant` | `log_type` / `log_name` | edr_antivirus_virus / 天擎病毒查杀日志 | 日志身份常量 |
| `constant` | `record_kind` | finding | 检测结论 |
| `constant` | `event_domain` | threat | 06 推荐值：威胁检测和安全发现 |
| `constant` | `event_type` | generic_event | 06 #28；06 暂无恶意软件检出类型（见未决 1） |
| `constant` | `operation` / `outcome` / `severity` | null / observed / info | generic_event 无动作；检出为观察结果；顶层 severity 用 06 枚举 info |
| `wpl.guid` | `source_original_event_id` | "sddguidD288505E-…" | WPL 直接映射 |
| `derived.entity_ref(host, platform_context.asset_id)` | `roles.source.ref_id` | "host::2811278348364284476" | 三段式引用；asset_id 见 platform-context 与 wpl-missing-fields |
| `derived.entity_ref(file, wpl.md5)` | `roles.target.ref_id` | "file::b4b7b2ba…" | 三段式引用 |
| `constant` | `observer_vendor/product` | qax/tianqing | 产品身份常量 |
| `wpl.name` | `source_host` | "WIN-UMAG4B1GGKV" | 标量投影 |
| `wpl.file_path` | `target_file_path` | 同左 | 标量投影 |
| `constant` | `source_finding_obj` 结构字段 | original_id/status/count | 装配 |
| `constant` | `extensions.profiles.endpoint_asset.subject_ref.ref_id` | "host::2811278348364284476" | 指向 roles.source |

## 三、不落库字段

| WPL 字段 | WPL 值 | 原因 |
|---|---|---|
| `os`/`release_id`/`build_version`/`main`/`describe`/`sys_space`/`core_number`/`memory_size`/`ie_version`/`computer_working_group`/`os_bit`/`nic_list`/`report_ipv6`/`state`/`activation`/`system_language` | 客户端元数据 | 终端资产画像，无检索价值 |
| `create_time`/`update_time` | 客户端登记/更新时间 | 非事件时间，无检索价值 |
| `login_account` | "zhangpeng15" | 终端登录账户，属于资产上下文；样例未建角色级 user（无独立用户主体动作） |
| `file_create_time` | 1731897537000 | 已落 `roles.target.file.created_time`（05:135 已注册） |
| `asset_id` | 2811278348364284476 | WPL 规则未抽，由 platform-context 补齐（见 wpl-missing-fields） |

## 四、未决问题

1. 06 枚举无恶意软件检出事件类型（无 malware/virus/detection 类），暂用 generic_event（#28）兜底；建议后续扩展 `malware_detection` 类型。
2. `trigger_mode`（2）、`result`（1）枚举含义待天擎字典确认。
3. `asset_id` 未在规则 json() 中直接抽取，样例由平台上下文按原始日志补齐（见 wpl-missing-fields）；建议规则补抽 `@asset_id`。
4. `guid` 非标准 GUID 格式（sddguid 前缀、短横线位置异常），作为 source_original_event_id 保留原值。

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
| `log_type` | `constant` | `constant` | "edr_antivirus_virus" | `—` | confirmed；日志身份 |
| `log_name` | `constant` | `constant` | "天擎病毒查杀日志" | `—` | confirmed；日志身份 |
| `record_kind` | `derived` | `constant` | `constant` | `—` | confirmed；检测结论 |
| `event_domain` | `derived` | `constant` | `constant` | `—` | confirmed；06 推荐值 |
| `event_type` | `derived` | `constant` | `constant` | `—` | confirmed；06 #28 兜底，06 无 malware 类型 |
| `operation` | `constant` | `constant` | `chars(None)` | `—` | confirmed；generic_event 无动作；06 severity 枚举 |
| `outcome` | `constant` | `constant` | "observed" | `—` | confirmed；generic_event 无动作；06 severity 枚举 |
| `severity` | `constant` | `constant` | "info" | `—` | confirmed；generic_event 无动作；06 severity 枚举 |
| `roles.source.ref_id` | `derived` | `derived.entity_ref(host, platform_context.asset_id)` | `derived.entity_ref(host, platform_context.asset_id)` | `—` | confirmed；三段式引用；asset_id 见 platform-context 与 wpl-missing-fields |
| `roles.target.ref_id` | `derived` | `derived.entity_ref(file, wpl.md5)` | `derived.entity_ref(file, wpl.md5)` | `—` | confirmed；三段式引用 |
| `observer_vendor` | `constant` | `constant` | "qax" | `—` | confirmed；产品身份 |
| `observer_product` | `constant` | `constant` | "tianqing" | `—` | confirmed；产品身份 |
| `source_finding_obj` | `derived` | `constant` | `constant` | `—` | confirmed；告警声明装配 |
| `extensions.profiles.endpoint_asset.subject_ref.ref_id` | `derived` | `derived.entity_ref(host, platform_context.asset_id)` | `derived.entity_ref(host, platform_context.asset_id)` | `—` | confirmed；指向 roles.source |
| `roles.source.host.id` | `context` | `platform_context.asset_id` | `platform_context.asset_id` | `—` | confirmed；WPL 缺口补齐（见 wpl-missing-fields） |
| `ingest_time` | `context` | `platform_context.ingest_time` | `read(ingest_time)` | `—` | confirmed；expected 事件中的平台上下文字段 |
| `parse_time` | `context` | `platform_context.parse_time` | `read(parse_time)` | `—` | confirmed；expected 事件中的平台上下文字段 |
| `data_src_category` | `constant` | `constant.data_src_category` | "endpoint_security" | `—` | confirmed；expected 事件确认的日志类型级常量 |

### 5.2 Content 区

| SDM 字段 | 规则类型 | WPL 字段 | 映射/赋值 | 未命中 | 状态与证据 |
|---|---|---|---|---|---|
| `source_original_event_id` | `projection` | `guid` | `wpl.guid` | `—` | confirmed；WPL 直接映射 |
| `source_host` | `projection` | `name` | `wpl.name` | `—` | confirmed；标量投影 |
| `target_file_path` | `projection` | `file_path` | `wpl.file_path` | `—` | confirmed；标量投影 |
| `occur_time` | `projection` | `file_alarm_time` | 1732493003000 | `—` | confirmed；19 位纳秒由 WPL time_timestamp 转毫秒，SDM 直接使用 WPL 值 |
| `source_finding.title` | `projection` | `virus_name` | "检出广告软件 Adware.Agent.30f0fd07" | `—` | confirmed；检出结论 |
| `source_finding.category.original` | `projection` | `virus_type` | "adware" | `—` | confirmed；病毒类型→原始分类 code |
| `roles.target.file.path` | `projection` | `file_path` | "C:\\Users\\zhangpeng15\\Desktop\\宏病毒样本sample\\宏病毒样本sample\\出品部门牌_Key.vbs" | `—` | confirmed；投影 target_file_path |
| `roles.target.file.created_time` | `projection` | `file_create_time` | 1731897537000 | `—` | confirmed；19 位纳秒由 WPL time_timestamp 转毫秒；05 目录 roles.target.file.created_time 已注册 |
| `roles.target.file.hashes.md5` | `projection` | `md5` | "b4b7b2baf26fc319ef817cb95d33ab59" | `—` | confirmed；检出文件 MD5 |
| `roles.target.file.hashes.sha1` | `projection` | `sha1` | "bf629dd7792044c8701d6939e66fe1e40fcba43d" | `—` | confirmed；检出文件 SHA1 |
| `source_finding.severity` | `projection` | `severity` | "0" | `—` | confirmed；原始严重度，0 不在 06 顶层枚举，保留原值 |
| `extensions.source_private.result` | `projection` | `result` | 1 | `—` | confirmed；删除成功，不进 outcome/finding.status |
| `extensions.source_private.trigger_mode` | `projection` | `trigger_mode` | 2 | `—` | confirmed；触发方式，枚举待确认 |
| `extensions.source_private.need_reboot` | `projection` | `need_reboot` | 0 | `—` | confirmed；是否需重启 |
| `extensions.source_private.scanners` | `projection` | `scanners` | "qce" | `—` | confirmed；查杀引擎 |
| `extensions.profiles.endpoint_asset.agent.id` | `projection` | `client_id` | "8424338-de7f6819c3625af3402bd64422d1400a" | `—` | confirmed；Agent ID |
| `extensions.profiles.endpoint_asset.agent.fingerprint_id` | `projection` | `mid` | "1909aacaa9d3411b9237145b0bada7ee" | `—` | confirmed；终端指纹 |
| `roles.source.host.name` | `projection` | `name` | "WIN-UMAG4B1GGKV" | `—` | confirmed；投影 source_host |
| `roles.source.host.ip` | `projection` | `report_ip` | "192.0.2.192" | `—` | confirmed；终端上报 IP |
| `roles.source.host.mac` | `projection` | `mac` | "00:00:5E:00:53:AC" | `—` | confirmed；分隔符归一 |
| `roles.source.host.domain` | `projection` | `domain` | "clinetsdddomain" | `—` | confirmed；主机域 |
| `extensions.profiles.endpoint_asset.ownership` | `projection` | `group_info` | "id=2814380010620583951 name=hy" | `—` | confirmed；终端分组，organization.id=asset_oid |

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
