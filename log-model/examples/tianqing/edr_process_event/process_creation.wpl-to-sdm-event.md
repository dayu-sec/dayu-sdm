# WPL → SDM Event 字段映射

> 样例：`process_creation.expected-sdm-event.json`；WPL 字段 62 个，映射 46，不落库 14，排除 2；另有平台默认、派生及结构字段 0 项。
> SDM 落位为逻辑路径；expected 位置为该样例中的实际物理 JSON 路径。

## 一、映射字段

| WPL 字段 | WPL 值 | SDM 落位 | expected 位置 | expected 值 | 说明 |
|---|---|---|---|---|---|
| `asset_oid` | "2653788242175861718" | `extensions.profiles.endpoint_asset.ownership.organization.id` | `extensions_obj.profiles.endpoint_asset.ownership.organization.id` | "2653788242175861718" | 组织资产节点 ID，三标准无锚点（国产组织模型） |
| `env_version` | "edr-8.0" | `extensions.profiles.endpoint_asset.agent.version` | `extensions_obj.profiles.endpoint_asset.agent.version` | "edr-8.0" | 天擎环境版本，三标准无锚点 |
| `event_date_creation` | 1734489737220 | `occur_time` | `occur_time` | 1734489737220 | 来源原始事件时间；OCSF metadata.original_time 语义完全对应；UDM event_timestamp 已核实；XDM 字段树无事件时间页 |
| `uuid` | "61794FDE-6769-464E-B071-6CE07B01FEE3" | `source_original_event_id` | `source_original_event_id` | "61794FDE-6769-464E-B071-6CE07B01FEE3" | 来源原始事件 ID，参与确定性 event_id；UDM product_log_id 定义为 vendor GUID 完全对应 |
| `hostname` | "DESKTOP-NU779RJ" | `roles.source.host.name` | `roles_obj.source.host.name` | "DESKTOP-NU779RJ" | 受管终端主机名，与 computer_name 同义 |
| `process_name` | "WmiPrvSE.exe" | `roles.target.process.name` | `roles_obj.target.process.name` | "WmiPrvSE.exe" | UDM 进程无 name，名称在 file 对象 |
| `process_guid` | "c943cfef43098320c2da9caecac9a87a" | `roles.target.process.uid` | `roles_obj.target.process.uid` | "c943cfef43098320c2da9caecac9a87a" | 三标准均无 guid 字段名；32hex 可落 OCSF uid |
| `process_id` | "16124" | `roles.target.process.pid` | `roles_obj.target.process.pid` | "16124" | 与 pid 同值，取一即可 |
| `pid` | "16124" | `roles.target.process.pid` | `roles_obj.target.process.pid` | "16124" | 与 process_id 冲突时按来源定义定优先级并记录质量问题 |
| `process_path` | "C:\\Windows\\System32\\wbem\\WmiPrvSE.exe" | `roles.target.process.path` | `roles_obj.target.process.path` | "C:\\Windows\\System32\\wbem\\WmiPrvSE.exe" |  |
| `process_command_line` | "C:\\Windows\\System32\\wbem\\WmiPrvSE.exe -secured -Embedding" | `roles.target.process.cmdline` | `roles_obj.target.process.cmdline` | "C:\\Windows\\System32\\wbem\\WmiPrvSE.exe -secured -Embedding" | OCSF 字段名是 cmd_line 非 command_line |
| `process_md5` | "8bb61c2b1e34ff3c778cf150bdf08238" | `roles.target.process.file.hashes.md5` | `roles_obj.target.process.file.hashes.md5` | "8bb61c2b1e34ff3c778cf150bdf08238" | 哈希统一小写 |
| `process_sha1` | "7f530281c5ba86b81ae4230dab1617cb55260d9e" | `roles.target.process.file.hashes.sha1` | `roles_obj.target.process.file.hashes.sha1` | "7f530281c5ba86b81ae4230dab1617cb55260d9e" | XDM executable 无 sha1（只有 md5/sha256）；registry v17 已注册标准路径（target/source/carriers 进程 file 均可用） |
| `process_original_name` | "Wmiprvse.exe" | `roles.target.process.file.original_name` | `roles_obj.target.process.file.original_name` | "Wmiprvse.exe" | PE OriginalFilename；OCSF 无专门字段（internal_name 语义不同）；registry v17 已注册标准路径 |
| `process_internal_name` | "Wmiprvse.exe" | `roles.target.process.file.internal_name` | `roles_obj.target.process.file.internal_name` | "Wmiprvse.exe" | OCSF 字段名直接对应；05 已注册标准路径 |
| `process_company` | "Microsoft Corporation" | `roles.target.process.file.company_name` | `roles_obj.target.process.file.company_name` | "Microsoft Corporation" | 05 已注册标准路径 |
| `process_product` | "Microsoft Windows Operating System" | `roles.target.process.file.product.name` | `roles_obj.target.process.file.product.name` | "Microsoft Windows Operating System" | registry v17 已注册标准路径 |
| `process_description` | "WMI Provider Host" | `roles.target.process.file.description` | `roles_obj.target.process.file.description` | "WMI Provider Host" | registry v17 已注册标准路径 |
| `process_sign` | "Microsoft Windows Publisher" | `roles.target.process.file.signatures[0].signer` | `roles_obj.target.process.file.signatures[0].signer` | "Microsoft Windows Publisher" | 05 已注册标准路径 |
| `process_version` | "10.0.19041.3636" | `roles.target.process.file.version` | `roles_obj.target.process.file.version` | "10.0.19041.3636" | UDM/XDM 无文件版本字段；registry v17 已注册标准路径 |
| `process_user` | "NT AUTHORITY\\NETWORK SERVICE" | `roles.target.process.user.name` | `roles_obj.target.process.user.name` | "NT AUTHORITY\\NETWORK SERVICE" | 当前进程的用户；角色由事件决定——process_event 落 target.process.user，ip_access/file_write 落 carriers[].process.user |
| `process_create_time` | "1734489700704" | `roles.target.process.created_time` | `roles_obj.target.process.created_time` | 1734489700704 | OCSF process.created_time 存在；SDM 05 文档暂未新增此路径（terminated_time 已新增） |
| `process_current_directory` | "C:\\Windows\\System32\\" | `roles.target.process.working_directory` | `roles_obj.target.process.working_directory` | "C:\\Windows\\System32\\" | OCSF 字段名 working_directory 直接对应；05 已注册标准路径 |
| `process_integrity_level` | "System" | `roles.target.process.integrity` | `roles_obj.target.process.integrity` | "System" | 三标准都有锚点；05 已注册标准路径 |
| `process_parent_name` | "svchost.exe" | `roles.source.process.name` | `roles_obj.source.process.name` | "svchost.exe" | XDM 只有 parent_id 平铺 ID，无父进程对象；父进程位置由事件类型决定（process_event 落 source.process，ip_access/file_write 落 related[]） |
| `process_parent_guid` | "d22b3fbcb9e77cb86834f6a18e2e0f68" | `roles.source.process.uid` | `roles_obj.source.process.uid` | "d22b3fbcb9e77cb86834f6a18e2e0f68" |  |
| `process_parent_id` | "844" | `roles.source.process.pid` | `roles_obj.source.process.pid` | "844" |  |
| `process_parent_path` | "C:\\Windows\\System32\\svchost.exe" | `roles.source.process.path` | `roles_obj.source.process.path` | "C:\\Windows\\System32\\svchost.exe" |  |
| `process_parent_command_line` | "C:\\Windows\\system32\\svchost.exe -k DcomLaunch -p" | `roles.source.process.cmdline` | `roles_obj.source.process.cmdline` | "C:\\Windows\\system32\\svchost.exe -k DcomLaunch -p" |  |
| `process_parent_internal_name` | "svchost.exe" | `roles.source.process.file.internal_name` | `roles_obj.source.process.file.internal_name` | "svchost.exe" | 父进程位置由事件类型决定（process_event 落 source.process，ip_access/file_write 落 related[]） |
| `process_parent_original_name` | "svchost.exe" | `roles.source.process.file.original_name` | `roles_obj.source.process.file.original_name` | "svchost.exe" | 同 process_original_name；父进程位置由事件类型决定 |
| `process_parent_sign` | "Microsoft Windows Publisher" | `roles.source.process.file.signatures[0].signer` | `roles_obj.source.process.file.signatures[0].signer` | "Microsoft Windows Publisher" | 父进程位置由事件类型决定 |
| `process_pparent_name` | "services.exe" | `roles.related[0].process.name` | `roles_obj.related[0].process.name` | "services.exe" | XDM 无祖父进程对象（parent_id 仅一层） |
| `process_pparent_path` | "C:\\WINDOWS\\system32\\services.exe" | `roles.related[0].process.path` | `roles_obj.related[0].process.path` | "C:\\WINDOWS\\system32\\services.exe" |  |
| `process_pparent_command_line` | "C:\\WINDOWS\\system32\\services.exe" | `roles.related[0].process.path` | `roles_obj.related[0].process.path` | "C:\\WINDOWS\\system32\\services.exe" |  |
| `computer_name` | "DESKTOP-NU779RJ" | `roles.source.host.name` | `roles_obj.source.host.name` | "DESKTOP-NU779RJ" | 受管终端主机名，投影 source_host |
| `ip` | "198.51.100.211" | `roles.source.host.ip` | `roles_obj.source.host.ip` | "198.51.100.211" | 终端属性 IP，不自动投影 source_ip；OCSF device.ip 弃用转 network_interfaces |
| `client_ip` | "198.51.100.211" | `roles.source.host.ip` | `roles_obj.source.host.ip` | "198.51.100.211" | 与 ip/report_ip 冲突时按 doc14 优先级 client_ip>ip>report_ip |
| `client_report_ip` | "198.51.100.211" | `roles.source.host.ip` | `roles_obj.source.host.ip` | "198.51.100.211" | 上报出口 IP（terminate 样例与 client_ip 不同 203.0.113.45）；三标准无直接锚点，值不同时必须保留（unmapped 或私有） |
| `report_ip` | "198.51.100.211" | `roles.source.host.ip` | `roles_obj.source.host.ip` | "198.51.100.211" | 同 client_report_ip；与 client_ip 不同时禁止静默丢弃 |
| `asset_id` | "2868257359929541780" | `roles.source.host.id` | `roles_obj.source.host.id` | "2868257359929541780" | 受管终端资产 ID，参与 host_ref_id |
| `client_id` | "0881058-dfb9a23257c64098060e699601b17217" | `extensions.profiles.endpoint_asset.agent.id` | `extensions_obj.profiles.endpoint_asset.agent.id` | "0881058-dfb9a23257c64098060e699601b17217" | 天擎 Agent ID，不等于 asset_id；OCSF 以 device.uid 承载 agent 设备 |
| `mid` | "ec80b820d87d7cd7ac916240bcdff7215ae3118feaf070c13afbf06e69af4eb3" | `extensions.profiles.endpoint_asset.agent.fingerprint_id` | `extensions_obj.profiles.endpoint_asset.agent.fingerprint_id` | "ec80b820d87d7cd7ac916240bcdff7215ae3118feaf070c13afbf06e69af4eb3" | Agent/终端指纹，三标准无锚点 |
| `gid` | "4f9c3833b800d1f7" | `extensions.profiles.endpoint_asset.ownership.group.id` | `extensions_obj.profiles.endpoint_asset.ownership.group.id` | "4f9c3833b800d1f7" | 资产分组 ID，三标准无锚点 |
| `group_name` | "未分组终端" | `extensions.profiles.endpoint_asset.ownership.group.name` | `extensions_obj.profiles.endpoint_asset.ownership.group.name` | "未分组终端" | 资产分组名，三标准无锚点 |
| `user_logon_id` | "S-1-5-20" | `roles.target.process.user.id` | `roles_obj.target.process.user.id` | "S-1-5-20" | SID（S-1-5-20）非用户名称；UDM windows_sid/XDM sid 已核实 |

