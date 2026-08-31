# 天擎 WPL 原始字段清单与 SDM2.0 映射逻辑

> **[历史记录] 本记录涉及的大禹告警表 `ldm_alert` 已在 feature/sdm2-alert-model 分支从交付物删除（SDM2.0 告警模型重新设计中）。文中 `ldm_alert` 相关内容仅描述当时的执行事实，不代表当前交付范围。**

> 本文只描述 WPL 抽取结果和 SDM2.0 字段组合/映射逻辑，不包含 OML 实现。
> 来源：`/Users/cloney/Config/warp-rule/models/wpl/tianqing/parse.wpl`。
> 目标：中间版 `sdm2_log.sdm_event`（55 列 + 4 个 VARIANT 对象）。

## 1. 职责边界

| 层次 | 职责 | 本文处理 |
|---|---|---|
| WPL | 按原始 JSON 结构识别规则并抽取字段 | 列出原始路径、类型、别名、数组/嵌套结构 |
| OML | 组合、赋值、转换、富化和对象构造 | 只描述目标逻辑，不写实现 |
| Doris | 保存标准事件事实 | 对应 `sdm_event` 标量列和 VARIANT 列 |

## 2. 通用组合逻辑

### 2.1 事件身份与时间

- `event_id`：优先使用来源稳定事件编号，如 `event_id`、`alert_id`、`uuid`、`eid`；无稳定编号时，用租户、日志类型、事件时间和稳定来源字段确定性生成。
- `log_id`：保留来源日志记录编号；不得用当前时间或随机数代替。
- `raw_msg`：当前中间阶段直接保存源日志原文；后期建设独立原始日志存储后，再从事件表分离原文并引入引用字段。
- `occur_time`：从 `event_date_creation`、`create_time`、`timestamp`、`event_time`、`attack_time`、`file_alarm_time`、`operation_time`、`start_time` 等候选中按规则选择最具体事件时间。
- `ingest_time`、`parse_time`：由平台处理阶段生成；`schema_version=1`，`mapping_id` 按日志类型保持稳定。

### 2.2 角色与对象

- `source_*`：主动发起行为的 IP、用户、主机、进程；优先使用 `src_*`、`source_*`、`process_user` 等事实字段。
- `target_*`：被访问、被修改、被创建或被检测的 IP、主机、用户、域名、文件；优先使用 `dst_*`、`target_*`、`file_*`、`virus_*`。
- `carrier_*`：承载行为的进程、协议、会话和命令行；优先使用 `process_*`、`network_protocol`、`process_command_line`、`process_guid`。
- `observer_*` 与设备字段：天擎产品、厂商、终端名称、终端管理 IP、MAC、MID、资产 ID 等观察上下文。
- `roles`：保存完整 source/target/carrier/observer 对象；不把 `attacker/victim` 直接当成 SDM source/target。

### 2.3 事件语义

- `log_type`：保留 WPL 规则的稳定日志类型。
- `event_type`：映射到受控 SDM 类型，不直接透传天擎 `type` 或 `event_type`。
- `operation`：表达具体动作，如 `open`、`close`、`exec`、`create`、`modify`、`delete`、`download`、`upload`。
- `outcome`：表达动作结果；处置动作写入 `source_alert_action` 或 `source_finding`，不与结果混用。
- `severity`：统一天擎等级；原始数值和转换依据保留在 `source_finding` 或 `extensions`。
- `event_category`：归一为 `auth`、`network`、`audit`、`system`、`alert`、`other`，不能直接写大禹数字分类。

### 2.4 来源检测与扩展

- `source_finding_*` / `source_finding`：承接天擎自身检测结论。
- `facets`：承接网络、HTTP、文件、进程、终端状态等查询维度对象。
- `extensions`：承接稳定且未进入标准列的天擎私有字段；不得复制完整原始 JSON 或完整 `raw_msg`。
- 大禹分类、平台告警状态、研判/处置字段不应伪装成日志标准字段；平台告警由后续 `ldm_alert` 链路生成。

### 2.5 WPL 与目标事件的字段缺口

- 当前 WPL 需要统一传递 `raw_msg`；`tenant_id`、`schema_version`、`mapping_id` 属于平台上下文或映射契约字段，由 OML/接入层补齐。
- `edr_alert_log` 经 `wpl-check` 实测可输出 `create_time`、`technique_id`、`tactic_id` 和完整嵌套 `process_details`；静态字段清单未完整反映 JSON 解析器的透传结果。当前真实缺口见样例目录的 `wpl-missing-fields.md`。
- 多数规则同时存在 `create_time`、`event_date_creation`、`timestamp` 等时间字段，必须按日志事实定义优先级，不能使用一个全局时间映射覆盖所有规则。
- WPL 的 `@ioc_alerts[0][0]`、`@group_info[0]` 是有损路径；如果后续需要完整 IOC、组信息或进程树，应把完整数组字段作为对象输入保留。

## 3. WPL 规则与原始字段

字段格式：`原始 JSON 路径` → `WPL 输出别名`（WPL 类型）。`(derived from ...)` 表示由父字段分组拆出的字段。

### 3.1 `ignore`

- `log_type`：`ignore`
- 描述：未声明
- 规则过滤：`f_chars_in(type, [login_logout, system_runtime_log])`
- 建议事件语义：忽略，不生成 SDM 事件
- 抽取字段数（按别名去重）：0

| 原始路径 | 输出别名 | WPL 类型 |
|---|---|---|
| 无业务字段（仅用于忽略或路由过滤） | — | — |

#### 组合与映射要点

- 本规则组合输入候选：身份候选：待从样例确认；时间候选：待从样例确认；主动方候选：待从样例确认；目标方候选：待从样例确认；载体候选：待从样例确认；检测候选：待从样例确认。
- 从本节字段选择稳定 ID 和事件发生时间；不能直接使用规则名作为 `event_id`。
- 按事实将终端、进程、网络、文件和用户放入 `roles`；不沿用大禹 `attacker/victim` 作为标准角色。
- 将天擎类型、状态、结果转换为受控 `event_type`、`operation`、`outcome`、`severity`；原始值保留在 `source_finding` 或 `extensions`。
- 低频字段进入 `facets`/`extensions` 前必须确认稳定性和调查价值。

### 3.2 `ignore_other`

- `log_type`：`ignore_other`
- 描述：未声明
- 规则过滤：`f_chars_in(syslog_topic, [information_gathering_client_summary_result])`
- 建议事件语义：忽略，不生成 SDM 事件
- 抽取字段数（按别名去重）：0

| 原始路径 | 输出别名 | WPL 类型 |
|---|---|---|
| 无业务字段（仅用于忽略或路由过滤） | — | — |

#### 组合与映射要点

- 本规则组合输入候选：身份候选：待从样例确认；时间候选：待从样例确认；主动方候选：待从样例确认；目标方候选：待从样例确认；载体候选：待从样例确认；检测候选：待从样例确认。
- 从本节字段选择稳定 ID 和事件发生时间；不能直接使用规则名作为 `event_id`。
- 按事实将终端、进程、网络、文件和用户放入 `roles`；不沿用大禹 `attacker/victim` 作为标准角色。
- 将天擎类型、状态、结果转换为受控 `event_type`、`operation`、`outcome`、`severity`；原始值保留在 `source_finding` 或 `extensions`。
- 低频字段进入 `facets`/`extensions` 前必须确认稳定性和调查价值。

### 3.3 `edr_alert_log`

- `log_type`：`edr_alert_log`
- 描述：天擎终端威胁告警日志
- 规则过滤：`f_chars_has(type, edr_alert)`
- 建议事件语义：来源检测/安全告警事件；event_category 候选为 alert
- 抽取字段数（按别名去重）：34

| 原始路径 | 输出别名 | WPL 类型 |
|---|---|---|
| `gid` | `gid` | `chars` |
| `group_name` | `group_name` | `chars` |
| `mid` | `mid` | `chars` |
| `mac` | `mac` | `chars` |
| `computer_name` | `computer_name` | `chars` |
| `report_ip` | `report_ip` | `chars` |
| `ip` | `ip` | `chars` |
| `client_id` | `client_id` | `chars` |
| `asset_oid` | `asset_oid` | `chars` |
| `asset_id` | `asset_id` | `chars` |
| `client_login_user` | `client_login_user` | `chars` |
| `description` | `description` | `chars` |
| `(derived from tmp1)` | `tmp1` | `chars` |
| `(derived from des_ip)` | `des_ip` | `chars` |
| `(derived from tmp2)` | `tmp2` | `chars` |
| `(derived from des_user)` | `des_user` | `chars` |
| `technique` | `technique` | `chars` |
| `tactic` | `tactic` | `chars` |
| `category_id` | `category_id` | `chars` |
| `severity` | `severity` | `chars` |
| `status` | `status` | `chars` |
| `compromise_status_cd` | `compromise_status_cd` | `chars` |
| `rule_id` | `rule_id` | `chars` |
| `process_details` | `process_details` | `array` |
| `ioc_alerts[0][0]/matched_ioc` | `ioc_value` | `chars` |
| `ioc_alerts[0][0]/malicious_family` | `malicious_family` | `chars` |
| `ioc_alerts[0][0]/malicious_type` | `malicious_type` | `chars` |
| `ioc_alerts[0][0]/kill_chain` | `origin_killchain` | `chars` |
| `ioc_alerts[0][0]/protocol` | `protocol` | `chars` |
| `alert_id` | `alert_id` | `chars` |
| `custom_group_paths` | `custom_group_paths` | `chars` |
| `risky_source` | `risky_source` | `chars` |
| `alert_name/zh_CN` | `alert_name` | `chars` |
| `log_type` | `other_type` | `chars` |

#### 组合与映射要点

- 本规则组合输入候选：身份候选：`alert_id`, `asset_id`；时间候选：`create_time`；来源 Finding 主张候选：`des_ip`, `risky_source/*`；受影响目标候选：`computer_name`, `ip`, `asset_id`；关联进程候选：`process_details`；检测候选：`alert_name`, `description_i18n/zh_CN`, `technique`, `tactic`, `category_id`, `rule_id`, `status`。
- 从本节字段选择稳定 ID 和事件发生时间；不能直接使用规则名作为 `event_id`。
- 按事实将终端、进程、网络、文件和用户放入 `roles`；不沿用大禹 `attacker/victim` 作为标准角色。
- 将天擎类型、状态、结果转换为受控 `event_type`、`operation`、`outcome`、`severity`；原始值保留在 `source_finding` 或 `extensions`。
- 低频字段进入 `facets`/`extensions` 前必须确认稳定性和调查价值。

### 3.4 `edr_antivirus_virus`

- `log_type`：`edr_antivirus_virus`
- 描述：天擎病毒查杀日志
- 规则过滤：`f_chars_has(syslog_topic, antivirus_virus)`
- 建议事件语义：待确认事件语义
- 抽取字段数（按别名去重）：43

| 原始路径 | 输出别名 | WPL 类型 |
|---|---|---|
| `file_alarm_time` | `file_alarm_time` | `time_timestamp` |
| `client_id` | `client_id` | `chars` |
| `guid` | `guid` | `chars` |
| `trigger_mode` | `trigger_mode` | `digit` |
| `virus_name` | `virus_name` | `chars` |
| `virus_type` | `virus_type` | `chars` |
| `file_path` | `file_path` | `chars` |
| `file_create_time` | `file_create_time` | `time_timestamp` |
| `md5` | `md5` | `chars` |
| `severity` | `severity` | `chars` |
| `sha1` | `sha1` | `chars` |
| `result` | `result` | `chars` |
| `need_reboot` | `need_reboot` | `chars` |
| `scanners` | `scanners` | `chars` |
| `client_info/report_ip` | `report_ip` | `chars` |
| `client_info/os` | `os` | `chars` |
| `client_info/create_time` | `create_time` | `time` |
| `client_info/os_version/release_id` | `release_id` | `chars` |
| `client_info/os_version/build_version` | `build_version` | `chars` |
| `client_info/os_version/main` | `main` | `chars` |
| `client_info/os_version/describe` | `describe` | `chars` |
| `client_info/mid` | `mid` | `chars` |
| `client_info/sys_space` | `sys_space` | `chars` |
| `client_info/core_number` | `core_number` | `digit` |
| `client_info/login_account` | `login_account` | `chars` |
| `client_info/mac` | `mac` | `chars` |
| `client_info/memory_size` | `memory_size` | `chars` |
| `client_info/update_time` | `update_time` | `time` |
| `client_info/ie_version` | `ie_version` | `chars` |
| `client_info/computer_working_group` | `computer_working_group` | `chars` |
| `client_info/domain` | `domain` | `chars` |
| `client_info/name` | `name` | `chars` |
| `client_info/os_bit` | `os_bit` | `chars` |
| `client_info/nic_list` | `nic_list` | `array` |
| `client_info/report_ipv6` | `report_ipv6` | `chars` |
| `client_info/state` | `state` | `chars` |
| `client_info/activation` | `activation` | `chars` |
| `client_info/system_language` | `system_language` | `chars` |
| `group_info[0]/node_type` | `node_type` | `chars` |
| `group_info[0]/tree_id` | `tree_id` | `chars` |
| `group_info[0]/node_name` | `node_name` | `chars` |
| `group_info[0]/oid` | `oid` | `chars` |
| `group_info[0]/node_id` | `node_id` | `chars` |

#### 组合与映射要点

- 本规则组合输入候选：身份候选：`guid`；时间候选：`create_time`, `file_alarm_time`；主动方候选：待从样例确认；目标方候选：`file_path`, `virus_name`；载体候选：待从样例确认；检测候选：`result`。
- 从本节字段选择稳定 ID 和事件发生时间；不能直接使用规则名作为 `event_id`。
- 按事实将终端、进程、网络、文件和用户放入 `roles`；不沿用大禹 `attacker/victim` 作为标准角色。
- 将天擎类型、状态、结果转换为受控 `event_type`、`operation`、`outcome`、`severity`；原始值保留在 `source_finding` 或 `extensions`。
- 低频字段进入 `facets`/`extensions` 前必须确认稳定性和调查价值。

### 3.5 `edr_antivirus_scan`

- `log_type`：`edr_antivirus_scan`
- 描述：天擎查杀任务日志
- 规则过滤：`f_chars_has(syslog_topic, antivirus_scan)`
- 建议事件语义：待确认事件语义
- 抽取字段数（按别名去重）：44

| 原始路径 | 输出别名 | WPL 类型 |
|---|---|---|
| `client_id` | `client_id` | `chars` |
| `guid` | `guid` | `chars` |
| `trigger_mode` | `trigger_mode` | `digit` |
| `scan_type` | `scan_type` | `chars` |
| `start_time` | `start_time` | `time_timestamp` |
| `virus_name` | `virus_name` | `chars` |
| `virus_type` | `virus_type` | `chars` |
| `file_path` | `file_path` | `chars` |
| `file_create_time` | `file_create_time` | `chars` |
| `file_alarm_time` | `file_alarm_time` | `chars` |
| `md5` | `md5` | `chars` |
| `sha1` | `sha1` | `chars` |
| `result` | `result` | `chars` |
| `need_reboot` | `need_reboot` | `chars` |
| `scanners` | `scanners` | `chars` |
| `client_info/report_ip` | `report_ip` | `chars` |
| `client_info/os` | `os` | `chars` |
| `client_info/create_time` | `create_time` | `time` |
| `client_info/os_version/release_id` | `release_id` | `chars` |
| `client_info/os_version/build_version` | `build_version` | `chars` |
| `client_info/os_version/main` | `main` | `chars` |
| `client_info/os_version/describe` | `describe` | `chars` |
| `client_info/mid` | `mid` | `chars` |
| `client_info/sys_space` | `sys_space` | `chars` |
| `client_info/core_number` | `core_number` | `digit` |
| `client_info/login_account` | `login_account` | `chars` |
| `client_info/mac` | `mac` | `chars` |
| `client_info/memory_size` | `memory_size` | `chars` |
| `client_info/update_time` | `update_time` | `time` |
| `client_info/ie_version` | `ie_version` | `chars` |
| `client_info/computer_working_group` | `computer_working_group` | `chars` |
| `client_info/domain` | `domain` | `chars` |
| `client_info/name` | `name` | `chars` |
| `client_info/os_bit` | `os_bit` | `chars` |
| `client_info/nic_list` | `nic_list` | `array` |
| `client_info/report_ipv6` | `report_ipv6` | `chars` |
| `client_info/state` | `state` | `chars` |
| `client_info/activation` | `activation` | `chars` |
| `client_info/system_language` | `system_language` | `chars` |
| `group_info/node_type` | `node_type` | `chars` |
| `group_info/tree_id` | `tree_id` | `chars` |
| `group_info/node_name` | `node_name` | `chars` |
| `group_info/oid` | `oid` | `chars` |
| `group_info/node_id` | `node_id` | `chars` |

#### 组合与映射要点

- 本规则组合输入候选：身份候选：`guid`；时间候选：`create_time`, `file_alarm_time`, `start_time`；主动方候选：待从样例确认；目标方候选：`file_path`, `virus_name`；载体候选：待从样例确认；检测候选：`result`。
- 从本节字段选择稳定 ID 和事件发生时间；不能直接使用规则名作为 `event_id`。
- 按事实将终端、进程、网络、文件和用户放入 `roles`；不沿用大禹 `attacker/victim` 作为标准角色。
- 将天擎类型、状态、结果转换为受控 `event_type`、`operation`、`outcome`、`severity`；原始值保留在 `source_finding` 或 `extensions`。
- 低频字段进入 `facets`/`extensions` 前必须确认稳定性和调查价值。

### 3.6 `edr_attack_protection`

- `log_type`：`edr_attack_protection`
- 描述：天擎攻击防护日志
- 规则过滤：`f_chars_has(syslog_topic, attack_protection_log)`
- 建议事件语义：来源检测/安全告警事件；event_category 候选为 alert
- 抽取字段数（按别名去重）：44

| 原始路径 | 输出别名 | WPL 类型 |
|---|---|---|
| `client_id` | `client_id` | `chars` |
| `guid` | `guid` | `chars` |
| `trigger_mode` | `trigger_mode` | `digit` |
| `virus_name` | `virus_name` | `chars` |
| `virus_type` | `virus_type` | `chars` |
| `file_path` | `file_path` | `chars` |
| `file_create_time` | `file_create_time` | `chars` |
| `file_alarm_time` | `file_alarm_time` | `chars` |
| `attack_time` | `attack_time` | `time_timestamp` |
| `md5` | `md5` | `chars` |
| `sha1` | `sha1` | `chars` |
| `result` | `result` | `chars` |
| `need_reboot` | `need_reboot` | `chars` |
| `attack_type` | `attack_type` | `chars` |
| `scanners` | `scanners` | `chars` |
| `client_info/report_ip` | `report_ip` | `chars` |
| `client_info/os` | `os` | `chars` |
| `client_info/create_time` | `create_time` | `time` |
| `client_info/os_version/release_id` | `release_id` | `chars` |
| `client_info/os_version/build_version` | `build_version` | `chars` |
| `client_info/os_version/main` | `main` | `chars` |
| `client_info/os_version/describe` | `describe` | `chars` |
| `client_info/mid` | `mid` | `chars` |
| `client_info/sys_space` | `sys_space` | `chars` |
| `client_info/core_number` | `core_number` | `digit` |
| `client_info/login_account` | `login_account` | `chars` |
| `client_info/mac` | `mac` | `chars` |
| `client_info/memory_size` | `memory_size` | `chars` |
| `client_info/update_time` | `update_time` | `time` |
| `client_info/ie_version` | `ie_version` | `chars` |
| `client_info/computer_working_group` | `computer_working_group` | `chars` |
| `client_info/domain` | `domain` | `chars` |
| `client_info/name` | `name` | `chars` |
| `client_info/os_bit` | `os_bit` | `chars` |
| `client_info/nic_list` | `nic_list` | `array` |
| `client_info/report_ipv6` | `report_ipv6` | `chars` |
| `client_info/state` | `state` | `chars` |
| `client_info/activation` | `activation` | `chars` |
| `client_info/system_language` | `system_language` | `chars` |
| `group_info/node_type` | `node_type` | `chars` |
| `group_info/tree_id` | `tree_id` | `chars` |
| `group_info/node_name` | `node_name` | `chars` |
| `group_info/oid` | `oid` | `chars` |
| `group_info/node_id` | `node_id` | `chars` |

#### 组合与映射要点

- 本规则组合输入候选：身份候选：`guid`；时间候选：`create_time`, `attack_time`, `file_alarm_time`；主动方候选：待从样例确认；目标方候选：`file_path`, `virus_name`；载体候选：待从样例确认；检测候选：`result`。
- 从本节字段选择稳定 ID 和事件发生时间；不能直接使用规则名作为 `event_id`。
- 按事实将终端、进程、网络、文件和用户放入 `roles`；不沿用大禹 `attacker/victim` 作为标准角色。
- 将天擎类型、状态、结果转换为受控 `event_type`、`operation`、`outcome`、`severity`；原始值保留在 `source_finding` 或 `extensions`。
- 低频字段进入 `facets`/`extensions` 前必须确认稳定性和调查价值。

