# WPL → SDM Event 字段映射

> 样例：`registry_set_value.expected-sdm-event.json`；WPL 字段 43 个，映射 36，不落库 7，排除 0；另有平台默认、派生及结构字段 37 项。
> SDM 落位为逻辑路径；expected 位置为该样例中的实际物理 JSON 路径。

## 一、映射字段

| WPL 字段 | WPL 值 | SDM 落位 | expected 位置 | expected 值 | 说明 |
|---|---|---|---|---|---|
| `asset_id` | "2868257359929541780" | `roles.source.host.id` | `roles_obj.source.host.id` | "2868257359929541780" | 按当前 expected 事件结构映射 |
| `asset_oid` | "2653788242175861718" | `extensions.profiles.endpoint_asset.ownership.organization.id` | `extensions_obj.profiles.endpoint_asset.ownership.organization.id` | "2653788242175861718" | 按当前 expected 事件结构映射 |
| `client_id` | "8558772-6b168d97c3f346a96ed4ecef42be407a" | `extensions.profiles.endpoint_asset.agent.id` | `extensions_obj.profiles.endpoint_asset.agent.id` | "8558772-6b168d97c3f346a96ed4ecef42be407a" | 按当前 expected 事件结构映射 |
| `computer_name` | "DESKTOP-EX02" | `roles.source.host.name` | `roles_obj.source.host.name` | "DESKTOP-EX02" | 按当前 expected 事件结构映射 |
| `event_date_creation` | 1732786708718 | `occur_time` | `occur_time` | 1732786708718 | 按当前 expected 事件结构映射 |
| `event_type` | "registry_set_value" | `event_type` | `event_type` | "registry_modification" | 按当前 expected 事件结构映射 |
| `gid` | "4f9c3833b800d1f7" | `extensions.profiles.endpoint_asset.ownership.group.id` | `extensions_obj.profiles.endpoint_asset.ownership.group.id` | "4f9c3833b800d1f7" | 按当前 expected 事件结构映射 |
| `group_name` | "未分组终端" | `extensions.profiles.endpoint_asset.ownership.group.name` | `extensions_obj.profiles.endpoint_asset.ownership.group.name` | "未分组终端" | 按当前 expected 事件结构映射 |
| `ip` | "192.0.2.206" | `roles.source.host.ip` | `roles_obj.source.host.ip` | "192.0.2.206" | 按当前 expected 事件结构映射 |
| `mac` | "00-00-5E-00-53-C6" | `roles.source.host.mac` | `roles_obj.source.host.mac` | "00:00:5E:00:53:CB" | 按当前 expected 事件结构映射 |
| `mid` | "1ca36f97756b33c2bf9139aab6ac36926903b9ec24e0009fae93fda96ded6898" | `extensions.profiles.endpoint_asset.agent.fingerprint_id` | `extensions_obj.profiles.endpoint_asset.agent.fingerprint_id` | "1ca36f97756b33c2bf9139aab6ac36926903b9ec24e0009fae93fda96ded6898" | 按当前 expected 事件结构映射 |
| `process_command_line` | "C:\\WINDOWS\\system32\\services.exe" | `roles.source.process.cmdline` | `roles_obj.source.process.cmdline` | "C:\\WINDOWS\\system32\\services.exe" | 按当前 expected 事件结构映射 |
| `process_guid` | "9b131f038a832de417c1fb69b7bed530" | `roles.source.process.uid` | `roles_obj.source.process.uid` | "9b131f038a832de417c1fb69b7bed530" | 按当前 expected 事件结构映射 |
| `process_id` | "720" | `roles.source.process.pid` | `roles_obj.source.process.pid` | "720" | 按当前 expected 事件结构映射 |
| `process_internal_name` | "services.exe" | `roles.source.process.file.internal_name` | `roles_obj.source.process.file.internal_name` | "services.exe" | 按当前 expected 事件结构映射 |
| `process_md5` | "4eacbe64bb1e7d58e8a26340ed1c7cbd" | `roles.source.process.file.hashes.md5` | `roles_obj.source.process.file.hashes.md5` | "4eacbe64bb1e7d58e8a26340ed1c7cbd" | 按当前 expected 事件结构映射 |
| `process_name` | "services.exe" | `roles.source.process.name` | `roles_obj.source.process.name` | "services.exe" | 按当前 expected 事件结构映射 |
| `process_original_name` | "services.exe" | `roles.source.process.file.original_name` | `roles_obj.source.process.file.original_name` | "services.exe" | 按当前 expected 事件结构映射 |
| `process_parent_command_line` | "wininit.exe" | `roles.related[0].process.cmdline` | `roles_obj.related[0].process.cmdline` | "wininit.exe" | 按当前 expected 事件结构映射 |
| `process_parent_internal_name` | "WinInit" | `roles.related[0].process.file.internal_name` | `roles_obj.related[0].process.file.internal_name` | "WinInit" | 按当前 expected 事件结构映射 |
| `process_parent_name` | "wininit.exe" | `roles.related[0].process.name` | `roles_obj.related[0].process.name` | "wininit.exe" | 按当前 expected 事件结构映射 |
| `process_parent_original_name` | "WinInit.exe" | `roles.related[0].process.file.original_name` | `roles_obj.related[0].process.file.original_name` | "WinInit.exe" | 按当前 expected 事件结构映射 |
| `process_parent_path` | "C:\\Windows\\System32\\wininit.exe" | `roles.related[0].process.path` | `roles_obj.related[0].process.path` | "C:\\Windows\\System32\\wininit.exe" | 按当前 expected 事件结构映射 |
| `process_parent_sign` | "Microsoft Windows Publisher" | `roles.related[0].process.file.signatures[0].signer` | `roles_obj.related[0].process.file.signatures[0].signer` | "Microsoft Windows Publisher" | 按当前 expected 事件结构映射 |
| `process_path` | "C:\\Windows\\System32\\services.exe" | `roles.source.process.path` | `roles_obj.source.process.path` | "C:\\Windows\\System32\\services.exe" | 按当前 expected 事件结构映射 |
| `process_sha1` | "6703d48349de8c836c0eaffac5cfac7679da7f60" | `roles.source.process.file.hashes.sha1` | `roles_obj.source.process.file.hashes.sha1` | "6703d48349de8c836c0eaffac5cfac7679da7f60" | 按当前 expected 事件结构映射 |
| `process_sign` | "Microsoft Windows Publisher" | `roles.source.process.file.signatures[0].signer` | `roles_obj.source.process.file.signatures[0].signer` | "Microsoft Windows Publisher" | 按当前 expected 事件结构映射 |
| `process_user` | "NT AUTHORITY\\SYSTEM" | `roles.source.process.user.name` | `roles_obj.source.process.user.name` | "NT AUTHORITY\\SYSTEM" | 按当前 expected 事件结构映射 |
| `registry_key_path` | "\\REGISTRY\\MACHINE\\SYSTEM\\ControlSet001\\Services\\wuauserv" | `facets.registry.key.path` | `facets_obj.registry.key.path` | "\\REGISTRY\\MACHINE\\SYSTEM\\ControlSet001\\Services\\wuauserv" | 按当前 expected 事件结构映射 |
| `registry_value_details` | "2" | `facets.registry.value.previous.data` | `facets_obj.registry.value.previous.data` | "2" | 按字段命名候选解释为变更前数据，需厂商说明确认 |
| `registry_value_details_new` | "2" | `facets.registry.value.current.data` | `facets_obj.registry.value.current.data` | "2" | 按字段命名候选解释为变更后数据，需厂商说明确认 |
| `registry_value_name` | "Start" | `facets.registry.value.name` | `facets_obj.registry.value.name` | "Start" | 按当前 expected 事件结构映射 |
| `registry_value_size` | 4 | `facets.registry.value.previous.size` | `facets_obj.registry.value.previous.size` | 4 | 按当前 expected 事件结构映射 |
| `registry_value_size_new` | 4 | `facets.registry.value.current.size` | `facets_obj.registry.value.current.size` | 4 | 按当前 expected 事件结构映射 |
| `registry_value_type` | "4" | `facets.registry.value.type` | `facets_obj.registry.value.type` | "reg_dword" | 按 Windows 注册表类型代码转换；当前值 4 映射为 reg_dword |
| `uuid` | "265DDF13-2B2B-4B3E-8F5A-406EA31144B3" | `source_original_event_id` | `source_original_event_id` | "265DDF13-2B2B-4B3E-8F5A-406EA31144B3" | 按当前 expected 事件结构映射 |

