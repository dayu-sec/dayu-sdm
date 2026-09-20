# WPL → SDM Event 字段映射

> 样例：`file_write.expected-sdm-event.json`；WPL 字段 42 个，映射 31，不落库 11，排除 0；另有平台默认、派生及结构字段 0 项。
> SDM 落位为逻辑路径；expected 位置为该样例中的实际物理 JSON 路径。

## 一、映射字段

| WPL 字段 | WPL 值 | SDM 落位 | expected 位置 | expected 值 | 说明 |
|---|---|---|---|---|---|
| `asset_oid` | "2653788242175861718" | `extensions.profiles.endpoint_asset.ownership.organization.id` | `extensions_obj.profiles.endpoint_asset.ownership.organization.id` | "2653788242175861718" | 组织资产节点 ID，三标准无锚点（国产组织模型） |
| `event_date_creation` | 1734489580781 | `occur_time` | `occur_time` | 1734489580781 | 来源原始事件时间；OCSF metadata.original_time 语义完全对应；UDM event_timestamp 已核实；XDM 字段树无事件时间页 |
| `process_parent_command_line` | "C:\\WINDOWS\\system32\\services.exe" | `roles.related[0].process.cmdline` | `roles_obj.related[0].process.cmdline` | "C:\\WINDOWS\\system32\\services.exe" |  |
| `process_parent_internal_name` | "services.exe" | `roles.related[0].process.file.internal_name` | `roles_obj.related[0].process.file.internal_name` | "services.exe" | 父进程位置由事件类型决定（process_event 落 source.process，ip_access/file_write 落 related[]） |
| `process_parent_name` | "services.exe" | `roles.related[0].process.name` | `roles_obj.related[0].process.name` | "services.exe" | XDM 只有 parent_id 平铺 ID，无父进程对象；父进程位置由事件类型决定（process_event 落 source.process，ip_access/file_write 落 related[]） |
| `process_parent_original_name` | "services.exe" | `roles.related[0].process.file.original_name` | `roles_obj.related[0].process.file.original_name` | "services.exe" | 同 process_original_name；父进程位置由事件类型决定 |
| `process_parent_sign` | "Microsoft Windows Publisher" | `roles.related[0].process.file.signatures[0].signer` | `roles_obj.related[0].process.file.signatures[0].signer` | "Microsoft Windows Publisher" | 父进程位置由事件类型决定 |
| `process_sha1` | "e4e3f6bbad17b41a42687b3d75ade4a10b0870ec" | `roles.carriers[0].process.file.hashes.sha1` | `roles_obj.carriers[0].process.file.hashes.sha1` | "e4e3f6bbad17b41a42687b3d75ade4a10b0870ec" | XDM executable 无 sha1（只有 md5/sha256）；registry v17 已注册标准路径（target/source/carriers 进程 file 均可用） |
| `uuid` | "FF34104C-20B9-4C05-8B06-0647524D7083" | `source_original_event_id` | `source_original_event_id` | "FF34104C-20B9-4C05-8B06-0647524D7083" | 来源原始事件 ID，参与确定性 event_id；UDM product_log_id 定义为 vendor GUID 完全对应 |
| `computer_name` | "DESKTOP-NU779RJ" | `roles.source.host.name` | `roles_obj.source.host.name` | "DESKTOP-NU779RJ" | 受管终端主机名，投影 source_host |
| `gid` | "4f9c3833b800d1f7" | `extensions.profiles.endpoint_asset.ownership.group.id` | `extensions_obj.profiles.endpoint_asset.ownership.group.id` | "4f9c3833b800d1f7" | 资产分组 ID，三标准无锚点 |
| `process_command_line` | "C:\\WINDOWS\\system32\\svchost.exe -k netsvcs -p -s Schedule" | `roles.carriers[0].process.cmdline` | `roles_obj.carriers[0].process.cmdline` | "C:\\WINDOWS\\system32\\svchost.exe -k netsvcs -p -s Schedule" | OCSF 字段名是 cmd_line 非 command_line |
| `process_internal_name` | "svchost.exe" | `roles.target.process.file.internal_name` | `carrier_process_name` | "svchost.exe" | OCSF 字段名直接对应；05 已注册标准路径 |
| `process_original_name` | "svchost.exe" | `roles.target.process.file.original_name` | `carrier_process_name` | "svchost.exe" | PE OriginalFilename；OCSF 无专门字段（internal_name 语义不同）；registry v17 已注册标准路径 |
| `process_parent_path` | "C:\\Windows\\System32\\services.exe" | `roles.related[0].process.path` | `roles_obj.related[0].process.path` | "C:\\Windows\\System32\\services.exe" |  |
| `process_sign` | "Microsoft Windows Publisher" | `roles.carriers[0].process.file.signatures[0].signer` | `roles_obj.carriers[0].process.file.signatures[0].signer` | "Microsoft Windows Publisher" | 05 已注册标准路径 |
| `process_user` | "NT AUTHORITY\\SYSTEM" | `roles.carriers[0].process.user.name` | `roles_obj.carriers[0].process.user.name` | "NT AUTHORITY\\SYSTEM" | 当前进程的用户；角色由事件决定——process_event 落 target.process.user，ip_access/file_write 落 carriers[].process.user |
| `report_ip` | "198.51.100.211" | `roles.source.host.ip` | `roles_obj.source.host.ip` | "198.51.100.211" | 同 client_report_ip；与 client_ip 不同时禁止静默丢弃 |
| `asset_id` | "2868257359929541780" | `roles.source.host.id` | `roles_obj.source.host.id` | "2868257359929541780" | 受管终端资产 ID，参与 host_ref_id |
| `client_id` | "0881058-dfb9a23257c64098060e699601b17217" | `extensions.profiles.endpoint_asset.agent.id` | `extensions_obj.profiles.endpoint_asset.agent.id` | "0881058-dfb9a23257c64098060e699601b17217" | 天擎 Agent ID，不等于 asset_id；OCSF 以 device.uid 承载 agent 设备 |
| `ip` | "198.51.100.211" | `roles.source.host.ip` | `roles_obj.source.host.ip` | "198.51.100.211" | 终端属性 IP，不自动投影 source_ip；OCSF device.ip 弃用转 network_interfaces |
| `file_md5` | "5d9afa5a5c717fefd1da8b9b396ad27a" | `roles.target.file.hashes.md5` | `roles_obj.target.file.hashes.md5` | "5d9afa5a5c717fefd1da8b9b396ad27a" |  |
| `file_name` | "Scheduled Start" | `target_file_name` | `target_file_name` | "Scheduled Start" |  |
| `file_path` | "C:\\WINDOWS\\System32\\Tasks\\Microsoft\\Windows\\WindowsUpdate\\Scheduled Start" | `target_file_path` | `target_file_path` | "C:\\WINDOWS\\System32\\Tasks\\Microsoft\\Windows\\WindowsUpdate\\Scheduled Start" |  |
| `group_name` | "未分组终端" | `extensions.profiles.endpoint_asset.ownership.group.name` | `extensions_obj.profiles.endpoint_asset.ownership.group.name` | "未分组终端" | 资产分组名，三标准无锚点 |
| `mid` | "ec80b820d87d7cd7ac916240bcdff7215ae3118feaf070c13afbf06e69af4eb3" | `extensions.profiles.endpoint_asset.agent.fingerprint_id` | `extensions_obj.profiles.endpoint_asset.agent.fingerprint_id` | "ec80b820d87d7cd7ac916240bcdff7215ae3118feaf070c13afbf06e69af4eb3" | Agent/终端指纹，三标准无锚点 |
| `process_guid` | "ae64b7b3dd9458ca6bdc6fe97f7d6344" | `roles.target.process.uid` | `carrier_process_guid` | "ae64b7b3dd9458ca6bdc6fe97f7d6344" | 三标准均无 guid 字段名；32hex 可落 OCSF uid |
| `process_id` | "1680" | `roles.target.process.pid` | `carrier_process_pid` | "1680" | 与 pid 同值，取一即可 |
| `process_md5` | "7469cc568ad6821fd9d925542730a7d8" | `roles.carriers[0].process.file.hashes.md5` | `roles_obj.carriers[0].process.file.hashes.md5` | "7469cc568ad6821fd9d925542730a7d8" | 哈希统一小写 |
| `process_name` | "svchost.exe" | `roles.target.process.name` | `carrier_process_name` | "svchost.exe" | UDM 进程无 name，名称在 file 对象 |
| `process_path` | "C:\\Windows\\System32\\svchost.exe" | `roles.carriers[0].process.path` | `roles_obj.carriers[0].process.path` | "C:\\Windows\\System32\\svchost.exe" |  |

