# WPL → SDM Event 字段映射

> 样例：`process_terminate.expected-sdm-event.json`；WPL 字段 61 个，映射 45，不落库 14，排除 2。
> SDM 落位 = 词典逻辑路径（roles./facets./extensions.…）；expected 位置 = 该值在期望事件中的实际路径。

## 一、映射字段

| WPL 字段 | WPL 值 | SDM 落位 | expected 位置 | expected 值 | 说明 |
|---|---|---|---|---|---|
| `asset_oid` | "2653788242175861718" | extensions.source_private.organization.asset_oid | `extensions_obj.profiles.endpoint_asset.ownership.organization.id` | "2653788242175861718" | 组织资产节点 ID，三标准无锚点（国产组织模型） |
| `env_version` | "edr-8.0" | extensions.source_private.env_version | `extensions_obj.profiles.endpoint_asset.agent.version` | "edr-8.0" | 天擎环境版本，三标准无锚点 |
| `event_date_creation` | 1734490003718 | occur_time | `occur_time` | 1734490003718 | 来源原始事件时间；OCSF metadata.original_time 语义完全对应；UDM event_timestamp 已核实；XDM 字段树无事件时间页 |
| `uuid` | "C349D9C7-874E-4498-A87C-48D1B9630A93" | source_original_event_id | `source_original_event_id` | "C349D9C7-874E-4498-A87C-48D1B9630A93" | 来源原始事件 ID，参与确定性 event_id；UDM product_log_id 定义为 vendor GUID 完全对应 |
| `hostname` | "DESKTOP-EX01" | roles.source.host.name | `roles_obj.source.host.name` | "DESKTOP-EX01" | 受管终端主机名，与 computer_name 同义 |
| `process_name` | "conhost.exe" | roles.target.process.name | `roles_obj.target.process.name` | "conhost.exe" | UDM 进程无 name，名称在 file 对象 |
| `process_guid` | "3cce505ecc4f1c7666b3d9d10780517f" | roles.target.process.uid | `roles_obj.target.process.uid` | "3cce505ecc4f1c7666b3d9d10780517f" | 三标准均无 guid 字段名；32hex 可落 OCSF uid |
| `process_id` | "21888" | roles.target.process.pid | `roles_obj.target.process.pid` | "21888" | 与 pid 同值，取一即可 |
| `pid` | "21888" | roles.target.process.pid | `roles_obj.target.process.pid` | "21888" | 与 process_id 冲突时按来源定义定优先级并记录质量问题 |
| `process_path` | "C:\\Windows\\System32\\conhost.exe" | roles.target.process.path | `roles_obj.target.process.path` | "C:\\Windows\\System32\\conhost.exe" |  |
| `process_command_line` | "\\??\\C:\\WINDOWS\\system32\\conhost.exe 0xffffffff -ForceV1" | roles.target.process.cmdline | `roles_obj.target.process.cmdline` | "\\??\\C:\\WINDOWS\\system32\\conhost.exe 0xffffffff -ForceV1" | OCSF 字段名是 cmd_line 非 command_line |
| `process_md5` | "0f568f6c821565ab9ff45c7457953789" | roles.target.process.file.hashes.md5 | `roles_obj.target.process.file.hashes.md5` | "0f568f6c821565ab9ff45c7457953789" | 哈希统一小写 |
| `process_sha1` | "f948a4c5e01a74b17d0f966615834ba76dc1badc" | roles.target.process.file.hashes.sha1 | `roles_obj.target.process.file.hashes.sha1` | "f948a4c5e01a74b17d0f966615834ba76dc1badc" | XDM executable 无 sha1（只有 md5/sha256）；registry v17 已注册标准路径（target/source/carriers 进程 file 均可用） |
| `process_original_name` | "CONHOST.EXE" | roles.target.process.file.original_name | `roles_obj.target.process.file.original_name` | "CONHOST.EXE" | PE OriginalFilename；OCSF 无专门字段（internal_name 语义不同）；registry v17 已注册标准路径 |
| `process_internal_name` | "ConHost" | roles.target.process.file.internal_name | `roles_obj.target.process.file.internal_name` | "ConHost" | OCSF 字段名直接对应；05 已注册标准路径 |
| `process_company` | "Microsoft Corporation" | roles.target.process.file.company_name | `roles_obj.target.process.file.company_name` | "Microsoft Corporation" | 05 已注册标准路径 |
| `process_product` | "Microsoft Windows Operating System" | roles.target.process.file.product.name | `roles_obj.target.process.file.product.name` | "Microsoft Windows Operating System" | registry v17 已注册标准路径 |
| `process_description` | "Console Window Host" | roles.target.process.file.description | `roles_obj.target.process.file.description` | "Console Window Host" | registry v17 已注册标准路径 |
| `process_sign` | "Microsoft Windows" | roles.target.process.file.signatures[].signer | `roles_obj.target.process.file.signatures[0].signer` | "Microsoft Windows" | 05 已注册标准路径 |
| `process_version` | "10.0.19041.4355" | roles.target.process.file.version | `roles_obj.target.process.file.version` | "10.0.19041.4355" | UDM/XDM 无文件版本字段；registry v17 已注册标准路径 |
| `process_user` | "NT AUTHORITY\\NETWORK SERVICE" | roles.target.process.user.name | `roles_obj.target.process.user.name` | "NT AUTHORITY\\NETWORK SERVICE" | 当前进程的用户；角色由事件决定——process_event 落 target.process.user，ip_access/file_write 落 carriers[].process.user |
| `process_create_time` | "1734489800704" | extensions.source_private.process.create_time | `roles_obj.target.process.created_time` | 1734489800704 | OCSF process.created_time 存在；SDM 05 文档暂未新增此路径（terminated_time 已新增） |
| `process_current_directory` | "C:\\WINDOWS" | roles.target.process.working_directory | `roles_obj.target.process.working_directory` | "C:\\WINDOWS" | OCSF 字段名 working_directory 直接对应；05 已注册标准路径 |
| `process_integrity_level` | "System" | roles.target.process.integrity | `roles_obj.target.process.integrity` | "System" | 三标准都有锚点；05 已注册标准路径 |
| `process_terminate_time` | "1734490003718" | roles.target.process.terminated_time | `roles_obj.target.process.terminated_time` | 1734490003718 | OCSF process.terminated_time 存在；05 已注册标准路径；WPL 值 '0' 为哨兵不落 |
| `process_parent_name` | "gpupdate.exe" | roles.source.process.name | `roles_obj.related[0].process.name` | "gpupdate.exe" | XDM 只有 parent_id 平铺 ID，无父进程对象；父进程位置由事件类型决定（process_event 落 source.process，ip_access/file_write 落 related[]） |
| `process_parent_guid` | "ee87e43d28587ff02591eb39fa43ab15" | roles.source.process.uid | `roles_obj.related[0].process.uid` | "ee87e43d28587ff02591eb39fa43ab15" |  |
| `process_parent_id` | "21780" | roles.source.process.pid | `roles_obj.related[0].process.pid` | "21780" |  |
| `process_parent_path` | "C:\\Windows\\System32\\gpupdate.exe" | roles.source.process.path | `roles_obj.related[0].process.path` | "C:\\Windows\\System32\\gpupdate.exe" |  |
| `process_parent_command_line` | "gpupdate.exe /target:computer" | roles.source.process.cmdline | `roles_obj.related[0].process.cmdline` | "gpupdate.exe /target:computer" |  |
| `process_parent_internal_name` | "GPUpdate.exe" | roles.source.process.file.internal_name | `roles_obj.related[0].process.file.internal_name` | "GPUpdate.exe" | 父进程位置由事件类型决定（process_event 落 source.process，ip_access/file_write 落 related[]） |
| `process_parent_original_name` | "GPUpdate.exe" | roles.source.process.file.original_name | `roles_obj.related[0].process.file.original_name` | "GPUpdate.exe" | 同 process_original_name；父进程位置由事件类型决定 |
| `process_parent_sign` | "Microsoft Windows" | roles.source.process.file.signatures[].signer | `roles_obj.related[0].process.file.signatures[0].signer` | "Microsoft Windows" | 父进程位置由事件类型决定 |
| `process_pparent_name` | "svchost.exe" | roles.carriers[1].process.name | `roles_obj.related[1].process.name` | "svchost.exe" | XDM 无祖父进程对象（parent_id 仅一层） |
| `process_pparent_path` | "C:\\Windows\\System32\\svchost.exe" | roles.carriers[1].process.path | `roles_obj.related[1].process.path` | "C:\\Windows\\System32\\svchost.exe" |  |
| `process_pparent_command_line` | "C:\\WINDOWS\\system32\\svchost.exe -k netsvcs -p -s Schedule" | roles.carriers[1].process.cmdline | `roles_obj.related[1].process.cmdline` | "C:\\WINDOWS\\system32\\svchost.exe -k netsvcs -p -s Schedule" |  |
| `computer_name` | "DESKTOP-EX01" | roles.source.host.name | `roles_obj.source.host.name` | "DESKTOP-EX01" | 受管终端主机名，投影 source_host |
| `ip` | "192.0.2.206" | roles.source.host.ip | `roles_obj.source.host.ip` | "192.0.2.206" | 终端属性 IP，不自动投影 source_ip；OCSF device.ip 弃用转 network_interfaces |
| `client_ip` | "192.0.2.206" | roles.source.host.ip | `roles_obj.source.host.ip` | "192.0.2.206" | 与 ip/report_ip 冲突时按 doc14 优先级 client_ip>ip>report_ip |
| `asset_id` | "2868257359929541780" | extensions.profiles.endpoint_asset.asset.id | `roles_obj.source.host.id` | "2868257359929541780" | 受管终端资产 ID，参与 host_ref_id |
| `client_id` | "8558772-6b168d97c3f346a96ed4ecef42be407a" | extensions.profiles.endpoint_asset.agent.id | `extensions_obj.profiles.endpoint_asset.agent.id` | "8558772-6b168d97c3f346a96ed4ecef42be407a" | 天擎 Agent ID，不等于 asset_id；OCSF 以 device.uid 承载 agent 设备 |
| `mid` | "1ca36f97756b33c2bf9139aab6ac36926903b9ec24e0009fae93fda96ded6898" | extensions.profiles.endpoint_asset.agent.fingerprint_id | `extensions_obj.profiles.endpoint_asset.agent.fingerprint_id` | "1ca36f97756b33c2bf9139aab6ac36926903b9ec24e0009fae93fda96ded6898" | Agent/终端指纹，三标准无锚点 |
| `gid` | "4f9c3833b800d1f7" | extensions.profiles.endpoint_asset.ownership.group.id | `extensions_obj.profiles.endpoint_asset.ownership.group.id` | "4f9c3833b800d1f7" | 资产分组 ID，三标准无锚点 |
| `group_name` | "未分组终端" | extensions.profiles.endpoint_asset.ownership.group.name | `extensions_obj.profiles.endpoint_asset.ownership.group.name` | "未分组终端" | 资产分组名，三标准无锚点 |
| `user_logon_id` | "S-1-5-20" | extensions.source_private.user.logon_id | `roles_obj.target.process.user.id` | "S-1-5-20" | SID（S-1-5-20）非用户名称；UDM windows_sid/XDM sid 已核实 |

