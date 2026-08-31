# WPL → SDM Event 字段映射

> 样例：`remote_login_failed.expected-sdm-event.json`；WPL 字段 39 个，映射 21，不落库 18，排除 0；另有平台默认、派生及结构字段 50 项。
> SDM 落位为逻辑路径；expected 位置为该样例中的实际物理 JSON 路径。

## 一、映射字段

| WPL 字段 | WPL 值 | SDM 落位 | expected 位置 | expected 值 | 说明 |
|---|---|---|---|---|---|
| `alert_id` | 2901778940093846007 | `source_original_event_id` | `source_original_event_id` | "2901778940093846007" | 按当前 expected 事件结构映射 |
| `asset_id` | 2838024086184001234 | `roles.target.host.id` | `roles_obj.target.host.id` | "2838024086184001234" | 按当前 expected 事件结构映射 |
| `asset_oid` | 271565193976001234 | `extensions.profiles.endpoint_asset.ownership.organization.id` | `extensions_obj.profiles.endpoint_asset.ownership.organization.id` | "271565193976001234" | 按当前 expected 事件结构映射 |
| `category_id` | 707 | `source_finding.category.original.code` | `source_finding_obj.category.original.code` | "707" | 按当前 expected 事件结构映射 |
| `client_id` | "7270627-289b66493f4ccba960e539723441f1b3" | `extensions.profiles.endpoint_asset.agent.id` | `extensions_obj.profiles.endpoint_asset.agent.id` | "7270627-289b66493f4ccba960e539723441f1b3" | 按当前 expected 事件结构映射 |
| `computer_name` | "DESKTOP-PBBOQGH" | `roles.target.host.name` | `roles_obj.target.host.name` | "DESKTOP-PBBOQGH" | 按当前 expected 事件结构映射 |
| `create_time` | 1733192603238 | `occur_time` | `occur_time` | 1733192603238 | 按当前 expected 事件结构映射 |
| `gid` | "4f9c3833b800d1f7" | `extensions.profiles.endpoint_asset.ownership.group.id` | `extensions_obj.profiles.endpoint_asset.ownership.group.id` | "4f9c3833b800d1f7" | 按当前 expected 事件结构映射 |
| `group_name` | "未分组终端" | `extensions.profiles.endpoint_asset.ownership.group.name` | `extensions_obj.profiles.endpoint_asset.ownership.group.name` | "未分组终端" | 按当前 expected 事件结构映射 |
| `ip` | "198.51.100.225" | `roles.target.host.ip` | `roles_obj.target.host.ip` | "198.51.100.225" | 按当前 expected 事件结构映射 |
| `mac` | "00-00-5E-00-53-EF" | `roles.target.host.mac` | `roles_obj.target.host.mac` | "00:00:5E:00:53:99" | 按当前 expected 事件结构映射 |
| `mid` | "f77c5d810841295807947633b324bc99d28e1678fc6461386400a59473057364" | `extensions.profiles.endpoint_asset.agent.fingerprint_id` | `extensions_obj.profiles.endpoint_asset.agent.fingerprint_id` | "f77c5d810841295807947633b324bc99d28e1678fc6461386400a59473057364" | 按当前 expected 事件结构映射 |
| `rule_id` | "41.0.0030" | `source_finding.rule.signature_id` | `source_finding_obj.rule.signature_id` | "41.0.0030" | 按当前 expected 事件结构映射 |
| `severity` | 3 | `source_finding.severity` | `source_finding_obj.severity` | "3" | 按当前 expected 事件结构映射 |
| `status` | 2 | `source_finding.status` | `source_finding_obj.status` | "2" | 按当前 expected 事件结构映射 |
| `tactic` | "Credential Access" | `source_finding.mitre.tactics[0]` | `source_finding_obj.mitre.tactics[0]` | "Credential Access" | 按当前 expected 事件结构映射 |
| `technique` | "Brute Force" | `source_finding.mitre.techniques[0]` | `source_finding_obj.mitre.techniques[0]` | "Brute Force" | 按当前 expected 事件结构映射 |
| `technique_id` | "T1110" | `source_finding.mitre.technique_id` | `source_finding_obj.mitre.technique_id` | "T1110" | 按当前 expected 事件结构映射 |
| `alert_name` | "远程登录失败" | `source_finding.title` | `source_finding_obj.title` | "远程登录失败" | 按当前 expected 事件结构映射 |
| `description_i18n/zh_CN` | "发现 \"203.0.113.13\" 使用用户名 \"ndows\" 远程登录失败。" | `source_finding.description` | `source_finding_obj.description` | "发现 \"203.0.113.13\" 使用用户名 \"ndows\" 远程登录失败。" | 按当前 expected 事件结构映射 |
| `process_details` | [{"process_create_time": 1731917394019, "process_id": "708", "process_guid": "4b8bf56ea503811181f20a2cac77405d", "process_name": "lsass.exe", "process_parent_guid": "process_parent_guid", "process_md5": "60e18f7b8d1f43731d0e9169c2d16547", "process_terminate_time": 1733192603238, "process_path": "C:lsass.exe", "process_command_line": "C:lsass.exe", "process_sign": "Microsoft Windows Publisher", "is_alert_trigger": true}] | `roles.related[0].process` | `roles_obj.related[0].process` | {"name": "lsass.exe", "uid": "4b8bf56ea503811181f20a2cac77405d", "pid": "708", "path": "C:lsass.exe", "cmdline": "C:lsass.exe", "file": {"hashes": {"md5": "60e18f7b8d1f43731d0e9169c2d16547"}, "signatures": [{"signer": "Microsoft Windows Publisher"}]}} | 告警触发进程对象；构造 related[0]，relation_type=alert_trigger_process，0 时间哨兵省略 |

