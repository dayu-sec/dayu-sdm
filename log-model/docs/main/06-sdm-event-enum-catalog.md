# SDM2.0 事件逻辑字段枚举说明

> 本文档独立于逻辑字段清单，集中说明当前中间版本使用的枚举和受控字典。
> 闭合枚举只能写入本文列出的值；开放字段的推荐值允许经评审扩展。
> `event.type + event.operation` 机器字典版本：`2026-08-05`。

## 记录种类

逻辑路径：`event.record_kind`。这是闭合枚举，新数据只能写入下列值。

| 枚举值 | 中文含义 |
|---|---|
| `activity` | 行为活动记录，表示已经发生或被观察到的操作。 |
| `finding` | 来源设备的检测或安全发现记录。 |
| `inventory` | 资产、软件、账号或配置清单记录。 |
| `state` | 对象在某个时点的状态记录。 |
| `remediation` | 隔离、阻断、删除等处置行为记录。 |

## 事件结果

逻辑路径：`event.outcome`。这是闭合枚举，新数据只能写入下列值。

| 枚举值 | 中文含义 |
|---|---|
| `success` | 操作成功完成。 |
| `failed` | 操作执行失败。 |
| `observed` | 仅确认观察到该操作，结果不适用。 |
| `denied` | 操作请求被拒绝或阻止。 |
| `allowed` | 操作请求被允许通过。 |
| `unknown` | 已知发生操作，但无法判断结果。 |

**取值判别（视角决定词表，按序自问）**：

```
这条日志里存在访问控制/策略判定吗？（防火墙/ACL/WAF/认证拒绝）
├─ 是 → 站在被判定的一方：被拦下 → denied；放行 → allowed
└─ 否（纯行为记录，无守门人）→ 站在行为主体：
     完成 → success；失败 → failed；
     只是观察到（无成败概念，如流量镜像）→ observed；判断不了 → unknown
```

易错对照：

| 场景 | 错 | 对 | 理由 |
|---|---|---|---|
| 登录被拒（密码错） | failed | denied | 认证是控制点判定 |
| 防火墙/WAF 阻断 | failed | denied | 策略拒绝，与 source_finding.action=block 对应 |
| 端口连不通（超时） | denied | failed | 无守门人，行为本身失败 |
| 流量会话记录 | success | observed | 镜像观察，无成败语义 |

一致性约束：`denied/allowed` 的事件几乎必然伴随 `source_finding.action`（block/allow）——二者是同一事实的两面。写了 denied 却无 action 声明，视为映射缺陷。

## 事件严重级别

逻辑路径：`event.severity`。这是闭合枚举，新数据只能写入下列值。

| 枚举值 | 中文含义 |
|---|---|
| `emerg` | 系统不可用的紧急情况。 |
| `alert` | 必须立即处理的警报。 |
| `crit` | 严重错误或严重故障。 |
| `error` | 一般错误。 |
| `warning` | 可能导致问题的警告。 |
| `notice` | 正常但值得注意的情况。 |
| `info` | 一般信息。 |
| `debug` | 调试信息。 |


## 数据来源类别

逻辑路径：`metadata.data_source.category`（物理列 `data_src_category`）。这是闭合枚举（2026-08-26 新增），新数据只能写入下列值。

| 枚举值 | 语义 | 典型来源 |
|---|---|---|
| `auth` | 认证、登录、授权、会话 | SSH、VPN、sudo |
| `network` | 连接、流量、HTTP 访问 | Nginx、防火墙 |
| `audit` | 进程、文件、配置和操作审计 | auditd、Windows 4688 |
| `system` | 内核、服务和系统状态 | journald、systemd |
| `alert` | 来源侧告警/检测结论 | SOC、HIDS、EDR、IPS、WAF |
| `other` | 不属于上述类型 | 自定义事件 |

判别口诀：**category 问日志内容性质，domain 问事件领域**——防火墙攻击告警 category=`alert`、domain=`threat`；防火墙纯流量 category=`network`、domain=`network`。

写入约束：
- `other` 仅在尝试过全部五类后仍无法归类时使用，禁止作为偷懒兜底；连续大量 `other` 应触发映射评审。
- 废弃值不得再写入：`security_log`、`security_device`、`endpoint_security`、`web_attack`（后者属事件粒度，归 `event.type` / `source_finding.category` 层）。

存量迁移映射（按 log_type 拆分）：

| 废弃值 | 迁移规则 |
|---|---|
| `endpoint_security`（天擎全线） | `edr_alert_log` 等告警类 → `alert`；`edr_process_event` / `edr_file_*` / `edr_reg_*` 等审计类 → `audit` |
| `security_log`（sangfor POC） | `fw_ips_protect_log` / `sip_atk_alarm_log` → `alert`；`flow_*` → `network` |
| `security_device` / `web_attack` | 按日志内容对号入座至五类 |

## 关联对象实体类型

逻辑路径：`roles.related[].entity_type、source_finding.entities.*[].entity_type`。这是闭合枚举，新数据只能写入下列值。

| 枚举值 | 中文含义 |
|---|---|
| `user` | 人员或用户主体。 |
| `account` | 用于登录或授权的账号。 |
| `host` | 主机或终端实体。 |
| `endpoint` | 网络通信端点。 |
| `process` | 操作系统进程。 |
| `file` | 文件对象。 |
| `service` | 系统或网络服务。 |
| `domain` | 域名对象。 |
| `url` | URL 对象。 |
| `device` | 采集设备或关联外设。 |
| `resource` | 统一资源对象。 |
| `application` | 应用程序或业务应用。 |
| `cloud` | 云资源对象。 |
| `container` | 容器对象。 |
| `certificate` | 数字证书对象。 |

