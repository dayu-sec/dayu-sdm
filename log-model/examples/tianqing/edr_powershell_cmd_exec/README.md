# `edr_powershell_cmd_exec` 样例

本目录保存天擎 PowerShell 命令执行日志的真实原始样例、现有 WPL 实际输出、测试平台上下文和预期 SDM2.0 事件。

| 文件 | 用途 |
|---|---|
| `powershell_execute.raw-log.json` | 天擎 `sample.dat` 第 52 条完整原始日志 |
| `powershell_execute.wpl-output.json` | 现有 WPL 经 `wpl-check` 验证后的 45 个输出字段 |
| `powershell_execute.platform-context.json` | 测试夹具提供的平台治理字段 |
| `powershell_execute.expected-sdm-event.json` | 预期的 `sdm_event` 物理行 |
| `powershell_execute.wpl-to-sdm-event.json` | WPL 字段到 SDM 事件的机器可读映射 |
| `powershell_execute.wpl-to-sdm-event.md` | WPL 字段映射中文审查文档 |
| `wpl-missing-fields.md` | 当前样例和 WPL 的字段缺口 |

## 主体、客体和载体

- 主体：受管终端 `DESKTOP-NU779RJ` 上的 `NT AUTHORITY\SYSTEM` 用户。
- 客体：当前日志没有证明脚本作用于某个文件、进程、注册表项或网络端点，因此 `roles.target` 为空。
- 载体：已存在的 `powershell.exe` 进程和其中执行的 PowerShell 脚本。
- 关联对象：启动 PowerShell 的父进程 `CompatTelRunner.exe`。

`powershell_create_time` 早于事件时间约 63 秒，所以这不是进程创建事件。当前受控事件类型没有脚本执行类型，暂用 `generic_event`；不得错误映射为 `process_launch`。

## 当前物理注册表迁移

本目录 expected 已迁移到当前 87 字段物理注册表。原始日志与映射身份未丢失：原文保存在 `*.raw-log.json`，expected 与 raw_log 的关联统一用 `event_id`，mapping 身份保存在对应映射 JSON/Markdown。