## 二、不落库字段

| WPL 字段 | WPL 值 | 原因 |
|---|---|---|
| `type` | "process_details" | WPL 规则类型 process_details，非标准字段；SDM 保留原值 |
| `task_id` | "task-poc-20241218-02" | 采集任务上下文，三标准无锚点 |
| `sub_task_id` | "subtask-poc-02" | 采集子任务上下文，三标准无锚点 |
| `custom_group_paths` | ",2868260887305703927,4f9c3833b800d1f7" | 组织分组路径原始串，三标准无锚点 |
| `timestamp` | 1734490020000 | 备用事件时间，仅 event_date_creation 缺失时用 |
| `event_type` | "process_terminate" | 天擎动作枚举，SDM 侧按转换表映射 process_launch/process_termination/process_uncategorized |
| `create_time` | 1734489763299 | 终端资产创建时间，非事件时间；OCSF device.first_seen 语义近似；禁止覆盖 occur_time |
| `logger` | "tianqing-agent" | tianqing-agent；OCSF logger 对象已核实；SDM 产品信息已在 observer 表达，不落 |
| `process_root_guid` | "" | WPL 值为空；与父/祖重合时去重，根进程 ID 可落 OCSF ancestry |
| `process_root_id` | "0" | WPL 值为 '0' 哨兵不落 |
| `client_report_ip` | "203.0.113.45" | 上报出口 IP（terminate 样例与 client_ip 不同 203.0.113.45）；三标准无直接锚点，值不同时必须保留（unmapped 或私有） |
| `report_ip` | "203.0.113.45" | 同 client_report_ip；与 client_ip 不同时禁止静默丢弃 |
| `mac` | "00-00-5E-00-53-C6" | SDM host 对象无 mac 路径（05 文档），暂落私有；OCSF/XDM 主机 mac 锚点已核实 |
| `user_session_id` | "0" | OCSF process.session 已核实；确认是认证会话 ID 时才进 facets.authentication.session_id，否则私有 |

