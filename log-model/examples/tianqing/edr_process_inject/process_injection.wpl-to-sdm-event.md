# WPL → SDM Event 字段映射

> 样例：`process_injection.expected-sdm-event.json`；WPL 字段 46 个，映射 38，不落库 8，排除 0；另有平台默认、派生及结构字段 37 项。
> SDM 落位为逻辑路径；expected 位置为该样例中的实际物理 JSON 路径。

## 一、映射字段

| WPL 字段 | WPL 值 | SDM 落位 | expected 位置 | expected 值 | 说明 |
|---|---|---|---|---|---|
| `asset_id` | "2868257359929541780" | `roles.source.host.id` | `roles_obj.source.host.id` | "2868257359929541780" | 按当前 expected 事件结构映射 |
| `asset_oid` | "2653788242175861718" | `extensions.profiles.endpoint_asset.ownership.organization.id` | `extensions_obj.profiles.endpoint_asset.ownership.organization.id` | "2653788242175861718" | 按当前 expected 事件结构映射 |
| `client_id` | "8558772-6b168d97c3f346a96ed4ecef42be407a" | `extensions.profiles.endpoint_asset.agent.id` | `extensions_obj.profiles.endpoint_asset.agent.id` | "8558772-6b168d97c3f346a96ed4ecef42be407a" | 按当前 expected 事件结构映射 |
| `computer_name` | "DESKTOP-EX02" | `roles.source.host.name` | `roles_obj.source.host.name` | "DESKTOP-EX02" | 按当前 expected 事件结构映射 |
| `event_date_creation` | 1732787303894 | `occur_time` | `occur_time` | 1732787303894 | 按当前 expected 事件结构映射 |
| `event_type` | "Process_Injection" | `event_type` | `event_type` | "process_injection" | 已确认枚举转换：Process_Injection 映射为 process_injection |
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
| `target_process_guid` | "a6a4e1ff66de42a7ec2477f188f04d96" | `roles.target.process.uid` | `roles_obj.target.process.uid` | "a6a4e1ff66de42a7ec2477f188f04d96" | 按当前 expected 事件结构映射 |
| `target_process_id` | "6688" | `roles.target.process.pid` | `roles_obj.target.process.pid` | "6688" | 按当前 expected 事件结构映射 |
| `target_process_md5` | "8bfd0993e6af9b71f6ec20967e7f4e66" | `roles.target.process.file.hashes.md5` | `roles_obj.target.process.file.hashes.md5` | "8bfd0993e6af9b71f6ec20967e7f4e66" | 按当前 expected 事件结构映射 |
| `target_process_path` | "C:\\Windows\\servicing\\TrustedInstaller.exe" | `roles.target.process.path` | `roles_obj.target.process.path` | "C:\\Windows\\servicing\\TrustedInstaller.exe" | 目标进程名称由路径 basename 确定性派生 |
| `target_process_sign` | "Microsoft Windows" | `roles.target.process.file.signatures[0].signer` | `roles_obj.target.process.file.signatures[0].signer` | "Microsoft Windows" | 按当前 expected 事件结构映射 |
| `target_thread_address` | 140701423552944 | `facets.process.injection.target_thread.address` | `facets_obj.process.injection.target_thread.address` | "140701423552944" | 按当前 expected 事件结构映射 |
| `target_thread_args` | "718250356736" | `facets.process.injection.target_thread.arguments` | `facets_obj.process.injection.target_thread.arguments` | "718250356736" | 按当前 expected 事件结构映射 |
| `target_thread_id` | 17716 | `facets.process.injection.target_thread.id` | `facets_obj.process.injection.target_thread.id` | "17716" | 按当前 expected 事件结构映射 |
| `target_thread_module_path` | "C:\\Windows\\servicing\\TrustedInstaller.exe" | `facets.process.injection.target_thread.module_path` | `facets_obj.process.injection.target_thread.module_path` | "C:\\Windows\\servicing\\TrustedInstaller.exe" | 按当前 expected 事件结构映射 |
| `uuid` | "EAE19C3E-B634-4F6F-B138-4E498C068F72" | `source_original_event_id` | `source_original_event_id` | "EAE19C3E-B634-4F6F-B138-4E498C068F72" | 按当前 expected 事件结构映射 |

## 二、不落库字段