## 二、不落库字段

| WPL 字段 | WPL 值 | 原因 |
|---|---|---|
| `client_login_user` | "client_login_user" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `custom_group_paths` | ",2868260887305703927,4f9c3833b800d1f7" | 分组路径原始串不进入事件对象；原值保留在 raw_msg |
| `description` | "发现 \"203.0.113.13\" 使用用户名 \"ndows\" 远程登录失败。" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `report_ip` | "198.51.100.225" | 疑似 Agent 上报链路地址；与终端 IP 不一致时不作为事件 source IP，原值保留在 raw_msg |
| `tactic_id` | "TA0006" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `type` | "edr_alert" | 仅用于 WPL 路由，稳定日志类型已由 log_type 表达；原值保留在 raw_msg |
| `log_type` | "flow_skylar_edr_alert_log" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `alert_name/zh_TW` | "遠端登入失敗" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `alert_name/en_US` | "Remote login failed" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `alert_name/zh_CN` | "远程登录失败" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `description_i18n/zh_TW` | "發現 \"203.0.113.13\" 使用使用者名稱 \"ndows\" 遠端登入失敗。" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `description_i18n/en_US` | "Found that \"203.0.113.13\" failed to remotely log in using username \"ndows\"." | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `ioc_value` | "blaxaplayer.com" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `malicious_family` | "Unknown" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `malicious_type` | "定向攻击" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `origin_killchain` | "c2" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `protocol` | "DNS" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `risky_source` | {"disposal_advice": "对终端进行断网操作，以避免影响其他终端", "ip": "198.51.100.23", "disposal_advice_i18n": {"zh_TW": "對終端進行斷網操作，以避免影響其他終端", "en_US": "Disconnect the terminal to prevent it from affecting other terminals", "zh_CN": "对终端进行断网操作，以避免影响其他终端"}, "mac": "00-00-5E-00-53-9C"} | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |

## 四、平台默认、派生及结构字段