### 3.7 `edr_system_protection`

- `log_type`：`edr_system_protection`
- 描述：天擎系统防护日志
- 规则过滤：`f_chars_has(syslog_topic, system_protection_log)`
- 建议事件语义：来源检测/安全告警事件；event_category 候选为 alert
- 抽取字段数（按别名去重）：43

| 原始路径 | 输出别名 | WPL 类型 |
|---|---|---|
| `client_id` | `client_id` | `chars` |
| `guid` | `guid` | `chars` |
| `trigger_mode` | `trigger_mode` | `digit` |
| `virus_name` | `virus_name` | `chars` |
| `virus_type` | `virus_type` | `chars` |
| `file_path` | `file_path` | `chars` |
| `file_create_time` | `file_create_time` | `chars` |
| `file_alarm_time` | `file_alarm_time` | `chars` |
| `event_time` | `event_time` | `time_timestamp` |
| `md5` | `md5` | `chars` |
| `sha1` | `sha1` | `chars` |
| `result` | `result` | `chars` |
| `need_reboot` | `need_reboot` | `chars` |
| `scanners` | `scanners` | `chars` |
| `client_info/report_ip` | `report_ip` | `chars` |
| `client_info/os` | `os` | `chars` |
| `client_info/create_time` | `create_time` | `time` |
| `client_info/os_version/release_id` | `release_id` | `chars` |
| `client_info/os_version/build_version` | `build_version` | `chars` |
| `client_info/os_version/main` | `main` | `chars` |
| `client_info/os_version/describe` | `describe` | `chars` |
| `client_info/mid` | `mid` | `chars` |
| `client_info/sys_space` | `sys_space` | `chars` |
| `client_info/core_number` | `core_number` | `digit` |
| `client_info/login_account` | `login_account` | `chars` |
| `client_info/mac` | `mac` | `chars` |
| `client_info/memory_size` | `memory_size` | `chars` |
| `client_info/update_time` | `update_time` | `time` |
| `client_info/ie_version` | `ie_version` | `chars` |
| `client_info/computer_working_group` | `computer_working_group` | `chars` |
| `client_info/domain` | `domain` | `chars` |
| `client_info/name` | `name` | `chars` |
| `client_info/os_bit` | `os_bit` | `chars` |
| `client_info/nic_list` | `nic_list` | `array` |
| `client_info/report_ipv6` | `report_ipv6` | `chars` |
| `client_info/state` | `state` | `chars` |
| `client_info/activation` | `activation` | `chars` |
| `client_info/system_language` | `system_language` | `chars` |
| `group_info/node_type` | `node_type` | `chars` |
| `group_info/tree_id` | `tree_id` | `chars` |
| `group_info/node_name` | `node_name` | `chars` |
| `group_info/oid` | `oid` | `chars` |
| `group_info/node_id` | `node_id` | `chars` |

#### 组合与映射要点

- 本规则组合输入候选：身份候选：`guid`；时间候选：`create_time`, `event_time`, `file_alarm_time`；主动方候选：待从样例确认；目标方候选：`file_path`, `virus_name`；载体候选：待从样例确认；检测候选：`result`。
- 从本节字段选择稳定 ID 和事件发生时间；不能直接使用规则名作为 `event_id`。
- 按事实将终端、进程、网络、文件和用户放入 `roles`；不沿用大禹 `attacker/victim` 作为标准角色。
- 将天擎类型、状态、结果转换为受控 `event_type`、`operation`、`outcome`、`severity`；原始值保留在 `source_finding` 或 `extensions`。
- 低频字段进入 `facets`/`extensions` 前必须确认稳定性和调查价值。

### 3.8 `edr_webpage_protection`

- `log_type`：`edr_webpage_protection`
- 描述：天擎网页安全防护日志
- 规则过滤：`f_chars_has(syslog_topic, webpage_protection_log)`
- 建议事件语义：来源检测/安全告警事件；event_category 候选为 alert
- 抽取字段数（按别名去重）：44

| 原始路径 | 输出别名 | WPL 类型 |
|---|---|---|
| `client_id` | `client_id` | `chars` |
| `guid` | `guid` | `chars` |
| `trigger_mode` | `trigger_mode` | `digit` |
| `virus_name` | `virus_name` | `chars` |
| `virus_type` | `virus_type` | `chars` |
| `file_path` | `file_path` | `chars` |
| `file_create_time` | `file_create_time` | `chars` |
| `file_alarm_time` | `file_alarm_time` | `chars` |
| `event_time` | `event_time` | `time_timestamp` |
| `md5` | `md5` | `chars` |
| `sha1` | `sha1` | `chars` |
| `result` | `result` | `chars` |
| `need_reboot` | `need_reboot` | `chars` |
| `scanners` | `scanners` | `chars` |
| `visit_ip` | `visit_ip` | `chars` |
| `client_info/report_ip` | `report_ip` | `chars` |
| `client_info/os` | `os` | `chars` |
| `client_info/create_time` | `create_time` | `time` |
| `client_info/os_version/release_id` | `release_id` | `chars` |
| `client_info/os_version/build_version` | `build_version` | `chars` |
| `client_info/os_version/main` | `main` | `chars` |
| `client_info/os_version/describe` | `describe` | `chars` |
| `client_info/mid` | `mid` | `chars` |
| `client_info/sys_space` | `sys_space` | `chars` |
| `client_info/core_number` | `core_number` | `digit` |
| `client_info/login_account` | `login_account` | `chars` |
| `client_info/mac` | `mac` | `chars` |
| `client_info/memory_size` | `memory_size` | `chars` |
| `client_info/update_time` | `update_time` | `time` |
| `client_info/ie_version` | `ie_version` | `chars` |
| `client_info/computer_working_group` | `computer_working_group` | `chars` |
| `client_info/domain` | `domain` | `chars` |
| `client_info/name` | `name` | `chars` |
| `client_info/os_bit` | `os_bit` | `chars` |
| `client_info/nic_list` | `nic_list` | `array` |
| `client_info/report_ipv6` | `report_ipv6` | `chars` |
| `client_info/state` | `state` | `chars` |
| `client_info/activation` | `activation` | `chars` |
| `client_info/system_language` | `system_language` | `chars` |
| `group_info/node_type` | `node_type` | `chars` |
| `group_info/tree_id` | `tree_id` | `chars` |
| `group_info/node_name` | `node_name` | `chars` |
| `group_info/oid` | `oid` | `chars` |
| `group_info/node_id` | `node_id` | `chars` |

#### 组合与映射要点

- 本规则组合输入候选：身份候选：`guid`；时间候选：`create_time`, `event_time`, `file_alarm_time`；主动方候选：待从样例确认；目标方候选：`file_path`, `virus_name`；载体候选：待从样例确认；检测候选：`result`。
- 从本节字段选择稳定 ID 和事件发生时间；不能直接使用规则名作为 `event_id`。
- 按事实将终端、进程、网络、文件和用户放入 `roles`；不沿用大禹 `attacker/victim` 作为标准角色。
- 将天擎类型、状态、结果转换为受控 `event_type`、`operation`、`outcome`、`severity`；原始值保留在 `source_finding` 或 `extensions`。
- 低频字段进入 `facets`/`extensions` 前必须确认稳定性和调查价值。

### 3.9 `edr_firewall`

- `log_type`：`edr_firewall`
- 描述：天擎防火墙日志
- 规则过滤：`f_chars_has(syslog_topic, firewall)`
- 建议事件语义：网络事实事件；event_category 候选为 network
- 抽取字段数（按别名去重）：45

| 原始路径 | 输出别名 | WPL 类型 |
|---|---|---|
| `client_id` | `client_id` | `chars` |
| `guid` | `guid` | `chars` |
| `dst_ip` | `dst_ip` | `ip` |
| `src_ip` | `src_ip` | `ip` |
| `intercept_time` | `intercept_time` | `time_timestamp` |
| `trigger_mode` | `trigger_mode` | `digit` |
| `virus_name` | `virus_name` | `chars` |
| `virus_type` | `virus_type` | `chars` |
| `file_path` | `file_path` | `chars` |
| `file_create_time` | `file_create_time` | `chars` |
| `file_alarm_time` | `file_alarm_time` | `chars` |
| `md5` | `md5` | `chars` |
| `sha1` | `sha1` | `chars` |
| `result` | `result` | `chars` |
| `need_reboot` | `need_reboot` | `chars` |
| `scanners` | `scanners` | `chars` |
| `client_info/report_ip` | `report_ip` | `chars` |
| `client_info/os` | `os` | `chars` |
| `client_info/create_time` | `create_time` | `time` |
| `client_info/os_version/release_id` | `release_id` | `chars` |
| `client_info/os_version/build_version` | `build_version` | `chars` |
| `client_info/os_version/main` | `main` | `chars` |
| `client_info/os_version/describe` | `describe` | `chars` |
| `client_info/mid` | `mid` | `chars` |
| `client_info/sys_space` | `sys_space` | `chars` |
| `client_info/core_number` | `core_number` | `digit` |
| `client_info/login_account` | `login_account` | `chars` |
| `client_info/mac` | `mac` | `chars` |
| `client_info/memory_size` | `memory_size` | `chars` |
| `client_info/update_time` | `update_time` | `time` |
| `client_info/ie_version` | `ie_version` | `chars` |
| `client_info/computer_working_group` | `computer_working_group` | `chars` |
| `client_info/domain` | `domain` | `chars` |
| `client_info/name` | `name` | `chars` |
| `client_info/os_bit` | `os_bit` | `chars` |
| `client_info/nic_list` | `nic_list` | `array` |
| `client_info/report_ipv6` | `report_ipv6` | `chars` |
| `client_info/state` | `state` | `chars` |
| `client_info/activation` | `activation` | `chars` |
| `client_info/system_language` | `system_language` | `chars` |
| `group_info/node_type` | `node_type` | `chars` |
| `group_info/tree_id` | `tree_id` | `chars` |
| `group_info/node_name` | `node_name` | `chars` |
| `group_info/oid` | `oid` | `chars` |
| `group_info/node_id` | `node_id` | `chars` |

#### 组合与映射要点

- 本规则组合输入候选：身份候选：`guid`；时间候选：`create_time`, `file_alarm_time`；主动方候选：`src_ip`；目标方候选：`dst_ip`, `file_path`, `virus_name`；载体候选：待从样例确认；检测候选：`result`。
- 从本节字段选择稳定 ID 和事件发生时间；不能直接使用规则名作为 `event_id`。
- 按事实将终端、进程、网络、文件和用户放入 `roles`；不沿用大禹 `attacker/victim` 作为标准角色。
- 将天擎类型、状态、结果转换为受控 `event_type`、`operation`、`outcome`、`severity`；原始值保留在 `source_finding` 或 `extensions`。
- 低频字段进入 `facets`/`extensions` 前必须确认稳定性和调查价值。

### 3.10 `edr_baseline_check_result`

- `log_type`：`edr_baseline_check_result`
- 描述：天擎基线检查结果日志
- 规则过滤：`f_chars_has(syslog_topic, baseline_check_result)`
- 建议事件语义：资产/配置/状态事件；event_category 候选为 system 或 audit
- 抽取字段数（按别名去重）：43

| 原始路径 | 输出别名 | WPL 类型 |
|---|---|---|
| `client_id` | `client_id` | `chars` |
| `guid` | `guid` | `chars` |
| `trigger_mode` | `trigger_mode` | `digit` |
| `virus_name` | `virus_name` | `chars` |
| `virus_type` | `virus_type` | `chars` |
| `file_path` | `file_path` | `chars` |
| `file_create_time` | `file_create_time` | `chars` |
| `file_alarm_time` | `file_alarm_time` | `chars` |
| `md5` | `md5` | `chars` |
| `sha1` | `sha1` | `chars` |
| `op` | `op` | `digit` |
| `result` | `result` | `chars` |
| `need_reboot` | `need_reboot` | `chars` |
| `scanners` | `scanners` | `chars` |
| `client_info/report_ip` | `report_ip` | `chars` |
| `client_info/os` | `os` | `chars` |
| `client_info/create_time` | `create_time` | `time` |
| `client_info/os_version/release_id` | `release_id` | `chars` |
| `client_info/os_version/build_version` | `build_version` | `chars` |
| `client_info/os_version/main` | `main` | `chars` |
| `client_info/os_version/describe` | `describe` | `chars` |
| `client_info/mid` | `mid` | `chars` |
| `client_info/sys_space` | `sys_space` | `chars` |
| `client_info/core_number` | `core_number` | `digit` |
| `client_info/login_account` | `login_account` | `chars` |
| `client_info/mac` | `mac` | `chars` |
| `client_info/memory_size` | `memory_size` | `chars` |
| `client_info/update_time` | `update_time` | `time` |
| `client_info/ie_version` | `ie_version` | `chars` |
| `client_info/computer_working_group` | `computer_working_group` | `chars` |
| `client_info/domain` | `domain` | `chars` |
| `client_info/name` | `name` | `chars` |
| `client_info/os_bit` | `os_bit` | `chars` |
| `client_info/nic_list` | `nic_list` | `array` |
| `client_info/report_ipv6` | `report_ipv6` | `chars` |
| `client_info/state` | `state` | `chars` |
| `client_info/activation` | `activation` | `chars` |
| `client_info/system_language` | `system_language` | `chars` |
| `group_info[0]/node_type` | `node_type` | `chars` |
| `group_info[0]/tree_id` | `tree_id` | `chars` |
| `group_info[0]/node_name` | `node_name` | `chars` |
| `group_info[0]/oid` | `oid` | `chars` |
| `group_info[0]/node_id` | `node_id` | `chars` |

#### 组合与映射要点

- 本规则组合输入候选：身份候选：`guid`；时间候选：`create_time`, `file_alarm_time`；主动方候选：待从样例确认；目标方候选：`file_path`, `virus_name`；载体候选：待从样例确认；检测候选：`result`。
- 从本节字段选择稳定 ID 和事件发生时间；不能直接使用规则名作为 `event_id`。
- 按事实将终端、进程、网络、文件和用户放入 `roles`；不沿用大禹 `attacker/victim` 作为标准角色。
- 将天擎类型、状态、结果转换为受控 `event_type`、`operation`、`outcome`、`severity`；原始值保留在 `source_finding` 或 `extensions`。
- 低频字段进入 `facets`/`extensions` 前必须确认稳定性和调查价值。

### 3.11 `edr_baseline_check_detail`

- `log_type`：`edr_baseline_check_detail`
- 描述：天擎基线检查明细日志
- 规则过滤：`f_chars_has(syslog_topic, baseline_check_detail)`
- 建议事件语义：资产/配置/状态事件；event_category 候选为 system 或 audit
- 抽取字段数（按别名去重）：42

| 原始路径 | 输出别名 | WPL 类型 |
|---|---|---|
| `client_id` | `client_id` | `chars` |
| `guid` | `guid` | `chars` |
| `trigger_mode` | `trigger_mode` | `digit` |
| `virus_name` | `virus_name` | `chars` |
| `virus_type` | `virus_type` | `chars` |
| `file_path` | `file_path` | `chars` |
| `file_create_time` | `file_create_time` | `chars` |
| `file_alarm_time` | `file_alarm_time` | `chars` |
| `md5` | `md5` | `chars` |
| `sha1` | `sha1` | `chars` |
| `result` | `result` | `chars` |
| `need_reboot` | `need_reboot` | `chars` |
| `scanners` | `scanners` | `chars` |
| `client_info/report_ip` | `report_ip` | `chars` |
| `client_info/os` | `os` | `chars` |
| `client_info/create_time` | `create_time` | `time` |
| `client_info/os_version/release_id` | `release_id` | `chars` |
| `client_info/os_version/build_version` | `build_version` | `chars` |
| `client_info/os_version/main` | `main` | `chars` |
| `client_info/os_version/describe` | `describe` | `chars` |
| `client_info/mid` | `mid` | `chars` |
| `client_info/sys_space` | `sys_space` | `chars` |
| `client_info/core_number` | `core_number` | `digit` |
| `client_info/login_account` | `login_account` | `chars` |
| `client_info/mac` | `mac` | `chars` |
| `client_info/memory_size` | `memory_size` | `chars` |
| `client_info/update_time` | `update_time` | `time` |
| `client_info/ie_version` | `ie_version` | `chars` |
| `client_info/computer_working_group` | `computer_working_group` | `chars` |
| `client_info/domain` | `domain` | `chars` |
| `client_info/name` | `name` | `chars` |
| `client_info/os_bit` | `os_bit` | `chars` |
| `client_info/nic_list` | `nic_list` | `array` |
| `client_info/report_ipv6` | `report_ipv6` | `chars` |
| `client_info/state` | `state` | `chars` |
| `client_info/activation` | `activation` | `chars` |
| `client_info/system_language` | `system_language` | `chars` |
| `group_info[0]/node_type` | `node_type` | `chars` |
| `group_info[0]/tree_id` | `tree_id` | `chars` |
| `group_info[0]/node_name` | `node_name` | `chars` |
| `group_info[0]/oid` | `oid` | `chars` |
| `group_info[0]/node_id` | `node_id` | `chars` |

#### 组合与映射要点

- 本规则组合输入候选：身份候选：`guid`；时间候选：`create_time`, `file_alarm_time`；主动方候选：待从样例确认；目标方候选：`file_path`, `virus_name`；载体候选：待从样例确认；检测候选：`result`。
- 从本节字段选择稳定 ID 和事件发生时间；不能直接使用规则名作为 `event_id`。
- 按事实将终端、进程、网络、文件和用户放入 `roles`；不沿用大禹 `attacker/victim` 作为标准角色。
- 将天擎类型、状态、结果转换为受控 `event_type`、`operation`、`outcome`、`severity`；原始值保留在 `source_finding` 或 `extensions`。
- 低频字段进入 `facets`/`extensions` 前必须确认稳定性和调查价值。

### 3.12 `edr_process_log`

- `log_type`：`edr_process_log`
- 描述：天擎进程管理日志
- 规则过滤：`f_chars_has(syslog_topic, process_log)`
- 建议事件语义：进程/系统审计事件；event_category 候选为 audit
- 抽取字段数（按别名去重）：45

| 原始路径 | 输出别名 | WPL 类型 |
|---|---|---|
| `client_id` | `client_id` | `chars` |
| `guid` | `guid` | `chars` |
| `trigger_mode` | `trigger_mode` | `digit` |
| `virus_name` | `virus_name` | `chars` |
| `virus_type` | `virus_type` | `chars` |
| `file_path` | `file_path` | `chars` |
| `file_create_time` | `file_create_time` | `chars` |
| `file_alarm_time` | `file_alarm_time` | `chars` |
| `md5` | `md5` | `chars` |
| `sha1` | `sha1` | `chars` |
| `result` | `result` | `chars` |
| `need_reboot` | `need_reboot` | `chars` |
| `scanners` | `scanners` | `chars` |
| `client_info/report_ip` | `report_ip` | `chars` |
| `client_info/os` | `os` | `chars` |
| `client_info/create_time` | `create_time` | `time` |
| `client_info/os_version/release_id` | `release_id` | `chars` |
| `client_info/os_version/build_version` | `build_version` | `chars` |
| `client_info/os_version/main` | `main` | `chars` |
| `client_info/os_version/describe` | `describe` | `chars` |
| `client_info/mid` | `mid` | `chars` |
| `client_info/sys_space` | `sys_space` | `chars` |
| `client_info/core_number` | `core_number` | `digit` |
| `client_info/login_account` | `login_account` | `chars` |
| `client_info/mac` | `mac` | `chars` |
| `client_info/memory_size` | `memory_size` | `chars` |
| `client_info/update_time` | `update_time` | `time` |
| `client_info/ie_version` | `ie_version` | `chars` |
| `client_info/computer_working_group` | `computer_working_group` | `chars` |
| `client_info/domain` | `domain` | `chars` |
| `client_info/name` | `name` | `chars` |
| `client_info/os_bit` | `os_bit` | `chars` |
| `client_info/nic_list` | `nic_list` | `array` |
| `client_info/report_ipv6` | `report_ipv6` | `chars` |
| `client_info/state` | `state` | `chars` |
| `client_info/activation` | `activation` | `chars` |
| `client_info/system_language` | `system_language` | `chars` |
| `group_info[0]/node_type` | `node_type` | `chars` |
| `group_info[0]/tree_id` | `tree_id` | `chars` |
| `group_info[0]/node_name` | `node_name` | `chars` |
| `group_info[0]/oid` | `oid` | `chars` |
| `group_info[0]/node_id` | `node_id` | `chars` |
| `client_info/path` | `path` | `chars` |
| `client_info/ip` | `ip` | `chars` |
| `client_info/mode` | `mode` | `chars` |

#### 组合与映射要点

