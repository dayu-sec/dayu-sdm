# edr_process_event / process_terminate 行为信封角色判定

句式：进程 `conhost.exe`（pid 21888）结束；日志未给出终止者。天擎只记录，无检测断言。

| 角色 | 判定 | 证据 |
|---|---|---|
| subject | `null` | 无法证明谁终止。父进程 `gpupdate.exe` 只是血缘，不是终止者。旧 expected 把 source 标成 `host`，把发生环境误当主体 |
| object | `process` `conhost.exe` / guid `3cce505ecc…` | raw/WPL `process_name` / `process_guid` / `process_id`。矩阵：客体=被终止进程 |
| carriers[] | 空 | 与创建事件相同。父进程不进载体。`execution_host` 仍 `m3_review`，本条不冻结 |
| 执行环境 | 终端进 `profiles.endpoint_asset.host` | WPL `computer_name` / `ip` / `mac` / `asset_id` |
| ancestry | 父 `gpupdate.exe`（pid 21780）+ 祖父 `svchost.exe` → `facets.process.ancestry[]` | 父不再是 subject，两条血缘都进 ancestry；`ref_id` 统一 `process::`；`related` 废除 |
| observer | `application` `tianqing` | 采集器 `collector-tianqing-poc-01` → `meta.data_source.instance_id` |
| observation | `action=record`，无 assertion | `source_finding_obj=null` |

## 迁移裁决（相对旧物理 expected）

- `behavior.layer=system` / `type=disappear` / `operation=terminate` / `outcome=observed`。
- 顶层 `severity=info` 删除。无 PRI、无检测。
- `occur_time` 用 WPL `event_date_creation=1734490003718` → `2024-12-18T02:46:43.718Z`。raw 为 `1732787221036`，冲突，信封跟 WPL。
- `computer_name`：raw `DESKTOP-NGMF7JI` vs WPL `DESKTOP-NU779RJ`，信封跟 WPL。
- `ip`/`client_ip=10.95.209.76` 进 `profiles.host.ip`；`report_ip`/`client_report_ip=172.16.12.12` 进 `source_private.report_ip`（不是同一地址，不能当别名吞掉）。
- `process_create_time`：raw `1732787214434` vs WPL `1734489800704`，非登记字段，不写。
- `log_id` 用来源稳定测试值；`uuid` → `source_private.original_event_id`。
- `uid`→`guid`，`cmdline`→`command_line`。PE 元数据（OriginalFilename/签名/版本）不进登记 process.file。
- MAC：`00-50-56-81-E3-7E` → `00:50:56:81:e3:7e`。
- `mapping_id=tianqing.edr_process_event.process_terminate.behavior.v1`。

旧 `process_terminate.expected-sdm-event.json` 保持 interim 物理形，M4 再切投影。
