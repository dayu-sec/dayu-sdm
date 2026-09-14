# SDM2.0 事件逻辑字段枚举说明

> 权威：`07-sdm-event-behavior.schema.json`（现行 `meta.schema_version` = `2.0`）。
> 本文说明行为事件现行闭合枚举与开放字段；物理表 `sdm_event_behavior`。
> 旧五层路径（`event.*` / `metadata.*` / `roles.*` / `source_finding.*`）见文末「已退役路径」，不得作为新写入目标。
> `event.type + event.operation` 105 项字典仅供存量对照，版本 `2026-08-05`。

## 事件种类

逻辑路径：`event_kind`。这是闭合枚举，新数据只能写入下列值。

| 枚举值 | 中文含义 |
|---|---|
| `behavior` | 行为事实：谁对谁做了什么。观察只能依附于行为事件 |

`state` 不是本阶段取值。

## 行为层次

逻辑路径：`behavior.layer`。这是闭合枚举，新数据只能写入下列值。

| 枚举值 | 中文含义 |
|---|---|
| `network` | 网络层观测 |
| `system` | 系统层观测 |
| `application` | 应用层观测 |

按实际观测层次判别，不按厂商产品名称推断。

## 行为类型

逻辑路径：`behavior.type`。这是闭合枚举，新数据只能写入下列值。

| 枚举值 | 中文含义 |
|---|---|
| `appear` | 出现：新实体从无到有 |
| `read` | 读取：数据原地被访问 |
| `change` | 变更：已有实体被修改 |
| `disappear` | 消失：实体从有到无 |
| `flow` | 流动：数据跨边界改变位置 |

来源无法分型时可省略。新动作归入五类，不扩模型。

## 行为结果

逻辑路径：`behavior.outcome`。这是闭合枚举，新数据只能写入下列值。

| 枚举值 | 中文含义 |
|---|---|
| `allowed` | 处置结果：请求被允许 |
| `denied` | 处置结果：请求被拒绝或阻断 |
| `success` | 执行结果：动作本身成功（须有退出码/执行确认等证据） |
| `failed` | 执行结果：动作本身失败 |
| `observed` | 记录段：仅确认观察到，无成败/处置语义 |
| `unknown` | 来源没有结果 |

三段不得混用。来源 `blocked` 按语义映射为 `denied`。`action=record` 且无 assertion 时默认 `observed`，协议层结果进 facet。

## 观察动作

逻辑路径：`observation.action`。这是闭合枚举，新数据只能写入下列值。

| 枚举值 | 中文含义 |
|---|---|
| `record` | 记录：无检测判断 |
| `detect` | 检测：必须有 assertion |
| `assess` | 研判：必须有 assertion |

## 实体类型

逻辑路径：`subject.entity_type` / `object.entity_type` / `carriers[].entity_type` / `observation.observer.entity_type`。这是闭合枚举，新数据只能写入下列值。

| 枚举值 | 中文含义 |
|---|---|
| `user` | 人员或用户主体 |
| `account` | 登录或授权账号 |
| `host` | 主机或终端 |
| `endpoint` | 网络通信端点 |
| `process` | 操作系统进程 |
| `file` | 文件 |
| `service` | 系统或网络服务 |
| `domain` | 域名 |
| `url` | URL |
| `device` | 采集设备或外设 |
| `resource` | 统一资源 |
| `application` | 应用程序 |
| `cloud` | 云资源 |
| `container` | 容器 |
| `certificate` | 数字证书 |
| `script` | 脚本 |

`geo` 不是独立类型。`carriers[]` 仅 8 类载体；`observation.observer` 仅 9 类观察者，见 object-fields.v1。

## 来源记录种类

逻辑路径：`meta.source_record.record_kind`。这是闭合枚举（07 Schema 收口），新数据只能写入下列值。

| 枚举值 | 中文含义 |
|---|---|
| `activity` | 行为活动记录 |
| `finding` | 来源设备的检测或安全发现 |
| `inventory` | 资产、软件、账号或配置清单 |
| `state` | 对象在某个时点的状态记录 |
| `remediation` | 隔离、阻断、删除等处置行为记录 |

## 数据来源类别

逻辑路径：`meta.data_source.category`。这是闭合枚举（07 Schema 收口），新数据只能写入下列值。