## 二、不落库字段

| WPL 字段 | WPL 值 | 原因 |
|---|---|---|
| `custom_group_paths` | "" | 组织分组路径原始串，三标准无锚点 |
| `file_name_renamed` | "" |  |
| `file_path_renamed` | "" |  |
| `file_previous_date_creation` | "0" |  |
| `removable_device` | "0" |  |
| `timestamp` | 1734489597000 | 条件回退字段：仅主事件时间缺失或无效时用于 occur_time；本样例未采用 |
| `type` | "file_operations" | WPL 规则类型 process_details，非标准字段；SDM 保留原值 |
| `file_date_creation` | "0" |  |
| `create_time` | 1734489625860243500 | 终端资产创建时间，非事件时间；OCSF device.first_seen 语义近似；禁止覆盖 occur_time |
| `event_type` | "file_write" | 天擎动作枚举，SDM 侧按转换表映射 process_launch/process_termination/process_uncategorized |
| `mac` | "00-00-5E-00-53-79" | SDM host 对象无 mac 路径（05 文档），暂落私有；OCSF/XDM 主机 mac 锚点已核实 |

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
| `mapping_id` | `constant` | `constant.mapping_id` | "qax.tianqing.edr_file_op" | `—` | confirmed；expected 事件确认的日志类型级常量 |
| `event_domain` | `constant` | `constant.event_domain` | "endpoint" | `—` | confirmed；expected 事件确认的日志类型级常量 |
| `data_src_product` | `constant` | `constant.data_src_product` | "tianqing" | `—` | confirmed；expected 事件确认的日志类型级常量 |
| `log_type` | `constant` | `constant.log_type` | "edr_file_op" | `—` | confirmed；expected 事件确认的日志类型级常量 |
| `data_src_category` | `constant` | `constant.data_src_category` | "endpoint_security" | `—` | confirmed；expected 事件确认的日志类型级常量 |
| `log_name` | `constant` | `constant.log_name` | "天擎 EDR 文件操作" | `—` | confirmed；expected 事件确认的日志类型级常量 |
| `record_kind` | `constant` | `constant.record_kind` | "activity" | `—` | confirmed；expected 事件确认的日志类型级常量 |
| `event_type` | `constant` | `constant.log_semantics` | "file_modification" | `—` | confirmed；当前日志类型的 expected 事件语义 |
| `event_category` | `constant` | `constant.event_category` | "audit" | `—` | confirmed；EDR 行为监控文件操作，PDF §3.9.5 |
| `operation` | `constant` | `constant.log_semantics` | "write" | `—` | confirmed；当前日志类型的 expected 事件语义 |
| `outcome` | `constant` | `constant.log_semantics` | "observed" | `—` | confirmed；当前日志类型的 expected 事件语义 |
| `severity` | `constant` | `constant.log_semantics` | "info" | `—` | confirmed；当前日志类型的 expected 事件语义 |

