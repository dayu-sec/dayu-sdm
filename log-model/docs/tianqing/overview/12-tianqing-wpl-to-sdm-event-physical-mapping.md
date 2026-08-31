# 天擎 WPL 字段到 sdm_event 物理字段映射

> **[历史记录] 本记录涉及的大禹告警表 `ldm_alert` 已在 alert-model 分支从交付物删除（SDM2.0 告警模型重新设计中）。文中 `ldm_alert` 相关内容仅描述当时的执行事实，不代表当前交付范围。**

> 本文档把《11-tianqing-wpl-source-field-and-sdm-mapping.md》中 WPL 已抽取的字段，映射到中间版本 `sdm2_log.sdm_event` 的 55 个 Doris 字段。
> 本文档只定义数据组合、语义转换和物理落位，不包含 OML 语法或实现。
> 当前结论均为待评审候选，尚未登记为批准的天擎映射契约。

## 1. 结论

天擎 WPL 的输出可以映射到当前 `sdm_event`，但不能按字段名全局直连，必须先按 `log_type` 判断字段语义，再构造五层逻辑对象，最后投影到 Doris。

```text
WPL 输出字段
  -> 按 log_type 组合 metadata / event / roles / facets / source_finding / extensions
  -> 高频路径投影到标量列
  -> 完整对象写入 4 个 VARIANT 列
```

首批选择 5 个日志类型完成逐字段映射：

1. `edr_alert_log`
2. `edr_antivirus_virus`
3. `edr_process_event`
4. `edr_file_audit`
5. `edr_ip_access`

其余规则已给出事件级落位建议，待补充样例和枚举值后再展开逐字段矩阵。

## 2. 映射边界

### 2.1 物理表边界

本文档只允许写入 `schema/007_sdm_event.sql` 中现有的 55 列：51 个标量投影列和 4 个 VARIANT 对象列。

| 逻辑对象 | Doris 物理列 | 用途 |
|---|---|---|
| `metadata`、`event` | 对应标量列 | 主键、时间、来源和高频事件语义 |
| `roles` | 高频角色标量列 + `roles_obj` | source、target、observer、carriers 和 related 完整对象 |
| `facets` | `network_*`、`k8s_*` + `facets_obj` | 网络、文件操作上下文、DNS、邮件、认证等事件维度 |
| `source_finding` | `source_finding_*` + `source_finding_obj` | 天擎自身产生的检测或告警判断 |
| `extensions` | `extensions_obj` | 已治理的终端资产 Profile 和天擎私有稳定字段 |

### 2.2 标量与 VARIANT 同步规则

- 字段对应 51 个标量投影路径时，同时写入逻辑对象和标量列；标量列不是第二份独立语义。
- 低频逻辑字段只进入对应 VARIANT，不为了接入天擎临时增加 Doris 列。
- `roles_obj`、`facets_obj`、`source_finding_obj` 保存完整标准逻辑对象。
- `extensions_obj` 只保存已声明的来源私有字段和 Profile，不复制完整原始日志。
- 当前由 `raw_msg` 直接保存源日志；不得把原始 JSON、`payload` 或 `process_details` 重复复制到 VARIANT。后期再分离原文存储与引用。

### 2.3 标识字段职责

| Doris 字段 | 赋值规则 |
|---|---|
| `tenant_id` | 来自可信租户或采集上下文；无显式租户时使用空字符串，不虚构租户标识。 |
| `event_id` | 确定性生成的 SDM 事件唯一标识。优先使用 `tenant_id + mapping_id + source_original_event_id`；来源无稳定 ID 时，使用 `tenant_id + log_id + log_type + 子事件序号`。重放必须保持一致。 |
| `log_id` | 一条原始安全日志的稳定标识，供 `ldm_alert.log_id_list` 回查。由来源记录 ID或采集位置确定，不使用随机值。 |
| `raw_msg` | 当前中间阶段装载的完整源日志原文，由采集链路提供；后期再分离到独立原始日志存储。 |
| `source_original_event_id` | 天擎日志自身的稳定事件编号，例如经确认后的 `uuid`、`alert_id`；不等同于 `event_id`。 |

### 2.4 固定值和平台上下文

| WPL/上下文 | 逻辑路径 | Doris 字段 | 组合或转换规则 |
|---|---|---|---|
| 租户上下文 | `metadata.tenant_id` | `tenant_id` | 无显式配置时暂用空字符串。 |
| 平台接收时间 | `metadata.ingest_time` | `ingest_time` | 由接入层生成，不取天擎事件时间。 |
| 标准化完成时间 | `metadata.parse_time` | `parse_time` | 由标准化处理层生成。 |
| 常量 `1` | `metadata.schema_version` | `schema_version` | 当前中间版本结构版本。 |
| `qax.tianqing.<log_type>` | `metadata.mapping_id` | `mapping_id` | 每个稳定日志类型使用独立映射编号。 |
| 常量 `qax` | `metadata.data_source.vendor` | `data_src_vendor` | 厂商标准编码，评审时确认是否统一使用英文编码。 |
| 常量 `tianqing` | `metadata.data_source.product` | `data_src_product` | 产品标准编码。 |
| 常量 `endpoint_security` | `metadata.data_source.category` | `data_src_category` | 天擎终端安全数据来源类别。 |
| 采集实例上下文 | `metadata.data_source.instance_id` | `data_src_instance_id` | 取采集任务或来源实例 ID，不把终端 `client_id` 当作采集实例。 |
| 规则 `log_type` | `metadata.log.type` | `log_type` | 使用 WPL 规则稳定名称。 |
| 规则中文描述 | `metadata.log.name` | `log_name` | 使用固定中文日志名称。 |
| 常量 `qax` | `roles.observer.device.vendor` | `observer_vendor` | 同时写入 `roles_obj`。 |
| 常量 `tianqing` | `roles.observer.product.name` | `observer_product` | 同时写入 `roles_obj`。 |

`log_level` 只接受天擎原始日志等级。告警危险等级不得写入 `log_level`，来源检测危险等级应写入 `source_finding_severity`。

## 3. 公共终端资产字段映射

下表适用于字段语义确实表示“被天擎 Agent 管理的终端”时。网络通信中的 `src_ip`、`dst_ip` 不适用本表。