## 二、不落库字段

| WPL 字段 | WPL 值 | 原因 |
|---|---|---|
| `custom_group_paths` | "" | 分组路径原始串不进入事件对象；原值保留在 raw_msg |
| `os_type` | 1 | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `registry_key_path_renamed` | "" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `report_ip` | "203.0.113.45" | 疑似 Agent 上报链路地址；与终端 IP 不一致时不作为事件 source IP，原值保留在 raw_msg |
| `report_ipv6` | "" | Agent 上报链路 IPv6；当前为空或语义未确认，暂不落库 |
| `timestamp` | 1732786668000 | 条件回退字段：仅 event_date_creation 缺失或无效时用于 occur_time；本样例未采用 |
| `type` | "registry_changes" | 仅用于 WPL 路由，稳定日志类型已由 log_type 表达；原值保留在 raw_msg |

## 四、平台默认、派生及结构字段

| 来源 | SDM 落位 | expected 值 | 赋值责任与说明 |
|---|---|---|---|
| `platform_context.tenant_id` | `tenant_id` | "" | 由平台上下文提供 |
| `derived.sha256('|'+mapping_id+'|'+source_original_event_id)` | `event_id` | "evt-3c02cc1ed1ee774725ec278f86bd465b7f09f76273674209679f694b3440ed41" | 按确定性规则 sha256('|'+mapping_id+'|'+source_original_event_id) 派生 |
| `platform_context.log_id` | `log_id` | "log-tianqing-reg-change-0001" | 由平台上下文提供 |
| `raw_log_input` | `raw_msg` | "{\"type\":\"registry_changes\",\"event_type\":\"registry_set_value\",\"uuid\":\"265DDF13-2B2B-4B3E-8F5A-406EA31144B3\",\"process_name\":\"services.exe\",\"registry_key_path\":\"\\\\REGISTRY\\\\MACHINE\\\\SYSTEM\\\\ControlSet001\\\\Services\\\\wuauserv\",\"registry_value_name\":\"Start\",\"registry_value_details_new\":\"2\"}" | 由原始日志接入层保存，不由 OML 拼装 |
| `platform_context.ingest_time` | `ingest_time` | 1732786709001 | 由平台上下文提供 |
| `platform_context.parse_time` | `parse_time` | 1732786709120 | 由平台上下文提供 |
| `constant.sdm_schema_version` | `schema_version` | 2 | 使用平台/映射规则常量 sdm_schema_version |
| `constant.mapping_id` | `mapping_id` | "qax.tianqing.edr_reg_change" | 使用平台/映射规则常量 mapping_id |
| `constant.mapping_vendor` | `data_src_vendor` | "qax" | 使用平台/映射规则常量 mapping_vendor |
| `constant.mapping_product` | `data_src_product` | "tianqing" | 使用平台/映射规则常量 mapping_product |
| `constant.mapping_category` | `data_src_category` | "endpoint_security" | 使用平台/映射规则常量 mapping_category |
| `platform_context.data_src_instance_id` | `data_src_instance_id` | "collector-tianqing-poc-01" | 由平台上下文提供 |
| `constant.log_type` | `log_type` | "edr_reg_change" | 使用平台/映射规则常量 log_type |
| `constant.log_name` | `log_name` | "天擎 EDR 注册表变更" | 使用平台/映射规则常量 log_name |
| `constant.record_kind` | `record_kind` | "activity" | 使用平台/映射规则常量 record_kind |
| `constant.event_domain` | `event_domain` | "system" | 使用平台/映射规则常量 event_domain |
| `derived.enum_projection` | `outcome` | "observed" | 由 WPL 枚举或日志语义转换为 SDM 标准值 |
| `constant.default_severity` | `severity` | "info" | 当前日志类型未提供标准 severity，按映射默认值 info 装配 |
| `wpl.process_user` | `source_user` | "NT AUTHORITY\\SYSTEM" | 由 WPL 字段 process_user 投影或转换后赋值 |
| `wpl.computer_name` | `source_host` | "DESKTOP-EX02" | 由 WPL 字段 computer_name 投影或转换后赋值 |
| `constant.mapping_vendor` | `observer_vendor` | "qax" | 使用平台/映射规则常量 mapping_vendor |
| `constant.mapping_product` | `observer_product` | "tianqing" | 使用平台/映射规则常量 mapping_product |
| `derived.entity_ref` | `roles.source.ref_id` | "host_2868257359929541780" | 按确定性规则 entity_ref 派生 |
| `constant.entity_type` | `roles.source.entity_type` | "host" | 使用平台/映射规则常量 entity_type |
| `derived.entity_ref` | `roles.target.ref_id` | "resource_registry_wuauserv_start" | 按确定性规则 entity_ref 派生 |
| `constant.entity_type` | `roles.target.entity_type` | "resource" | 使用平台/映射规则常量 entity_type |
| `wpl.registry_value_name` | `roles.target.resource.name` | "Start" | 由 WPL 字段 registry_value_name 投影或转换后赋值 |
| `constant.entity_type` | `roles.target.resource.type` | "registry_value" | 使用平台/映射规则常量 entity_type |
| `derived.registry_value_id` | `roles.target.resource.external_id` | "\\REGISTRY\\MACHINE\\SYSTEM\\ControlSet001\\Services\\wuauserv\\Start" | 由 WPL 注册表键路径与值名称拼接形成稳定外部标识 |
| `constant.mapping_product` | `roles.observer.product.name` | "tianqing" | 使用平台/映射规则常量 mapping_product |
| `constant.mapping_vendor` | `roles.observer.device.vendor` | "qax" | 使用平台/映射规则常量 mapping_vendor |
| `derived.entity_ref` | `roles.related[0].ref_id` | "process_parent_wininit_01" | 按确定性规则 entity_ref 派生 |
| `constant.entity_type` | `roles.related[0].entity_type` | "process" | 使用平台/映射规则常量 entity_type |
| `constant.relation_type` | `roles.related[0].relation_type` | "parent_process" | 使用平台/映射规则常量 relation_type |
| `constant.sdm_schema_version` | `extensions.schema_version` | 2 | 使用平台/映射规则常量 sdm_schema_version |
| `derived.entity_ref` | `extensions.profiles.endpoint_asset.subject_ref.ref_id` | "host_2868257359929541780" | 按确定性规则 entity_ref 派生 |
| `platform_context.env_version` | `extensions.profiles.endpoint_asset.agent.version` | "edr-8.0" | 由平台上下文提供 |

