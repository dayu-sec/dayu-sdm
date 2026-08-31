# WPL → SDM Event 字段映射

> 样例：`account_password_change.expected-sdm-event.json`；WPL 字段 32 个，映射 21，不落库 11，排除 0；另有平台默认、派生及结构字段 39 项。
> SDM 落位为逻辑路径；expected 位置为该样例中的实际物理 JSON 路径。

## 一、映射字段

| WPL 字段 | WPL 值 | SDM 落位 | expected 位置 | expected 值 | 说明 |
|---|---|---|---|---|---|
| `alert_id` | 2880734758592098843 | `source_original_event_id` | `source_original_event_id` | "2880734758592098843" | 按当前 expected 事件结构映射 |
| `asset_id` | 2838024086184002130 | `roles.target.host.id` | `roles_obj.target.host.id` | "2838024086184002130" | 按当前 expected 事件结构映射 |
| `asset_oid` | 2715651939760080161 | `extensions.profiles.endpoint_asset.ownership.organization.id` | `extensions_obj.profiles.endpoint_asset.ownership.organization.id` | "2715651939760080161" | 按当前 expected 事件结构映射 |
| `category_id` | 2 | `source_finding.category.original.code` | `source_finding_obj.category.original.code` | "2" | 按当前 expected 事件结构映射 |
| `client_id` | "7036994-ffdc79ca939f96375c1605a3ba6d71ef" | `extensions.profiles.endpoint_asset.agent.id` | `extensions_obj.profiles.endpoint_asset.agent.id` | "7036994-ffdc79ca939f96375c1605a3ba6d71ef" | 按当前 expected 事件结构映射 |
| `computer_name` | "EDRAUTOTEST-1717" | `roles.target.host.name` | `roles_obj.target.host.name` | "EDRAUTOTEST-1717" | 按当前 expected 事件结构映射 |
| `create_time` | 1717051732000 | `occur_time` | `occur_time` | 1717051732000 | 按当前 expected 事件结构映射 |
| `gid` | "4fdcff0b7800b21b" | `extensions.profiles.endpoint_asset.ownership.group.id` | `extensions_obj.profiles.endpoint_asset.ownership.group.id` | "4fdcff0b7800b21b" | 按当前 expected 事件结构映射 |
| `group_name` | "未分组终端" | `extensions.profiles.endpoint_asset.ownership.group.name` | `extensions_obj.profiles.endpoint_asset.ownership.group.name` | "未分组终端" | 按当前 expected 事件结构映射 |
| `ip` | "198.51.100.114" | `roles.target.host.ip` | `roles_obj.target.host.ip` | "198.51.100.114" | 按当前 expected 事件结构映射 |
| `mac` | "e8-6a-64-e0-05-6d" | `roles.target.host.mac` | `roles_obj.target.host.mac` | "e8:6a:64:e0:05:6d" | 按当前 expected 事件结构映射 |
| `mid` | "81a15464af48af9f7fc8652fd820f9a75724c678e2920d7d5e7317fc57a2e900" | `extensions.profiles.endpoint_asset.agent.fingerprint_id` | `extensions_obj.profiles.endpoint_asset.agent.fingerprint_id` | "81a15464af48af9f7fc8652fd820f9a75724c678e2920d7d5e7317fc57a2e900" | 按当前 expected 事件结构映射 |
| `rule_id` | "1.10.0003" | `source_finding.rule.signature_id` | `source_finding_obj.rule.signature_id` | "1.10.0003" | 按当前 expected 事件结构映射 |
| `severity` | 2 | `source_finding.severity` | `source_finding_obj.severity` | "2" | 按当前 expected 事件结构映射 |
| `status` | 0 | `source_finding.status` | `source_finding_obj.status` | "0" | 按当前 expected 事件结构映射 |
| `tactic` | "Persistence" | `source_finding.mitre.tactics[0]` | `source_finding_obj.mitre.tactics[0]` | "Persistence" | 按当前 expected 事件结构映射 |
| `technique` | "Account Manipulation" | `source_finding.mitre.techniques[0]` | `source_finding_obj.mitre.techniques[0]` | "Account Manipulation" | 按当前 expected 事件结构映射 |
| `technique_id` | "T1098" | `source_finding.mitre.technique_id` | `source_finding_obj.mitre.technique_id` | "T1098" | 按当前 expected 事件结构映射 |
| `alert_name` | "发现账户\"NetUser\"修改密码" | `source_finding.title` | `source_finding_obj.title` | "发现账户\"NetUser\"修改密码" | 按当前 expected 事件结构映射 |
| `description_i18n/zh_CN` | "发现用户\"DESKTOP-AACOVHR$\"修改了用户\"NetUser\"的密码." | `source_finding.description` | `source_finding_obj.description` | "发现用户\"DESKTOP-AACOVHR$\"修改了用户\"NetUser\"的密码." | 按当前 expected 事件结构映射 |
| `process_details` | [{"process_name": "explorer.exe", "process_id": "5526", "process_md5": "7a413ddd10e81adb6bb5d5e38f399d08", "process_path": "C:\\Windows\\explorer.exe", "process_sign": "Microsoft Windows", "process_command_line": "C:\\Windows\\Explorer.EXE", "process_create_time": 1717051719680, "process_terminate_time": 0, "process_guid": "4012f6f0f7cf4afe8838042a18080dec", "process_parent_guid": "e583b89c51e9246dbecd2abb7a784cc0", "child_process_details": [{"process_name": "cmd.exe", "process_id": "6585", "process_md5": "8a2122e8162dbef04694b9c3e0b6cdee", "process_path": "C:\\Windows\\system32\\cmd.exe", "process_sign": "Microsoft Windows", "process_command_line": "C:\\Windows\\system32\\cmd.exe", "process_create_time": 1717051719680, "process_terminate_time": 0, "process_guid": "c84108f5d67bbd5e0aa17618d3b593d3", "process_parent_guid": "4012f6f0f7cf4afe8838042a18080dec", "child_process_details": [{"process_name": "curl.exe", "process_id": "5041", "process_md5": "eac53ddafb5cc9e780a7cc086ce7b2b1", "process_path": "C:\\Windows\\System32\\curl.exe", "process_sign": "HaoShuQing", "process_command_line": "C:\\Windows\\System32\\curl.exe", "process_create_time": 1717051719680, "process_terminate_time": 0, "process_guid": "63fe679e70ab3c96e517da0be9f271d3", "process_parent_guid": "c84108f5d67bbd5e0aa17618d3b593d3", "is_alert_trigger": true}]}]}] | `roles.related[0].process` | `roles_obj.related[0].process` | {"name": "curl.exe", "uid": "63fe679e70ab3c96e517da0be9f271d3", "pid": "5041", "path": "C:\\Windows\\System32\\curl.exe", "cmdline": "C:\\Windows\\System32\\curl.exe", "file": {"hashes": {"md5": "eac53ddafb5cc9e780a7cc086ce7b2b1"}, "signatures": [{"signer": "HaoShuQing"}]}} | 告警触发进程对象；构造 related[0]，relation_type=alert_trigger_process，0 时间哨兵省略 |

