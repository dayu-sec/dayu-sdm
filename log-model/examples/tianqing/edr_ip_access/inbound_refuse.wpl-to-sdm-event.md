# WPL → SDM Event 字段映射

> 样例：`inbound_refuse.expected-sdm-event.json`；WPL 字段 45 个，映射 36，不落库 9，排除 0；另有平台默认、派生及结构字段 0 项。
> SDM 落位为逻辑路径；expected 位置为该样例中的实际物理 JSON 路径。

## 一、映射字段

| WPL 字段 | WPL 值 | SDM 落位 | expected 位置 | expected 值 | 说明 |
|---|---|---|---|---|---|
| `asset_oid` | "org-2653788242175861718" | `extensions.profiles.endpoint_asset.ownership.organization.id` | `extensions_obj.profiles.endpoint_asset.ownership.organization.id` | "org-2653788242175861718" | 组织资产节点 ID，三标准无锚点（国产组织模型） |
| `dst_host_name` | "SERVER-APP01" | `roles.target.host.name` | `roles_obj.target.host.name` | "SERVER-APP01" |  |
| `event_date_creation` | 1734490098000 | `occur_time` | `occur_time` | 1734490098000 | 来源原始事件时间；OCSF metadata.original_time 语义完全对应；UDM event_timestamp 已核实；XDM 字段树无事件时间页 |
| `process_parent_command_line` | "C:\\Windows\\System32\\services.exe" | `roles.related[0].process.cmdline` | `roles_obj.related[0].process.cmdline` | "C:\\Windows\\System32\\services.exe" |  |
| `process_parent_internal_name` | "services.exe" | `roles.related[0].process.file.internal_name` | `roles_obj.related[0].process.file.internal_name` | "services.exe" | 父进程位置由事件类型决定（process_event 落 source.process，ip_access/file_write 落 related[]） |
| `process_parent_name` | "services.exe" | `roles.related[0].process.name` | `roles_obj.related[0].process.name` | "services.exe" | XDM 只有 parent_id 平铺 ID，无父进程对象；父进程位置由事件类型决定（process_event 落 source.process，ip_access/file_write 落 related[]） |
| `process_parent_original_name` | "services.exe" | `roles.related[0].process.file.original_name` | `roles_obj.related[0].process.file.original_name` | "services.exe" | 同 process_original_name；父进程位置由事件类型决定 |
| `process_parent_sign` | "Microsoft Windows Publisher" | `roles.related[0].process.file.signatures[0].signer` | `roles_obj.related[0].process.file.signatures[0].signer` | "Microsoft Windows Publisher" | 父进程位置由事件类型决定 |
| `process_sha1` | "7f530281c5ba86b81ae4230dab1617cb55260d9e" | `roles.carriers[0].process.file.hashes.sha1` | `roles_obj.carriers[0].process.file.hashes.sha1` | "7f530281c5ba86b81ae4230dab1617cb55260d9e" | XDM executable 无 sha1（只有 md5/sha256）；registry v17 已注册标准路径（target/source/carriers 进程 file 均可用） |
| `uuid` | "61794FDE-6769-464E-B071-6CE07B01FEE5" | `source_original_event_id` | `source_original_event_id` | "61794FDE-6769-464E-B071-6CE07B01FEE5" | 来源原始事件 ID，参与确定性 event_id；UDM product_log_id 定义为 vendor GUID 完全对应 |
| `computer_name` | "SERVER-APP01" | `roles.source.host.name` | `target_host` | "SERVER-APP01" | 受管终端主机名，投影 source_host |
| `dst_ip_addr` | "198.51.100.118" | `roles.target.endpoint.ip` | `roles_obj.target.endpoint.ip` | "198.51.100.118" | 网络目标方端点 IP，投影 target_ip |
| `dst_port` | "3389" | `roles.target.endpoint.port` | `roles_obj.target.endpoint.port` | 3389 | WPL 为字符串，写前转 0-65535 整数 |
| `gid` | "servers-01" | `extensions.profiles.endpoint_asset.ownership.group.id` | `extensions_obj.profiles.endpoint_asset.ownership.group.id` | "servers-01" | 资产分组 ID，三标准无锚点 |
| `network_protocol` | "TCP" | `facets.network.protocol` | `network_protocol` | "tcp" | 统一为小写标准值（tcp/udp）；OCSF 在 connection_info、UDM/XDM 在 ip_protocol |
| `process_command_line` | "C:\\Windows\\System32\\svchost.exe -k TermService" | `roles.carriers[0].process.cmdline` | `roles_obj.carriers[0].process.cmdline` | "C:\\Windows\\System32\\svchost.exe -k TermService" | OCSF 字段名是 cmd_line 非 command_line |
| `process_internal_name` | "svchost.exe" | `roles.target.process.file.internal_name` | `carrier_process_name` | "svchost.exe" | OCSF 字段名直接对应；05 已注册标准路径 |
| `process_original_name` | "svchost.exe" | `roles.target.process.file.original_name` | `carrier_process_name` | "svchost.exe" | PE OriginalFilename；OCSF 无专门字段（internal_name 语义不同）；registry v17 已注册标准路径 |
| `process_parent_path` | "C:\\Windows\\System32\\services.exe" | `roles.related[0].process.path` | `roles_obj.related[0].process.path` | "C:\\Windows\\System32\\services.exe" |  |
| `process_sign` | "Microsoft Windows Publisher" | `roles.carriers[0].process.file.signatures[0].signer` | `roles_obj.carriers[0].process.file.signatures[0].signer` | "Microsoft Windows Publisher" | 05 已注册标准路径 |
| `process_user` | "NT AUTHORITY\\NETWORK SERVICE" | `roles.carriers[0].process.user.name` | `roles_obj.carriers[0].process.user.name` | "NT AUTHORITY\\NETWORK SERVICE" | 当前进程的用户；角色由事件决定——process_event 落 target.process.user，ip_access/file_write 落 carriers[].process.user |
| `process_version` | "10.0.19041.3636" | `roles.carriers[0].process.file.version` | `roles_obj.carriers[0].process.file.version` | "10.0.19041.3636" | UDM/XDM 无文件版本字段；registry v17 已注册标准路径 |
| `report_ip` | "198.51.100.118" | `target_ip` | `target_ip` | "198.51.100.118" | 同 client_report_ip；与 client_ip 不同时禁止静默丢弃 |
| `src_ip_addr` | "198.51.100.114" | `roles.source.endpoint.ip` | `roles_obj.source.endpoint.ip` | "198.51.100.114" | 网络主动方端点 IP，投影 source_ip（与终端属性 host.ip 区分） |
| `src_port` | 55321 | `roles.source.endpoint.port` | `roles_obj.source.endpoint.port` | 55321 | 转 0-65535 整数 |
| `asset_id` | "server-198.51.100.118" | `roles.target.host.id` | `roles_obj.target.host.id` | "server-198.51.100.118" | 受管终端资产 ID，参与 host_ref_id |
| `client_id` | "agent-server-01" | `extensions.profiles.endpoint_asset.agent.id` | `extensions_obj.profiles.endpoint_asset.agent.id` | "agent-server-01" | 天擎 Agent ID，不等于 asset_id；OCSF 以 device.uid 承载 agent 设备 |
| `ip` | "198.51.100.118" | `roles.source.host.ip` | `target_ip` | "198.51.100.118" | 终端属性 IP，不自动投影 source_ip；OCSF device.ip 弃用转 network_interfaces |
| `group_name` | "服务器" | `extensions.profiles.endpoint_asset.ownership.group.name` | `extensions_obj.profiles.endpoint_asset.ownership.group.name` | "服务器" | 资产分组名，三标准无锚点 |
| `mac` | "00:50:56:81:e8:20" | `roles.target.host.mac` | `roles_obj.target.host.mac` | "00:50:56:81:e8:20" | 受管终端主机 MAC，规范化为冒号分隔小写格式 |
| `mid` | "mid-server-01" | `extensions.profiles.endpoint_asset.agent.fingerprint_id` | `extensions_obj.profiles.endpoint_asset.agent.fingerprint_id` | "mid-server-01" | Agent/终端指纹，三标准无锚点 |
| `process_guid` | "f9e0f1be8d7c4e45b9d2a1c0f5e6d789" | `roles.target.process.uid` | `carrier_process_guid` | "f9e0f1be8d7c4e45b9d2a1c0f5e6d789" | 三标准均无 guid 字段名；32hex 可落 OCSF uid |
| `process_id` | "912" | `roles.target.process.pid` | `carrier_process_pid` | "912" | 与 pid 同值，取一即可 |
| `process_md5` | "8bb61c2b1e34ff3c778cf150bdf08238" | `roles.carriers[0].process.file.hashes.md5` | `roles_obj.carriers[0].process.file.hashes.md5` | "8bb61c2b1e34ff3c778cf150bdf08238" | 哈希统一小写 |
| `process_name` | "svchost.exe" | `roles.target.process.name` | `carrier_process_name` | "svchost.exe" | UDM 进程无 name，名称在 file 对象 |
| `process_path` | "C:\\Windows\\System32\\svchost.exe" | `roles.carriers[0].process.path` | `roles_obj.carriers[0].process.path` | "C:\\Windows\\System32\\svchost.exe" |  |

