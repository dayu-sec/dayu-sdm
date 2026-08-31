# WPL → SDM Event 字段映射

> 样例：`upload_to_site.expected-sdm-event.json`；WPL 字段 228 个，映射 21，不落库 207，排除 0；另有平台默认、派生及结构字段 40 项。
> SDM 落位为逻辑路径；expected 位置为该样例中的实际物理 JSON 路径。

## 一、映射字段

| WPL 字段 | WPL 值 | SDM 落位 | expected 位置 | expected 值 | 说明 |
|---|---|---|---|---|---|
| `client_info/asset_version/main_program_version` | "10.7.0.2815" | `extensions.profiles.endpoint_asset.agent.version` | `extensions_obj.profiles.endpoint_asset.agent.version` | "10.7.0.2815" | 按当前 expected 事件结构映射 |
| `remote_file_path` | "/data/liaoqq/lqq//外部数据管理平台运营商接口迁移设计方案v1(1).docx" | `roles.target.file.path` | `roles_obj.target.file.path` | "/data/liaoqq/lqq//外部数据管理平台运营商接口迁移设计方案v1(1).docx" | 按当前 expected 事件结构映射 |
| `asset_id` | "2803747593140568836" | `roles.source.host.id` | `roles_obj.source.host.id` | "2803747593140568836" | 按当前 expected 事件结构映射 |
| `transfer_method` | "upload_to_site" | `operation` | `operation` | "upload" | 已确认 upload_to_site 映射为 operation=upload |
| `client_login_account` | "LQQ" | `roles.source.account.name` | `roles_obj.source.account.name` | "LQQ" | 按当前 expected 事件结构映射 |
| `client_os_version_main` | "Windows 10" | `roles.source.host.os.name` | `roles_obj.source.host.os.name` | "Windows 10" | 按当前 expected 事件结构映射 |
| `client_os_version_build_version` | "19043.2364" | `roles.source.host.os.version` | `roles_obj.source.host.os.version` | "19043.2364" | 按当前 expected 事件结构映射 |
| `client_mac` | "90-98-38-CC-62-87" | `roles.source.host.mac` | `roles_obj.source.host.mac` | "90:98:38:cc:62:87" | 按当前 expected 事件结构映射 |
| `file_size` | "410583" | `roles.target.file.size` | `roles_obj.target.file.size` | 410583 | 按字节转换为整数；仍需厂商字段说明确认单位 |
| `client_mid` | "95a443509a4d3a7eaca6d0492ec9b1a0889402e1cfe73d1b09f1113b47cf4859" | `extensions.profiles.endpoint_asset.agent.fingerprint_id` | `extensions_obj.profiles.endpoint_asset.agent.fingerprint_id` | "95a443509a4d3a7eaca6d0492ec9b1a0889402e1cfe73d1b09f1113b47cf4859" | 按当前 expected 事件结构映射 |
| `client_id` | "2569671-715b7f777025ef6170248b55e3e29b50" | `extensions.profiles.endpoint_asset.agent.id` | `extensions_obj.profiles.endpoint_asset.agent.id` | "2569671-715b7f777025ef6170248b55e3e29b50" | 按当前 expected 事件结构映射 |
| `asset_oid` | "2715543661537396001" | `extensions.profiles.endpoint_asset.ownership.organization.id` | `extensions_obj.profiles.endpoint_asset.ownership.organization.id` | "2715543661537396001" | 按当前 expected 事件结构映射 |
| `process_name` | "explorer.exe" | `roles.source.process.name` | `roles_obj.source.process.name` | "explorer.exe" | 按当前 expected 事件结构映射 |
| `client_ip` | "198.51.100.243" | `roles.source.host.ip` | `roles_obj.source.host.ip` | "198.51.100.243" | 按当前 expected 事件结构映射 |
| `create_time` | 1779072179000 | `occur_time` | `occur_time` | 1779072179000 | 按当前 expected 事件结构映射 |
| `group_node_id` | "4e1ffdfb48000017" | `extensions.profiles.endpoint_asset.ownership.group.id` | `extensions_obj.profiles.endpoint_asset.ownership.group.id` | "4e1ffdfb48000017" | 按当前 expected 事件结构映射 |
| `file_id` | "974ACD69B7B145CDB198464213A51E9F" | `roles.target.file.id` | `roles_obj.target.file.id` | "974ACD69B7B145CDB198464213A51E9F" | 按当前 expected 事件结构映射 |
| `local_file_path` | "外部数据管理平台运营商接口迁移设计方案v1(1).docx" | `roles.related[0].file.path` | `roles_obj.related[0].file.path` | "外部数据管理平台运营商接口迁移设计方案v1(1).docx" | 本地同名源文件，构造 related[0]，relation_type=source_file |
| `client_name` | "DESKTOP-lqq" | `roles.source.host.name` | `roles_obj.source.host.name` | "DESKTOP-lqq" | 按当前 expected 事件结构映射 |
| `file_name` | "外部数据管理平台运营商接口迁移设计方案v1(1).docx" | `roles.target.file.name` | `roles_obj.target.file.name` | "外部数据管理平台运营商接口迁移设计方案v1(1).docx" | 按当前 expected 事件结构映射 |
| `group_node_name` | "产品研发部" | `extensions.profiles.endpoint_asset.ownership.group.name` | `extensions_obj.profiles.endpoint_asset.ownership.group.name` | "产品研发部" | 按当前 expected 事件结构映射 |

