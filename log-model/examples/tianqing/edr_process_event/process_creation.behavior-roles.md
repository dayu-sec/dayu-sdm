# edr_process_event / process_creation 行为信封角色判定

句式：父进程 `svchost.exe`（pid 844）在主机 `DESKTOP-NU779RJ` 上创建 `WmiPrvSE.exe`（pid 16124）；天擎只记录，无检测断言。

| 角色 | 判定 | 证据 |
|---|---|---|
| subject | `process` `svchost.exe` / guid `d22b3fbc…` | raw/WPL `process_parent_*`。旧 expected 把 source 标成 `host` 且并列 `host+process`，违反「只能选一」；父进程才是创建者 |
| object | `process` `WmiPrvSE.exe` / guid `c943cfef…` | raw `process_name` / `process_guid` / `process_id` |
| carriers[] | 空 | 进程创建载体可省略（字段目录 / examples-contract）。父进程已是 subject，不按 `parent_process` 重复。`execution_host` 仍是 `m3_review`，本条不冻结 |
| 执行环境 | 终端进 `extensions.profiles.endpoint_asset.host` | `computer_name` / `ip` / `mac` / `asset_id`。不是主体、不是载体 |
| ancestry | 祖父 `services.exe` → `facets.process.ancestry[]` | raw `process_pparent_*`；`related_routing.grandparent_process` |
| observer | `application` `tianqing` | 检测产品。`collector-tianqing-poc-01` 是采集器 → `meta.data_source.instance_id`，不进 observer |
| observation | `action=record`，无 assertion | `source_finding_obj=null`；审计记录不是 finding |

## 迁移裁决（相对旧物理 expected）

- `behavior.layer=system` / `type=appear` / `operation=spawn` / `outcome=observed`：无成败证据，不升 success。
- 顶层 `severity=info` 删除。本条无 PRI、无检测严重度。
- `occur_time` 由 Unix 毫秒 `1734489737220` 转为 `2024-12-18T02:42:17.220Z`。
- `log_id` 用来源稳定测试值，不与 `event_id` 同源派生；来源 `uuid` 进 `source_private.original_event_id`。
- 进程 `uid`→`guid`，`cmdline`→`command_line`。typed object 只留登记字段；SID、会话、完整性、工作目录进 `source_private`。
- 命令行空格、用户名空格：WPL 已分词（raw 无空格）。信封用 WPL 值。
- MAC：WPL `00-00-5E-00-53-79` → 信封 `00:00:5E:00:53:23`（冒号、小写）。
- `process_create_time`：raw `1734489800704` vs WPL `1734489700704` 冲突，且非登记字段，不写入。
- `mapping_id=tianqing.edr_process_event.process_creation.behavior.v1`。

旧 `process_creation.expected-sdm-event.json` 保持 interim 物理形，M4 再切投影。
