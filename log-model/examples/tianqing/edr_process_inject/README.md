# `edr_process_inject` 样例

本目录保存天擎进程注入日志的真实原始样例、现有 WPL 实际输出、测试平台上下文和预期 SDM2.0 事件。

| 文件 | 用途 |
|---|---|
| `process_injection.raw-log.json` | 天擎 `sample.dat` 第 42 条完整原始日志 |
| `process_injection.wpl-output.json` | 当前 WPL 经 `wpl-check` 验证后的 46 个输出字段 |
| `process_injection.platform-context.json` | 测试夹具提供的平台治理字段 |
| `process_injection.expected-sdm-event.json` | interim 物理五层/投影形（M4 前保留） |
| `process_injection.expected-sdm-event.behavior.json` | M3 行为信封（07 Schema）；见 `process_injection.behavior-roles.md` |
| `process_injection.behavior-roles.md` | 四角色与 pending 列裁决 |
| `process_injection.wpl-to-sdm-event.json` | WPL 字段到 SDM 事件的机器可读映射（interim） |
| `process_injection.wpl-to-sdm-event.md` | WPL 字段映射中文审查文档（interim） |
| `process_injection.wpl-to-sdm-event.behavior.json` | M3 行为信封字段映射 |
| `process_injection.wpl-to-sdm-event.behavior.md` | 映射评审表 |
| `wpl-missing-fields.md` | 当前样例、注入方式和结果字段缺口 |

约定（interim 物理仍按下述旧角色；行为信封以 `process_injection.behavior-roles.md` 为准）：

主体是受管终端上的 `services.exe`，客体是被注入的 `TrustedInstaller.exe`，`wininit.exe` 是主体进程的父进程。目标线程信息属于进程注入维度，不重复构造成进程实体。

## process_injection 行为信封（M3）

- 主体：注入进程 `services.exe`（不是 host；旧 expected 的 host+process 双类型作废）
- 客体：被注入进程 `TrustedInstaller.exe`
- 载体：空。`execution_host` 仍 `m3_review`
- 线程：`facets.process.injection.target_thread`，不升实体
- `type=change` / `operation=inject` / `outcome=observed`
- `mapping_id=tianqing.edr_process_inject.process_injection.behavior.v1`

## 当前物理注册表迁移

本目录 expected 已迁移到当前 87 字段物理注册表。原始日志与映射身份未丢失：原文保存在 `*.raw-log.json`，expected 与 raw_log 的关联统一用 `event_id`，mapping 身份保存在对应映射 JSON/Markdown。
