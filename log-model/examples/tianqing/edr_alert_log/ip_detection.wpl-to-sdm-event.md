# WPL → SDM Event 字段映射

> 样例：`ip_detection.expected-sdm-event.json`；WPL 字段 29 个，映射 17，不落库 12，排除 0；另有平台默认、派生及结构字段 45 项。
> SDM 落位为逻辑路径；expected 位置为该样例中的实际物理 JSON 路径。

## 一、映射字段

| WPL 字段 | WPL 值 | SDM 落位 | expected 位置 | expected 值 | 说明 |
|---|---|---|---|---|---|
| `alert_id` | 2788957435086241906 | `source_original_event_id` | `source_original_event_id` | "2788957435086241906" | 按当前 expected 事件结构映射 |
| `asset_id` | 2743783992242209615 | `roles.target.host.id` | `roles_obj.target.host.id` | "2743783992242209615" | 按当前 expected 事件结构映射 |
| `asset_oid` | 2715651939760080161 | `extensions.profiles.endpoint_asset.ownership.organization.id` | `extensions_obj.profiles.endpoint_asset.ownership.organization.id` | "2715651939760080161" | 按当前 expected 事件结构映射 |
| `category_id` | 3 | `source_finding.category.original.code` | `source_finding_obj.category.original.code` | "3" | 按当前 expected 事件结构映射 |
| `client_id` | "5140676-a4e38981588fd663277bc9acecf2d0ba" | `extensions.profiles.endpoint_asset.agent.id` | `extensions_obj.profiles.endpoint_asset.agent.id` | "5140676-a4e38981588fd663277bc9acecf2d0ba" | 按当前 expected 事件结构映射 |
| `computer_name` | "DESKTOP-G1JPE9R" | `roles.target.host.name` | `roles_obj.target.host.name` | "DESKTOP-G1JPE9R" | 按当前 expected 事件结构映射 |
| `create_time` | 1726818300736 | `occur_time` | `occur_time` | 1726818300736 | 按当前 expected 事件结构映射 |
| `gid` | "4d67b9be1e0000c0" | `extensions.profiles.endpoint_asset.ownership.group.id` | `extensions_obj.profiles.endpoint_asset.ownership.group.id` | "4d67b9be1e0000c0" | 按当前 expected 事件结构映射 |
| `group_name` | "edr" | `extensions.profiles.endpoint_asset.ownership.group.name` | `extensions_obj.profiles.endpoint_asset.ownership.group.name` | "edr" | 按当前 expected 事件结构映射 |
| `ip` | "203.0.113.101" | `roles.target.host.ip` | `roles_obj.target.host.ip` | "203.0.113.101" | 按当前 expected 事件结构映射 |
| `mac` | "00-0C-29-BC-5C-73" | `roles.target.host.mac` | `roles_obj.target.host.mac` | "00:0c:29:bc:5c:73" | 按当前 expected 事件结构映射 |
| `mid` | "916fb9cf5509058e723735a7414af82d274bcf72c4c839e0644d8e86aa292a1b" | `extensions.profiles.endpoint_asset.agent.fingerprint_id` | `extensions_obj.profiles.endpoint_asset.agent.fingerprint_id` | "916fb9cf5509058e723735a7414af82d274bcf72c4c839e0644d8e86aa292a1b" | 按当前 expected 事件结构映射 |
| `rule_id` | "99.0.0003" | `source_finding.rule.signature_id` | `source_finding_obj.rule.signature_id` | "99.0.0003" | 按当前 expected 事件结构映射 |
| `severity` | 4 | `source_finding.severity` | `source_finding_obj.severity` | "4" | 按当前 expected 事件结构映射 |
| `status` | 0 | `source_finding.status` | `source_finding_obj.status` | "0" | 按当前 expected 事件结构映射 |
| `description_i18n/zh_CN` | "IP日志检测dip" | `source_finding.description` | `source_finding_obj.description` | "IP日志检测dip" | 按当前 expected 事件结构映射 |
| `process_details` | [{"process_name": "curl.exe", "process_id": "15828", "process_md5": "bdebd2fc4927da00eea263af9cf8f7ed", "process_path": "C:\\Windows\\system32\\curl.exe", "process_sign": "Microsoft Windows", "process_command_line": "curl 203.0.113.15", "process_create_time": 0, "process_terminate_time": 0, "process_guid": "70512dd92328f8f330377892e63cfc4e", "process_parent_guid": "", "is_alert_trigger": true}] | `roles.related[0].process` | `roles_obj.related[0].process` | {"name": "curl.exe", "uid": "70512dd92328f8f330377892e63cfc4e", "pid": "15828", "path": "C:\\Windows\\system32\\curl.exe", "cmdline": "curl 203.0.113.15", "file": {"hashes": {"md5": "bdebd2fc4927da00eea263af9cf8f7ed"}, "signatures": [{"signer": "Microsoft Windows"}]}} | 告警触发进程对象；构造 related[0]，relation_type=alert_trigger_process，0 时间哨兵省略 |

