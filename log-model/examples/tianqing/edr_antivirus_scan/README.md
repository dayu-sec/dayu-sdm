# `edr_antivirus_scan` 样例（病毒扫描日志）

本目录用于编写和验收天擎 `edr_antivirus_scan`（病毒扫描）日志的 OML 与 SDM2.0 映射。

| 文件 | 用途 |
|---|---|
| `customize_scan.raw-log.json` | 天擎真实原始日志（sample.dat:8） |
| `customize_scan.wpl-output.json` | 按 parse.wpl `edr_antivirus_scan` 规则抽取的 WPL 输出（44 字段） |
| `customize_scan.wpl-missing-fields.json` | WPL 抽取缺口（asset_id）与故意不抽字段 |
| `customize_scan.platform-context.json` | 平台上下文 |
| `customize_scan.expected-sdm-event.json` | 期望 SDM 事件 |
| `customize_scan.wpl-to-sdm-event.{json,md}` | 逐字段映射 |

## 事件事实

终端 `Test-shifang-Win7`（192.0.2.71，Windows 7 SP1，分组 CRH）执行自定义扫描（customize_scan），扫描 2010 个文件，威胁 0、清除 0，扫描结果 result=4，引擎 qce/qowl/qde/qre，耗时 17 秒。原始日志无检出（病毒字段为空），无用户操作/进程执行证据。

## 主体 / 客体 / 载体

- 主体：无主动行为主体（扫描为引擎任务，日志未提供触发进程/用户动作）；`roles.source.host` 是扫描发生的承载终端（观测位置）
- 客体：无特定客体（扫描范围为终端本地，无独立实体）→ `roles.target=null`
- 载体：无进程载体 → `carriers=[]`

## 关键映射决策

- `event_category=other`：扫描任务执行，不是来源告警。
- `event_type=scan_host`（扫描主机）。
- `operation=completed`：PDF §3.2.2 `result=4` = 扫描完成。
- `outcome=observed`：完成态已在 operation，不升 success。
- 扫描统计（scanned_files_count/threatens_count/killings_count）与引擎/触发方式无标准路径，入 source_private。
- `source_finding_obj=null`：扫描执行记录非检测告警，无告警声明。
- 事件时间 `occur_time` = start_time（WPL 纳秒→毫秒）。
- `source_original_event_id` = guid（标准 GUID，WPL 已抽）。
- 终端资产：`roles.source.host`（name/ip/mac）+ `profiles.endpoint_asset`（agent/fingerprint/ownership）。
- `asset_id` 规则未抽，由平台上下文补齐（见 wpl-missing-fields）。

## 舍弃字段

| 字段 | 原因 |
|---|---|
| `virus_name`/`virus_type`/`file_path`/`md5`/`sha1`/`file_alarm_time`/`file_create_time` | 无检出空值 |
| `os` 版本/内存/网卡等画像字段 | 资产画像元数据，无检索价值 |
| `create_time`/`update_time` | 客户端登记/更新时间，非事件时间 |
| `login_account` | 终端登录账户，资产上下文，无独立用户主体动作 |

## 未决问题

1. `result=4` 已由 Syslog V1.11 §3.2.2 确认为扫描完成；写入 `operation=completed`，不升 `outcome=success`。
2. `trigger_mode`（0）含义待确认（0=手动触发?）。
3. 06 无 `scan_type` 路径，自定义扫描类型暂存 source_private；建议后续扩展扫描类型字典。

## 当前物理注册表迁移

本目录 expected 已迁移到当前 87 字段物理注册表。原始日志与映射身份未丢失：原文保存在 `*.raw-log.json`，expected 与 raw_log 的关联统一用 `event_id`，mapping 身份保存在对应映射 JSON/Markdown。