## 二、不落库字段

| WPL 字段 | WPL 值 | 原因 |
|---|---|---|
| `client_info/access_point/deployment_id/asset_id/oid` | "2715543661537396001" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `client_info/access_point/deployment_id/asset_id/id` | "2803747593140568836" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `client_info/access_point/deployment_id/id` | "skylar_console_id" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `client_info/access_point/id` | "console.qax-ats-ca.2715543661537396001.9ox5-x6qw-q32m-1zyd" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `client_info/mid` | "95a443509a4d3a7eaca6d0492ec9b1a0889402e1cfe73d1b09f1113b47cf4859" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `client_info/client_type` | "win" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `client_info/core_number` | 6 | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `client_info/mac` | "90-98-38-CC-62-87" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `client_info/update_time` | "2026-05-18T00:09:43Z" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `client_info/ipv6` | "" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `client_info/ie_version` | "11.0.19041.1566" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `client_info/computer_working_group` | "WORKGROUP" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `client_info/tos/desktop` | true | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `client_info/tos/os` | 1 | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `client_info/tos/dist` | "Windows 10 CoreCountrySpecific" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `client_info/tos/arch` | 2 | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `client_info/tos/version/kernel_version` | "19043.2364" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `client_info/tos/version/version` | "21H1" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `client_info/os_bit` | 1 | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `client_info/report_ipv6` | "" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `client_info/state` | 0 | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `client_info/system_language` | "zh-JT" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `client_info/report_ip` | "203.0.113.186" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `client_info/create_time` | "2023-03-03T04:01:55Z" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `client_info/os` | 0 | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `client_info/asset_version/update_time` | "2026-05-18T00:49:41Z" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `client_info/asset_version/peripheral_devices_version` | "2026.02.09.1906" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `client_info/asset_version/create_time` | "2023-03-03T04:01:55Z" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `client_info/asset_version/software_library_version` | "2026.05.12.0841" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `client_info/asset_version/virus_bd_version` | "203.0.113.73" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `client_info/asset_version/delete_at` | "1970-01-01T00:00:00Z" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `client_info/asset_version/virus_version` | "2026.05.17.3001" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `client_info/asset_version/patch_version` | "2026.05.13.1000" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `client_info/ip` | "198.51.100.243" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `client_info/os_version/release_id` | "21H1" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `client_info/os_version/build_version` | "19043.2364" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `client_info/os_version/main` | "Windows 10" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `client_info/os_version/describe` | "CoreCountrySpecific" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `client_info/asset_computer/update_time` | "2026-05-18T00:10:47Z" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `client_info/asset_computer/create_time` | "2023-03-03T04:02:00Z" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `client_info/asset_computer/board_serial_number` | "YLYYU21602001810" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `client_info/asset_computer/board_model` | "HUAWEI PUL-WDX9-PCB-B1" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `client_info/asset_computer/delete_at` | "1970-01-01T00:00:00Z" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `client_info/asset_computer/board_bios` | "HUAWEI 1.22 :12/18/2021" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `client_info/asset_computer/brand_model` | "HUAWEI PUL-WDX9(MateStation)" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `client_info/asset_computer/board_chipset` | "PCI standard ISA bridge" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `client_info/asset_computer/board_temperature` | "" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `client_info/sys_space` | "53772" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `client_info/login_account` | "LQQ" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `client_info/memory_size` | 16384 | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `client_info/domain` | "" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `client_info/name` | "DESKTOP-lqq" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `client_info/activation` | true | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `client_info/online_info/last_time` | "2026-05-18T02:43:03.002463152Z" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `client_info/online_info/is_online` | true | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `client_info/online_info/state` | 0 | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `group_info[0]/node_type` | 6 | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `group_info[0]/tree_id` | "4dd1fa38fe000017" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `group_info[0]/node_name` | "pf_2818800716439617559" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `group_info[0]/oid` | "2803747593140568836" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `group_info[0]/node_id` | "4dedb78020000017" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `group_info[1]/node_type` | 6 | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `group_info[1]/tree_id` | "4dd1fa38fe000017" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `group_info[1]/node_name` | "pf_2808379448745787415" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `group_info[1]/oid` | "2803747593140568836" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `group_info[1]/node_id` | "2803769066869751831" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `group_info[2]/node_type` | 6 | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `group_info[2]/tree_id` | "4dd1fa38fe000017" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `group_info[2]/node_name` | "pf_2818800926540693527" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `group_info[2]/oid` | "2803747593140568836" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `group_info[2]/node_id` | "4dedb78020000017" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `group_info[3]/node_type` | 6 | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `group_info[3]/tree_id` | "4dd1fa38fe000017" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `group_info[3]/node_name` | "pf_2818800420841848855" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `group_info[3]/oid` | "2803747593140568836" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `group_info[3]/node_id` | "4dedb78020000017" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `group_info[4]/node_type` | 6 | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `group_info[4]/tree_id` | "4dd1fa38fe000017" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `group_info[4]/node_name` | "pf_2818800326822330391" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `group_info[4]/oid` | "2803747593140568836" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `group_info[4]/node_id` | "4dedb78020000017" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `group_info[5]/node_type` | 6 | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `group_info[5]/tree_id` | "4dd1fa38fe000017" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `group_info[5]/node_name` | "pf_2818800639163760663" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `group_info[5]/oid` | "2803747593140568836" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `group_info[5]/node_id` | "4dedb78020000017" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `group_info[6]/node_type` | 6 | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `group_info[6]/tree_id` | "4dd1fa38fe000017" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `group_info[6]/node_name` | "pf_2825804518938116201" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `group_info[6]/oid` | "2803747593140568836" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `group_info[6]/node_id` | "4dedb78020000017" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `group_info[7]/node_type` | 6 | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `group_info[7]/tree_id` | "4dd1fa38fe000017" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `group_info[7]/node_name` | "pf_2818800573078306839" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `group_info[7]/oid` | "2803747593140568836" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `group_info[7]/node_id` | "4dedb78020000017" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `group_info[8]/node_type` | 6 | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `group_info[8]/tree_id` | "4dd1fa38fe000017" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `group_info[8]/node_name` | "pf_2818800778397876247" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `group_info[8]/oid` | "2803747593140568836" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `group_info[8]/node_id` | "4dedb78020000017" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `group_info[9]/node_type` | 6 | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `group_info[9]/tree_id` | "4dd1fa38fe000017" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `group_info[9]/node_name` | "pf_2818800989824352279" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `group_info[9]/oid` | "2803747593140568836" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `group_info[9]/node_id` | "4dedb78020000017" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `group_info[10]/node_type` | 6 | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `group_info[10]/tree_id` | "4dd1fa38fe000017" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `group_info[10]/node_name` | "pf_2818801961560702999" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `group_info[10]/oid` | "2803747593140568836" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `group_info[10]/node_id` | "2803769066869751831" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `group_info[11]/node_type` | 6 | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `group_info[11]/tree_id` | "4dd1fa38fe000017" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `group_info[11]/node_name` | "pf_2950917402323320921" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `group_info[11]/oid` | "2803747593140568836" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `group_info[11]/node_id` | "2803769066869751831" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `group_info[12]/node_type` | 0 | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `group_info[12]/tree_id` | "4dd1fa38fe000017" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `group_info[12]/node_name` | "产品研发部" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `group_info[12]/oid` | "2803747593140568836" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `group_info[12]/node_id` | "4dedb78020000017" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `group_info[13]/node_type` | 6 | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `group_info[13]/tree_id` | "4dd1fa38fe000017" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `group_info[13]/node_name` | "pf_2945260826946175065" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `group_info[13]/oid` | "2803747593140568836" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `group_info[13]/node_id` | "4dedb78020000017" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `group_info[14]/node_type` | 6 | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `group_info[14]/tree_id` | "4dd1fa38fe000017" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `group_info[14]/node_name` | "pf_2931055878184370265" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `group_info[14]/oid` | "2803747593140568836" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `group_info[14]/node_id` | "2803769066869751831" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `group_info[15]/node_type` | 6 | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `group_info[15]/tree_id` | "4dd1fa38fe000017" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `group_info[15]/node_name` | "pf_2925255878045073413" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `group_info[15]/oid` | "2803747593140568836" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `group_info[15]/node_id` | "2803769066869751831" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `group_info[16]/node_type` | 6 | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `group_info[16]/tree_id` | "4dd1fa38fe000017" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `group_info[16]/node_name` | "pf_2970631737564004507" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `group_info[16]/oid` | "2803747593140568836" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `group_info[16]/node_id` | "4dedb78020000017" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `group_info[17]/node_type` | 6 | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `group_info[17]/tree_id` | "4dd1fa38fe000017" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `group_info[17]/node_name` | "pf_2904960475236139158" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `group_info[17]/oid` | "2803747593140568836" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `group_info[17]/node_id` | "2803769066869751831" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `group_info[18]/node_type` | 6 | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `group_info[18]/tree_id` | "4dd1fa38fe000017" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `group_info[18]/node_name` | "pf_2903076336702587030" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `group_info[18]/oid` | "2803747593140568836" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `group_info[18]/node_id` | "2803769066869751831" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `group_info[19]/node_type` | 6 | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `group_info[19]/tree_id` | "4dd1fa38fe000017" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `group_info[19]/node_name` | "pf_2876257412405264605" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `group_info[19]/oid` | "2803747593140568836" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `group_info[19]/node_id` | "4dedb78020000017" | 终端资产或分组快照字段；当前事件不复制完整快照，原值保留在 raw_msg |
| `client_activation` | "1" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `client_core_number` | 6 | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `client_os_bit` | 1 | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `client_state` | 0 | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `usb_type` | "0" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `client_create_time` | "2023-03-03T04:01:55Z" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `client_os_version_describe` | "CoreCountrySpecific" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `handle` | "0" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `collect_time` | "1779072183464" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `group_tree_id` | "4dd1fa38fe000017;4dd1fa38fe000017;4dd1fa38fe000017;4dd1fa38fe000017;4dd1fa38fe000017;4dd1fa38fe000017;4dd1fa38fe000017;4dd1fa38fe000017;4dd1fa38fe000017;4dd1fa38fe000017;4dd1fa38fe000017;4dd1fa38fe000017;4dd1fa38fe000017;4dd1fa38fe000017;4dd1fa38fe000017;4dd1fa38fe000017;4dd1fa38fe000017;4dd1fa38fe000017;4dd1fa38fe000017;4dd1fa38fe000017" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `client_computer_working_group` | "WORKGROUP" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `result` | "0" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `client_report_ip` | "203.0.113.186" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `client_os` | 0 | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `behavior` | "0" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `local_file_is_exists` | "0" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `auth_node_id` | "2803769066869751831,4dedb78020000017,4e1ffdfb48000017" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `client_tos_arch` | 2 | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `path_level1` | "全网计算机" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `path_level2` | "湖南省农村信用社联合社" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `path_level3` | "产品研发部" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `path_level4` | "产品研发部" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `path_level5` | "产品研发部(本级)" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `path_level6` | "" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `path_level7` | "" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `path_level8` | "" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `path_level9` | "" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `client_os_version_release_id` | "21H1" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `client_domain` | "" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `operation_type` | "0" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `group_node_type` | "6;6;6;6;6;6;6;6;6;6;6;6;0;6;6;6;6;6;6;6" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `client_type` | "win" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `client_tos_dist` | "Windows 10 CoreCountrySpecific" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `client_tos_os` | 1 | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `group_node_path` | "[\"全网计算机\",\"湖南省农村信用社联合社\",\"产品研发部\"]" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `path_level10` | "" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `level` | 0 | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `group_oid` | "2803747593140568836;2803747593140568836;2803747593140568836;2803747593140568836;2803747593140568836;2803747593140568836;2803747593140568836;2803747593140568836;2803747593140568836;2803747593140568836;2803747593140568836;2803747593140568836;2803747593140568836;2803747593140568836;2803747593140568836;2803747593140568836;2803747593140568836;2803747593140568836;2803747593140568836;2803747593140568836" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `client_memory_size` | 16384 | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `client_ie_version` | "11.0.19041.1566" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `client_tos_version` | "21H1" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `transfer_channel` | "4" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `report_time` | 1779072179000 | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `client_sys_space` | "53772" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `client_report_ipv6` | "" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `client_nic_list` | "[]" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `client_system_language` | "zh-JT" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `client_update_time` | "2026-05-18T00:09:43Z" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `search_id` | "2715543661537396001_2803747593140568836_4dd1fa38fe000017_2803769066869751831_4dedb78020000017_4e1ffdfb48000017" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `syslog_topic` | "file_audit" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `audit_type` | "2" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |

