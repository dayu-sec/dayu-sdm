# `edr_ssid_log` 样例（天擎 SSID 无线日志）

本目录用于编写和验收天擎 `edr_ssid_log` 日志的 OML 与 SDM2.0 映射。

| 文件 | 用途 |
|---|---|
| `ssid_test_protect.raw-log.json` | 天擎真实原始日志 |
| `ssid_test_protect.wpl-output.json` | WPL 输出 |
| `ssid_test_protect.wpl-missing-fields.json` | 规则缺口与故意不抽字段 |
| `ssid_test_protect.platform-context.json` | 平台上下文 |
| `ssid_test_protect.expected-sdm-event.json` | 期望 SDM 事件 |
| `ssid_test_protect.wpl-to-sdm-event.{json,md}` | 逐字段映射 |

## 事件事实

终端（无线 MAC 00-00-5E-00-53-56）无线网络管控：SSID「test」，保护类型 protect_type=1，结果 result=1，日志类型 log_type=1。

## 主体 / 客体 / 载体

- 主体：执行 SSID 管控的终端 `DESKTOP-3162Q7H` → `roles.source.host`；资产画像继续通过 profiles 关联
- 客体：SSID 无线网络「test」→ `roles.target.resource{type: ssid_network}`（受控值未确认）
- 载体：无进程载体 → `carriers=[]`

## 关键映射决策

- `record_kind=activity`、`event_domain=network`：无线接入管控活动记录。
- `event_type=generic_event`（#28）兜底：06 枚举无 SSID/无线类型。
- `resource.type=ssid_network` 为样例自定受控值，待 registry 确认（未决 2）。
- `source_original_event_id` 无 uuid，派生组合兜底。

## 未决问题

1. 06 枚举无 SSID/无线网络事件类型，暂用 generic_event；建议扩展
2. resource.type=ssid_network 待 registry 确认
3. log_type/protect_type/result 枚举待确认
4. 原始日志无事件 ID，派生组合兜底

## 当前物理注册表迁移

本目录 expected 已迁移到当前 87 字段物理注册表。原始日志与映射身份未丢失：原文保存在 `*.raw-log.json`，expected 与 raw_log 的关联统一用 `event_id`，mapping 身份保存在对应映射 JSON/Markdown。