| 枚举值 | 语义 | 典型来源 |
|---|---|---|
| `auth` | 认证、登录、授权、会话 | SSH、VPN、sudo |
| `network` | 连接、流量、HTTP 访问 | Nginx、防火墙 |
| `audit` | 进程、文件、配置和操作审计 | auditd、Windows 4688 |
| `system` | 内核、服务和系统状态 | journald、systemd |
| `alert` | 来源侧告警/检测结论 | SOC、HIDS、EDR、IPS、WAF |
| `other` | 不属于上述类型 | 自定义事件 |

判别：category 问日志内容性质。防火墙攻击告警 = `alert`，纯流量 = `network`。`other` 禁止偷懒兜底。

废弃值不得再写入：`security_log`、`security_device`、`endpoint_security`、`web_attack`。

## Windows 注册表值类型

逻辑路径：`facets.registry.value.type`。这是闭合枚举，新数据只能写入下列值。

| 枚举值 | 中文含义 |
|---|---|
| `reg_none` | 未定义具体数据类型（Windows 类型代码 0） |
| `reg_sz` | 以空字符结尾的字符串（代码 1） |
| `reg_expand_sz` | 可展开环境变量的字符串（代码 2） |
| `reg_binary` | 任意二进制数据（代码 3） |
| `reg_dword` | 32 位小端整数（代码 4） |
| `reg_dword_big_endian` | 32 位大端整数（代码 5） |
| `reg_link` | 注册表符号链接（代码 6） |
| `reg_multi_sz` | 字符串数组（代码 7） |
| `reg_resource_list` | 设备驱动程序资源列表（代码 8） |
| `reg_full_resource_descriptor` | 完整资源描述符（代码 9） |
| `reg_resource_requirements_list` | 资源需求列表（代码 10） |
| `reg_qword` | 64 位小端整数（代码 11） |

## 事件类型与操作

历史对照：旧五层 `event.type` 是 105 项受控字典；`event.operation` 必须与当时的事件类型组合解释。
新行为信封不要求登记 `event.type`；`behavior.operation` 为开放动作名，必须归属 `behavior.type` 五类。
“—”表示该事件类型不允许填写 `event.operation`。已废弃类型只用于读取存量数据。

