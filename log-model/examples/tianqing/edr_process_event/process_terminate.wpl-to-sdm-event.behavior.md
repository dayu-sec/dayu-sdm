# process_terminate 行为信封映射

样例：`process_terminate.expected-sdm-event.behavior.json`  
`mapping_id=tianqing.edr_process_event.process_terminate.behavior.v1`  
旧物理 mapping 保留。

## 相对旧 mapping 的关键纠正

| 来源 | 旧落位 | 新落位 |
|---|---|---|
| 终止者 | `roles.source=host` | `subject=null`（父进程不是终止者） |
| `process_*`（conhost） | `roles.target.process` | `object.process`；`uid`→`guid` |
| `process_parent_*` / `process_pparent_*` | `roles.related[]` | `facets.process.ancestry[]`；`ref_id` 统一 `process::`；父 `pid` 进 `ancestry[0]` |
| `ip` / `mac` / `computer_name` | `roles.source.host` | `profiles.endpoint_asset.host`；`carriers=[]` |
| `report_ip` / `client_report_ip` | 与 host.ip 混用 | `source_private.report_ip`（`203.0.113.45` ≠ `192.0.2.206`） |
| `uuid` | `source_original_event_id` | `source_private.original_event_id` |
| `severity=info` | 顶层 | 删除 |
| `outcome` | `observed` | 保持 `observed`；`type=disappear` / `operation=terminate` |

`event_kind=behavior`，`record_kind=activity`，`action=record`，无 assertion。  
raw/WPL 冲突（时间、主机名）跟 WPL。`execution_host` 仍 `m3_review`。

校验：`logical_schema=passed`，`semantic_review=passed`；物理投影 `not_run`。
