# file_write 行为信封映射

样例：`file_write.expected-sdm-event.behavior.json`  
`mapping_id=tianqing.edr_file_op.file_write.behavior.v1`  
旧物理 mapping 保留。

## 相对旧 mapping 的关键纠正

| 来源 | 旧落位 | 新落位 |
|---|---|---|
| `process_*`（svchost.exe） | `roles.source=host` + `carriers[]` 同进程 | `subject.process` 单类型；carriers 空 |
| `file_name` / `file_path` / `file_md5` | `roles.target.file` | `object.file` |
| `process_md5` / `process_sha1` | 进程映像 | `subject.process.file.hashes`，不与 `file_md5` 混 |
| `process_parent_*` | `roles.related[]` | `facets.process.ancestry[]` |
| `ip` / `mac` / `computer_name` | `roles.source.host` | `profiles.endpoint_asset.host` |
| `severity=info` | 顶层 | 删除 |
| `file_date_creation=0` | 可能当时间 | 哨兵，丢弃 |

`event_kind=behavior`，`type=change`，`operation=write`，`action=record`。矩阵「文件读取」是另一动作。

校验：`logical_schema=passed`，`semantic_review=passed`；物理投影 `not_run`。