- 本规则组合输入候选：身份候选：`guid`；时间候选：`create_time`, `file_alarm_time`；主动方候选：待从样例确认；目标方候选：`file_path`, `virus_name`；载体候选：待从样例确认；检测候选：`result`。
- 从本节字段选择稳定 ID 和事件发生时间；不能直接使用规则名作为 `event_id`。
- 按事实将终端、进程、网络、文件和用户放入 `roles`；不沿用大禹 `attacker/victim` 作为标准角色。
- 将天擎类型、状态、结果转换为受控 `event_type`、`operation`、`outcome`、`severity`；原始值保留在 `source_finding` 或 `extensions`。
- 低频字段进入 `facets`/`extensions` 前必须确认稳定性和调查价值。

### 3.13 `edr_ssid_log`

- `log_type`：`edr_ssid_log`
- 描述：天擎SSID防护日志
- 规则过滤：`f_chars_has(syslog_topic, ssid_log)`
- 建议事件语义：网络事实事件；event_category 候选为 network
- 抽取字段数（按别名去重）：45

| 原始路径 | 输出别名 | WPL 类型 |
|---|---|---|
| `client_id` | `client_id` | `chars` |
| `guid` | `guid` | `chars` |
| `trigger_mode` | `trigger_mode` | `digit` |
| `virus_name` | `virus_name` | `chars` |
| `virus_type` | `virus_type` | `chars` |
| `file_path` | `file_path` | `chars` |
| `file_create_time` | `file_create_time` | `chars` |
| `file_alarm_time` | `file_alarm_time` | `chars` |
| `log_type` | `ssid_log_type` | `digit` |
| `md5` | `md5` | `chars` |
| `sha1` | `sha1` | `chars` |
| `result` | `result` | `chars` |
| `mac` | `mac` | `chars` |
| `need_reboot` | `need_reboot` | `chars` |
| `scanners` | `scanners` | `chars` |
| `client_info/report_ip` | `report_ip` | `chars` |
| `client_info/os` | `os` | `chars` |
| `client_info/mac` | `client_mac` | `chars` |
| `client_info/create_time` | `create_time` | `time` |
| `client_info/os_version/release_id` | `release_id` | `chars` |
| `client_info/os_version/build_version` | `build_version` | `chars` |
| `client_info/os_version/main` | `main` | `chars` |
| `client_info/os_version/describe` | `describe` | `chars` |
| `client_info/mid` | `mid` | `chars` |
| `client_info/sys_space` | `sys_space` | `chars` |
| `client_info/core_number` | `core_number` | `digit` |
| `client_info/login_account` | `login_account` | `chars` |
| `client_info/memory_size` | `memory_size` | `chars` |
| `client_info/update_time` | `update_time` | `time` |
| `client_info/ie_version` | `ie_version` | `chars` |
| `client_info/computer_working_group` | `computer_working_group` | `chars` |
| `client_info/domain` | `domain` | `chars` |
| `client_info/name` | `name` | `chars` |
| `client_info/os_bit` | `os_bit` | `chars` |
| `client_info/nic_list` | `nic_list` | `array` |
| `client_info/report_ipv6` | `report_ipv6` | `chars` |
| `client_info/state` | `state` | `chars` |
| `client_info/activation` | `activation` | `chars` |
| `client_info/system_language` | `system_language` | `chars` |
| `group_info[0]/node_type` | `node_type` | `chars` |
| `group_info[0]/tree_id` | `tree_id` | `chars` |
| `group_info[0]/node_name` | `node_name` | `chars` |
| `group_info[0]/oid` | `oid` | `chars` |
| `group_info[0]/node_id` | `node_id` | `chars` |
| `client_info/action` | `action` | `chars` |

#### 组合与映射要点

- 本规则组合输入候选：身份候选：`guid`；时间候选：`create_time`, `file_alarm_time`；主动方候选：待从样例确认；目标方候选：`file_path`, `virus_name`；载体候选：待从样例确认；检测候选：`result`。
- 从本节字段选择稳定 ID 和事件发生时间；不能直接使用规则名作为 `event_id`。
- 按事实将终端、进程、网络、文件和用户放入 `roles`；不沿用大禹 `attacker/victim` 作为标准角色。
- 将天擎类型、状态、结果转换为受控 `event_type`、`operation`、`outcome`、`severity`；原始值保留在 `source_finding` 或 `extensions`。
- 低频字段进入 `facets`/`extensions` 前必须确认稳定性和调查价值。

### 3.14 `edr_energy_manage_log`

- `log_type`：`edr_energy_manage_log`
- 描述：天擎能耗管理日志
- 规则过滤：`f_chars_has(syslog_topic, energy_manage_log)`
- 建议事件语义：资产/配置/状态事件；event_category 候选为 system 或 audit
- 抽取字段数（按别名去重）：43

| 原始路径 | 输出别名 | WPL 类型 |
|---|---|---|
| `client_id` | `client_id` | `chars` |
| `guid` | `guid` | `chars` |
| `trigger_mode` | `trigger_mode` | `digit` |
| `virus_name` | `virus_name` | `chars` |
| `virus_type` | `virus_type` | `chars` |
| `file_path` | `file_path` | `chars` |
| `file_create_time` | `file_create_time` | `chars` |
| `file_alarm_time` | `file_alarm_time` | `chars` |
| `md5` | `md5` | `chars` |
| `sha1` | `sha1` | `chars` |
| `result` | `result` | `chars` |
| `need_reboot` | `need_reboot` | `chars` |
| `scanners` | `scanners` | `chars` |
| `client_info/report_ip` | `report_ip` | `chars` |
| `client_info/os` | `os` | `chars` |
| `client_info/create_time` | `create_time` | `time` |
| `client_info/os_version/release_id` | `release_id` | `chars` |
| `client_info/os_version/build_version` | `build_version` | `chars` |
| `client_info/os_version/main` | `main` | `chars` |
| `client_info/os_version/describe` | `describe` | `chars` |
| `client_info/mid` | `mid` | `chars` |
| `client_info/sys_space` | `sys_space` | `chars` |
| `client_info/core_number` | `core_number` | `digit` |
| `client_info/login_account` | `login_account` | `chars` |
| `client_info/mac` | `mac` | `chars` |
| `client_info/memory_size` | `memory_size` | `chars` |
| `client_info/update_time` | `update_time` | `time` |
| `client_info/ie_version` | `ie_version` | `chars` |
| `client_info/computer_working_group` | `computer_working_group` | `chars` |
| `client_info/domain` | `domain` | `chars` |
| `client_info/name` | `name` | `chars` |
| `client_info/os_bit` | `os_bit` | `chars` |
| `client_info/nic_list` | `nic_list` | `array` |
| `client_info/report_ipv6` | `report_ipv6` | `chars` |
| `client_info/state` | `state` | `chars` |
| `client_info/activation` | `activation` | `chars` |
| `client_info/system_language` | `system_language` | `chars` |
| `group_info[0]/node_type` | `node_type` | `chars` |
| `group_info[0]/tree_id` | `tree_id` | `chars` |
| `group_info[0]/node_name` | `node_name` | `chars` |
| `group_info[0]/oid` | `oid` | `chars` |
| `group_info[0]/node_id` | `node_id` | `chars` |
| `client_info/action` | `action` | `chars` |

#### 组合与映射要点

- 本规则组合输入候选：身份候选：`guid`；时间候选：`create_time`, `file_alarm_time`；主动方候选：待从样例确认；目标方候选：`file_path`, `virus_name`；载体候选：待从样例确认；检测候选：`result`。
- 从本节字段选择稳定 ID 和事件发生时间；不能直接使用规则名作为 `event_id`。
- 按事实将终端、进程、网络、文件和用户放入 `roles`；不沿用大禹 `attacker/victim` 作为标准角色。
- 将天擎类型、状态、结果转换为受控 `event_type`、`operation`、`outcome`、`severity`；原始值保留在 `source_finding` 或 `extensions`。
- 低频字段进入 `facets`/`extensions` 前必须确认稳定性和调查价值。

### 3.15 `edr_net_out_log`

- `log_type`：`edr_net_out_log`
- 描述：天擎V10违规外联日志
- 规则过滤：`f_chars_has(syslog_topic, net_out_log)`
- 建议事件语义：网络事实事件；event_category 候选为 network
- 抽取字段数（按别名去重）：43

| 原始路径 | 输出别名 | WPL 类型 |
|---|---|---|
| `client_id` | `client_id` | `chars` |
| `guid` | `guid` | `chars` |
| `trigger_mode` | `trigger_mode` | `digit` |
| `virus_name` | `virus_name` | `chars` |
| `virus_type` | `virus_type` | `chars` |
| `file_path` | `file_path` | `chars` |
| `file_create_time` | `file_create_time` | `chars` |
| `file_alarm_time` | `file_alarm_time` | `chars` |
| `md5` | `md5` | `chars` |
| `sha1` | `sha1` | `chars` |
| `result` | `result` | `chars` |
| `need_reboot` | `need_reboot` | `chars` |
| `scanners` | `scanners` | `chars` |
| `client_info/report_ip` | `report_ip` | `chars` |
| `client_info/os` | `os` | `chars` |
| `client_info/create_time` | `create_time` | `time` |
| `client_info/os_version/release_id` | `release_id` | `chars` |
| `client_info/os_version/build_version` | `build_version` | `chars` |
| `client_info/os_version/main` | `main` | `chars` |
| `client_info/os_version/describe` | `describe` | `chars` |
| `client_info/mid` | `mid` | `chars` |
| `client_info/sys_space` | `sys_space` | `chars` |
| `client_info/core_number` | `core_number` | `digit` |
| `client_info/login_account` | `login_account` | `chars` |
| `client_info/mac` | `mac` | `chars` |
| `client_info/memory_size` | `memory_size` | `chars` |
| `client_info/update_time` | `update_time` | `time` |
| `client_info/ie_version` | `ie_version` | `chars` |
| `client_info/computer_working_group` | `computer_working_group` | `chars` |
| `client_info/domain` | `domain` | `chars` |
| `client_info/name` | `name` | `chars` |
| `client_info/os_bit` | `os_bit` | `chars` |
| `client_info/nic_list` | `nic_list` | `array` |
| `client_info/report_ipv6` | `report_ipv6` | `chars` |
| `client_info/state` | `state` | `chars` |
| `client_info/activation` | `activation` | `chars` |
| `client_info/system_language` | `system_language` | `chars` |
| `group_info[0]/node_type` | `node_type` | `chars` |
| `group_info[0]/tree_id` | `tree_id` | `chars` |
| `group_info[0]/node_name` | `node_name` | `chars` |
| `group_info[0]/oid` | `oid` | `chars` |
| `group_info[0]/node_id` | `node_id` | `chars` |
| `client_info/online_info/last_time` | `last_time` | `time` |

#### 组合与映射要点

- 本规则组合输入候选：身份候选：`guid`；时间候选：`create_time`, `file_alarm_time`；主动方候选：待从样例确认；目标方候选：`file_path`, `virus_name`；载体候选：待从样例确认；检测候选：`result`。
- 从本节字段选择稳定 ID 和事件发生时间；不能直接使用规则名作为 `event_id`。
- 按事实将终端、进程、网络、文件和用户放入 `roles`；不沿用大禹 `attacker/victim` 作为标准角色。
- 将天擎类型、状态、结果转换为受控 `event_type`、`operation`、`outcome`、`severity`；原始值保留在 `source_finding` 或 `extensions`。
- 低频字段进入 `facets`/`extensions` 前必须确认稳定性和调查价值。

### 3.16 `edr_external_device_alarm`

- `log_type`：`edr_external_device_alarm`
- 描述：天擎外设管理日志
- 规则过滤：`f_chars_has(syslog_topic, external_device_alarm)`
- 建议事件语义：资产/配置/状态事件；event_category 候选为 system 或 audit
- 抽取字段数（按别名去重）：44

| 原始路径 | 输出别名 | WPL 类型 |
|---|---|---|
| `client_id` | `client_id` | `chars` |
| `guid` | `guid` | `chars` |
| `trigger_mode` | `trigger_mode` | `digit` |
| `virus_name` | `virus_name` | `chars` |
| `virus_type` | `virus_type` | `chars` |
| `file_path` | `file_path` | `chars` |
| `file_create_time` | `file_create_time` | `chars` |
| `file_alarm_time` | `file_alarm_time` | `chars` |
| `md5` | `md5` | `chars` |
| `sha1` | `sha1` | `chars` |
| `result` | `result` | `chars` |
| `need_reboot` | `need_reboot` | `chars` |
| `scanners` | `scanners` | `chars` |
| `client_info/report_ip` | `report_ip` | `chars` |
| `client_info/os` | `os` | `chars` |
| `client_info/create_time` | `create_time` | `time` |
| `client_info/os_version/release_id` | `release_id` | `chars` |
| `client_info/os_version/build_version` | `build_version` | `chars` |
| `client_info/os_version/main` | `main` | `chars` |
| `client_info/os_version/describe` | `describe` | `chars` |
| `client_info/mid` | `mid` | `chars` |
| `client_info/sys_space` | `sys_space` | `chars` |
| `client_info/core_number` | `core_number` | `digit` |
| `client_info/login_account` | `login_account` | `chars` |
| `client_info/mac` | `mac` | `chars` |
| `client_info/memory_size` | `memory_size` | `chars` |
| `client_info/update_time` | `update_time` | `time` |
| `client_info/ie_version` | `ie_version` | `chars` |
| `client_info/computer_working_group` | `computer_working_group` | `chars` |
| `client_info/domain` | `domain` | `chars` |
| `client_info/name` | `host_name` | `chars` |
| `name` | `name` | `chars` |
| `client_info/os_bit` | `os_bit` | `chars` |
| `client_info/nic_list` | `nic_list` | `array` |
| `client_info/report_ipv6` | `report_ipv6` | `chars` |
| `client_info/state` | `state` | `chars` |
| `client_info/activation` | `activation` | `chars` |
| `client_info/system_language` | `system_language` | `chars` |
| `group_info[0]/node_type` | `node_type` | `chars` |
| `group_info[0]/tree_id` | `tree_id` | `chars` |
| `group_info[0]/node_name` | `node_name` | `chars` |
| `group_info[0]/oid` | `oid` | `chars` |
| `group_info[0]/node_id` | `node_id` | `chars` |
| `client_info/action` | `action` | `chars` |

#### 组合与映射要点

- 本规则组合输入候选：身份候选：`guid`；时间候选：`create_time`, `file_alarm_time`；主动方候选：待从样例确认；目标方候选：`file_path`, `virus_name`；载体候选：待从样例确认；检测候选：`result`。
- 从本节字段选择稳定 ID 和事件发生时间；不能直接使用规则名作为 `event_id`。
- 按事实将终端、进程、网络、文件和用户放入 `roles`；不沿用大禹 `attacker/victim` 作为标准角色。
- 将天擎类型、状态、结果转换为受控 `event_type`、`operation`、`outcome`、`severity`；原始值保留在 `source_finding` 或 `extensions`。
- 低频字段进入 `facets`/`extensions` 前必须确认稳定性和调查价值。

### 3.17 `edr_remote_assistance_log`

- `log_type`：`edr_remote_assistance_log`
- 描述：天擎远程协助日志
- 规则过滤：`f_chars_has(syslog_topic, remote_assistance_log)`
- 建议事件语义：文件/数据访问事件；event_category 候选为 audit
- 抽取字段数（按别名去重）：44

| 原始路径 | 输出别名 | WPL 类型 |
|---|---|---|
| `client_id` | `client_id` | `chars` |
| `guid` | `guid` | `chars` |
| `trigger_mode` | `trigger_mode` | `digit` |
| `virus_name` | `virus_name` | `chars` |
| `virus_type` | `virus_type` | `chars` |
| `file_path` | `file_path` | `chars` |
| `file_create_time` | `file_create_time` | `chars` |
| `file_alarm_time` | `file_alarm_time` | `chars` |
| `md5` | `md5` | `chars` |
| `sha1` | `sha1` | `chars` |
| `result` | `result` | `chars` |
| `need_reboot` | `need_reboot` | `chars` |
| `scanners` | `scanners` | `chars` |
| `client_info/report_ip` | `report_ip` | `chars` |
| `client_info/os` | `os` | `chars` |
| `create_time` | `create_time` | `time_timestamp` |
| `client_info/os_version/release_id` | `release_id` | `chars` |
| `client_info/os_version/build_version` | `build_version` | `chars` |
| `client_info/os_version/main` | `main` | `chars` |
| `client_info/os_version/describe` | `describe` | `chars` |
| `client_info/mid` | `mid` | `chars` |
| `client_info/sys_space` | `sys_space` | `chars` |
| `client_info/core_number` | `core_number` | `digit` |
| `client_info/login_account` | `login_account` | `chars` |
| `client_info/mac` | `mac` | `chars` |
| `client_info/memory_size` | `memory_size` | `chars` |
| `client_info/update_time` | `update_time` | `time` |
| `client_info/ie_version` | `ie_version` | `chars` |
| `client_info/computer_working_group` | `computer_working_group` | `chars` |
| `client_info/domain` | `domain` | `chars` |
| `client_info/name` | `name` | `chars` |
| `client_info/os_bit` | `os_bit` | `chars` |
| `client_info/nic_list` | `nic_list` | `array` |
| `client_info/report_ipv6` | `report_ipv6` | `chars` |
| `client_info/state` | `state` | `chars` |
| `client_info/activation` | `activation` | `chars` |
| `client_info/system_language` | `system_language` | `chars` |
| `group_info[0]/node_type` | `node_type` | `chars` |
| `group_info[0]/tree_id` | `tree_id` | `chars` |
| `group_info[0]/node_name` | `node_name` | `chars` |
| `group_info[0]/oid` | `oid` | `chars` |
| `group_info[0]/node_id` | `node_id` | `chars` |
| `client_info/action` | `action` | `chars` |
| `report_time` | `report_time` | `time_timestamp` |

#### 组合与映射要点

- 本规则组合输入候选：身份候选：`guid`；时间候选：`create_time`, `file_alarm_time`；主动方候选：待从样例确认；目标方候选：`file_path`, `virus_name`；载体候选：待从样例确认；检测候选：`result`。
- 从本节字段选择稳定 ID 和事件发生时间；不能直接使用规则名作为 `event_id`。
- 按事实将终端、进程、网络、文件和用户放入 `roles`；不沿用大禹 `attacker/victim` 作为标准角色。
- 将天擎类型、状态、结果转换为受控 `event_type`、`operation`、`outcome`、`severity`；原始值保留在 `source_finding` 或 `extensions`。
- 低频字段进入 `facets`/`extensions` 前必须确认稳定性和调查价值。

### 3.18 `edr_remote_assistance_file_transfer`

- `log_type`：`edr_remote_assistance_file_transfer`
- 描述：天擎远程文件传输日志
- 规则过滤：`f_chars_has(syslog_topic, remote_assistance_file_transfer)`
- 建议事件语义：文件/数据访问事件；event_category 候选为 audit
- 抽取字段数（按别名去重）：44

| 原始路径 | 输出别名 | WPL 类型 |
|---|---|---|
| `client_id` | `client_id` | `chars` |
| `guid` | `guid` | `chars` |
| `trigger_mode` | `trigger_mode` | `digit` |
| `virus_name` | `virus_name` | `chars` |
| `virus_type` | `virus_type` | `chars` |
| `file_path` | `file_path` | `chars` |
| `file_create_time` | `file_create_time` | `chars` |
| `file_alarm_time` | `file_alarm_time` | `chars` |
| `md5` | `md5` | `chars` |
| `sha1` | `sha1` | `chars` |
| `result` | `result` | `chars` |
| `need_reboot` | `need_reboot` | `chars` |
| `scanners` | `scanners` | `chars` |
| `client_info/report_ip` | `report_ip` | `chars` |
| `client_info/os` | `os` | `chars` |
| `create_time` | `create_time` | `time_timestamp` |
| `client_info/os_version/release_id` | `release_id` | `chars` |
| `client_info/os_version/build_version` | `build_version` | `chars` |
| `client_info/os_version/main` | `main` | `chars` |
| `client_info/os_version/describe` | `describe` | `chars` |
| `client_info/mid` | `mid` | `chars` |
| `client_info/sys_space` | `sys_space` | `chars` |
| `client_info/core_number` | `core_number` | `digit` |
| `client_info/login_account` | `login_account` | `chars` |
| `client_info/mac` | `mac` | `chars` |
| `client_info/memory_size` | `memory_size` | `chars` |
| `client_info/update_time` | `update_time` | `time` |
| `client_info/ie_version` | `ie_version` | `chars` |
| `client_info/computer_working_group` | `computer_working_group` | `chars` |
| `client_info/domain` | `domain` | `chars` |
| `client_info/name` | `name` | `chars` |
| `client_info/os_bit` | `os_bit` | `chars` |
| `client_info/nic_list` | `nic_list` | `array` |
| `client_info/report_ipv6` | `report_ipv6` | `chars` |
| `client_info/state` | `state` | `chars` |
| `client_info/activation` | `activation` | `chars` |
| `client_info/system_language` | `system_language` | `chars` |
| `group_info[0]/node_type` | `node_type` | `chars` |
| `group_info[0]/tree_id` | `tree_id` | `chars` |
| `group_info[0]/node_name` | `node_name` | `chars` |
| `group_info[0]/oid` | `oid` | `chars` |
| `group_info[0]/node_id` | `node_id` | `chars` |
| `client_info/action` | `action` | `chars` |
| `report_time` | `report_time` | `time_timestamp` |

