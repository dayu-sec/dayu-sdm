# inbound_refuse 行为信封映射

样例：`inbound_refuse.expected-sdm-event.behavior.json`  
`mapping_id=tianqing.edr_ip_access.inbound_refuse.behavior.v1`  
旧物理 mapping 保留。

## 相对旧 mapping 的关键纠正

| 来源 | 旧落位 | 新落位 |
|---|---|---|
| `src_ip_addr` | `source_ip` + host 主体 | `subject.endpoint`（发起端才是主体） |
| `dst_ip_addr`/`dst_port` | `roles.target` | `object.endpoint`；端口不进 ref_id |
| `process_*`（svchost） | `roles.carriers[]` 复用 | 保持 carriers，`carrier_role=server_process` |
| `outcome=failed` | 顶层 | `observed`；`connection_refused` 进 `facets.network.connection_result` |
| `operation=refuse` | 顶层 | `connect`（refused 是结果） |
| `src_host_name=unknown` | 可能当主机名 | 占位，丢弃 |
| `severity=info` | 顶层 | 删除 |

与 `outbound_open` 对称：协议层连接结果一律 facet + `observed`。

校验：`logical_schema=passed`，`semantic_review=passed`。
