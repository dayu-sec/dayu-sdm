# WPL → SDM Event 字段映射

> 样例：`rdp_bruteforce.expected-sdm-event.json`；WPL 字段 34 个，映射 22，不落库 12，排除 0；另有平台默认、派生及结构字段 87 项。
> SDM 落位为逻辑路径；expected 位置为该样例中的实际物理 JSON 路径。

## 一、映射字段

| WPL 字段 | WPL 值 | SDM 落位 | expected 位置 | expected 值 | 说明 |
|---|---|---|---|---|---|
| `alert_id` | "2897526172445364727" | `source_original_event_id` | `source_original_event_id` | "2897526172445364727" | 按当前 expected 事件结构映射 |
| `alert_name` | "检测到远程RDP爆破" | `source_finding.title` | `source_finding_obj.title` | "检测到远程RDP爆破" | 按当前 expected 事件结构映射 |
| `asset_id` | "2868257359929541780" | `roles.target.host.id` | `roles_obj.target.host.id` | "2868257359929541780" | 按当前 expected 事件结构映射 |
| `asset_oid` | "2653788242175861718" | `extensions.profiles.endpoint_asset.ownership.organization.id` | `extensions_obj.profiles.endpoint_asset.ownership.organization.id` | "2653788242175861718" | 按当前 expected 事件结构映射 |
| `category_id` | "801" | `source_finding.category.original.code` | `source_finding_obj.category.original.code` | "801" | 按当前 expected 事件结构映射 |
| `client_id` | "0881058-dfb9a23257c64098060e699601b17217" | `extensions.profiles.endpoint_asset.agent.id` | `extensions_obj.profiles.endpoint_asset.agent.id` | "0881058-dfb9a23257c64098060e699601b17217" | 按当前 expected 事件结构映射 |
| `computer_name` | "DESKTOP-NU779RJ" | `roles.target.host.name` | `roles_obj.target.host.name` | "DESKTOP-NU779RJ" | 按当前 expected 事件结构映射 |
| `create_time` | 1727060095000 | `occur_time` | `occur_time` | 1727060095000 | 按当前 expected 事件结构映射 |
| `des_ip` | "203.0.113.31" | `source_finding.attacker.endpoint.ip` | `source_finding_obj.attacker.endpoint.ip` | "203.0.113.31" | 仅对已确认的 RDP 爆破类别解释为攻击端 IP；其他类别不得按字段位置套用 |
| `description_i18n/zh_CN` | "检测到\"203.0.113.31\"正在对本机进行远程RDP爆破" | `source_finding.description` | `source_finding_obj.description` | "检测到\"203.0.113.31\"正在对本机进行远程RDP爆破" | 按当前 expected 事件结构映射 |
| `gid` | "4f9c3833b800d1f7" | `extensions.profiles.endpoint_asset.ownership.group.id` | `extensions_obj.profiles.endpoint_asset.ownership.group.id` | "4f9c3833b800d1f7" | 按当前 expected 事件结构映射 |
| `group_name` | "未分组终端" | `extensions.profiles.endpoint_asset.ownership.group.name` | `extensions_obj.profiles.endpoint_asset.ownership.group.name` | "未分组终端" | 按当前 expected 事件结构映射 |
| `ip` | "198.51.100.211" | `roles.target.host.ip` | `roles_obj.target.host.ip` | "198.51.100.211" | 按当前 expected 事件结构映射 |
| `mac` | "00-00-5E-00-53-79" | `roles.target.host.mac` | `roles_obj.target.host.mac` | "00:00:5E:00:53:23" | 按当前 expected 事件结构映射 |
| `mid` | "ec80b820d87d7cd7ac916240bcdff7215ae3118feaf070c13afbf06e69af4eb3" | `extensions.profiles.endpoint_asset.agent.fingerprint_id` | `extensions_obj.profiles.endpoint_asset.agent.fingerprint_id` | "ec80b820d87d7cd7ac916240bcdff7215ae3118feaf070c13afbf06e69af4eb3" | 按当前 expected 事件结构映射 |
| `process_details` | [{"process_name": "svchost.exe", "process_id": "784", "process_md5": "7469cc568ad6821fd9d925542730a7d8", "process_path": "C:\\Windows\\System32\\svchost.exe", "process_sign": "Microsoft Windows Publisher", "process_command_line": "C:\\WINDOWS\\System32\\svchost.exe -k NetworkService -s TermService", "process_create_time": 0, "process_terminate_time": 0, "process_guid": "7578323a1a41c3fd4532c3aac828551e", "process_parent_guid": "", "is_alert_trigger": true}] | `roles.related[0].process` | `roles_obj.related[0].process` | {"name": "svchost.exe", "uid": "7578323a1a41c3fd4532c3aac828551e", "pid": "784", "path": "C:\\Windows\\System32\\svchost.exe", "cmdline": "C:\\WINDOWS\\System32\\svchost.exe -k NetworkService -s TermService", "file": {"hashes": {"md5": "7469cc568ad6821fd9d925542730a7d8"}, "signatures": [{"signer": "Microsoft Windows Publisher"}]}} | 告警触发进程对象；构造 related[0]，relation_type=alert_trigger_process，0 时间哨兵省略 |
| `rule_id` | "41.0.0198" | `source_finding.rule.signature_id` | `source_finding_obj.rule.signature_id` | "41.0.0198" | 按当前 expected 事件结构映射 |
| `severity` | "2" | `source_finding.severity` | `source_finding_obj.severity` | "2" | 按当前 expected 事件结构映射 |
| `status` | "0" | `source_finding.status` | `source_finding_obj.status` | "0" | 按当前 expected 事件结构映射 |
| `tactic` | "Credential Access" | `source_finding.mitre.tactics[0]` | `source_finding_obj.mitre.tactics[0]` | "Credential Access" | 按当前 expected 事件结构映射 |
| `technique` | "Brute Force" | `source_finding.mitre.techniques[0]` | `source_finding_obj.mitre.techniques[0]` | "Brute Force" | 按当前 expected 事件结构映射 |
| `technique_id` | "T1110" | `source_finding.mitre.technique_id` | `source_finding_obj.mitre.technique_id` | "T1110" | 按当前 expected 事件结构映射 |

