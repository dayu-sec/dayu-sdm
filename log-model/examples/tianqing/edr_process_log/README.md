# `edr_process_log` 样例（天擎进程管理日志）

本目录用于编写和验收天擎 `edr_process_log` 日志的 OML 与 SDM2.0 映射。

| 文件 | 用途 |
|---|---|
| `chrome_manage_rule.raw-log.json` | 天擎真实原始日志 |
| `chrome_manage_rule.wpl-output.json` | WPL 输出 |
| `chrome_manage_rule.wpl-missing-fields.json` | 规则缺口与故意不抽字段 |
| `chrome_manage_rule.platform-context.json` | 平台上下文 |
| `chrome_manage_rule.expected-sdm-event.json` | 期望 SDM 事件 |
| `chrome_manage_rule.wpl-to-sdm-event.{json,md}` | 逐字段映射 |

## 事件事实

运维用户 tianqing 对进程 chrome.exe 执行管控操作：动作 action=1、类型 type=1、权限 permission=1、管控内容 process_id=test、描述 test。

## 主体 / 客体 / 载体

- 主体：操作者 `tianqing` → `roles.source.user`（staff_name，规则未抽）
- 客体：被管控进程 `chrome.exe` → `roles.target.process`（process_name，规则未抽）
- 载体：无进程载体 → `carriers=[]`

## 关键映射决策

- `record_kind=activity`、`event_domain=endpoint`：进程管控为管理活动记录。
- `event_type=process_uncategorized`（06 #49）：进程相关但无具体动作类型。
- 管控细节（action/type/permission/content/gid/report_type）入 source_private。
- `source_original_event_id` 无 uuid，用 `create_time_ms|process_name|staff_name` 派生组合。

## 未决问题

1. action/type/permission 枚举待确认（1=添加管控?）
2. process_log 语义为管控操作而非进程执行，06 无更贴切类型
3. 原始日志无事件 ID，派生组合兜底

## 当前物理注册表迁移

本目录 expected 已迁移到当前 87 字段物理注册表。原始日志与映射身份未丢失：原文保存在 `*.raw-log.json`，expected 与 raw_log 的关联统一用 `event_id`，mapping 身份保存在对应映射 JSON/Markdown。