## 二、不落库字段

| WPL 字段 | WPL 值 | 原因 |
|---|---|---|
| `client_login_user` | "" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `custom_group_paths` | ",2877377393142575643,4fdcff0b7800b21b" | 分组路径原始串不进入事件对象；原值保留在 raw_msg |
| `description` | "发现用户\"DESKTOP-AACOVHR$\"修改了用户\"NetUser\"的密码." | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `report_ip` | "198.51.100.114" | 疑似 Agent 上报链路地址；与终端 IP 不一致时不作为事件 source IP，原值保留在 raw_msg |
| `tactic_id` | "TA0003" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `type` | "edr_alert" | 仅用于 WPL 路由，稳定日志类型已由 log_type 表达；原值保留在 raw_msg |
| `alert_name/en_US` | "Found that account \"NetUser\" changed password" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `alert_name/zh_CN` | "发现账户\"NetUser\"修改密码" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `alert_name/zh_TW` | "發現帳戶\"NetUser\"修改密碼" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `description_i18n/zh_TW` | "發現使用者\"DESKTOP-AACOVHR$\"修改了使用者\"NetUser\"的密碼." | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `description_i18n/en_US` | "It was found that user \"DESKTOP-AACOVHR$\" changed the password of user \"NetUser\"." | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |

## 四、平台默认、派生及结构字段