## 四、平台默认、派生及结构字段

| 来源 | SDM 落位 | expected 值 | 赋值责任与说明 |
|---|---|---|---|
| `platform_context.tenant_id` | `tenant_id` | "" | 由平台上下文提供 |
| `derived.sha256('|'+mapping_id+'|'+source_original_event_id)` | `event_id` | "evt-80e08a623fe0fc61e19f5d5d485c7c6b1626197c3c7e5c288dce5f7450016736" | 按确定性规则 sha256('|'+mapping_id+'|'+source_original_event_id) 派生 |
| `platform_context.log_id` | `log_id` | "log-tianqing-file-audit-0001" | 由平台上下文提供 |
| `raw_log_input` | `raw_msg` | "{\"syslog_topic\":\"file_audit\",\"create_time\":1779072179,\"process_name\":\"explorer.exe\",\"transfer_method\":\"upload_to_site\",\"file_id\":\"974ACD69B7B145CDB198464213A51E9F\",\"file_name\":\"外部数据管理平台运营商接口迁移设计方案v1(1).docx\",\"remote_file_path\":\"/data/liaoqq/lqq//外部数据管理平台运营商接口迁移设计方案v1(1).docx\"}" | 由原始日志接入层保存，不由 OML 拼装 |
| `platform_context.ingest_time` | `ingest_time` | 1779072184001 | 由平台上下文提供 |
| `platform_context.parse_time` | `parse_time` | 1779072184120 | 由平台上下文提供 |
| `constant.sdm_schema_version` | `schema_version` | 2 | 使用平台/映射规则常量 sdm_schema_version |
| `constant.mapping_id` | `mapping_id` | "qax.tianqing.edr_file_audit" | 使用平台/映射规则常量 mapping_id |
| `constant.mapping_vendor` | `data_src_vendor` | "qax" | 使用平台/映射规则常量 mapping_vendor |
| `constant.mapping_product` | `data_src_product` | "tianqing" | 使用平台/映射规则常量 mapping_product |
| `constant.mapping_category` | `data_src_category` | "endpoint_security" | 使用平台/映射规则常量 mapping_category |
| `platform_context.data_src_instance_id` | `data_src_instance_id` | "collector-tianqing-poc-01" | 由平台上下文提供 |
| `constant.log_type` | `log_type` | "edr_file_audit" | 使用平台/映射规则常量 log_type |
| `constant.log_name` | `log_name` | "天擎文件审计日志" | 使用平台/映射规则常量 log_name |
| `constant.record_kind` | `record_kind` | "activity" | 使用平台/映射规则常量 record_kind |
| `constant.event_domain` | `event_domain` | "endpoint" | 使用平台/映射规则常量 event_domain |
| `constant.event_type` | `event_type` | "file_creation" | 使用平台/映射规则常量 event_type |
| `derived.enum_projection` | `outcome` | "observed" | 由 WPL 枚举或日志语义转换为 SDM 标准值 |
| `constant.default_severity` | `severity` | "info" | 当前日志类型未提供标准 severity，按映射默认值 info 装配 |
| `wpl.client_login_account` | `source_user` | "LQQ" | 由 WPL 字段 client_login_account 投影或转换后赋值 |
| `wpl.client_name` | `source_host` | "DESKTOP-lqq" | 由 WPL 字段 client_name 投影或转换后赋值 |
| `wpl.remote_file_path` | `target_file_path` | "/data/liaoqq/lqq//外部数据管理平台运营商接口迁移设计方案v1(1).docx" | 由 WPL 字段 remote_file_path 投影或转换后赋值 |
| `constant.mapping_vendor` | `observer_vendor` | "qax" | 使用平台/映射规则常量 mapping_vendor |
| `constant.mapping_product` | `observer_product` | "tianqing" | 使用平台/映射规则常量 mapping_product |
| `derived.entity_ref` | `roles.source.ref_id` | "host_2803747593140568836" | 按确定性规则 entity_ref 派生 |
| `constant.entity_type` | `roles.source.entity_type` | "host" | 使用平台/映射规则常量 entity_type |
| `derived.entity_ref` | `roles.target.ref_id` | "file_remote_974acd69b7b145cdb198464213a51e9f" | 按确定性规则 entity_ref 派生 |
| `constant.entity_type` | `roles.target.entity_type` | "file" | 使用平台/映射规则常量 entity_type |
| `derived.basename_extension` | `roles.target.file.extension` | "docx" | 从 WPL 文件名或路径按 basename/扩展名规则派生 |
| `constant.mapping_product` | `roles.observer.product.name` | "tianqing" | 使用平台/映射规则常量 mapping_product |
| `constant.mapping_vendor` | `roles.observer.device.vendor` | "qax" | 使用平台/映射规则常量 mapping_vendor |
| `derived.entity_ref` | `roles.related[0].ref_id` | "file_local_974acd69b7b145cdb198464213a51e9f" | 按确定性规则 entity_ref 派生 |
| `constant.entity_type` | `roles.related[0].entity_type` | "file" | 使用平台/映射规则常量 entity_type |
| `constant.relation_type` | `roles.related[0].relation_type` | "source_file" | 使用平台/映射规则常量 relation_type |
| `wpl.file_id` | `roles.related[0].file.id` | "974ACD69B7B145CDB198464213A51E9F" | 由 WPL 字段 file_id 投影或转换后赋值 |
| `derived.path_basename` | `roles.related[0].file.name` | "外部数据管理平台运营商接口迁移设计方案v1(1).docx" | 从对应的 WPL 文件或进程路径取 basename 派生 |
| `wpl.file_size` | `roles.related[0].file.size` | 410583 | 由 WPL 字段 file_size 投影或转换后赋值 |
| `derived.basename_extension` | `roles.related[0].file.extension` | "docx" | 从 WPL 文件名或路径按 basename/扩展名规则派生 |
| `constant.sdm_schema_version` | `extensions.schema_version` | 2 | 使用平台/映射规则常量 sdm_schema_version |
| `derived.entity_ref` | `extensions.profiles.endpoint_asset.subject_ref.ref_id` | "host_2803747593140568836" | 按确定性规则 entity_ref 派生 |

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
| `mapping_id` | `constant` | `constant.mapping_id` | "qax.tianqing.edr_file_audit" | `—` | confirmed；使用平台/映射规则常量 mapping_id |
| `data_src_vendor` | `constant` | `constant.mapping_vendor` | "qax" | `—` | confirmed；使用平台/映射规则常量 mapping_vendor |
| `data_src_product` | `constant` | `constant.mapping_product` | "tianqing" | `—` | confirmed；使用平台/映射规则常量 mapping_product |
| `data_src_category` | `constant` | `constant.mapping_category` | "endpoint_security" | `—` | confirmed；使用平台/映射规则常量 mapping_category |
| `data_src_instance_id` | `context` | `platform_context.data_src_instance_id` | `platform_context.data_src_instance_id` | `—` | confirmed；由平台上下文提供 |
| `log_type` | `constant` | `constant.log_type` | "edr_file_audit" | `—` | confirmed；使用平台/映射规则常量 log_type |
| `log_name` | `constant` | `constant.log_name` | "天擎文件审计日志" | `—` | confirmed；使用平台/映射规则常量 log_name |
| `record_kind` | `constant` | `constant.record_kind` | "activity" | `—` | confirmed；使用平台/映射规则常量 record_kind |
| `event_domain` | `constant` | `constant.event_domain` | "endpoint" | `—` | confirmed；使用平台/映射规则常量 event_domain |
| `event_type` | `constant` | `constant.event_type` | "file_creation" | `—` | confirmed；使用平台/映射规则常量 event_type |
| `event_category` | `constant` | `constant.event_category` | "audit" | `—` | confirmed；终端文件审计，PDF §3.11.1 |
| `severity` | `constant` | `constant.default_severity` | "info" | `—` | confirmed；当前日志类型未提供标准 severity，按映射默认值 info 装配 |
| `observer_vendor` | `constant` | `constant.mapping_vendor` | "qax" | `—` | confirmed；使用平台/映射规则常量 mapping_vendor |
| `observer_product` | `constant` | `constant.mapping_product` | "tianqing" | `—` | confirmed；使用平台/映射规则常量 mapping_product |
| `roles.source.ref_id` | `derived` | `derived.entity_ref` | `derived.entity_ref` | `—` | confirmed；按确定性规则 entity_ref 派生 |
| `roles.source.entity_type` | `constant` | `constant.entity_type` | "host" | `—` | confirmed；使用平台/映射规则常量 entity_type |
| `roles.target.ref_id` | `derived` | `derived.entity_ref` | `derived.entity_ref` | `—` | confirmed；按确定性规则 entity_ref 派生 |
| `roles.target.entity_type` | `constant` | `constant.entity_type` | "file" | `—` | confirmed；使用平台/映射规则常量 entity_type |
| `roles.target.file.extension` | `derived` | `derived.basename_extension` | `derived.basename_extension` | `—` | confirmed；从 WPL 文件名或路径按 basename/扩展名规则派生 |
| `roles.observer.product.name` | `constant` | `constant.mapping_product` | "tianqing" | `—` | confirmed；使用平台/映射规则常量 mapping_product |
| `roles.observer.device.vendor` | `constant` | `constant.mapping_vendor` | "qax" | `—` | confirmed；使用平台/映射规则常量 mapping_vendor |
| `roles.related[0].ref_id` | `derived` | `derived.entity_ref` | `derived.entity_ref` | `—` | confirmed；按确定性规则 entity_ref 派生 |
| `roles.related[0].entity_type` | `constant` | `constant.entity_type` | "file" | `—` | confirmed；使用平台/映射规则常量 entity_type |
| `roles.related[0].relation_type` | `constant` | `constant.relation_type` | "source_file" | `—` | confirmed；使用平台/映射规则常量 relation_type |
| `roles.related[0].file.name` | `derived` | `derived.path_basename` | `derived.path_basename` | `—` | confirmed；从对应的 WPL 文件或进程路径取 basename 派生 |
| `roles.related[0].file.extension` | `derived` | `derived.basename_extension` | `derived.basename_extension` | `—` | confirmed；从 WPL 文件名或路径按 basename/扩展名规则派生 |
| `extensions.profiles.endpoint_asset.subject_ref.ref_id` | `derived` | `derived.entity_ref` | `derived.entity_ref` | `—` | confirmed；按确定性规则 entity_ref 派生 |
| `outcome` | `constant` | `log_semantics` | "observed" | `—` | confirmed；由该日志类型的事件事实确定，不是来源枚举转换 |
| `ingest_time` | `context` | `platform_context.ingest_time` | `read(ingest_time)` | `—` | confirmed；expected 事件中的平台上下文字段 |
| `parse_time` | `context` | `platform_context.parse_time` | `read(parse_time)` | `—` | confirmed；expected 事件中的平台上下文字段 |
| `operation` | `constant` | `constant.log_semantics` | "upload" | `—` | confirmed；当前日志类型的 expected 事件语义 |