| WPL 字段 | WPL 值 | 原因 |
|---|---|---|
| `custom_group_paths` | "" | 分组路径原始串不进入事件对象；原值保留在 raw_msg |
| `execute_method_name` | "" | 来源为空；当前根据目标线程证据候选归一为 remote_thread，仍需厂商枚举确认 |
| `injected_dll` | "" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `os_type` | 1 | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `report_ip` | "203.0.113.45" | 疑似 Agent 上报链路地址；与终端 IP 不一致时不作为事件 source IP，原值保留在 raw_msg |
| `report_ipv6` | "" | Agent 上报链路 IPv6；当前为空或语义未确认，暂不落库 |
| `timestamp` | 1732787264000 | 条件回退字段：仅 event_date_creation 缺失或无效时用于 occur_time；本样例未采用 |
| `type` | "process_injection" | 仅用于 WPL 路由，稳定日志类型已由 log_type 表达；原值保留在 raw_msg |

## 四、平台默认、派生及结构字段

| 来源 | SDM 落位 | expected 值 | 赋值责任与说明 |
|---|---|---|---|
| `platform_context.tenant_id` | `tenant_id` | "" | 由平台上下文提供 |
| `derived.sha256('|'+mapping_id+'|'+source_original_event_id)` | `event_id` | "evt-808535db2e8e00154df461611d8a9a7bcdc164e1212d2f01fca04cb62764df0d" | 按确定性规则 sha256('|'+mapping_id+'|'+source_original_event_id) 派生 |
| `platform_context.log_id` | `log_id` | "log-tianqing-process-inject-0001" | 由平台上下文提供 |
| `raw_log_input` | `raw_msg` | "{\"type\":\"process_injection\",\"event_type\":\"Process_Injection\",\"uuid\":\"EAE19C3E-B634-4F6F-B138-4E498C068F72\",\"process_name\":\"services.exe\",\"target_process_path\":\"C:\\\\Windows\\\\servicing\\\\TrustedInstaller.exe\",\"target_thread_id\":17716}" | 由原始日志接入层保存，不由 OML 拼装 |
| `platform_context.ingest_time` | `ingest_time` | 1732787304001 | 由平台上下文提供 |
| `platform_context.parse_time` | `parse_time` | 1732787304120 | 由平台上下文提供 |
| `constant.sdm_schema_version` | `schema_version` | 2 | 使用平台/映射规则常量 sdm_schema_version |
| `constant.mapping_id` | `mapping_id` | "qax.tianqing.edr_process_inject" | 使用平台/映射规则常量 mapping_id |
| `constant.mapping_vendor` | `data_src_vendor` | "qax" | 使用平台/映射规则常量 mapping_vendor |
| `constant.mapping_product` | `data_src_product` | "tianqing" | 使用平台/映射规则常量 mapping_product |
| `constant.mapping_category` | `data_src_category` | "endpoint_security" | 使用平台/映射规则常量 mapping_category |
| `platform_context.data_src_instance_id` | `data_src_instance_id` | "collector-tianqing-poc-01" | 由平台上下文提供 |
| `constant.log_type` | `log_type` | "edr_process_inject" | 使用平台/映射规则常量 log_type |
| `constant.log_name` | `log_name` | "天擎 EDR 进程注入" | 使用平台/映射规则常量 log_name |
| `constant.record_kind` | `record_kind` | "activity" | 使用平台/映射规则常量 record_kind |
| `constant.event_domain` | `event_domain` | "endpoint" | 使用平台/映射规则常量 event_domain |
| `derived.enum_projection` | `operation` | "remote_thread" | 由目标线程证据推断为 remote_thread；execute_method_name 为空，需厂商方法枚举确认后才能固化 |
| `derived.enum_projection` | `outcome` | "observed" | 由 WPL 枚举或日志语义转换为 SDM 标准值 |
| `constant.default_severity` | `severity` | "info" | 当前日志类型未提供标准 severity，按映射默认值 info 装配 |
| `wpl.process_user` | `source_user` | "NT AUTHORITY\\SYSTEM" | 由 process_user 投影到事件标量字段 |
| `wpl.computer_name` | `source_host` | "DESKTOP-EX02" | 由 computer_name 投影到事件标量字段 |
| `constant.mapping_vendor` | `observer_vendor` | "qax" | 由平台厂商常量 qax 投影 |
| `constant.mapping_product` | `observer_product` | "tianqing" | 由平台产品常量 tianqing 投影 |
| `derived.entity_ref` | `roles.source.ref_id` | "host_2868257359929541780" | 按确定性规则 entity_ref 派生 |
| `constant.entity_type` | `roles.source.entity_type` | "host" | 使用平台/映射规则常量 entity_type |
| `derived.entity_ref` | `roles.target.ref_id` | "process_a6a4e1ff66de42a7ec2477f188f04d96" | 按确定性规则 entity_ref 派生 |
| `constant.entity_type` | `roles.target.entity_type` | "process" | 使用平台/映射规则常量 entity_type |
| `derived.path_basename` | `roles.target.process.name` | "TrustedInstaller.exe" | 由 target_process_path 取 basename 派生，不是 WPL 原始字段 |
| `constant.mapping_product` | `roles.observer.product.name` | "tianqing" | 使用平台/映射规则常量 mapping_product |
| `constant.mapping_vendor` | `roles.observer.device.vendor` | "qax" | 使用平台/映射规则常量 mapping_vendor |
| `derived.entity_ref` | `roles.related[0].ref_id` | "process_parent_wininit_01" | 父进程无稳定 GUID；当前使用 tenant、主机和父进程稳定属性生成，必须保证跨主机不碰撞 |
| `constant.entity_type` | `roles.related[0].entity_type` | "process" | 使用平台/映射规则常量 entity_type |
| `constant.relation_type` | `roles.related[0].relation_type` | "parent_process" | 使用平台/映射规则常量 relation_type |
| `derived.injection_method` | `facets.process.injection.method` | "remote_thread" | 同 operation 的候选注入方式；当前由目标线程 ID、地址和参数支持，需厂商枚举确认 |
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
| `mapping_id` | `constant` | `constant.mapping_id` | "qax.tianqing.edr_process_inject" | `—` | confirmed；使用平台/映射规则常量 mapping_id |
| `data_src_vendor` | `constant` | `constant.mapping_vendor` | "qax" | `—` | confirmed；使用平台/映射规则常量 mapping_vendor |
| `data_src_product` | `constant` | `constant.mapping_product` | "tianqing" | `—` | confirmed；使用平台/映射规则常量 mapping_product |
| `data_src_category` | `constant` | `constant.mapping_category` | "endpoint_security" | `—` | confirmed；使用平台/映射规则常量 mapping_category |
| `data_src_instance_id` | `context` | `platform_context.data_src_instance_id` | `platform_context.data_src_instance_id` | `—` | confirmed；由平台上下文提供 |
| `log_type` | `constant` | `constant.log_type` | "edr_process_inject" | `—` | confirmed；使用平台/映射规则常量 log_type |
| `log_name` | `constant` | `constant.log_name` | "天擎 EDR 进程注入" | `—` | confirmed；使用平台/映射规则常量 log_name |
| `record_kind` | `constant` | `constant.record_kind` | "activity" | `—` | confirmed；使用平台/映射规则常量 record_kind |
| `event_domain` | `constant` | `constant.event_domain` | "endpoint" | `—` | confirmed；使用平台/映射规则常量 event_domain |
| `severity` | `constant` | `constant.default_severity` | "info" | `—` | confirmed；当前日志类型未提供标准 severity，按映射默认值 info 装配 |
| `observer_vendor` | `constant` | `constant.mapping_vendor` | "qax" | `—` | confirmed；由平台厂商常量 qax 投影 |
| `observer_product` | `constant` | `constant.mapping_product` | "tianqing" | `—` | confirmed；由平台产品常量 tianqing 投影 |
| `roles.source.ref_id` | `derived` | `derived.entity_ref` | `derived.entity_ref` | `—` | confirmed；按确定性规则 entity_ref 派生 |
| `roles.source.entity_type` | `constant` | `constant.entity_type` | "host" | `—` | confirmed；使用平台/映射规则常量 entity_type |
| `roles.target.ref_id` | `derived` | `derived.entity_ref` | `derived.entity_ref` | `—` | confirmed；按确定性规则 entity_ref 派生 |
| `roles.target.entity_type` | `constant` | `constant.entity_type` | "process" | `—` | confirmed；使用平台/映射规则常量 entity_type |
| `roles.target.process.name` | `derived` | `derived.path_basename` | `derived.path_basename` | `—` | confirmed；由 target_process_path 取 basename 派生，不是 WPL 原始字段 |
| `roles.observer.product.name` | `constant` | `constant.mapping_product` | "tianqing" | `—` | confirmed；使用平台/映射规则常量 mapping_product |
| `roles.observer.device.vendor` | `constant` | `constant.mapping_vendor` | "qax" | `—` | confirmed；使用平台/映射规则常量 mapping_vendor |
| `roles.related[0].ref_id` | `derived` | `derived.entity_ref` | `derived.entity_ref` | `—` | confirmed；父进程无稳定 GUID；当前使用 tenant、主机和父进程稳定属性生成，必须保证跨主机不碰撞 |
| `roles.related[0].entity_type` | `constant` | `constant.entity_type` | "process" | `—` | confirmed；使用平台/映射规则常量 entity_type |
| `roles.related[0].relation_type` | `constant` | `constant.relation_type` | "parent_process" | `—` | confirmed；使用平台/映射规则常量 relation_type |
| `facets.process.injection.method` | `derived` | `derived.injection_method` | `derived.injection_method` | `—` | confirmed；同 operation 的候选注入方式；当前由目标线程 ID、地址和参数支持，需厂商枚举确认 |
| `extensions.profiles.endpoint_asset.subject_ref.ref_id` | `derived` | `derived.entity_ref` | `derived.entity_ref` | `—` | confirmed；按确定性规则 entity_ref 派生 |
| `extensions.profiles.endpoint_asset.agent.version` | `context` | `platform_context.env_version` | `platform_context.env_version` | `—` | confirmed；由平台上下文提供 |
| `outcome` | `constant` | `log_semantics` | "observed" | `—` | confirmed；由该日志类型的事件事实确定，不是来源枚举转换 |
| `ingest_time` | `context` | `platform_context.ingest_time` | `read(ingest_time)` | `—` | confirmed；expected 事件中的平台上下文字段 |
| `parse_time` | `context` | `platform_context.parse_time` | `read(parse_time)` | `—` | confirmed；expected 事件中的平台上下文字段 |
| `operation` | `constant` | `constant.log_semantics` | "remote_thread" | `—` | confirmed；当前日志类型的 expected 事件语义 |