#### 组合与映射要点

- 本规则组合输入候选：身份候选：`guid`；时间候选：`create_time`, `file_alarm_time`；主动方候选：待从样例确认；目标方候选：`file_path`, `virus_name`；载体候选：待从样例确认；检测候选：`result`。
- 从本节字段选择稳定 ID 和事件发生时间；不能直接使用规则名作为 `event_id`。
- 按事实将终端、进程、网络、文件和用户放入 `roles`；不沿用大禹 `attacker/victim` 作为标准角色。
- 将天擎类型、状态、结果转换为受控 `event_type`、`operation`、`outcome`、`severity`；原始值保留在 `source_finding` 或 `extensions`。
- 低频字段进入 `facets`/`extensions` 前必须确认稳定性和调查价值。

### 3.19 `cs_op_log`

- `log_type`：`cs_op_log`
- 描述：计算系统操作日志
- 规则过滤：`f_has(operator_name)`
- 建议事件语义：待确认事件语义
- 抽取字段数（按别名去重）：11

| 原始路径 | 输出别名 | WPL 类型 |
|---|---|---|
| `create_time` | `create_time` | `time_timestamp` |
| `client_ip` | `client_ip` | `chars` |
| `operator` | `operator` | `chars` |
| `operator_name` | `operator_name` | `chars` |
| `path` | `path` | `chars` |
| `entity_id` | `entity_id` | `chars` |
| `status` | `status` | `chars` |
| `op_level` | `op_level` | `chars` |
| `asset_id` | `asset_id` | `chars` |
| `asset_oid` | `asset_oid` | `chars` |
| `op_type` | `op_type` | `chars` |

#### 组合与映射要点

- 本规则组合输入候选：身份候选：`asset_id`；时间候选：`create_time`；主动方候选：待从样例确认；目标方候选：待从样例确认；载体候选：待从样例确认；检测候选：`status`。
- 从本节字段选择稳定 ID 和事件发生时间；不能直接使用规则名作为 `event_id`。
- 按事实将终端、进程、网络、文件和用户放入 `roles`；不沿用大禹 `attacker/victim` 作为标准角色。
- 将天擎类型、状态、结果转换为受控 `event_type`、`operation`、`outcome`、`severity`；原始值保留在 `source_finding` 或 `extensions`。
- 低频字段进入 `facets`/`extensions` 前必须确认稳定性和调查价值。

### 3.20 `edr_process_event`

- `log_type`：`edr_process_event`
- 描述：天擎EDR进程事件
- 规则过滤：`f_chars_has(type, process_details)`
- 建议事件语义：进程/系统审计事件；event_category 候选为 audit
- 抽取字段数（按别名去重）：61

| 原始路径 | 输出别名 | WPL 类型 |
|---|---|---|
| `task_id` | `task_id` | `chars` |
| `sub_task_id` | `sub_task_id` | `chars` |
| `asset_oid` | `asset_oid` | `chars` |
| `custom_group_paths` | `custom_group_paths` | `chars` |
| `env_version` | `env_version` | `chars` |
| `event_date_creation` | `event_date_creation` | `time_timestamp` |
| `process_current_directory` | `process_current_directory` | `chars` |
| `process_integrity_level` | `process_integrity_level` | `chars` |
| `process_parent_command_line` | `process_parent_command_line` | `chars` |
| `process_parent_id` | `process_parent_id` | `chars` |
| `process_parent_internal_name` | `process_parent_internal_name` | `chars` |
| `process_parent_name` | `process_parent_name` | `chars` |
| `process_parent_original_name` | `process_parent_original_name` | `chars` |
| `process_parent_sign` | `process_parent_sign` | `chars` |
| `process_pparent_command_line` | `process_pparent_command_line` | `chars` |
| `process_pparent_name` | `process_pparent_name` | `chars` |
| `process_pparent_path` | `process_pparent_path` | `chars` |
| `process_root_guid` | `process_root_guid` | `chars` |
| `process_root_id` | `process_root_id` | `chars` |
| `process_sha1` | `process_sha1` | `chars` |
| `process_terminate_time` | `process_terminate_time` | `chars` |
| `timestamp` | `timestamp` | `time_timestamp` |
| `type` | `type` | `chars` |
| `user_logon_id` | `user_logon_id` | `chars` |
| `user_session_id` | `user_session_id` | `chars` |
| `uuid` | `uuid` | `chars` |
| `computer_name` | `computer_name` | `chars` |
| `gid` | `gid` | `chars` |
| `hostname` | `hostname` | `chars` |
| `logger` | `logger` | `chars` |
| `pid` | `pid` | `chars` |
| `process_command_line` | `process_command_line` | `chars` |
| `process_company` | `process_company` | `chars` |
| `process_copyright` | `process_copyright` | `chars` |
| `process_description` | `process_description` | `chars` |
| `process_internal_name` | `process_internal_name` | `chars` |
| `process_original_name` | `process_original_name` | `chars` |
| `process_parent_guid` | `process_parent_guid` | `chars` |
| `process_parent_path` | `process_parent_path` | `chars` |
| `process_product` | `process_product` | `chars` |
| `process_sign` | `process_sign` | `chars` |
| `process_user` | `process_user` | `chars` |
| `process_version` | `process_version` | `chars` |
| `client_report_ip` | `client_report_ip` | `chars` |
| `report_ip` | `report_ip` | `chars` |
| `asset_id` | `asset_id` | `chars` |
| `client_id` | `client_id` | `chars` |
| `client_ip` | `client_ip` | `chars` |
| `ip` | `ip` | `chars` |
| `create_time` | `create_time` | `time_timestamp` |
| `event_type` | `event_type` | `chars` |
| `group_name` | `group_name` | `chars` |
| `mac` | `mac` | `chars` |
| `mid` | `mid` | `chars` |
| `payload` | `payload` | `chars` |
| `process_create_time` | `process_create_time` | `chars` |
| `process_guid` | `process_guid` | `chars` |
| `process_id` | `process_id` | `chars` |
| `process_md5` | `process_md5` | `chars` |
| `process_name` | `process_name` | `chars` |
| `process_path` | `process_path` | `chars` |

#### 组合与映射要点

- 本规则组合输入候选：身份候选：`uuid`, `asset_id`；时间候选：`event_date_creation`, `create_time`, `timestamp`；主动方候选：`process_user`；目标方候选：待从样例确认；载体候选：`process_name`, `process_guid`, `process_id`, `process_command_line`；检测候选：待从样例确认。
- 从本节字段选择稳定 ID 和事件发生时间；不能直接使用规则名作为 `event_id`。
- 按事实将终端、进程、网络、文件和用户放入 `roles`；不沿用大禹 `attacker/victim` 作为标准角色。
- 将天擎类型、状态、结果转换为受控 `event_type`、`operation`、`outcome`、`severity`；原始值保留在 `source_finding` 或 `extensions`。
- 低频字段进入 `facets`/`extensions` 前必须确认稳定性和调查价值。

### 3.21 `edr_file_op`

- `log_type`：`edr_file_op`
- 描述：天擎EDR文件操作
- 规则过滤：`f_chars_has(type, file_operations)`
- 建议事件语义：文件/数据访问事件；event_category 候选为 audit
- 抽取字段数（按别名去重）：50

| 原始路径 | 输出别名 | WPL 类型 |
|---|---|---|
| `task_id` | `task_id` | `chars` |
| `sub_task_id` | `sub_task_id` | `chars` |
| `asset_oid` | `asset_oid` | `chars` |
| `custom_group_paths` | `custom_group_paths` | `chars` |
| `env_version` | `env_version` | `chars` |
| `event_date_creation` | `event_date_creation` | `time_timestamp` |
| `file_name_renamed` | `file_name_renamed` | `chars` |
| `file_path_renamed` | `file_path_renamed` | `chars` |
| `file_previous_date_creation` | `file_previous_date_creation` | `chars` |
| `process_parent_command_line` | `process_parent_command_line` | `chars` |
| `process_parent_internal_name` | `process_parent_internal_name` | `chars` |
| `process_parent_name` | `process_parent_name` | `chars` |
| `process_parent_original_name` | `process_parent_original_name` | `chars` |
| `process_parent_sign` | `process_parent_sign` | `chars` |
| `process_sha1` | `process_sha1` | `chars` |
| `removable_device` | `removable_device` | `chars` |
| `timestamp` | `timestamp` | `time_timestamp` |
| `type` | `type` | `chars` |
| `uuid` | `uuid` | `chars` |
| `computer_name` | `computer_name` | `chars` |
| `file_date_creation` | `file_date_creation` | `chars` |
| `gid` | `gid` | `chars` |
| `hostname` | `hostname` | `chars` |
| `logger` | `logger` | `chars` |
| `pid` | `pid` | `chars` |
| `process_command_line` | `process_command_line` | `chars` |
| `process_internal_name` | `process_internal_name` | `chars` |
| `process_original_name` | `process_original_name` | `chars` |
| `process_parent_path` | `process_parent_path` | `chars` |
| `process_sign` | `process_sign` | `chars` |
| `process_user` | `process_user` | `chars` |
| `client_report_ip` | `client_report_ip` | `chars` |
| `report_ip` | `report_ip` | `chars` |
| `asset_id` | `asset_id` | `chars` |
| `client_id` | `client_id` | `chars` |
| `client_ip` | `client_ip` | `chars` |
| `ip` | `ip` | `chars` |
| `create_time` | `create_time` | `time_timestamp` |
| `file_md5` | `file_md5` | `chars` |
| `file_name` | `file_name` | `chars` |
| `file_path` | `file_path` | `chars` |
| `group_name` | `group_name` | `chars` |
| `mac` | `mac` | `chars` |
| `mid` | `mid` | `chars` |
| `payload` | `payload` | `chars` |
| `process_guid` | `process_guid` | `chars` |
| `process_id` | `process_id` | `chars` |
| `process_md5` | `process_md5` | `chars` |
| `process_name` | `process_name` | `chars` |
| `process_path` | `process_path` | `chars` |

#### 组合与映射要点

- 本规则组合输入候选：身份候选：`uuid`, `asset_id`；时间候选：`event_date_creation`, `create_time`, `timestamp`；主动方候选：`process_user`；目标方候选：`file_path`, `file_name`；载体候选：`process_name`, `process_guid`, `process_id`, `process_command_line`；检测候选：待从样例确认。
- 从本节字段选择稳定 ID 和事件发生时间；不能直接使用规则名作为 `event_id`。
- 按事实将终端、进程、网络、文件和用户放入 `roles`；不沿用大禹 `attacker/victim` 作为标准角色。
- 将天擎类型、状态、结果转换为受控 `event_type`、`operation`、`outcome`、`severity`；原始值保留在 `source_finding` 或 `extensions`。
- 低频字段进入 `facets`/`extensions` 前必须确认稳定性和调查价值。

### 3.22 `edr_wmi_event`

- `log_type`：`edr_wmi_event`
- 描述：天擎EDR_WMI事件
- 规则过滤：`f_chars_has(type, wmi_event)`
- 建议事件语义：进程/系统审计事件；event_category 候选为 audit
- 抽取字段数（按别名去重）：45

| 原始路径 | 输出别名 | WPL 类型 |
|---|---|---|
| `task_id` | `task_id` | `chars` |
| `sub_task_id` | `sub_task_id` | `chars` |
| `asset_oid` | `asset_oid` | `chars` |
| `custom_group_paths` | `custom_group_paths` | `chars` |
| `event_date_creation` | `event_date_creation` | `time_timestamp` |
| `process_parent_command_line` | `process_parent_command_line` | `chars` |
| `process_parent_internal_name` | `process_parent_internal_name` | `chars` |
| `process_parent_name` | `process_parent_name` | `chars` |
| `process_parent_original_name` | `process_parent_original_name` | `chars` |
| `process_parent_sign` | `process_parent_sign` | `chars` |
| `process_sha1` | `process_sha1` | `chars` |
| `timestamp` | `timestamp` | `time_timestamp` |
| `type` | `type` | `chars` |
| `uuid` | `uuid` | `chars` |
| `wmi_consumer_destination` | `wmi_consumer_destination` | `chars` |
| `wmi_consumer_name` | `wmi_consumer_name` | `chars` |
| `wmi_consumer_type` | `wmi_consumer_type` | `chars` |
| `wmi_filter_name` | `wmi_filter_name` | `chars` |
| `wmi_filter_wql` | `wmi_filter_wql` | `chars` |
| `wmi_namespace` | `wmi_namespace` | `chars` |
| `wmi_operation` | `wmi_operation` | `chars` |
| `computer_name` | `computer_name` | `chars` |
| `gid` | `gid` | `chars` |
| `process_command_line` | `process_command_line` | `chars` |
| `process_internal_name` | `process_internal_name` | `chars` |
| `process_original_name` | `process_original_name` | `chars` |
| `process_parent_path` | `process_parent_path` | `chars` |
| `process_sign` | `process_sign` | `chars` |
| `process_user` | `process_user` | `chars` |
| `client_report_ip` | `client_report_ip` | `chars` |
| `report_ip` | `report_ip` | `chars` |
| `asset_id` | `asset_id` | `chars` |
| `client_id` | `client_id` | `chars` |
| `event_type` | `event_type` | `chars` |
| `group_name` | `group_name` | `chars` |
| `mac` | `mac` | `chars` |
| `mid` | `mid` | `chars` |
| `payload` | `payload` | `chars` |
| `process_guid` | `process_guid` | `chars` |
| `process_id` | `process_id` | `chars` |
| `process_md5` | `process_md5` | `chars` |
| `process_name` | `process_name` | `chars` |
| `process_path` | `process_path` | `chars` |
| `client_ip` | `client_ip` | `chars` |
| `ip` | `ip` | `chars` |

#### 组合与映射要点

- 本规则组合输入候选：身份候选：`uuid`, `asset_id`；时间候选：`event_date_creation`, `timestamp`；主动方候选：`process_user`；目标方候选：待从样例确认；载体候选：`process_name`, `process_guid`, `process_id`, `process_command_line`；检测候选：待从样例确认。
- 从本节字段选择稳定 ID 和事件发生时间；不能直接使用规则名作为 `event_id`。
- 按事实将终端、进程、网络、文件和用户放入 `roles`；不沿用大禹 `attacker/victim` 作为标准角色。
- 将天擎类型、状态、结果转换为受控 `event_type`、`operation`、`outcome`、`severity`；原始值保留在 `source_finding` 或 `extensions`。
- 低频字段进入 `facets`/`extensions` 前必须确认稳定性和调查价值。

### 3.23 `edr_powershell_cmd_exec`

- `log_type`：`edr_powershell_cmd_exec`
- 描述：天擎EDR_POWERSHELL命令执行
- 规则过滤：`f_chars_has(type, powershell_execute)`
- 建议事件语义：进程/系统审计事件；event_category 候选为 audit
- 抽取字段数（按别名去重）：40

| 原始路径 | 输出别名 | WPL 类型 |
|---|---|---|
| `task_id` | `task_id` | `chars` |
| `sub_task_id` | `sub_task_id` | `chars` |
| `asset_oid` | `asset_oid` | `chars` |
| `custom_group_paths` | `custom_group_paths` | `chars` |
| `env_version` | `env_version` | `chars` |
| `event_date_creation` | `event_date_creation` | `time_timestamp` |
| `powershell_payload` | `powershell_payload` | `chars` |
| `script_command` | `script_command` | `chars` |
| `script_id` | `script_id` | `chars` |
| `security_id` | `security_id` | `chars` |
| `timestamp` | `timestamp` | `time_timestamp` |
| `type` | `type` | `chars` |
| `uuid` | `uuid` | `chars` |
| `computer_name` | `computer_name` | `chars` |
| `gid` | `gid` | `chars` |
| `hostname` | `hostname` | `chars` |
| `logger` | `logger` | `chars` |
| `pid` | `pid` | `chars` |
| `powershell_create_time` | `powershell_create_time` | `time_timestamp` |
| `process_internal_name` | `process_internal_name` | `chars` |
| `process_sign` | `process_sign` | `chars` |
| `process_user` | `process_user` | `chars` |
| `client_report_ip` | `client_report_ip` | `chars` |
| `report_ip` | `report_ip` | `chars` |
| `user_data` | `user_data` | `chars` |
| `asset_id` | `asset_id` | `chars` |
| `client_id` | `client_id` | `chars` |
| `client_ip` | `client_ip` | `chars` |
| `ip` | `ip` | `chars` |
| `create_time` | `create_time` | `time_timestamp` |
| `event_id` | `event_id` | `chars` |
| `event_type` | `event_type` | `chars` |
| `group_name` | `group_name` | `chars` |
| `keywords` | `keywords` | `chars` |
| `mac` | `mac` | `chars` |
| `mid` | `mid` | `chars` |
| `payload` | `payload` | `chars` |
| `process_guid` | `process_guid` | `chars` |
| `process_id` | `process_id` | `chars` |
| `thread_id` | `thread_id` | `digit` |

#### 组合与映射要点

- 本规则组合输入候选：身份候选：`event_id`, `uuid`, `asset_id`；时间候选：`event_date_creation`, `create_time`, `timestamp`；主动方候选：`process_user`；目标方候选：待从样例确认；载体候选：`process_guid`, `process_id`；检测候选：待从样例确认。
- 从本节字段选择稳定 ID 和事件发生时间；不能直接使用规则名作为 `event_id`。
- 按事实将终端、进程、网络、文件和用户放入 `roles`；不沿用大禹 `attacker/victim` 作为标准角色。
- 将天擎类型、状态、结果转换为受控 `event_type`、`operation`、`outcome`、`severity`；原始值保留在 `source_finding` 或 `extensions`。
- 低频字段进入 `facets`/`extensions` 前必须确认稳定性和调查价值。

> 2026-08-05 使用真实样例和当前 WPL 实测：规则成功输出 45 个字段、残留 0 字节。公共解析段还输出了 `process_name/path/command_line/md5/sha1`、父进程字段、`context_info`、`os_type` 和 `report_ipv6`，因此实际映射以验证后的 WPL 输出为准，不以本节 40 字段静态扫描结果为限。

### 3.24 `edr_account_change`

- `log_type`：`edr_account_change`
- 描述：天擎EDR账号变更
- 规则过滤：`f_chars_has(type, account_change)`
- 建议事件语义：身份/账号审计事件；event_category 候选为 auth 或 audit，需按事实确认
- 抽取字段数（按别名去重）：45

| 原始路径 | 输出别名 | WPL 类型 |
|---|---|---|
| `task_id` | `task_id` | `chars` |
| `sub_task_id` | `sub_task_id` | `chars` |
| `env_version` | `env_version` | `chars` |
| `process_parent_command_line` | `process_parent_command_line` | `chars` |
| `process_parent_internal_name` | `process_parent_internal_name` | `chars` |
| `process_parent_name` | `process_parent_name` | `chars` |
| `process_parent_original_name` | `process_parent_original_name` | `chars` |
| `process_parent_sign` | `process_parent_sign` | `chars` |
| `process_sha1` | `process_sha1` | `chars` |
| `timestamp` | `timestamp` | `time` |
| `type` | `type` | `chars` |
| `uuid` | `uuid` | `chars` |
| `logger` | `logger` | `chars` |
| `process_original_name` | `process_original_name` | `chars` |
| `process_parent_path` | `process_parent_path` | `chars` |
| `process_sign` | `process_sign` | `chars` |
| `process_user` | `process_user` | `chars` |
| `client_report_ip` | `client_report_ip` | `chars` |
| `report_ip` | `report_ip` | `chars` |
| `account_name` | `account_name` | `chars` |
| `account_user` | `account_user` | `chars` |
| `asset_id` | `asset_id` | `chars` |
| `asset_oid` | `asset_oid` | `chars` |
| `client_id` | `client_id` | `chars` |
| `client_ip` | `client_ip` | `chars` |
| `ip` | `ip` | `chars` |
| `computer_name` | `computer_name` | `chars` |
| `create_time` | `create_time` | `time` |
| `custom_group_paths` | `custom_group_paths` | `chars` |
| `event_date_creation` | `event_date_creation` | `time` |
| `event_type` | `event_type` | `chars` |
| `gid` | `gid` | `chars` |
| `group_name` | `group_name` | `chars` |
| `hostname` | `hostname` | `chars` |
| `mac` | `mac` | `chars` |
| `mid` | `mid` | `chars` |
| `payload` | `payload` | `chars` |
| `pid` | `pid` | `chars` |
| `process_command_line` | `process_command_line` | `chars` |
| `process_guid` | `process_guid` | `chars` |
| `process_id` | `process_id` | `chars` |
| `process_internal_name` | `process_internal_name` | `chars` |
| `process_md5` | `process_md5` | `chars` |
| `process_name` | `process_name` | `chars` |
| `process_path` | `process_path` | `chars` |

#### 组合与映射要点