| 来源 | SDM 落位 | expected 值 | 赋值责任与说明 |
|---|---|---|---|
| `platform_context.tenant_id` | `tenant_id` | "" | 由平台上下文提供 |
| `derived.sha256('|'+mapping_id+'|'+source_original_event_id)` | `event_id` | "evt-65c14e837739b457820c8409ac7636832aea9768549a025eac58932a78e207c6" | 按固定格式 sha256('|'+mapping_id+'|'+source_original_event_id) 生成；本样例 source_original_event_id 来自 WPL alert_id，tenant_id 为空不参与该公式 |
| `platform_context.log_id` | `log_id` | "log-tianqing-edr-alert-remote_login_failed" | 由平台上下文提供 |
| `raw_log_input` | `raw_msg` | "{\"gid\":\"4f9c3833b800d1f7\",\"collect_time_hour\":\"2024120310\",\"tactic_id\":\"TA0006\",\"mid\":\"f77c5d810841295807947633b324bc99d28e1678fc6461386400a59473057364\",\"description\":\"发现 \\\"203.0.113.13\\\" 使用用户名 \\\"ndows\\\" 远程登录失败。\",\"technique\":\"Brute Force\",\"asset_id\":2838024086184001234,\"installTime\":1733192603238,\"collect_time_date\":\"20241203\",\"type\":\"edr_alert\",\"mac\":\"00-00-5E-00-53-EF\",\"client_id\":\"7270627-289b66493f4ccba960e539723441f1b3\",\"tactic\":\"Credential Access\",\"asset_oid\":271565193976001234,\"process_details\":[{\"process_create_time\":1731917394019,\"process_id\":\"708\",\"process_guid\":\"4b8bf56ea503811181f20a2cac77405d\",\"process_name\":\"lsass.exe\",\"process_parent_guid\":\"process_parent_guid\",\"process_md5\":\"60e18f7b8d1f43731d0e9169c2d16547\",\"process_terminate_time\":1733192603238,\"process_path\":\"C:lsass.exe\",\"process_command_line\":\"C:lsass.exe\",\"process_sign\":\"Microsoft Windows Publisher\",\"is_alert_trigger\":true}],\"log_type\":\"flow_skylar_edr_alert_log\",\"category_id\":707,\"dispose_time\":1733192603238,\"occur_time\":1733192603238,\"alert_id\":2901778940093846007,\"sn\":\"271565193976001234-2838024086184001234\",\"risky_source\":{\"disposal_advice\":\"对终端进行断网操作，以避免影响其他终端\",\"ip\":\"198.51.100.23\",\"disposal_advice_i18n\":{\"zh_TW\":\"對終端進行斷網操作，以避免影響其他終端\",\"en_US\":\"Disconnect the terminal to prevent it from affecting other terminals\",\"zh_CN\":\"对终端进行断网操作，以避免影响其他终端\"},\"mac\":\"00-00-5E-00-53-9C\"},\"severity\":3,\"computer_name\":\"DESKTOP-PBBOQGH\",\"log_id\":\"567ad2b6fc9342ffbefc88b94c0d3b8c\",\"report_ip\":\"198.51.100.225\",\"batch_no\":\"98@5777308\",\"create_time\":1733192603238,\"group_name\":\"未分组终端\",\"ip\":\"198.51.100.225\",\"client_login_user\":\"client_login_user\",\"ioc_alerts\":[[{\"alert_name_en\":\"AridViper APT Organization Incident\",\"malicious_family\":\"Unknown\",\"protocol\":\"DNS\",\"kill_chain\":\"c2\",\"malicious_type\":\"定向攻击\",\"matched_ioc\":\"blaxaplayer.com\",\"malicious_type_en\":\"APT Incident\",\"alert_name\":\"AridViper APT活动事件\"}]],\"rule_id\":\"41.0.0030\",\"description_i18n\":{\"zh_TW\":\"發現 \\\"203.0.113.13\\\" 使用使用者名稱 \\\"ndows\\\" 遠端登入失敗。\",\"en_US\":\"Found that \\\"203.0.113.13\\\" failed to remotely log in using username \\\"ndows\\\".\",\"zh_CN\":\"发现 \\\"203.0.113.13\\\" 使用用户名 \\\"ndows\\\" 远程登录失败。\"},\"technique_id\":\"T1110\",\"collect_time\":1733192603238,\"custom_group_paths\":\",2868260887305703927,4f9c3833b800d1f7\",\"alert_name\":{\"zh_TW\":\"遠端登入失敗\",\"en_US\":\"Remote login failed\",\"zh_CN\":\"远程登录失败\"},\"status\":2}" | 由原始日志接入层保存，不由 OML 拼装 |
| `platform_context.ingest_time` | `ingest_time` | 1733192604239 | 由平台上下文提供 |
| `platform_context.parse_time` | `parse_time` | 1733192604358 | 由平台上下文提供 |
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
| `wpl.computer_name` | `source_host` | "DESKTOP-PBBOQGH" | 由 WPL 字段 computer_name 投影或转换后赋值 |
| `wpl.computer_name` | `target_host` | "DESKTOP-PBBOQGH" | 由 WPL 字段 computer_name 投影或转换后赋值 |
| `constant.qax` | `observer_vendor` | "qax" | 使用平台/映射规则常量 qax |
| `constant.tianqing` | `observer_product` | "tianqing" | 使用平台/映射规则常量 tianqing |
| `wpl.alert_id` | `source_finding_original_id` | "2901778940093846007" | 由 WPL 字段 alert_id 投影或转换后赋值 |
| `wpl.alert_name` | `source_finding_title` | "远程登录失败" | 由 WPL 字段 alert_name 投影或转换后赋值 |
| `wpl.severity` | `source_finding_severity` | "3" | 由 WPL 字段 severity 投影或转换后赋值 |
| `wpl.category_id` | `source_finding_category` | "707" | 由 WPL 字段 category_id 投影或转换后赋值 |
| `wpl.rule_id` | `source_finding_signature_id` | "41.0.0030" | 由 WPL 字段 rule_id 投影或转换后赋值 |
| `derived.entity_ref(host, wpl.asset_id)` | `roles.target.ref_id` | "host::2838024086184001234" | 按确定性规则 entity_ref(host, wpl.asset_id) 派生 |
| `constant.host` | `roles.target.entity_type` | "host" | 使用平台/映射规则常量 host |
| `constant.tianqing` | `roles.observer.product.name` | "tianqing" | 使用平台/映射规则常量 tianqing |
| `constant.qax` | `roles.observer.device.vendor` | "qax" | 使用平台/映射规则常量 qax |
| `derived.entity_ref(process, wpl.process_details[0].process_guid)` | `roles.related[0].ref_id` | "process::4b8bf56ea503811181f20a2cac77405d" | 按确定性规则 entity_ref(process, wpl.process_details[0].process_guid) 派生 |
| `constant.process` | `roles.related[0].entity_type` | "process" | 使用平台/映射规则常量 process |
| `constant.alert_trigger_process` | `roles.related[0].relation_type` | "alert_trigger_process" | 使用平台/映射规则常量 alert_trigger_process |
| `wpl.alert_id` | `source_finding.original_id` | "2901778940093846007" | 由 WPL 字段 alert_id 投影或转换后赋值 |
| `assembly.one_finding_per_wpl_alert` | `source_finding.count` | 1 | 当前一条 WPL 告警装配一个 finding，因此固定为 1 |
| `constant.sdm_schema_version` | `extensions.schema_version` | 2 | 使用平台/映射规则常量 sdm_schema_version |
| `wpl.ioc_value` | `extensions.source_private.ioc_value` | "blaxaplayer.com" | 由 WPL 字段 ioc_value 投影或转换后赋值 |
| `wpl.malicious_family` | `extensions.source_private.malicious_family` | "Unknown" | 由 WPL 字段 malicious_family 投影或转换后赋值 |
| `wpl.malicious_type` | `extensions.source_private.malicious_type` | "定向攻击" | 由 WPL 字段 malicious_type 投影或转换后赋值 |
| `wpl.origin_killchain` | `extensions.source_private.origin_killchain` | "c2" | 由 WPL 字段 origin_killchain 投影或转换后赋值 |
| `wpl.protocol` | `extensions.source_private.protocol` | "DNS" | 由 WPL 字段 protocol 投影或转换后赋值 |
| `assembly.sdm_projection` | `extensions.source_private.risky_source.disposal_advice` | "对终端进行断网操作，以避免影响其他终端" | 按事件装配约定 sdm_projection 生成 |
| `wpl.risky_source.ip` | `extensions.source_private.risky_source.ip` | "198.51.100.23" | 由 WPL 字段 risky_source.ip 投影或转换后赋值 |
| `wpl.risky_source.disposal_advice_i18n.zh_TW` | `extensions.source_private.risky_source.disposal_advice_i18n.zh_TW` | "對終端進行斷網操作，以避免影響其他終端" | 由 WPL 字段 risky_source.disposal_advice_i18n.zh_TW 投影或转换后赋值 |
| `wpl.risky_source.disposal_advice_i18n.en_US` | `extensions.source_private.risky_source.disposal_advice_i18n.en_US` | "Disconnect the terminal to prevent it from affecting other terminals" | 由 WPL 字段 risky_source.disposal_advice_i18n.en_US 投影或转换后赋值 |
| `assembly.sdm_projection` | `extensions.source_private.risky_source.disposal_advice_i18n.zh_CN` | "对终端进行断网操作，以避免影响其他终端" | 按事件装配约定 sdm_projection 生成 |
| `wpl.risky_source.mac` | `extensions.source_private.risky_source.mac` | "00-00-5E-00-53-9C" | 由 WPL 字段 risky_source.mac 投影或转换后赋值 |
| `derived.entity_ref(host, wpl.asset_id)` | `extensions.profiles.endpoint_asset.subject_ref.ref_id` | "host::2838024086184001234" | 按确定性规则 entity_ref(host, wpl.asset_id) 派生 |

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
| `extensions.source_private.risky_source.disposal_advice` | `derived` | `assembly.sdm_projection` | `assembly.sdm_projection` | `—` | confirmed；按事件装配约定 sdm_projection 生成 |
| `extensions.source_private.risky_source.disposal_advice_i18n.zh_CN` | `derived` | `assembly.sdm_projection` | `assembly.sdm_projection` | `—` | confirmed；按事件装配约定 sdm_projection 生成 |
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
| `extensions.source_private.ioc_value` | `projection` | `ioc_value` | `wpl.ioc_value` | `—` | confirmed；由 WPL 字段 ioc_value 投影或转换后赋值 |
| `extensions.source_private.malicious_family` | `projection` | `malicious_family` | `wpl.malicious_family` | `—` | confirmed；由 WPL 字段 malicious_family 投影或转换后赋值 |
| `extensions.source_private.malicious_type` | `projection` | `malicious_type` | `wpl.malicious_type` | `—` | confirmed；由 WPL 字段 malicious_type 投影或转换后赋值 |
| `extensions.source_private.origin_killchain` | `projection` | `origin_killchain` | `wpl.origin_killchain` | `—` | confirmed；由 WPL 字段 origin_killchain 投影或转换后赋值 |
| `extensions.source_private.protocol` | `projection` | `protocol` | `wpl.protocol` | `—` | confirmed；由 WPL 字段 protocol 投影或转换后赋值 |
| `extensions.source_private.risky_source.ip` | `projection` | `risky_source.ip` | `wpl.risky_source.ip` | `—` | confirmed；由 WPL 字段 risky_source.ip 投影或转换后赋值 |
| `extensions.source_private.risky_source.disposal_advice_i18n.zh_TW` | `projection` | `risky_source.disposal_advice_i18n.zh_TW` | `wpl.risky_source.disposal_advice_i18n.zh_TW` | `—` | confirmed；由 WPL 字段 risky_source.disposal_advice_i18n.zh_TW 投影或转换后赋值 |
| `extensions.source_private.risky_source.disposal_advice_i18n.en_US` | `projection` | `risky_source.disposal_advice_i18n.en_US` | `wpl.risky_source.disposal_advice_i18n.en_US` | `—` | confirmed；由 WPL 字段 risky_source.disposal_advice_i18n.en_US 投影或转换后赋值 |
| `extensions.source_private.risky_source.mac` | `projection` | `risky_source.mac` | `wpl.risky_source.mac` | `—` | confirmed；由 WPL 字段 risky_source.mac 投影或转换后赋值 |
| `source_original_event_id` | `projection` | `alert_id` | "2901778940093846007" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.target.host.id` | `projection` | `asset_id` | "2838024086184001234" | `—` | confirmed；按当前 expected 事件结构映射 |
| `extensions.profiles.endpoint_asset.ownership.organization.id` | `projection` | `asset_oid` | "271565193976001234" | `—` | confirmed；按当前 expected 事件结构映射 |
| `source_finding.category.original.code` | `projection` | `category_id` | "707" | `—` | confirmed；按当前 expected 事件结构映射 |
| `extensions.profiles.endpoint_asset.agent.id` | `projection` | `client_id` | "7270627-289b66493f4ccba960e539723441f1b3" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.target.host.name` | `projection` | `computer_name` | "DESKTOP-PBBOQGH" | `—` | confirmed；按当前 expected 事件结构映射 |
| `occur_time` | `projection` | `create_time` | 1733192603238 | `—` | confirmed；按当前 expected 事件结构映射 |
| `extensions.profiles.endpoint_asset.ownership.group.id` | `projection` | `gid` | "4f9c3833b800d1f7" | `—` | confirmed；按当前 expected 事件结构映射 |
| `extensions.profiles.endpoint_asset.ownership.group.name` | `projection` | `group_name` | "未分组终端" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.target.host.ip` | `projection` | `ip` | "198.51.100.225" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.target.host.mac` | `projection` | `mac` | "00:00:5E:00:53:99" | `—` | confirmed；按当前 expected 事件结构映射 |
| `extensions.profiles.endpoint_asset.agent.fingerprint_id` | `projection` | `mid` | "f77c5d810841295807947633b324bc99d28e1678fc6461386400a59473057364" | `—` | confirmed；按当前 expected 事件结构映射 |
| `source_finding.rule.signature_id` | `projection` | `rule_id` | "41.0.0030" | `—` | confirmed；按当前 expected 事件结构映射 |
| `source_finding.status` | `projection` | `status` | "2" | `—` | confirmed；按当前 expected 事件结构映射 |
| `source_finding.mitre.tactics[0]` | `projection` | `tactic` | "Credential Access" | `—` | confirmed；按当前 expected 事件结构映射 |
| `source_finding.mitre.techniques[0]` | `projection` | `technique` | "Brute Force" | `—` | confirmed；按当前 expected 事件结构映射 |
| `source_finding.mitre.technique_id` | `projection` | `technique_id` | "T1110" | `—` | confirmed；按当前 expected 事件结构映射 |
| `source_finding.title` | `projection` | `alert_name` | "远程登录失败" | `—` | confirmed；按当前 expected 事件结构映射 |
| `source_finding.description` | `projection` | `description_i18n/zh_CN` | "发现 \"203.0.113.13\" 使用用户名 \"ndows\" 远程登录失败。" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.related[0].process` | `projection` | `process_details` | {"name": "lsass.exe", "uid": "4b8bf56ea503811181f20a2cac77405d", "pid": "708", "path": "C:lsass.exe", "cmdline": "C:lsass.exe", "file": {"hashes": {"md5": "60e18f7b8d1f43731d0e9169c2d16547"}, "signatures": [{"signer": "Microsoft Windows Publisher"}]}} | `—` | confirmed；告警触发进程对象；构造 related[0]，relation_type=alert_trigger_process，0 时间哨兵省略 |
| `source_finding.severity` | `dictionary` | `severity` | 3 -> "3" | `preserve_in_extension_and_review` | partial；按当前 expected 事件结构映射 |
| `source_finding.severity` | `transform` | `severity` | "3" | `—` | confirmed；按当前 expected 事件结构映射 |

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