| WPL 输出字段 | 逻辑路径 | Doris 物理落位 | 组合或转换规则 |
|---|---|---|---|
| `asset_id` | 对应角色的 `host.id` | `roles_obj` | 终端资产稳定 ID；Profile 通过 `subject_ref.ref_id` 引用该主机，不重复保存资产 ID。 |
| `client_id` | `extensions.profiles.endpoint_asset.agent.id` | `extensions_obj` | 天擎 Agent ID。 |
| `mid`、`client_mid` | `extensions.profiles.endpoint_asset.agent.fingerprint_id` | `extensions_obj` | Agent 或终端指纹 ID。 |
| `env_version` | `extensions.profiles.endpoint_asset.agent.version` | `extensions_obj` | 天擎 EDR 终端环境版本按 Agent 版本保存；空值省略，不能写观察设备 OS 版本。 |
| `computer_name`、`client_name`、`name` | 对应角色的 `host.name` | `source_host` 或 `target_host`，并写 `roles_obj` | 具体角色由日志事实决定，不按字段名全局固定。 |
| `ip`、`client_ip`、`report_ip`、`client_report_ip` | 对应角色的 `host.ip/ipv4/ipv6` | `roles_obj`；作为网络主动方时才投影 `source_ip`，作为网络目标时才投影 `target_ip` | 终端管理 IP 不自动等同于网络会话 source/target。 |
| `mac`、`client_mac` | 受管终端主机的 MAC 资产属性 | 来源主机使用 `roles.source.host.mac`；其他角色没有已注册等价路径时进入对应来源私有字段 | `host.mac` 表示主机资产属性，`endpoint.mac` 只表示网络会话端点。写入标准路径后不得在来源私有字段中重复保存。 |
| `os`、`client_os_version_*`、`release_id`、`build_version`、`main`、`describe`、`os_bit` | 对应角色的 `host.os.*` | `roles_obj` | 按名称、版本、构建号和架构分别组合，禁止拼成不可拆字符串后丢弃原值。 |
| `gid`、`group_id` | `extensions.profiles.endpoint_asset.ownership.group.id` | `extensions_obj` | 保存终端在事件发生时的分组编号。 |
| `group_name` | `extensions.profiles.endpoint_asset.ownership.group.name` | `extensions_obj` | 保存终端在事件发生时的分组名称。 |
| `group_node_id`、`group_node_name`、`group_node_path`、`custom_group_paths` | `extensions.source_private.qax.tianqing.asset_context.group.*` | `extensions_obj` | 当前 Profile 没有层级路径字段；数组保持数组，待组织模型扩展评审。 |
| `login_account`、`client_login_account` | 对应角色的 `account.name` | `roles_obj`；明确为行为发起用户时可投影 `source_user` | 账号与人员名称不自动互拷。 |
| `state` | `extensions.profiles.endpoint_asset.lifecycle.status` | `extensions_obj` | 必须先取得天擎枚举含义；未确认前保存在来源私有路径。 |
| `activation` | `extensions.profiles.endpoint_asset.agent.status` | `extensions_obj` | 只有确认字段表示 Agent 激活状态后才写 Profile；否则保存在来源私有路径。 |
| `create_time`、`update_time` | endpoint_asset 对应生命周期字段 | `extensions_obj` | 仅在字段确为资产创建/更新时间时使用，不能覆盖事件 `occur_time`。 |
| `nic_list`、`report_ipv6` | 对应角色的主机网络属性 | `roles_obj` | 保留多网卡和多地址结构，不截取首项作为唯一事实。 |
| `asset_oid` | `extensions.profiles.endpoint_asset.ownership.organization.id` | `extensions_obj` | 旧 OML 明确将其解释为 `asset_org_id`，与终端 `host.id` 分开保存。 |
| `oid`、`tree_id`、`node_id`、`node_type`、`node_name` | `extensions.source_private.qax.tianqing.asset_context.*` | `extensions_obj` | 当前 Profile 无完全等价路径时保留稳定私有结构，待确认组织字段语义后再迁移。 |

## 4. 全部 WPL 规则的事件级落位

表中的 `event.type` 是候选值。只有取得原始枚举和样例验证后才能定稿；无法证明具体行为时使用受控的 `*_uncategorized`，不根据产品名创造事件类型。

| WPL 规则 | `record_kind` | `event.domain` | `event.type` 候选 | 主要对象/维度 | 当前状态 |
|---|---|---|---|---|---|
| `ignore` | — | — | — | 不生成事件 | 确定 |
| `ignore_other` | — | — | — | 不生成事件 | 确定 |
| `edr_alert_log` | `finding` | `threat` | `generic_event` | 终端、来源检测、IOC、MITRE | 阻塞：WPL 未输出事件时间 |
| `edr_antivirus_virus` | `finding` | `threat` | `scan_file` | 终端、文件、恶意软件检测 | 首批详细映射 |
| `edr_antivirus_scan` | `activity` | `endpoint` | `scan_file` | 终端、扫描任务、文件 | 待确认扫描状态枚举 |
| `edr_attack_protection` | `finding` | `threat` | `generic_event` | 终端、文件、攻击检测 | 待展开 |
| `edr_system_protection` | `finding` | `threat` | `generic_event` | 终端、文件、系统防护检测 | 待展开 |
| `edr_webpage_protection` | `finding` | `threat` | `generic_event` | 终端、访问 IP、网页防护检测 | 待展开 |
| `edr_firewall` | `activity` | `network` | `network_connection` | 网络端点、终端、防火墙结果 | 待确认 `result`、方向和端口字段 |
| `edr_baseline_check_result` | `finding` | `asset` | `generic_event` | 终端、基线任务、检查结果 | 待确认检查结果枚举 |
| `edr_baseline_check_detail` | `finding` | `asset` | `generic_event` | 终端、基线检查项 | 待确认检查项语义 |
| `edr_process_log` | `activity` | `endpoint` | `process_uncategorized` | 终端、进程 | 待确认动作枚举 |
| `edr_ssid_log` | `finding` | `network` | `network_uncategorized` | 终端、SSID、防护结果 | 待确认 SSID 字段语义 |
| `edr_energy_manage_log` | `state` | `asset` | `status_update` | 终端、能耗状态 | 待确认是否应形成事件 |
| `edr_net_out_log` | `finding` | `network` | `network_connection` | 终端、外联目标、检测结果 | 待确认网络端点字段 |
| `edr_external_device_alarm` | `finding` | `endpoint` | `generic_event` | 终端、关联外设、管控结果 | 待展开 |
| `edr_remote_assistance_log` | `activity` | `endpoint` | `user_resource_access` | 终端、用户、远程会话 | 待确认会话动作枚举 |
| `edr_remote_assistance_file_transfer` | `activity` | `endpoint` | `file_uncategorized` | 终端、远程会话、文件 | 待确认上传/下载方向 |
| `cs_op_log` | `activity` | `system` | `generic_event` | 操作员、管理操作 | 待补充样例 |
| `edr_process_event` | `activity` | `endpoint` | 按 `event_type` 映射 `process_launch`、`process_termination` 或 `process_uncategorized` | 终端、进程树、用户 | 首批详细映射 |
| `edr_file_op` | `activity` | `endpoint` | 按原始动作映射文件事件类型 | 终端、进程、文件 | 待确认动作枚举 |
| `edr_wmi_event` | `activity` | `endpoint` | `process_uncategorized` | 终端、WMI、进程 | 待确认 WMI 行为类型 |
| `edr_powershell_cmd_exec` | `activity` | `endpoint` | `generic_event` | 用户、终端、PowerShell 进程、脚本 | 已完成首条真实样例；不是进程创建 |
| `edr_account_change`（`account_change`） | `activity` | `identity` | 按动作映射账号事件类型 | 终端、账号、操作者 | 阻塞：与 3.49 重名且过滤值不同 |
| `edr_file_audit` | `activity` | `endpoint` | 当前样例为 `file_creation/upload` | 终端、账号、进程、本地和远端文件 | 已完成 `upload_to_site` 真实样例；其他渠道待补充 |
| `edr_mobile_storage_client_log` | `activity` 或 `finding` | `endpoint` | 按原始动作映射文件或设备事件 | 终端、移动存储、文件、检测 | 字段较多，需按子事件拆分评估 |
| `data_breach_event` | `finding` | `threat` | `generic_event` | 终端、数据对象、来源检测 | 待展开 |
| `edr_dns_access` | `activity` | `network` | `network_dns` | 终端、DNS 查询和响应 | 已完成首条真实样例；协议和 DNS 服务器待补充 |
| `edr_driver_file_load` | `activity` | `endpoint` | `process_module_load` | 终端、进程、驱动文件 | 待展开 |
| `edr_file_trans` | `activity` | `endpoint` | 按方向映射 `file_creation` 或 `file_read` | 终端、进程、文件、网络端点 | 待确认传输方向 |
| `edr_fileless_script_behavior_event` | `activity` 或 `finding` | `endpoint` | `process_uncategorized` | 终端、脚本、进程、检测 | 待确认是行为事实还是检测结果 |
| `edr_im_audit` | `activity` | `application` | `user_communication` | 终端、账号、即时通信内容摘要 | 待展开并处理隐私字段 |
| `edr_image_file_load` | `activity` | `endpoint` | `process_module_load` | 终端、进程、映像文件 | 待展开 |
| `edr_ip_access` | `activity` | `network` | `network_connection` | 网络端点、终端、进程 | 首批详细映射 |
| `edr_mail_attachment_trans` | `activity` | `application` | `email_transaction` | 邮件、附件、终端 | 待确认发送/接收方向 |
| `edr_mail_audit` | `activity` | `application` | `email_transaction` 或 `email_uncategorized` | 邮件、账号、终端 | 待补充样例和动作枚举 |
| `edr_memory_shield_log` | `finding` | `threat` | `process_uncategorized` | 终端、进程、内存防护检测 | 待展开 |
| `edr_mobile_storage_web_log` | `activity` | `endpoint` | 按原始动作映射文件或设备事件 | 移动存储、操作员、文件 | 待补充样例 |
| `edr_name_pipe_event` | `activity` | `endpoint` | `process_uncategorized` | 终端、进程、命名管道 | 待确认是否需要标准扩展 Profile |
| `edr_patch_info` | `inventory` 或 `state` | `asset` | `status_update` | 终端、补丁、安装状态 | 待确认是一条清单还是变更事件 |
| `edr_print_audit` | `activity` | `application` | `resource_written` | 终端、用户、打印文件、打印机 | 待补充样例 |
| `edr_process_inject` | `activity` | `endpoint` | `process_injection` | 源进程、目标进程、目标线程、终端 | 已完成首条真实样例；注入方法枚举和结果待补充 |
| `edr_process_permission_info` | `state` | `endpoint` | `process_privilege_escalation` 或 `process_uncategorized` | 进程、权限信息 | 待确认是否发生权限变更 |
| `edr_reg_change` | `activity` | `system` | 当前样例为 `registry_modification` | 终端、进程、注册表键值 | 已完成 `registry_set_value` 真实样例；其他动作待补充 |
| `edr_system_account_audit` | `activity` | `identity` | 按动作映射账号事件类型 | 终端、账号、操作者 | 待确认动作枚举 |
| `edr_usb_file_trans` | `activity` | `endpoint` | 按方向映射 `file_creation` 或 `file_read` | 终端、U 盘、文件 | 待确认传输方向 |
| `edr_website_audit` | `activity` | `application` | `network_http` | 终端、用户、URL、HTTP | 待补充样例 |
| `edr_penetration_event` | `finding` | `threat` | `generic_event` | 终端、进程、网络、来源检测 | 待展开 |
| `edr_account_change`（`account_changes`） | `activity` | `identity` | 按动作映射账号事件类型 | 终端、账号、操作者 | 阻塞：样例解析报 `expected <time>` |