- 本规则组合输入候选：身份候选：`uuid`, `asset_id`；时间候选：`event_date_creation`, `create_time`, `timestamp`；主动方候选：`process_user`, `account_name`；目标方候选：`account_user`；载体候选：`process_name`, `process_guid`, `process_id`, `process_command_line`；检测候选：待从样例确认。
- 从本节字段选择稳定 ID 和事件发生时间；不能直接使用规则名作为 `event_id`。
- 按事实将终端、进程、网络、文件和用户放入 `roles`；不沿用大禹 `attacker/victim` 作为标准角色。
- 将天擎类型、状态、结果转换为受控 `event_type`、`operation`、`outcome`、`severity`；原始值保留在 `source_finding` 或 `extensions`。
- 低频字段进入 `facets`/`extensions` 前必须确认稳定性和调查价值。

### 3.25 `edr_file_audit`

- `log_type`：`edr_file_audit`
- 描述：天擎文件审计日志
- 规则过滤：`f_chars_has(syslog_topic, file_audit)`
- 建议事件语义：文件/数据访问事件；event_category 候选为 audit
- 抽取字段数（按别名去重）：39

| 原始路径 | 输出别名 | WPL 类型 |
|---|---|---|
| `asset_oid` | `asset_oid` | `chars` |
| `asset_id` | `asset_id` | `chars` |
| `client_id` | `client_id` | `chars` |
| `client_ip` | `client_ip` | `chars` |
| `client_report_ip` | `client_report_ip` | `chars` |
| `client_name` | `client_name` | `chars` |
| `client_mac` | `client_mac` | `chars` |
| `client_mid` | `client_mid` | `chars` |
| `client_type` | `client_type` | `chars` |
| `client_login_account` | `client_login_account` | `chars` |
| `client_os_version_main` | `client_os_version_main` | `chars` |
| `client_os_version_describe` | `client_os_version_describe` | `chars` |
| `client_os_version_build_version` | `client_os_version_build_version` | `chars` |
| `client_os_version_release_id` | `client_os_version_release_id` | `chars` |
| `group_node_id` | `group_node_id` | `chars` |
| `group_node_name` | `group_node_name` | `chars` |
| `group_node_path` | `group_node_path` | `chars` |
| `path_level1` | `path_level1` | `chars` |
| `path_level2` | `path_level2` | `chars` |
| `path_level3` | `path_level3` | `chars` |
| `path_level4` | `path_level4` | `chars` |
| `create_time` | `create_time` | `time_timestamp` |
| `report_time` | `report_time` | `time_timestamp` |
| `collect_time` | `collect_time` | `chars` |
| `process_name` | `process_name` | `chars` |
| `transfer_method` | `transfer_method` | `chars` |
| `transfer_channel` | `transfer_channel` | `chars` |
| `operation_type` | `operation_type` | `chars` |
| `audit_type` | `audit_type` | `chars` |
| `behavior` | `behavior` | `chars` |
| `result` | `result` | `chars` |
| `handle` | `handle` | `chars` |
| `usb_type` | `usb_type` | `chars` |
| `local_file_is_exists` | `local_file_is_exists` | `chars` |
| `file_size` | `file_size` | `chars` |
| `file_name` | `file_name` | `chars` |
| `local_file_path` | `local_file_path` | `chars` |
| `upload_url` | `upload_url` | `chars` |
| `syslog_topic` | `syslog_topic` | `chars` |

#### 组合与映射要点

- 本规则组合输入候选：身份候选：`asset_id`；时间候选：`create_time`；主动方候选：待从样例确认；目标方候选：`file_name`；载体候选：`process_name`；检测候选：`result`。
- 从本节字段选择稳定 ID 和事件发生时间；不能直接使用规则名作为 `event_id`。
- 按事实将终端、进程、网络、文件和用户放入 `roles`；不沿用大禹 `attacker/victim` 作为标准角色。
- 将天擎类型、状态、结果转换为受控 `event_type`、`operation`、`outcome`、`severity`；原始值保留在 `source_finding` 或 `extensions`。
- 低频字段进入 `facets`/`extensions` 前必须确认稳定性和调查价值。

### 3.26 `edr_mobile_storage_client_log`

- `log_type`：`edr_mobile_storage_client_log`
- 描述：天擎移动存储客户端日志
- 规则过滤：`f_chars_has(syslog_topic, mobile_storage_client_log)`
- 建议事件语义：文件/数据访问事件；event_category 候选为 audit
- 抽取字段数（按别名去重）：125

| 原始路径 | 输出别名 | WPL 类型 |
|---|---|---|
| `f` | `f` | `chars` |
| `name` | `name` | `chars` |
| `client_id` | `client_id` | `chars` |
| `eid` | `eid` | `chars` |
| `number` | `number` | `chars` |
| `device_id` | `device_id` | `chars` |
| `usb_type` | `usb_type` | `chars` |
| `log_report_type` | `log_report_type` | `chars` |
| `is_register` | `is_register` | `chars` |
| `log_type` | `src_log_type` | `chars` |
| `out_valid_day` | `out_valid_day` | `chars` |
| `usb_status` | `usb_status` | `chars` |
| `supplier` | `supplier` | `chars` |
| `pid` | `pid` | `chars` |
| `vid` | `vid` | `chars` |
| `server_id` | `server_id` | `chars` |
| `user_name` | `user_name` | `chars` |
| `capacity` | `capacity` | `chars` |
| `is_roam` | `is_roam` | `chars` |
| `out_permission` | `out_permission` | `chars` |
| `is_intranet` | `is_intranet` | `chars` |
| `detail` | `detail` | `chars` |
| `label_name` | `label_name` | `chars` |
| `result` | `result` | `chars` |
| `user_number` | `user_number` | `chars` |
| `operation_time` | `operation_time` | `chars` |
| `source` | `source` | `chars` |
| `destination` | `destination` | `chars` |
| `client_report_ip` | `client_report_ip` | `chars` |
| `report_ip` | `report_ip` | `chars` |
| `client_report_ipv6` | `client_report_ipv6` | `chars` |
| `report_ipv6` | `report_ipv6` | `chars` |
| `client_type` | `client_type` | `chars` |
| `os` | `os` | `chars` |
| `client_create_time` | `client_create_time` | `chars` |
| `create_time` | `create_time` | `time_timestamp` |
| `client_os_version_release_id` | `client_os_version_release_id` | `chars` |
| `client_tos_version` | `client_tos_version` | `chars` |
| `client_os_version_build_version` | `client_os_version_build_version` | `chars` |
| `client_os_version_main` | `client_os_version_main` | `chars` |
| `client_os_version_describe` | `client_os_version_describe` | `chars` |
| `client_tos_dist` | `client_tos_dist` | `chars` |
| `client_mid` | `client_mid` | `chars` |
| `mid` | `mid` | `chars` |
| `client_sys_space` | `client_sys_space` | `chars` |
| `sys_space` | `sys_space` | `chars` |
| `client_core_number` | `client_core_number` | `chars` |
| `core_number` | `core_number` | `chars` |
| `client_login_account` | `client_login_account` | `chars` |
| `login_account` | `login_account` | `chars` |
| `client_mac` | `client_mac` | `chars` |
| `mac` | `mac` | `chars` |
| `client_memory_size` | `client_memory_size` | `chars` |
| `memory_size` | `memory_size` | `chars` |
| `client_update_time` | `client_update_time` | `chars` |
| `update_time` | `update_time` | `chars` |
| `client_ie_version` | `client_ie_version` | `chars` |
| `ie_version` | `ie_version` | `chars` |
| `client_computer_working_group` | `client_computer_working_group` | `chars` |
| `computer_working_group` | `computer_working_group` | `chars` |
| `client_domain` | `client_domain` | `chars` |
| `domain` | `domain` | `chars` |
| `client_name` | `client_name` | `chars` |
| `client_os` | `client_os` | `chars` |
| `client_tos_os` | `client_tos_os` | `chars` |
| `client_os_bit` | `client_os_bit` | `chars` |
| `os_bit` | `os_bit` | `chars` |
| `client_nic_list` | `client_nic_list` | `chars` |
| `nic_list` | `nic_list` | `chars` |
| `client_state` | `client_state` | `chars` |
| `state` | `state` | `chars` |
| `client_activation` | `client_activation` | `chars` |
| `activation` | `activation` | `chars` |
| `client_system_language` | `client_system_language` | `chars` |
| `system_language` | `system_language` | `chars` |
| `group_node_type` | `group_node_type` | `chars` |
| `node_type` | `node_type` | `chars` |
| `group_tree_id` | `group_tree_id` | `chars` |
| `tree_id` | `tree_id` | `chars` |
| `group_node_name` | `group_node_name` | `chars` |
| `node_name` | `node_name` | `chars` |
| `group_oid` | `group_oid` | `chars` |
| `oid` | `oid` | `chars` |
| `group_node_id` | `group_node_id` | `chars` |
| `node_id` | `node_id` | `chars` |
| `client_ip` | `client_ip` | `chars` |
| `ip` | `ip` | `chars` |
| `asset_id` | `asset_id` | `chars` |
| `asset_oid` | `asset_oid` | `chars` |
| `admin_name` | `admin_name` | `chars` |
| `login_user` | `login_user` | `chars` |
| `user_id` | `user_id` | `chars` |
| `user_info` | `user_info` | `chars` |
| `user_email` | `user_email` | `chars` |
| `user_mobile_phone_number` | `user_mobile_phone_number` | `chars` |
| `user_real_name` | `user_real_name` | `chars` |
| `user_third_id` | `user_third_id` | `chars` |
| `user_group_info` | `user_group_info` | `chars` |
| `user_group_names` | `user_group_names` | `chars` |
| `user_create_time` | `user_create_time` | `chars` |
| `user_update_time` | `user_update_time` | `chars` |
| `user_state` | `user_state` | `chars` |
| `user_source_factor_name` | `user_source_factor_name` | `chars` |
| `user_source_factor` | `user_source_factor` | `chars` |
| `group_node_path` | `group_node_path` | `chars` |
| `client_tos_arch` | `client_tos_arch` | `chars` |
| `search_id` | `search_id` | `chars` |
| `auth_node_id` | `auth_node_id` | `chars` |
| `syslog_topic` | `syslog_topic` | `chars` |
| `path_level1` | `path_level1` | `chars` |
| `path_level2` | `path_level2` | `chars` |
| `path_level3` | `path_level3` | `chars` |
| `path_level4` | `path_level4` | `chars` |
| `path_level5` | `path_level5` | `chars` |
| `path_level6` | `path_level6` | `chars` |
| `path_level7` | `path_level7` | `chars` |
| `path_level8` | `path_level8` | `chars` |
| `path_level9` | `path_level9` | `chars` |
| `path_level10` | `path_level10` | `chars` |
| `user_mobile_phone_country_code` | `user_mobile_phone_country_code` | `chars` |
| `user_source_factor_id` | `user_source_factor_id` | `chars` |
| `out_valid_max_times` | `out_valid_max_times` | `chars` |
| `client_info` | `client_info` | `chars` |
| `client_info/online_info/last_time` | `last_time` | `time` |
| `group_info` | `group_info` | `array` |

#### 组合与映射要点

- 本规则组合输入候选：身份候选：`eid`, `asset_id`；时间候选：`create_time`, `operation_time`；主动方候选：待从样例确认；目标方候选：待从样例确认；载体候选：待从样例确认；检测候选：`result`。
- 从本节字段选择稳定 ID 和事件发生时间；不能直接使用规则名作为 `event_id`。
- 按事实将终端、进程、网络、文件和用户放入 `roles`；不沿用大禹 `attacker/victim` 作为标准角色。
- 将天擎类型、状态、结果转换为受控 `event_type`、`operation`、`outcome`、`severity`；原始值保留在 `source_finding` 或 `extensions`。
- 低频字段进入 `facets`/`extensions` 前必须确认稳定性和调查价值。

### 3.27 `data_breach_event`

- `log_type`：`data_breach_event`
- 描述：天擎数据泄露事件
- 规则过滤：`f_chars_has(syslog_topic, data_leakage_prevent)`
- 建议事件语义：来源检测/安全告警事件；event_category 候选为 alert
- 抽取字段数（按别名去重）：35

| 原始路径 | 输出别名 | WPL 类型 |
|---|---|---|
| `event_id` | `event_id` | `chars` |
| `details` | `details` | `chars` |
| `asset_id` | `asset_id` | `chars` |
| `asset_oid` | `asset_oid` | `chars` |
| `cachet` | `cachet` | `array` |
| `cachet_count` | `cachet_count` | `chars` |
| `channel_id` | `channel_id` | `chars` |
| `channelitem_id` | `channelitem_id` | `chars` |
| `create_time` | `create_time` | `time_timestamp` |
| `event_time` | `event_time` | `time_timestamp` |
| `client_id` | `client_id` | `chars` |
| `client_ip` | `client_ip` | `chars` |
| `client_info/ip` | `ip` | `chars` |
| `client_info/mid` | `mid` | `chars` |
| `client_report_ip` | `client_report_ip` | `chars` |
| `client_info/report_ip` | `report_ip` | `chars` |
| `dest_ip` | `dest_ip` | `chars` |
| `client_info/mac` | `mac` | `chars` |
| `file_download_urls` | `file_download_urls` | `array` |
| `file_md5s` | `file_md5s` | `array` |
| `file_names` | `file_names` | `array` |
| `file_postions` | `file_postions` | `array` |
| `file_sizes` | `file_sizes` | `array` |
| `matchrule_contents` | `matchrule_contents` | `array` |
| `matchrule_name` | `matchrule_name` | `array` |
| `matchrule_number` | `matchrule_number` | `array` |
| `hit_number` | `hit_number` | `chars` |
| `opt_flag` | `opt_flag` | `chars` |
| `severity` | `severity` | `chars` |
| `severity_name` | `severity_name` | `chars` |
| `severity_weight` | `severity_weight` | `chars` |
| `source_ext` | `source_ext` | `chars` |
| `dest_ext` | `dest_ext` | `chars` |
| `timestamp` | `timestamp` | `time_timestamp` |
| `syslog_topic` | `syslog_topic` | `chars` |

#### 组合与映射要点

- 本规则组合输入候选：身份候选：`event_id`, `asset_id`；时间候选：`create_time`, `timestamp`, `event_time`；主动方候选：待从样例确认；目标方候选：待从样例确认；载体候选：待从样例确认；检测候选：待从样例确认。
- 从本节字段选择稳定 ID 和事件发生时间；不能直接使用规则名作为 `event_id`。
- 按事实将终端、进程、网络、文件和用户放入 `roles`；不沿用大禹 `attacker/victim` 作为标准角色。
- 将天擎类型、状态、结果转换为受控 `event_type`、`operation`、`outcome`、`severity`；原始值保留在 `source_finding` 或 `extensions`。
- 低频字段进入 `facets`/`extensions` 前必须确认稳定性和调查价值。

### 3.28 `edr_dns_access`

- `log_type`：`edr_dns_access`
- 描述：天擎EDR_DNS访问
- 规则过滤：`f_chars_has(type, dns_access)`
- 建议事件语义：网络事实事件；event_category 候选为 network
- 抽取字段数（按别名去重）：38

| 原始路径 | 输出别名 | WPL 类型 |
|---|---|---|
| `asset_oid` | `asset_oid` | `chars` |
| `custom_group_paths` | `custom_group_paths` | `chars` |
| `dns_query_results` | `dns_query_results` | `chars` |
| `dns_query_status` | `dns_query_status` | `chars` |
| `dns_typed` | `dns_typed` | `chars` |
| `event_date_creation` | `event_date_creation` | `time_timestamp` |
| `process_parent_command_line` | `process_parent_command_line` | `chars` |
| `process_parent_internal_name` | `process_parent_internal_name` | `chars` |
| `process_parent_name` | `process_parent_name` | `chars` |
| `process_parent_original_name` | `process_parent_original_name` | `chars` |
| `process_parent_sign` | `process_parent_sign` | `chars` |
| `process_sha1` | `process_sha1` | `chars` |
| `timestamp` | `timestamp` | `time_timestamp` |
| `type` | `type` | `chars` |
| `uuid` | `uuid` | `chars` |
| `computer_name` | `computer_name` | `chars` |
| `dns_host_name` | `dns_host_name` | `chars` |
| `dns_host_name_md5` | `dns_host_name_md5` | `chars` |
| `gid` | `gid` | `chars` |
| `process_command_line` | `process_command_line` | `chars` |
| `process_internal_name` | `process_internal_name` | `chars` |
| `process_original_name` | `process_original_name` | `chars` |
| `process_parent_path` | `process_parent_path` | `chars` |
| `process_sign` | `process_sign` | `chars` |
| `process_user` | `process_user` | `chars` |
| `report_ip` | `report_ip` | `chars` |
| `asset_id` | `asset_id` | `chars` |
| `client_id` | `client_id` | `chars` |
| `ip` | `ip` | `chars` |
| `event_type` | `event_type` | `chars` |
| `group_name` | `group_name` | `chars` |
| `mac` | `mac` | `chars` |
| `mid` | `mid` | `chars` |
| `process_guid` | `process_guid` | `chars` |
| `process_id` | `process_id` | `chars` |
| `process_md5` | `process_md5` | `chars` |
| `process_name` | `process_name` | `chars` |
| `process_path` | `process_path` | `chars` |

#### 组合与映射要点

- 本规则组合输入候选：身份候选：`uuid`, `asset_id`；时间候选：`event_date_creation`, `timestamp`；主动方候选：`process_user`；目标方候选：待从样例确认；载体候选：`process_name`, `process_guid`, `process_id`, `process_command_line`；检测候选：待从样例确认。
- 从本节字段选择稳定 ID 和事件发生时间；不能直接使用规则名作为 `event_id`。
- 按事实将终端、进程、网络、文件和用户放入 `roles`；不沿用大禹 `attacker/victim` 作为标准角色。
- 将天擎类型、状态、结果转换为受控 `event_type`、`operation`、`outcome`、`severity`；原始值保留在 `source_finding` 或 `extensions`。
- 低频字段进入 `facets`/`extensions` 前必须确认稳定性和调查价值。

### 3.29 `edr_driver_file_load`

- `log_type`：`edr_driver_file_load`
- 描述：天擎EDR驱动文件加载
- 规则过滤：`f_chars_has(type, driver_loaded)`
- 建议事件语义：进程/系统审计事件；event_category 候选为 audit
- 抽取字段数（按别名去重）：44

| 原始路径 | 输出别名 | WPL 类型 |
|---|---|---|
| `asset_oid` | `asset_oid` | `chars` |
| `custom_group_paths` | `custom_group_paths` | `chars` |
| `event_date_creation` | `event_date_creation` | `time_timestamp` |
| `file_company_name` | `file_company_name` | `chars` |
| `file_description` | `file_description` | `chars` |
| `file_is_signed` | `file_is_signed` | `chars` |
| `file_original_name` | `file_original_name` | `chars` |
| `file_product_name` | `file_product_name` | `chars` |
| `file_sign` | `file_sign` | `chars` |
| `file_sign_status` | `file_sign_status` | `chars` |
| `process_parent_command_line` | `process_parent_command_line` | `chars` |
| `process_parent_internal_name` | `process_parent_internal_name` | `chars` |
| `process_parent_name` | `process_parent_name` | `chars` |
| `process_parent_original_name` | `process_parent_original_name` | `chars` |
| `process_parent_sign` | `process_parent_sign` | `chars` |
| `process_sha1` | `process_sha1` | `chars` |
| `timestamp` | `timestamp` | `time_timestamp` |
| `type` | `type` | `chars` |
| `uuid` | `uuid` | `chars` |
| `computer_name` | `computer_name` | `chars` |
| `gid` | `gid` | `chars` |
| `process_command_line` | `process_command_line` | `chars` |
| `process_internal_name` | `process_internal_name` | `chars` |
| `process_original_name` | `process_original_name` | `chars` |
| `process_parent_path` | `process_parent_path` | `chars` |
| `process_sign` | `process_sign` | `chars` |
| `process_user` | `process_user` | `chars` |
| `report_ip` | `report_ip` | `chars` |
| `asset_id` | `asset_id` | `chars` |
| `client_id` | `client_id` | `chars` |
| `ip` | `ip` | `chars` |
| `event_type` | `event_type` | `chars` |
| `file_md5` | `file_md5` | `chars` |
| `file_name` | `file_name` | `chars` |
| `file_path` | `file_path` | `chars` |
| `file_version` | `file_version` | `chars` |
| `group_name` | `group_name` | `chars` |
| `mac` | `mac` | `chars` |
| `mid` | `mid` | `chars` |
| `process_guid` | `process_guid` | `chars` |
| `process_id` | `process_id` | `chars` |
| `process_md5` | `process_md5` | `chars` |
| `process_name` | `process_name` | `chars` |
| `process_path` | `process_path` | `chars` |

#### 组合与映射要点