| 序号 | `event.type` | 中文含义 | 合法 `event.operation` | 动作中文说明 | 状态 |
|---:|---|---|---|---|---|
| 1 | `analyst_add_comment` | 分析人员添加评论 | — | — | 无需动作细分 |
| 2 | `analyst_update_priority` | 分析人员更新优先级 | — | — | 无需动作细分 |
| 3 | `analyst_update_reason` | 分析人员更新原因 | — | — | 无需动作细分 |
| 4 | `analyst_update_reputation` | 分析人员更新信誉 | — | — | 无需动作细分 |
| 5 | `analyst_update_risk_score` | 分析人员更新风险评分 | — | — | 无需动作细分 |
| 6 | `analyst_update_root_cause` | 分析人员更新根本原因 | — | — | 无需动作细分 |
| 7 | `analyst_update_severity_score` | 分析人员更新严重度评分 | — | — | 无需动作细分 |
| 8 | `analyst_update_status` | 分析人员更新状态 | — | — | 无需动作细分 |
| 9 | `analyst_update_verdict` | 分析人员更新研判结论 | — | — | 无需动作细分 |
| 10 | `device_config_update` | 设备配置更新 | — | — | 无需动作细分 |
| 11 | `device_firmware_update` | 设备固件更新 | — | — | 无需动作细分 |
| 12 | `device_program_download` | 设备程序下载 | — | — | 无需动作细分 |
| 13 | `device_program_upload` | 设备程序上传 | — | — | 无需动作细分 |
| 14 | `email_transaction` | 邮件事务 | `send`、`receive`、`scan`、`trace`、`mta_relay` | `send`：发送；`receive`：接收；`scan`：扫描；`trace`：邮件跟踪；`mta_relay`：邮件中继 | 完整映射 |
| 15 | `email_uncategorized` | 邮件未分类 | — | — | 无可靠动作映射 |
| 16 | `email_url_click` | 邮件URL点击 | — | — | 已废弃，只读兼容 |
| 17 | `entity_risk_change` | 实体风险变更 | — | — | 无需动作细分 |
| 18 | `eventtype_unspecified` | 事件类型未指定 | — | — | 已废弃，只读兼容 |
| 19 | `file_copy` | 文件复制 | — | — | 无需动作细分 |
| 20 | `file_creation` | 文件创建 | `upload`、`checkin` | `upload`：上传；`checkin`：签入 | 完整映射 |
| 21 | `file_deletion` | 文件删除 | `recycled`、`versions`、`site` | `recycled`：移入回收站；`versions`：版本操作；`site`：站点操作 | 完整映射 |
| 22 | `file_modification` | 文件修改 | `checkin`、`write` | `checkin`：签入；`write`：写入 | 完整映射 |
| 23 | `file_move` | 文件移动 | — | — | 无需动作细分 |
| 24 | `file_open` | 文件打开 | — | — | 无需动作细分 |
| 25 | `file_read` | 文件读取 | `download`、`preview`、`checkout`、`extended` | `download`：下载；`preview`：预览；`checkout`：签出；`extended`：扩展读取 | 完整映射 |
| 26 | `file_sync` | 文件同步 | — | — | 无需动作细分 |
| 27 | `file_uncategorized` | 文件未分类 | — | — | 无可靠动作映射 |
| 28 | `generic_event` | 通用事件 | — | — | 无可靠动作映射 |
| 29 | `group_creation` | 用户组创建 | — | — | 无需动作细分 |
| 30 | `group_deletion` | 用户组删除 | — | — | 无需动作细分 |
| 31 | `group_modification` | 用户组修改 | `assign_privileges`、`revoke_privileges`、`add_user`、`remove_user`、`add_subgroup`、`remove_subgroup` | `assign_privileges`：授予权限；`revoke_privileges`：撤销权限；`add_user`：添加用户；`remove_user`：移除用户；`add_subgroup`：添加子组；`remove_subgroup`：移除子组 | 完整映射 |
| 32 | `group_uncategorized` | 用户组未分类 | — | — | 无可靠动作映射 |
| 33 | `mutex_creation` | 互斥体创建 | — | — | 无需动作细分 |
| 34 | `mutex_uncategorized` | 互斥体未分类 | — | — | 无可靠动作映射 |
| 35 | `network_connection` | 网络连接 | `open`、`close`、`reset`、`fail`、`refuse`、`traffic`、`listen` | `open`：打开；`close`：关闭；`reset`：重置连接；`fail`：失败；`refuse`：拒绝连接；`traffic`：传输流量；`listen`：监听 | 完整映射 |
| 36 | `network_dhcp` | 网络DHCP | `discover`、`offer`、`request`、`decline`、`ack`、`nak`、`release`、`inform`、`expire`、`assign`、`renew`、`dns_update` | `discover`：发现；`offer`：提供租约；`request`：请求租约；`decline`：拒绝租约；`ack`：确认应答；`nak`：否定应答；`release`：释放租约；`inform`：通知配置；`expire`：租约过期；`assign`：分配；`renew`：续租；`dns_update`：更新 DNS | 部分映射 |
| 37 | `network_dns` | 网络DNS | `query`、`response`、`traffic` | `query`：查询；`response`：响应；`traffic`：传输流量 | 完整映射 |
| 38 | `network_flow` | 网络流量 | — | — | 无需动作细分 |
| 39 | `network_ftp` | 网络FTP | `put`、`get`、`poll`、`delete`、`rename`、`list` | `put`：上传写入；`get`：获取；`poll`：轮询；`delete`：删除；`rename`：重命名；`list`：列出 | 完整映射 |
| 40 | `network_http` | 网络HTTP | — | — | 无需动作细分 |
| 41 | `network_smtp` | 网络SMTP | `send`、`receive`、`scan`、`trace`、`mta_relay` | `send`：发送；`receive`：接收；`scan`：扫描；`trace`：邮件跟踪；`mta_relay`：邮件中继 | 完整映射 |
| 42 | `network_uncategorized` | 网络未分类 | — | — | 无可靠动作映射 |
| 43 | `process_injection` | 进程注入 | `remote_thread`、`load_library`、`queue_apc` | `remote_thread`：创建远程线程；`load_library`：加载动态库；`queue_apc`：排队 APC | 完整映射 |
| 44 | `process_launch` | 进程启动 | `spawn`、`fork`、`exec` | `spawn`：创建进程；`fork`：派生进程；`exec`：执行程序 | 完整映射 |
| 45 | `process_module_load` | 进程模块加载 | — | — | 无需动作细分 |
| 46 | `process_open` | 进程打开 | — | — | 无需动作细分 |
| 47 | `process_privilege_escalation` | 进程权限提升 | `set_user_id`、`assume_role` | `set_user_id`：设置用户标识；`assume_role`：承担角色 | 部分映射 |
| 48 | `process_termination` | 进程终止 | — | — | 无需动作细分 |
| 49 | `process_uncategorized` | 进程未分类 | — | — | 无可靠动作映射 |
| 50 | `registry_creation` | 注册表创建 | — | — | 无需动作细分 |
| 51 | `registry_deletion` | 注册表删除 | — | — | 无需动作细分 |
| 52 | `registry_modification` | 注册表修改 | — | — | 无需动作细分 |
| 53 | `registry_uncategorized` | 注册表未分类 | — | — | 无可靠动作映射 |
| 54 | `resource_creation` | 资源创建 | — | — | 无需动作细分 |
| 55 | `resource_deletion` | 资源删除 | — | — | 无需动作细分 |
| 56 | `resource_permissions_change` | 资源权限变更 | — | — | 无需动作细分 |
| 57 | `resource_read` | 资源读取 | — | — | 无需动作细分 |
| 58 | `resource_written` | 资源写入 | — | — | 无需动作细分 |
| 59 | `scan_file` | 扫描文件 | `started`、`completed`、`cancelled`、`duration_violation`、`pause_violation`、`error`、`paused`、`resumed`、`restarted`、`delayed` | `started`：已开始；`completed`：已完成；`cancelled`：已取消；`duration_violation`：持续时间超限；`pause_violation`：暂停时间超限；`error`：执行错误；`paused`：已暂停；`resumed`：已恢复；`restarted`：已重新启动；`delayed`：已延迟 | 完整映射 |
| 60 | `scan_host` | 扫描主机 | `started`、`completed`、`cancelled`、`duration_violation`、`pause_violation`、`error`、`paused`、`resumed`、`restarted`、`delayed` | `started`：已开始；`completed`：已完成；`cancelled`：已取消；`duration_violation`：持续时间超限；`pause_violation`：暂停时间超限；`error`：执行错误；`paused`：已暂停；`resumed`：已恢复；`restarted`：已重新启动；`delayed`：已延迟 | 完整映射 |
| 61 | `scan_network` | 扫描网络 | `started`、`completed`、`cancelled`、`duration_violation`、`pause_violation`、`error`、`paused`、`resumed`、`restarted`、`delayed` | `started`：已开始；`completed`：已完成；`cancelled`：已取消；`duration_violation`：持续时间超限；`pause_violation`：暂停时间超限；`error`：执行错误；`paused`：已暂停；`resumed`：已恢复；`restarted`：已重新启动；`delayed`：已延迟 | 完整映射 |
| 62 | `scan_process` | 扫描进程 | `started`、`completed`、`cancelled`、`duration_violation`、`pause_violation`、`error`、`paused`、`resumed`、`restarted`、`delayed` | `started`：已开始；`completed`：已完成；`cancelled`：已取消；`duration_violation`：持续时间超限；`pause_violation`：暂停时间超限；`error`：执行错误；`paused`：已暂停；`resumed`：已恢复；`restarted`：已重新启动；`delayed`：已延迟 | 完整映射 |
| 63 | `scan_process_behaviors` | 扫描进程行为 | — | — | 已废弃，只读兼容 |
| 64 | `scan_uncategorized` | 扫描未分类 | `started`、`completed`、`cancelled`、`duration_violation`、`pause_violation`、`error`、`paused`、`resumed`、`restarted`、`delayed` | `started`：已开始；`completed`：已完成；`cancelled`：已取消；`duration_violation`：持续时间超限；`pause_violation`：暂停时间超限；`error`：执行错误；`paused`：已暂停；`resumed`：已恢复；`restarted`：已重新启动；`delayed`：已延迟 | 完整映射 |
| 65 | `scan_vuln_host` | 扫描漏洞主机 | `started`、`completed`、`cancelled`、`duration_violation`、`pause_violation`、`error`、`paused`、`resumed`、`restarted`、`delayed` | `started`：已开始；`completed`：已完成；`cancelled`：已取消；`duration_violation`：持续时间超限；`pause_violation`：暂停时间超限；`error`：执行错误；`paused`：已暂停；`resumed`：已恢复；`restarted`：已重新启动；`delayed`：已延迟 | 完整映射 |
| 66 | `scan_vuln_network` | 扫描漏洞网络 | `started`、`completed`、`cancelled`、`duration_violation`、`pause_violation`、`error`、`paused`、`resumed`、`restarted`、`delayed` | `started`：已开始；`completed`：已完成；`cancelled`：已取消；`duration_violation`：持续时间超限；`pause_violation`：暂停时间超限；`error`：执行错误；`paused`：已暂停；`resumed`：已恢复；`restarted`：已重新启动；`delayed`：已延迟 | 完整映射 |
| 67 | `scheduled_task_creation` | 计划任务创建 | — | — | 无需动作细分 |
| 68 | `scheduled_task_deletion` | 计划任务删除 | — | — | 无需动作细分 |
| 69 | `scheduled_task_disable` | 计划任务禁用 | — | — | 无需动作细分 |
| 70 | `scheduled_task_enable` | 计划任务启用 | — | — | 无需动作细分 |
| 71 | `scheduled_task_modification` | 计划任务修改 | — | — | 无需动作细分 |
| 72 | `scheduled_task_uncategorized` | 计划任务未分类 | `start` | `start`：开始 | 部分映射 |
| 73 | `service_creation` | 服务创建 | `install` | `install`：安装 | 部分映射 |
| 74 | `service_deletion` | 服务删除 | `remove` | `remove`：移除 | 完整映射 |
| 75 | `service_modification` | 服务修改 | `enable`、`disable`、`update` | `enable`：启用；`disable`：禁用；`update`：更新 | 部分映射 |
| 76 | `service_start` | 服务启动 | `restart` | `restart`：重新启动 | 部分映射 |
| 77 | `service_stop` | 服务停止 | — | — | 无需动作细分 |
| 78 | `service_unspecified` | 服务未指定 | — | — | 无可靠动作映射 |
| 79 | `setting_creation` | 设置创建 | — | — | 无需动作细分 |
| 80 | `setting_deletion` | 设置删除 | — | — | 无需动作细分 |
| 81 | `setting_modification` | 设置修改 | — | — | 无需动作细分 |
| 82 | `setting_uncategorized` | 设置未分类 | — | — | 无可靠动作映射 |
| 83 | `status_heartbeat` | 状态心跳 | — | — | 无需动作细分 |
| 84 | `status_shutdown` | 状态关闭 | — | — | 无需动作细分 |
| 85 | `status_startup` | 状态启动 | — | — | 无需动作细分 |
| 86 | `status_uncategorized` | 状态未分类 | — | — | 无可靠动作映射 |
| 87 | `status_update` | 状态更新 | — | — | 无需动作细分 |
| 88 | `system_audit_log_uncategorized` | 系统审计日志未分类 | — | — | 无可靠动作映射 |
| 89 | `system_audit_log_wipe` | 系统审计日志清除 | `clear`、`delete` | `clear`：清除；`delete`：删除 | 完整映射 |
| 90 | `triage_agent_update_investigation` | 研判Agent更新调查 | — | — | 无需动作细分 |
| 91 | `user_badge_in` | 用户门禁卡进入 | — | — | 无可靠动作映射 |
| 92 | `user_change_password` | 用户变更密码 | — | — | 无需动作细分 |
| 93 | `user_change_permissions` | 用户变更权限 | `assign_privileges`、`revoke_privileges` | `assign_privileges`：授予权限；`revoke_privileges`：撤销权限 | 完整映射 |
| 94 | `user_communication` | 用户通信 | — | — | 无可靠动作映射 |
| 95 | `user_creation` | 用户创建 | — | — | 无需动作细分 |
| 96 | `user_deletion` | 用户删除 | — | — | 无需动作细分 |
| 97 | `user_login` | 用户登录 | `authentication_ticket`、`service_ticket_request`、`service_ticket_renew`、`preauth`、`account_switch`、`system`、`interactive`、`remote_interactive`、`service`、`remote_service`、`remote`、`assume_role` | `authentication_ticket`：获取认证票据；`service_ticket_request`：请求服务票据；`service_ticket_renew`：续订服务票据；`preauth`：预认证；`account_switch`：切换账号；`system`：系统登录；`interactive`：交互式登录；`remote_interactive`：远程交互式登录；`service`：服务登录；`remote_service`：远程服务登录；`remote`：远程登录；`assume_role`：承担角色 | 部分映射 |
| 98 | `user_logout` | 用户登出 | `system`、`interactive`、`remote_interactive`、`service`、`remote_service`、`remote` | `system`：系统登录；`interactive`：交互式登录；`remote_interactive`：远程交互式登录；`service`：服务登录；`remote_service`：远程服务登录；`remote`：远程登录 | 完整映射 |
| 99 | `user_resource_access` | 用户资源access | `download`、`preview`、`open` | `download`：下载；`preview`：预览；`open`：打开 | 完整映射 |
| 100 | `user_resource_creation` | 用户资源创建 | `upload` | `upload`：上传 | 完整映射 |
| 101 | `user_resource_deletion` | 用户资源删除 | — | — | 无需动作细分 |
| 102 | `user_resource_update_content` | 用户资源更新内容 | `update`、`rename`、`copy`、`move`、`restore`、`lock`、`unlock`、`sync`、`unsync` | `update`：更新；`rename`：重命名；`copy`：复制；`move`：移动；`restore`：恢复；`lock`：锁定；`unlock`：解锁；`sync`：同步；`unsync`：取消同步 | 部分映射 |
| 103 | `user_resource_update_permissions` | 用户资源更新权限 | `share`、`unshare`、`access_check` | `share`：共享；`unshare`：取消共享；`access_check`：访问检查 | 完整映射 |
| 104 | `user_stats` | 用户统计 | — | — | 已废弃，只读兼容 |
| 105 | `user_uncategorized` | 用户未分类 | — | — | 无可靠动作映射 |


