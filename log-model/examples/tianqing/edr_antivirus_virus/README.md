# `edr_antivirus_virus` 样例（病毒查杀日志）

本目录用于编写和验收天擎 `edr_antivirus_virus`（病毒查杀）日志的 OML 与 SDM2.0 映射。

| 文件 | 用途 |
|---|---|
| `adware_detection.raw-log.json` | 天擎真实原始日志（sample.dat:38） |
| `adware_detection.wpl-output.json` | 按 parse.wpl `edr_antivirus_virus` 规则抽取的 WPL 输出（39 字段） |
| `adware_detection.platform-context.json` | 平台上下文 |
| `adware_detection.expected-sdm-event.json` | 期望 SDM 事件 |
| `adware_detection.wpl-to-sdm-event.{json,md}` | 逐字段映射 |

## 事件事实

终端 `WIN-UMAG4B1GGKV`（账户 zhangpeng15，Windows 7 SP1）上，天擎实时查杀引擎（qce）检出广告软件 `Adware.Agent.30f0fd07`，命中文件为 `C:\Users\zhangpeng15\Desktop\宏病毒样本sample\宏病毒样本sample\出品部门牌_Key.vbs`（md5/sha1 见事件）。原始日志没有用户操作、进程执行或网络行为证据，因此不构建这些角色。

## 主体 / 客体 / 载体

- 主体：无主动行为主体（引擎检测事件，日志未提供触发进程/用户动作）；`roles.source.host` 是检出事件的发生/承载主机（观测位置），不是行为发起者
- 客体：检出文件 `出品部门牌_Key.vbs` → `roles.target.file`（name/path/hashes）
- 载体：查杀引擎 qce、触发方式 trigger_mode=2（枚举待确认）；引擎标识入 source_private
- 受管终端：`WIN-UMAG4B1GGKV` → `roles.source.host` + `extensions.profiles.endpoint_asset`

## 关键映射决策

- `event_category=alert`：病毒检出是来源检测结论。
- `event_type=generic_event`：标准无恶意软件检出类型。
- 检测结论入 `source_finding`：title（检出病毒名）、severity（原始 "0"，不进顶层）、category.original（adware/广告软件）。
- PDF §3.2.1 `result=1` = 删除成功，写入 `source_private.result`，**不**进 `outcome`，也**不**进 `source_finding.status`。
- `outcome=observed`：检出为观察结果。
- 顶层 `severity=info`：按闭合枚举取一般信息级；来源 `severity=0` 留在 finding。
- 事件时间 `occur_time` = file_alarm_time（WPL 纳秒→毫秒）；文件创建时间 file_create_time 因 registry 无 `roles.target.file.created_time` 路径未落库（未决 4）。
- 终端资产：`roles.source.host`（name/report_ip/mac/domain）+ `profiles.endpoint_asset`（agent.id=client_id、fingerprint_id=mid、ownership=asset_oid/group）。
- `source_original_event_id` = guid（WPL 已抽，非标准 GUID 格式，未决 5）。
- 客户端资产画像元数据（os 版本/内存/网卡等）无检索价值，不落库。

## 舍弃字段

| 字段 | 原因 |
|---|---|
| `os`/`release_id`/`main`/`describe`/`sys_space`/`core_number`/`memory_size`/`ie_version`/`nic_list`/`report_ipv6`/`state`/`activation`/`system_language`/`computer_working_group`/`os_bit` | 资产画像元数据，无检索价值，原值保留 raw_msg |
| `create_time`/`update_time` | 客户端登记/更新时间，非事件时间 |
| `login_account` | 终端登录账户，资产上下文；无独立用户主体动作，不建角色级 user |
| `file_create_time` | registry 无 `roles.target.file.created_time` 路径 |
| `client_info`/`group_info` 其余嵌套 | 规则抽取外的上下文，raw_msg 可回查 |

## 未决问题

1. 06 枚举无恶意软件检出事件类型（无 malware/virus/detection 类），暂用 generic_event（#28）；建议后续扩展 `malware_detection`。
2. `result=1` 已由 Syslog V1.11 §3.2.1 确认为删除成功；只进 `source_private.result`。`trigger_mode=2` 仍待确认。
3. `asset_id` 未在规则 json() 中直接抽取，样例由平台上下文提供；建议规则补抽 `@asset_id`。
4. `roles.target.file.created_time` 路径未注册（registry 无），file_create_time 暂不落库。
5. `guid` 非标准 GUID（sddguid 前缀、短横线位置异常），source_original_event_id 保留原值。

## 当前物理注册表迁移

本目录 expected 已迁移到当前 87 字段物理注册表。原始日志与映射身份未丢失：原文保存在 `*.raw-log.json`，expected 与 raw_log 的关联统一用 `event_id`，mapping 身份保存在对应映射 JSON/Markdown。
