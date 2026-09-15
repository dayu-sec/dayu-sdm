# WPL → SDM Event 字段映射

> 样例：`outbound_open.expected-sdm-event.json`；WPL 字段 45 个，映射 37，不落库 8，排除 0；另有平台默认、派生及结构字段 0 项。
> SDM 落位为逻辑路径；expected 位置为该样例中的实际物理 JSON 路径。

## 一、映射字段

| WPL 字段 | WPL 值 | SDM 落位 | expected 位置 | expected 值 | 说明 |
|---|---|---|---|---|---|
| `asset_oid` | "org-2653788242175861718" | `extensions.profiles.endpoint_asset.ownership.organization.id` | `extensions_obj.profiles.endpoint_asset.ownership.organization.id` | "org-2653788242175861718" | 组织资产节点 ID，三标准无锚点（国产组织模型） |
| `dst_host_name` | "api.example.net" | `roles.target.host.name` | `roles_obj.target.host.name` | "api.example.net" |  |
| `event_date_creation` | 1734490012000 | `occur_time` | `occur_time` | 1734490012000 | 来源原始事件时间；OCSF metadata.original_time 语义完全对应；UDM event_timestamp 已核实；XDM 字段树无事件时间页 |
| `process_parent_command_line` | "C:\\Windows\\System32\\services.exe" | `roles.related[0].process.cmdline` | `roles_obj.related[0].process.cmdline` | "C:\\Windows\\System32\\services.exe" |  |
| `process_parent_internal_name` | "services.exe" | `roles.related[0].process.file.internal_name` | `roles_obj.related[0].process.file.internal_name` | "services.exe" | 父进程位置由事件类型决定（process_event 落 source.process，ip_access/file_write 落 related[]） |
| `process_parent_name` | "services.exe" | `roles.related[0].process.name` | `roles_obj.related[0].process.name` | "services.exe" | XDM 只有 parent_id 平铺 ID，无父进程对象；父进程位置由事件类型决定（process_event 落 source.process，ip_access/file_write 落 related[]） |
| `process_parent_original_name` | "services.exe" | `roles.related[0].process.file.original_name` | `roles_obj.related[0].process.file.original_name` | "services.exe" | 同 process_original_name；父进程位置由事件类型决定 |
| `process_parent_sign` | "Microsoft Windows Publisher" | `roles.related[0].process.file.signatures[0].signer` | `roles_obj.related[0].process.file.signatures[0].signer` | "Microsoft Windows Publisher" | 父进程位置由事件类型决定 |
| `process_sha1` | "6b2f9d1f50d57c6c30c2f6f1e34c5f3a7f7d4c2e" | `roles.carriers[0].process.file.hashes.sha1` | `roles_obj.carriers[0].process.file.hashes.sha1` | "6b2f9d1f50d57c6c30c2f6f1e34c5f3a7f7d4c2e" | XDM executable 无 sha1（只有 md5/sha256）；registry v17 已注册标准路径（target/source/carriers 进程 file 均可用） |
| `src_host_name` | "DESKTOP-EX01" | `roles.source.host.name` | `roles_obj.source.host.name` | "DESKTOP-EX01" | unknown 等缺失占位值不写入 |
| `uuid` | "61794FDE-6769-464E-B071-6CE07B01FEE4" | `source_original_event_id` | `source_original_event_id` | "61794FDE-6769-464E-B071-6CE07B01FEE4" | 来源原始事件 ID，参与确定性 event_id；UDM product_log_id 定义为 vendor GUID 完全对应 |
| `computer_name` | "DESKTOP-EX01" | `roles.source.host.name` | `roles_obj.source.host.name` | "DESKTOP-EX01" | 受管终端主机名，投影 source_host |
| `dst_ip_addr` | "203.0.113.25" | `roles.target.endpoint.ip` | `roles_obj.target.endpoint.ip` | "203.0.113.25" | 网络目标方端点 IP，投影 target_ip |
| `dst_port` | "443" | `roles.target.endpoint.port` | `roles_obj.target.endpoint.port` | 443 | WPL 为字符串，写前转 0-65535 整数 |
| `gid` | "4f9c3833b800d1f7" | `extensions.profiles.endpoint_asset.ownership.group.id` | `extensions_obj.profiles.endpoint_asset.ownership.group.id` | "4f9c3833b800d1f7" | 资产分组 ID，三标准无锚点 |
| `network_protocol` | "TCP" | `facets.network.protocol` | `network_protocol` | "tcp" | 统一为小写标准值（tcp/udp）；OCSF 在 connection_info、UDM/XDM 在 ip_protocol |
| `process_command_line` | "C:\\Program Files\\Acme\\agent.exe --sync" | `roles.carriers[0].process.cmdline` | `roles_obj.carriers[0].process.cmdline` | "C:\\Program Files\\Acme\\agent.exe --sync" | OCSF 字段名是 cmd_line 非 command_line |
| `process_internal_name` | "agent.exe" | `roles.target.process.file.internal_name` | `carrier_process_name` | "agent.exe" | OCSF 字段名直接对应；05 已注册标准路径 |
| `process_original_name` | "AcmeAgent.exe" | `roles.carriers[0].process.file.original_name` | `roles_obj.carriers[0].process.file.original_name` | "AcmeAgent.exe" | PE OriginalFilename；OCSF 无专门字段（internal_name 语义不同）；registry v17 已注册标准路径 |
| `process_parent_path` | "C:\\Windows\\System32\\services.exe" | `roles.related[0].process.path` | `roles_obj.related[0].process.path` | "C:\\Windows\\System32\\services.exe" |  |
| `process_sign` | "Acme Security Ltd." | `roles.carriers[0].process.file.signatures[0].signer` | `roles_obj.carriers[0].process.file.signatures[0].signer` | "Acme Security Ltd." | 05 已注册标准路径 |
| `process_user` | "NT AUTHORITY\\SYSTEM" | `roles.carriers[0].process.user.name` | `roles_obj.carriers[0].process.user.name` | "NT AUTHORITY\\SYSTEM" | 当前进程的用户；角色由事件决定——process_event 落 target.process.user，ip_access/file_write 落 carriers[].process.user |
| `process_version` | "203.0.113.252" | `roles.carriers[0].process.file.version` | `roles_obj.carriers[0].process.file.version` | "203.0.113.252" | UDM/XDM 无文件版本字段；registry v17 已注册标准路径 |
| `report_ip` | "198.51.100.211" | `source_ip` | `source_ip` | "198.51.100.211" | 同 client_report_ip；与 client_ip 不同时禁止静默丢弃 |
| `src_ip_addr` | "198.51.100.211" | `roles.source.endpoint.ip` | `roles_obj.source.endpoint.ip` | "198.51.100.211" | 网络主动方端点 IP，投影 source_ip（与终端属性 host.ip 区分） |
| `src_port` | 51532 | `roles.source.endpoint.port` | `roles_obj.source.endpoint.port` | 51532 | 转 0-65535 整数 |
| `asset_id` | "2868257359929541780" | `roles.source.host.id` | `roles_obj.source.host.id` | "2868257359929541780" | 受管终端资产 ID，参与 host_ref_id |
| `client_id` | "0881058-dfb9a23257c64098060e699601b17217" | `extensions.profiles.endpoint_asset.agent.id` | `extensions_obj.profiles.endpoint_asset.agent.id` | "0881058-dfb9a23257c64098060e699601b17217" | 天擎 Agent ID，不等于 asset_id；OCSF 以 device.uid 承载 agent 设备 |
| `ip` | "198.51.100.211" | `roles.source.host.ip` | `roles_obj.source.host.ip` | "198.51.100.211" | 终端属性 IP，不自动投影 source_ip；OCSF device.ip 弃用转 network_interfaces |
| `group_name` | "研发终端" | `extensions.profiles.endpoint_asset.ownership.group.name` | `extensions_obj.profiles.endpoint_asset.ownership.group.name` | "研发终端" | 资产分组名，三标准无锚点 |
| `mac` | "00:00:5E:00:53:23" | `roles.source.host.mac` | `roles_obj.source.host.mac` | "00:00:5E:00:53:23" | 受管终端主机 MAC，规范化为冒号分隔小写格式 |
| `mid` | "ec80b820d87d7cd7ac916240bcdff7215ae3118feaf070c13afbf06e69af4eb3" | `extensions.profiles.endpoint_asset.agent.fingerprint_id` | `extensions_obj.profiles.endpoint_asset.agent.fingerprint_id` | "ec80b820d87d7cd7ac916240bcdff7215ae3118feaf070c13afbf06e69af4eb3" | Agent/终端指纹，三标准无锚点 |
| `process_guid` | "4eacb509de8348659c847be955b6e1f1" | `roles.target.process.uid` | `carrier_process_guid` | "4eacb509de8348659c847be955b6e1f1" | 三标准均无 guid 字段名；32hex 可落 OCSF uid |
| `process_id` | "2716" | `roles.target.process.pid` | `carrier_process_pid` | "2716" | 与 pid 同值，取一即可 |
| `process_md5` | "a7a77e44a5d80b2191a47f2ee2a30a10" | `roles.carriers[0].process.file.hashes.md5` | `roles_obj.carriers[0].process.file.hashes.md5` | "a7a77e44a5d80b2191a47f2ee2a30a10" | 哈希统一小写 |
| `process_name` | "agent.exe" | `roles.target.process.name` | `carrier_process_name` | "agent.exe" | UDM 进程无 name，名称在 file 对象 |
| `process_path` | "C:\\Program Files\\Acme\\agent.exe" | `roles.carriers[0].process.path` | `roles_obj.carriers[0].process.path` | "C:\\Program Files\\Acme\\agent.exe" |  |

