# `edr_energy_manage_log` 样例（天擎能耗管理日志）

本目录用于编写和验收天擎 `edr_energy_manage_log` 日志的 OML 与 SDM2.0 映射。

| 文件 | 用途 |
|---|---|
| `power_off_reminder.raw-log.json` | 天擎真实原始日志 |
| `power_off_reminder.wpl-output.json` | WPL 输出 |
| `power_off_reminder.wpl-missing-fields.json` | 规则缺口与故意不抽字段 |
| `power_off_reminder.platform-context.json` | 平台上下文 |
| `power_off_reminder.expected-sdm-event.json` | 期望 SDM 事件 |
| `power_off_reminder.wpl-to-sdm-event.{json,md}` | 逐字段映射 |

## 事件事实

能耗管理告警：终端超过 264 小时未关机，执行处置措施「仅提示」；告警类别 alarm_category=1、类型 alarm_type=1。

## 主体 / 客体 / 载体

- 主体：无主动行为主体；终端资产入 profiles
- 客体：超过阈值未关机的终端 `DESKTOP-3162Q7H` → `roles.target.host`
- 载体：无进程载体 → `carriers=[]`

## 关键映射决策

- `event_category=alert`、`record_kind=finding`：能耗策略告警。`event_domain=system` 仅表示系统能耗域，不是 `event_category=system`。
- `event_type=generic_event`（#28）：06 无能耗管理类型。
- 告警内容（content）入 source_finding.title + source_private。
- `source_original_event_id` 无 uuid，派生组合兜底。

## 未决问题

1. 06 枚举无能耗管理类型，保持 generic_event
2. PDF 有 `action`/`handle`/`result`/`level`，本条样本均无
3. 原始日志无事件 ID，派生组合兜底

## 当前物理注册表迁移

本目录 expected 已迁移到当前 87 字段物理注册表。原始日志与映射身份未丢失：原文保存在 `*.raw-log.json`，expected 与 raw_log 的关联统一用 `event_id`，mapping 身份保存在对应映射 JSON/Markdown。