## 5. 首批逐字段映射

### 5.1 `edr_alert_log`

#### 事件评估

- 事件事实：天擎对受管终端产生的一条来源侧威胁检测。
- `record_kind=finding`，`event_domain=threat`。
- `event_type` 暂用受控兜底值 `generic_event`；不能把 `edr_alert` 直接写成标准事件类型。
- `wpl-check` 已确认当前规则能够输出来源 `create_time`，可作为 `occur_time`；不得改用平台 `parse_time` 冒充事件时间。

| WPL 输出字段 | 字段含义 | SDM 逻辑路径 | Doris 物理落位 | 组合/转换逻辑 | 状态 |
|---|---|---|---|---|---|
| `alert_id` | 天擎告警编号 | `source_finding.original_id`、`metadata.original_event_id` | `source_finding_original_id`、`source_original_event_id`，并写 `source_finding_obj` | 确认全局稳定后，用于确定性生成 `event_id`；不直接覆盖 `log_id`。 | 候选 |
| `alert_name` | 告警名称 | `source_finding.title` | `source_finding_title` + `source_finding_obj` | 保留中文名称。 | 确定 |
| `description` | 告警描述 | `source_finding.description` | `source_finding_obj`；可生成有界 `log_content` | 不复制完整原文；`log_content` 最大 4096 字符。 | 确定 |
| `severity` | 来源告警危险等级 | `source_finding.severity` | `source_finding_severity` + `source_finding_obj` | 保留原值或按来源契约归一；不得写入 syslog 语义的 `severity`。 | 确定 |
| `category_id` | 来源告警分类编号 | `source_finding.category.original.code` | `source_finding_obj` | 若另有分类名称，再写 `source_finding.category` 并投影 `source_finding_category`。 | 候选 |
| `rule_id` | 触发规则编号 | `source_finding.rule.signature_id` | `source_finding_signature_id` + `source_finding_obj` | 字符串保留。 | 确定 |
| `status` | 来源告警状态 | `source_finding.status` | `source_finding_obj` | 需取得枚举；不得直接作为平台 `ldm_alert` 状态。 | 待确认 |
| `compromise_status_cd` | 失陷状态编码 | `source_finding.compromise_status` | `source_finding_obj` | 取得天擎枚举后转成可解释值，同时在来源私有字段保留原始编码。 | 待确认 |
| `technique` | MITRE 技术 | `source_finding.mitre.techniques` | `source_finding_obj` | 逻辑类型为字符串数组，多值必须保持数组。 | 候选 |
| `tactic` | MITRE 战术 | `source_finding.mitre.tactics` | `source_finding_obj` | 逻辑类型为字符串数组，多值必须保持数组。 | 候选 |
| `ioc_value` | 命中的 IOC 值 | `source_finding.indicators[].value` | `source_finding_obj` | 与类型、协议等字段组成同一个 indicator 对象。当前 WPL 只取首项，存在信息截断。 | 待修复 |
| `malicious_type` | IOC/恶意对象类型 | `source_finding.indicators[].type` | `source_finding_obj` | 与 `ioc_value` 同索引组合。 | 待确认枚举 |
| `malicious_family` | 恶意家族 | `source_finding.malware.family` | `source_finding_obj` | 保留来源值。 | 候选 |
| `origin_killchain` | 来源杀伤链阶段 | `source_finding.original_killchain` | `source_finding_obj` | 保留来源杀伤链原值；标准化值经评审后可另写 `source_finding.killchain`。 | 候选 |
| `protocol` | IOC 关联协议 | `extensions.source_private.qax.tianqing.edr_alert_log.ioc_protocol` | `extensions_obj` | 当前 indicator 对象没有协议路径；不写 `network_protocol`，除非该告警明确描述一次网络通信事实。 | 候选 |
| `risky_source` | 天擎声称的风险来源 | `extensions.source_private.qax.tianqing.edr_alert_log.risky_source` | `extensions_obj` | 不直接写 `source_ip`，除非字段值被解析并证明是行为主动方 IP。 | 确定边界 |
| `des_ip` | 从描述引号内容派生的候选值 | 按 `category_id` 决定 | `source_finding_obj` | 类别 801 的 RDP 爆破样例中是攻击者 IP；其他类别可能是进程名或域名，禁止无条件当作 IP。 | 条件 |
| `des_user` | 从描述派生的目标用户 | `extensions.source_private.qax.tianqing.edr_alert_log.derived_target_user` | `extensions_obj` | 当前 victim 对象没有用户名称路径；派生值需标注证据，不自动投影 `target_user`。 | 候选 |
| `client_login_user` | 受管终端当前登录账号 | `roles.target.account.name` | `roles_obj` | 告警对象是终端时作为目标账号，不解释为攻击者。 | 候选 |
| `computer_name` | 受管终端名称 | `roles.target.host.name` | `target_host` + `roles_obj` | 同终端资产 Profile 建立一致引用。 | 候选 |
| `ip`、`report_ip` | 受管终端地址 | `roles.target.host.ip/ipv4/ipv6` | `roles_obj` | 不直接写 `target_ip`，除非该告警明确描述网络目标端点。 | 候选 |
| `mac` | 受管终端 MAC | `extensions.source_private.qax.tianqing.edr_alert_log.host.mac` | `extensions_obj` | 这是告警目标主机的资产属性；当前只注册了 `roles.source.host.mac`，不能为了复用该路径改变告警目标角色，也不能误写为网络会话端点。 | 候选 |
| `asset_id`、`client_id`、`mid`、`gid`、`group_name`、`custom_group_paths`、`asset_oid` | 终端资产和分组上下文 | 见第 3 节 | `extensions_obj` | 构造 endpoint_asset Profile；无标准路径的字段进入天擎私有结构。 | 候选 |
| `process_details` | 告警关联进程列表 | `roles.related[]`，并由 `source_finding.entities.affected[]` 引用 | `roles_obj` + `source_finding_obj` | 必须逐项构造进程对象和事件内 `ref_id`，禁止把数组原样塞入私有字段；需先确认元素结构。 | 待确认 |
| `other_type` | 来源日志子类型 | `extensions.source_private.qax.tianqing.edr_alert_log.other_type` | `extensions_obj` | 仅在有稳定区分价值时保留。 | 候选 |
| `tmp1`、`tmp2` | WPL 中间变量 | — | 不落库 | 只用于派生 `des_ip`、`des_user`，不得形成业务字段。 | 确定 |