## 三、排除字段（原始载荷）

| WPL 字段 | 说明 |
|---|---|
| `raw_msg` | 原始日志载荷，不参与映射（用户规则 2026-08-05）；经 event_id 回查 |
| `payload` | 原始日志载荷，不参与映射；payload/raw_msg 同语义（厂商命名差异） |

## 五、WPL/OML 编写规则

> WPL 只负责提取表中的 source 字段；Meta 和 Content 的赋值由 OML 按下表实现。
> `partial` 表示当前只有样例值或局部说明，不能视为完整厂商字典。

### 5.1 Meta 区

| SDM 字段 | 规则类型 | 输入/来源 | 赋值 | 未命中 | 状态与证据 |
|---|---|---|---|---|---|
| `log_id` | `context` | `platform_context.log_id` | `read(log_id)` | `—` | confirmed；expected 事件中的平台上下文字段 |
| `tenant_id` | `context` | `platform_context.tenant_id` | `read(tenant_id)` | `—` | confirmed；expected 事件中的平台上下文字段 |
| `ingest_time` | `context` | `platform_context.ingest_time` | `read(ingest_time)` | `—` | confirmed；expected 事件中的平台上下文字段 |
| `parse_time` | `context` | `platform_context.parse_time` | `read(parse_time)` | `—` | confirmed；expected 事件中的平台上下文字段 |
| `data_src_instance_id` | `context` | `platform_context.data_src_instance_id` | `read(data_src_instance_id)` | `—` | confirmed；expected 事件中的平台上下文字段 |
| `schema_version` | `constant` | `constant.schema_version` | 2 | `—` | confirmed；expected 事件确认的日志类型级常量 |
| `observer_vendor` | `constant` | `constant.observer_vendor` | "qax" | `—` | confirmed；expected 事件确认的日志类型级常量 |
| `data_src_vendor` | `constant` | `constant.data_src_vendor` | "qax" | `—` | confirmed；expected 事件确认的日志类型级常量 |
| `observer_product` | `constant` | `constant.observer_product` | "tianqing" | `—` | confirmed；expected 事件确认的日志类型级常量 |
| `mapping_id` | `constant` | `constant.mapping_id` | "qax.tianqing.edr_process_event" | `—` | confirmed；expected 事件确认的日志类型级常量 |
| `event_domain` | `constant` | `constant.event_domain` | "endpoint" | `—` | confirmed；expected 事件确认的日志类型级常量 |
| `data_src_product` | `constant` | `constant.data_src_product` | "tianqing" | `—` | confirmed；expected 事件确认的日志类型级常量 |
| `log_type` | `constant` | `constant.log_type` | "edr_process_event" | `—` | confirmed；expected 事件确认的日志类型级常量 |
| `data_src_category` | `constant` | `constant.data_src_category` | "endpoint_security" | `—` | confirmed；expected 事件确认的日志类型级常量 |
| `log_name` | `constant` | `constant.log_name` | "天擎 EDR 进程事件" | `—` | confirmed；expected 事件确认的日志类型级常量 |
| `record_kind` | `constant` | `constant.record_kind` | "activity" | `—` | confirmed；expected 事件确认的日志类型级常量 |
| `event_category` | `constant` | `constant.log_semantics` | "audit" | `—` | confirmed；EDR 行为监控进程事件，PDF §3.9.1 |
| `outcome` | `constant` | `constant.log_semantics` | "observed" | `—` | confirmed；当前日志类型的 expected 事件语义 |
| `severity` | `constant` | `constant.log_semantics` | "info" | `—` | confirmed；当前日志类型的 expected 事件语义 |