## 非枚举字段

下列字段容易被误认为枚举，但 07 没有可执行的闭合集合。facet 叶子全表见字段目录 2.8。

| 逻辑路径 | 当前约束 | 备注 |
|---|---|---|
| `behavior.operation` | 开放动作名，必须归属五类 | 如 login、query、write、connect |
| `meta.source_record.log_level` | 原始日志等级，按来源契约 | 不是 assertion.severity |
| `observation.assertion.severity` | 检测严重度，按来源契约 | 与 log_level 分轨 |
| `facets.authentication.auth_type` | 认证方式，未形成闭合枚举 | |
| `facets.authentication.auth_result` | 认证专属结果，不等同于 behavior.outcome | |
| `facets.network.direction` | 网络方向，未形成闭合枚举 | |
| `facets.network.connection_result` | 协议层连接结果 | 不是 behavior.outcome |
| `facets.http.request.method` | HTTP 方法 | 开放 |
| `facets.dns.response.code` | DNS 应答码 | 不是 behavior.outcome |
| `facets.application.name` | 应用层名称 | 开放 |

## 写入规则

- 标准枚举值统一小写。
- `behavior.outcome` 不保存阻断动作字面量；来源 `blocked` 映射为 `denied`。
- 处置段 `allowed/denied` 须有 `observation.assertion.conclusion` 支撑。
- `meta.data_source.category` 按日志内容性质，不是设备类型。
- 不得写入已退役路径：`event.type`、`event.severity`、`event.domain`、`event.record_kind`、`event.outcome`、`metadata.*`、`roles.*`、`source_finding.*`。
- 开放字段新增推荐值须更新 07 / object-fields 与本文，不允许单个接入规则自由造词。

## 已退役路径

旧 `sdm_event` 五层路径，仅对照存量，禁止新写入。

| 旧路径 | 现行位置 |
|---|---|
| `event.record_kind` | `meta.source_record.record_kind` |
| `event.outcome` | `behavior.outcome` |
| `event.severity` | 已删除；日志等级 → `meta.source_record.log_level`，检测严重度 → `observation.assertion.severity` |
| `event.domain` | 已删除 |
| `event.type` / `event.operation` | `behavior.type` 五类 + `behavior.operation` 开放名 |
| `metadata.data_source.category` | `meta.data_source.category` |
| `metadata.log.*` | `meta.source_record.*` |
| `roles.source` / `roles.target` | `subject` / `object` |
| `roles.related[]` | 已删除；实体只在 subject / object / carriers |
| `roles.observer` | `observation.observer` |
| `source_finding.*` | `observation.assertion` |
| `source_finding.attack_direction` | 断言主张，不进事实层 |
