# WPL → SDM Event 字段映射

> 样例：`customize_scan.expected-sdm-event.json`；WPL 字段 44 个；另有平台上下文与结构字段。

## 一、WPL 字段映射

| WPL 字段 | WPL 值 | SDM 落位 | expected 位置 | expected 值 | 说明 |
|---|---|---|---|---|---|
| `start_time` | 1617353766663 | `occur_time` | `occur_time` | 1617353766663 | 原始纳秒 1617353766663364600 由 WPL `time_timestamp` 转毫秒，SDM 直接用 |
| `guid` | "C0953102-F942-4739-AE97-62FD849E5F65" | `source_original_event_id` | `source_original_event_id` | 同左 | WPL 直接映射（标准 GUID） |
| `scan_type` | "customize_scan" | `extensions.source_private.scan_type` | `extensions_obj.source_private.scan_type` | 同左 | 扫描类型，无标准路径，私有暂存（未决 3） |
| `scanners` | "qce,qowl,qde,qre" | `extensions.source_private.scanners` | 同左 | 同左 | 引擎列表 |
| `result` | 4 | `extensions.source_private.result` | 同左 | 4 | 扫描结果枚举（未决 1） |
| `trigger_mode` | 0 | `extensions.source_private.trigger_mode` | 同左 | 0 | 触发方式（未决 2） |
| `time_used` | 17000000000 | `extensions.source_private.time_used` | 同左 | 同左 | 耗时（纳秒） |
| `scanned_files_count` | 2010 | `extensions.source_private.scanned_files_count` | 同左 | 2010 | 扫描文件数 |
| `threatens_count` | 0 | `extensions.source_private.threatens_count` | 同左 | 0 | 威胁数 |
| `killings_count` | 0 | `extensions.source_private.killings_count` | 同左 | 0 | 清除数 |
| `name` | "Test-shifang-Win7" | `roles.source.host.name` | `roles_obj.source.host.name` | 同左 | 终端主机名，投影 source_host |
| `report_ip` | "192.0.2.71" | `roles.source.host.ip` | `roles_obj.source.host.ip` | 同左 | 上报 IP |
| `mac` | "00-50-56-80-C8-49" | `roles.source.host.mac` | `roles_obj.source.host.mac` | "00:50:56:80:c8:49" | 分隔符/大小写归一 |
| `node_name` | "CRH" | `profiles.endpoint_asset.ownership.group.name` | `extensions_obj…` | 同左 | 分组名 |
| `node_id` | "2713465372446557376" | `profiles.endpoint_asset.ownership.group.id` | 同左 | 同左 | 分组 ID |
| `oid` | "100103" | `profiles.endpoint_asset.ownership.organization.id` | 同左 | 同左 | 组织 OID |
| `client_id` | "8863058-…" | `profiles.endpoint_asset.agent.id` | 同左 | 同左 | 客户端 ID |
| `mid` | "09d24a99…" | `profiles.endpoint_asset.agent.fingerprint_id` | 同左 | 同左 | 客户端指纹 |

## 二、不落库字段

| WPL 字段 | 原因 |
|---|---|
| `virus_name`/`virus_type`/`file_path`/`md5`/`sha1`/`file_alarm_time`/`file_create_time` | 本样例为自定义扫描无检出，空值不落库 |
| `need_reboot` | 哨兵值 0 |
| `os`/`release_id`/`build_version`/`main`/`describe`/`sys_space`/`core_number`/`memory_size`/`ie_version`/`computer_working_group`/`os_bit`/`nic_list`/`report_ipv6`/`state`/`activation`/`system_language`/`create_time`/`update_time`/`login_account`/`domain` | 资产画像元数据/登记时间，无检索价值 |
| `node_type`/`tree_id` | 分组树元数据，无检索价值 |

## 三、平台/派生字段