### 5.2 `edr_antivirus_virus`

#### 事件评估

- 事件事实：天擎在受管终端文件上产生的病毒检测/查杀结果。
- 候选语义：`record_kind=finding`、`event_domain=threat`、`event_type=scan_file`。
- `operation` 只有在 `result` 或其他字段能证明扫描已完成时才写 `completed`，否则留空。

| WPL 输出字段 | 字段含义 | SDM 逻辑路径 | Doris 物理落位 | 组合/转换逻辑 | 状态 |
|---|---|---|---|---|---|
| `file_alarm_time` | 病毒告警时间 | `metadata.occur_time` | `occur_time` | 作为首选事件时间，按已确认时区转换为 `DATETIME(3)`。 | 候选 |
| `guid` | 来源记录 GUID | `metadata.original_event_id` | `source_original_event_id` | 确认稳定性后参与生成 `event_id`。 | 候选 |
| `virus_name` | 病毒名称 | `source_finding.title`、`source_finding.malware.name` | `source_finding_title` + `source_finding_obj` | 标题可组合为“检测到病毒：<virus_name>”。 | 候选 |
| `virus_type` | 病毒类型 | `source_finding.malware.type`、`source_finding.category` | `source_finding_category` + `source_finding_obj` | 保留来源分类值。 | 候选 |
| `severity` | 来源检测危险等级 | `source_finding.severity` | `source_finding_severity` + `source_finding_obj` | 不写事件 `severity`。 | 确定 |
| `result` | 查杀结果 | `source_finding.action`、`event.outcome` | `source_finding_action`、`outcome` + `source_finding_obj` | 建立枚举表后映射；如“处理成功”可映射 `success`，如“阻止”可映射 `denied`。 | 待确认枚举 |
| `file_path` | 被检测文件路径 | `roles.target.file.path` | `target_file_path` + `roles_obj` | 从路径派生文件名时仍保留原路径。 | 确定 |
| `md5` | 被检测文件 MD5 | `roles.target.file.hashes.md5` | `roles_obj` | 当前无 MD5 标量列。 | 确定 |
| `sha1` | 被检测文件 SHA-1 | `roles.target.file.hashes.sha1` | `roles_obj` | 当前无 SHA-1 标量列。 | 确定 |
| `file_create_time` | 文件创建时间 | `roles.target.file.created_time` | `roles_obj` | 不作为事件发生时间。 | 确定 |
| `trigger_mode` | 扫描触发方式编码 | `extensions.source_private.qax.tianqing.edr_antivirus_virus.trigger_mode` | `extensions_obj` | 当前标准 Finding 没有触发方式路径；需取得枚举含义。 | 待确认 |
| `need_reboot` | 处置后是否需重启 | `extensions.source_private.qax.tianqing.edr_antivirus_virus.need_reboot` | `extensions_obj` | 转为布尔值；当前标准 Finding 没有等价路径。 | 待确认 |
| `scanners` | 扫描引擎/扫描器 | `extensions.source_private.qax.tianqing.edr_antivirus_virus.scanners` | `extensions_obj` | 当前标准 Finding 没有扫描引擎路径；需确认值结构。 | 待确认 |
| `report_ip`、`name`、`mac`、`login_account` | 受管终端属性 | `roles.target.host.*`、`roles.target.account.name` | `target_host`（名称）+ `roles_obj` | 终端是检测对象，不作为 observer.device。 | 候选 |
| `client_id`、`mid`、资产状态、OS、分组和网卡字段 | 终端资产快照 | 见第 3 节 | `extensions_obj` + `roles_obj` | Profile 只保存事件时点快照。 | 候选 |
| `create_time`、`update_time` | 终端资产时间 | endpoint_asset 生命周期路径 | `extensions_obj` | 不覆盖 `occur_time`。 | 候选 |

### 5.3 `edr_process_event`

#### 事件评估

- 事件事实：受管终端上的进程创建、结束或其他进程活动。
- `record_kind=activity`、`event_domain=endpoint`。
- `event_type` 必须按天擎原始 `event_type` 枚举转换：创建/启动映射 `process_launch`，结束映射 `process_termination`，其余映射 `process_uncategorized`。