### 5.2 Content 区

| SDM 字段 | 规则类型 | WPL 字段 | 映射/赋值 | 未命中 | 状态与证据 |
|---|---|---|---|---|---|
| `operation` | `dictionary` | `derived.enum_projection` | — | `preserve_in_extension_and_review` | partial；由目标线程证据推断为 remote_thread；execute_method_name 为空，需厂商方法枚举确认后才能固化 |
| `outcome` | `dictionary` | `derived.enum_projection` | — | `preserve_in_extension_and_review` | partial；由 WPL 枚举或日志语义转换为 SDM 标准值 |
| `source_user` | `projection` | `process_user` | `wpl.process_user` | `—` | confirmed；由 process_user 投影到事件标量字段 |
| `source_host` | `projection` | `computer_name` | `wpl.computer_name` | `—` | confirmed；由 computer_name 投影到事件标量字段 |
| `roles.source.host.id` | `projection` | `asset_id` | "2868257359929541780" | `—` | confirmed；按当前 expected 事件结构映射 |
| `extensions.profiles.endpoint_asset.ownership.organization.id` | `projection` | `asset_oid` | "2653788242175861718" | `—` | confirmed；按当前 expected 事件结构映射 |
| `extensions.profiles.endpoint_asset.agent.id` | `projection` | `client_id` | "8558772-6b168d97c3f346a96ed4ecef42be407a" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.source.host.name` | `projection` | `computer_name` | "DESKTOP-EX02" | `—` | confirmed；按当前 expected 事件结构映射 |
| `occur_time` | `projection` | `event_date_creation` | 1732787303894 | `—` | confirmed；按当前 expected 事件结构映射 |
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
| `roles.target.process.uid` | `projection` | `target_process_guid` | "a6a4e1ff66de42a7ec2477f188f04d96" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.target.process.pid` | `projection` | `target_process_id` | "6688" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.target.process.file.hashes.md5` | `projection` | `target_process_md5` | "8bfd0993e6af9b71f6ec20967e7f4e66" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.target.process.path` | `projection` | `target_process_path` | "C:\\Windows\\servicing\\TrustedInstaller.exe" | `—` | confirmed；目标进程名称由路径 basename 确定性派生 |
| `roles.target.process.file.signatures[0].signer` | `projection` | `target_process_sign` | "Microsoft Windows" | `—` | confirmed；按当前 expected 事件结构映射 |
| `facets.process.injection.target_thread.address` | `projection` | `target_thread_address` | "140701423552944" | `—` | confirmed；按当前 expected 事件结构映射 |
| `facets.process.injection.target_thread.arguments` | `projection` | `target_thread_args` | "718250356736" | `—` | confirmed；按当前 expected 事件结构映射 |
| `facets.process.injection.target_thread.id` | `projection` | `target_thread_id` | "17716" | `—` | confirmed；按当前 expected 事件结构映射 |
| `facets.process.injection.target_thread.module_path` | `projection` | `target_thread_module_path` | "C:\\Windows\\servicing\\TrustedInstaller.exe" | `—` | confirmed；按当前 expected 事件结构映射 |
| `source_original_event_id` | `projection` | `uuid` | "EAE19C3E-B634-4F6F-B138-4E498C068F72" | `—` | confirmed；按当前 expected 事件结构映射 |
| `event_type` | `dictionary` | `event_type` | "Process_Injection" -> "process_injection" | `preserve_in_extension_and_review` | partial；已确认枚举转换：Process_Injection 映射为 process_injection |

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
