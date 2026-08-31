# `edr_webpage_protection` 样例（天擎网页防护日志）

本目录用于编写和验收天擎 `edr_webpage_protection` 日志的 OML 与 SDM2.0 映射。

| 文件 | 用途 |
|---|---|
| `jsssh_webpage_block.raw-log.json` | 天擎真实原始日志 |
| `jsssh_webpage_block.wpl-output.json` | WPL 输出 |
| `jsssh_webpage_block.wpl-missing-fields.json` | 规则缺口与故意不抽字段 |
| `jsssh_webpage_block.platform-context.json` | 平台上下文 |
| `jsssh_webpage_block.expected-sdm-event.json` | 期望 SDM 事件 |
| `jsssh_webpage_block.wpl-to-sdm-event.{json,md}` | 逐字段映射 |

## 事件事实

终端 `Test-shifang-Win7` 访问网页 `jsssh.cn`（192.0.2.246）被网页防护处理，防护动作 protect_action=0（含义待确认）。

## 主体 / 客体 / 载体

- 主体：访问终端 `Test-shifang-Win7` → `roles.source.host`；资产画像继续通过 profiles 关联
- 客体：访问域名 `jsssh.cn` → `roles.target.domain`（visit_domain，规则未抽）
- 载体：无进程载体 → `carriers=[]`

## 关键映射决策

- `record_kind=finding`、`event_domain=network`：网页防护为检测结论，入 `source_finding`。
- `event_type=network_http`（06 #40）：访问网页语义。
- `outcome=observed`：protect_action=0 含义未确认，不擅自映射拦截/放行。
- `visit_ip` 无 domain 挂载路径，入 source_private。

## 未决问题

1. protect_action（0）/protect_details（0）枚举待确认
2. 06 的 network_http 是否适合承载网页防护拦截动作待评估
3. 原始日志无事件 ID，派生组合兜底

## 当前物理注册表迁移

本目录 expected 已迁移到当前 87 字段物理注册表。原始日志与映射身份未丢失：原文保存在 `*.raw-log.json`，expected 与 raw_log 的关联统一用 `event_id`，mapping 身份保存在对应映射 JSON/Markdown。