- 本规则组合输入候选：身份候选：`uuid`, `asset_id`；时间候选：`event_date_creation`, `timestamp`；主动方候选：`process_user`；目标方候选：`file_path`, `file_name`；载体候选：`process_name`, `process_guid`, `process_id`, `process_command_line`；检测候选：待从样例确认。
- 从本节字段选择稳定 ID 和事件发生时间；不能直接使用规则名作为 `event_id`。
- 按事实将终端、进程、网络、文件和用户放入 `roles`；不沿用大禹 `attacker/victim` 作为标准角色。
- 将天擎类型、状态、结果转换为受控 `event_type`、`operation`、`outcome`、`severity`；原始值保留在 `source_finding` 或 `extensions`。
- 低频字段进入 `facets`/`extensions` 前必须确认稳定性和调查价值。

### 3.30 `edr_file_trans`

- `log_type`：`edr_file_trans`
- 描述：天擎EDR文件传输
- 规则过滤：`f_chars_has(type, file_download)`
- 建议事件语义：文件/数据访问事件；event_category 候选为 audit
- 抽取字段数（按别名去重）：32

| 原始路径 | 输出别名 | WPL 类型 |
|---|---|---|
| `asset_oid` | `asset_oid` | `chars` |
| `custom_group_paths` | `custom_group_paths` | `chars` |
| `event_date_creation` | `event_date_creation` | `time_timestamp` |
| `process_sha1` | `process_sha1` | `chars` |
| `timestamp` | `timestamp` | `time_timestamp` |
| `type` | `type` | `chars` |
| `uuid` | `uuid` | `chars` |
| `computer_name` | `computer_name` | `chars` |
| `file_date_creation` | `file_date_creation` | `time_timestamp` |
| `gid` | `gid` | `chars` |
| `process_command_line` | `process_command_line` | `chars` |
| `process_internal_name` | `process_internal_name` | `chars` |
| `process_sign` | `process_sign` | `chars` |
| `process_user` | `process_user` | `chars` |
| `report_ip` | `report_ip` | `chars` |
| `asset_id` | `asset_id` | `chars` |
| `client_id` | `client_id` | `chars` |
| `ip` | `ip` | `chars` |
| `event_type` | `event_type` | `chars` |
| `file_md5` | `file_md5` | `chars` |
| `file_name` | `file_name` | `chars` |
| `file_path` | `file_path` | `chars` |
| `file_sha1` | `file_sha1` | `chars` |
| `file_size` | `file_size` | `chars` |
| `group_name` | `group_name` | `chars` |
| `mac` | `mac` | `chars` |
| `mid` | `mid` | `chars` |
| `process_guid` | `process_guid` | `chars` |
| `process_id` | `process_id` | `chars` |
| `process_md5` | `process_md5` | `chars` |
| `process_name` | `process_name` | `chars` |
| `process_path` | `process_path` | `chars` |

#### 组合与映射要点

- 本规则组合输入候选：身份候选：`uuid`, `asset_id`；时间候选：`event_date_creation`, `timestamp`；主动方候选：`process_user`；目标方候选：`file_path`, `file_name`；载体候选：`process_name`, `process_guid`, `process_id`, `process_command_line`；检测候选：待从样例确认。
- 从本节字段选择稳定 ID 和事件发生时间；不能直接使用规则名作为 `event_id`。
- 按事实将终端、进程、网络、文件和用户放入 `roles`；不沿用大禹 `attacker/victim` 作为标准角色。
- 将天擎类型、状态、结果转换为受控 `event_type`、`operation`、`outcome`、`severity`；原始值保留在 `source_finding` 或 `extensions`。
- 低频字段进入 `facets`/`extensions` 前必须确认稳定性和调查价值。

### 3.31 `edr_fileless_script_behavior_event`

- `log_type`：`edr_fileless_script_behavior_event`
- 描述：天擎EDR无文件脚本行为事件
- 规则过滤：`f_chars_has(type, memory_script_action)`
- 建议事件语义：文件/数据访问事件；event_category 候选为 audit
- 抽取字段数（按别名去重）：52

| 原始路径 | 输出别名 | WPL 类型 |
|---|---|---|
| `asset_id` | `asset_id` | `chars` |
| `asset_oid` | `asset_oid` | `chars` |
| `client_id` | `client_id` | `chars` |
| `ip` | `ip` | `chars` |
| `computer_name` | `computer_name` | `chars` |
| `custom_group_paths` | `custom_group_paths` | `chars` |
| `event_date_creation` | `event_date_creation` | `time_timestamp` |
| `event_type` | `event_type` | `chars` |
| `execute_method_argc` | `execute_method_argc` | `chars` |
| `execute_method_args` | `execute_method_args` | `chars` |
| `execute_method_name` | `execute_method_name` | `chars` |
| `execute_method_type` | `execute_method_type` | `chars` |
| `executed_command_line` | `executed_command_line` | `chars` |
| `file_md5` | `file_md5` | `chars` |
| `file_name` | `file_name` | `chars` |
| `file_path` | `file_path` | `chars` |
| `gid` | `gid` | `chars` |
| `group_name` | `group_name` | `chars` |
| `mac` | `mac` | `chars` |
| `mid` | `mid` | `chars` |
| `process_command_line` | `process_command_line` | `chars` |
| `process_granted_access` | `process_granted_access` | `chars` |
| `process_guid` | `process_guid` | `chars` |
| `process_id` | `process_id` | `chars` |
| `process_internal_name` | `process_internal_name` | `chars` |
| `process_md5` | `process_md5` | `chars` |
| `process_name` | `process_name` | `chars` |
| `process_original_name` | `process_original_name` | `chars` |
| `process_parent_command_line` | `process_parent_command_line` | `chars` |
| `process_parent_internal_name` | `process_parent_internal_name` | `chars` |
| `process_parent_name` | `process_parent_name` | `chars` |
| `process_parent_original_name` | `process_parent_original_name` | `chars` |
| `process_parent_path` | `process_parent_path` | `chars` |
| `process_parent_sign` | `process_parent_sign` | `chars` |
| `process_path` | `process_path` | `chars` |
| `process_sha1` | `process_sha1` | `chars` |
| `process_sign` | `process_sign` | `chars` |
| `process_user` | `process_user` | `chars` |
| `report_ip` | `report_ip` | `chars` |
| `script_file_context` | `script_file_context` | `chars` |
| `script_file_md5` | `script_file_md5` | `chars` |
| `script_file_path` | `script_file_path` | `chars` |
| `target_process_command_line` | `target_process_command_line` | `chars` |
| `target_process_md5` | `target_process_md5` | `chars` |
| `target_process_name` | `target_process_name` | `chars` |
| `target_process_path` | `target_process_path` | `chars` |
| `target_process_sign` | `target_process_sign` | `chars` |
| `target_thread_id` | `target_thread_id` | `chars` |
| `timestamp` | `timestamp` | `time_timestamp` |
| `type` | `type` | `chars` |
| `url_context` | `url_context` | `chars` |
| `operation_memory_size` | `operation_memory_size` | `chars` |

#### 组合与映射要点

- 本规则组合输入候选：身份候选：`asset_id`；时间候选：`event_date_creation`, `timestamp`；主动方候选：`process_user`；目标方候选：`file_path`, `file_name`；载体候选：`process_name`, `process_guid`, `process_id`, `process_command_line`；检测候选：待从样例确认。
- 从本节字段选择稳定 ID 和事件发生时间；不能直接使用规则名作为 `event_id`。
- 按事实将终端、进程、网络、文件和用户放入 `roles`；不沿用大禹 `attacker/victim` 作为标准角色。
- 将天擎类型、状态、结果转换为受控 `event_type`、`operation`、`outcome`、`severity`；原始值保留在 `source_finding` 或 `extensions`。
- 低频字段进入 `facets`/`extensions` 前必须确认稳定性和调查价值。

### 3.32 `edr_im_audit`

- `log_type`：`edr_im_audit`
- 描述：天擎V10IM审计日志
- 规则过滤：`f_chars_has(syslog_topic, im_audit)`
- 建议事件语义：身份/账号审计事件；event_category 候选为 auth 或 audit，需按事实确认
- 抽取字段数（按别名去重）：20

| 原始路径 | 输出别名 | WPL 类型 |
|---|---|---|
| `asset_oid` | `asset_oid` | `chars` |
| `asset_id` | `asset_id` | `chars` |
| `client_id` | `client_id` | `chars` |
| `client_mac` | `client_mac` | `chars` |
| `client_ip` | `client_ip` | `chars` |
| `client_info/ip` | `ip` | `chars` |
| `client_report_ip` | `client_report_ip` | `chars` |
| `client_info/report_ip` | `report_ip` | `chars` |
| `create_time` | `create_time` | `time_timestamp` |
| `report_time` | `report_time` | `time_timestamp` |
| `software_name` | `software_name` | `chars` |
| `process_name` | `process_name` | `chars` |
| `event_detail` | `event_detail` | `chars` |
| `local_account` | `local_account` | `chars` |
| `remote_account` | `remote_account` | `chars` |
| `chat_message` | `chat_message` | `chars` |
| `file_size` | `file_size` | `chars` |
| `action` | `action` | `chars` |
| `message_type` | `message_type` | `chars` |
| `syslog_topic` | `syslog_topic` | `chars` |

#### 组合与映射要点

- 本规则组合输入候选：身份候选：`asset_id`；时间候选：`create_time`；主动方候选：待从样例确认；目标方候选：待从样例确认；载体候选：`process_name`；检测候选：待从样例确认。
- 从本节字段选择稳定 ID 和事件发生时间；不能直接使用规则名作为 `event_id`。
- 按事实将终端、进程、网络、文件和用户放入 `roles`；不沿用大禹 `attacker/victim` 作为标准角色。
- 将天擎类型、状态、结果转换为受控 `event_type`、`operation`、`outcome`、`severity`；原始值保留在 `source_finding` 或 `extensions`。
- 低频字段进入 `facets`/`extensions` 前必须确认稳定性和调查价值。

### 3.33 `edr_image_file_load`

- `log_type`：`edr_image_file_load`
- 描述：天擎EDR映像文件加载
- 规则过滤：`f_chars_has(type, image_loaded)`
- 建议事件语义：文件/数据访问事件；event_category 候选为 audit
- 抽取字段数（按别名去重）：45

| 原始路径 | 输出别名 | WPL 类型 |
|---|---|---|
| `asset_oid` | `asset_oid` | `chars` |
| `custom_group_paths` | `custom_group_paths` | `chars` |
| `event_date_creation` | `event_date_creation` | `time_timestamp` |
| `file_company_name` | `file_company_name` | `chars` |
| `file_description` | `file_description` | `chars` |
| `file_internal_name` | `file_internal_name` | `chars` |
| `file_is_signed` | `file_is_signed` | `chars` |
| `file_original_name` | `file_original_name` | `chars` |
| `file_product_name` | `file_product_name` | `chars` |
| `file_sign` | `file_sign` | `chars` |
| `file_sign_status` | `file_sign_status` | `chars` |
| `process_parent_command_line` | `process_parent_command_line` | `chars` |
| `process_parent_internal_name` | `process_parent_internal_name` | `chars` |
| `process_parent_name` | `process_parent_name` | `chars` |
| `process_parent_original_name` | `process_parent_original_name` | `chars` |
| `process_parent_sign` | `process_parent_sign` | `chars` |
| `process_sha1` | `process_sha1` | `chars` |
| `timestamp` | `timestamp` | `time_timestamp` |
| `type` | `type` | `chars` |
| `uuid` | `uuid` | `chars` |
| `computer_name` | `computer_name` | `chars` |
| `gid` | `gid` | `chars` |
| `process_command_line` | `process_command_line` | `chars` |
| `process_internal_name` | `process_internal_name` | `chars` |
| `process_original_name` | `process_original_name` | `chars` |
| `process_parent_path` | `process_parent_path` | `chars` |
| `process_sign` | `process_sign` | `chars` |
| `process_user` | `process_user` | `chars` |
| `report_ip` | `report_ip` | `chars` |
| `asset_id` | `asset_id` | `chars` |
| `client_id` | `client_id` | `chars` |
| `ip` | `ip` | `chars` |
| `event_type` | `event_type` | `chars` |
| `file_md5` | `file_md5` | `chars` |
| `file_name` | `file_name` | `chars` |
| `file_path` | `file_path` | `chars` |
| `file_version` | `file_version` | `chars` |
| `group_name` | `group_name` | `chars` |
| `mac` | `mac` | `chars` |
| `mid` | `mid` | `chars` |
| `process_guid` | `process_guid` | `chars` |
| `process_id` | `process_id` | `chars` |
| `process_md5` | `process_md5` | `chars` |
| `process_name` | `process_name` | `chars` |
| `process_path` | `process_path` | `chars` |

#### 组合与映射要点

- 本规则组合输入候选：身份候选：`uuid`, `asset_id`；时间候选：`event_date_creation`, `timestamp`；主动方候选：`process_user`；目标方候选：`file_path`, `file_name`；载体候选：`process_name`, `process_guid`, `process_id`, `process_command_line`；检测候选：待从样例确认。
- 从本节字段选择稳定 ID 和事件发生时间；不能直接使用规则名作为 `event_id`。
- 按事实将终端、进程、网络、文件和用户放入 `roles`；不沿用大禹 `attacker/victim` 作为标准角色。
- 将天擎类型、状态、结果转换为受控 `event_type`、`operation`、`outcome`、`severity`；原始值保留在 `source_finding` 或 `extensions`。
- 低频字段进入 `facets`/`extensions` 前必须确认稳定性和调查价值。

### 3.34 `edr_ip_access`

- `log_type`：`edr_ip_access`
- 描述：天擎EDR_IP访问
- 规则过滤：`f_chars_has(type, ip_access)`
- 建议事件语义：网络事实事件；event_category 候选为 network
- 抽取字段数（按别名去重）：45

| 原始路径 | 输出别名 | WPL 类型 |
|---|---|---|
| `asset_oid` | `asset_oid` | `chars` |
| `custom_group_paths` | `custom_group_paths` | `chars` |
| `dst_host_name` | `dst_host_name` | `chars` |
| `dst_is_ipv6` | `dst_is_ipv6` | `chars` |
| `event_date_creation` | `event_date_creation` | `time_timestamp` |
| `inout` | `inout` | `chars` |
| `network_connection_initiated` | `network_connection_initiated` | `chars` |
| `process_parent_command_line` | `process_parent_command_line` | `chars` |
| `process_parent_internal_name` | `process_parent_internal_name` | `chars` |
| `process_parent_name` | `process_parent_name` | `chars` |
| `process_parent_original_name` | `process_parent_original_name` | `chars` |
| `process_parent_sign` | `process_parent_sign` | `chars` |
| `process_sha1` | `process_sha1` | `chars` |
| `src_host_name` | `src_host_name` | `chars` |
| `src_is_ipv6` | `src_is_ipv6` | `chars` |
| `timestamp` | `timestamp` | `time_timestamp` |
| `type` | `type` | `chars` |
| `uuid` | `uuid` | `chars` |
| `computer_name` | `computer_name` | `chars` |
| `dst_ip_addr` | `dst_ip_addr` | `chars` |
| `dst_port` | `dst_port` | `chars` |
| `gid` | `gid` | `chars` |
| `network_protocol` | `network_protocol` | `chars` |
| `process_command_line` | `process_command_line` | `chars` |
| `process_internal_name` | `process_internal_name` | `chars` |
| `process_original_name` | `process_original_name` | `chars` |
| `process_parent_path` | `process_parent_path` | `chars` |
| `process_sign` | `process_sign` | `chars` |
| `process_user` | `process_user` | `chars` |
| `process_version` | `process_version` | `chars` |
| `report_ip` | `report_ip` | `chars` |
| `src_ip_addr` | `src_ip_addr` | `chars` |
| `src_port` | `src_port` | `digit` |
| `asset_id` | `asset_id` | `chars` |
| `client_id` | `client_id` | `chars` |
| `ip` | `ip` | `chars` |
| `event_type` | `event_type` | `chars` |
| `group_name` | `group_name` | `chars` |
| `mac` | `mac` | `chars` |
| `mid` | `mid` | `chars` |
| `process_guid` | `process_guid` | `chars` |
| `process_id` | `process_id` | `chars` |
| `process_md5` | `process_md5` | `chars` |
| `process_name` | `process_name` | `chars` |
| `process_path` | `process_path` | `chars` |

#### 组合与映射要点

- 本规则组合输入候选：身份候选：`uuid`, `asset_id`；时间候选：`event_date_creation`, `timestamp`；主动方候选：`src_ip_addr`, `process_user`；目标方候选：`dst_ip_addr`；载体候选：`process_name`, `process_guid`, `process_id`, `process_command_line`, `network_protocol`；检测候选：待从样例确认。
- 从本节字段选择稳定 ID 和事件发生时间；不能直接使用规则名作为 `event_id`。
- 按事实将终端、进程、网络、文件和用户放入 `roles`；不沿用大禹 `attacker/victim` 作为标准角色。
- 将天擎类型、状态、结果转换为受控 `event_type`、`operation`、`outcome`、`severity`；原始值保留在 `source_finding` 或 `extensions`。
- 低频字段进入 `facets`/`extensions` 前必须确认稳定性和调查价值。

### 3.35 `edr_mail_attachment_trans`

- `log_type`：`edr_mail_attachment_trans`
- 描述：天擎EDR_V10_邮件附件传输
- 规则过滤：`f_chars_has(type, mail_files)`
- 建议事件语义：文件/数据访问事件；event_category 候选为 audit
- 抽取字段数（按别名去重）：30

| 原始路径 | 输出别名 | WPL 类型 |
|---|---|---|
| `asset_oid` | `asset_oid` | `chars` |
| `custom_group_paths` | `custom_group_paths` | `chars` |
| `event_date_creation` | `event_date_creation` | `time_timestamp` |
| `process_sha1` | `process_sha1` | `chars` |
| `timestamp` | `timestamp` | `time_timestamp` |
| `type` | `type` | `chars` |
| `uuid` | `uuid` | `chars` |
| `computer_name` | `computer_name` | `chars` |
| `from` | `from` | `chars` |
| `gid` | `gid` | `chars` |
| `process_command_line` | `process_command_line` | `chars` |
| `process_internal_name` | `process_internal_name` | `chars` |
| `process_sign` | `process_sign` | `chars` |
| `process_user` | `process_user` | `chars` |
| `report_ip` | `report_ip` | `chars` |
| `subject` | `subject` | `chars` |
| `to` | `to` | `chars` |
| `asset_id` | `asset_id` | `chars` |
| `attachment` | `attachment` | `chars` |
| `client_id` | `client_id` | `chars` |
| `event_type` | `event_type` | `chars` |
| `group_name` | `group_name` | `chars` |
| `mac` | `mac` | `chars` |
| `mid` | `mid` | `chars` |
| `process_guid` | `process_guid` | `chars` |
| `process_id` | `process_id` | `chars` |
| `process_md5` | `process_md5` | `chars` |
| `process_name` | `process_name` | `chars` |
| `process_path` | `process_path` | `chars` |
| `ip` | `ip` | `chars` |

#### 组合与映射要点

- 本规则组合输入候选：身份候选：`uuid`, `asset_id`；时间候选：`event_date_creation`, `timestamp`；主动方候选：`process_user`；目标方候选：待从样例确认；载体候选：`process_name`, `process_guid`, `process_id`, `process_command_line`；检测候选：待从样例确认。
- 从本节字段选择稳定 ID 和事件发生时间；不能直接使用规则名作为 `event_id`。
- 按事实将终端、进程、网络、文件和用户放入 `roles`；不沿用大禹 `attacker/victim` 作为标准角色。
- 将天擎类型、状态、结果转换为受控 `event_type`、`operation`、`outcome`、`severity`；原始值保留在 `source_finding` 或 `extensions`。
- 低频字段进入 `facets`/`extensions` 前必须确认稳定性和调查价值。

### 3.36 `edr_mail_audit`

- `log_type`：`edr_mail_audit`
- 描述：天擎V10邮件审计日志
- 规则过滤：`f_chars_has(syslog_topic, mail_audit)`
- 建议事件语义：待确认事件语义
- 抽取字段数（按别名去重）：19

| 原始路径 | 输出别名 | WPL 类型 |
|---|---|---|
| `asset_oid` | `asset_oid` | `chars` |
| `asset_id` | `asset_id` | `chars` |
| `client_id` | `client_id` | `chars` |
| `client_mac` | `client_mac` | `chars` |
| `client_ip` | `client_ip` | `chars` |
| `client_info/ip` | `ip` | `chars` |
| `client_report_ip` | `client_report_ip` | `chars` |
| `client_info/report_ip` | `report_ip` | `chars` |
| `create_time` | `create_time` | `time_timestamp` |
| `report_time` | `report_time` | `time_timestamp` |
| `process_name` | `process_name` | `chars` |
| `sender_urls` | `sender_urls` | `chars` |
| `addressee_urls` | `addressee_urls` | `chars` |
| `mail_title` | `mail_title` | `chars` |
| `send_copy` | `send_copy` | `chars` |
| `enclosure_name` | `enclosure_name` | `chars` |
| `message_body` | `message_body` | `chars` |
| `enclosure_detail` | `enclosure_detail` | `array` |
| `syslog_topic` | `syslog_topic` | `chars` |

#### 组合与映射要点