| 来源 | SDM 落位 | expected 值 | 赋值责任与说明 |
|---|---|---|---|
| `platform_context.tenant_id` | `tenant_id` | "" | 由平台上下文提供 |
| `derived.sha256('|'+mapping_id+'|'+source_original_event_id)` | `event_id` | "evt-9e32ff9531f75c1d1915c422405b7dbcda937f2b4ab3498f0e44c63cdc8f71fd" | 按固定格式 sha256('|'+mapping_id+'|'+source_original_event_id) 生成；本样例 source_original_event_id 来自 WPL alert_id，tenant_id 为空不参与该公式 |
| `platform_context.log_id` | `log_id` | "log-tianqing-edr-alert-account_password_change" | 由平台上下文提供 |
| `raw_log_input` | `raw_msg` | "{\"type\":\"edr_alert\",\"alert_id\":2880734758592098843,\"alert_name\":{\"en_US\":\"Found that account \\\"NetUser\\\" changed password\",\"zh_CN\":\"发现账户\\\"NetUser\\\"修改密码\",\"zh_TW\":\"發現帳戶\\\"NetUser\\\"修改密碼\"},\"gid\":\"4fdcff0b7800b21b\",\"group_name\":\"未分组终端\",\"mid\":\"81a15464af48af9f7fc8652fd820f9a75724c678e2920d7d5e7317fc57a2e900\",\"mac\":\"e8-6a-64-e0-05-6d\",\"computer_name\":\"EDRAUTOTEST-1717\",\"custom_group_paths\":\",2877377393142575643,4fdcff0b7800b21b\",\"report_ip\":\"198.51.100.114\",\"ip\":\"198.51.100.114\",\"client_id\":\"7036994-ffdc79ca939f96375c1605a3ba6d71ef\",\"asset_oid\":2715651939760080161,\"asset_id\":2838024086184002130,\"client_login_user\":\"\",\"severity\":2,\"category_id\":2,\"technique_id\":\"T1098\",\"tactic_id\":\"TA0003\",\"description\":\"发现用户\\\"DESKTOP-AACOVHR$\\\"修改了用户\\\"NetUser\\\"的密码.\",\"description_i18n\":{\"zh_CN\":\"发现用户\\\"DESKTOP-AACOVHR$\\\"修改了用户\\\"NetUser\\\"的密码.\",\"zh_TW\":\"發現使用者\\\"DESKTOP-AACOVHR$\\\"修改了使用者\\\"NetUser\\\"的密碼.\",\"en_US\":\"It was found that user \\\"DESKTOP-AACOVHR$\\\" changed the password of user \\\"NetUser\\\".\"},\"technique\":\"Account Manipulation\",\"tactic\":\"Persistence\",\"create_time\":1717051732000,\"status\":0,\"rule_id\":\"1.10.0003\",\"process_details\":[{\"process_name\":\"explorer.exe\",\"process_id\":\"5526\",\"process_md5\":\"7a413ddd10e81adb6bb5d5e38f399d08\",\"process_path\":\"C:\\\\Windows\\\\explorer.exe\",\"process_sign\":\"Microsoft Windows\",\"process_command_line\":\"C:\\\\Windows\\\\Explorer.EXE\",\"process_create_time\":1717051719680,\"process_terminate_time\":0,\"process_guid\":\"4012f6f0f7cf4afe8838042a18080dec\",\"process_parent_guid\":\"e583b89c51e9246dbecd2abb7a784cc0\",\"child_process_details\":[{\"process_name\":\"cmd.exe\",\"process_id\":\"6585\",\"process_md5\":\"8a2122e8162dbef04694b9c3e0b6cdee\",\"process_path\":\"C:\\\\Windows\\\\system32\\\\cmd.exe\",\"process_sign\":\"Microsoft Windows\",\"process_command_line\":\"C:\\\\Windows\\\\system32\\\\cmd.exe\",\"process_create_time\":1717051719680,\"process_terminate_time\":0,\"process_guid\":\"c84108f5d67bbd5e0aa17618d3b593d3\",\"process_parent_guid\":\"4012f6f0f7cf4afe8838042a18080dec\",\"child_process_details\":[{\"process_name\":\"curl.exe\",\"process_id\":\"5041\",\"process_md5\":\"eac53ddafb5cc9e780a7cc086ce7b2b1\",\"process_path\":\"C:\\\\Windows\\\\System32\\\\curl.exe\",\"process_sign\":\"HaoShuQing\",\"process_command_line\":\"C:\\\\Windows\\\\System32\\\\curl.exe\",\"process_create_time\":1717051719680,\"process_terminate_time\":0,\"process_guid\":\"63fe679e70ab3c96e517da0be9f271d3\",\"process_parent_guid\":\"c84108f5d67bbd5e0aa17618d3b593d3\",\"is_alert_trigger\":true}]}]}],\"ioc_alerts\":[],\"risky_source\":{}}" | 由原始日志接入层保存，不由 OML 拼装 |
| `platform_context.ingest_time` | `ingest_time` | 1717051733001 | 由平台上下文提供 |
| `platform_context.parse_time` | `parse_time` | 1717051733120 | 由平台上下文提供 |
| `constant.sdm_schema_version` | `schema_version` | 2 | 使用平台/映射规则常量 sdm_schema_version |
| `constant.qax.tianqing.edr_alert_log` | `mapping_id` | "qax.tianqing.edr_alert_log" | 使用平台/映射规则常量 qax.tianqing.edr_alert_log |
| `constant.qax` | `data_src_vendor` | "qax" | 使用平台/映射规则常量 qax |
| `constant.tianqing` | `data_src_product` | "tianqing" | 使用平台/映射规则常量 tianqing |
| `constant.endpoint_security` | `data_src_category` | "endpoint_security" | 使用平台/映射规则常量 endpoint_security |
| `platform_context.data_src_instance_id` | `data_src_instance_id` | "collector-tianqing-poc-01" | 由平台上下文提供 |
| `constant.edr_alert_log` | `log_type` | "edr_alert_log" | 使用平台/映射规则常量 edr_alert_log |
| `constant.天擎终端威胁告警日志` | `log_name` | "天擎终端威胁告警日志" | 使用平台/映射规则常量 天擎终端威胁告警日志 |
| `constant.finding` | `record_kind` | "finding" | 使用平台/映射规则常量 finding |
| `constant.threat` | `event_domain` | "threat" | 使用平台/映射规则常量 threat |
| `constant.generic_event` | `event_type` | "generic_event" | 使用平台/映射规则常量 generic_event |
| `derived.enum_projection` | `outcome` | "observed" | 由 WPL 枚举或日志语义转换为 SDM 标准值 |
| `constant.default_severity` | `severity` | "info" | 当前日志类型未提供标准 severity，按映射默认值 info 装配 |
| `wpl.computer_name` | `source_host` | "EDRAUTOTEST-1717" | 由 WPL 字段 computer_name 投影或转换后赋值 |
| `wpl.computer_name` | `target_host` | "EDRAUTOTEST-1717" | 由 WPL 字段 computer_name 投影或转换后赋值 |
| `constant.qax` | `observer_vendor` | "qax" | 使用平台/映射规则常量 qax |
| `constant.tianqing` | `observer_product` | "tianqing" | 使用平台/映射规则常量 tianqing |
| `wpl.alert_id` | `source_finding_original_id` | "2880734758592098843" | 由 WPL 字段 alert_id 投影或转换后赋值 |
| `wpl.alert_name` | `source_finding_title` | "发现账户\"NetUser\"修改密码" | 由 WPL 字段 alert_name 投影或转换后赋值 |
| `wpl.severity` | `source_finding_severity` | "2" | 由 WPL 字段 severity 投影或转换后赋值 |
| `wpl.category_id` | `source_finding_category` | "2" | 由 WPL 字段 category_id 投影或转换后赋值 |
| `wpl.rule_id` | `source_finding_signature_id` | "1.10.0003" | 由 WPL 字段 rule_id 投影或转换后赋值 |
| `derived.entity_ref(host, wpl.asset_id)` | `roles.target.ref_id` | "host::2838024086184002130" | 按确定性规则 entity_ref(host, wpl.asset_id) 派生 |
| `constant.host` | `roles.target.entity_type` | "host" | 使用平台/映射规则常量 host |
| `constant.tianqing` | `roles.observer.product.name` | "tianqing" | 使用平台/映射规则常量 tianqing |
| `constant.qax` | `roles.observer.device.vendor` | "qax" | 使用平台/映射规则常量 qax |
| `derived.entity_ref(process, wpl.process_details[0].process_guid)` | `roles.related[0].ref_id` | "process::63fe679e70ab3c96e517da0be9f271d3" | 按确定性规则 entity_ref(process, wpl.process_details[0].process_guid) 派生 |
| `constant.process` | `roles.related[0].entity_type` | "process" | 使用平台/映射规则常量 process |
| `constant.alert_trigger_process` | `roles.related[0].relation_type` | "alert_trigger_process" | 使用平台/映射规则常量 alert_trigger_process |
| `wpl.alert_id` | `source_finding.original_id` | "2880734758592098843" | 由 WPL 字段 alert_id 投影或转换后赋值 |
| `assembly.one_finding_per_wpl_alert` | `source_finding.count` | 1 | 当前一条 WPL 告警装配一个 finding，因此固定为 1 |
| `constant.sdm_schema_version` | `extensions.schema_version` | 2 | 使用平台/映射规则常量 sdm_schema_version |
| `derived.entity_ref(host, wpl.asset_id)` | `extensions.profiles.endpoint_asset.subject_ref.ref_id` | "host::2838024086184002130" | 按确定性规则 entity_ref(host, wpl.asset_id) 派生 |

