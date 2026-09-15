# `edr_remote_assistance_log` 样例（天擎远程协助日志）

本目录用于编写和验收天擎 `edr_remote_assistance_log` 日志的 OML 与 SDM2.0 映射。

| 文件 | 用途 |
|---|---|
| `admin_remote_help.raw-log.json` | 天擎真实原始日志 |
| `admin_remote_help.wpl-output.json` | WPL 输出 |
| `admin_remote_help.wpl-missing-fields.json` | 规则缺口与故意不抽字段 |
| `admin_remote_help.platform-context.json` | 平台上下文 |
| `admin_remote_help.expected-sdm-event.json` | 期望 SDM 事件 |
| `admin_remote_help.wpl-to-sdm-event.{json,md}` | 逐字段映射 |

## 事件事实

管理员 admin 对终端发起远程协助：发起方 remote_initiator=0、原因 ceshi、结果 remote_result=1、时长 51 秒、终端确认 terminal_confirm=1。

## 主体 / 客体 / 载体

- 主体：协助管理员 `admin` → `roles.source.user`（admin_name，规则未抽）
- 客体：被协助终端 `WIN-EX01` → `roles.target.host`；资产画像继续通过 profiles 关联
- 载体：无进程载体 → `carriers=[]`

## 关键映射决策

- `record_kind=activity`、`event_domain=system`：远程协助为运维活动记录。
- `event_type=generic_event`（#28）兜底：06 枚举无远程协助类型。
- 会话详情（reason/result/time/confirm/initiator）入 source_private。
- `source_original_event_id` = params_id（会话参数 ID，唯一）。

## 未决问题

1. 06 枚举无远程协助事件类型，暂用 generic_event；建议扩展
2. remote_initiator/remote_result/terminal_confirm 枚举待确认
3. 受协助终端与 admin 的关系（admin 是否本域用户）待确认

## 当前物理注册表迁移

本目录 expected 已迁移到当前 87 字段物理注册表。原始日志与映射身份未丢失：原文保存在 `*.raw-log.json`，expected 与 raw_log 的关联统一用 `event_id`，mapping 身份保存在对应映射 JSON/Markdown。