## 二、不落库字段

| WPL 字段 | WPL 值 | 原因 |
|---|---|---|
| `type` | "process_details" | WPL 规则类型 process_details，非标准字段；SDM 保留原值 |
| `task_id` | "task-poc-20241218-01" | 采集任务上下文，三标准无锚点 |
| `sub_task_id` | "subtask-poc-01" | 采集子任务上下文，三标准无锚点 |
| `custom_group_paths` | ",2868260887305703927,4f9c3833b800d1f7" | 组织分组路径原始串，三标准无锚点 |
| `timestamp` | 1734489754000 | 条件回退字段：仅主事件时间缺失或无效时用于 occur_time；本样例未采用 |
| `event_type` | "process_creation" | 天擎动作枚举，SDM 侧按转换表映射 process_launch/process_termination/process_uncategorized |
| `create_time` | 1734489763299 | 终端资产创建时间，非事件时间；OCSF device.first_seen 语义近似；禁止覆盖 occur_time |
| `logger` | "tianqing-agent" | tianqing-agent；OCSF logger 对象已核实；SDM 产品信息已在 observer 表达，不落 |
| `process_copyright` | "" | 三标准均无；WPL 值为空，不落 |
| `process_terminate_time` | "0" | OCSF process.terminated_time 存在；05 已注册标准路径；WPL 值 '0' 为哨兵不落 |
| `process_root_guid` | "" | WPL 值为空；与父/祖重合时去重，根进程 ID 可落 OCSF ancestry |
| `process_root_id` | "0" | WPL 值为 '0' 哨兵不落 |
| `mac` | "00-00-5E-00-53-79" | SDM host 对象无 mac 路径（05 文档），暂落私有；OCSF/XDM 主机 mac 锚点已核实 |
| `user_session_id` | "0" | OCSF process.session 已核实；确认是认证会话 ID 时才进 facets.authentication.session_id，否则私有 |

