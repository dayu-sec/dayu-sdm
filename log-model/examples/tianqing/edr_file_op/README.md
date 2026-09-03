# `edr_file_op` 样例

本目录用于编写和验收天擎 `edr_file_op` 的 OML。当前只实现已有真实样例支持的 `file_write` 分支。

| 文件 | 用途 |
|---|---|
| `file_write.raw-log.json` | 天擎真实原始日志（wpl 抽取源，sample.dat） |
| `file_write.wpl-output.json` | WPL 已抽取的文件写入字段 |
| `file_write.platform-context.json` | 测试夹具提供的平台上下文 |
| `file_write.expected-sdm-event.json` | interim 物理五层/投影形（M4 前保留） |
| `file_write.expected-sdm-event.behavior.json` | M3 行为信封（07 Schema）；见 `file_write.behavior-roles.md` |
| `file_write.behavior-roles.md` | 四角色与 pending 列裁决 |
| `file_write.wpl-to-sdm-event.behavior.json` | M3 行为信封字段映射 |
| `file_write.wpl-to-sdm-event.behavior.md` | 映射评审表 |

约定（interim 物理仍按下述旧角色；行为信封以 `file_write.behavior-roles.md` 为准）：

- `event_date_creation` 是事件发生时间，`timestamp` 是天擎上报时间。
- `file_write` 映射为 `event_type=file_modification`、`operation=write`（06 枚举目录 file_modification 支持 `checkin`、`write`）。
- 受管终端进入 `roles.source.host`，执行写入的当前进程进入 `roles.source.process`，被写入文件进入 `roles.target.file`，父进程进入 `roles.related[]`；载体为执行写入的当前进程（svchost.exe，与主体进程同对象，`roles.carriers` 复用该进程引用）。
- `file_md5` 属于目标文件；`process_md5/process_sha1` 属于主体进程映像文件。
- `file_date_creation=0`、`file_previous_date_creation=0` 是哨兵值，不生成文件时间。
- 空的重命名字段不生成关联文件；`removable_device=0` 不生成可移动设备对象。
- `task_id`、`sub_task_id`、`logger`、原始 `type`、空 `custom_group_paths` 和完整 `payload` 不落库。

## file_write 行为信封（M3）

- 主体：写入进程 `svchost.exe`（不是 host；不把同一进程再挂 carriers）
- 客体：`file` `Scheduled Start`
- 载体：空。`execution_host` 仍 `m3_review`
- `type=change` / `operation=write` / `outcome=observed`
- `mapping_id=tianqing.edr_file_op.file_write.behavior.v1`

## 当前物理注册表迁移

本目录 expected 已迁移到当前 87 字段物理注册表。原始日志与映射身份未丢失：原文保存在 `*.raw-log.json`，expected 与 raw_log 的关联统一用 `event_id`，mapping 身份保存在对应映射 JSON/Markdown。
