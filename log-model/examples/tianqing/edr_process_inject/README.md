# `edr_process_inject` 样例

本目录保存天擎进程注入日志的真实原始样例、现有 WPL 实际输出、测试平台上下文和预期 SDM2.0 事件。

| 文件 | 用途 |
|---|---|
| `process_injection.raw-log.json` | 天擎 `sample.dat` 第 42 条完整原始日志 |
| `process_injection.wpl-output.json` | 当前 WPL 经 `wpl-check` 验证后的 46 个输出字段 |
| `process_injection.platform-context.json` | 测试夹具提供的平台治理字段 |
| `process_injection.expected-sdm-event.json` | 预期的 `sdm_event` 物理行 |
| `process_injection.wpl-to-sdm-event.json` | WPL 字段到 SDM 事件的机器可读映射 |
| `process_injection.wpl-to-sdm-event.md` | WPL 字段映射中文审查文档 |
| `wpl-missing-fields.md` | 当前样例、注入方式和结果字段缺口 |

主体是受管终端上的 `services.exe`，客体是被注入的 `TrustedInstaller.exe`，`wininit.exe` 是主体进程的父进程。目标线程信息属于进程注入维度，不重复构造成进程实体。

## 当前物理注册表迁移

本目录 expected 已迁移到当前 87 字段物理注册表。原始日志与映射身份未丢失：原文保存在 `*.raw-log.json`，expected 与 raw_log 的关联统一用 `event_id`，mapping 身份保存在对应映射 JSON/Markdown。
