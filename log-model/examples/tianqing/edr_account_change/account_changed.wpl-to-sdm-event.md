# WPL → SDM Event 字段映射

> 样例：`account_changed.expected-sdm-event.json`；WPL 字段 45 个，映射 28，不落库 16，排除 1；另有平台默认、派生及结构字段 35 项。
> SDM 落位为逻辑路径；expected 位置为该样例中的实际物理 JSON 路径。

## 一、映射字段

| WPL 字段 | WPL 值 | SDM 落位 | expected 位置 | expected 值 | 说明 |
|---|---|---|---|---|---|
| `process_parent_command_line` | "wininit.exe" | `roles.related[0].process.cmdline` | `roles_obj.related[0].process.cmdline` | "wininit.exe" | 按当前 expected 事件结构映射 |
| `process_parent_internal_name` | "WinInit" | `roles.related[0].process.file.internal_name` | `roles_obj.related[0].process.file.internal_name` | "WinInit" | 按当前 expected 事件结构映射 |
| `process_parent_name` | "wininit.exe" | `roles.related[0].process.name` | `roles_obj.related[0].process.name` | "wininit.exe" | 按当前 expected 事件结构映射 |
| `process_parent_original_name` | "WinInit.exe" | `roles.related[0].process.file.original_name` | `roles_obj.related[0].process.file.original_name` | "WinInit.exe" | 按当前 expected 事件结构映射 |
| `process_parent_sign` | "Microsoft Windows Publisher" | `roles.related[0].process.file.signatures[0].signer` | `roles_obj.related[0].process.file.signatures[0].signer` | "Microsoft Windows Publisher" | 按当前 expected 事件结构映射 |
| `process_sha1` | "20a244c0440ed0b418f454f8a12ed0de6a8bd6d2" | `roles.source.process.file.hashes.sha1` | `roles_obj.source.process.file.hashes.sha1` | "20a244c0440ed0b418f454f8a12ed0de6a8bd6d2" | 按当前 expected 事件结构映射 |
| `uuid` | "16EEBAD5-E974-405F-9603-973D8FA464C9" | `source_original_event_id` | `source_original_event_id` | "16EEBAD5-E974-405F-9603-973D8FA464C9" | 按当前 expected 事件结构映射 |
| `process_original_name` | "lsass.exe" | `roles.source.process.file.original_name` | `roles_obj.source.process.file.original_name` | "lsass.exe" | 按当前 expected 事件结构映射 |
| `process_parent_path` | "C:\\WINDOWS\\System32\\wininit.exe" | `roles.related[0].process.path` | `roles_obj.related[0].process.path` | "C:\\Windows\\System32\\wininit.exe" | 按当前 expected 事件结构映射 |
| `process_sign` | "Microsoft Windows Publisher" | `roles.source.process.file.signatures[0].signer` | `roles_obj.source.process.file.signatures[0].signer` | "Microsoft Windows Publisher" | 按当前 expected 事件结构映射 |
| `process_user` | "NT AUTHORITY\\SYSTEM" | `roles.source.process.user.name` | `roles_obj.source.process.user.name` | "NT AUTHORITY\\SYSTEM" | 按当前 expected 事件结构映射 |
| `account_name` | "XXXXXX" | `roles.target.account.name` | `roles_obj.target.account.name` | "XXXXXX" | 目标账户名称；样例值已脱敏为 XXXXXX |
| `account_user` | "XXXXXX" | `target_user` | `target_user` | "XXXXXX" | 投影为 target_user；样例值已脱敏，未据此推断账户类型 |
| `asset_id` | "100231" | `roles.source.host.id` | `roles_obj.source.host.id` | "100231" | 按当前 expected 事件结构映射 |
| `asset_oid` | "2653788242175861718" | `extensions.profiles.endpoint_asset.ownership.organization.id` | `extensions_obj.profiles.endpoint_asset.ownership.organization.id` | "2653788242175861718" | 按当前 expected 事件结构映射 |
| `client_id` | "4709450-42a2c1474b27be3f445f30952XXXXXX" | `extensions.profiles.endpoint_asset.agent.id` | `extensions_obj.profiles.endpoint_asset.agent.id` | "4709450-42a2c1474b27be3f445f30952XXXXXX" | 按当前 expected 事件结构映射 |
| `computer_name` | "A0XXXXX-NC02" | `roles.source.host.name` | `roles_obj.source.host.name` | "A0XXXXX-NC02" | 按当前 expected 事件结构映射 |
| `event_date_creation` | "1629440451126" | `occur_time` | `occur_time` | 1629440451126 | 按当前 expected 事件结构映射 |
| `event_type` | "userinfo_changed" | `event_type` | `event_type` | "user_uncategorized" | 修改用户信息；标准无 account_change，不是改密 |
| `mac` | "XX-XX-XX-XX-XX-XX" | `roles.source.host.mac` | `roles_obj.source.host.mac` | "XX:XX:XX:XX:XX:XX" | 按当前 expected 事件结构映射 |
| `mid` | "d4bb9bc2621630fdc27154105d9da5630940658a996fcfe8824965d3d8XXXXXX" | `extensions.profiles.endpoint_asset.agent.fingerprint_id` | `extensions_obj.profiles.endpoint_asset.agent.fingerprint_id` | "d4bb9bc2621630fdc27154105d9da5630940658a996fcfe8824965d3d8XXXXXX" | 按当前 expected 事件结构映射 |
| `process_command_line` | "C:\\WINDOWS\\system32\\lsass.exe" | `roles.source.process.cmdline` | `roles_obj.source.process.cmdline` | "C:\\WINDOWS\\system32\\lsass.exe" | 按当前 expected 事件结构映射 |
| `process_guid` | "f4cdcc09ee421ef79d1136ebdbdda395" | `roles.source.process.uid` | `roles_obj.source.process.uid` | "f4cdcc09ee421ef79d1136ebdbdda395" | 按当前 expected 事件结构映射 |
| `process_id` | "824" | `roles.source.process.pid` | `roles_obj.source.process.pid` | "824" | 按当前 expected 事件结构映射 |
| `process_internal_name` | "lsass.exe" | `roles.source.process.file.internal_name` | `roles_obj.source.process.file.internal_name` | "lsass.exe" | 按当前 expected 事件结构映射 |
| `process_md5` | "5ae8589cdde46ed132aef8280bc8894a" | `roles.source.process.file.hashes.md5` | `roles_obj.source.process.file.hashes.md5` | "5ae8589cdde46ed132aef8280bc8894a" | 按当前 expected 事件结构映射 |
| `process_name` | "lsass.exe" | `roles.source.process.name` | `roles_obj.source.process.name` | "lsass.exe" | 按当前 expected 事件结构映射 |
| `process_path` | "C:\\WINDOWS\\System32\\lsass.exe" | `roles.source.process.path` | `roles_obj.source.process.path` | "C:\\Windows\\System32\\lsass.exe" | 按当前 expected 事件结构映射 |