## 五、WPL/OML 编写规则

> WPL 只负责提取表中的 source 字段；Meta 和 Content 的赋值由 OML 按下表实现。
> `partial` 表示当前只有样例值或局部说明，不能视为完整厂商字典。

### 5.1 Meta 区

| SDM 字段 | 规则类型 | 输入/来源 | 赋值 | 未命中 | 状态与证据 |
|---|---|---|---|---|---|
| `tenant_id` | `context` | `platform_context.tenant_id` | `platform_context.tenant_id` | `—` | confirmed；由平台上下文提供 |
| `event_id` | `derived` | `derived.sha256('|'+mapping_id+'|'+source_original_event_id)` | `derived.sha256('|'+mapping_id+'|'+source_original_event_id)` | `—` | confirmed；按确定性规则 sha256('|'+mapping_id+'|'+source_original_event_id) 派生 |
| `log_id` | `context` | `platform_context.log_id` | `platform_context.log_id` | `—` | confirmed；由平台上下文提供 |
| `schema_version` | `constant` | `constant.sdm_schema_version` | 2 | `—` | confirmed；使用平台/映射规则常量 sdm_schema_version |
| `mapping_id` | `constant` | `constant.mapping_id` | "qax.tianqing.edr_reg_change" | `—` | confirmed；使用平台/映射规则常量 mapping_id |
| `data_src_vendor` | `constant` | `constant.mapping_vendor` | "qax" | `—` | confirmed；使用平台/映射规则常量 mapping_vendor |
| `data_src_product` | `constant` | `constant.mapping_product` | "tianqing" | `—` | confirmed；使用平台/映射规则常量 mapping_product |
| `data_src_category` | `constant` | `constant.mapping_category` | "endpoint_security" | `—` | confirmed；使用平台/映射规则常量 mapping_category |
| `data_src_instance_id` | `context` | `platform_context.data_src_instance_id` | `platform_context.data_src_instance_id` | `—` | confirmed；由平台上下文提供 |
| `log_type` | `constant` | `constant.log_type` | "edr_reg_change" | `—` | confirmed；使用平台/映射规则常量 log_type |
| `log_name` | `constant` | `constant.log_name` | "天擎 EDR 注册表变更" | `—` | confirmed；使用平台/映射规则常量 log_name |
| `record_kind` | `constant` | `constant.record_kind` | "activity" | `—` | confirmed；使用平台/映射规则常量 record_kind |
| `event_domain` | `constant` | `constant.event_domain` | "system" | `—` | confirmed；使用平台/映射规则常量 event_domain |
| `severity` | `constant` | `constant.default_severity` | "info" | `—` | confirmed；当前日志类型未提供标准 severity，按映射默认值 info 装配 |
| `observer_vendor` | `constant` | `constant.mapping_vendor` | "qax" | `—` | confirmed；使用平台/映射规则常量 mapping_vendor |
| `observer_product` | `constant` | `constant.mapping_product` | "tianqing" | `—` | confirmed；使用平台/映射规则常量 mapping_product |
| `roles.source.ref_id` | `derived` | `derived.entity_ref` | `derived.entity_ref` | `—` | confirmed；按确定性规则 entity_ref 派生 |
| `roles.source.entity_type` | `constant` | `constant.entity_type` | "host" | `—` | confirmed；使用平台/映射规则常量 entity_type |
| `roles.target.ref_id` | `derived` | `derived.entity_ref` | `derived.entity_ref` | `—` | confirmed；按确定性规则 entity_ref 派生 |
| `roles.target.entity_type` | `constant` | `constant.entity_type` | "resource" | `—` | confirmed；使用平台/映射规则常量 entity_type |
| `roles.target.resource.type` | `constant` | `constant.entity_type` | "registry_value" | `—` | confirmed；使用平台/映射规则常量 entity_type |
| `roles.target.resource.external_id` | `derived` | `derived.registry_value_id` | `derived.registry_value_id` | `—` | confirmed；由 WPL 注册表键路径与值名称拼接形成稳定外部标识 |
| `roles.observer.product.name` | `constant` | `constant.mapping_product` | "tianqing" | `—` | confirmed；使用平台/映射规则常量 mapping_product |
| `roles.observer.device.vendor` | `constant` | `constant.mapping_vendor` | "qax" | `—` | confirmed；使用平台/映射规则常量 mapping_vendor |
| `roles.related[0].ref_id` | `derived` | `derived.entity_ref` | `derived.entity_ref` | `—` | confirmed；按确定性规则 entity_ref 派生 |
| `roles.related[0].entity_type` | `constant` | `constant.entity_type` | "process" | `—` | confirmed；使用平台/映射规则常量 entity_type |
| `roles.related[0].relation_type` | `constant` | `constant.relation_type` | "parent_process" | `—` | confirmed；使用平台/映射规则常量 relation_type |
| `extensions.profiles.endpoint_asset.subject_ref.ref_id` | `derived` | `derived.entity_ref` | `derived.entity_ref` | `—` | confirmed；按确定性规则 entity_ref 派生 |
| `extensions.profiles.endpoint_asset.agent.version` | `context` | `platform_context.env_version` | `platform_context.env_version` | `—` | confirmed；由平台上下文提供 |
| `outcome` | `constant` | `log_semantics` | "observed" | `—` | confirmed；由该日志类型的事件事实确定，不是来源枚举转换 |
| `ingest_time` | `context` | `platform_context.ingest_time` | `read(ingest_time)` | `—` | confirmed；expected 事件中的平台上下文字段 |
| `parse_time` | `context` | `platform_context.parse_time` | `read(parse_time)` | `—` | confirmed；expected 事件中的平台上下文字段 |