## 二、不落库字段

| WPL 字段 | WPL 值 | 原因 |
|---|---|---|
| `alert_name/en_US` | "Remote RDP brute force detected" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `alert_name/zh_TW` | "偵測到遠程RDP爆破" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `client_login_user` | "" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `custom_group_paths` | ",2868260887305703927,4f9c3833b800d1f7" | 分组路径原始串不进入事件对象；原值保留在 raw_msg |
| `tmp1` | "检测到" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `tmp2` | "正在对本机进行远程RDP爆破" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `des_user` | "" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `description_i18n/en_US` | "Detected that \"203.0.113.31\" is performing remote RDP brute force on this machine" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `description_i18n/zh_TW` | "偵測到\"203.0.113.31\"正在對本機進行遠端RDP爆破" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `report_ip` | "198.51.100.211" | 疑似 Agent 上报链路地址；与终端 IP 不一致时不作为事件 source IP，原值保留在 raw_msg |
| `tactic_id` | "TA0006" | 当前事件未采用该字段；空值、哨兵、机械重复或非检索上下文不落库，原值保留在 raw_msg |
| `type` | "edr_alert" | 仅用于 WPL 路由，稳定日志类型已由 log_type 表达；原值保留在 raw_msg |

## 四、平台默认、派生及结构字段