## 二、不落库字段

| WPL 字段 | WPL 值 | 原因 |
|---|---|---|
| `client_login_user` | "" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `custom_group_paths` | ",2788715602640896192,4d67b9be1e0000c0" | 分组路径原始串不进入事件对象；原值保留在 raw_msg |
| `description` | "IP日志检测dip" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `report_ip` | "198.51.100.198" | 疑似 Agent 上报链路地址；与终端 IP 不一致时不作为事件 source IP，原值保留在 raw_msg |
| `tactic` | "" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `technique` | "" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `type` | "edr_alert" | 仅用于 WPL 路由，稳定日志类型已由 log_type 表达；原值保留在 raw_msg |
| `ioc_value` | "203.0.113.15:80" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `malicious_family` | "Generic Trojan" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `malicious_type` | "远控木马" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `origin_killchain` | "general" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `protocol` | "TCP" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |

## 四、平台默认、派生及结构字段

| 来源 | SDM 落位 | expected 值 | 赋值责任与说明 |
|---|---|---|---|
| `platform_context.tenant_id` | `tenant_id` | "" | 由平台上下文提供 |
| `derived.sha256('|'+mapping_id+'|'+source_original_event_id)` | `event_id` | "evt-4b73cefc3f1a5fa1d95589ac700b3ac9928ab03eed706d138abcef4c11cb37e7" | 按固定格式 sha256('|'+mapping_id+'|'+source_original_event_id) 生成；本样例 source_original_event_id 来自 WPL alert_id，tenant_id 为空不参与该公式 |
| `platform_context.log_id` | `log_id` | "log-tianqing-edr-alert-ip_detection" | 由平台上下文提供 |
| `raw_log_input` | `raw_msg` | "{\"type\":\"edr_alert\",\"alert_id\":2788957435086241906,\"gid\":\"4d67b9be1e0000c0\",\"group_name\":\"edr\",\"mid\":\"916fb9cf5509058e723735a7414af82d274bcf72c4c839e0644d8e86aa292a1b\",\"mac\":\"00-0C-29-BC-5C-73\",\"computer_name\":\"DESKTOP-G1JPE9R\",\"custom_group_paths\":\",2788715602640896192,4d67b9be1e0000c0\",\"report_ip\":\"198.51.100.198\",\"ip\":\"203.0.113.101\",\"client_id\":\"5140676-a4e38981588fd663277bc9acecf2d0ba\",\"asset_oid\":2715651939760080161,\"asset_id\":2743783992242209615,\"client_login_user\":\"\",\"severity\":4,\"category_id\":3,\"description\":\"IP日志检测dip\",\"technique\":\"\",\"tactic\":\"\",\"create_time\":1726818300736,\"status\":0,\"rule_id\":\"99.0.0003\",\"process_details\":[{\"process_name\":\"curl.exe\",\"process_id\":\"15828\",\"process_md5\":\"bdebd2fc4927da00eea263af9cf8f7ed\",\"process_path\":\"C:\\\\Windows\\\\system32\\\\curl.exe\",\"process_sign\":\"Microsoft Windows\",\"process_command_line\":\"curl 203.0.113.15\",\"process_create_time\":0,\"process_terminate_time\":0,\"process_guid\":\"70512dd92328f8f330377892e63cfc4e\",\"process_parent_guid\":\"\",\"is_alert_trigger\":true}],\"ioc_alerts\":[[{\"matched_ioc\":\"203.0.113.15:80\",\"malicious_family\":\"Generic Trojan\",\"malicious_type\":\"远控木马\",\"kill_chain\":\"general\",\"alert_name\":\"普通远控木马活动事件\",\"protocol\":\"TCP\"}]]}" | 由原始日志接入层保存，不由 OML 拼装 |
| `platform_context.ingest_time` | `ingest_time` | 1726818301737 | 由平台上下文提供 |
| `platform_context.parse_time` | `parse_time` | 1726818301856 | 由平台上下文提供 |
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
| `wpl.computer_name` | `source_host` | "DESKTOP-G1JPE9R" | 由 WPL 字段 computer_name 投影或转换后赋值 |
| `wpl.computer_name` | `target_host` | "DESKTOP-G1JPE9R" | 由 WPL 字段 computer_name 投影或转换后赋值 |
| `constant.qax` | `observer_vendor` | "qax" | 使用平台/映射规则常量 qax |
| `constant.tianqing` | `observer_product` | "tianqing" | 使用平台/映射规则常量 tianqing |
| `wpl.alert_id` | `source_finding_original_id` | "2788957435086241906" | 由 WPL 字段 alert_id 投影或转换后赋值 |
| `wpl.alert_name` | `source_finding_title` | "IP日志检测dip" | 由 WPL 字段 alert_name 投影或转换后赋值 |
| `wpl.severity` | `source_finding_severity` | "4" | 由 WPL 字段 severity 投影或转换后赋值 |
| `wpl.category_id` | `source_finding_category` | "3" | 由 WPL 字段 category_id 投影或转换后赋值 |
| `wpl.rule_id` | `source_finding_signature_id` | "99.0.0003" | 由 WPL 字段 rule_id 投影或转换后赋值 |
| `derived.entity_ref(host, wpl.asset_id)` | `roles.target.ref_id` | "host::2743783992242209615" | 按确定性规则 entity_ref(host, wpl.asset_id) 派生 |
| `constant.host` | `roles.target.entity_type` | "host" | 使用平台/映射规则常量 host |
| `constant.tianqing` | `roles.observer.product.name` | "tianqing" | 使用平台/映射规则常量 tianqing |
| `constant.qax` | `roles.observer.device.vendor` | "qax" | 使用平台/映射规则常量 qax |
| `derived.entity_ref(process, wpl.process_details[0].process_guid)` | `roles.related[0].ref_id` | "process::70512dd92328f8f330377892e63cfc4e" | 按确定性规则 entity_ref(process, wpl.process_details[0].process_guid) 派生 |
| `constant.process` | `roles.related[0].entity_type` | "process" | 使用平台/映射规则常量 process |
| `constant.alert_trigger_process` | `roles.related[0].relation_type` | "alert_trigger_process" | 使用平台/映射规则常量 alert_trigger_process |
| `wpl.alert_id` | `source_finding.original_id` | "2788957435086241906" | 由 WPL 字段 alert_id 投影或转换后赋值 |
| `assembly.sdm_projection` | `source_finding.title` | "IP日志检测dip" | 按事件装配约定 sdm_projection 生成 |
| `assembly.one_finding_per_wpl_alert` | `source_finding.count` | 1 | 当前一条 WPL 告警装配一个 finding，因此固定为 1 |
| `constant.sdm_schema_version` | `extensions.schema_version` | 2 | 使用平台/映射规则常量 sdm_schema_version |
| `wpl.ioc_value` | `extensions.source_private.ioc_value` | "203.0.113.15:80" | 由 WPL 字段 ioc_value 投影或转换后赋值 |
| `wpl.malicious_family` | `extensions.source_private.malicious_family` | "Generic Trojan" | 由 WPL 字段 malicious_family 投影或转换后赋值 |
| `wpl.malicious_type` | `extensions.source_private.malicious_type` | "远控木马" | 由 WPL 字段 malicious_type 投影或转换后赋值 |
| `wpl.origin_killchain` | `extensions.source_private.origin_killchain` | "general" | 由 WPL 字段 origin_killchain 投影或转换后赋值 |
| `wpl.protocol` | `extensions.source_private.protocol` | "TCP" | 由 WPL 字段 protocol 投影或转换后赋值 |
| `derived.entity_ref(host, wpl.asset_id)` | `extensions.profiles.endpoint_asset.subject_ref.ref_id` | "host::2743783992242209615" | 按确定性规则 entity_ref(host, wpl.asset_id) 派生 |

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
| `source_finding.title` | `derived` | `assembly.sdm_projection` | `assembly.sdm_projection` | `—` | confirmed；按事件装配约定 sdm_projection 生成 |
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
| `extensions.source_private.ioc_value` | `projection` | `ioc_value` | `wpl.ioc_value` | `—` | confirmed；由 WPL 字段 ioc_value 投影或转换后赋值 |
| `extensions.source_private.malicious_family` | `projection` | `malicious_family` | `wpl.malicious_family` | `—` | confirmed；由 WPL 字段 malicious_family 投影或转换后赋值 |
| `extensions.source_private.malicious_type` | `projection` | `malicious_type` | `wpl.malicious_type` | `—` | confirmed；由 WPL 字段 malicious_type 投影或转换后赋值 |
| `extensions.source_private.origin_killchain` | `projection` | `origin_killchain` | `wpl.origin_killchain` | `—` | confirmed；由 WPL 字段 origin_killchain 投影或转换后赋值 |
| `extensions.source_private.protocol` | `projection` | `protocol` | `wpl.protocol` | `—` | confirmed；由 WPL 字段 protocol 投影或转换后赋值 |
| `source_original_event_id` | `projection` | `alert_id` | "2788957435086241906" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.target.host.id` | `projection` | `asset_id` | "2743783992242209615" | `—` | confirmed；按当前 expected 事件结构映射 |
| `extensions.profiles.endpoint_asset.ownership.organization.id` | `projection` | `asset_oid` | "2715651939760080161" | `—` | confirmed；按当前 expected 事件结构映射 |
| `source_finding.category.original.code` | `projection` | `category_id` | "3" | `—` | confirmed；按当前 expected 事件结构映射 |
| `extensions.profiles.endpoint_asset.agent.id` | `projection` | `client_id` | "5140676-a4e38981588fd663277bc9acecf2d0ba" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.target.host.name` | `projection` | `computer_name` | "DESKTOP-G1JPE9R" | `—` | confirmed；按当前 expected 事件结构映射 |
| `occur_time` | `projection` | `create_time` | 1726818300736 | `—` | confirmed；按当前 expected 事件结构映射 |
| `extensions.profiles.endpoint_asset.ownership.group.id` | `projection` | `gid` | "4d67b9be1e0000c0" | `—` | confirmed；按当前 expected 事件结构映射 |
| `extensions.profiles.endpoint_asset.ownership.group.name` | `projection` | `group_name` | "edr" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.target.host.ip` | `projection` | `ip` | "203.0.113.101" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.target.host.mac` | `projection` | `mac` | "00:0c:29:bc:5c:73" | `—` | confirmed；按当前 expected 事件结构映射 |
| `extensions.profiles.endpoint_asset.agent.fingerprint_id` | `projection` | `mid` | "916fb9cf5509058e723735a7414af82d274bcf72c4c839e0644d8e86aa292a1b" | `—` | confirmed；按当前 expected 事件结构映射 |
| `source_finding.rule.signature_id` | `projection` | `rule_id` | "99.0.0003" | `—` | confirmed；按当前 expected 事件结构映射 |
| `source_finding.status` | `projection` | `status` | "0" | `—` | confirmed；按当前 expected 事件结构映射 |
| `source_finding.description` | `projection` | `description_i18n/zh_CN` | "IP日志检测dip" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.related[0].process` | `projection` | `process_details` | {"name": "curl.exe", "uid": "70512dd92328f8f330377892e63cfc4e", "pid": "15828", "path": "C:\\Windows\\system32\\curl.exe", "cmdline": "curl 203.0.113.15", "file": {"hashes": {"md5": "bdebd2fc4927da00eea263af9cf8f7ed"}, "signatures": [{"signer": "Microsoft Windows"}]}} | `—` | confirmed；告警触发进程对象；构造 related[0]，relation_type=alert_trigger_process，0 时间哨兵省略 |
| `source_finding.severity` | `dictionary` | `severity` | 4 -> "4" | `preserve_in_extension_and_review` | partial；按当前 expected 事件结构映射 |
| `source_finding.severity` | `transform` | `severity` | "4" | `—` | confirmed；按当前 expected 事件结构映射 |

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
