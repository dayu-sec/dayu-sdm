# `edr_baseline_check_result` 样例（天擎基线检查结果日志）

本目录用于编写和验收天擎 `edr_baseline_check_result` 日志的 OML 与 SDM2.0 映射。

| 文件 | 用途 |
|---|---|
| `baseline_score_90.raw-log.json` | 天擎真实原始日志 |
| `baseline_score_90.wpl-output.json` | WPL 输出 |
| `baseline_score_90.wpl-missing-fields.json` | 规则缺口与故意不抽字段 |
| `baseline_score_90.platform-context.json` | 平台上下文 |
| `baseline_score_90.expected-sdm-event.json` | 期望 SDM 事件 |
| `baseline_score_90.wpl-to-sdm-event.{json,md}` | 逐字段映射 |

## 事件事实

终端（wangyg 分组）基线检查完成：通过 17 项、失败 10 项、未修复 10 项，得分 90，等级 3，检查状态 check_status=1，结果 result=0。

## 主体 / 客体 / 载体

- 主体：无主动行为主体（检查为平台任务）；终端资产入 profiles
- 客体：被检查终端 `QAX02V` → `roles.target.host`；任务本身不是事件客体
- 载体：无进程载体 → `carriers=[]`

## 关键映射决策

- `event_category=system`、`record_kind=finding`、`event_domain=system`：主机基线核查汇总，不是威胁告警。
- `event_type=scan_host`：SR-020 批准升级——基线核查语义为主机合规扫描，与 `edr_antivirus_scan`（SR-016）同构。`operation=completed`：PDF §3.4.1 `check_status=1` 检查完成。
- 检查统计（score/pass/fail/level）无标准路径，入 source_private。
- `source_original_event_id` = task（检查任务 GUID，去花括号）；无事件级 uuid。

## 未决问题

1. ~~06 枚举无基线核查类型，保持 generic_event~~ 已由 SR-020 批准升级 scan_host
2. `result=0` 为「非按检查结果」，不进 outcome；`op=1` 策略执行不单独升类型
3. task 为任务 ID 非事件 ID，多条详情/结果事件会共享

## 当前物理注册表迁移

本目录 expected 已迁移到当前 87 字段物理注册表。原始日志与映射身份未丢失：原文保存在 `*.raw-log.json`，expected 与 raw_log 的关联统一用 `event_id`，mapping 身份保存在对应映射 JSON/Markdown。
