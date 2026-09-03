# process_injection 行为信封映射

样例：`process_injection.expected-sdm-event.behavior.json`  
`mapping_id=tianqing.edr_process_inject.process_injection.behavior.v1`  
旧物理 mapping 保留。

## 相对旧 mapping 的关键纠正

| 来源 | 旧落位 | 新落位 |
|---|---|---|
| `process_*`（services.exe） | `roles.source` 上 host+process | `subject.process` 单类型 |
| `target_process_*` | `roles.target.process` | `object.process` |
| `target_thread_*` | `facets.process.injection` | 保持 facet，不升实体 |
| `process_parent_*` | `roles.related[]` | `facets.process.ancestry[]` |
| `ip` / `mac` / `computer_name` | `roles.source.host` | `profiles.endpoint_asset.host` |
| `report_ip` | 与 host.ip 混用 | `source_private`（`203.0.113.45` ≠ `192.0.2.206`） |
| `operation=remote_thread` | 顶层 operation | `behavior.operation=inject`；方法进 `injection.method` |
| `severity=info` | 顶层 | 删除 |

`event_kind=behavior`，`type=change`，`action=record`，无 assertion。

校验：`logical_schema=passed`，`semantic_review=passed`；物理投影 `not_run`。