## 五、WPL/OML 编写规则

> WPL 只负责提取表中的 source 字段；Meta 和 Content 的赋值由 OML 按下表实现。
> `partial` 表示当前只有样例值或局部说明，不能视为完整厂商字典。

### 5.1 Meta 区

| SDM 字段 | 规则类型 | 输入/来源 | 赋值 | 未命中 | 状态与证据 |
|---|---|---|---|---|---|
| `tenant_id` | `context` | `platform_context.tenant_id` | `platform_context.tenant_id` | `—` | confirmed；由平台上下文提供 |
| `event_id` | `derived` | `derived.sha256('|'+mapping_id+'|'+source_original_event_id)` | `derived.sha256('|'+mapping_id+'|'+source_original_event_id)` | `—` | confirmed；按固定格式 sha256('|'+mapping_id+'|'+source_original_event_id) 生成；本样例 source_original_event_id 来自 WPL alert_id，tenant_id 为空不参与该公式 |
| `log_id` | `context` | `platform_context.log_id` | `platform_context.log_id` | `—` | confirmed；由平台上下文提供 |
| `schema_version` | `constant` | `constant.sdm_schema_version` | 2 | `—` | confirmed；使用平台/映射规则常量 sdm_schema_version |
| `mapping_id` | `constant` | `constant.qax.tianqing.edr_alert_log` | "qax.tianqing.edr_alert_log" | `—` | confirmed；使用平台/映射规则常量 qax.tianqing.edr_alert_log |
| `data_src_vendor` | `constant` | `constant.qax` | "qax" | `—` | confirmed；使用平台/映射规则常量 qax |
| `data_src_product` | `constant` | `constant.tianqing` | "tianqing" | `—` | confirmed；使用平台/映射规则常量 tianqing |
| `data_src_category` | `constant` | `constant.endpoint_security` | "endpoint_security" | `—` | confirmed；使用平台/映射规则常量 endpoint_security |
| `data_src_instance_id` | `context` | `platform_context.data_src_instance_id` | `platform_context.data_src_instance_id` | `—` | confirmed；由平台上下文提供 |
| `log_type` | `constant` | `constant.edr_alert_log` | "edr_alert_log" | `—` | confirmed；使用平台/映射规则常量 edr_alert_log |
| `log_name` | `constant` | `constant.天擎终端威胁告警日志` | "天擎终端威胁告警日志" | `—` | confirmed；使用平台/映射规则常量 天擎终端威胁告警日志 |
| `record_kind` | `constant` | `constant.finding` | "finding" | `—` | confirmed；使用平台/映射规则常量 finding |
| `event_domain` | `constant` | `constant.threat` | "threat" | `—` | confirmed；使用平台/映射规则常量 threat |
| `event_type` | `constant` | `constant.generic_event` | "generic_event" | `—` | confirmed；使用平台/映射规则常量 generic_event |
| `severity` | `constant` | `constant.default_severity` | "info" | `—` | confirmed；当前日志类型未提供标准 severity，按映射默认值 info 装配 |
| `observer_vendor` | `constant` | `constant.qax` | "qax" | `—` | confirmed；使用平台/映射规则常量 qax |
| `observer_product` | `constant` | `constant.tianqing` | "tianqing" | `—` | confirmed；使用平台/映射规则常量 tianqing |
| `roles.target.ref_id` | `derived` | `derived.entity_ref(host, wpl.asset_id)` | `derived.entity_ref(host, wpl.asset_id)` | `—` | confirmed；按确定性规则 entity_ref(host, wpl.asset_id) 派生 |
| `roles.target.entity_type` | `constant` | `constant.host` | "host" | `—` | confirmed；使用平台/映射规则常量 host |
| `roles.observer.product.name` | `constant` | `constant.tianqing` | "tianqing" | `—` | confirmed；使用平台/映射规则常量 tianqing |
| `roles.observer.device.vendor` | `constant` | `constant.qax` | "qax" | `—` | confirmed；使用平台/映射规则常量 qax |
| `roles.related[0].ref_id` | `derived` | `derived.entity_ref(process, wpl.process_details[0].process_guid)` | `derived.entity_ref(process, wpl.process_details[0].process_guid)` | `—` | confirmed；按确定性规则 entity_ref(process, wpl.process_details[0].process_guid) 派生 |
| `roles.related[0].entity_type` | `constant` | `constant.process` | "process" | `—` | confirmed；使用平台/映射规则常量 process |
| `roles.related[0].relation_type` | `constant` | `constant.alert_trigger_process` | "alert_trigger_process" | `—` | confirmed；使用平台/映射规则常量 alert_trigger_process |
| `source_finding.count` | `derived` | `assembly.one_finding_per_wpl_alert` | `assembly.one_finding_per_wpl_alert` | `—` | confirmed；当前一条 WPL 告警装配一个 finding，因此固定为 1 |
| `extensions.profiles.endpoint_asset.subject_ref.ref_id` | `derived` | `derived.entity_ref(host, wpl.asset_id)` | `derived.entity_ref(host, wpl.asset_id)` | `—` | confirmed；按确定性规则 entity_ref(host, wpl.asset_id) 派生 |
| `outcome` | `constant` | `log_semantics` | "observed" | `—` | confirmed；由该日志类型的事件事实确定，不是来源枚举转换 |
| `ingest_time` | `context` | `platform_context.ingest_time` | `read(ingest_time)` | `—` | confirmed；expected 事件中的平台上下文字段 |
| `parse_time` | `context` | `platform_context.parse_time` | `read(parse_time)` | `—` | confirmed；expected 事件中的平台上下文字段 |

