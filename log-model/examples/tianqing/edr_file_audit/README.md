# `edr_file_audit` 样例

本目录保存天擎文件审计日志的真实原始样例、现有 WPL 实际输出、测试平台上下文和预期 SDM2.0 事件。

| 文件 | 用途 |
|---|---|
| `upload_to_site.raw-log.json` | 天擎 `sample.dat` 第 55 条完整原始日志 |
| `upload_to_site.wpl-output.json` | 当前 WPL 经 `wpl-check` 验证后的 228 个输出字段 |
| `upload_to_site.platform-context.json` | 测试夹具提供的平台治理字段 |
| `upload_to_site.expected-sdm-event.json` | 预期的 `sdm_event` 物理行 |
| `upload_to_site.wpl-to-sdm-event.json` | WPL 字段到 SDM 事件的机器可读映射 |
| `upload_to_site.wpl-to-sdm-event.md` | WPL 字段映射中文审查文档 |
| `wpl-missing-fields.md` | 当前样例、来源枚举和文件传输字段缺口 |

主体是受管终端上的账号 `LQQ` 和进程 `explorer.exe`，客体是上传到远端路径的文件，本地同名文件作为 `source_file` 关联对象。WPL 展开的完整资产快照不会复制进事件扩展，只提取 host 与 endpoint_asset 所需增量。

## 当前物理注册表迁移

本目录 expected 已迁移到当前 87 字段物理注册表。原始日志与映射身份未丢失：原文保存在 `*.raw-log.json`，expected 与 raw_log 的关联统一用 `event_id`，mapping 身份保存在对应映射 JSON/Markdown。