| WPL 输出字段 | 字段含义 | SDM 逻辑路径 | Doris 物理落位 | 组合/转换逻辑 | 状态 |
|---|---|---|---|---|---|
| `event_date_creation` | 进程事件发生时间 | `metadata.occur_time` | `occur_time` | 首选时间；`timestamp` 作为一致性校验或备选。 | 候选 |
| `uuid` | 天擎事件 UUID | `metadata.original_event_id` | `source_original_event_id` | 参与确定性生成 `event_id`。 | 候选 |
| `event_type` | 天擎进程动作类型 | `event.type`、`event.operation` | `event_type`、`operation` | 按已评审枚举映射，不原样直写；只有执行语义明确时使用 `operation=exec`。 | 待确认枚举 |
| `process_name` | 当前进程名称 | `roles.target.process.name` | `roles_obj` | 创建事件表示新创建进程，终止事件表示被终止进程；两者都是事件客体。 | 确定 |
| `process_guid` | 当前进程 GUID | `roles.target.process.uid` | `roles_obj` | 保留字符串，并优先用于生成目标进程 `ref_id`。 | 确定 |
| `process_id`、`pid` | 当前进程 PID | `roles.target.process.pid` | `roles_obj` | `process_id` 优先、`pid` 备用；冲突时记录质量问题。 | 确定 |
| `process_command_line` | 当前进程命令行 | `roles.target.process.cmdline` | `roles_obj` | 当前 55 列无命令行标量。 | 确定 |
| `process_path` | 当前进程路径 | `roles.target.process.path` | `roles_obj` | 保留完整路径。 | 确定 |
| `process_md5` | 当前进程映像文件 MD5 | `roles.target.process.file.hashes.md5` | `roles_obj` | 作为当前进程映像属性，哈希统一小写。 | 确定 |
| `process_sha1` | 当前进程映像文件 SHA-1 | `roles.target.process.file.hashes.sha1` | `roles_obj` | 作为当前进程映像属性，哈希统一小写。 | 确定 |
| `process_user` | 当前进程运行账号 | `roles.target.process.user.name` | `roles_obj` | 这是目标进程的运行身份，不能据此生成 `source_user`。 | 确定 |
| `process_create_time` | 当前进程创建时间 | `roles.target.process.created_time` | `roles_obj` | 按 Unix 毫秒转换为带时区时间；不覆盖事件发生时间。 | 确定 |
| `process_current_directory` | 当前工作目录 | `roles.target.process.working_directory` | `roles_obj` | 保留完整目录，不误写成进程映像路径。 | 确定 |
| `process_integrity_level` | 进程完整性级别 | `roles.target.process.integrity` | `roles_obj` | 保留来源值；完成枚举治理前不自行换算数值等级。 | 确定 |
| `process_parent_*` | 直接父进程属性 | 创建事件：`roles.source.process.*`；终止事件：`roles.related[]`，`relation_type=parent_process` | `roles_obj` | 创建事件能证明父进程创建了目标进程；终止事件只能将父进程作为关联对象，不能误判为行为主体。 | 确定结构 |
| `process_pparent_*` | 祖父进程属性 | `roles.related[]`，`relation_type=grandparent_process` | `roles_obj` | 构造独立进程关联对象；关系类型使用固定值，不编码对象 ID。 | 确定结构 |
| `process_root_*` | 根进程属性 | `roles.related[]`，`relation_type=root_process` | `roles_obj` | 仅保存非空且有意义的根进程字段；不能把占位值 `0` 当作真实进程。 | 候选 |
| `process_terminate_time` | 进程结束时间 | `roles.target.process.terminated_time` | `roles_obj` | 仅结束事件填写；空值、`0` 等哨兵值不保存。 | 确定 |
| `user_logon_id` | 当前进程用户 SID | `roles.target.process.user.id` | `roles_obj` | 样例值是 Windows SID，不作为用户名或认证会话编号。 | 确定 |
| `user_session_id` | 当前进程用户会话编号 | `roles.target.process.user.session_id` | `roles_obj` | 与进程运行用户绑定；不写 `facets.authentication.session_id`。 | 确定 |
| `computer_name`、`ip`、`client_ip`、`report_ip` | 发生行为的受管终端 | `roles.source.host.*` | `source_host` + `roles_obj` | IP 是主机属性时不自动投影 `source_ip`；只有行为网络端点语义明确时才投影。 | 候选 |
| `mac` | 受管终端 MAC | `roles.source.host.mac` | `source_mac` + `roles_obj` | 规范化后写来源主机资产属性；不写 `roles.source.endpoint.mac`，也不在来源私有扩展中重复保存。 | 确定 |
| `asset_id`、`client_id`、`mid`、`gid`、`group_name`、`asset_oid`、`env_version` | 终端资产上下文 | 见第 3 节 | `extensions.profiles.endpoint_asset` | 分别构造资产、Agent、分组和组织字段。 | 确定 |
| `task_id`、`sub_task_id`、`logger`、`type`、`custom_group_paths` | 天擎处理上下文和冗余分组路径 | — | 不落库 | 中间版本不参与检索或事件语义；完整原值仍保留在 `raw_msg`。 | 丢弃 |
| `payload` | 原始或半原始载荷 | `raw_msg` 的来源内容之一 | `raw_msg` | 保留完整源日志原文，不重复写入 VARIANT。 | 确定 |
| `process_internal_name`、`process_company`、`process_product`、`process_version`、`process_description` | 进程映像文件元数据 | `roles.target.process.file.internal_name/company_name/product.name/version/description` | `roles_obj` | 按独立字段保存，不拼成描述文本。 | 确定 |
| `process_sign` | 进程映像签名主体 | `roles.target.process.file.signatures[].signer` | `roles_obj` | 只保存来源提供的签名主体；不能据此生成签名状态或验证结果。 | 确定 |
| `process_original_name` | PE OriginalFilename | `roles.target.process.file.original_name` | `roles_obj` | 与 `internal_name` 分开保存，不因示例值相同而合并。 | 确定 |
| `process_copyright` | PE 版权信息 | — | 不落库 | 当前样例为空且无检索需求；完整原值仍保留在 `raw_msg`。 | 丢弃 |

### 5.4 `edr_file_audit`

#### 事件评估

- 当前真实样例是终端账号通过 `explorer.exe` 将 DOCX 文件上传到站点侧远端路径。
- 映射为 `record_kind=activity`、`event_domain=endpoint`、`event_type=file_creation`、`operation=upload`、`outcome=observed`。
- `transfer_method=upload_to_site` 提供上传动作证据；`result=0` 没有枚举说明，不能推断为成功。

| WPL 输出字段 | 字段含义 | SDM 逻辑路径 | Doris 物理落位 | 组合/转换逻辑 | 状态 |
|---|---|---|---|---|---|
| `create_time` | 文件审计事件时间 | `metadata.occur_time` | `occur_time` | 首选事件时间。`report_time` 是上报时间，不覆盖事件时间。 | 候选 |
| `transfer_method=upload_to_site` | 文件上传动作 | `event.type`、`event.operation` | `event_type`、`operation` | 映射为 `file_creation/upload`。 | 确定 |
| `operation_type`、`behavior`、`result` | 来源动作和结果代码 | — | — | 当前均为 0 且无枚举说明，不参与事件类型或结果推断。 | 待确认枚举 |
| `process_name` | 执行文件上传的进程 | `roles.source.process.name` | `roles_obj` | 当前进程是行为主体，不作为 carrier。 | 确定 |
| `remote_file_path`、`file_name`、`file_id` | 上传后的远端文件 | `roles.target.file.*` | `target_file_path` + `roles_obj` | 远端文件是事件客体；file_id 只作为文件标识。 | 确定 |
| `local_file_path` | 本地来源文件 | `roles.related[].file.path` | `roles_obj` | 关系类型 `source_file`；当前只有文件名，不补造目录。 | 确定 |
| `file_size` | 文件大小 | target/related file size | `roles_obj` | 解析为非负整数；当前候选单位为字节。 | 待确认单位 |
| `upload_url` | 上传目标 URL | `roles.target.url.full` | `roles_obj` | 保留完整 URL；解析出明确域名时可投影 `target_domain`。 | 候选 |
| `transfer_channel` | 来源传输渠道代码 | — | — | 当前值 4 缺少枚举说明，暂不保存。 | 待确认 |
| `usb_type` | 移动存储类型 | `roles.related[].device.type` | `roles_obj` | 构造关联设备；无设备 ID 时不要生成虚假 ID。 | 候选 |
| `local_file_is_exists`、`handle`、`audit_type` | 来源审计代码 | — | — | 当前没有枚举说明，不构造 finding 或私有扩展。 | 待确认 |
| `client_name`、`client_ip`、`client_report_ip`、`client_mac`、`client_login_account` | 行为发生终端和账号 | `roles.source.host.*`、`roles.source.account.name` | `source_host` + `roles_obj` | 网络端点语义不明确时不投影 `source_ip`。 | 候选 |
| `asset_id`、`client_id`、`client_mid`、OS 和当前分组 | host + endpoint_asset Profile | `roles_obj` + `extensions_obj` | 只保存实体和 Profile 所需增量，不复制完整资产快照。 | 确定 |
| `report_time`、`collect_time` | 上报/采集时间 | 来源私有处理时间 | `extensions_obj` | 不覆盖 `ingest_time`，除非可证明与平台接收时间语义一致。 | 候选 |
| `syslog_topic` | 路由主题 | — | 通常不落库 | `log_type` 已表达稳定日志类型；仅排障确有价值时保留私有字段。 | 候选删除 |

### 5.5 `edr_ip_access`

> 样例实现已补充到 `examples/tianqing/edr_ip_access`。当前按网络五元组语义实现两条分支：出站建立 (`open/success`) 和入站拒绝 (`refuse/failure`)。入站场景中外部 IP 是 source，受管终端是 target host；不能用采集终端身份覆盖网络角色。OML 仍需以天擎实际枚举和更多原始样本做联调确认。

#### 事件评估

- 事件事实：受管终端进程发起或接收的一次 IP 网络连接活动。
- `record_kind=activity`、`event_domain=network`、`event_type=network_connection`。
- `operation` 按 `network_connection_initiated` 和原始 `event_type` 映射 `open/close/reset/fail/refuse/traffic/listen`；没有证据时留空。