### 5.2 Content 区

| SDM 字段 | 规则类型 | WPL 字段 | 映射/赋值 | 未命中 | 状态与证据 |
|---|---|---|---|---|---|
| `outcome` | `dictionary` | `derived.enum_projection` | — | `preserve_in_extension_and_review` | partial；由 WPL 枚举或日志语义转换为 SDM 标准值 |
| `source_host` | `projection` | `computer_name` | `wpl.computer_name` | `—` | confirmed；由 WPL 字段 computer_name 投影或转换后赋值 |
| `target_host` | `projection` | `computer_name` | `wpl.computer_name` | `—` | confirmed；由 WPL 字段 computer_name 投影或转换后赋值 |
| `source_finding_original_id` | `projection` | `alert_id` | `wpl.alert_id` | `—` | confirmed；由 WPL 字段 alert_id 投影或转换后赋值 |
| `source_finding_title` | `projection` | `alert_name` | `wpl.alert_name` | `—` | confirmed；由 WPL 字段 alert_name 投影或转换后赋值 |
| `source_finding_severity` | `projection` | `severity` | `wpl.severity` | `—` | confirmed；由 WPL 字段 severity 投影或转换后赋值 |
| `source_finding_category` | `projection` | `category_id` | `wpl.category_id` | `—` | confirmed；由 WPL 字段 category_id 投影或转换后赋值 |
| `source_finding_signature_id` | `projection` | `rule_id` | `wpl.rule_id` | `—` | confirmed；由 WPL 字段 rule_id 投影或转换后赋值 |
| `source_finding.original_id` | `projection` | `alert_id` | `wpl.alert_id` | `—` | confirmed；由 WPL 字段 alert_id 投影或转换后赋值 |
| `source_original_event_id` | `projection` | `alert_id` | "2880734758592098843" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.target.host.id` | `projection` | `asset_id` | "2838024086184002130" | `—` | confirmed；按当前 expected 事件结构映射 |
| `extensions.profiles.endpoint_asset.ownership.organization.id` | `projection` | `asset_oid` | "2715651939760080161" | `—` | confirmed；按当前 expected 事件结构映射 |
| `source_finding.category.original.code` | `projection` | `category_id` | "2" | `—` | confirmed；按当前 expected 事件结构映射 |
| `extensions.profiles.endpoint_asset.agent.id` | `projection` | `client_id` | "7036994-ffdc79ca939f96375c1605a3ba6d71ef" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.target.host.name` | `projection` | `computer_name` | "EDRAUTOTEST-1717" | `—` | confirmed；按当前 expected 事件结构映射 |
| `occur_time` | `projection` | `create_time` | 1717051732000 | `—` | confirmed；按当前 expected 事件结构映射 |
| `extensions.profiles.endpoint_asset.ownership.group.id` | `projection` | `gid` | "4fdcff0b7800b21b" | `—` | confirmed；按当前 expected 事件结构映射 |
| `extensions.profiles.endpoint_asset.ownership.group.name` | `projection` | `group_name` | "未分组终端" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.target.host.ip` | `projection` | `ip` | "198.51.100.114" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.target.host.mac` | `projection` | `mac` | "e8:6a:64:e0:05:6d" | `—` | confirmed；按当前 expected 事件结构映射 |
| `extensions.profiles.endpoint_asset.agent.fingerprint_id` | `projection` | `mid` | "81a15464af48af9f7fc8652fd820f9a75724c678e2920d7d5e7317fc57a2e900" | `—` | confirmed；按当前 expected 事件结构映射 |
| `source_finding.rule.signature_id` | `projection` | `rule_id` | "1.10.0003" | `—` | confirmed；按当前 expected 事件结构映射 |
| `source_finding.status` | `projection` | `status` | "0" | `—` | confirmed；按当前 expected 事件结构映射 |
| `source_finding.mitre.tactics[0]` | `projection` | `tactic` | "Persistence" | `—` | confirmed；按当前 expected 事件结构映射 |
| `source_finding.mitre.techniques[0]` | `projection` | `technique` | "Account Manipulation" | `—` | confirmed；按当前 expected 事件结构映射 |
| `source_finding.mitre.technique_id` | `projection` | `technique_id` | "T1098" | `—` | confirmed；按当前 expected 事件结构映射 |
| `source_finding.title` | `projection` | `alert_name` | "发现账户\"NetUser\"修改密码" | `—` | confirmed；按当前 expected 事件结构映射 |
| `source_finding.description` | `projection` | `description_i18n/zh_CN` | "发现用户\"DESKTOP-AACOVHR$\"修改了用户\"NetUser\"的密码." | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.related[0].process` | `projection` | `process_details` | {"name": "curl.exe", "uid": "63fe679e70ab3c96e517da0be9f271d3", "pid": "5041", "path": "C:\\Windows\\System32\\curl.exe", "cmdline": "C:\\Windows\\System32\\curl.exe", "file": {"hashes": {"md5": "eac53ddafb5cc9e780a7cc086ce7b2b1"}, "signatures": [{"signer": "HaoShuQing"}]}} | `—` | confirmed；告警触发进程对象；构造 related[0]，relation_type=alert_trigger_process，0 时间哨兵省略 |
| `source_finding.severity` | `dictionary` | `severity` | 2 -> "2" | `preserve_in_extension_and_review` | partial；按当前 expected 事件结构映射 |
| `source_finding.severity` | `transform` | `severity` | "2" | `—` | confirmed；按当前 expected 事件结构映射 |

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
