# `edr_system_protection` 样例（天擎系统防护日志）

本目录用于编写和验收天擎 `edr_system_protection` 日志的 OML 与 SDM2.0 映射。

| 文件 | 用途 |
|---|---|
| `iexplore_cc_ip_block.raw-log.json` | 天擎真实原始日志 |
| `iexplore_cc_ip_block.wpl-output.json` | WPL 输出 |
| `iexplore_cc_ip_block.wpl-missing-fields.json` | 规则缺口与故意不抽字段 |
| `iexplore_cc_ip_block.platform-context.json` | 平台上下文 |
| `iexplore_cc_ip_block.expected-sdm-event.json` | 期望 SDM 事件 |
| `iexplore_cc_ip_block.wpl-to-sdm-event.{json,md}` | 逐字段映射 |

## 事件事实

终端 `Test-shifang-Win7` 上系统防护拦截 `iexplore.exe` 对风险 IP 198.51.100.67（DriveTheLife CC）的访问，防护动作 defend_action=1，事件计数 3，触发方式 trigger_mode=5。

## 主体 / 客体 / 载体

- 主体：`iexplore.exe` → `roles.source.process`（subject_process 含路径，规则未抽，raw_log 补齐）
- 客体：风险 IP `198.51.100.67` → `roles.target.endpoint`（object 字段，规则未抽）
- 载体：无进程载体 → `carriers=[]`

## 关键映射决策

- `record_kind=finding`、`event_domain=threat`：系统防护拦截为检测告警，结论入 `source_finding`。
- `event_type=generic_event`（#28）兜底：06 枚举无系统防护类型。
- `outcome=denied`：防护拦截语义=拒绝。
- `source_original_event_id` 无 uuid，用 `event_time_ms|subject_process` 派生组合。

## 未决问题

1. 06 枚举无系统防护事件类型，暂用 generic_event；建议扩展
2. action（21）/defend_action（1）/trigger_mode（5）枚举待确认
3. 原始日志无事件 ID，派生组合兜底

## 当前物理注册表迁移

本目录 expected 已迁移到当前 87 字段物理注册表。原始日志与映射身份未丢失：原文保存在 `*.raw-log.json`，expected 与 raw_log 的关联统一用 `event_id`，mapping 身份保存在对应映射 JSON/Markdown。