## 二、不落库字段

| WPL 字段 | WPL 值 | 原因 |
|---|---|---|
| `custom_group_paths` | "总部/服务器区" | 组织分组路径原始串，三标准无锚点 |
| `dst_is_ipv6` | "false" | 候选删除：IP 值本身决定地址族，仅质量校验 |
| `inout` | "in" | 归一为 inbound/outbound 开放值；XDM 无 direction（经 source/target 表达）；只作方向事实不改变两端角色 |
| `network_connection_initiated` | "false" | 方向校验事实，仅用于校验 source/target 角色，不落标准路径 |
| `src_host_name` | "unknown" | unknown 等缺失占位值不写入 |
| `src_is_ipv6` | "false" | 候选删除：IP 值本身决定地址族，仅质量校验 |
| `timestamp` | 1734490098500 | 条件回退字段：仅主事件时间缺失或无效时用于 occur_time；本样例未采用 |
| `type` | "ip_access" | WPL 规则类型 process_details，非标准字段；SDM 保留原值 |
| `event_type` | "connection_refused" | 天擎动作枚举，SDM 侧按转换表映射 process_launch/process_termination/process_uncategorized |

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
| `mapping_id` | `constant` | `constant.mapping_id` | "qax.tianqing.edr_ip_access" | `—` | confirmed；expected 事件确认的日志类型级常量 |
| `event_domain` | `constant` | `constant.event_domain` | "network" | `—` | confirmed；expected 事件确认的日志类型级常量 |
| `data_src_product` | `constant` | `constant.data_src_product` | "tianqing" | `—` | confirmed；expected 事件确认的日志类型级常量 |
| `log_type` | `constant` | `constant.log_type` | "edr_ip_access" | `—` | confirmed；expected 事件确认的日志类型级常量 |
| `data_src_category` | `constant` | `constant.data_src_category` | "endpoint_security" | `—` | confirmed；expected 事件确认的日志类型级常量 |
| `log_name` | `constant` | `constant.log_name` | "天擎 EDR IP访问" | `—` | confirmed；expected 事件确认的日志类型级常量 |
| `record_kind` | `constant` | `constant.record_kind` | "activity" | `—` | confirmed；expected 事件确认的日志类型级常量 |
| `event_type` | `constant` | `constant.log_semantics` | "network_connection" | `—` | confirmed；当前日志类型的 expected 事件语义 |
| `operation` | `constant` | `constant.log_semantics` | "refuse" | `—` | confirmed；当前日志类型的 expected 事件语义 |
| `outcome` | `constant` | `constant.log_semantics` | "failed" | `—` | confirmed；当前日志类型的 expected 事件语义 |
| `severity` | `constant` | `constant.log_semantics` | "info" | `—` | confirmed；当前日志类型的 expected 事件语义 |

