# `edr_baseline_check_detail` 样例（天擎基线检查详情日志）

本目录用于编写和验收天擎 `edr_baseline_check_detail` 日志的 OML 与 SDM2.0 映射。

| 文件 | 用途 |
|---|---|
| `check_item_disabled.raw-log.json` | 天擎真实原始日志 |
| `check_item_disabled.wpl-output.json` | WPL 输出 |
| `check_item_disabled.wpl-missing-fields.json` | 规则缺口与故意不抽字段 |
| `check_item_disabled.platform-context.json` | 平台上下文 |
| `check_item_disabled.expected-sdm-event.json` | 期望 SDM 事件 |
| `check_item_disabled.wpl-to-sdm-event.{json,md}` | 逐字段映射 |

## 事件事实

基线检查项（name=1015，scope=9005）结果为「已禁用」（check_std），评分 1，拒绝 reject=0；检查任务 9546E589-…，关联用户 qinxin（秦鑫）。

## 主体 / 客体 / 载体

- 主体：无主动行为主体；关联用户 qinxin 为资产归属/操作人，入 source_private（未确认检查由用户执行）
- 客体：检查项所针对的终端 `A003076-PC01` → `roles.target.host`
- 载体：无进程载体 → `carriers=[]`

## 关键映射决策

- `event_category=system`、`record_kind=finding`、`event_domain=system`：检查项结果是系统配置核查结论，不是威胁告警。
- `event_type=generic_event`（#28）：06 无基线检查项类型。
- 检查项（scope/score/reject/check_std）入 source_private；`result=0`（不通过）不进 `outcome`/`finding.status`；check_std 语义（已禁用）入 title。
- 用户信息（qinxin/秦鑫）入 source_private（未确认为执行人）。

## 未决问题

1. 06 枚举无基线检查项类型，保持 generic_event
2. 检查项 `name=1015` 业务名未见
3. 用户 qinxin 是否为检查执行人未确认

## 当前物理注册表迁移

本目录 expected 已迁移到当前 87 字段物理注册表。原始日志与映射身份未丢失：原文保存在 `*.raw-log.json`，expected 与 raw_log 的关联统一用 `event_id`，mapping 身份保存在对应映射 JSON/Markdown。
