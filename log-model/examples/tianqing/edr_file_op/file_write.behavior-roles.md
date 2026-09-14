# edr_file_op / file_write 行为信封角色判定

句式：进程 `svchost.exe`（pid 1680）写入文件 `Scheduled Start`；天擎只记录，无检测断言。

矩阵「文件读取」是 `file / read`。本条是 `file_write` → `change / write`，客体仍是 file。

| 角色 | 判定 | 证据 |
|---|---|---|
| subject | `process` `svchost.exe` / guid `ae64b7b3…` | 写入进程。旧 expected 把 source 标成 host，进程进 carriers（与主体同对象重复） |
| object | `file` `Scheduled Start` | `file_name` / `file_path` / `file_md5`。`file_md5` 属于客体文件，不是进程映像 |
| carriers[] | 空 | 写入进程已是 subject，不按 carrier 再挂一份。`execution_host` 仍 `m3_review` |
| ancestry | 父 `services.exe` → `facets.process.ancestry[]` | `process_parent_*`；`ref_id` 与 DNS 审计同一路径哈希 `process::75215cee…` |
| observer | `application` `tianqing` | 采集器 → `meta.data_source.instance_id` |
| observation | `action=record`，无 assertion | `source_finding_obj=null` |

## 迁移裁决（相对旧物理 expected）

- `behavior.layer=system` / `type=change` / `operation=write` / `outcome=observed`。
- 顶层 `severity=info` 删除。
- `occur_time` `1734489580781` → `2024-12-18T02:39:40.781Z`。
- `file_date_creation=0`、`file_previous_date_creation=0` 哨兵，不写文件时间。
- 空重命名字段、`removable_device=0` 丢弃。
- `create_time` 量级异常（非毫秒），丢弃。
- `report_ip` 与 `ip` 同值，不进 `source_private`。
- MAC：`00-50-56-81-E8-1C` → `00:50:56:81:e8:1c`。
- `mapping_id=tianqing.edr_file_op.file_write.behavior.v1`。

旧 `file_write.expected-sdm-event.json` 保持 interim 物理形，M4 再切投影。