### 5.2 Content 区

| SDM 字段 | 规则类型 | WPL 字段 | 映射/赋值 | 未命中 | 状态与证据 |
|---|---|---|---|---|---|
| `outcome` | `dictionary` | `derived.enum_projection` | — | `preserve_in_extension_and_review` | partial；由 WPL 枚举或日志语义转换为 SDM 标准值 |
| `source_user` | `projection` | `process_user` | `wpl.process_user` | `—` | confirmed；由 WPL 字段 process_user 投影或转换后赋值 |
| `source_host` | `projection` | `computer_name` | `wpl.computer_name` | `—` | confirmed；由 WPL 字段 computer_name 投影或转换后赋值 |
| `roles.target.resource.name` | `projection` | `registry_value_name` | `wpl.registry_value_name` | `—` | confirmed；由 WPL 字段 registry_value_name 投影或转换后赋值 |
| `roles.source.host.id` | `projection` | `asset_id` | "2868257359929541780" | `—` | confirmed；按当前 expected 事件结构映射 |
| `extensions.profiles.endpoint_asset.ownership.organization.id` | `projection` | `asset_oid` | "2653788242175861718" | `—` | confirmed；按当前 expected 事件结构映射 |
| `extensions.profiles.endpoint_asset.agent.id` | `projection` | `client_id` | "8558772-6b168d97c3f346a96ed4ecef42be407a" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.source.host.name` | `projection` | `computer_name` | "DESKTOP-EX02" | `—` | confirmed；按当前 expected 事件结构映射 |
| `occur_time` | `projection` | `event_date_creation` | 1732786708718 | `—` | confirmed；按当前 expected 事件结构映射 |
| `extensions.profiles.endpoint_asset.ownership.group.id` | `projection` | `gid` | "4f9c3833b800d1f7" | `—` | confirmed；按当前 expected 事件结构映射 |
| `extensions.profiles.endpoint_asset.ownership.group.name` | `projection` | `group_name` | "未分组终端" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.source.host.ip` | `projection` | `ip` | "192.0.2.206" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.source.host.mac` | `projection` | `mac` | "00:00:5E:00:53:CB" | `—` | confirmed；按当前 expected 事件结构映射 |
| `extensions.profiles.endpoint_asset.agent.fingerprint_id` | `projection` | `mid` | "1ca36f97756b33c2bf9139aab6ac36926903b9ec24e0009fae93fda96ded6898" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.source.process.cmdline` | `projection` | `process_command_line` | "C:\\WINDOWS\\system32\\services.exe" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.source.process.uid` | `projection` | `process_guid` | "9b131f038a832de417c1fb69b7bed530" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.source.process.pid` | `projection` | `process_id` | "720" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.source.process.file.internal_name` | `projection` | `process_internal_name` | "services.exe" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.source.process.file.hashes.md5` | `projection` | `process_md5` | "4eacbe64bb1e7d58e8a26340ed1c7cbd" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.source.process.name` | `projection` | `process_name` | "services.exe" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.source.process.file.original_name` | `projection` | `process_original_name` | "services.exe" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.related[0].process.cmdline` | `projection` | `process_parent_command_line` | "wininit.exe" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.related[0].process.file.internal_name` | `projection` | `process_parent_internal_name` | "WinInit" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.related[0].process.name` | `projection` | `process_parent_name` | "wininit.exe" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.related[0].process.file.original_name` | `projection` | `process_parent_original_name` | "WinInit.exe" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.related[0].process.path` | `projection` | `process_parent_path` | "C:\\Windows\\System32\\wininit.exe" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.related[0].process.file.signatures[0].signer` | `projection` | `process_parent_sign` | "Microsoft Windows Publisher" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.source.process.path` | `projection` | `process_path` | "C:\\Windows\\System32\\services.exe" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.source.process.file.hashes.sha1` | `projection` | `process_sha1` | "6703d48349de8c836c0eaffac5cfac7679da7f60" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.source.process.file.signatures[0].signer` | `projection` | `process_sign` | "Microsoft Windows Publisher" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.source.process.user.name` | `projection` | `process_user` | "NT AUTHORITY\\SYSTEM" | `—` | confirmed；按当前 expected 事件结构映射 |
| `facets.registry.key.path` | `projection` | `registry_key_path` | "\\REGISTRY\\MACHINE\\SYSTEM\\ControlSet001\\Services\\wuauserv" | `—` | confirmed；按当前 expected 事件结构映射 |
| `facets.registry.value.previous.data` | `projection` | `registry_value_details` | "2" | `—` | confirmed；按字段命名候选解释为变更前数据，需厂商说明确认 |
| `facets.registry.value.current.data` | `projection` | `registry_value_details_new` | "2" | `—` | confirmed；按字段命名候选解释为变更后数据，需厂商说明确认 |
| `facets.registry.value.name` | `projection` | `registry_value_name` | "Start" | `—` | confirmed；按当前 expected 事件结构映射 |
| `facets.registry.value.previous.size` | `projection` | `registry_value_size` | 4 | `—` | confirmed；按当前 expected 事件结构映射 |
| `facets.registry.value.current.size` | `projection` | `registry_value_size_new` | 4 | `—` | confirmed；按当前 expected 事件结构映射 |
| `facets.registry.value.type` | `projection` | `registry_value_type` | "reg_dword" | `—` | confirmed；按 Windows 注册表类型代码转换；当前值 4 映射为 reg_dword |
| `source_original_event_id` | `projection` | `uuid` | "265DDF13-2B2B-4B3E-8F5A-406EA31144B3" | `—` | confirmed；按当前 expected 事件结构映射 |
| `event_type` | `dictionary` | `event_type` | "registry_set_value" -> "registry_modification" | `preserve_in_extension_and_review` | partial；按当前 expected 事件结构映射 |

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