## 二、不落库字段

| WPL 字段 | WPL 值 | 原因 |
|---|---|---|
| `task_id` | "0" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `sub_task_id` | "0" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `env_version` | "" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `timestamp` | "0" | 条件回退字段：仅 event_date_creation 缺失或无效时用于 occur_time；本样例未采用 |
| `type` | "account_changes" | 仅用于 WPL 路由，稳定日志类型已由 log_type 表达；原值保留在 raw_msg |
| `logger` | "" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `client_report_ip` | "" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `report_ip` | "" | 疑似 Agent 上报链路地址；与终端 IP 不一致时不作为事件 source IP，原值保留在 raw_msg |
| `client_ip` | "" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `ip` | "" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `create_time` | "1629440445569" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `custom_group_paths` | "" | 分组路径原始串不进入事件对象；原值保留在 raw_msg |
| `gid` | "" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `group_name` | "" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `hostname` | "A0XXXXX-NC02" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `pid` | "0" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |

## 三、排除字段（重复或空载荷）

| WPL 字段 | 说明 |
|---|---|
| `payload` | 完整原文已由 raw_msg 保存，不重复写入 VARIANT |

## 四、平台默认、派生及结构字段

| 来源 | SDM 落位 | expected 值 | 赋值责任与说明 |
|---|---|---|---|
| `platform_context.tenant_id` | `tenant_id` | "" | 由平台上下文提供 |
| `derived.sha256('|'+mapping_id+'|'+source_original_event_id)` | `event_id` | "evt-741756944a090df6dd4d2de97ae51b9a045e0146bb01391468908926ff92bf6b" | 按确定性规则 sha256('|'+mapping_id+'|'+source_original_event_id) 派生 |
| `platform_context.log_id` | `log_id` | "log-tianqing-account-change-0001" | 由平台上下文提供 |
| `raw_log_input` | `raw_msg` | "{\"task_id\":0,\"sub_task_id\":0,\"env_version\":\"\",\"process_parent_command_line\":\"wininit.exe\",\"process_parent_internal_name\":\"WinInit\",\"process_parent_name\":\"wininit.exe\",\"process_parent_original_name\":\"WinInit.exe\",\"process_parent_sign\":\"Microsoft Windows Publisher\",\"process_sha1\":\"20a244c0440ed0b418f454f8a12ed0de6a8bd6d2\",\"timestamp\":0,\"type\":\"account_changes\",\"uuid\":\"16EEBAD5-E974-405F-9603-973D8FA464C9\",\"logger\":\"\",\"process_original_name\":\"lsass.exe\",\"process_parent_path\":\"C:\\\\WINDOWS\\\\System32\\\\wininit.exe\",\"process_sign\":\"Microsoft Windows Publisher\",\"process_user\":\"NT AUTHORITY\\\\SYSTEM\",\"client_report_ip\":\"\",\"report_ip\":\"\",\"account_name\":\"XXXXXX\",\"account_user\":\"XXXXXX\",\"asset_id\":\"100231\",\"asset_oid\":\"2653788242175861718\",\"client_id\":\"4709450-42a2c1474b27be3f445f30952XXXXXX\",\"client_ip\":\"\",\"ip\":\"\",\"computer_name\":\"A0XXXXX-NC02\",\"create_time\":1629440445569977300,\"custom_group_paths\":\"\",\"event_date_creation\":1629440451126,\"event_type\":\"userinfo_changed\",\"gid\":\"\",\"group_name\":\"\",\"hostname\":\"A0XXXXX-NC02\",\"mac\":\"XX-XX-XX-XX-XX-XX\",\"mid\":\"d4bb9bc2621630fdc27154105d9da5630940658a996fcfe8824965d3d8XXXXXX\",\"payload\":\"\",\"pid\":0,\"process_command_line\":\"C:\\\\WINDOWS\\\\system32\\\\lsass.exe\",\"process_guid\":\"f4cdcc09ee421ef79d1136ebdbdda395\",\"process_id\":\"824\",\"process_internal_name\":\"lsass.exe\",\"process_md5\":\"5ae8589cdde46ed132aef8280bc8894a\",\"process_name\":\"lsass.exe\",\"process_path\":\"C:\\\\Windows\\\\System32\\\\lsass.exe\"}" | 由原始日志接入层保存，不由 OML 拼装 |
| `platform_context.ingest_time` | `ingest_time` | 1629440452001 | 由平台上下文提供 |
| `platform_context.parse_time` | `parse_time` | 1629440452120 | 由平台上下文提供 |
| `constant.sdm_schema_version` | `schema_version` | 2 | 使用平台/映射规则常量 sdm_schema_version |
| `constant.mapping_id` | `mapping_id` | "qax.tianqing.edr_account_change" | 使用平台/映射规则常量 mapping_id |
| `constant.mapping_vendor` | `data_src_vendor` | "qax" | 使用平台/映射规则常量 mapping_vendor |
| `constant.mapping_product` | `data_src_product` | "tianqing" | 使用平台/映射规则常量 mapping_product |
| `constant.mapping_category` | `data_src_category` | "endpoint_security" | 使用平台/映射规则常量 mapping_category |
| `platform_context.data_src_instance_id` | `data_src_instance_id` | "collector-tianqing-poc-01" | 由平台上下文提供 |
| `constant.log_type` | `log_type` | "edr_account_change" | 使用平台/映射规则常量 log_type |
| `constant.log_name` | `log_name` | "天擎 EDR 账号变更" | 使用平台/映射规则常量 log_name |
| `constant.record_kind` | `record_kind` | "activity" | 使用平台/映射规则常量 record_kind |
| `constant.event_domain` | `event_domain` | "auth" | 使用平台/映射规则常量 event_domain |
| `derived.enum_projection` | `outcome` | "observed" | 由 WPL 枚举或日志语义转换为 SDM 标准值 |
| `constant.default_severity` | `severity` | "info" | 当前日志类型未提供标准 severity，按映射默认值 info 装配 |
| `wpl.process_user` | `source_user` | "NT AUTHORITY\\SYSTEM" | 由 WPL 字段 process_user 投影或转换后赋值 |
| `wpl.computer_name` | `source_host` | "A0XXXXX-NC02" | 由 WPL 字段 computer_name 投影或转换后赋值 |
| `constant.mapping_vendor` | `observer_vendor` | "qax" | 使用平台/映射规则常量 mapping_vendor |
| `constant.mapping_product` | `observer_product` | "tianqing" | 使用平台/映射规则常量 mapping_product |
| `derived.entity_ref` | `roles.source.ref_id` | "host_100231" | 按确定性规则 entity_ref 派生 |
| `constant.entity_type` | `roles.source.entity_type` | "host" | 使用平台/映射规则常量 entity_type |
| `derived.entity_ref` | `roles.target.ref_id` | "account_XXXXXX" | 按确定性规则 entity_ref 派生 |
| `constant.entity_type` | `roles.target.entity_type` | "account" | 使用平台/映射规则常量 entity_type |
| `constant.mapping_product` | `roles.observer.product.name` | "tianqing" | 使用平台/映射规则常量 mapping_product |
| `constant.mapping_vendor` | `roles.observer.device.vendor` | "qax" | 使用平台/映射规则常量 mapping_vendor |
| `derived.entity_ref` | `roles.related[0].ref_id` | "process_wininit_fallback" | 按确定性规则 entity_ref 派生 |
| `constant.entity_type` | `roles.related[0].entity_type` | "process" | 使用平台/映射规则常量 entity_type |
| `constant.relation_type` | `roles.related[0].relation_type` | "parent_process" | 使用平台/映射规则常量 relation_type |
| `constant.sdm_schema_version` | `extensions.schema_version` | 2 | 使用平台/映射规则常量 sdm_schema_version |
| `derived.entity_ref` | `extensions.profiles.endpoint_asset.subject_ref.ref_id` | "host_100231" | 按确定性规则 entity_ref 派生 |
| `platform_context.env_version` | `extensions.profiles.endpoint_asset.agent.version` | "edr-8.0" | 由平台上下文提供 |
| `data_gap.wpl_field_missing` | `extensions.unmapped.account_action` | "WPL 仅输出 userinfo_changed，未提供可确认的 create/disable/password_change 等动作枚举" | WPL 未抽取该字段；此处仅记录数据缺口，不应伪造业务值 |

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
| `mapping_id` | `constant` | `constant.mapping_id` | "qax.tianqing.edr_account_change" | `—` | confirmed；使用平台/映射规则常量 mapping_id |
| `data_src_vendor` | `constant` | `constant.mapping_vendor` | "qax" | `—` | confirmed；使用平台/映射规则常量 mapping_vendor |
| `data_src_product` | `constant` | `constant.mapping_product` | "tianqing" | `—` | confirmed；使用平台/映射规则常量 mapping_product |
| `data_src_category` | `constant` | `constant.mapping_category` | "endpoint_security" | `—` | confirmed；使用平台/映射规则常量 mapping_category |
| `data_src_instance_id` | `context` | `platform_context.data_src_instance_id` | `platform_context.data_src_instance_id` | `—` | confirmed；由平台上下文提供 |
| `log_type` | `constant` | `constant.log_type` | "edr_account_change" | `—` | confirmed；使用平台/映射规则常量 log_type |
| `log_name` | `constant` | `constant.log_name` | "天擎 EDR 账号变更" | `—` | confirmed；使用平台/映射规则常量 log_name |
| `record_kind` | `constant` | `constant.record_kind` | "activity" | `—` | confirmed；使用平台/映射规则常量 record_kind |
| `event_domain` | `constant` | `constant.event_domain` | "auth" | `—` | confirmed；使用平台/映射规则常量 event_domain |
| `severity` | `constant` | `constant.default_severity` | "info" | `—` | confirmed；当前日志类型未提供标准 severity，按映射默认值 info 装配 |
| `observer_vendor` | `constant` | `constant.mapping_vendor` | "qax" | `—` | confirmed；使用平台/映射规则常量 mapping_vendor |
| `observer_product` | `constant` | `constant.mapping_product` | "tianqing" | `—` | confirmed；使用平台/映射规则常量 mapping_product |
| `roles.source.ref_id` | `derived` | `derived.entity_ref` | `derived.entity_ref` | `—` | confirmed；按确定性规则 entity_ref 派生 |
| `roles.source.entity_type` | `constant` | `constant.entity_type` | "host" | `—` | confirmed；使用平台/映射规则常量 entity_type |
| `roles.target.ref_id` | `derived` | `derived.entity_ref` | `derived.entity_ref` | `—` | confirmed；按确定性规则 entity_ref 派生 |
| `roles.target.entity_type` | `constant` | `constant.entity_type` | "account" | `—` | confirmed；使用平台/映射规则常量 entity_type |
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
| `extensions.unmapped.account_action` | `gap` | `data_gap.wpl_field_missing` | `data_gap.wpl_field_missing` | `—` | missing；WPL 未抽取该字段；此处仅记录数据缺口，不应伪造业务值 |
| `roles.related[0].process.cmdline` | `projection` | `process_parent_command_line` | "wininit.exe" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.related[0].process.file.internal_name` | `projection` | `process_parent_internal_name` | "WinInit" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.related[0].process.name` | `projection` | `process_parent_name` | "wininit.exe" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.related[0].process.file.original_name` | `projection` | `process_parent_original_name` | "WinInit.exe" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.related[0].process.file.signatures[0].signer` | `projection` | `process_parent_sign` | "Microsoft Windows Publisher" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.source.process.file.hashes.sha1` | `projection` | `process_sha1` | "20a244c0440ed0b418f454f8a12ed0de6a8bd6d2" | `—` | confirmed；按当前 expected 事件结构映射 |
| `source_original_event_id` | `projection` | `uuid` | "16EEBAD5-E974-405F-9603-973D8FA464C9" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.source.process.file.original_name` | `projection` | `process_original_name` | "lsass.exe" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.related[0].process.path` | `projection` | `process_parent_path` | "C:\\Windows\\System32\\wininit.exe" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.source.process.file.signatures[0].signer` | `projection` | `process_sign` | "Microsoft Windows Publisher" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.source.process.user.name` | `projection` | `process_user` | "NT AUTHORITY\\SYSTEM" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.target.account.name` | `projection` | `account_name` | "XXXXXX" | `—` | confirmed；目标账户名称；样例值已脱敏为 XXXXXX |
| `target_user` | `projection` | `account_user` | "XXXXXX" | `—` | confirmed；投影为 target_user；样例值已脱敏，未据此推断账户类型 |
| `roles.source.host.id` | `projection` | `asset_id` | "100231" | `—` | confirmed；按当前 expected 事件结构映射 |
| `extensions.profiles.endpoint_asset.ownership.organization.id` | `projection` | `asset_oid` | "2653788242175861718" | `—` | confirmed；按当前 expected 事件结构映射 |
| `extensions.profiles.endpoint_asset.agent.id` | `projection` | `client_id` | "4709450-42a2c1474b27be3f445f30952XXXXXX" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.source.host.name` | `projection` | `computer_name` | "A0XXXXX-NC02" | `—` | confirmed；按当前 expected 事件结构映射 |
| `occur_time` | `projection` | `event_date_creation` | 1629440451126 | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.source.host.mac` | `projection` | `mac` | "XX:XX:XX:XX:XX:XX" | `—` | confirmed；按当前 expected 事件结构映射 |
| `extensions.profiles.endpoint_asset.agent.fingerprint_id` | `projection` | `mid` | "d4bb9bc2621630fdc27154105d9da5630940658a996fcfe8824965d3d8XXXXXX" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.source.process.cmdline` | `projection` | `process_command_line` | "C:\\WINDOWS\\system32\\lsass.exe" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.source.process.uid` | `projection` | `process_guid` | "f4cdcc09ee421ef79d1136ebdbdda395" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.source.process.pid` | `projection` | `process_id` | "824" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.source.process.file.internal_name` | `projection` | `process_internal_name` | "lsass.exe" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.source.process.file.hashes.md5` | `projection` | `process_md5` | "5ae8589cdde46ed132aef8280bc8894a" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.source.process.name` | `projection` | `process_name` | "lsass.exe" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.source.process.path` | `projection` | `process_path` | "C:\\Windows\\System32\\lsass.exe" | `—` | confirmed；按当前 expected 事件结构映射 |
| `event_type` | `dictionary` | `event_type` | "userinfo_changed" -> "user_uncategorized" | `preserve_in_extension_and_review` | partial；标准无 account_change |

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