| 来源 | SDM 落位 | expected 值 | 说明 |
|---|---|---|---|
| `derived.sha256(tenant_id=''\|mapping_id\|guid)` | `event_id` | "evt-531bc368…" | 确定性哈希，前缀 evt- |
| `derived.entity_ref(host, platform_context.asset_id)` | `roles.source.ref_id` | "host::100103" | 三段式引用 |
| `platform_context.asset_id` | `roles.source.host.id` | "100103" | WPL 缺口补齐（见 wpl-missing-fields） |
| `constant` | `event_type`/`operation`/`outcome`/`severity` | scan_host/completed/observed/info | 06 #60；result 未确认故 outcome 保守 |
| `constant` | `record_kind`/`event_domain` | activity/threat | 扫描活动记录 |

## 四、未决问题

1. `result`（4）枚举含义待天擎字典确认。
2. `trigger_mode`（0）含义待确认。
3. 06 无 `scan_type` 路径，扫描类型暂存 source_private。

## 五、WPL/OML 编写规则

> WPL 只负责提取表中的 source 字段；Meta 和 Content 的赋值由 OML 按下表实现。
> `partial` 表示当前只有样例值或局部说明，不能视为完整厂商字典。

### 5.1 Meta 区

| SDM 字段 | 规则类型 | 输入/来源 | 赋值 | 未命中 | 状态与证据 |
|---|---|---|---|---|---|
| `event_id` | `derived` | `derived.sha256(tenant_id=''|mapping_id|source_original_event_id)` | `derived.sha256(tenant_id=''|mapping_id|source_original_event_id)` | `—` | confirmed；确定性哈希，前缀 evt- |
| `roles.source.ref_id` | `derived` | `derived.entity_ref(host, platform_context.asset_id)` | `derived.entity_ref(host, platform_context.asset_id)` | `—` | confirmed；三段式引用 |
| `extensions.profiles.endpoint_asset.subject_ref.ref_id` | `derived` | `derived.entity_ref(host, platform_context.asset_id)` | `derived.entity_ref(host, platform_context.asset_id)` | `—` | confirmed；指向 roles.source |
| `roles.source.host.id` | `context` | `platform_context.asset_id` | `platform_context.asset_id` | `—` | confirmed；WPL 缺口补齐（见 wpl-missing-fields） |
| `event_type` | `constant` | `constant` | "scan_host" | `—` | confirmed；06 #60；result 枚举未确认故 outcome 保守 |
| `operation` | `constant` | `constant` | "completed" | `—` | confirmed；06 #60；result 枚举未确认故 outcome 保守 |
| `outcome` | `constant` | `constant` | "observed" | `—` | confirmed；06 #60；result 枚举未确认故 outcome 保守 |
| `severity` | `constant` | `constant` | "info" | `—` | confirmed；06 #60；result 枚举未确认故 outcome 保守 |
| `extensions.source_private.scanned_files_count` | `derived` | `raw_log.scanned_files_count` | `raw_log.scanned_files_count` | `—` | confirmed；原始日志字段，规则 json() 未抽（见 wpl-missing-fields） |
| `extensions.source_private.threatens_count` | `derived` | `raw_log.threatens_count` | `raw_log.threatens_count` | `—` | confirmed；原始日志字段，规则未抽（见 wpl-missing-fields） |
| `extensions.source_private.killings_count` | `derived` | `raw_log.killings_count` | `raw_log.killings_count` | `—` | confirmed；原始日志字段，规则未抽（见 wpl-missing-fields） |
| `extensions.source_private.time_used` | `derived` | `raw_log.time_used` | `raw_log.time_used` | `—` | confirmed；原始日志字段，规则未抽（见 wpl-missing-fields） |
| `record_kind` | `constant` | `constant` | "activity" | `—` | confirmed；扫描活动记录，06 推荐域 |
| `event_domain` | `constant` | `constant` | "threat" | `—` | confirmed；扫描活动记录，06 推荐域 |
| `observer_vendor` | `constant` | `constant` | "qax" | `—` | confirmed；产品身份 |
| `observer_product` | `constant` | `constant` | "tianqing" | `—` | confirmed；产品身份 |
| `log_id` | `context` | `platform_context.log_id` | `read(log_id)` | `—` | confirmed；expected 事件中的平台上下文字段 |
| `tenant_id` | `context` | `platform_context.tenant_id` | `read(tenant_id)` | `—` | confirmed；expected 事件中的平台上下文字段 |
| `ingest_time` | `context` | `platform_context.ingest_time` | `read(ingest_time)` | `—` | confirmed；expected 事件中的平台上下文字段 |
| `parse_time` | `context` | `platform_context.parse_time` | `read(parse_time)` | `—` | confirmed；expected 事件中的平台上下文字段 |
| `data_src_instance_id` | `context` | `platform_context.data_src_instance_id` | `read(data_src_instance_id)` | `—` | confirmed；expected 事件中的平台上下文字段 |
| `schema_version` | `constant` | `constant.schema_version` | 2 | `—` | confirmed；expected 事件确认的日志类型级常量 |
| `data_src_vendor` | `constant` | `constant.data_src_vendor` | "qax" | `—` | confirmed；expected 事件确认的日志类型级常量 |
| `mapping_id` | `constant` | `constant.mapping_id` | "qax.tianqing.edr_antivirus_scan" | `—` | confirmed；expected 事件确认的日志类型级常量 |
| `data_src_product` | `constant` | `constant.data_src_product` | "tianqing" | `—` | confirmed；expected 事件确认的日志类型级常量 |
| `log_type` | `constant` | `constant.log_type` | "edr_antivirus_scan" | `—` | confirmed；expected 事件确认的日志类型级常量 |
| `data_src_category` | `constant` | `constant.data_src_category` | "endpoint_security" | `—` | confirmed；expected 事件确认的日志类型级常量 |
| `log_name` | `constant` | `constant.log_name` | "天擎病毒扫描日志" | `—` | confirmed；expected 事件确认的日志类型级常量 |

