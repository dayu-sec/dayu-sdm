# WPL → SDM Event 字段映射

> 样例：`powershell_execute.expected-sdm-event.json`；WPL 字段 45 个，映射 33，不落库 12，排除 0；另有平台默认、派生及结构字段 43 项。
> SDM 落位为逻辑路径；expected 位置为该样例中的实际物理 JSON 路径。

## 一、映射字段

| WPL 字段 | WPL 值 | SDM 落位 | expected 位置 | expected 值 | 说明 |
|---|---|---|---|---|---|
| `asset_id` | "2868257359929541780" | `roles.source.host.id` | `roles_obj.source.host.id` | "2868257359929541780" | 按当前 expected 事件结构映射 |
| `asset_oid` | "2653788242175861718" | `extensions.profiles.endpoint_asset.ownership.organization.id` | `extensions_obj.profiles.endpoint_asset.ownership.organization.id` | "2653788242175861718" | 按当前 expected 事件结构映射 |
| `client_id` | "0881058-dfb9a23257c64098060e699601b17217" | `extensions.profiles.endpoint_asset.agent.id` | `extensions_obj.profiles.endpoint_asset.agent.id` | "0881058-dfb9a23257c64098060e699601b17217" | 按当前 expected 事件结构映射 |
| `computer_name` | "DESKTOP-EX01" | `roles.source.host.name` | `roles_obj.source.host.name` | "DESKTOP-EX01" | 按当前 expected 事件结构映射 |
| `event_date_creation` | 1734466270549 | `occur_time` | `occur_time` | 1734466270549 | 按当前 expected 事件结构映射 |
| `event_id` | "4104" | `extensions.source_private.windows_event_id` | `extensions_obj.source_private.windows_event_id` | "4104" | Windows 事件代码 4104，不是 SDM event_id |
| `gid` | "4f9c3833b800d1f7" | `extensions.profiles.endpoint_asset.ownership.group.id` | `extensions_obj.profiles.endpoint_asset.ownership.group.id` | "4f9c3833b800d1f7" | 按当前 expected 事件结构映射 |
| `group_name` | "未分组终端" | `extensions.profiles.endpoint_asset.ownership.group.name` | `extensions_obj.profiles.endpoint_asset.ownership.group.name` | "未分组终端" | 按当前 expected 事件结构映射 |
| `ip` | "198.51.100.211" | `roles.source.host.ip` | `roles_obj.source.host.ip` | "198.51.100.211" | 按当前 expected 事件结构映射 |
| `keywords` | "0x0" | `extensions.source_private.keywords` | `extensions_obj.source_private.keywords` | "0x0" | 按当前 expected 事件结构映射 |
| `mac` | "00-00-5E-00-53-79" | `roles.source.host.mac` | `roles_obj.source.host.mac` | "00:00:5E:00:53:23" | 按当前 expected 事件结构映射 |
| `mid` | "ec80b820d87d7cd7ac916240bcdff7215ae3118feaf070c13afbf06e69af4eb3" | `extensions.profiles.endpoint_asset.agent.fingerprint_id` | `extensions_obj.profiles.endpoint_asset.agent.fingerprint_id` | "ec80b820d87d7cd7ac916240bcdff7215ae3118feaf070c13afbf06e69af4eb3" | 按当前 expected 事件结构映射 |
| `powershell_create_time` | 1734466207744 | `roles.carriers[0].process.created_time` | `roles_obj.carriers[0].process.created_time` | 1734466207744 | 按当前 expected 事件结构映射 |
| `process_command_line` | "powershell.exe -ExecutionPolicy Restricted -Command  $Res = 0; $Infs = Get-Item -Path ($env:WinDir + '\\inf\\*.inf'); foreach ($Inf in $Infs) { $Data = Get-Content $Inf.FullName; if ($Data -match '\\[defaultinstall.nt(amd64\|arm\|arm64\|x86)\\]') { $Res = 1; break; } } Write-Host 'Final result:', $Res;" | `roles.carriers[0].process.cmdline` | `roles_obj.carriers[0].process.cmdline` | "powershell.exe -ExecutionPolicy Restricted -Command  $Res = 0; $Infs = Get-Item -Path ($env:WinDir + '\\inf\\*.inf'); foreach ($Inf in $Infs) { $Data = Get-Content $Inf.FullName; if ($Data -match '\\[defaultinstall.nt(amd64\|arm\|arm64\|x86)\\]') { $Res = 1; break; } } Write-Host 'Final result:', $Res;" | 按当前 expected 事件结构映射 |
| `process_guid` | "17315699910326c507f53b59d93c68b7" | `roles.carriers[0].process.uid` | `roles_obj.carriers[0].process.uid` | "17315699910326c507f53b59d93c68b7" | 按当前 expected 事件结构映射 |
| `process_id` | "16400" | `roles.carriers[0].process.pid` | `roles_obj.carriers[0].process.pid` | "16400" | 按当前 expected 事件结构映射 |
| `process_internal_name` | "POWERSHELL" | `roles.carriers[0].process.file.internal_name` | `roles_obj.carriers[0].process.file.internal_name` | "POWERSHELL" | 按当前 expected 事件结构映射 |
| `process_md5` | "2e5a8590cf6848968fc23de3fa1e25f1" | `roles.carriers[0].process.file.hashes.md5` | `roles_obj.carriers[0].process.file.hashes.md5` | "2e5a8590cf6848968fc23de3fa1e25f1" | 按当前 expected 事件结构映射 |
| `process_name` | "powershell.exe" | `roles.carriers[0].process.name` | `roles_obj.carriers[0].process.name` | "powershell.exe" | 按当前 expected 事件结构映射 |
| `process_parent_command_line` | "C:\\WINDOWS\\system32\\CompatTelRunner.exe -m:appraiser.dll -f:DoScheduledTelemetryRun -cv:OQgCHuoMqEyFikre.1" | `roles.related[0].process.cmdline` | `roles_obj.related[0].process.cmdline` | "C:\\WINDOWS\\system32\\CompatTelRunner.exe -m:appraiser.dll -f:DoScheduledTelemetryRun -cv:OQgCHuoMqEyFikre.1" | 按当前 expected 事件结构映射 |
| `process_parent_internal_name` | "CompatTelRunner.exe" | `roles.related[0].process.file.internal_name` | `roles_obj.related[0].process.file.internal_name` | "CompatTelRunner.exe" | 按当前 expected 事件结构映射 |
| `process_parent_name` | "CompatTelRunner.exe" | `roles.related[0].process.name` | `roles_obj.related[0].process.name` | "CompatTelRunner.exe" | 按当前 expected 事件结构映射 |
| `process_parent_original_name` | "CompatTelRunner.exe" | `roles.related[0].process.file.original_name` | `roles_obj.related[0].process.file.original_name` | "CompatTelRunner.exe" | 按当前 expected 事件结构映射 |
| `process_parent_path` | "C:\\Windows\\System32\\CompatTelRunner.exe" | `roles.related[0].process.path` | `roles_obj.related[0].process.path` | "C:\\Windows\\System32\\CompatTelRunner.exe" | 按当前 expected 事件结构映射 |
| `process_parent_sign` | "Microsoft Corporation" | `roles.related[0].process.file.signatures[0].signer` | `roles_obj.related[0].process.file.signatures[0].signer` | "Microsoft Corporation" | 按当前 expected 事件结构映射 |
| `process_path` | "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" | `roles.carriers[0].process.path` | `roles_obj.carriers[0].process.path` | "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" | 按当前 expected 事件结构映射 |
| `process_sha1` | "801262e122db6a2e758962896f260b55bbd0136a" | `roles.carriers[0].process.file.hashes.sha1` | `roles_obj.carriers[0].process.file.hashes.sha1` | "801262e122db6a2e758962896f260b55bbd0136a" | 按当前 expected 事件结构映射 |
| `process_sign` | "Microsoft Windows" | `roles.carriers[0].process.file.signatures[0].signer` | `roles_obj.carriers[0].process.file.signatures[0].signer` | "Microsoft Windows" | 按当前 expected 事件结构映射 |
| `process_user` | "NT AUTHORITY\\SYSTEM" | `roles.carriers[0].process.user.name` | `roles_obj.carriers[0].process.user.name` | "NT AUTHORITY\\SYSTEM" | 按当前 expected 事件结构映射 |
| `script_command` | "$global:?" | `roles.carriers[1].script.command` | `roles_obj.carriers[1].script.command` | "$global:?" | 按当前 expected 事件结构映射 |
| `script_id` | "12e821ca-0d5c-409a-8bbf-fa39567d4d70" | `roles.carriers[1].script.id` | `roles_obj.carriers[1].script.id` | "12e821ca-0d5c-409a-8bbf-fa39567d4d70" | 按当前 expected 事件结构映射 |
| `thread_id` | 14728 | `extensions.source_private.thread_id` | `extensions_obj.source_private.thread_id` | 14728 | 按当前 expected 事件结构映射 |
| `uuid` | "AD5061E8-3AB4-411A-8A9C-672EAAFC87FE" | `source_original_event_id` | `source_original_event_id` | "AD5061E8-3AB4-411A-8A9C-672EAAFC87FE" | 按当前 expected 事件结构映射 |

