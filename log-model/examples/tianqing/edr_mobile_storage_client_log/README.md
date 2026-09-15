# `edr_mobile_storage_client_log` 样例（移动存储客户端日志）

本目录用于编写和验收天擎 `edr_mobile_storage_client_log`（移动存储设备管控）日志的 OML 与 SDM2.0 映射。

| 文件 | 用途 |
|---|---|
| `usb_storage_connect.raw-log.json` | 天擎真实原始日志（sample.dat:56） |
| `usb_storage_connect.wpl-output.json` | 按 parse.wpl `edr_mobile_storage_client_log` 规则抽取的 WPL 输出（45 字段） |
| `usb_storage_connect.platform-context.json` | 平台上下文 |
| `usb_storage_connect.wpl-missing-fields.json` | WPL/来源缺口声明（事件 ID 缺失） |
| `usb_storage_connect.expected-sdm-event.json` | 期望 SDM 事件 |
| `usb_storage_connect.wpl-to-sdm-event.{json,md}` | 逐字段映射 |

## 事件事实

终端 `DESKTOP-EX09`（Windows 11）接入 sony USB 存储设备（device_id=180E2001555223、vid=054C/pid=0B6F、容量 7161MB、登记名 ic_recorder），记录类型 log_report_type=1、usb_type=1。原始日志没有用户动作、进程或网络行为证据；设备接入/拔出语义由 usb_type/log_report_type 表达（枚举待确认）。

## 主体 / 客体 / 载体

- 主体：终端主机（接入动作的承载方）→ `roles.source.host`
- 客体：USB 存储设备 → `roles.target.resource`（type=usb_storage_device，id=device_id，name=登记名）
- 载体：无（设备接入无进程/会话载体，不虚构）

## 关键映射决策

- `record_kind=activity`（设备操作记录，非检测告警）、`event_domain=endpoint`（06 推荐值：终端活动）；`event_type=generic_event`（#28）兜底——**06 枚举暂无 USB/移动存储事件类型**，未决问题见下。
- 设备属性（supplier/vid/pid/capacity/usb_type/usb_status/外带管控位）无标准模型路径，入 `source_private`。
- `source_finding_obj=null`：本日志是设备操作活动，无检测结论，不构造告警声明。
- `outcome=observed`：result（0）枚举含义未确认，不擅自映射成功/失败。
- 事件时间 `occur_time` = create_time（WPL 秒→毫秒）；operation_time 与 create_time 同秒，不重复。
- `source_original_event_id` = eid（设备标识兜底）——**原始日志无事件 ID**，见 wpl-missing-fields.json 与未决问题。注意：同一设备多条事件将产生相同 eid，跨事件去重需依赖 occur_time+asset_id 组合；采集层须为每条事件补充事件 ID。
- 终端资产：`roles.source.host`（name/ip/mac）+ `profiles.endpoint_asset`（agent.id=client_id、fingerprint_id=client_mid、ownership=asset_oid/分组）。
- 客户端资产画像元数据（OS 版本/登录账户/在线时间等）无检索价值，不落库。

## 舍弃字段

| 字段 | 原因 |
|---|---|
| `client_report_ip` | 上报链路地址，非事件 IP |
| `operation_time` | 与 create_time 同秒，事件时间已表达 |
| `src_log_type`/`syslog_topic` | WPL 路由标识，log_type 已表达 |
| `collect_time` | 采集侧时间，非事件时间 |
| `client_type`/`client_os_version_*`/`client_login_account`/`last_time` | 资产画像元数据，无检索价值 |
| `detail`/`label_name`/`server_id`/`user_name`/`user_number`/`source`/`destination`/`number` | 空值 |

## 未决问题

1. 06 枚举无 USB/移动存储事件类型，暂用 generic_event（#28）；建议后续扩展 `usb_storage_access` 或类似类型。
2. `usb_type`（1）、`usb_status`（0）、`log_report_type`（1）、`result`（0）枚举含义待天擎字典确认。
3. `roles.target.resource.type="usb_storage_device"` 为样例自定受控值，待 registry 确认或扩展资源类型字典。
4. 原始日志无事件 ID，source_original_event_id 暂用 eid 兜底；建议采集层补事件 ID（影响跨事件去重）。

## 当前物理注册表迁移

本目录 expected 已迁移到当前 87 字段物理注册表。原始日志与映射身份未丢失：原文保存在 `*.raw-log.json`，expected 与 raw_log 的关联统一用 `event_id`，mapping 身份保存在对应映射 JSON/Markdown。
