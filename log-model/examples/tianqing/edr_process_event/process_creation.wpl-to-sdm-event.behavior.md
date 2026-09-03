# process_creation 行为信封映射

样例：`process_creation.expected-sdm-event.behavior.json`  
`mapping_id=tianqing.edr_process_event.process_creation.behavior.v1`  
旧物理 mapping 保留。

## 相对旧 mapping 的关键纠正

| 来源 | 旧落位 | 新落位 |
|---|---|---|
| `process_parent_*` | `roles.source.process`（且 source 还挂了 host） | `subject.process` 单类型 |
| `process_*`（子进程） | `roles.target.process` | `object.process`；`uid`→`guid`，`cmdline`→`command_line` |
| `process_pparent_*` | `roles.related[]` | `facets.process.ancestry[]` |
| `ip` / `mac` / `computer_name` | `roles.source.host` | `profiles.endpoint_asset.host`；`carriers=[]` |
| `mac` | 旧 mapping 不落库 | 归一为 `00:00:5E:00:53:23` |
| `uuid` | `source_original_event_id` | `source_private.original_event_id` |
| `process_create_time` | `created_time` | 丢弃（raw/WPL 冲突，非登记字段） |
| 签名/版本/OriginalFilename | `process.file.*` | 丢弃（非登记字段） |
| `severity=info` | 顶层 | 删除（无 PRI、无检测） |
| `data_src_instance_id` | 与 observer 混用 | 只进 `meta.data_source.instance_id` |

`event_kind=behavior`，`record_kind=activity`，`action=record`，无 assertion。  
`execution_host` 仍 `m3_review`，本条不冻结。

校验：`logical_schema=passed`，`semantic_review=passed`；物理投影 `not_run`。
