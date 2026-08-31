# WPL → SDM Event 字段映射

> 样例：`wmi_execute.expected-sdm-event.json`；WPL 字段 40 个，映射 30，不落库 10，排除 0；另有平台默认、派生及结构字段 38 项。
> SDM 落位为逻辑路径；expected 位置为该样例中的实际物理 JSON 路径。

## 一、映射字段

| WPL 字段 | WPL 值 | SDM 落位 | expected 位置 | expected 值 | 说明 |
|---|---|---|---|---|---|
| `asset_oid` | "2653788242175861718" | `extensions.profiles.endpoint_asset.ownership.organization.id` | `extensions_obj.profiles.endpoint_asset.ownership.organization.id` | "2653788242175861718" | 按当前 expected 事件结构映射 |
| `event_date_creation` | 1733932552630 | `occur_time` | `occur_time` | 1733932552630 | 按当前 expected 事件结构映射 |
| `process_parent_command_line` | "C:\\WINDOWS\\system32\\services.exe" | `roles.related[0].process.cmdline` | `roles_obj.related[0].process.cmdline` | "C:\\WINDOWS\\system32\\services.exe" | 按当前 expected 事件结构映射 |
| `process_parent_internal_name` | "services.exe" | `roles.related[0].process.file.internal_name` | `roles_obj.related[0].process.file.internal_name` | "services.exe" | 按当前 expected 事件结构映射 |
| `process_parent_name` | "services.exe" | `roles.related[0].process.name` | `roles_obj.related[0].process.name` | "services.exe" | 按当前 expected 事件结构映射 |
| `process_parent_original_name` | "services.exe" | `roles.related[0].process.file.original_name` | `roles_obj.related[0].process.file.original_name` | "services.exe" | 按当前 expected 事件结构映射 |
| `process_parent_sign` | "Microsoft Windows Publisher" | `roles.related[0].process.file.signatures[0].signer` | `roles_obj.related[0].process.file.signatures[0].signer` | "Microsoft Windows Publisher" | 按当前 expected 事件结构映射 |
| `process_sha1` | "e4e3f6bbad17b41a42687b3d75ade4a10b0870ec" | `roles.carriers[0].process.file.hashes.sha1` | `roles_obj.carriers[0].process.file.hashes.sha1` | "e4e3f6bbad17b41a42687b3d75ade4a10b0870ec" | 按当前 expected 事件结构映射 |
| `uuid` | "0C295907-0423-46AC-B6E4-8F171BA7D60A" | `source_original_event_id` | `source_original_event_id` | "0C295907-0423-46AC-B6E4-8F171BA7D60A" | 按当前 expected 事件结构映射 |
| `wmi_filter_wql` | "SELECT * FROM __InstanceOperationEvent WHERE TargetInstance ISA 'AntiVirusProduct' OR TargetInstance ISA 'FirewallProduct' OR TargetInstance ISA 'AntiSpywareProduct'" | `extensions.source_private.filter_wql` | `extensions_obj.source_private.filter_wql` | "SELECT * FROM __InstanceOperationEvent WHERE TargetInstance ISA 'AntiVirusProduct' OR TargetInstance ISA 'FirewallProduct' OR TargetInstance ISA 'AntiSpywareProduct'" | WMI 查询原文；当前不据此构造虚假的文件、网络或进程目标 |
| `computer_name` | "DESKTOP-NGMF7JI" | `roles.source.host.name` | `roles_obj.source.host.name` | "DESKTOP-NGMF7JI" | 按当前 expected 事件结构映射 |
| `gid` | "4f9c3833b800d1f7" | `extensions.profiles.endpoint_asset.ownership.group.id` | `extensions_obj.profiles.endpoint_asset.ownership.group.id` | "4f9c3833b800d1f7" | 按当前 expected 事件结构映射 |
| `process_command_line` | "C:\\WINDOWS\\system32\\svchost.exe -k netsvcs -p -s Winmgmt" | `roles.carriers[0].process.cmdline` | `roles_obj.carriers[0].process.cmdline` | "C:\\WINDOWS\\system32\\svchost.exe -k netsvcs -p -s Winmgmt" | 按当前 expected 事件结构映射 |
| `process_internal_name` | "svchost.exe" | `roles.carriers[0].process.file.internal_name` | `roles_obj.carriers[0].process.file.internal_name` | "svchost.exe" | 按当前 expected 事件结构映射 |
| `process_original_name` | "svchost.exe" | `roles.carriers[0].process.file.original_name` | `roles_obj.carriers[0].process.file.original_name` | "svchost.exe" | 按当前 expected 事件结构映射 |
| `process_parent_path` | "C:\\Windows\\System32\\services.exe" | `roles.related[0].process.path` | `roles_obj.related[0].process.path` | "C:\\Windows\\System32\\services.exe" | 按当前 expected 事件结构映射 |
| `process_sign` | "Microsoft Windows Publisher" | `roles.carriers[0].process.file.signatures[0].signer` | `roles_obj.carriers[0].process.file.signatures[0].signer` | "Microsoft Windows Publisher" | 按当前 expected 事件结构映射 |
| `process_user` | "NT AUTHORITY\\SYSTEM" | `roles.carriers[0].process.user.name` | `roles_obj.carriers[0].process.user.name` | "NT AUTHORITY\\SYSTEM" | 按当前 expected 事件结构映射 |
| `asset_id` | "2868257359929541780" | `roles.source.host.id` | `roles_obj.source.host.id` | "2868257359929541780" | 按当前 expected 事件结构映射 |
| `client_id` | "8558772-6b168d97c3f346a96ed4ecef42be407a" | `extensions.profiles.endpoint_asset.agent.id` | `extensions_obj.profiles.endpoint_asset.agent.id` | "8558772-6b168d97c3f346a96ed4ecef42be407a" | 按当前 expected 事件结构映射 |
| `event_type` | "wmi_execute" | `event_type` | `event_type` | "process_uncategorized" | wmi_execute 暂映射为 process_uncategorized；没有受控 operation 时留空 |
| `group_name` | "未分组终端" | `extensions.profiles.endpoint_asset.ownership.group.name` | `extensions_obj.profiles.endpoint_asset.ownership.group.name` | "未分组终端" | 按当前 expected 事件结构映射 |
| `mac` | "00-50-56-81-E3-7E" | `roles.source.host.mac` | `roles_obj.source.host.mac` | "00:50:56:81:e3:7e" | 按当前 expected 事件结构映射 |
| `mid` | "1ca36f97756b33c2bf9139aab6ac36926903b9ec24e0009fae93fda96ded6898" | `extensions.profiles.endpoint_asset.agent.fingerprint_id` | `extensions_obj.profiles.endpoint_asset.agent.fingerprint_id` | "1ca36f97756b33c2bf9139aab6ac36926903b9ec24e0009fae93fda96ded6898" | 按当前 expected 事件结构映射 |
| `process_guid` | "e3c04c6237c7e24cf9566bdb5bbf3b5a" | `roles.carriers[0].process.uid` | `roles_obj.carriers[0].process.uid` | "e3c04c6237c7e24cf9566bdb5bbf3b5a" | 按当前 expected 事件结构映射 |
| `process_id` | "2360" | `roles.carriers[0].process.pid` | `roles_obj.carriers[0].process.pid` | "2360" | 按当前 expected 事件结构映射 |
| `process_md5` | "7469cc568ad6821fd9d925542730a7d8" | `roles.carriers[0].process.file.hashes.md5` | `roles_obj.carriers[0].process.file.hashes.md5` | "7469cc568ad6821fd9d925542730a7d8" | 按当前 expected 事件结构映射 |
| `process_name` | "svchost.exe" | `roles.carriers[0].process.name` | `roles_obj.carriers[0].process.name` | "svchost.exe" | 按当前 expected 事件结构映射 |
| `process_path` | "C:\\Windows\\System32\\svchost.exe" | `roles.carriers[0].process.path` | `roles_obj.carriers[0].process.path` | "C:\\Windows\\System32\\svchost.exe" | 按当前 expected 事件结构映射 |
| `ip` | "192.0.2.206" | `roles.source.host.ip` | `roles_obj.source.host.ip` | "192.0.2.206" | 按当前 expected 事件结构映射 |