### 5.2 Content 区

| SDM 字段 | 规则类型 | WPL 字段 | 映射/赋值 | 未命中 | 状态与证据 |
|---|---|---|---|---|---|
| `source_host` | `projection` | `name` | `wpl.name` | `—` | confirmed；标量投影 |
| `occur_time` | `projection` | `start_time` | 1617353766663 | `—` | confirmed；WPL 纳秒→毫秒，SDM 直接用 |
| `source_original_event_id` | `projection` | `guid` | "C0953102-F942-4739-AE97-62FD849E5F65" | `—` | confirmed；WPL 直接映射 |
| `extensions.source_private.scan_type` | `projection` | `scan_type` | "customize_scan" | `—` | confirmed；扫描类型（无标准路径，私有暂存） |
| `extensions.source_private.scanners` | `projection` | `scanners` | "qce,qowl,qde,qre" | `—` | confirmed；引擎列表（私有） |
| `extensions.source_private.result` | `projection` | `result` | 4 | `—` | confirmed；扫描结果枚举（4 含义待确认，私有暂存） |
| `extensions.source_private.trigger_mode` | `projection` | `trigger_mode` | 0 | `—` | confirmed；触发方式（0 待确认） |
| `roles.source.host.name + source_host` | `projection` | `name` | "Test-shifang-Win7" | `—` | confirmed；终端主机名（标量投影） |
| `roles.source.host.ip` | `projection` | `report_ip` | "192.0.2.71" | `—` | confirmed；上报 IP |
| `roles.source.host.mac` | `projection` | `mac` | "00-50-56-80-C8-49" | `—` | confirmed；归一化 00-50-56-80-C8-49 → 00:50:56:80:c8:49 |
| `profiles.endpoint_asset.ownership.group.name` | `projection` | `node_name` | "CRH" | `—` | confirmed；分组名 |
| `profiles.endpoint_asset.ownership.group.id` | `projection` | `node_id` | "2713465372446557376" | `—` | confirmed；分组 ID |
| `profiles.endpoint_asset.ownership.organization.id` | `projection` | `oid` | "100103" | `—` | confirmed；组织 OID |
| `profiles.endpoint_asset.agent.id` | `projection` | `client_id` | "8863058-d816e136fa1a79d971206d99b1a1418f" | `—` | confirmed；客户端 ID |
| `profiles.endpoint_asset.agent.fingerprint_id` | `projection` | `mid` | "09d24a99dfe6f5d9bbf3e79865aa2d02a66158d59c1657d55a496cf15786df61" | `—` | confirmed；客户端指纹 |

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