## 二、不落库字段

| WPL 字段 | WPL 值 | 原因 |
|---|---|---|
| `context_info` | "" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `create_time` | 1734466261238 | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `custom_group_paths` | "" | 分组路径原始串不进入事件对象；原值保留在 raw_msg |
| `event_type` | "powershell_execute" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `os_type` | "1" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `powershell_payload` | "" | 当前为空，不构造 script.content；字段缺口记录在 extensions.unmapped |
| `report_ip` | "198.51.100.211" | 疑似 Agent 上报链路地址；与终端 IP 不一致时不作为事件 source IP，原值保留在 raw_msg |
| `report_ipv6` | "" | Agent 上报链路 IPv6；当前为空或语义未确认，暂不落库 |
| `security_id` | "S-1-5-18" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `timestamp` | 1734466286000 | 条件回退字段：仅 event_date_creation 缺失或无效时用于 occur_time；本样例未采用 |
| `type` | "powershell_execute" | 仅用于 WPL 路由，稳定日志类型已由 log_type 表达；原值保留在 raw_msg |
| `user_data` | "" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |

## 四、平台默认、派生及结构字段

| 来源 | SDM 落位 | expected 值 | 赋值责任与说明 |
|---|---|---|---|
| `platform_context.tenant_id` | `tenant_id` | "" | 由平台上下文提供 |
| `derived.sha256('|'+mapping_id+'|'+source_original_event_id)` | `event_id` | "evt-c3f0de26eab40e9f8d33ec6540f80d3bd63e7079d2bb103ae928806bc2c3193b" | 按确定性规则 sha256('|'+mapping_id+'|'+source_original_event_id) 派生 |
| `platform_context.log_id` | `log_id` | "log-tianqing-powershell-exec-0001" | 由平台上下文提供 |
| `raw_log_input` | `raw_msg` | "{\"type\":\"powershell_execute\",\"event_type\":\"powershell_execute\",\"uuid\":\"AD5061E8-3AB4-411A-8A9C-672EAAFC87FE\",\"script_id\":\"12e821ca-0d5c-409a-8bbf-fa39567d4d70\",\"script_command\":\"$global:?\",\"process_name\":\"powershell.exe\"}" | 由原始日志接入层保存，不由 OML 拼装 |
| `platform_context.ingest_time` | `ingest_time` | 1734466287001 | 由平台上下文提供 |
| `platform_context.parse_time` | `parse_time` | 1734466287120 | 由平台上下文提供 |
| `constant.sdm_schema_version` | `schema_version` | 2 | 使用平台/映射规则常量 sdm_schema_version |
| `constant.mapping_id` | `mapping_id` | "qax.tianqing.edr_powershell_cmd_exec" | 使用平台/映射规则常量 mapping_id |
| `constant.mapping_vendor` | `data_src_vendor` | "qax" | 使用平台/映射规则常量 mapping_vendor |
| `constant.mapping_product` | `data_src_product` | "tianqing" | 使用平台/映射规则常量 mapping_product |
| `constant.mapping_category` | `data_src_category` | "endpoint_security" | 使用平台/映射规则常量 mapping_category |
| `platform_context.data_src_instance_id` | `data_src_instance_id` | "collector-tianqing-poc-01" | 由平台上下文提供 |
| `constant.log_type` | `log_type` | "edr_powershell_cmd_exec" | 使用平台/映射规则常量 log_type |
| `constant.log_name` | `log_name` | "天擎 EDR PowerShell 命令执行" | 使用平台/映射规则常量 log_name |
| `constant.record_kind` | `record_kind` | "activity" | 使用平台/映射规则常量 record_kind |
| `constant.event_domain` | `event_domain` | "endpoint" | 使用平台/映射规则常量 event_domain |
| `constant.event_type` | `event_type` | "generic_event" | 使用平台/映射规则常量 event_type |
| `derived.enum_projection` | `outcome` | "observed" | 由 WPL 枚举或日志语义转换为 SDM 标准值 |
| `constant.default_severity` | `severity` | "info" | 当前日志类型未提供标准 severity，按映射默认值 info 装配 |
| `wpl.process_user` | `source_user` | "NT AUTHORITY\\SYSTEM" | 由 WPL 字段 process_user 投影或转换后赋值 |
| `wpl.computer_name` | `source_host` | "DESKTOP-EX01" | 由 WPL 字段 computer_name 投影或转换后赋值 |
| `constant.mapping_vendor` | `observer_vendor` | "qax" | 使用平台/映射规则常量 mapping_vendor |
| `constant.mapping_product` | `observer_product` | "tianqing" | 使用平台/映射规则常量 mapping_product |
| `wpl.process_name` | `carrier_process_name` | "powershell.exe" | 由 WPL 字段 process_name 投影或转换后赋值 |
| `wpl.process_guid` | `carrier_process_guid` | "17315699910326c507f53b59d93c68b7" | 由 WPL 字段 process_guid 投影或转换后赋值 |
| `wpl.process_id` | `carrier_process_pid` | "16400" | 由 WPL 字段 process_id 投影或转换后赋值 |
| `derived.entity_ref` | `roles.source.ref_id` | "host_2868257359929541780" | 按确定性规则 entity_ref 派生 |
| `constant.entity_type` | `roles.source.entity_type` | "host" | 使用平台/映射规则常量 entity_type |
| `derived.entity_ref` | `roles.carriers[0].ref_id` | "process_17315699910326c507f53b59d93c68b7" | 按确定性规则 entity_ref 派生 |
| `constant.entity_type` | `roles.carriers[0].entity_type` | "process" | 使用平台/映射规则常量 entity_type |
| `wpl.security_id` | `roles.carriers[0].process.user.id` | "S-1-5-18" | 由 WPL 字段 security_id 投影或转换后赋值 |
| `derived.entity_ref` | `roles.carriers[1].ref_id` | "script_12e821ca_0d5c_409a_8bbf_fa39567d4d70" | 按确定性规则 entity_ref 派生 |
| `constant.entity_type` | `roles.carriers[1].entity_type` | "script" | 使用平台/映射规则常量 entity_type |
| `wpl.process_internal_name` | `roles.carriers[1].script.language` | "powershell" | 由 WPL 字段 process_internal_name 投影或转换后赋值 |
| `constant.mapping_product` | `roles.observer.product.name` | "tianqing" | 使用平台/映射规则常量 mapping_product |
| `constant.mapping_vendor` | `roles.observer.device.vendor` | "qax" | 使用平台/映射规则常量 mapping_vendor |
| `derived.entity_ref` | `roles.related[0].ref_id` | "process_parent_compattelrunner_01" | 按确定性规则 entity_ref 派生 |
| `constant.entity_type` | `roles.related[0].entity_type` | "process" | 使用平台/映射规则常量 entity_type |
| `constant.relation_type` | `roles.related[0].relation_type` | "parent_process" | 使用平台/映射规则常量 relation_type |
| `constant.sdm_schema_version` | `extensions.schema_version` | 2 | 使用平台/映射规则常量 sdm_schema_version |
| `derived.entity_ref` | `extensions.profiles.endpoint_asset.subject_ref.ref_id` | "host_2868257359929541780" | 按确定性规则 entity_ref 派生 |
| `platform_context.env_version` | `extensions.profiles.endpoint_asset.agent.version` | "edr-8.0" | 由平台上下文提供 |
| `data_gap.wpl_field_missing` | `extensions.unmapped.script_content` | "powershell_payload 为空，未构造 script.content" | WPL 未抽取该字段；此处仅记录数据缺口，不应伪造业务值 |

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
| `mapping_id` | `constant` | `constant.mapping_id` | "qax.tianqing.edr_powershell_cmd_exec" | `—` | confirmed；使用平台/映射规则常量 mapping_id |
| `data_src_vendor` | `constant` | `constant.mapping_vendor` | "qax" | `—` | confirmed；使用平台/映射规则常量 mapping_vendor |
| `data_src_product` | `constant` | `constant.mapping_product` | "tianqing" | `—` | confirmed；使用平台/映射规则常量 mapping_product |
| `data_src_category` | `constant` | `constant.mapping_category` | "endpoint_security" | `—` | confirmed；使用平台/映射规则常量 mapping_category |
| `data_src_instance_id` | `context` | `platform_context.data_src_instance_id` | `platform_context.data_src_instance_id` | `—` | confirmed；由平台上下文提供 |
| `log_type` | `constant` | `constant.log_type` | "edr_powershell_cmd_exec" | `—` | confirmed；使用平台/映射规则常量 log_type |
| `log_name` | `constant` | `constant.log_name` | "天擎 EDR PowerShell 命令执行" | `—` | confirmed；使用平台/映射规则常量 log_name |
| `record_kind` | `constant` | `constant.record_kind` | "activity" | `—` | confirmed；使用平台/映射规则常量 record_kind |
| `event_domain` | `constant` | `constant.event_domain` | "endpoint" | `—` | confirmed；使用平台/映射规则常量 event_domain |
| `event_type` | `constant` | `constant.event_type` | "generic_event" | `—` | confirmed；使用平台/映射规则常量 event_type |
| `event_category` | `constant` | `constant.event_category` | "audit" | `—` | confirmed；EDR 行为监控 PowerShell 命令执行，PDF §3.9.10 |
| `severity` | `constant` | `constant.default_severity` | "info" | `—` | confirmed；当前日志类型未提供标准 severity，按映射默认值 info 装配 |
| `observer_vendor` | `constant` | `constant.mapping_vendor` | "qax" | `—` | confirmed；使用平台/映射规则常量 mapping_vendor |
| `observer_product` | `constant` | `constant.mapping_product` | "tianqing" | `—` | confirmed；使用平台/映射规则常量 mapping_product |
| `roles.source.ref_id` | `derived` | `derived.entity_ref` | `derived.entity_ref` | `—` | confirmed；按确定性规则 entity_ref 派生 |
| `roles.source.entity_type` | `constant` | `constant.entity_type` | "host" | `—` | confirmed；使用平台/映射规则常量 entity_type |
| `roles.carriers[0].ref_id` | `derived` | `derived.entity_ref` | `derived.entity_ref` | `—` | confirmed；按确定性规则 entity_ref 派生 |
| `roles.carriers[0].entity_type` | `constant` | `constant.entity_type` | "process" | `—` | confirmed；使用平台/映射规则常量 entity_type |
| `roles.carriers[1].ref_id` | `derived` | `derived.entity_ref` | `derived.entity_ref` | `—` | confirmed；按确定性规则 entity_ref 派生 |
| `roles.carriers[1].entity_type` | `constant` | `constant.entity_type` | "script" | `—` | confirmed；使用平台/映射规则常量 entity_type |
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
| `carrier_process_name` | `projection` | `process_name` | `wpl.process_name` | `—` | confirmed；由 WPL 字段 process_name 投影或转换后赋值 |
| `carrier_process_guid` | `projection` | `process_guid` | `wpl.process_guid` | `—` | confirmed；由 WPL 字段 process_guid 投影或转换后赋值 |
| `carrier_process_pid` | `projection` | `process_id` | `wpl.process_id` | `—` | confirmed；由 WPL 字段 process_id 投影或转换后赋值 |
| `roles.carriers[0].process.user.id` | `projection` | `security_id` | `wpl.security_id` | `—` | confirmed；由 WPL 字段 security_id 投影或转换后赋值 |
| `roles.carriers[1].script.language` | `projection` | `process_internal_name` | `wpl.process_internal_name` | `—` | confirmed；由 WPL 字段 process_internal_name 投影或转换后赋值 |
| `extensions.unmapped.script_content` | `gap` | `data_gap.wpl_field_missing` | `data_gap.wpl_field_missing` | `—` | missing；WPL 未抽取该字段；此处仅记录数据缺口，不应伪造业务值 |
| `roles.source.host.id` | `projection` | `asset_id` | "2868257359929541780" | `—` | confirmed；按当前 expected 事件结构映射 |
| `extensions.profiles.endpoint_asset.ownership.organization.id` | `projection` | `asset_oid` | "2653788242175861718" | `—` | confirmed；按当前 expected 事件结构映射 |
| `extensions.profiles.endpoint_asset.agent.id` | `projection` | `client_id` | "0881058-dfb9a23257c64098060e699601b17217" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.source.host.name` | `projection` | `computer_name` | "DESKTOP-EX01" | `—` | confirmed；按当前 expected 事件结构映射 |
| `occur_time` | `projection` | `event_date_creation` | 1734466270549 | `—` | confirmed；按当前 expected 事件结构映射 |
| `extensions.source_private.windows_event_id` | `projection` | `event_id` | "4104" | `—` | confirmed；Windows 事件代码 4104，不是 SDM event_id |
| `extensions.profiles.endpoint_asset.ownership.group.id` | `projection` | `gid` | "4f9c3833b800d1f7" | `—` | confirmed；按当前 expected 事件结构映射 |
| `extensions.profiles.endpoint_asset.ownership.group.name` | `projection` | `group_name` | "未分组终端" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.source.host.ip` | `projection` | `ip` | "198.51.100.211" | `—` | confirmed；按当前 expected 事件结构映射 |
| `extensions.source_private.keywords` | `projection` | `keywords` | "0x0" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.source.host.mac` | `projection` | `mac` | "00:00:5E:00:53:23" | `—` | confirmed；按当前 expected 事件结构映射 |
| `extensions.profiles.endpoint_asset.agent.fingerprint_id` | `projection` | `mid` | "ec80b820d87d7cd7ac916240bcdff7215ae3118feaf070c13afbf06e69af4eb3" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.carriers[0].process.created_time` | `projection` | `powershell_create_time` | 1734466207744 | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.carriers[0].process.cmdline` | `projection` | `process_command_line` | "powershell.exe -ExecutionPolicy Restricted -Command  $Res = 0; $Infs = Get-Item -Path ($env:WinDir + '\\inf\\*.inf'); foreach ($Inf in $Infs) { $Data = Get-Content $Inf.FullName; if ($Data -match '\\[defaultinstall.nt(amd64|arm|arm64|x86)\\]') { $Res = 1; break; } } Write-Host 'Final result:', $Res;" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.carriers[0].process.uid` | `projection` | `process_guid` | "17315699910326c507f53b59d93c68b7" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.carriers[0].process.pid` | `projection` | `process_id` | "16400" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.carriers[0].process.file.internal_name` | `projection` | `process_internal_name` | "POWERSHELL" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.carriers[0].process.file.hashes.md5` | `projection` | `process_md5` | "2e5a8590cf6848968fc23de3fa1e25f1" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.carriers[0].process.name` | `projection` | `process_name` | "powershell.exe" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.related[0].process.cmdline` | `projection` | `process_parent_command_line` | "C:\\WINDOWS\\system32\\CompatTelRunner.exe -m:appraiser.dll -f:DoScheduledTelemetryRun -cv:OQgCHuoMqEyFikre.1" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.related[0].process.file.internal_name` | `projection` | `process_parent_internal_name` | "CompatTelRunner.exe" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.related[0].process.name` | `projection` | `process_parent_name` | "CompatTelRunner.exe" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.related[0].process.file.original_name` | `projection` | `process_parent_original_name` | "CompatTelRunner.exe" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.related[0].process.path` | `projection` | `process_parent_path` | "C:\\Windows\\System32\\CompatTelRunner.exe" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.related[0].process.file.signatures[0].signer` | `projection` | `process_parent_sign` | "Microsoft Corporation" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.carriers[0].process.path` | `projection` | `process_path` | "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.carriers[0].process.file.hashes.sha1` | `projection` | `process_sha1` | "801262e122db6a2e758962896f260b55bbd0136a" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.carriers[0].process.file.signatures[0].signer` | `projection` | `process_sign` | "Microsoft Windows" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.carriers[0].process.user.name` | `projection` | `process_user` | "NT AUTHORITY\\SYSTEM" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.carriers[1].script.command` | `projection` | `script_command` | "$global:?" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.carriers[1].script.id` | `projection` | `script_id` | "12e821ca-0d5c-409a-8bbf-fa39567d4d70" | `—` | confirmed；按当前 expected 事件结构映射 |
| `extensions.source_private.thread_id` | `projection` | `thread_id` | 14728 | `—` | confirmed；按当前 expected 事件结构映射 |
| `source_original_event_id` | `projection` | `uuid` | "AD5061E8-3AB4-411A-8A9C-672EAAFC87FE" | `—` | confirmed；按当前 expected 事件结构映射 |

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