### 5.2 Content 区

| SDM 字段 | 规则类型 | WPL 字段 | 映射/赋值 | 未命中 | 状态与证据 |
|---|---|---|---|---|---|
| `extensions.source_private.organization.asset_oid` | `projection` | `asset_oid` | "2653788242175861718" | `—` | confirmed；组织资产节点 ID，三标准无锚点（国产组织模型） |
| `extensions.source_private.env_version` | `projection` | `env_version` | "edr-8.0" | `—` | confirmed；天擎环境版本，三标准无锚点 |
| `occur_time` | `projection` | `event_date_creation` | 1734490003718 | `—` | confirmed；来源原始事件时间；OCSF metadata.original_time 语义完全对应；UDM event_timestamp 已核实；XDM 字段树无事件时间页 |
| `source_original_event_id` | `projection` | `uuid` | "C349D9C7-874E-4498-A87C-48D1B9630A93" | `—` | confirmed；来源原始事件 ID，参与确定性 event_id；UDM product_log_id 定义为 vendor GUID 完全对应 |
| `roles.source.host.name` | `projection` | `hostname` | "DESKTOP-EX01" | `—` | confirmed；受管终端主机名，与 computer_name 同义 |
| `roles.target.process.name` | `projection` | `process_name` | "conhost.exe" | `—` | confirmed；UDM 进程无 name，名称在 file 对象 |
| `roles.target.process.uid` | `projection` | `process_guid` | "3cce505ecc4f1c7666b3d9d10780517f" | `—` | confirmed；三标准均无 guid 字段名；32hex 可落 OCSF uid |
| `roles.target.process.pid` | `projection` | `process_id` | "21888" | `—` | confirmed；与 pid 同值，取一即可 |
| `roles.target.process.pid` | `projection` | `pid` | "21888" | `—` | confirmed；与 process_id 冲突时按来源定义定优先级并记录质量问题 |
| `roles.target.process.path` | `projection` | `process_path` | "C:\\Windows\\System32\\conhost.exe" | `—` | confirmed； |
| `roles.target.process.cmdline` | `projection` | `process_command_line` | "\\??\\C:\\WINDOWS\\system32\\conhost.exe 0xffffffff -ForceV1" | `—` | confirmed；OCSF 字段名是 cmd_line 非 command_line |
| `roles.target.process.file.hashes.md5` | `projection` | `process_md5` | "0f568f6c821565ab9ff45c7457953789" | `—` | confirmed；哈希统一小写 |
| `roles.target.process.file.hashes.sha1` | `projection` | `process_sha1` | "f948a4c5e01a74b17d0f966615834ba76dc1badc" | `—` | confirmed；XDM executable 无 sha1（只有 md5/sha256）；registry v17 已注册标准路径（target/source/carriers 进程 file 均可用） |
| `roles.target.process.file.original_name` | `projection` | `process_original_name` | "CONHOST.EXE" | `—` | confirmed；PE OriginalFilename；OCSF 无专门字段（internal_name 语义不同）；registry v17 已注册标准路径 |
| `roles.target.process.file.internal_name` | `projection` | `process_internal_name` | "ConHost" | `—` | confirmed；OCSF 字段名直接对应；05 已注册标准路径 |
| `roles.target.process.file.company_name` | `projection` | `process_company` | "Microsoft Corporation" | `—` | confirmed；05 已注册标准路径 |
| `roles.target.process.file.product.name` | `projection` | `process_product` | "Microsoft Windows Operating System" | `—` | confirmed；registry v17 已注册标准路径 |
| `roles.target.process.file.description` | `projection` | `process_description` | "Console Window Host" | `—` | confirmed；registry v17 已注册标准路径 |
| `roles.target.process.file.signatures[].signer` | `projection` | `process_sign` | "Microsoft Windows" | `—` | confirmed；05 已注册标准路径 |
| `roles.target.process.file.version` | `projection` | `process_version` | "10.0.19041.4355" | `—` | confirmed；UDM/XDM 无文件版本字段；registry v17 已注册标准路径 |
| `roles.target.process.user.name` | `projection` | `process_user` | "NT AUTHORITY\\NETWORK SERVICE" | `—` | confirmed；当前进程的用户；角色由事件决定——process_event 落 target.process.user，ip_access/file_write 落 carriers[].process.user |
| `extensions.source_private.process.create_time` | `projection` | `process_create_time` | 1734489800704 | `—` | confirmed；OCSF process.created_time 存在；SDM 05 文档暂未新增此路径（terminated_time 已新增） |
| `roles.target.process.working_directory` | `projection` | `process_current_directory` | "C:\\WINDOWS" | `—` | confirmed；OCSF 字段名 working_directory 直接对应；05 已注册标准路径 |
| `roles.target.process.integrity` | `projection` | `process_integrity_level` | "System" | `—` | confirmed；三标准都有锚点；05 已注册标准路径 |
| `roles.target.process.terminated_time` | `projection` | `process_terminate_time` | 1734490003718 | `—` | confirmed；OCSF process.terminated_time 存在；05 已注册标准路径；WPL 值 '0' 为哨兵不落 |
| `roles.source.process.name` | `projection` | `process_parent_name` | "gpupdate.exe" | `—` | confirmed；XDM 只有 parent_id 平铺 ID，无父进程对象；父进程位置由事件类型决定（process_event 落 source.process，ip_access/file_write 落 related[]） |
| `roles.source.process.uid` | `projection` | `process_parent_guid` | "ee87e43d28587ff02591eb39fa43ab15" | `—` | confirmed； |
| `roles.source.process.pid` | `projection` | `process_parent_id` | "21780" | `—` | confirmed； |
| `roles.source.process.path` | `projection` | `process_parent_path` | "C:\\Windows\\System32\\gpupdate.exe" | `—` | confirmed； |
| `roles.source.process.cmdline` | `projection` | `process_parent_command_line` | "gpupdate.exe /target:computer" | `—` | confirmed； |
| `roles.source.process.file.internal_name` | `projection` | `process_parent_internal_name` | "GPUpdate.exe" | `—` | confirmed；父进程位置由事件类型决定（process_event 落 source.process，ip_access/file_write 落 related[]） |
| `roles.source.process.file.original_name` | `projection` | `process_parent_original_name` | "GPUpdate.exe" | `—` | confirmed；同 process_original_name；父进程位置由事件类型决定 |
| `roles.source.process.file.signatures[].signer` | `projection` | `process_parent_sign` | "Microsoft Windows" | `—` | confirmed；父进程位置由事件类型决定 |
| `roles.carriers[1].process.name` | `projection` | `process_pparent_name` | "svchost.exe" | `—` | confirmed；XDM 无祖父进程对象（parent_id 仅一层） |
| `roles.carriers[1].process.path` | `projection` | `process_pparent_path` | "C:\\Windows\\System32\\svchost.exe" | `—` | confirmed； |
| `roles.carriers[1].process.cmdline` | `projection` | `process_pparent_command_line` | "C:\\WINDOWS\\system32\\svchost.exe -k netsvcs -p -s Schedule" | `—` | confirmed； |
| `roles.source.host.name` | `projection` | `computer_name` | "DESKTOP-EX01" | `—` | confirmed；受管终端主机名，投影 source_host |
| `roles.source.host.ip` | `projection` | `ip` | "192.0.2.206" | `—` | confirmed；终端属性 IP，不自动投影 source_ip；OCSF device.ip 弃用转 network_interfaces |
| `roles.source.host.ip` | `projection` | `client_ip` | "192.0.2.206" | `—` | confirmed；与 ip/report_ip 冲突时按 doc14 优先级 client_ip>ip>report_ip |
| `extensions.profiles.endpoint_asset.asset.id` | `projection` | `asset_id` | "2868257359929541780" | `—` | confirmed；受管终端资产 ID，参与 host_ref_id |
| `extensions.profiles.endpoint_asset.agent.id` | `projection` | `client_id` | "8558772-6b168d97c3f346a96ed4ecef42be407a" | `—` | confirmed；天擎 Agent ID，不等于 asset_id；OCSF 以 device.uid 承载 agent 设备 |
| `extensions.profiles.endpoint_asset.agent.fingerprint_id` | `projection` | `mid` | "1ca36f97756b33c2bf9139aab6ac36926903b9ec24e0009fae93fda96ded6898" | `—` | confirmed；Agent/终端指纹，三标准无锚点 |
| `extensions.profiles.endpoint_asset.ownership.group.id` | `projection` | `gid` | "4f9c3833b800d1f7" | `—` | confirmed；资产分组 ID，三标准无锚点 |
| `extensions.profiles.endpoint_asset.ownership.group.name` | `projection` | `group_name` | "未分组终端" | `—` | confirmed；资产分组名，三标准无锚点 |
| `extensions.source_private.user.logon_id` | `projection` | `user_logon_id` | "S-1-5-20" | `—` | confirmed；SID（S-1-5-20）非用户名称；UDM windows_sid/XDM sid 已核实 |
| `event_type` | `dictionary` | `event_type` | "process_terminate" -> "process_termination" | `preserve_in_extension_and_review` | partial；天擎动作枚举，SDM 侧按转换表映射 process_launch/process_termination/process_uncategorized |

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
