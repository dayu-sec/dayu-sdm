# `edr_external_device_alarm` 样例（天擎外部设备告警日志）

本目录用于编写和验收天擎 `edr_external_device_alarm` 日志的 OML 与 SDM2.0 映射。

| 文件 | 用途 |
|---|---|
| `usb_reader_alert.raw-log.json` | 天擎真实原始日志 |
| `usb_reader_alert.wpl-output.json` | WPL 输出 |
| `usb_reader_alert.wpl-missing-fields.json` | 规则缺口与故意不抽字段 |
| `usb_reader_alert.platform-context.json` | 平台上下文 |
| `usb_reader_alert.expected-sdm-event.json` | 期望 SDM 事件 |
| `usb_reader_alert.wpl-to-sdm-event.{json,md}` | 逐字段映射 |

## 事件事实

外部设备告警：USB 读卡器 MULTIFLASHREADERUSBDEVICE（VID_413C&PID_8197）接入，命中管控规则 test，结果 result=1，告警类型 alarm_type=1。

## 主体 / 客体 / 载体

- 主体：无主动行为主体 → `roles.source=null`
- 客体：接入外设的终端 `DESKTOP-EX03` → `roles.target.host`；USB 读卡器 → `roles.related.device{relation_type: connected_peripheral}`
- 载体：无进程载体 → `carriers=[]`

## 关键映射决策

- `event_category=alert`、`record_kind=finding`、`event_domain=endpoint`：外设管控告警。
- `event_type=generic_event`（#28）：06 无此外设类型；逻辑 fixture 的 `external_device_alarm` 不写入物理 `event_type`。
- 命中管控规则 → `source_finding.rule.label`。
- `source_original_event_id` = guid（设备类 GUID，非事件 ID，兜底）。

## 未决问题

1. 06 枚举无外部设备告警类型，保持 generic_event
2. guid 为设备类 GUID 非事件 ID，多条告警会共享
3. `outcome=allowed`：PDF §3.6.5 `result=1` 放行
4. `device.type=usb_device` 相对官方 fixture `usb_storage` 更贴近读卡器，待对象类型表确认

## 当前物理注册表迁移

本目录 expected 已迁移到当前 87 字段物理注册表。原始日志与映射身份未丢失：原文保存在 `*.raw-log.json`，expected 与 raw_log 的关联统一用 `event_id`，mapping 身份保存在对应映射 JSON/Markdown。