| 来源 | SDM 落位 | expected 值 | 赋值责任与说明 |
|---|---|---|---|
| `platform_context.tenant_id` | `tenant_id` | "" | 由平台上下文提供 |
| `derived.sha256('|'+mapping_id+'|'+source_original_event_id)` | `event_id` | "evt-520d887852e860b5cf9ee38d95fb7a5ea5a1ecbe0dd82e3a3b47f277b961216e" | 按固定格式 sha256('|'+mapping_id+'|'+source_original_event_id) 生成；本样例 source_original_event_id 来自 WPL alert_id，tenant_id 为空不参与该公式 |
| `platform_context.log_id` | `log_id` | "log-tianqing-edr-alert-0001" | 由平台上下文提供 |
| `raw_log_input` | `raw_msg` | "{\"type\":\"edr_alert\",\"alert_id\":2897526172445364727,\"alert_name\":{\"en_US\":\"Remote RDP brute force detected\",\"zh_CN\":\"检测到远程RDP爆破\",\"zh_TW\":\"偵測到遠程RDP爆破\"},\"gid\":\"4f9c3833b800d1f7\",\"group_name\":\"未分组终端\",\"mid\":\"ec80b820d87d7cd7ac916240bcdff7215ae3118feaf070c13afbf06e69af4eb3\",\"mac\":\"00-00-5E-00-53-79\",\"computer_name\":\"DESKTOP-NU779RJ\",\"custom_group_paths\":\",2868260887305703927,4f9c3833b800d1f7\",\"report_ip\":\"198.51.100.211\",\"ip\":\"198.51.100.211\",\"client_id\":\"0881058-dfb9a23257c64098060e699601b17217\",\"asset_oid\":2653788242175861718,\"asset_id\":2868257359929541780,\"client_login_user\":\"\",\"severity\":2,\"category_id\":801,\"technique_id\":\"T1110\",\"tactic_id\":\"TA0006\",\"description\":\"检测到\\\"203.0.113.31\\\"正在对本机进行远程RDP爆破\",\"description_i18n\":{\"zh_CN\":\"检测到\\\"203.0.113.31\\\"正在对本机进行远程RDP爆破\",\"zh_TW\":\"偵測到\\\"203.0.113.31\\\"正在對本機進行遠端RDP爆破\",\"en_US\":\"Detected that \\\"203.0.113.31\\\" is performing remote RDP brute force on this machine\"},\"technique\":\"Brute Force\",\"tactic\":\"Credential Access\",\"create_time\":1727060095000,\"status\":0,\"rule_id\":\"41.0.0198\",\"process_details\":[{\"process_name\":\"svchost.exe\",\"process_id\":\"784\",\"process_md5\":\"7469cc568ad6821fd9d925542730a7d8\",\"process_path\":\"C:\\\\Windows\\\\System32\\\\svchost.exe\",\"process_sign\":\"Microsoft Windows Publisher\",\"process_command_line\":\"C:\\\\WINDOWS\\\\System32\\\\svchost.exe -k NetworkService -s TermService\",\"process_create_time\":0,\"process_terminate_time\":0,\"process_guid\":\"7578323a1a41c3fd4532c3aac828551e\",\"process_parent_guid\":\"\",\"is_alert_trigger\":true}],\"ioc_alerts\":[],\"risky_source\":{}}" | 由原始日志接入层保存，不由 OML 拼装 |
| `platform_context.ingest_time` | `ingest_time` | 1727060096001 | 由平台上下文提供 |
| `platform_context.parse_time` | `parse_time` | 1727060096120 | 由平台上下文提供 |
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
| `platform_context.enrichment.victim.asset.name` | `target_host` | "DESKTOP-NU779RJ" | 由平台上下文提供 |
| `constant.qax` | `observer_vendor` | "qax" | 使用平台/映射规则常量 qax |
| `constant.tianqing` | `observer_product` | "tianqing" | 使用平台/映射规则常量 tianqing |
| `wpl.alert_name` | `source_finding_title` | "检测到远程RDP爆破" | 由 WPL 字段 alert_name 投影或转换后赋值 |
| `wpl.severity` | `source_finding_severity` | "2" | 由 WPL 字段 severity 投影或转换后赋值 |
| `wpl.category_id` | `source_finding_category` | "801" | 由 WPL 字段 category_id 投影或转换后赋值 |
| `wpl.rule_id` | `source_finding_signature_id` | "41.0.0198" | 由 WPL 字段 rule_id 投影或转换后赋值 |
| `wpl.alert_id` | `source_finding_original_id` | "2897526172445364727" | 由 WPL 字段 alert_id 投影或转换后赋值 |
| `derived.entity_ref(host, wpl.asset_id)` | `roles.target.ref_id` | "host_2868257359929541780" | 按确定性规则 entity_ref(host, wpl.asset_id) 派生 |
| `constant.host` | `roles.target.entity_type` | "host" | 使用平台/映射规则常量 host |
| `platform_context.enrichment.victim.asset.id` | `roles.target.resource.id` | "2868257359929541780" | 由平台上下文提供 |
| `platform_context.enrichment.victim.asset.name` | `roles.target.resource.name` | "DESKTOP-NU779RJ" | 由平台上下文提供 |
| `platform_asset_type` | `roles.target.resource.type` | "terminal" | 平台资产类型结果；本样例为 terminal，不是 WPL 原始字段 |
| `platform_context.enrichment.victim.asset.system_id` | `roles.target.resource.system.id` | "SYS-005" | 由平台上下文提供 |
| `platform_context.enrichment.victim.asset.system_name` | `roles.target.resource.system.name` | "审计系统" | 由平台上下文提供 |
| `platform_context.enrichment.victim.asset.company_name` | `roles.target.resource.organization.name` | "示例集团安全部" | 由平台上下文提供 |
| `constant.tianqing` | `roles.observer.product.name` | "tianqing" | 使用平台/映射规则常量 tianqing |
| `constant.qax` | `roles.observer.device.vendor` | "qax" | 使用平台/映射规则常量 qax |
| `derived.entity_ref(process, wpl.process_details[0].process_guid)` | `roles.related[0].ref_id` | "process_7578323a1a41c3fd4532c3aac828551e" | 按确定性规则 entity_ref(process, wpl.process_details[0].process_guid) 派生 |
| `constant.process` | `roles.related[0].entity_type` | "process" | 使用平台/映射规则常量 process |
| `constant.alert_trigger_process` | `roles.related[0].relation_type` | "alert_trigger_process" | 使用平台/映射规则常量 alert_trigger_process |
| `platform_context.enrichment.communication_direction` | `facets.network.direction` | "L2L" | 由平台上下文提供 |
| `wpl.alert_id` | `source_finding.original_id` | "2897526172445364727" | 由 WPL 字段 alert_id 投影或转换后赋值 |
| `assembly.one_finding_per_wpl_alert` | `source_finding.count` | 1 | 当前一条 WPL 告警装配一个 finding，因此固定为 1 |
| `category_dictionary(wpl.category_id)` | `source_finding.category.original.name` | "横向渗透攻击" | 通过平台告警分类字典将 WPL category_id=801 富化为“横向渗透攻击” |
| `category_dictionary(wpl.category_id)` | `source_finding.category.normalized.level1.code` | "101" | 通过平台告警分类字典将 category_id=801 归一为 101 |
| `category_dictionary(wpl.category_id)` | `source_finding.category.normalized.level1.name` | "攻击利用" | 通过平台告警分类字典将 category_id=801 归一为“攻击利用” |
| `category_dictionary(wpl.category_id)` | `source_finding.category.normalized.level2.code` | "101999" | 通过平台告警分类字典将 category_id=801 归一为 101999 |
| `category_dictionary(wpl.category_id)` | `source_finding.category.normalized.level2.name` | "其他类攻击利用" | 通过平台告警分类字典将 category_id=801 归一为“其他类攻击利用” |
| `platform_context.enrichment.attacker.ip` | `source_finding.attacker.endpoint.ipv4` | "203.0.113.31" | 由平台上下文提供 |
| `platform_context.enrichment.attacker.geo.continent` | `source_finding.attacker.geo.continent.name` | "北美洲" | 由平台上下文提供 |
| `platform_context.enrichment.attacker.geo.country_code` | `source_finding.attacker.geo.country.code` | "US" | 由平台上下文提供 |
| `platform_context.enrichment.attacker.geo.country_name` | `source_finding.attacker.geo.country.name` | "美国" | 由平台上下文提供 |
| `platform_context.enrichment.attacker.geo.province_name` | `source_finding.attacker.geo.region.name` | "California" | 由平台上下文提供 |
| `platform_context.enrichment.attacker.geo.city_name` | `source_finding.attacker.geo.city.name` | "Mountain View" | 由平台上下文提供 |
| `platform_context.enrichment.attacker.geo.latitude` | `source_finding.attacker.geo.coordinates.latitude` | 37.422 | 由平台上下文提供 |
| `platform_context.enrichment.attacker.geo.longitude` | `source_finding.attacker.geo.coordinates.longitude` | -122.085 | 由平台上下文提供 |
| `platform_context.enrichment.attacker.asset.id` | `source_finding.attacker.resource.id` | "AST-0008" | 由平台上下文提供 |
| `platform_context.enrichment.attacker.asset.name` | `source_finding.attacker.resource.name` | "攻击源终端-01" | 由平台上下文提供 |
| `platform_context.enrichment.attacker.asset.type` | `source_finding.attacker.resource.type` | "terminal" | 由平台上下文提供 |
| `platform_context.enrichment.attacker.asset.system_id` | `source_finding.attacker.resource.system.id` | "SYS-004" | 由平台上下文提供 |
| `platform_context.enrichment.attacker.asset.system_name` | `source_finding.attacker.resource.system.name` | "财务系统" | 由平台上下文提供 |
| `platform_context.enrichment.attacker.asset.company_name` | `source_finding.attacker.resource.organization.name` | "示例集团财务部" | 由平台上下文提供 |
| `constant.host` | `source_finding.victim.type` | "host" | 使用平台/映射规则常量 host |
| `platform_context.enrichment.victim.ip` | `source_finding.victim.endpoint.ip` | "198.51.100.211" | 由平台上下文提供 |
| `platform_context.enrichment.victim.ip` | `source_finding.victim.endpoint.ipv4` | "198.51.100.211" | 由平台上下文提供 |
| `platform_context.enrichment.victim.geo.continent` | `source_finding.victim.geo.continent.name` | "北美洲" | 由平台上下文提供 |
| `platform_context.enrichment.victim.geo.country_code` | `source_finding.victim.geo.country.code` | "US" | 由平台上下文提供 |
| `platform_context.enrichment.victim.geo.country_name` | `source_finding.victim.geo.country.name` | "美国" | 由平台上下文提供 |
| `platform_context.enrichment.victim.geo.province_name` | `source_finding.victim.geo.region.name` | "Ohio" | 由平台上下文提供 |
| `platform_context.enrichment.victim.geo.city_name` | `source_finding.victim.geo.city.name` | "Columbus" | 由平台上下文提供 |
| `platform_context.enrichment.victim.geo.latitude` | `source_finding.victim.geo.coordinates.latitude` | 39.9819 | 由平台上下文提供 |
| `platform_context.enrichment.victim.geo.longitude` | `source_finding.victim.geo.coordinates.longitude` | -82.9048 | 由平台上下文提供 |
| `platform_context.enrichment.victim.asset.id` | `source_finding.victim.resource.id` | "2868257359929541780" | 由平台上下文提供 |
| `platform_context.enrichment.victim.asset.name` | `source_finding.victim.resource.name` | "DESKTOP-NU779RJ" | 由平台上下文提供 |
| `platform_context.enrichment.victim.asset.type` | `source_finding.victim.resource.type` | "terminal" | 由平台上下文提供 |
| `platform_context.enrichment.victim.asset.system_id` | `source_finding.victim.resource.system.id` | "SYS-005" | 由平台上下文提供 |
| `platform_context.enrichment.victim.asset.system_name` | `source_finding.victim.resource.system.name` | "审计系统" | 由平台上下文提供 |
| `platform_context.enrichment.victim.asset.company_name` | `source_finding.victim.resource.organization.name` | "示例集团安全部" | 由平台上下文提供 |
| `platform_context.enrichment.attack_direction` | `source_finding.attack_direction` | "L2L" | 由平台上下文提供 |
| `constant.sdm_schema_version` | `extensions.schema_version` | 2 | 使用平台/映射规则常量 sdm_schema_version |
| `derived.entity_ref(host, wpl.asset_id)` | `extensions.profiles.endpoint_asset.subject_ref.ref_id` | "host_2868257359929541780" | 按确定性规则 entity_ref(host, wpl.asset_id) 派生 |
| `platform_context.env_version` | `extensions.profiles.endpoint_asset.agent.version` | "edr-8.0" | 由平台上下文提供 |
| `platform_context.enrichment.provider` | `extensions.enrichments.provider` | "poc-fixture" | 由平台上下文提供 |
| `platform_context.enrichment.geo_database` | `extensions.enrichments.geo_database` | "poc-geo-20260805" | 由平台上下文提供 |
| `platform_context.enrichment.asset_database` | `extensions.enrichments.asset_database` | "poc-cmdb-20260805" | 由平台上下文提供 |
| `platform_context.enrichment.matched_at` | `extensions.enrichments.matched_at` | "2026-08-05T10:00:00+08:00" | 由平台上下文提供 |
| `platform_context.enrichment.match_method` | `extensions.enrichments.match_method` | "fixture" | 由平台上下文提供 |
| `platform_context.enrichment.confidence` | `extensions.enrichments.confidence` | "fixture" | 由平台上下文提供 |
| `platform_context.enrichment.network_boundary` | `extensions.enrichments.network_boundary` | "tenant-managed-boundary" | 由平台上下文提供 |

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
| `target_host` | `context` | `platform_context.enrichment.victim.asset.name` | `platform_context.enrichment.victim.asset.name` | `—` | confirmed；由平台上下文提供 |
| `observer_vendor` | `constant` | `constant.qax` | "qax" | `—` | confirmed；使用平台/映射规则常量 qax |
| `observer_product` | `constant` | `constant.tianqing` | "tianqing" | `—` | confirmed；使用平台/映射规则常量 tianqing |
| `roles.target.ref_id` | `derived` | `derived.entity_ref(host, wpl.asset_id)` | `derived.entity_ref(host, wpl.asset_id)` | `—` | confirmed；按确定性规则 entity_ref(host, wpl.asset_id) 派生 |
| `roles.target.entity_type` | `constant` | `constant.host` | "host" | `—` | confirmed；使用平台/映射规则常量 host |
| `roles.target.resource.id` | `context` | `platform_context.enrichment.victim.asset.id` | `platform_context.enrichment.victim.asset.id` | `—` | confirmed；由平台上下文提供 |
| `roles.target.resource.name` | `context` | `platform_context.enrichment.victim.asset.name` | `platform_context.enrichment.victim.asset.name` | `—` | confirmed；由平台上下文提供 |
| `roles.target.resource.type` | `derived` | `platform_asset_type` | `platform_asset_type` | `—` | confirmed；平台资产类型结果；本样例为 terminal，不是 WPL 原始字段 |
| `roles.target.resource.system.id` | `context` | `platform_context.enrichment.victim.asset.system_id` | `platform_context.enrichment.victim.asset.system_id` | `—` | confirmed；由平台上下文提供 |
| `roles.target.resource.system.name` | `context` | `platform_context.enrichment.victim.asset.system_name` | `platform_context.enrichment.victim.asset.system_name` | `—` | confirmed；由平台上下文提供 |
| `roles.target.resource.organization.name` | `context` | `platform_context.enrichment.victim.asset.company_name` | `platform_context.enrichment.victim.asset.company_name` | `—` | confirmed；由平台上下文提供 |
| `roles.observer.product.name` | `constant` | `constant.tianqing` | "tianqing" | `—` | confirmed；使用平台/映射规则常量 tianqing |
| `roles.observer.device.vendor` | `constant` | `constant.qax` | "qax" | `—` | confirmed；使用平台/映射规则常量 qax |
| `roles.related[0].ref_id` | `derived` | `derived.entity_ref(process, wpl.process_details[0].process_guid)` | `derived.entity_ref(process, wpl.process_details[0].process_guid)` | `—` | confirmed；按确定性规则 entity_ref(process, wpl.process_details[0].process_guid) 派生 |
| `roles.related[0].entity_type` | `constant` | `constant.process` | "process" | `—` | confirmed；使用平台/映射规则常量 process |
| `roles.related[0].relation_type` | `constant` | `constant.alert_trigger_process` | "alert_trigger_process" | `—` | confirmed；使用平台/映射规则常量 alert_trigger_process |
| `facets.network.direction` | `context` | `platform_context.enrichment.communication_direction` | `platform_context.enrichment.communication_direction` | `—` | confirmed；由平台上下文提供 |
| `source_finding.count` | `derived` | `assembly.one_finding_per_wpl_alert` | `assembly.one_finding_per_wpl_alert` | `—` | confirmed；当前一条 WPL 告警装配一个 finding，因此固定为 1 |
| `source_finding.attacker.endpoint.ipv4` | `context` | `platform_context.enrichment.attacker.ip` | `platform_context.enrichment.attacker.ip` | `—` | confirmed；由平台上下文提供 |
| `source_finding.attacker.geo.continent.name` | `context` | `platform_context.enrichment.attacker.geo.continent` | `platform_context.enrichment.attacker.geo.continent` | `—` | confirmed；由平台上下文提供 |
| `source_finding.attacker.geo.country.code` | `context` | `platform_context.enrichment.attacker.geo.country_code` | `platform_context.enrichment.attacker.geo.country_code` | `—` | confirmed；由平台上下文提供 |
| `source_finding.attacker.geo.country.name` | `context` | `platform_context.enrichment.attacker.geo.country_name` | `platform_context.enrichment.attacker.geo.country_name` | `—` | confirmed；由平台上下文提供 |
| `source_finding.attacker.geo.region.name` | `context` | `platform_context.enrichment.attacker.geo.province_name` | `platform_context.enrichment.attacker.geo.province_name` | `—` | confirmed；由平台上下文提供 |
| `source_finding.attacker.geo.city.name` | `context` | `platform_context.enrichment.attacker.geo.city_name` | `platform_context.enrichment.attacker.geo.city_name` | `—` | confirmed；由平台上下文提供 |
| `source_finding.attacker.geo.coordinates.latitude` | `context` | `platform_context.enrichment.attacker.geo.latitude` | `platform_context.enrichment.attacker.geo.latitude` | `—` | confirmed；由平台上下文提供 |
| `source_finding.attacker.geo.coordinates.longitude` | `context` | `platform_context.enrichment.attacker.geo.longitude` | `platform_context.enrichment.attacker.geo.longitude` | `—` | confirmed；由平台上下文提供 |
| `source_finding.attacker.resource.id` | `context` | `platform_context.enrichment.attacker.asset.id` | `platform_context.enrichment.attacker.asset.id` | `—` | confirmed；由平台上下文提供 |
| `source_finding.attacker.resource.name` | `context` | `platform_context.enrichment.attacker.asset.name` | `platform_context.enrichment.attacker.asset.name` | `—` | confirmed；由平台上下文提供 |
| `source_finding.attacker.resource.type` | `context` | `platform_context.enrichment.attacker.asset.type` | `platform_context.enrichment.attacker.asset.type` | `—` | confirmed；由平台上下文提供 |
| `source_finding.attacker.resource.system.id` | `context` | `platform_context.enrichment.attacker.asset.system_id` | `platform_context.enrichment.attacker.asset.system_id` | `—` | confirmed；由平台上下文提供 |
| `source_finding.attacker.resource.system.name` | `context` | `platform_context.enrichment.attacker.asset.system_name` | `platform_context.enrichment.attacker.asset.system_name` | `—` | confirmed；由平台上下文提供 |
| `source_finding.attacker.resource.organization.name` | `context` | `platform_context.enrichment.attacker.asset.company_name` | `platform_context.enrichment.attacker.asset.company_name` | `—` | confirmed；由平台上下文提供 |
| `source_finding.victim.type` | `constant` | `constant.host` | "host" | `—` | confirmed；使用平台/映射规则常量 host |
| `source_finding.victim.endpoint.ip` | `context` | `platform_context.enrichment.victim.ip` | `platform_context.enrichment.victim.ip` | `—` | confirmed；由平台上下文提供 |
| `source_finding.victim.endpoint.ipv4` | `context` | `platform_context.enrichment.victim.ip` | `platform_context.enrichment.victim.ip` | `—` | confirmed；由平台上下文提供 |
| `source_finding.victim.geo.continent.name` | `context` | `platform_context.enrichment.victim.geo.continent` | `platform_context.enrichment.victim.geo.continent` | `—` | confirmed；由平台上下文提供 |
| `source_finding.victim.geo.country.code` | `context` | `platform_context.enrichment.victim.geo.country_code` | `platform_context.enrichment.victim.geo.country_code` | `—` | confirmed；由平台上下文提供 |
| `source_finding.victim.geo.country.name` | `context` | `platform_context.enrichment.victim.geo.country_name` | `platform_context.enrichment.victim.geo.country_name` | `—` | confirmed；由平台上下文提供 |
| `source_finding.victim.geo.region.name` | `context` | `platform_context.enrichment.victim.geo.province_name` | `platform_context.enrichment.victim.geo.province_name` | `—` | confirmed；由平台上下文提供 |
| `source_finding.victim.geo.city.name` | `context` | `platform_context.enrichment.victim.geo.city_name` | `platform_context.enrichment.victim.geo.city_name` | `—` | confirmed；由平台上下文提供 |
| `source_finding.victim.geo.coordinates.latitude` | `context` | `platform_context.enrichment.victim.geo.latitude` | `platform_context.enrichment.victim.geo.latitude` | `—` | confirmed；由平台上下文提供 |
| `source_finding.victim.geo.coordinates.longitude` | `context` | `platform_context.enrichment.victim.geo.longitude` | `platform_context.enrichment.victim.geo.longitude` | `—` | confirmed；由平台上下文提供 |
| `source_finding.victim.resource.id` | `context` | `platform_context.enrichment.victim.asset.id` | `platform_context.enrichment.victim.asset.id` | `—` | confirmed；由平台上下文提供 |
| `source_finding.victim.resource.name` | `context` | `platform_context.enrichment.victim.asset.name` | `platform_context.enrichment.victim.asset.name` | `—` | confirmed；由平台上下文提供 |
| `source_finding.victim.resource.type` | `context` | `platform_context.enrichment.victim.asset.type` | `platform_context.enrichment.victim.asset.type` | `—` | confirmed；由平台上下文提供 |
| `source_finding.victim.resource.system.id` | `context` | `platform_context.enrichment.victim.asset.system_id` | `platform_context.enrichment.victim.asset.system_id` | `—` | confirmed；由平台上下文提供 |
| `source_finding.victim.resource.system.name` | `context` | `platform_context.enrichment.victim.asset.system_name` | `platform_context.enrichment.victim.asset.system_name` | `—` | confirmed；由平台上下文提供 |
| `source_finding.victim.resource.organization.name` | `context` | `platform_context.enrichment.victim.asset.company_name` | `platform_context.enrichment.victim.asset.company_name` | `—` | confirmed；由平台上下文提供 |
| `source_finding.attack_direction` | `context` | `platform_context.enrichment.attack_direction` | `platform_context.enrichment.attack_direction` | `—` | confirmed；由平台上下文提供 |
| `extensions.profiles.endpoint_asset.subject_ref.ref_id` | `derived` | `derived.entity_ref(host, wpl.asset_id)` | `derived.entity_ref(host, wpl.asset_id)` | `—` | confirmed；按确定性规则 entity_ref(host, wpl.asset_id) 派生 |
| `extensions.profiles.endpoint_asset.agent.version` | `context` | `platform_context.env_version` | `platform_context.env_version` | `—` | confirmed；由平台上下文提供 |
| `extensions.enrichments.provider` | `context` | `platform_context.enrichment.provider` | `platform_context.enrichment.provider` | `—` | confirmed；由平台上下文提供 |
| `extensions.enrichments.geo_database` | `context` | `platform_context.enrichment.geo_database` | `platform_context.enrichment.geo_database` | `—` | confirmed；由平台上下文提供 |
| `extensions.enrichments.asset_database` | `context` | `platform_context.enrichment.asset_database` | `platform_context.enrichment.asset_database` | `—` | confirmed；由平台上下文提供 |
| `extensions.enrichments.matched_at` | `context` | `platform_context.enrichment.matched_at` | `platform_context.enrichment.matched_at` | `—` | confirmed；由平台上下文提供 |
| `extensions.enrichments.match_method` | `context` | `platform_context.enrichment.match_method` | `platform_context.enrichment.match_method` | `—` | confirmed；由平台上下文提供 |
| `extensions.enrichments.confidence` | `context` | `platform_context.enrichment.confidence` | `platform_context.enrichment.confidence` | `—` | confirmed；由平台上下文提供 |
| `extensions.enrichments.network_boundary` | `context` | `platform_context.enrichment.network_boundary` | `platform_context.enrichment.network_boundary` | `—` | confirmed；由平台上下文提供 |
| `ingest_time` | `context` | `platform_context.ingest_time` | `read(ingest_time)` | `—` | confirmed；expected 事件中的平台上下文字段 |
| `parse_time` | `context` | `platform_context.parse_time` | `read(parse_time)` | `—` | confirmed；expected 事件中的平台上下文字段 |