## 二、不落库字段

| WPL 字段 | WPL 值 | 原因 |
|---|---|---|
| `custom_group_paths` | "总部/研发中心" | 组织分组路径原始串，三标准无锚点 |
| `dst_is_ipv6` | "false" | 候选删除：IP 值本身决定地址族，仅质量校验 |
| `inout` | "out" | 归一为 inbound/outbound 开放值；XDM 无 direction（经 source/target 表达）；只作方向事实不改变两端角色 |
| `network_connection_initiated` | "true" | 方向校验事实，仅用于校验 source/target 角色，不落标准路径 |
| `src_is_ipv6` | "false" | 候选删除：IP 值本身决定地址族，仅质量校验 |
| `timestamp` | 1734490012500 | 条件回退字段：仅主事件时间缺失或无效时用于 occur_time；本样例未采用 |
| `type` | "ip_access" | WPL 规则类型 process_details，非标准字段；SDM 保留原值 |
| `event_type` | "connection_established" | 天擎动作枚举，SDM 侧按转换表映射 process_launch/process_termination/process_uncategorized |

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
| `operation` | `constant` | `constant.log_semantics` | "open" | `—` | confirmed；当前日志类型的 expected 事件语义 |
| `outcome` | `constant` | `constant.log_semantics` | "success" | `—` | confirmed；当前日志类型的 expected 事件语义 |
| `severity` | `constant` | `constant.log_semantics` | "info" | `—` | confirmed；当前日志类型的 expected 事件语义 |