## 二、不落库字段

| WPL 字段 | WPL 值 | 原因 |
|---|---|---|
| `custom_group_paths` | "" | 分组路径原始串不进入事件对象；原值保留在 raw_msg |
| `timestamp` | 1733932530000 | 条件回退字段：仅 event_date_creation 缺失或无效时用于 occur_time；本样例未采用 |
| `type` | "wmi_event" | 仅用于 WPL 路由，稳定日志类型已由 log_type 表达；原值保留在 raw_msg |
| `wmi_consumer_destination` | "" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `wmi_consumer_name` | "" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `wmi_consumer_type` | "" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `wmi_filter_name` | "" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `wmi_namespace` | "" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `wmi_operation` | "" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `report_ip` | "203.0.113.45" | 疑似 Agent 上报链路地址；与终端 IP 不一致时不作为事件 source IP，原值保留在 raw_msg |

## 四、平台默认、派生及结构字段

| 来源 | SDM 落位 | expected 值 | 赋值责任与说明 |
|---|---|---|---|
| `platform_context.tenant_id` | `tenant_id` | "" | 由平台上下文提供 |
| `derived.sha256('|'+mapping_id+'|'+source_original_event_id)` | `event_id` | "evt-47ff97752b53a3457b726e32c3090ee710da8da90a976cf64f0cfd8ad6b2423c" | 按确定性规则 sha256('|'+mapping_id+'|'+source_original_event_id) 派生 |
| `platform_context.log_id` | `log_id` | "log-tianqing-wmi-event-0001" | 由平台上下文提供 |
| `raw_log_input` | `raw_msg` | "{\"type\":\"wmi_event\",\"event_type\":\"wmi_execute\",\"uuid\":\"0C295907-0423-46AC-B6E4-8F171BA7D60A\",\"wmi_filter_wql\":\"SELECT * FROM __InstanceOperationEvent WHERE TargetInstance ISA 'AntiVirusProduct' OR TargetInstance ISA 'FirewallProduct' OR TargetInstance ISA 'AntiSpywareProduct'\",\"process_name\":\"svchost.exe\"}" | 接入层原样保存原始日志 |
| `platform_context.ingest_time` | `ingest_time` | 1733932554001 | 由平台上下文提供 |
| `platform_context.parse_time` | `parse_time` | 1733932554120 | 由平台上下文提供 |
| `constant.sdm_schema_version` | `schema_version` | 2 | 使用平台/映射规则常量 sdm_schema_version |
| `constant.mapping_id` | `mapping_id` | "qax.tianqing.edr_wmi_event" | 使用平台/映射规则常量 mapping_id |
| `constant.mapping_vendor` | `data_src_vendor` | "qax" | 使用平台/映射规则常量 mapping_vendor |
| `constant.mapping_product` | `data_src_product` | "tianqing" | 使用平台/映射规则常量 mapping_product |
| `constant.mapping_category` | `data_src_category` | "endpoint_security" | 使用平台/映射规则常量 mapping_category |
| `platform_context.data_src_instance_id` | `data_src_instance_id` | "collector-tianqing-poc-01" | 由平台上下文提供 |
| `constant.log_type` | `log_type` | "edr_wmi_event" | 使用平台/映射规则常量 log_type |
| `constant.log_name` | `log_name` | "天擎 EDR WMI 事件" | 使用平台/映射规则常量 log_name |
| `constant.record_kind` | `record_kind` | "activity" | 使用平台/映射规则常量 record_kind |
| `constant.event_domain` | `event_domain` | "endpoint" | 使用平台/映射规则常量 event_domain |
| `derived.enum_projection` | `outcome` | "observed" | 由 WPL 枚举或日志语义转换为 SDM 标准值 |
| `constant.default_severity` | `severity` | "info" | 当前日志类型未提供标准 severity，按映射默认值 info 装配 |
| `wpl.computer_name` | `source_host` | "DESKTOP-NGMF7JI" | 由 WPL 字段 computer_name 投影或转换后赋值 |
| `wpl.mac` | `source_mac` | "00:50:56:81:e3:7e" | 由 WPL 字段 mac 投影或转换后赋值 |
| `constant.mapping_vendor` | `observer_vendor` | "qax" | 使用平台/映射规则常量 mapping_vendor |
| `constant.mapping_product` | `observer_product` | "tianqing" | 使用平台/映射规则常量 mapping_product |
| `wpl.process_name` | `carrier_process_name` | "svchost.exe" | 由 WPL 字段 process_name 投影或转换后赋值 |
| `wpl.process_guid` | `carrier_process_guid` | "e3c04c6237c7e24cf9566bdb5bbf3b5a" | 由 WPL 字段 process_guid 投影或转换后赋值 |
| `wpl.process_id` | `carrier_process_pid` | "2360" | 由 WPL 字段 process_id 投影或转换后赋值 |
| `derived.entity_ref` | `roles.source.ref_id` | "host_2868257359929541780" | 按确定性规则 entity_ref 派生 |
| `constant.entity_type` | `roles.source.entity_type` | "host" | 使用平台/映射规则常量 entity_type |
| `derived.entity_ref` | `roles.carriers[0].ref_id` | "process_e3c04c6237c7e24cf9566bdb5bbf3b5a" | 按确定性规则 entity_ref 派生 |
| `constant.entity_type` | `roles.carriers[0].entity_type` | "process" | 使用平台/映射规则常量 entity_type |
| `constant.mapping_product` | `roles.observer.product.name` | "tianqing" | 使用平台/映射规则常量 mapping_product |
| `constant.mapping_vendor` | `roles.observer.device.vendor` | "qax" | 使用平台/映射规则常量 mapping_vendor |
| `derived.entity_ref` | `roles.related[0].ref_id` | "process_0c0b3c9013915af81340261b4cf20835" | 按确定性规则 entity_ref 派生 |
| `constant.entity_type` | `roles.related[0].entity_type` | "process" | 使用平台/映射规则常量 entity_type |
| `constant.relation_type` | `roles.related[0].relation_type` | "parent_process" | 使用平台/映射规则常量 relation_type |
| `constant.sdm_schema_version` | `extensions.schema_version` | 2 | 使用平台/映射规则常量 sdm_schema_version |
| `derived.entity_ref` | `extensions.profiles.endpoint_asset.subject_ref.ref_id` | "host_2868257359929541780" | 按确定性规则 entity_ref 派生 |
| `platform_context.env_version` | `extensions.profiles.endpoint_asset.agent.version` | "edr-8.0" | 由平台上下文提供 |
| `data_gap.wpl_field_missing` | `extensions.unmapped.source_process` | "WPL 规则未抽取 raw source_process_* 字段" | WPL 未抽取该字段；此处仅记录数据缺口，不应伪造业务值 |

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
| `mapping_id` | `constant` | `constant.mapping_id` | "qax.tianqing.edr_wmi_event" | `—` | confirmed；使用平台/映射规则常量 mapping_id |
| `data_src_vendor` | `constant` | `constant.mapping_vendor` | "qax" | `—` | confirmed；使用平台/映射规则常量 mapping_vendor |
| `data_src_product` | `constant` | `constant.mapping_product` | "tianqing" | `—` | confirmed；使用平台/映射规则常量 mapping_product |
| `data_src_category` | `constant` | `constant.mapping_category` | "endpoint_security" | `—` | confirmed；使用平台/映射规则常量 mapping_category |
| `data_src_instance_id` | `context` | `platform_context.data_src_instance_id` | `platform_context.data_src_instance_id` | `—` | confirmed；由平台上下文提供 |
| `log_type` | `constant` | `constant.log_type` | "edr_wmi_event" | `—` | confirmed；使用平台/映射规则常量 log_type |
| `log_name` | `constant` | `constant.log_name` | "天擎 EDR WMI 事件" | `—` | confirmed；使用平台/映射规则常量 log_name |
| `record_kind` | `constant` | `constant.record_kind` | "activity" | `—` | confirmed；使用平台/映射规则常量 record_kind |
| `event_domain` | `constant` | `constant.event_domain` | "endpoint" | `—` | confirmed；使用平台/映射规则常量 event_domain |
| `event_category` | `constant` | `constant.event_category` | "audit" | `—` | confirmed；EDR 行为监控 WMI 事件，PDF §3.9.13 |
| `severity` | `constant` | `constant.default_severity` | "info" | `—` | confirmed；当前日志类型未提供标准 severity，按映射默认值 info 装配 |
| `observer_vendor` | `constant` | `constant.mapping_vendor` | "qax" | `—` | confirmed；使用平台/映射规则常量 mapping_vendor |
| `observer_product` | `constant` | `constant.mapping_product` | "tianqing" | `—` | confirmed；使用平台/映射规则常量 mapping_product |
| `roles.source.ref_id` | `derived` | `derived.entity_ref` | `derived.entity_ref` | `—` | confirmed；按确定性规则 entity_ref 派生 |
| `roles.source.entity_type` | `constant` | `constant.entity_type` | "host" | `—` | confirmed；使用平台/映射规则常量 entity_type |
| `roles.carriers[0].ref_id` | `derived` | `derived.entity_ref` | `derived.entity_ref` | `—` | confirmed；按确定性规则 entity_ref 派生 |
| `roles.carriers[0].entity_type` | `constant` | `constant.entity_type` | "process" | `—` | confirmed；使用平台/映射规则常量 entity_type |
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
| `source_host` | `projection` | `computer_name` | `wpl.computer_name` | `—` | confirmed；由 WPL 字段 computer_name 投影或转换后赋值 |
| `source_mac` | `projection` | `mac` | `wpl.mac` | `—` | confirmed；由 WPL 字段 mac 投影或转换后赋值 |
| `carrier_process_name` | `projection` | `process_name` | `wpl.process_name` | `—` | confirmed；由 WPL 字段 process_name 投影或转换后赋值 |
| `carrier_process_guid` | `projection` | `process_guid` | `wpl.process_guid` | `—` | confirmed；由 WPL 字段 process_guid 投影或转换后赋值 |
| `carrier_process_pid` | `projection` | `process_id` | `wpl.process_id` | `—` | confirmed；由 WPL 字段 process_id 投影或转换后赋值 |
| `extensions.unmapped.source_process` | `gap` | `data_gap.wpl_field_missing` | `data_gap.wpl_field_missing` | `—` | missing；WPL 未抽取该字段；此处仅记录数据缺口，不应伪造业务值 |
| `extensions.profiles.endpoint_asset.ownership.organization.id` | `projection` | `asset_oid` | "2653788242175861718" | `—` | confirmed；按当前 expected 事件结构映射 |
| `occur_time` | `projection` | `event_date_creation` | 1733932552630 | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.related[0].process.cmdline` | `projection` | `process_parent_command_line` | "C:\\WINDOWS\\system32\\services.exe" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.related[0].process.file.internal_name` | `projection` | `process_parent_internal_name` | "services.exe" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.related[0].process.name` | `projection` | `process_parent_name` | "services.exe" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.related[0].process.file.original_name` | `projection` | `process_parent_original_name` | "services.exe" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.related[0].process.file.signatures[0].signer` | `projection` | `process_parent_sign` | "Microsoft Windows Publisher" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.carriers[0].process.file.hashes.sha1` | `projection` | `process_sha1` | "e4e3f6bbad17b41a42687b3d75ade4a10b0870ec" | `—` | confirmed；按当前 expected 事件结构映射 |
| `source_original_event_id` | `projection` | `uuid` | "0C295907-0423-46AC-B6E4-8F171BA7D60A" | `—` | confirmed；按当前 expected 事件结构映射 |
| `extensions.source_private.filter_wql` | `projection` | `wmi_filter_wql` | "SELECT * FROM __InstanceOperationEvent WHERE TargetInstance ISA 'AntiVirusProduct' OR TargetInstance ISA 'FirewallProduct' OR TargetInstance ISA 'AntiSpywareProduct'" | `—` | confirmed；WMI 查询原文；当前不据此构造虚假的文件、网络或进程目标 |
| `roles.source.host.name` | `projection` | `computer_name` | "DESKTOP-NGMF7JI" | `—` | confirmed；按当前 expected 事件结构映射 |
| `extensions.profiles.endpoint_asset.ownership.group.id` | `projection` | `gid` | "4f9c3833b800d1f7" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.carriers[0].process.cmdline` | `projection` | `process_command_line` | "C:\\WINDOWS\\system32\\svchost.exe -k netsvcs -p -s Winmgmt" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.carriers[0].process.file.internal_name` | `projection` | `process_internal_name` | "svchost.exe" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.carriers[0].process.file.original_name` | `projection` | `process_original_name` | "svchost.exe" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.related[0].process.path` | `projection` | `process_parent_path` | "C:\\Windows\\System32\\services.exe" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.carriers[0].process.file.signatures[0].signer` | `projection` | `process_sign` | "Microsoft Windows Publisher" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.carriers[0].process.user.name` | `projection` | `process_user` | "NT AUTHORITY\\SYSTEM" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.source.host.id` | `projection` | `asset_id` | "2868257359929541780" | `—` | confirmed；按当前 expected 事件结构映射 |
| `extensions.profiles.endpoint_asset.agent.id` | `projection` | `client_id` | "8558772-6b168d97c3f346a96ed4ecef42be407a" | `—` | confirmed；按当前 expected 事件结构映射 |
| `extensions.profiles.endpoint_asset.ownership.group.name` | `projection` | `group_name` | "未分组终端" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.source.host.mac` | `projection` | `mac` | "00:50:56:81:e3:7e" | `—` | confirmed；按当前 expected 事件结构映射 |
| `extensions.profiles.endpoint_asset.agent.fingerprint_id` | `projection` | `mid` | "1ca36f97756b33c2bf9139aab6ac36926903b9ec24e0009fae93fda96ded6898" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.carriers[0].process.uid` | `projection` | `process_guid` | "e3c04c6237c7e24cf9566bdb5bbf3b5a" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.carriers[0].process.pid` | `projection` | `process_id` | "2360" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.carriers[0].process.file.hashes.md5` | `projection` | `process_md5` | "7469cc568ad6821fd9d925542730a7d8" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.carriers[0].process.name` | `projection` | `process_name` | "svchost.exe" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.carriers[0].process.path` | `projection` | `process_path` | "C:\\Windows\\System32\\svchost.exe" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.source.host.ip` | `projection` | `ip` | "192.0.2.206" | `—` | confirmed；按当前 expected 事件结构映射 |
| `event_type` | `dictionary` | `event_type` | "wmi_execute" -> "process_uncategorized" | `preserve_in_extension_and_review` | partial；wmi_execute 暂映射为 process_uncategorized；没有受控 operation 时留空 |

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