### 5.2 Content 区

| SDM 字段 | 规则类型 | WPL 字段 | 映射/赋值 | 未命中 | 状态与证据 |
|---|---|---|---|---|---|
| `extensions.profiles.endpoint_asset.ownership.organization.id` | `projection` | `asset_oid` | "2653788242175861718" | `—` | confirmed；组织资产节点 ID，三标准无锚点（国产组织模型） |
| `occur_time` | `projection` | `event_date_creation` | 1734489580781 | `—` | confirmed；来源原始事件时间；OCSF metadata.original_time 语义完全对应；UDM event_timestamp 已核实；XDM 字段树无事件时间页 |
| `roles.related[0].process.cmdline` | `projection` | `process_parent_command_line` | "C:\\WINDOWS\\system32\\services.exe" | `—` | confirmed； |
| `roles.related[0].process.file.internal_name` | `projection` | `process_parent_internal_name` | "services.exe" | `—` | confirmed；父进程位置由事件类型决定（process_event 落 source.process，ip_access/file_write 落 related[]） |
| `roles.related[0].process.name` | `projection` | `process_parent_name` | "services.exe" | `—` | confirmed；XDM 只有 parent_id 平铺 ID，无父进程对象；父进程位置由事件类型决定（process_event 落 source.process，ip_access/file_write 落 related[]） |
| `roles.related[0].process.file.original_name` | `projection` | `process_parent_original_name` | "services.exe" | `—` | confirmed；同 process_original_name；父进程位置由事件类型决定 |
| `roles.related[0].process.file.signatures[0].signer` | `projection` | `process_parent_sign` | "Microsoft Windows Publisher" | `—` | confirmed；父进程位置由事件类型决定 |
| `roles.carriers[0].process.file.hashes.sha1` | `projection` | `process_sha1` | "e4e3f6bbad17b41a42687b3d75ade4a10b0870ec" | `—` | confirmed；XDM executable 无 sha1（只有 md5/sha256）；registry v17 已注册标准路径（target/source/carriers 进程 file 均可用） |
| `source_original_event_id` | `projection` | `uuid` | "FF34104C-20B9-4C05-8B06-0647524D7083" | `—` | confirmed；来源原始事件 ID，参与确定性 event_id；UDM product_log_id 定义为 vendor GUID 完全对应 |
| `roles.source.host.name` | `projection` | `computer_name` | "DESKTOP-NU779RJ" | `—` | confirmed；受管终端主机名，投影 source_host |
| `extensions.profiles.endpoint_asset.ownership.group.id` | `projection` | `gid` | "4f9c3833b800d1f7" | `—` | confirmed；资产分组 ID，三标准无锚点 |
| `roles.carriers[0].process.cmdline` | `projection` | `process_command_line` | "C:\\WINDOWS\\system32\\svchost.exe -k netsvcs -p -s Schedule" | `—` | confirmed；OCSF 字段名是 cmd_line 非 command_line |
| `roles.target.process.file.internal_name` | `projection` | `process_internal_name` | "svchost.exe" | `—` | confirmed；OCSF 字段名直接对应；05 已注册标准路径 |
| `roles.target.process.file.original_name` | `projection` | `process_original_name` | "svchost.exe" | `—` | confirmed；PE OriginalFilename；OCSF 无专门字段（internal_name 语义不同）；registry v17 已注册标准路径 |
| `roles.related[0].process.path` | `projection` | `process_parent_path` | "C:\\Windows\\System32\\services.exe" | `—` | confirmed； |
| `roles.carriers[0].process.file.signatures[0].signer` | `projection` | `process_sign` | "Microsoft Windows Publisher" | `—` | confirmed；05 已注册标准路径 |
| `roles.carriers[0].process.user.name` | `projection` | `process_user` | "NT AUTHORITY\\SYSTEM" | `—` | confirmed；当前进程的用户；角色由事件决定——process_event 落 target.process.user，ip_access/file_write 落 carriers[].process.user |
| `roles.source.host.ip` | `projection` | `report_ip` | "198.51.100.211" | `—` | confirmed；同 client_report_ip；与 client_ip 不同时禁止静默丢弃 |
| `roles.source.host.id` | `projection` | `asset_id` | "2868257359929541780" | `—` | confirmed；受管终端资产 ID，参与 host_ref_id |
| `extensions.profiles.endpoint_asset.agent.id` | `projection` | `client_id` | "0881058-dfb9a23257c64098060e699601b17217" | `—` | confirmed；天擎 Agent ID，不等于 asset_id；OCSF 以 device.uid 承载 agent 设备 |
| `roles.source.host.ip` | `projection` | `ip` | "198.51.100.211" | `—` | confirmed；终端属性 IP，不自动投影 source_ip；OCSF device.ip 弃用转 network_interfaces |
| `roles.target.file.hashes.md5` | `projection` | `file_md5` | "5d9afa5a5c717fefd1da8b9b396ad27a" | `—` | confirmed； |
| `target_file_name` | `projection` | `file_name` | "Scheduled Start" | `—` | confirmed； |
| `target_file_path` | `projection` | `file_path` | "C:\\WINDOWS\\System32\\Tasks\\Microsoft\\Windows\\WindowsUpdate\\Scheduled Start" | `—` | confirmed； |
| `extensions.profiles.endpoint_asset.ownership.group.name` | `projection` | `group_name` | "未分组终端" | `—` | confirmed；资产分组名，三标准无锚点 |
| `extensions.profiles.endpoint_asset.agent.fingerprint_id` | `projection` | `mid` | "ec80b820d87d7cd7ac916240bcdff7215ae3118feaf070c13afbf06e69af4eb3" | `—` | confirmed；Agent/终端指纹，三标准无锚点 |
| `roles.target.process.uid` | `projection` | `process_guid` | "ae64b7b3dd9458ca6bdc6fe97f7d6344" | `—` | confirmed；三标准均无 guid 字段名；32hex 可落 OCSF uid |
| `roles.target.process.pid` | `projection` | `process_id` | "1680" | `—` | confirmed；与 pid 同值，取一即可 |
| `roles.carriers[0].process.file.hashes.md5` | `projection` | `process_md5` | "7469cc568ad6821fd9d925542730a7d8" | `—` | confirmed；哈希统一小写 |
| `roles.target.process.name` | `projection` | `process_name` | "svchost.exe" | `—` | confirmed；UDM 进程无 name，名称在 file 对象 |
| `roles.carriers[0].process.path` | `projection` | `process_path` | "C:\\Windows\\System32\\svchost.exe" | `—` | confirmed； |

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