- 本规则组合输入候选：身份候选：`asset_id`；时间候选：`create_time`；主动方候选：待从样例确认；目标方候选：待从样例确认；载体候选：`process_name`；检测候选：待从样例确认。
- 从本节字段选择稳定 ID 和事件发生时间；不能直接使用规则名作为 `event_id`。
- 按事实将终端、进程、网络、文件和用户放入 `roles`；不沿用大禹 `attacker/victim` 作为标准角色。
- 将天擎类型、状态、结果转换为受控 `event_type`、`operation`、`outcome`、`severity`；原始值保留在 `source_finding` 或 `extensions`。
- 低频字段进入 `facets`/`extensions` 前必须确认稳定性和调查价值。

### 3.37 `edr_memory_shield_log`

- `log_type`：`edr_memory_shield_log`
- 描述：天擎EDR内存执行日志
- 规则过滤：`f_chars_has(type, memory_shield)`
- 建议事件语义：进程/系统审计事件；event_category 候选为 audit
- 抽取字段数（按别名去重）：38

| 原始路径 | 输出别名 | WPL 类型 |
|---|---|---|
| `asset_id` | `asset_id` | `chars` |
| `asset_oid` | `asset_oid` | `chars` |
| `client_id` | `client_id` | `chars` |
| `computer_name` | `computer_name` | `chars` |
| `event_date_creation` | `event_date_creation` | `time_timestamp` |
| `event_type` | `event_type` | `chars` |
| `injected_dll` | `injected_dll` | `chars` |
| `ip` | `ip` | `chars` |
| `mac` | `mac` | `chars` |
| `report_ip` | `report_ip` | `chars` |
| `mid` | `mid` | `chars` |
| `module_file_path` | `module_file_path` | `chars` |
| `process_call_trace` | `process_call_trace` | `chars` |
| `process_command_line` | `process_command_line` | `chars` |
| `process_files_chain` | `process_files_chain` | `chars` |
| `process_guid` | `process_guid` | `chars` |
| `process_id` | `process_id` | `chars` |
| `process_internal_name` | `process_internal_name` | `chars` |
| `process_md5` | `process_md5` | `chars` |
| `process_name` | `process_name` | `chars` |
| `process_original_name` | `process_original_name` | `chars` |
| `process_path` | `process_path` | `chars` |
| `process_sha1` | `process_sha1` | `chars` |
| `process_sign` | `process_sign` | `chars` |
| `process_user` | `process_user` | `chars` |
| `process_parent_command_line` | `process_parent_command_line` | `chars` |
| `process_parent_internal_name` | `process_parent_internal_name` | `chars` |
| `process_parent_name` | `process_parent_name` | `chars` |
| `process_parent_original_name` | `process_parent_original_name` | `chars` |
| `process_parent_path` | `process_parent_path` | `chars` |
| `process_parent_sign` | `process_parent_sign` | `chars` |
| `target_process_command_line` | `target_process_command_line` | `chars` |
| `target_process_id` | `target_process_id` | `chars` |
| `target_process_md5` | `target_process_md5` | `chars` |
| `target_process_name` | `target_process_name` | `chars` |
| `target_process_path` | `target_process_path` | `chars` |
| `target_process_sign` | `target_process_sign` | `chars` |
| `type` | `type` | `chars` |

#### 组合与映射要点

- 本规则组合输入候选：身份候选：`asset_id`；时间候选：`event_date_creation`；主动方候选：`process_user`；目标方候选：待从样例确认；载体候选：`process_name`, `process_guid`, `process_id`, `process_command_line`；检测候选：待从样例确认。
- 从本节字段选择稳定 ID 和事件发生时间；不能直接使用规则名作为 `event_id`。
- 按事实将终端、进程、网络、文件和用户放入 `roles`；不沿用大禹 `attacker/victim` 作为标准角色。
- 将天擎类型、状态、结果转换为受控 `event_type`、`operation`、`outcome`、`severity`；原始值保留在 `source_finding` 或 `extensions`。
- 低频字段进入 `facets`/`extensions` 前必须确认稳定性和调查价值。

### 3.38 `edr_mobile_storage_web_log`

- `log_type`：`edr_mobile_storage_web_log`
- 描述：天擎移动存储WEB端日志
- 规则过滤：`f_chars_has(syslog_topic, mobile_storage_web_log)`
- 建议事件语义：文件/数据访问事件；event_category 候选为 audit
- 抽取字段数（按别名去重）：27

| 原始路径 | 输出别名 | WPL 类型 |
|---|---|---|
| `name` | `name` | `chars` |
| `register_node_id` | `register_node_id` | `chars` |
| `register_node_name` | `register_node_name` | `chars` |
| `register_node_path` | `register_node_path` | `chars` |
| `eid` | `eid` | `chars` |
| `number` | `number` | `chars` |
| `usb_type` | `usb_type` | `chars` |
| `usb_status` | `usb_status` | `chars` |
| `log_report_type` | `log_report_type` | `chars` |
| `pid` | `pid` | `chars` |
| `vid` | `vid` | `chars` |
| `server_id` | `server_id` | `chars` |
| `user_name` | `user_name` | `chars` |
| `capacity` | `capacity` | `chars` |
| `is_roam` | `is_roam` | `chars` |
| `out_permission` | `out_permission` | `chars` |
| `label_name` | `label_name` | `chars` |
| `log_type` | `a` | `chars` |
| `admin_name` | `admin_name` | `chars` |
| `device_id` | `device_id` | `chars` |
| `out_valid_day` | `out_valid_day` | `chars` |
| `result` | `result` | `chars` |
| `user_number` | `user_number` | `chars` |
| `create_time` | `create_time` | `time_timestamp` |
| `asset_oid` | `asset_oid` | `chars` |
| `asset_id` | `asset_id` | `chars` |
| `syslog_topic` | `syslog_topic` | `chars` |

#### 组合与映射要点

- 本规则组合输入候选：身份候选：`eid`, `asset_id`；时间候选：`create_time`；主动方候选：待从样例确认；目标方候选：待从样例确认；载体候选：待从样例确认；检测候选：`result`。
- 从本节字段选择稳定 ID 和事件发生时间；不能直接使用规则名作为 `event_id`。
- 按事实将终端、进程、网络、文件和用户放入 `roles`；不沿用大禹 `attacker/victim` 作为标准角色。
- 将天擎类型、状态、结果转换为受控 `event_type`、`operation`、`outcome`、`severity`；原始值保留在 `source_finding` 或 `extensions`。
- 低频字段进入 `facets`/`extensions` 前必须确认稳定性和调查价值。

### 3.39 `edr_name_pipe_event`

- `log_type`：`edr_name_pipe_event`
- 描述：天擎EDR命名管道事件
- 规则过滤：`f_chars_has(type, pipe_event)`
- 建议事件语义：进程/系统审计事件；event_category 候选为 audit
- 抽取字段数（按别名去重）：27

| 原始路径 | 输出别名 | WPL 类型 |
|---|---|---|
| `asset_oid` | `asset_oid` | `chars` |
| `custom_group_paths` | `custom_group_paths` | `chars` |
| `event_date_creation` | `event_date_creation` | `time_timestamp` |
| `process_sha1` | `process_sha1` | `chars` |
| `timestamp` | `timestamp` | `time_timestamp` |
| `type` | `type` | `chars` |
| `uuid` | `uuid` | `chars` |
| `computer_name` | `computer_name` | `chars` |
| `gid` | `gid` | `chars` |
| `process_command_line` | `process_command_line` | `chars` |
| `process_internal_name` | `process_internal_name` | `chars` |
| `process_sign` | `process_sign` | `chars` |
| `process_user` | `process_user` | `chars` |
| `report_ip` | `report_ip` | `chars` |
| `asset_id` | `asset_id` | `chars` |
| `client_id` | `client_id` | `chars` |
| `ip` | `ip` | `chars` |
| `event_type` | `event_type` | `chars` |
| `group_name` | `group_name` | `chars` |
| `mac` | `mac` | `chars` |
| `mid` | `mid` | `chars` |
| `pipe_name` | `pipe_name` | `chars` |
| `process_guid` | `process_guid` | `chars` |
| `process_id` | `process_id` | `chars` |
| `process_md5` | `process_md5` | `chars` |
| `process_name` | `process_name` | `chars` |
| `process_path` | `process_path` | `chars` |

#### 组合与映射要点

- 本规则组合输入候选：身份候选：`uuid`, `asset_id`；时间候选：`event_date_creation`, `timestamp`；主动方候选：`process_user`；目标方候选：待从样例确认；载体候选：`process_name`, `process_guid`, `process_id`, `process_command_line`；检测候选：待从样例确认。
- 从本节字段选择稳定 ID 和事件发生时间；不能直接使用规则名作为 `event_id`。
- 按事实将终端、进程、网络、文件和用户放入 `roles`；不沿用大禹 `attacker/victim` 作为标准角色。
- 将天擎类型、状态、结果转换为受控 `event_type`、`operation`、`outcome`、`severity`；原始值保留在 `source_finding` 或 `extensions`。
- 低频字段进入 `facets`/`extensions` 前必须确认稳定性和调查价值。

### 3.40 `edr_patch_info`

- `log_type`：`edr_patch_info`
- 描述：天擎补丁管理日志
- 规则过滤：`f_chars_has(syslog_topic, patch_log)`
- 建议事件语义：资产/配置/状态事件；event_category 候选为 system 或 audit
- 抽取字段数（按别名去重）：56

| 原始路径 | 输出别名 | WPL 类型 |
|---|---|---|
| `patch_cnnid` | `patch_cnnid` | `array` |
| `patch_all_num` | `patch_all_num` | `chars` |
| `patch_info/cloud_patch_status` | `cloud_patch_status` | `chars` |
| `patch_cnurl` | `patch_cnurl` | `chars` |
| `patch_current_version` | `patch_current_version` | `chars` |
| `patch_cveid` | `patch_cveid` | `array` |
| `patch_description` | `patch_description` | `chars` |
| `patch_exist_num` | `patch_exist_num` | `chars` |
| `patch_initial_version` | `patch_initial_version` | `chars` |
| `patch_issues` | `patch_issues` | `chars` |
| `patch_name` | `patch_name` | `chars` |
| `patch_os_type` | `patch_os_type` | `chars` |
| `patch_info/patch_file_details` | `patch_path_file_details` | `array` |
| `patch_patch_type` | `patch_patch_type` | `chars` |
| `patch_publish_date` | `patch_publish_date` | `chars` |
| `patch_restart` | `patch_restart` | `chars` |
| `patch_superseded` | `patch_superseded` | `array` |
| `patch_supersedes` | `patch_supersedes` | `array` |
| `patch_info` | `patch_info` | `chars` |
| `search_id` | `search_id` | `chars` |
| `patch_level` | `patch_level` | `chars` |
| `client_report_ip` | `client_report_ip` | `chars` |
| `client_info/report_ip` | `report_ip` | `chars` |
| `client_info/os` | `os` | `digit` |
| `create_time` | `create_time` | `time_timestamp` |
| `client_info/os_version/release_id` | `release_id` | `chars` |
| `client_info/os_version/build_version` | `build_version` | `chars` |
| `client_info/os_version/main` | `main` | `chars` |
| `client_info/os_version/describe` | `describe` | `chars` |
| `client_info/mid` | `mid` | `chars` |
| `client_info/sys_space` | `sys_space` | `chars` |
| `client_info/core_number` | `core_number` | `digit` |
| `client_info/login_account` | `login_account` | `chars` |
| `client_info/mac` | `mac` | `chars` |
| `client_info/memory_size` | `memory_size` | `digit` |
| `client_info/update_time` | `update_time` | `time` |
| `client_info/ie_version` | `ie_version` | `chars` |
| `client_info/computer_working_group` | `computer_working_group` | `chars` |
| `client_info/domain` | `domain` | `chars` |
| `client_info/name` | `name` | `chars` |
| `client_info/os_bit` | `os_bit` | `chars` |
| `client_info/nic_list` | `nic_list` | `array` |
| `client_info/report_ipv6` | `report_ipv6` | `chars` |
| `client_info/state` | `state` | `chars` |
| `client_info/activation` | `activation` | `chars` |
| `client_info/system_language` | `system_language` | `chars` |
| `group_info/node_type` | `node_type` | `chars` |
| `group_info/tree_id` | `tree_id` | `chars` |
| `group_info/node_name` | `node_name` | `chars` |
| `group_info/oid` | `oid` | `chars` |
| `group_info/node_id` | `node_id` | `chars` |
| `client_ip` | `client_ip` | `chars` |
| `client_info/ip` | `ip` | `chars` |
| `asset_oid` | `asset_oid` | `chars` |
| `asset_id` | `asset_id` | `chars` |
| `syslog_topic` | `syslog_topic` | `chars` |

#### 组合与映射要点

- 本规则组合输入候选：身份候选：`asset_id`；时间候选：`create_time`；主动方候选：待从样例确认；目标方候选：待从样例确认；载体候选：待从样例确认；检测候选：待从样例确认。
- 从本节字段选择稳定 ID 和事件发生时间；不能直接使用规则名作为 `event_id`。
- 按事实将终端、进程、网络、文件和用户放入 `roles`；不沿用大禹 `attacker/victim` 作为标准角色。
- 将天擎类型、状态、结果转换为受控 `event_type`、`operation`、`outcome`、`severity`；原始值保留在 `source_finding` 或 `extensions`。
- 低频字段进入 `facets`/`extensions` 前必须确认稳定性和调查价值。

### 3.41 `edr_print_audit`

- `log_type`：`edr_print_audit`
- 描述：天擎V10打印审计日志
- 规则过滤：`f_chars_has(syslog_topic, print_audit)`
- 建议事件语义：待确认事件语义
- 抽取字段数（按别名去重）：15

| 原始路径 | 输出别名 | WPL 类型 |
|---|---|---|
| `asset_oid` | `asset_oid` | `chars` |
| `asset_id` | `asset_id` | `chars` |
| `client_id` | `client_id` | `chars` |
| `client_mac` | `client_mac` | `chars` |
| `client_ip` | `client_ip` | `chars` |
| `client_info/ip` | `ip` | `chars` |
| `client_report_ip` | `client_report_ip` | `chars` |
| `client_info/report_ip` | `report_ip` | `chars` |
| `create_time` | `create_time` | `time_timestamp` |
| `report_time` | `report_time` | `time_timestamp` |
| `process_name` | `process_name` | `chars` |
| `event_detail` | `event_detail` | `chars` |
| `print_title` | `print_title` | `chars` |
| `file_size` | `file_size` | `digit` |
| `syslog_topic` | `syslog_topic` | `chars` |

#### 组合与映射要点

- 本规则组合输入候选：身份候选：`asset_id`；时间候选：`create_time`；主动方候选：待从样例确认；目标方候选：待从样例确认；载体候选：`process_name`；检测候选：待从样例确认。
- 从本节字段选择稳定 ID 和事件发生时间；不能直接使用规则名作为 `event_id`。
- 按事实将终端、进程、网络、文件和用户放入 `roles`；不沿用大禹 `attacker/victim` 作为标准角色。
- 将天擎类型、状态、结果转换为受控 `event_type`、`operation`、`outcome`、`severity`；原始值保留在 `source_finding` 或 `extensions`。
- 低频字段进入 `facets`/`extensions` 前必须确认稳定性和调查价值。

### 3.42 `edr_process_inject`

- `log_type`：`edr_process_inject`
- 描述：天擎EDR进程注入
- 规则过滤：`f_chars_has(type, process_injection)`
- 建议事件语义：进程/系统审计事件；event_category 候选为 audit
- 抽取字段数（按别名去重）：39

| 原始路径 | 输出别名 | WPL 类型 |
|---|---|---|
| `asset_oid` | `asset_oid` | `chars` |
| `custom_group_paths` | `custom_group_paths` | `chars` |
| `event_date_creation` | `event_date_creation` | `time_timestamp` |
| `process_parent_command_line` | `process_parent_command_line` | `chars` |
| `process_parent_internal_name` | `process_parent_internal_name` | `chars` |
| `process_parent_name` | `process_parent_name` | `chars` |
| `process_parent_original_name` | `process_parent_original_name` | `chars` |
| `process_parent_sign` | `process_parent_sign` | `chars` |
| `process_sha1` | `process_sha1` | `chars` |
| `target_process_guid` | `target_process_guid` | `chars` |
| `target_process_id` | `target_process_id` | `chars` |
| `target_process_md5` | `target_process_md5` | `chars` |
| `target_process_sign` | `target_process_sign` | `chars` |
| `timestamp` | `timestamp` | `time_timestamp` |
| `type` | `type` | `chars` |
| `uuid` | `uuid` | `chars` |
| `computer_name` | `computer_name` | `chars` |
| `gid` | `gid` | `chars` |
| `process_command_line` | `process_command_line` | `chars` |
| `process_internal_name` | `process_internal_name` | `chars` |
| `process_original_name` | `process_original_name` | `chars` |
| `process_parent_path` | `process_parent_path` | `chars` |
| `process_sign` | `process_sign` | `chars` |
| `process_user` | `process_user` | `chars` |
| `report_ip` | `report_ip` | `chars` |
| `target_process_path` | `target_process_path` | `chars` |
| `asset_id` | `asset_id` | `chars` |
| `client_id` | `client_id` | `chars` |
| `ip` | `ip` | `chars` |
| `event_type` | `event_type` | `chars` |
| `group_name` | `group_name` | `chars` |
| `injected_dll` | `injected_dll` | `chars` |
| `mac` | `mac` | `chars` |
| `mid` | `mid` | `chars` |
| `process_guid` | `process_guid` | `chars` |
| `process_id` | `process_id` | `chars` |
| `process_md5` | `process_md5` | `chars` |
| `process_name` | `process_name` | `chars` |
| `process_path` | `process_path` | `chars` |

#### 组合与映射要点

- 本规则组合输入候选：身份候选：`uuid`, `asset_id`；时间候选：`event_date_creation`, `timestamp`；主动方候选：`process_user`；目标方候选：待从样例确认；载体候选：`process_name`, `process_guid`, `process_id`, `process_command_line`；检测候选：待从样例确认。
- 从本节字段选择稳定 ID 和事件发生时间；不能直接使用规则名作为 `event_id`。
- 按事实将终端、进程、网络、文件和用户放入 `roles`；不沿用大禹 `attacker/victim` 作为标准角色。
- 将天擎类型、状态、结果转换为受控 `event_type`、`operation`、`outcome`、`severity`；原始值保留在 `source_finding` 或 `extensions`。
- 低频字段进入 `facets`/`extensions` 前必须确认稳定性和调查价值。

### 3.43 `edr_process_permission_info`

- `log_type`：`edr_process_permission_info`
- 描述：天擎EDR进程权限信息
- 规则过滤：`f_chars_has(type, process_access)`
- 建议事件语义：进程/系统审计事件；event_category 候选为 audit
- 抽取字段数（按别名去重）：32

| 原始路径 | 输出别名 | WPL 类型 |
|---|---|---|
| `asset_oid` | `asset_oid` | `chars` |
| `custom_group_paths` | `custom_group_paths` | `chars` |
| `event_date_creation` | `event_date_creation` | `time_timestamp` |
| `process_call_trace` | `process_call_trace` | `chars` |
| `process_sha1` | `process_sha1` | `chars` |
| `target_process_guid` | `target_process_guid` | `chars` |
| `target_process_id` | `target_process_id` | `chars` |
| `timestamp` | `timestamp` | `time_timestamp` |
| `type` | `type` | `chars` |
| `uuid` | `uuid` | `chars` |
| `computer_name` | `computer_name` | `chars` |
| `gid` | `gid` | `chars` |
| `process_command_line` | `process_command_line` | `chars` |
| `process_granted_access` | `process_granted_access` | `chars` |
| `process_internal_name` | `process_internal_name` | `chars` |
| `process_sign` | `process_sign` | `chars` |
| `process_user` | `process_user` | `chars` |
| `report_ip` | `report_ip` | `chars` |
| `target_process_path` | `target_process_path` | `chars` |
| `asset_id` | `asset_id` | `chars` |
| `client_id` | `client_id` | `chars` |
| `ip` | `ip` | `chars` |
| `event_type` | `event_type` | `chars` |
| `group_name` | `group_name` | `chars` |
| `mac` | `mac` | `chars` |
| `mid` | `mid` | `chars` |
| `process_guid` | `process_guid` | `chars` |
| `process_id` | `process_id` | `chars` |
| `process_md5` | `process_md5` | `chars` |
| `process_name` | `process_name` | `chars` |
| `process_path` | `process_path` | `chars` |
| `thread_id` | `thread_id` | `chars` |

#### 组合与映射要点

- 本规则组合输入候选：身份候选：`uuid`, `asset_id`；时间候选：`event_date_creation`, `timestamp`；主动方候选：`process_user`；目标方候选：待从样例确认；载体候选：`process_name`, `process_guid`, `process_id`, `process_command_line`；检测候选：待从样例确认。
- 从本节字段选择稳定 ID 和事件发生时间；不能直接使用规则名作为 `event_id`。
- 按事实将终端、进程、网络、文件和用户放入 `roles`；不沿用大禹 `attacker/victim` 作为标准角色。
- 将天擎类型、状态、结果转换为受控 `event_type`、`operation`、`outcome`、`severity`；原始值保留在 `source_finding` 或 `extensions`。
- 低频字段进入 `facets`/`extensions` 前必须确认稳定性和调查价值。