## 三、排除字段（重复或空载荷）

| WPL 字段 | 说明 |
|---|---|
| `raw_msg` | 原始日志载荷，不参与映射（用户规则 2026-08-05）；经 event_id 回查 |
| `payload` | 原始日志载荷，不参与映射；payload/raw_msg 同语义（厂商命名差异） |

## 四、平台默认、派生及结构字段

| 来源 | SDM 落位 | expected 值 | 赋值责任与说明 |
|---|---|---|---|

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
| `event_type` | `constant` | `constant.log_semantics` | "process_launch" | `—` | confirmed；当前日志类型的 expected 事件语义 |
| `event_category` | `constant` | `constant.log_semantics` | "audit" | `—` | confirmed；EDR 行为监控进程事件，PDF §3.9.1 |
| `operation` | `constant` | `constant.log_semantics` | "spawn" | `—` | confirmed；当前日志类型的 expected 事件语义 |
| `outcome` | `constant` | `constant.log_semantics` | "observed" | `—` | confirmed；当前日志类型的 expected 事件语义 |
| `severity` | `constant` | `constant.log_semantics` | "info" | `—` | confirmed；当前日志类型的 expected 事件语义 |

### 5.2 Content 区

| SDM 字段 | 规则类型 | WPL 字段 | 映射/赋值 | 未命中 | 状态与证据 |
|---|---|---|---|---|---|
| `extensions.profiles.endpoint_asset.ownership.organization.id` | `projection` | `asset_oid` | "2653788242175861718" | `—` | confirmed；组织资产节点 ID，三标准无锚点（国产组织模型） |
| `extensions.profiles.endpoint_asset.agent.version` | `projection` | `env_version` | "edr-8.0" | `—` | confirmed；天擎环境版本，三标准无锚点 |
| `occur_time` | `projection` | `event_date_creation` | 1734489737220 | `—` | confirmed；来源原始事件时间；OCSF metadata.original_time 语义完全对应；UDM event_timestamp 已核实；XDM 字段树无事件时间页 |
| `source_original_event_id` | `projection` | `uuid` | "61794FDE-6769-464E-B071-6CE07B01FEE3" | `—` | confirmed；来源原始事件 ID，参与确定性 event_id；UDM product_log_id 定义为 vendor GUID 完全对应 |
| `roles.source.host.name` | `projection` | `hostname` | "DESKTOP-NU779RJ" | `—` | confirmed；受管终端主机名，与 computer_name 同义 |
| `roles.target.process.name` | `projection` | `process_name` | "WmiPrvSE.exe" | `—` | confirmed；UDM 进程无 name，名称在 file 对象 |
| `roles.target.process.uid` | `projection` | `process_guid` | "c943cfef43098320c2da9caecac9a87a" | `—` | confirmed；三标准均无 guid 字段名；32hex 可落 OCSF uid |
| `roles.target.process.pid` | `projection` | `process_id` | "16124" | `—` | confirmed；与 pid 同值，取一即可 |
| `roles.target.process.pid` | `projection` | `pid` | "16124" | `—` | confirmed；与 process_id 冲突时按来源定义定优先级并记录质量问题 |
| `roles.target.process.path` | `projection` | `process_path` | "C:\\Windows\\System32\\wbem\\WmiPrvSE.exe" | `—` | confirmed； |
| `roles.target.process.cmdline` | `projection` | `process_command_line` | "C:\\Windows\\System32\\wbem\\WmiPrvSE.exe -secured -Embedding" | `—` | confirmed；OCSF 字段名是 cmd_line 非 command_line |
| `roles.target.process.file.hashes.md5` | `projection` | `process_md5` | "8bb61c2b1e34ff3c778cf150bdf08238" | `—` | confirmed；哈希统一小写 |
| `roles.target.process.file.hashes.sha1` | `projection` | `process_sha1` | "7f530281c5ba86b81ae4230dab1617cb55260d9e" | `—` | confirmed；XDM executable 无 sha1（只有 md5/sha256）；registry v17 已注册标准路径（target/source/carriers 进程 file 均可用） |
| `roles.target.process.file.original_name` | `projection` | `process_original_name` | "Wmiprvse.exe" | `—` | confirmed；PE OriginalFilename；OCSF 无专门字段（internal_name 语义不同）；registry v17 已注册标准路径 |
| `roles.target.process.file.internal_name` | `projection` | `process_internal_name` | "Wmiprvse.exe" | `—` | confirmed；OCSF 字段名直接对应；05 已注册标准路径 |
| `roles.target.process.file.company_name` | `projection` | `process_company` | "Microsoft Corporation" | `—` | confirmed；05 已注册标准路径 |
| `roles.target.process.file.product.name` | `projection` | `process_product` | "Microsoft Windows Operating System" | `—` | confirmed；registry v17 已注册标准路径 |
| `roles.target.process.file.description` | `projection` | `process_description` | "WMI Provider Host" | `—` | confirmed；registry v17 已注册标准路径 |
| `roles.target.process.file.signatures[0].signer` | `projection` | `process_sign` | "Microsoft Windows Publisher" | `—` | confirmed；05 已注册标准路径 |
| `roles.target.process.file.version` | `projection` | `process_version` | "10.0.19041.3636" | `—` | confirmed；UDM/XDM 无文件版本字段；registry v17 已注册标准路径 |
| `roles.target.process.user.name` | `projection` | `process_user` | "NT AUTHORITY\\NETWORK SERVICE" | `—` | confirmed；当前进程的用户；角色由事件决定——process_event 落 target.process.user，ip_access/file_write 落 carriers[].process.user |
| `roles.target.process.created_time` | `projection` | `process_create_time` | 1734489700704 | `—` | confirmed；OCSF process.created_time 存在；SDM 05 文档暂未新增此路径（terminated_time 已新增） |
| `roles.target.process.working_directory` | `projection` | `process_current_directory` | "C:\\Windows\\System32\\" | `—` | confirmed；OCSF 字段名 working_directory 直接对应；05 已注册标准路径 |
| `roles.target.process.integrity` | `projection` | `process_integrity_level` | "System" | `—` | confirmed；三标准都有锚点；05 已注册标准路径 |
| `roles.source.process.name` | `projection` | `process_parent_name` | "svchost.exe" | `—` | confirmed；XDM 只有 parent_id 平铺 ID，无父进程对象；父进程位置由事件类型决定（process_event 落 source.process，ip_access/file_write 落 related[]） |
| `roles.source.process.uid` | `projection` | `process_parent_guid` | "d22b3fbcb9e77cb86834f6a18e2e0f68" | `—` | confirmed； |
| `roles.source.process.pid` | `projection` | `process_parent_id` | "844" | `—` | confirmed； |
| `roles.source.process.path` | `projection` | `process_parent_path` | "C:\\Windows\\System32\\svchost.exe" | `—` | confirmed； |
| `roles.source.process.cmdline` | `projection` | `process_parent_command_line` | "C:\\Windows\\system32\\svchost.exe -k DcomLaunch -p" | `—` | confirmed； |
| `roles.source.process.file.internal_name` | `projection` | `process_parent_internal_name` | "svchost.exe" | `—` | confirmed；父进程位置由事件类型决定（process_event 落 source.process，ip_access/file_write 落 related[]） |
| `roles.source.process.file.original_name` | `projection` | `process_parent_original_name` | "svchost.exe" | `—` | confirmed；同 process_original_name；父进程位置由事件类型决定 |
| `roles.source.process.file.signatures[0].signer` | `projection` | `process_parent_sign` | "Microsoft Windows Publisher" | `—` | confirmed；父进程位置由事件类型决定 |
| `roles.related[0].process.name` | `projection` | `process_pparent_name` | "services.exe" | `—` | confirmed；XDM 无祖父进程对象（parent_id 仅一层） |
| `roles.related[0].process.path` | `projection` | `process_pparent_path` | "C:\\WINDOWS\\system32\\services.exe" | `—` | confirmed； |
| `roles.related[0].process.path` | `projection` | `process_pparent_command_line` | "C:\\WINDOWS\\system32\\services.exe" | `—` | confirmed； |
| `roles.source.host.name` | `projection` | `computer_name` | "DESKTOP-NU779RJ" | `—` | confirmed；受管终端主机名，投影 source_host |
| `roles.source.host.ip` | `projection` | `ip` | "198.51.100.211" | `—` | confirmed；终端属性 IP，不自动投影 source_ip；OCSF device.ip 弃用转 network_interfaces |
| `roles.source.host.ip` | `projection` | `client_ip` | "198.51.100.211" | `—` | confirmed；与 ip/report_ip 冲突时按 doc14 优先级 client_ip>ip>report_ip |
| `roles.source.host.ip` | `projection` | `client_report_ip` | "198.51.100.211" | `—` | confirmed；上报出口 IP（terminate 样例与 client_ip 不同 203.0.113.45）；三标准无直接锚点，值不同时必须保留（unmapped 或私有） |
| `roles.source.host.ip` | `projection` | `report_ip` | "198.51.100.211" | `—` | confirmed；同 client_report_ip；与 client_ip 不同时禁止静默丢弃 |
| `roles.source.host.id` | `projection` | `asset_id` | "2868257359929541780" | `—` | confirmed；受管终端资产 ID，参与 host_ref_id |
| `extensions.profiles.endpoint_asset.agent.id` | `projection` | `client_id` | "0881058-dfb9a23257c64098060e699601b17217" | `—` | confirmed；天擎 Agent ID，不等于 asset_id；OCSF 以 device.uid 承载 agent 设备 |
| `extensions.profiles.endpoint_asset.agent.fingerprint_id` | `projection` | `mid` | "ec80b820d87d7cd7ac916240bcdff7215ae3118feaf070c13afbf06e69af4eb3" | `—` | confirmed；Agent/终端指纹，三标准无锚点 |
| `extensions.profiles.endpoint_asset.ownership.group.id` | `projection` | `gid` | "4f9c3833b800d1f7" | `—` | confirmed；资产分组 ID，三标准无锚点 |
| `extensions.profiles.endpoint_asset.ownership.group.name` | `projection` | `group_name` | "未分组终端" | `—` | confirmed；资产分组名，三标准无锚点 |
| `roles.target.process.user.id` | `projection` | `user_logon_id` | "S-1-5-20" | `—` | confirmed；SID（S-1-5-20）非用户名称；UDM windows_sid/XDM sid 已核实 |

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