| WPL 输出字段 | 字段含义 | SDM 逻辑路径 | Doris 物理落位 | 组合/转换逻辑 | 状态 |
|---|---|---|---|---|---|
| `event_date_creation` | 网络事件发生时间 | `metadata.occur_time` | `occur_time` | 首选时间；`timestamp` 用于一致性校验或备选。 | 候选 |
| `uuid` | 天擎网络事件 UUID | `metadata.original_event_id` | `source_original_event_id` | 参与确定性生成 `event_id`。 | 候选 |
| `src_ip_addr` | 网络主动方 IP | `roles.source.endpoint.ip` | `source_ip` + `roles_obj` | 先校验 IP 格式。 | 确定 |
| `src_port` | 网络主动方端口 | `roles.source.endpoint.port` | `source_port` + `roles_obj` | 转为 0-65535 整数。 | 确定 |
| `src_host_name` | 网络主动方主机名 | `roles.source.host.name` | `source_host` + `roles_obj` | 保留来源主机名。 | 候选 |
| `dst_ip_addr` | 网络目标 IP | `roles.target.endpoint.ip` | `target_ip` + `roles_obj` | 先校验 IP 格式。 | 确定 |
| `dst_port` | 网络目标端口 | `roles.target.endpoint.port` | `target_port` + `roles_obj` | WPL 当前为字符串，写 Doris 前转为 0-65535 整数。 | 确定转换 |
| `dst_host_name` | 网络目标主机名 | `roles.target.host.name` | `target_host` + `roles_obj` | 保留来源主机名。 | 候选 |
| `network_protocol` | 网络协议 | `facets.network.protocol` | `network_protocol` + `facets_obj` | 统一为小写标准值，例如 tcp/udp。 | 确定 |
| `inout` | 连接方向 | `facets.network.direction` | `facets_obj` | 根据天擎枚举归一为入/出方向标准值。 | 待确认枚举 |
| `network_connection_initiated` | 是否由本机发起连接 | `facets.network.direction`、角色校验 | `facets_obj` | 用于校验 src/target 角色；不得在值未知时交换两端。 | 待确认枚举 |
| `src_is_ipv6`、`dst_is_ipv6` | 地址族标志 | 来源私有字段或地址校验结果 | `extensions_obj` | IP 地址本身已能确定版本时可不保留，仅用于质量校验。 | 候选删除 |
| `event_type` | 天擎网络动作类型 | `event.operation` | `operation` | 只映射合法的 `network_connection` 动作，不原样写入。 | 待确认枚举 |
| `process_name`、`process_guid`、`process_id`、`process_command_line`、`process_path` | 承载网络连接的进程 | `roles.carriers[].process.*` | 进程 3 个标量投影 + `roles_obj` | name/guid/pid 投影；命令行、路径留在完整对象。 | 确定 |
| `process_md5`、`process_sha1` | 进程映像文件哈希 | `roles.carriers[].process.file.hashes.md5/sha1` | `roles_obj` | 写入当前承载进程的映像文件对象，哈希统一小写。 | 确定 |
| `process_original_name`、`process_internal_name`、`process_sign`、`process_version` | 进程映像名称、签名和版本 | `roles.carriers[].process.file.*` | `roles_obj` | 分别映射到 `original_name`、`internal_name`、`signatures[].signer` 和 `version`。 | 确定 |
| `process_parent_*` | 父进程属性 | `roles.related[].process.*` | `roles_obj` | 与当前承载进程分开构造，关系类型为 `parent_process`。 | 确定结构 |
| `process_user` | 进程运行用户 | `roles.carriers[].process.user.name` | `roles_obj` | 用户属于承载连接的当前进程，不投影为网络主动方用户。 | 确定 |
| `computer_name`、`ip`、`report_ip`、`mac` | 受管终端资产属性 | 角色 host + endpoint_asset Profile | `roles_obj` + `extensions_obj` | 不覆盖明确的 `src_ip_addr/dst_ip_addr` 网络端点。 | 确定边界 |
| `asset_id`、`client_id`、`mid`、分组字段 | 终端资产上下文 | 见第 3 节 | `extensions_obj` | 构造 endpoint_asset Profile。 | 候选 |

### 5.6 `edr_file_op`

#### 事件评估

- 当前真实样例为 `event_type=file_write`，事实是受管终端进程写入一个文件。
- 映射为 `record_kind=activity`、`event_domain=endpoint`、`event_type=file_modification`、`operation=write`、`outcome=observed`。
- 当前只确认 `file_write` 分支；其他动作等待真实样例和枚举。

| WPL 输出字段 | 字段含义 | SDM 逻辑路径 | Doris 物理落位 | 组合/转换逻辑 | 状态 |
|---|---|---|---|---|---|
| `event_date_creation` | 文件操作发生时间 | `metadata.occur_time` | `occur_time` | Unix 毫秒；缺失时才使用 `timestamp`。 | 确定 |
| `uuid` | 来源事件 ID | `metadata.original_event_id` | `source_original_event_id` | 参与确定性生成 event_id。 | 确定 |
| `event_type=file_write` | 文件写入动作 | `event.type`、`event.operation` | `event_type`、`operation` | 映射 `file_modification/write`。 | 确定 |
| `computer_name/asset_id/ip/mac` | 受管终端 | `roles.source.host.*` | `source_host/source_mac` + `roles_obj` | IP 作为 host 属性，不生成网络 source_ip。 | 确定 |
| `process_*` | 执行文件操作的主体进程及映像 | `roles.source.process.*` | `source_process_name` + `roles_obj` | `process_id` 作为 PID；用户和映像信息进入 source process；carriers 为空。 | 确定 |
| `process_parent_*` | 父进程 | `roles.related[].process.*` | `roles_obj` | 关系类型 `parent_process`。 | 确定 |
| `file_name/file_path/file_md5` | 被操作文件 | `roles.target.file.*` | `target_file_name/target_file_path` + `roles_obj` | `file_md5` 属于目标文件。 | 确定 |
| `file_date_creation/file_previous_date_creation` | 文件时间 | target/related file 时间 | `roles_obj` | `0` 是哨兵值，当前样例不落库。 | 条件 |
| `file_name_renamed/file_path_renamed` | 重命名后的文件 | 待真实 rename 样例确认 | `roles_obj` | 当前为空，不生成对象。 | 待确认 |
| `removable_device` | 是否涉及可移动设备 | `roles.related[].device` 候选 | `roles_obj` | 当前为 0，不生成对象。 | 待确认 |
| `asset_oid/client_id/mid/gid/group_name` | 资产上下文 | endpoint_asset Profile | `extensions_obj` | 保存 Agent、组织和分组增量字段。 | 确定 |

### 5.9 `edr_dns_access`

#### 事件评估

- 当前真实样例是终端发起的 DNS 查询，查询域名为 `kv501.prod.do.dsp.mp.microsoft.com`，返回一个 A 记录地址。
- 映射为 `record_kind=activity`、`event_domain=network`、`event_type=network_dns`、`operation=query`、`outcome=success`、`severity=info`。
- 查询终端是 source，查询域名是 target domain，发起查询的 `svchost.exe` 是 carrier；DNS 返回地址是 facet answer，不是 target IP。

