# `edr_reg_change` 样例

本目录保存天擎注册表值变更日志的真实原始样例、现有 WPL 实际输出、测试平台上下文和预期 SDM2.0 事件。

| 文件 | 用途 |
|---|---|
| `registry_set_value.raw-log.json` | 天擎 `sample.dat` 第 44 条完整原始日志 |
| `registry_set_value.wpl-output.json` | 当前 WPL 经 `wpl-check` 验证后的 43 个输出字段 |
| `registry_set_value.platform-context.json` | 测试夹具提供的平台治理字段 |
| `registry_set_value.expected-sdm-event.json` | 预期的 `sdm_event` 物理行 |
| `registry_set_value.wpl-to-sdm-event.json` | WPL 字段到 SDM 事件的机器可读映射 |
| `registry_set_value.wpl-to-sdm-event.md` | WPL 字段映射中文审查文档 |
| `wpl-missing-fields.md` | 当前样例、动作枚举和结果字段缺口 |

主体是受管终端上的 `services.exe`，客体是 `wuauserv` 注册表键下的 `Start` 值。注册表键值细节位于 `facets.registry`，不放入天擎私有扩展。

## 当前物理注册表迁移

本目录 expected 已迁移到当前 87 字段物理注册表。原始日志与映射身份未丢失：原文保存在 `*.raw-log.json`，expected 与 raw_log 的关联统一用 `event_id`，mapping 身份保存在对应映射 JSON/Markdown。