### 5.2 Content 区

| SDM 字段 | 规则类型 | WPL 字段 | 映射/赋值 | 未命中 | 状态与证据 |
|---|---|---|---|---|---|
| `extensions.profiles.endpoint_asset.ownership.organization.id` | `projection` | `asset_oid` | "org-2653788242175861718" | `—` | confirmed；组织资产节点 ID，三标准无锚点（国产组织模型） |
| `roles.target.host.name` | `projection` | `dst_host_name` | "SERVER-APP01" | `—` | confirmed； |
| `occur_time` | `projection` | `event_date_creation` | 1734490098000 | `—` | confirmed；来源原始事件时间；OCSF metadata.original_time 语义完全对应；UDM event_timestamp 已核实；XDM 字段树无事件时间页 |
| `roles.related[0].process.cmdline` | `projection` | `process_parent_command_line` | "C:\\Windows\\System32\\services.exe" | `—` | confirmed； |
| `roles.related[0].process.file.internal_name` | `projection` | `process_parent_internal_name` | "services.exe" | `—` | confirmed；父进程位置由事件类型决定（process_event 落 source.process，ip_access/file_write 落 related[]） |
| `roles.related[0].process.name` | `projection` | `process_parent_name` | "services.exe" | `—` | confirmed；XDM 只有 parent_id 平铺 ID，无父进程对象；父进程位置由事件类型决定（process_event 落 source.process，ip_access/file_write 落 related[]） |
| `roles.related[0].process.file.original_name` | `projection` | `process_parent_original_name` | "services.exe" | `—` | confirmed；同 process_original_name；父进程位置由事件类型决定 |
| `roles.related[0].process.file.signatures[0].signer` | `projection` | `process_parent_sign` | "Microsoft Windows Publisher" | `—` | confirmed；父进程位置由事件类型决定 |
| `roles.carriers[0].process.file.hashes.sha1` | `projection` | `process_sha1` | "7f530281c5ba86b81ae4230dab1617cb55260d9e" | `—` | confirmed；XDM executable 无 sha1（只有 md5/sha256）；registry v17 已注册标准路径（target/source/carriers 进程 file 均可用） |
| `source_original_event_id` | `projection` | `uuid` | "61794FDE-6769-464E-B071-6CE07B01FEE5" | `—` | confirmed；来源原始事件 ID，参与确定性 event_id；UDM product_log_id 定义为 vendor GUID 完全对应 |
| `roles.source.host.name` | `projection` | `computer_name` | "SERVER-APP01" | `—` | confirmed；受管终端主机名，投影 source_host |
| `roles.target.endpoint.ip` | `projection` | `dst_ip_addr` | "198.51.100.118" | `—` | confirmed；网络目标方端点 IP，投影 target_ip |
| `roles.target.endpoint.port` | `projection` | `dst_port` | 3389 | `—` | confirmed；WPL 为字符串，写前转 0-65535 整数 |
| `extensions.profiles.endpoint_asset.ownership.group.id` | `projection` | `gid` | "servers-01" | `—` | confirmed；资产分组 ID，三标准无锚点 |
| `facets.network.protocol` | `projection` | `network_protocol` | "tcp" | `—` | confirmed；统一为小写标准值（tcp/udp）；OCSF 在 connection_info、UDM/XDM 在 ip_protocol |
| `roles.carriers[0].process.cmdline` | `projection` | `process_command_line` | "C:\\Windows\\System32\\svchost.exe -k TermService" | `—` | confirmed；OCSF 字段名是 cmd_line 非 command_line |
| `roles.target.process.file.internal_name` | `projection` | `process_internal_name` | "svchost.exe" | `—` | confirmed；OCSF 字段名直接对应；05 已注册标准路径 |
| `roles.target.process.file.original_name` | `projection` | `process_original_name` | "svchost.exe" | `—` | confirmed；PE OriginalFilename；OCSF 无专门字段（internal_name 语义不同）；registry v17 已注册标准路径 |
| `roles.related[0].process.path` | `projection` | `process_parent_path` | "C:\\Windows\\System32\\services.exe" | `—` | confirmed； |
| `roles.carriers[0].process.file.signatures[0].signer` | `projection` | `process_sign` | "Microsoft Windows Publisher" | `—` | confirmed；05 已注册标准路径 |
| `roles.carriers[0].process.user.name` | `projection` | `process_user` | "NT AUTHORITY\\NETWORK SERVICE" | `—` | confirmed；当前进程的用户；角色由事件决定——process_event 落 target.process.user，ip_access/file_write 落 carriers[].process.user |
| `roles.carriers[0].process.file.version` | `projection` | `process_version` | "10.0.19041.3636" | `—` | confirmed；UDM/XDM 无文件版本字段；registry v17 已注册标准路径 |
| `target_ip` | `projection` | `report_ip` | "198.51.100.118" | `—` | confirmed；同 client_report_ip；与 client_ip 不同时禁止静默丢弃 |
| `roles.source.endpoint.ip` | `projection` | `src_ip_addr` | "198.51.100.114" | `—` | confirmed；网络主动方端点 IP，投影 source_ip（与终端属性 host.ip 区分） |
| `roles.source.endpoint.port` | `projection` | `src_port` | 55321 | `—` | confirmed；转 0-65535 整数 |
| `roles.target.host.id` | `projection` | `asset_id` | "server-198.51.100.118" | `—` | confirmed；受管终端资产 ID，参与 host_ref_id |
| `extensions.profiles.endpoint_asset.agent.id` | `projection` | `client_id` | "agent-server-01" | `—` | confirmed；天擎 Agent ID，不等于 asset_id；OCSF 以 device.uid 承载 agent 设备 |
| `roles.source.host.ip` | `projection` | `ip` | "198.51.100.118" | `—` | confirmed；终端属性 IP，不自动投影 source_ip；OCSF device.ip 弃用转 network_interfaces |
| `extensions.profiles.endpoint_asset.ownership.group.name` | `projection` | `group_name` | "服务器" | `—` | confirmed；资产分组名，三标准无锚点 |
| `roles.target.host.mac` | `projection` | `mac` | "00:50:56:81:e8:20" | `—` | confirmed；受管终端主机 MAC，规范化为冒号分隔小写格式 |
| `extensions.profiles.endpoint_asset.agent.fingerprint_id` | `projection` | `mid` | "mid-server-01" | `—` | confirmed；Agent/终端指纹，三标准无锚点 |
| `roles.target.process.uid` | `projection` | `process_guid` | "f9e0f1be8d7c4e45b9d2a1c0f5e6d789" | `—` | confirmed；三标准均无 guid 字段名；32hex 可落 OCSF uid |
| `roles.target.process.pid` | `projection` | `process_id` | "912" | `—` | confirmed；与 pid 同值，取一即可 |
| `roles.carriers[0].process.file.hashes.md5` | `projection` | `process_md5` | "8bb61c2b1e34ff3c778cf150bdf08238" | `—` | confirmed；哈希统一小写 |
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
