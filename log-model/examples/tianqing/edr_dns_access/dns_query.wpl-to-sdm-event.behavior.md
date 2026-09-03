# dns_query 行为信封映射

样例：`dns_query.expected-sdm-event.behavior.json`  
`mapping_id=tianqing.edr_dns_access.dns_query.behavior.v1`  
旧物理 mapping 保留。

## 相对旧 mapping 的关键纠正

| 来源 | 旧落位 | 新落位 |
|---|---|---|
| 查询进程 `svchost.exe` | `roles.carriers[]`（source 是 host） | `subject.process` |
| `dns_host_name` | `target_domain` / `roles.target.domain` | `object.domain` + `facets.dns.question.name` |
| `dns_query_results` | 不应当 target IP | `facets.dns.answers[].address` |
| `dns_query_status=0` | `outcome=success` | `facets.dns.response.code=0`；`outcome=observed` |
| `dns_typed=1` | 私有或扁平 | `question.type=A` + 原值私有 |
| `ip` / `mac` / `computer_name` | `roles.source.host` | `profiles.endpoint_asset.host`；`carriers=[]` |
| `process_parent_*` | `roles.related[]` | `facets.process.ancestry[]` |
| `severity=info` | 顶层 | 删除 |

对照流量包 `sxf_probe/flow_dns`：本条 `type=read`、客体 `domain`，不是对端 endpoint。

校验：`logical_schema=passed`，`semantic_review=passed`；物理投影 `not_run`。