## 事件领域推荐值

逻辑路径：`event.domain`。这是开放字段，下列值是当前中间版本推荐集合，不是强制全集。

| 枚举值 | 中文含义 |
|---|---|
| `identity` | 身份、登录和认证活动。 |
| `network` | 网络连接、流量和协议活动。 |
| `endpoint` | 终端、主机、进程和文件活动。 |
| `threat` | 威胁检测和安全发现。 |
| `asset` | 资产、配置和清单信息。 |
| `system` | 操作系统和系统审计活动。 |
| `application` | 应用程序和业务应用活动。 |
| `discovery` | 扫描、发现和探测活动。 |

## 攻击方向

逻辑路径：`source_finding.attack_direction`。这是闭合枚举，新数据只能写入下列值。

| 枚举值 | 中文含义 |
|---|---|
| `L2L` | 攻击方和受害方均位于受治理的内部网络。 |
| `L2W` | 攻击方位于内部网络，受害方位于外部网络。 |
| `W2L` | 攻击方位于外部网络，受害方位于内部网络。 |
| `W2W` | 攻击方和受害方均位于外部网络。 |
| `unknown` | 缺少边界信息，无法可靠判断攻击方向。 |

## Windows 注册表值类型

逻辑路径：`facets.registry.value.type`。这是闭合枚举，新数据只能写入下列值。

| 枚举值 | 中文含义 |
|---|---|
| `reg_none` | 未定义具体数据类型（Windows 类型代码 0）。 |
| `reg_sz` | 以空字符结尾的字符串（代码 1）。 |
| `reg_expand_sz` | 可展开环境变量的字符串（代码 2）。 |
| `reg_binary` | 任意二进制数据（代码 3）。 |
| `reg_dword` | 32 位小端整数（代码 4）。 |
| `reg_dword_big_endian` | 32 位大端整数（代码 5）。 |
| `reg_link` | 注册表符号链接（代码 6）。 |
| `reg_multi_sz` | 字符串数组（代码 7）。 |
| `reg_resource_list` | 设备驱动程序资源列表（代码 8）。 |
| `reg_full_resource_descriptor` | 完整资源描述符（代码 9）。 |
| `reg_resource_requirements_list` | 资源需求列表（代码 10）。 |
| `reg_qword` | 64 位小端整数（代码 11）。 |

## 事件类型与操作

`event.type` 是 105 项受控字典；`event.operation` 必须与当前事件类型组合解释。
“—”表示该事件类型不允许填写 `event.operation`。已废弃类型只用于读取存量数据，新数据禁止写入。

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

下列字段容易被误认为枚举，但当前没有可执行的闭合集合：

| 逻辑路径 | 当前约束 |
|---|---|
| `event.domain` | 开放字段，本文仅给出当前推荐值。 |
| `source_finding.severity` | 保存来源设备检测严重度，当前按来源契约映射，不与 `event.severity` 共用枚举。 |
| `facets.authentication.auth_type` | 认证方式，当前未形成闭合枚举。 |
| `facets.authentication.auth_result` | 认证专属结果，当前未形成闭合枚举，不等同于 `event.outcome`。 |
| `facets.authentication.auth_failure_reason` | 认证失败原因，当前未形成闭合枚举。 |
| `facets.network.direction` | 网络方向，当前未形成 SDM2.0 闭合枚举。 |
| `facets.network.connection_state` | 网络连接状态，当前未形成 SDM2.0 闭合枚举。 |

## 写入规则

- `data_src_category` 使用「数据来源类别」闭合枚举；判别以日志内容性质为准（不是设备类型），同一产品不同 log_type 可落不同枚举值。
- 所有标准枚举值统一使用小写形式。
- `event.outcome` 不保存阻断动作或检测结论；来源 `blocked` 应根据语义映射为 `denied`。
- `event.severity` 使用 syslog 八级；来源告警的高、中、低危写入 `source_finding.severity`。
- **severity 按 record_kind 分治（2026-08-26 修订）**：
  - `record_kind=finding`：`event.severity` 允许继承来源检测严重度，但必须经映射注册表统一换算表投影为 syslog 八级闭合枚举后写入；禁止在接入规则内各自换算（同一来源值只能有一条换算路径）。契约须在映射 manifest 中声明 `severity_policy: inherit_from_finding`，审计按此校验两列一致性——声明继承的 finding 事件两列换算后不相等视为违规。
  - 其他 `record_kind`（activity 等）：`event.severity` 独立赋值，仅在有独立行为证据时写入（如失败登录 → `warning`）；无证据留空，不从 `source_finding.severity` 复制。
- 来源处置动作必须写入标准键 `source_finding.action`（枚举：`block` / `allow` / `alert` / `reset` 等小写），不得写入 `source_finding.status`（该字段表示检测结果状态如 `active`）。列投影 `source_finding_action` 仅从 `source_finding.action` 读取；有动作语义时 `event.outcome` 按 action 推导（block→`denied`、allow→`allowed`），推导口径以 `event.type + event.operation` 机器字典为准。
- `metadata.schema_version` 是五层逻辑模型版本的唯一权威值；`extensions.schema_version`（如保留）必须与其一致，由 writer 模板同一常量产生，禁止两处独立维护出现分叉。
- 未在字典中的 `(event.type, event.operation)` 组合必须将 `event.operation` 留空。
- 开放字段新增推荐值时，需要更新契约和本文档，不应由单个接入规则自由造词。