### 5.2 Content 区

| SDM 字段 | 规则类型 | WPL 字段 | 映射/赋值 | 未命中 | 状态与证据 |
|---|---|---|---|---|---|
| `outcome` | `dictionary` | `derived.enum_projection` | — | `preserve_in_extension_and_review` | partial；由 WPL 枚举或日志语义转换为 SDM 标准值 |
| `source_user` | `projection` | `client_login_account` | `wpl.client_login_account` | `—` | confirmed；由 WPL 字段 client_login_account 投影或转换后赋值 |
| `source_host` | `projection` | `client_name` | `wpl.client_name` | `—` | confirmed；由 WPL 字段 client_name 投影或转换后赋值 |
| `target_file_path` | `projection` | `remote_file_path` | `wpl.remote_file_path` | `—` | confirmed；由 WPL 字段 remote_file_path 投影或转换后赋值 |
| `roles.related[0].file.id` | `projection` | `file_id` | `wpl.file_id` | `—` | confirmed；由 WPL 字段 file_id 投影或转换后赋值 |
| `roles.related[0].file.size` | `projection` | `file_size` | `wpl.file_size` | `—` | confirmed；由 WPL 字段 file_size 投影或转换后赋值 |
| `extensions.profiles.endpoint_asset.agent.version` | `projection` | `client_info/asset_version/main_program_version` | "10.7.0.2815" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.target.file.path` | `projection` | `remote_file_path` | "/data/liaoqq/lqq//外部数据管理平台运营商接口迁移设计方案v1(1).docx" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.source.host.id` | `projection` | `asset_id` | "2803747593140568836" | `—` | confirmed；按当前 expected 事件结构映射 |
| `operation` | `projection` | `transfer_method` | "upload" | `—` | confirmed；已确认 upload_to_site 映射为 operation=upload |
| `roles.source.account.name` | `projection` | `client_login_account` | "LQQ" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.source.host.os.name` | `projection` | `client_os_version_main` | "Windows 10" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.source.host.os.version` | `projection` | `client_os_version_build_version` | "19043.2364" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.source.host.mac` | `projection` | `client_mac` | "90:98:38:cc:62:87" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.target.file.size` | `projection` | `file_size` | 410583 | `—` | confirmed；按字节转换为整数；仍需厂商字段说明确认单位 |
| `extensions.profiles.endpoint_asset.agent.fingerprint_id` | `projection` | `client_mid` | "95a443509a4d3a7eaca6d0492ec9b1a0889402e1cfe73d1b09f1113b47cf4859" | `—` | confirmed；按当前 expected 事件结构映射 |
| `extensions.profiles.endpoint_asset.agent.id` | `projection` | `client_id` | "2569671-715b7f777025ef6170248b55e3e29b50" | `—` | confirmed；按当前 expected 事件结构映射 |
| `extensions.profiles.endpoint_asset.ownership.organization.id` | `projection` | `asset_oid` | "2715543661537396001" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.source.process.name` | `projection` | `process_name` | "explorer.exe" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.source.host.ip` | `projection` | `client_ip` | "198.51.100.243" | `—` | confirmed；按当前 expected 事件结构映射 |
| `occur_time` | `projection` | `create_time` | 1779072179000 | `—` | confirmed；按当前 expected 事件结构映射 |
| `extensions.profiles.endpoint_asset.ownership.group.id` | `projection` | `group_node_id` | "4e1ffdfb48000017" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.target.file.id` | `projection` | `file_id` | "974ACD69B7B145CDB198464213A51E9F" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.related[0].file.path` | `projection` | `local_file_path` | "外部数据管理平台运营商接口迁移设计方案v1(1).docx" | `—` | confirmed；本地同名源文件，构造 related[0]，relation_type=source_file |
| `roles.source.host.name` | `projection` | `client_name` | "DESKTOP-lqq" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.target.file.name` | `projection` | `file_name` | "外部数据管理平台运营商接口迁移设计方案v1(1).docx" | `—` | confirmed；按当前 expected 事件结构映射 |
| `extensions.profiles.endpoint_asset.ownership.group.name` | `projection` | `group_node_name` | "产品研发部" | `—` | confirmed；按当前 expected 事件结构映射 |

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