| WPL 输出字段 | 字段含义 | SDM 逻辑路径 | Doris 物理落位 | 组合/转换逻辑 | 状态 |
|---|---|---|---|---|---|
| `event_date_creation` | DNS 查询时间 | `metadata.occur_time` | `occur_time` | Unix 毫秒；缺失时使用 `timestamp`。 | 确定 |
| `uuid` | 来源事件 ID | `metadata.original_event_id` | `source_original_event_id` | 参与确定性生成 event_id。 | 确定 |
| `event_type=DNS_Query` | DNS 查询事实 | `event.type` | `event_type` | 归一为 `network_dns`。 | 确定 |
| `dns_host_name` | 查询域名 | `roles.target.domain.name`、`facets.dns.question.name` | `target_domain` + `roles_obj/facets_obj` | 同一语义在 target 和 facet 保持一致。 | 确定 |
| `dns_typed=1` | DNS 类型代码 | `facets.dns.question.type` | `facets_obj` | DNS 类型 1 归一为 `A`。 | 条件 |
| `dns_query_results` | DNS 应答地址 | `facets.dns.answers[].address` | `facets_obj` | 按逗号或数组拆分；当前为单个 IPv4。 | 确定 |
| `dns_query_status=0` | DNS 应答状态 | `facets.dns.response.code`、`event.outcome` | `facets_obj` + `outcome` | 0 且有应答映射 `success`；非零枚举待确认。 | 候选 |
| `computer_name/asset_id/ip/mac` | 查询终端 | `roles.source.host.*` | `source_host` + `roles_obj` | 终端 IP 是 host 属性，不生成 DNS 服务器 source_ip。 | 确定 |
| `process_*` | 发起 DNS 查询的进程 | `roles.carriers[].process.*` | carrier 三个标量 + `roles_obj` | 进程用户写入 carrier user。 | 确定 |
| `process_parent_*` | 查询进程父进程 | `roles.related[].process.*` | `roles_obj` | 关系类型 `parent_process`。 | 确定 |
| `asset_oid/client_id/mid/gid/group_name` | 资产上下文 | endpoint_asset Profile | `extensions_obj` | 保存 Agent、组织和分组增量字段。 | 确定 |

### 5.10 `edr_process_inject`

#### 事件评估

- 当前真实样例是 `services.exe` 对 `TrustedInstaller.exe` 产生的进程注入事件。
- 映射为 `record_kind=activity`、`event_domain=endpoint`、`event_type=process_injection`、`operation=remote_thread`、`outcome=observed`。
- `remote_thread` 由目标线程字段推导，置信度为中；来源没有结果字段，不能映射为成功或失败。

| WPL 输出字段 | 字段含义 | SDM 逻辑路径 | Doris 物理落位 | 组合/转换逻辑 | 状态 |
|---|---|---|---|---|---|
| `event_date_creation` | 进程注入事件时间 | `metadata.occur_time` | `occur_time` | Unix 毫秒；缺失时使用 `timestamp`。 | 确定 |
| `uuid` | 来源事件 ID | `metadata.original_event_id` | `source_original_event_id` | 参与确定性生成 `event_id`。 | 确定 |
| `event_type=Process_Injection` | 进程注入事实 | `event.type` | `event_type` | 归一为 `process_injection`。 | 确定 |
| `process_*` | 发起注入的进程及映像 | `roles.source.process.*` | `roles_obj` | 主动进程属于 source，不作为 carrier；当前 55 列表不重复投影 source process。 | 确定 |
| `process_user` | 主动进程用户 | `roles.source.user.name`、source process user | `source_user` + `roles_obj` | 同时表达事件主体用户与进程运行用户。 | 确定 |
| `target_process_*` | 被注入进程 | `roles.target.process.*` | `roles_obj` | 名称可从路径 basename 确定性取得。 | 确定 |
| `target_thread_id/address/args/module_path` | 注入目标线程信息 | `facets.process.injection.target_thread.*` | `facets_obj` | 全部转为字符串；地址不做数值运算。 | 确定 |
| `process_parent_*` | 主动进程父进程 | `roles.related[].process.*` | `roles_obj` | 关系类型 `parent_process`。 | 确定 |
| `execute_method_name` | 注入方式名称 | `facets.process.injection.method`、`event.operation` | `facets_obj` + `operation` | 当前为空，依据线程证据候选映射 `remote_thread`；需枚举确认。 | 候选 |
| `injected_dll` | 注入 DLL | carrier file 或进程注入载荷 | `roles_obj` 或 `facets_obj` | 当前为空，不输出；非空样例需评审对象边界。 | 待确认 |
| `computer_name/asset_id/ip/mac` | 受管终端 | `roles.source.host.*` | `source_host` + `roles_obj` | IP 是 host 属性，不生成网络 source_ip。 | 确定 |
| `asset_oid/client_id/mid/gid/group_name` | 资产上下文 | endpoint_asset Profile | `extensions_obj` | 保存 Agent、组织和分组增量字段。 | 确定 |

### 5.11 `edr_reg_change`

#### 事件评估

- 当前真实样例是 `services.exe` 设置 Windows Update 服务注册表键下的 `Start` 值。
- 映射为 `record_kind=activity`、`event_domain=system`、`event_type=registry_modification`、`operation=null`、`outcome=observed`。
- 来源没有执行结果；变更前后数据均为 `2`，只能保留原始事实，不能推断修改是否产生实际状态变化。

| WPL 输出字段 | 字段含义 | SDM 逻辑路径 | Doris 物理落位 | 组合/转换逻辑 | 状态 |
|---|---|---|---|---|---|
| `event_date_creation` | 注册表事件时间 | `metadata.occur_time` | `occur_time` | Unix 毫秒；缺失时使用 `timestamp`。 | 确定 |
| `uuid` | 来源事件 ID | `metadata.original_event_id` | `source_original_event_id` | 参与确定性生成 `event_id`。 | 确定 |
| `event_type=registry_set_value` | 设置注册表值 | `event.type` | `event_type` | 归一为 `registry_modification`；operation 留空。 | 确定 |
| `process_*` | 执行修改的进程及映像 | `roles.source.process.*` | `roles_obj` | 主动进程属于 source，不作为 carrier。 | 确定 |
| `process_user` | 主动进程用户 | `roles.source.user.name`、source process user | `source_user` + `roles_obj` | 同时表达事件主体用户与进程运行用户。 | 确定 |
| `registry_key_path` | 注册表键路径 | target resource、`facets.registry.key.path` | `roles_obj` + `facets_obj` | 原样保留完整内核注册表路径。 | 确定 |
| `registry_key_path_renamed` | 重命名后键路径 | `facets.registry.key.renamed_path` | `facets_obj` | 仅非空时输出。 | 条件 |
| `registry_value_name/type` | 注册表值名称和类型 | `facets.registry.value.name/type` | `facets_obj` | Windows 类型代码 4 归一为 `reg_dword`。 | 确定 |
| `registry_value_details/size` | 变更前值和字节数 | `facets.registry.value.previous.*` | `facets_obj` | 值保留字符串，字节数转非负整数；旧值语义待字段说明确认。 | 候选 |
| `registry_value_details_new/size_new` | 变更后值和字节数 | `facets.registry.value.current.*` | `facets_obj` | 值保留字符串，字节数转非负整数。 | 确定 |
| `process_parent_*` | 主动进程父进程 | `roles.related[].process.*` | `roles_obj` | 关系类型 `parent_process`。 | 确定 |
| `computer_name/asset_id/ip/mac` | 受管终端 | `roles.source.host.*` | `source_host` + `roles_obj` | IP 是 host 属性，不生成网络 source_ip。 | 确定 |
| `asset_oid/client_id/mid/gid/group_name` | 资产上下文 | endpoint_asset Profile | `extensions_obj` | 保存 Agent、组织和分组增量字段。 | 确定 |

### 5.7 `edr_wmi_event`

#### 事件评估

- 当前两条真实样例均为 `wmi_execute`，由 Winmgmt 服务进程执行 WQL 查询。
- 暂映射为 `record_kind=activity`、`event_domain=endpoint`、`event_type=process_uncategorized`、`operation=null`、`outcome=observed`。
- 原始日志的 `source_process_*` 和 `execute_method_*` 未被 WPL 抽取，因此当前只能形成不完整主体关系。