### 5.2 Content 区

| SDM 字段 | 规则类型 | WPL 字段 | 映射/赋值 | 未命中 | 状态与证据 |
|---|---|---|---|---|---|
| `source_finding_title` | `projection` | `alert_name` | `wpl.alert_name` | `—` | confirmed；由 WPL 字段 alert_name 投影或转换后赋值 |
| `source_finding_severity` | `projection` | `severity` | `wpl.severity` | `—` | confirmed；由 WPL 字段 severity 投影或转换后赋值 |
| `source_finding_category` | `projection` | `category_id` | `wpl.category_id` | `—` | confirmed；由 WPL 字段 category_id 投影或转换后赋值 |
| `source_finding_signature_id` | `projection` | `rule_id` | `wpl.rule_id` | `—` | confirmed；由 WPL 字段 rule_id 投影或转换后赋值 |
| `source_finding_original_id` | `projection` | `alert_id` | `wpl.alert_id` | `—` | confirmed；由 WPL 字段 alert_id 投影或转换后赋值 |
| `source_finding.original_id` | `projection` | `alert_id` | `wpl.alert_id` | `—` | confirmed；由 WPL 字段 alert_id 投影或转换后赋值 |
| `source_finding.category.original.name` | `dictionary` | `category_id` | "801" -> "横向渗透攻击" | `preserve_in_extension_and_review` | partial；通过平台告警分类字典将 WPL category_id=801 富化为“横向渗透攻击” |
| `source_finding.category.normalized.level1.code` | `dictionary` | `category_id` | "801" -> "101" | `preserve_in_extension_and_review` | partial；通过平台告警分类字典将 category_id=801 归一为 101 |
| `source_finding.category.normalized.level1.name` | `dictionary` | `category_id` | "801" -> "攻击利用" | `preserve_in_extension_and_review` | partial；通过平台告警分类字典将 category_id=801 归一为“攻击利用” |
| `source_finding.category.normalized.level2.code` | `dictionary` | `category_id` | "801" -> "101999" | `preserve_in_extension_and_review` | partial；通过平台告警分类字典将 category_id=801 归一为 101999 |
| `source_finding.category.normalized.level2.name` | `dictionary` | `category_id` | "801" -> "其他类攻击利用" | `preserve_in_extension_and_review` | partial；通过平台告警分类字典将 category_id=801 归一为“其他类攻击利用” |
| `source_original_event_id` | `projection` | `alert_id` | "2897526172445364727" | `—` | confirmed；按当前 expected 事件结构映射 |
| `source_finding.title` | `projection` | `alert_name` | "检测到远程RDP爆破" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.target.host.id` | `projection` | `asset_id` | "2868257359929541780" | `—` | confirmed；按当前 expected 事件结构映射 |
| `extensions.profiles.endpoint_asset.ownership.organization.id` | `projection` | `asset_oid` | "2653788242175861718" | `—` | confirmed；按当前 expected 事件结构映射 |
| `source_finding.category.original.code` | `projection` | `category_id` | "801" | `—` | confirmed；按当前 expected 事件结构映射 |
| `extensions.profiles.endpoint_asset.agent.id` | `projection` | `client_id` | "0881058-dfb9a23257c64098060e699601b17217" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.target.host.name` | `projection` | `computer_name` | "DESKTOP-NU779RJ" | `—` | confirmed；按当前 expected 事件结构映射 |
| `occur_time` | `projection` | `create_time` | 1727060095000 | `—` | confirmed；按当前 expected 事件结构映射 |
| `source_finding.attacker.endpoint.ip` | `projection` | `des_ip` | "203.0.113.31" | `—` | confirmed；仅对已确认的 RDP 爆破类别解释为攻击端 IP；其他类别不得按字段位置套用 |
| `source_finding.description` | `projection` | `description_i18n/zh_CN` | "检测到\"203.0.113.31\"正在对本机进行远程RDP爆破" | `—` | confirmed；按当前 expected 事件结构映射 |
| `extensions.profiles.endpoint_asset.ownership.group.id` | `projection` | `gid` | "4f9c3833b800d1f7" | `—` | confirmed；按当前 expected 事件结构映射 |
| `extensions.profiles.endpoint_asset.ownership.group.name` | `projection` | `group_name` | "未分组终端" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.target.host.ip` | `projection` | `ip` | "198.51.100.211" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.target.host.mac` | `projection` | `mac` | "00:00:5E:00:53:23" | `—` | confirmed；按当前 expected 事件结构映射 |
| `extensions.profiles.endpoint_asset.agent.fingerprint_id` | `projection` | `mid` | "ec80b820d87d7cd7ac916240bcdff7215ae3118feaf070c13afbf06e69af4eb3" | `—` | confirmed；按当前 expected 事件结构映射 |
| `roles.related[0].process` | `projection` | `process_details` | {"name": "svchost.exe", "uid": "7578323a1a41c3fd4532c3aac828551e", "pid": "784", "path": "C:\\Windows\\System32\\svchost.exe", "cmdline": "C:\\WINDOWS\\System32\\svchost.exe -k NetworkService -s TermService", "file": {"hashes": {"md5": "7469cc568ad6821fd9d925542730a7d8"}, "signatures": [{"signer": "Microsoft Windows Publisher"}]}} | `—` | confirmed；告警触发进程对象；构造 related[0]，relation_type=alert_trigger_process，0 时间哨兵省略 |
| `source_finding.rule.signature_id` | `projection` | `rule_id` | "41.0.0198" | `—` | confirmed；按当前 expected 事件结构映射 |
| `source_finding.severity` | `projection` | `severity` | "2" | `—` | confirmed；按当前 expected 事件结构映射 |
| `source_finding.status` | `projection` | `status` | "0" | `—` | confirmed；按当前 expected 事件结构映射 |
| `source_finding.mitre.tactics[0]` | `projection` | `tactic` | "Credential Access" | `—` | confirmed；按当前 expected 事件结构映射 |
| `source_finding.mitre.techniques[0]` | `projection` | `technique` | "Brute Force" | `—` | confirmed；按当前 expected 事件结构映射 |
| `source_finding.mitre.technique_id` | `projection` | `technique_id` | "T1110" | `—` | confirmed；按当前 expected 事件结构映射 |

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
