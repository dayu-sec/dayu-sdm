# outbound_open 行为信封映射

样例：`outbound_open.expected-sdm-event.behavior.json`  
`mapping_id=tianqing.edr_ip_access.outbound_open.behavior.v1`  
旧物理 mapping 保留。

## 相对旧 mapping 的关键纠正

| 来源 | 旧落位 | 新落位 |
|---|---|---|
| `process_*`（agent.exe） | `roles.carriers[]`（source 是 host+endpoint） | `subject.process` |
| `dst_ip_addr`/`dst_port` | `roles.target` 上 endpoint+host | `object.endpoint` 单类型 |
| `src_ip_addr`/`src_port` | source.endpoint | `facets.network.src_*`（主体已是进程） |
| `outcome=success` | 顶层 | `observed`（字段目录 2.3） |
| `operation=open` | 顶层 | `connect` |
| `dst_host_name` | target.host | `source_private` |
| `process_parent_*` | `roles.related[]` | `ancestry[]` |

校验：`logical_schema=passed`，`semantic_review=passed`。