### 3.44 `edr_reg_change`

- `log_type`：`edr_reg_change`
- 描述：天擎EDR注册表变更
- 规则过滤：`f_chars_has(type, registry_changes)`
- 建议事件语义：待确认事件语义
- 抽取字段数（按别名去重）：39

| 原始路径 | 输出别名 | WPL 类型 |
|---|---|---|
| `asset_oid` | `asset_oid` | `chars` |
| `custom_group_paths` | `custom_group_paths` | `chars` |
| `event_date_creation` | `event_date_creation` | `time_timestamp` |
| `process_parent_command_line` | `process_parent_command_line` | `chars` |
| `process_parent_internal_name` | `process_parent_internal_name` | `chars` |
| `process_parent_name` | `process_parent_name` | `chars` |
| `process_parent_original_name` | `process_parent_original_name` | `chars` |
| `process_parent_sign` | `process_parent_sign` | `chars` |
| `process_sha1` | `process_sha1` | `chars` |
| `registry_key_path` | `registry_key_path` | `chars` |
| `registry_key_path_renamed` | `registry_key_path_renamed` | `chars` |
| `registry_value_details` | `registry_value_details` | `chars` |
| `registry_value_details_new` | `registry_value_details_new` | `chars` |
| `registry_value_name` | `registry_value_name` | `chars` |
| `registry_value_type` | `registry_value_type` | `chars` |
| `timestamp` | `timestamp` | `time_timestamp` |
| `type` | `type` | `chars` |
| `uuid` | `uuid` | `chars` |
| `computer_name` | `computer_name` | `chars` |
| `gid` | `gid` | `chars` |
| `process_command_line` | `process_command_line` | `chars` |
| `process_internal_name` | `process_internal_name` | `chars` |
| `process_original_name` | `process_original_name` | `chars` |
| `process_parent_path` | `process_parent_path` | `chars` |
| `process_sign` | `process_sign` | `chars` |
| `process_user` | `process_user` | `chars` |
| `report_ip` | `report_ip` | `chars` |
| `asset_id` | `asset_id` | `chars` |
| `client_id` | `client_id` | `chars` |
| `ip` | `ip` | `chars` |
| `event_type` | `event_type` | `chars` |
| `group_name` | `group_name` | `chars` |
| `mac` | `mac` | `chars` |
| `mid` | `mid` | `chars` |
| `process_guid` | `process_guid` | `chars` |
| `process_id` | `process_id` | `chars` |
| `process_md5` | `process_md5` | `chars` |
| `process_name` | `process_name` | `chars` |
| `process_path` | `process_path` | `chars` |

#### 组合与映射要点

- 本规则组合输入候选：身份候选：`uuid`, `asset_id`；时间候选：`event_date_creation`, `timestamp`；主动方候选：`process_user`；目标方候选：待从样例确认；载体候选：`process_name`, `process_guid`, `process_id`, `process_command_line`；检测候选：待从样例确认。
- 从本节字段选择稳定 ID 和事件发生时间；不能直接使用规则名作为 `event_id`。
- 按事实将终端、进程、网络、文件和用户放入 `roles`；不沿用大禹 `attacker/victim` 作为标准角色。
- 将天擎类型、状态、结果转换为受控 `event_type`、`operation`、`outcome`、`severity`；原始值保留在 `source_finding` 或 `extensions`。
- 低频字段进入 `facets`/`extensions` 前必须确认稳定性和调查价值。

### 3.45 `edr_system_account_audit`

- `log_type`：`edr_system_account_audit`
- 描述：天擎V10系统账号审计日志
- 规则过滤：`f_chars_has(syslog_topic, system_account_audit)`
- 建议事件语义：身份/账号审计事件；event_category 候选为 auth 或 audit，需按事实确认
- 抽取字段数（按别名去重）：14

| 原始路径 | 输出别名 | WPL 类型 |
|---|---|---|
| `asset_oid` | `asset_oid` | `chars` |
| `asset_id` | `asset_id` | `chars` |
| `client_id` | `client_id` | `chars` |
| `client_mac` | `client_mac` | `chars` |
| `client_ip` | `client_ip` | `chars` |
| `client_info/ip` | `ip` | `chars` |
| `client_report_ip` | `client_report_ip` | `chars` |
| `client_info/report_ip` | `report_ip` | `chars` |
| `create_time` | `create_time` | `time_timestamp` |
| `report_time` | `report_time` | `time_timestamp` |
| `account_type` | `account_type` | `digit` |
| `account_name` | `account_name` | `chars` |
| `action` | `action` | `digit` |
| `syslog_topic` | `syslog_topic` | `chars` |

#### 组合与映射要点

- 本规则组合输入候选：身份候选：`asset_id`；时间候选：`create_time`；主动方候选：`account_name`；目标方候选：待从样例确认；载体候选：待从样例确认；检测候选：待从样例确认。
- 从本节字段选择稳定 ID 和事件发生时间；不能直接使用规则名作为 `event_id`。
- 按事实将终端、进程、网络、文件和用户放入 `roles`；不沿用大禹 `attacker/victim` 作为标准角色。
- 将天擎类型、状态、结果转换为受控 `event_type`、`operation`、`outcome`、`severity`；原始值保留在 `source_finding` 或 `extensions`。
- 低频字段进入 `facets`/`extensions` 前必须确认稳定性和调查价值。

### 3.46 `edr_usb_file_trans`

- `log_type`：`edr_usb_file_trans`
- 描述：天擎EDR_V10_U盘文件传输
- 规则过滤：`f_chars_has(type, udisk_files)`
- 建议事件语义：文件/数据访问事件；event_category 候选为 audit
- 抽取字段数（按别名去重）：38

| 原始路径 | 输出别名 | WPL 类型 |
|---|---|---|
| `asset_oid` | `asset_oid` | `chars` |
| `custom_group_paths` | `custom_group_paths` | `chars` |
| `event_date_creation` | `event_date_creation` | `time_timestamp` |
| `file_path_new` | `file_path_new` | `chars` |
| `process_parent_command_line` | `process_parent_command_line` | `chars` |
| `process_parent_internal_name` | `process_parent_internal_name` | `chars` |
| `process_parent_name` | `process_parent_name` | `chars` |
| `process_parent_original_name` | `process_parent_original_name` | `chars` |
| `process_parent_sign` | `process_parent_sign` | `chars` |
| `process_sha1` | `process_sha1` | `chars` |
| `timestamp` | `timestamp` | `time_timestamp` |
| `type` | `type` | `chars` |
| `usb_sn_new` | `usb_sn_new` | `chars` |
| `uuid` | `uuid` | `chars` |
| `computer_name` | `computer_name` | `chars` |
| `gid` | `gid` | `chars` |
| `process_command_line` | `process_command_line` | `chars` |
| `process_internal_name` | `process_internal_name` | `chars` |
| `process_original_name` | `process_original_name` | `chars` |
| `process_parent_path` | `process_parent_path` | `chars` |
| `process_sign` | `process_sign` | `chars` |
| `process_user` | `process_user` | `chars` |
| `report_ip` | `report_ip` | `chars` |
| `usb_sn` | `usb_sn` | `chars` |
| `asset_id` | `asset_id` | `chars` |
| `client_id` | `client_id` | `chars` |
| `ip` | `ip` | `chars` |
| `event_type` | `event_type` | `chars` |
| `file_md5` | `file_md5` | `chars` |
| `file_path` | `file_path` | `chars` |
| `group_name` | `group_name` | `chars` |
| `mac` | `mac` | `chars` |
| `mid` | `mid` | `chars` |
| `process_guid` | `process_guid` | `chars` |
| `process_id` | `process_id` | `chars` |
| `process_md5` | `process_md5` | `chars` |
| `process_name` | `process_name` | `chars` |
| `process_path` | `process_path` | `chars` |

#### 组合与映射要点

- 本规则组合输入候选：身份候选：`uuid`, `asset_id`；时间候选：`event_date_creation`, `timestamp`；主动方候选：`process_user`；目标方候选：`file_path`；载体候选：`process_name`, `process_guid`, `process_id`, `process_command_line`；检测候选：待从样例确认。
- 从本节字段选择稳定 ID 和事件发生时间；不能直接使用规则名作为 `event_id`。
- 按事实将终端、进程、网络、文件和用户放入 `roles`；不沿用大禹 `attacker/victim` 作为标准角色。
- 将天擎类型、状态、结果转换为受控 `event_type`、`operation`、`outcome`、`severity`；原始值保留在 `source_finding` 或 `extensions`。
- 低频字段进入 `facets`/`extensions` 前必须确认稳定性和调查价值。

### 3.47 `edr_website_audit`

- `log_type`：`edr_website_audit`
- 描述：天擎V10网站访问审计日志
- 规则过滤：`f_chars_has(syslog_topic, website_audit)`
- 建议事件语义：待确认事件语义
- 抽取字段数（按别名去重）：14

| 原始路径 | 输出别名 | WPL 类型 |
|---|---|---|
| `asset_oid` | `asset_oid` | `chars` |
| `asset_id` | `asset_id` | `chars` |
| `client_id` | `client_id` | `chars` |
| `client_mac` | `client_mac` | `chars` |
| `client_ip` | `client_ip` | `chars` |
| `client_info/ip` | `ip` | `chars` |
| `client_report_ip` | `client_report_ip` | `chars` |
| `client_info/report_ip` | `report_ip` | `chars` |
| `create_time` | `create_time` | `time_timestamp` |
| `report_time` | `report_time` | `time_timestamp` |
| `process_name` | `process_name` | `chars` |
| `website_title` | `website_title` | `chars` |
| `target_url` | `target_url` | `chars` |
| `syslog_topic` | `syslog_topic` | `chars` |

#### 组合与映射要点

- 本规则组合输入候选：身份候选：`asset_id`；时间候选：`create_time`；主动方候选：待从样例确认；目标方候选：待从样例确认；载体候选：`process_name`；检测候选：待从样例确认。
- 从本节字段选择稳定 ID 和事件发生时间；不能直接使用规则名作为 `event_id`。
- 按事实将终端、进程、网络、文件和用户放入 `roles`；不沿用大禹 `attacker/victim` 作为标准角色。
- 将天擎类型、状态、结果转换为受控 `event_type`、`operation`、`outcome`、`severity`；原始值保留在 `source_finding` 或 `extensions`。
- 低频字段进入 `facets`/`extensions` 前必须确认稳定性和调查价值。

### 3.48 `edr_penetration_event`

- `log_type`：`edr_penetration_event`
- 描述：天擎EDR渗透事件
- 规则过滤：`f_chars_has(type, lateral_movement)`
- 建议事件语义：来源检测/安全告警事件；event_category 候选为 alert
- 抽取字段数（按别名去重）：68

| 原始路径 | 输出别名 | WPL 类型 |
|---|---|---|
| `device_type` | `device_type` | `chars` |
| `all_share_path` | `all_share_path` | `chars` |
| `asset_id` | `asset_id` | `chars` |
| `asset_oid` | `asset_oid` | `chars` |
| `client_id` | `client_id` | `chars` |
| `ip` | `ip` | `chars` |
| `computer_name` | `computer_name` | `chars` |
| `custom_group_paths` | `custom_group_paths` | `chars` |
| `event_date_creation` | `event_date_creation` | `time_timestamp` |
| `event_type` | `event_type` | `chars` |
| `execute_method_name` | `execute_method_name` | `chars` |
| `execute_method_type` | `execute_method_type` | `chars` |
| `executed_command_line` | `executed_command_line` | `chars` |
| `executed_command_type` | `executed_command_type` | `chars` |
| `file_md5` | `file_md5` | `chars` |
| `file_path` | `file_path` | `chars` |
| `gid` | `gid` | `chars` |
| `group_name` | `group_name` | `chars` |
| `mac` | `mac` | `chars` |
| `mid` | `mid` | `chars` |
| `process_command_line` | `process_command_line` | `chars` |
| `process_guid` | `process_guid` | `chars` |
| `process_id` | `process_id` | `chars` |
| `process_internal_name` | `process_internal_name` | `chars` |
| `process_md5` | `process_md5` | `chars` |
| `process_name` | `process_name` | `chars` |
| `process_original_name` | `process_original_name` | `chars` |
| `process_parent_command_line` | `process_parent_command_line` | `chars` |
| `process_parent_internal_name` | `process_parent_internal_name` | `chars` |
| `process_parent_name` | `process_parent_name` | `chars` |
| `process_parent_original_name` | `process_parent_original_name` | `chars` |
| `process_parent_path` | `process_parent_path` | `chars` |
| `process_parent_sign` | `process_parent_sign` | `chars` |
| `process_path` | `process_path` | `chars` |
| `process_sha1` | `process_sha1` | `chars` |
| `process_sign` | `process_sign` | `chars` |
| `process_user` | `process_user` | `chars` |
| `registry_key_path` | `registry_key_path` | `chars` |
| `registry_value_name` | `registry_value_name` | `chars` |
| `registry_value_type` | `registry_value_type` | `chars` |
| `registry_value_details` | `registry_value_details` | `chars` |
| `registry_value_details_new` | `registry_value_details_new` | `chars` |
| `report_ip` | `report_ip` | `chars` |
| `service_name` | `service_name` | `chars` |
| `service_path` | `service_path` | `chars` |
| `source_process_command_line` | `source_process_command_line` | `chars` |
| `source_process_guid` | `source_process_guid` | `chars` |
| `source_process_id` | `source_process_id` | `chars` |
| `source_process_md5` | `source_process_md5` | `chars` |
| `source_process_name` | `source_process_name` | `chars` |
| `source_process_path` | `source_process_path` | `chars` |
| `src_ip_addr` | `src_ip_addr` | `chars` |
| `src_ip_host` | `src_ip_host` | `chars` |
| `target_process_command_line` | `target_process_command_line` | `chars` |
| `target_process_md5` | `target_process_md5` | `chars` |
| `target_process_name` | `target_process_name` | `chars` |
| `target_process_path` | `target_process_path` | `chars` |
| `target_process_sign` | `target_process_sign` | `chars` |
| `task_command` | `task_command` | `chars` |
| `task_create_time` | `task_create_time` | `chars` |
| `task_flag` | `task_flag` | `chars` |
| `task_name` | `task_name` | `chars` |
| `task_next_time` | `task_next_time` | `chars` |
| `task_sign` | `task_sign` | `chars` |
| `timestamp` | `timestamp` | `time_timestamp` |
| `type` | `type` | `chars` |
| `wmi_filter_wql` | `wmi_filter_wql` | `chars` |
| `wmi_wql_extend` | `wmi_wql_extend` | `chars` |

#### 组合与映射要点

- 本规则组合输入候选：身份候选：`asset_id`；时间候选：`event_date_creation`, `timestamp`；主动方候选：`src_ip_addr`, `source_process_name`, `process_user`；目标方候选：`file_path`；载体候选：`process_name`, `process_guid`, `process_id`, `process_command_line`；检测候选：待从样例确认。
- 从本节字段选择稳定 ID 和事件发生时间；不能直接使用规则名作为 `event_id`。
- 按事实将终端、进程、网络、文件和用户放入 `roles`；不沿用大禹 `attacker/victim` 作为标准角色。
- 将天擎类型、状态、结果转换为受控 `event_type`、`operation`、`outcome`、`severity`；原始值保留在 `source_finding` 或 `extensions`。
- 低频字段进入 `facets`/`extensions` 前必须确认稳定性和调查价值。

### 3.49 `edr_account_change`

- `log_type`：`edr_account_change`
- 描述：天擎EDR账号变更
- 规则过滤：`f_chars_has(type, account_changes)`
- 建议事件语义：身份/账号审计事件；event_category 候选为 auth 或 audit，需按事实确认
- 抽取字段数（按别名去重）：45

| 原始路径 | 输出别名 | WPL 类型 |
|---|---|---|
| `task_id` | `task_id` | `digit` |
| `sub_task_id` | `sub_task_id` | `digit` |
| `env_version` | `env_version` | `chars` |
| `process_parent_command_line` | `process_parent_command_line` | `chars` |
| `process_parent_internal_name` | `process_parent_internal_name` | `chars` |
| `process_parent_name` | `process_parent_name` | `chars` |
| `process_parent_original_name` | `process_parent_original_name` | `chars` |
| `process_parent_sign` | `process_parent_sign` | `chars` |
| `process_sha1` | `process_sha1` | `chars` |
| `timestamp` | `timestamp` | `chars` |
| `type` | `type` | `chars` |
| `uuid` | `uuid` | `chars` |
| `logger` | `logger` | `chars` |
| `process_original_name` | `process_original_name` | `chars` |
| `process_parent_path` | `process_parent_path` | `chars` |
| `process_sign` | `process_sign` | `chars` |
| `process_user` | `process_user` | `chars` |
| `client_report_ip` | `client_report_ip` | `chars` |
| `report_ip` | `report_ip` | `chars` |
| `account_name` | `account_name` | `chars` |
| `account_user` | `account_user` | `chars` |
| `asset_id` | `asset_id` | `chars` |
| `asset_oid` | `asset_oid` | `chars` |
| `client_id` | `client_id` | `chars` |
| `client_ip` | `client_ip` | `chars` |
| `ip` | `ip` | `chars` |
| `computer_name` | `computer_name` | `chars` |
| `create_time` | `create_time` | `chars` |
| `custom_group_paths` | `custom_group_paths` | `chars` |
| `event_date_creation` | `event_date_creation` | `time_timestamp` |
| `event_type` | `event_type` | `chars` |
| `gid` | `gid` | `chars` |
| `group_name` | `group_name` | `chars` |
| `hostname` | `hostname` | `chars` |
| `mac` | `mac` | `chars` |
| `mid` | `mid` | `chars` |
| `payload` | `payload` | `chars` |
| `pid` | `pid` | `digit` |
| `process_command_line` | `process_command_line` | `chars` |
| `process_guid` | `process_guid` | `chars` |
| `process_id` | `process_id` | `chars` |
| `process_internal_name` | `process_internal_name` | `chars` |
| `process_md5` | `process_md5` | `chars` |
| `process_name` | `process_name` | `chars` |
| `process_path` | `process_path` | `chars` |

#### 组合与映射要点

- 本规则组合输入候选：身份候选：`uuid`, `asset_id`；时间候选：`event_date_creation`, `create_time`, `timestamp`；主动方候选：`process_user`, `account_name`；目标方候选：`account_user`；载体候选：`process_name`, `process_guid`, `process_id`, `process_command_line`；检测候选：待从样例确认。
- 从本节字段选择稳定 ID 和事件发生时间；不能直接使用规则名作为 `event_id`。
- 按事实将终端、进程、网络、文件和用户放入 `roles`；不沿用大禹 `attacker/victim` 作为标准角色。
- 将天擎类型、状态、结果转换为受控 `event_type`、`operation`、`outcome`、`severity`；原始值保留在 `source_finding` 或 `extensions`。
- 低频字段进入 `facets`/`extensions` 前必须确认稳定性和调查价值。

## 4. 规则级待确认项

| 项目 | 影响 | 处理建议 |
|---|---|---|
| `edr_account_change` 重复定义 | `account_change` 与 `account_changes` 可能路由歧义，且时间类型不同 | 拆成唯一规则名，分别补样例后再改 OML |
| WPL 样例覆盖不足 | 当前样例只覆盖约 30 种判别值 | 每个业务规则至少补 1 条代表样例，覆盖可选字段和数组 |
| `@ioc_alerts[0][0]` | 只抽取首个 IOC，可能丢失多个 IOC | 完整数组进入 `source_finding`/`extensions` |
| `@group_info[0]`、`@process_details` | 只取首个组对象或整体数组 | 明确是否保留完整数组 |
| `raw_msg` | WPL 复制原文 | 当前中间版直接写入事件表 `raw_msg`；后期再分离到独立原始日志存储 |
| `alert_cat_*`、`attacker_*`、`victim_*` | 混有大禹/平台告警语义 | 来源检测进入 `source_finding`，平台告警另写 `ldm_alert` |
| 账号变更时间 | 抽查出现 `expected <time>` | 按真实字段格式选择 `time` 或 `time_timestamp` |

## 5. 推荐实施顺序

1. 修复 WPL 重复规则、字段类型和样例覆盖；WPL 不承担 SDM 语义映射。
2. 按本清单为每个 `log_type` 建立身份、时间、角色、事件类型、动作、结果、检测结论和扩展映射契约。
3. 先试点 `edr_alert_log`、`edr_process_event`、`edr_ip_access`、`edr_file_audit`、`edr_antivirus_virus` 五类。
4. 先验证 WPL 抽取，再验证 OML 组合，最后写入 `sdm2_log.sdm_event`。
5. 试点通过后扩展到其余规则；`ldm_alert` 生成链路单独设计。