### 5.2 Content 区

| SDM 字段 | 规则类型 | WPL 字段 | 映射/赋值 | 未命中 | 状态与证据 |
|---|---|---|---|---|---|
| `extensions.profiles.endpoint_asset.ownership.organization.id` | `projection` | `asset_oid` | "org-2653788242175861718" | `—` | confirmed；组织资产节点 ID，三标准无锚点（国产组织模型） |
| `roles.target.host.name` | `projection` | `dst_host_name` | "api.example.net" | `—` | confirmed； |
| `occur_time` | `projection` | `event_date_creation` | 1734490012000 | `—` | confirmed；来源原始事件时间；OCSF metadata.original_time 语义完全对应；UDM event_timestamp 已核实；XDM 字段树无事件时间页 |
| `roles.related[0].process.cmdline` | `projection` | `process_parent_command_line` | "C:\\Windows\\System32\\services.exe" | `—` | confirmed； |
| `roles.related[0].process.file.internal_name` | `projection` | `process_parent_internal_name` | "services.exe" | `—` | confirmed；父进程位置由事件类型决定（process_event 落 source.process，ip_access/file_write 落 related[]） |
| `roles.related[0].process.name` | `projection` | `process_parent_name` | "services.exe" | `—` | confirmed；XDM 只有 parent_id 平铺 ID，无父进程对象；父进程位置由事件类型决定（process_event 落 source.process，ip_access/file_write 落 related[]） |
| `roles.related[0].process.file.original_name` | `projection` | `process_parent_original_name` | "services.exe" | `—` | confirmed；同 process_original_name；父进程位置由事件类型决定 |
| `roles.related[0].process.file.signatures[0].signer` | `projection` | `process_parent_sign` | "Microsoft Windows Publisher" | `—` | confirmed；父进程位置由事件类型决定 |
| `roles.carriers[0].process.file.hashes.sha1` | `projection` | `process_sha1` | "6b2f9d1f50d57c6c30c2f6f1e34c5f3a7f7d4c2e" | `—` | confirmed；XDM executable 无 sha1（只有 md5/sha256）；registry v17 已注册标准路径（target/source/carriers 进程 file 均可用） |
| `roles.source.host.name` | `projection` | `src_host_name` | "DESKTOP-EX01" | `—` | confirmed；unknown 等缺失占位值不写入 |
| `source_original_event_id` | `projection` | `uuid` | "61794FDE-6769-464E-B071-6CE07B01FEE4" | `—` | confirmed；来源原始事件 ID，参与确定性 event_id；UDM product_log_id 定义为 vendor GUID 完全对应 |
| `roles.source.host.name` | `projection` | `computer_name` | "DESKTOP-EX01" | `—` | confirmed；受管终端主机名，投影 source_host |
| `roles.target.endpoint.ip` | `projection` | `dst_ip_addr` | "203.0.113.25" | `—` | confirmed；网络目标方端点 IP，投影 target_ip |
| `roles.target.endpoint.port` | `projection` | `dst_port` | 443 | `—` | confirmed；WPL 为字符串，写前转 0-65535 整数 |
| `extensions.profiles.endpoint_asset.ownership.group.id` | `projection` | `gid` | "4f9c3833b800d1f7" | `—` | confirmed；资产分组 ID，三标准无锚点 |
| `facets.network.protocol` | `projection` | `network_protocol` | "tcp" | `—` | confirmed；统一为小写标准值（tcp/udp）；OCSF 在 connection_info、UDM/XDM 在 ip_protocol |
| `roles.carriers[0].process.cmdline` | `projection` | `process_command_line` | "C:\\Program Files\\Acme\\agent.exe --sync" | `—` | confirmed；OCSF 字段名是 cmd_line 非 command_line |
| `roles.target.process.file.internal_name` | `projection` | `process_internal_name` | "agent.exe" | `—` | confirmed；OCSF 字段名直接对应；05 已注册标准路径 |
| `roles.carriers[0].process.file.original_name` | `projection` | `process_original_name` | "AcmeAgent.exe" | `—` | confirmed；PE OriginalFilename；OCSF 无专门字段（internal_name 语义不同）；registry v17 已注册标准路径 |
| `roles.related[0].process.path` | `projection` | `process_parent_path` | "C:\\Windows\\System32\\services.exe" | `—` | confirmed； |
| `roles.carriers[0].process.file.signatures[0].signer` | `projection` | `process_sign` | "Acme Security Ltd." | `—` | confirmed；05 已注册标准路径 |
| `roles.carriers[0].process.user.name` | `projection` | `process_user` | "NT AUTHORITY\\SYSTEM" | `—` | confirmed；当前进程的用户；角色由事件决定——process_event 落 target.process.user，ip_access/file_write 落 carriers[].process.user |
| `roles.carriers[0].process.file.version` | `projection` | `process_version` | "203.0.113.252" | `—` | confirmed；UDM/XDM 无文件版本字段；registry v17 已注册标准路径 |
| `source_ip` | `projection` | `report_ip` | "198.51.100.211" | `—` | confirmed；同 client_report_ip；与 client_ip 不同时禁止静默丢弃 |
| `roles.source.endpoint.ip` | `projection` | `src_ip_addr` | "198.51.100.211" | `—` | confirmed；网络主动方端点 IP，投影 source_ip（与终端属性 host.ip 区分） |
| `roles.source.endpoint.port` | `projection` | `src_port` | 51532 | `—` | confirmed；转 0-65535 整数 |
| `roles.source.host.id` | `projection` | `asset_id` | "2868257359929541780" | `—` | confirmed；受管终端资产 ID，参与 host_ref_id |
| `extensions.profiles.endpoint_asset.agent.id` | `projection` | `client_id` | "0881058-dfb9a23257c64098060e699601b17217" | `—` | confirmed；天擎 Agent ID，不等于 asset_id；OCSF 以 device.uid 承载 agent 设备 |
| `roles.source.host.ip` | `projection` | `ip` | "198.51.100.211" | `—` | confirmed；终端属性 IP，不自动投影 source_ip；OCSF device.ip 弃用转 network_interfaces |
| `extensions.profiles.endpoint_asset.ownership.group.name` | `projection` | `group_name` | "研发终端" | `—` | confirmed；资产分组名，三标准无锚点 |
| `roles.source.host.mac` | `projection` | `mac` | "00:00:5E:00:53:23" | `—` | confirmed；受管终端主机 MAC，规范化为冒号分隔小写格式 |
| `extensions.profiles.endpoint_asset.agent.fingerprint_id` | `projection` | `mid` | "ec80b820d87d7cd7ac916240bcdff7215ae3118feaf070c13afbf06e69af4eb3" | `—` | confirmed；Agent/终端指纹，三标准无锚点 |
| `roles.target.process.uid` | `projection` | `process_guid` | "4eacb509de8348659c847be955b6e1f1" | `—` | confirmed；三标准均无 guid 字段名；32hex 可落 OCSF uid |
| `roles.target.process.pid` | `projection` | `process_id` | "2716" | `—` | confirmed；与 pid 同值，取一即可 |
| `roles.carriers[0].process.file.hashes.md5` | `projection` | `process_md5` | "a7a77e44a5d80b2191a47f2ee2a30a10" | `—` | confirmed；哈希统一小写 |
| `roles.target.process.name` | `projection` | `process_name` | "agent.exe" | `—` | confirmed；UDM 进程无 name，名称在 file 对象 |
| `roles.carriers[0].process.path` | `projection` | `process_path` | "C:\\Program Files\\Acme\\agent.exe" | `—` | confirmed； |

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