| WPL 输出字段 | 字段含义 | SDM 逻辑路径 | Doris 物理落位 | 组合/转换逻辑 | 状态 |
|---|---|---|---|---|---|
| `event_date_creation` | WMI 事件时间 | `metadata.occur_time` | `occur_time` | Unix 毫秒，缺失时使用 timestamp。 | 确定 |
| `uuid` | 来源事件 ID | `metadata.original_event_id` | `source_original_event_id` | 参与确定性生成 event_id。 | 确定 |
| `event_type=wmi_execute` | WMI 执行动作 | `event.type` | `event_type` | 暂映射 `process_uncategorized`，operation 留空。 | 候选 |
| `computer_name/asset_id/ip/mac` | 受管终端 | `roles.source.host.*` | `source_host/source_mac` + `roles_obj` | 主机是事件环境，IP 不生成网络 source_ip。 | 确定 |
| `process_*` | Winmgmt WMI 服务进程及映像 | `roles.carriers[].process.*` | carrier 三个标量 + `roles_obj` | 当前只能确认其承载 WMI 查询。 | 确定 |
| `process_parent_*` | WMI 服务父进程 | `roles.related[].process.*` | `roles_obj` | 关系类型 `parent_process`。 | 确定 |
| `wmi_filter_wql` | WQL 查询语句 | `extensions.source_private.qax.tianqing.edr_wmi_event.filter_wql` | `extensions_obj` | 当前无等价标准路径，保留稳定私有字段。 | 候选 |
| `wmi_namespace/wmi_operation/wmi_consumer_*` | WMI 对象和操作属性 | 同一 WMI 私有对象 | `extensions_obj` | 仅非空时输出。 | 条件 |
| 原始 `source_process_*` | WMI 请求发起进程 | 当前无 WPL 输出 | — | WPL 未抽取，OML 不得构造。 | 阻塞 |
| `asset_oid/client_id/mid/gid/group_name` | 资产上下文 | endpoint_asset Profile | `extensions_obj` | 保存 Agent、组织和分组增量字段。 | 确定 |

### 5.8 `edr_powershell_cmd_exec`

#### 事件评估

- 当前真实样例是已存在 PowerShell 进程中的脚本命令执行，`powershell_create_time` 比事件时间早约 63 秒。
- 不能映射为 `process_launch`。当前受控事件类型没有脚本执行类型，暂映射 `record_kind=activity`、`event_domain=endpoint`、`event_type=generic_event`、`operation=null`、`outcome=observed`。
- 主体是受管终端上的 SYSTEM 用户；载体是 PowerShell 进程和脚本；当前没有可证明的客体。

| WPL 输出字段 | 字段含义 | SDM 逻辑路径 | Doris 物理落位 | 组合/转换逻辑 | 状态 |
|---|---|---|---|---|---|
| `event_date_creation` | 脚本事件发生时间 | `metadata.occur_time` | `occur_time` | Unix 毫秒；缺失时使用 `timestamp`。 | 确定 |
| `uuid` | 来源事件唯一标识 | `metadata.original_event_id` | `source_original_event_id` | 参与确定性生成 event_id。 | 确定 |
| `event_type/type=powershell_execute` | PowerShell 脚本执行事实 | `event.type` | `event_type` | 暂映射 `generic_event`，不填 operation。 | 候选 |
| `computer_name/asset_id/ip/mac` | 受管终端 | `roles.source.host.*` | `source_host/source_mac` + `roles_obj` | IP 是 host 属性，不生成网络 source_ip。 | 确定 |
| `process_user/security_id` | 执行用户和 Windows SID | `roles.source.user.*`、载体进程 user | `source_user` + `roles_obj` | SID 写 `uid/id`。 | 确定 |
| `process_*` | PowerShell 进程及映像 | `roles.carriers[].process.*` | carrier 进程标量 + `roles_obj` | `powershell_create_time` 写进程创建时间。 | 确定 |
| `script_id/script_command` | PowerShell 脚本标识和命令 | `roles.carriers[].script.*` | `roles_obj` | 脚本语言固定为 `powershell`。 | 确定 |
| `powershell_payload` | 脚本正文 | `roles.carriers[].script.content` | `roles_obj` | 仅非空时输出；当前样例为空。 | 条件 |
| `process_parent_*` | PowerShell 父进程 | `roles.related[].process.*` | `roles_obj` | 关系类型 `parent_process`。 | 确定 |
| `event_id/thread_id/keywords` | Windows 事件代码、线程号和关键字 | 来源私有 PowerShell 对象 | `extensions_obj` | 保留为稳定调查字段。 | 候选 |
| `asset_oid/client_id/mid/gid/group_name` | 资产上下文 | endpoint_asset Profile | `extensions_obj` | 保存 Agent、组织和分组增量字段。 | 确定 |

## 6. 不落库和待确认字段

### 6.1 默认不落库

| 字段 | 原因 |
|---|---|
| WPL 临时字段 `tmp1`、`tmp2` | 只承担中间计算，不是业务事实。 |
| 完整 `payload`、完整 `process_details` 的 VARIANT 副本 | 原文已由 `raw_msg` 保存，不应重复进入 VARIANT；结构化成员按需映射。 |
| 仅用于 WPL 路由且已被 `log_type` 表达的 `syslog_topic`、`type` | 重复信息，除非排障证明有长期保留价值。 |
| 可从标准值确定的 `src_is_ipv6`、`dst_is_ipv6` | 可用于标准化时质量校验，无需长期重复保存。 |

### 6.2 必须补齐的输入资料

1. 每个业务 `log_type` 至少 3 条脱敏样例，覆盖成功、失败和主要动作分支。
2. 天擎 `event_type`、`operation_type`、`behavior`、`result`、`status`、`severity`、`trigger_mode`、`inout` 等枚举表。
3. 所有来源时间字段的格式、时区和空值规则。
4. `uuid`、`guid`、`alert_id`、`asset_id` 的唯一性范围和重放稳定性说明。
5. `process_details`、`ioc_alerts`、`nic_list` 等数组的完整元素结构，取消只取 `[0]` 的截断方式。

## 7. 已知阻塞项

| 阻塞项 | 影响 | 处理要求 |
|---|---|---|
| `edr_account_change` 有两条同名规则 | 无法形成唯一 `mapping_id` 和确定的规则优先级 | 按 `account_change`、`account_changes` 的真实格式拆成稳定且不同的 `log_type`。 |
| `account_changes` 样例解析报 `expected <time>` | 该格式不能稳定进入映射层 | 修正时间抽取并补充验证样例。 |
| `ioc_alerts[0][0]`、`group_info[0]` 只取首项 | 丢失多 IOC、多组织节点事实 | WPL 保留完整数组，组合层逐项构造标准数组对象。 |
| 尚无批准的天擎映射契约 | 映射路径和枚举仍可能变化 | 完成样例验证和评审后，再登记独立映射契约。 |

## 8. 验收标准

- 每个正式接入的 `log_type` 都有唯一 `mapping_id`、明确时间来源和确定性 `event_id` 规则。
- WPL 输出字段在映射矩阵中只能有一种处理结果：标准字段、受治理扩展、明确丢弃或待确认阻塞。
- `event.type + event.operation` 组合通过 `event_operation_dictionary.json` 校验。
- `record_kind`、`outcome`、`severity` 只使用中间版本枚举文档允许的值。
- source/target 按行为主动方和受影响对象判定，不按攻击者/受害者字段名机械映射。
- 4 个 VARIANT 对象不包含完整原始日志，不发生数组首项截断。
- 标量投影与对应 VARIANT 逻辑路径值一致。
- 告警生成链路只通过 `ldm_alert.log_id_list` 关联本表 `log_id`，不在日志映射中直接拼装平台告警。

## 9. 映射登记状态

- 来源选择器：`vendor=qax`、`product=tianqing`、`format_version=1`。
- 已批准映射：无。
- `edr_alert_log` 注册表解析结果：未找到已登记映射。
- 本文档状态：候选映射，待样例、枚举和人工评审。
