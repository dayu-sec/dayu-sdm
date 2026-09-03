# flow_dns 行为信封映射

样例：`runtime_observed.expected-sdm-event.behavior.json`  
`mapping_id=sxf_probe.flow_dns.behavior.v1`  
旧物理 mapping 保留。

## 相对旧 mapping 的关键纠正

| 来源 | 旧落位 | 新落位 |
|---|---|---|
| `src_ip` / `dst_ip` | `source_ip` / `target_ip`；roles 为 null | `subject.endpoint` / `object.endpoint` |
| `queries` | source_private | `facets.dns.question.name` |
| `qtypes=12` | source_private | `question.type=PTR` + 原值私有 |
| `transproto=UDP` | 扁平 `protocol` | `facets.network.protocol=udp` |
| `outcome` | writer `success` | `observed`（`qr=0` 且 `ancnt=0`） |
| `id=1` | 候选 event_id | DNS 报文 ID，私有 |
| `vendor` | 私有复写 | 丢弃（已有 `data_source.vendor`） |
| `Questions` | 私有垃圾串 | 丢弃 |
| `appproto=DNS` | 候选 protocol | 丢弃（dns facet 已表达） |

客体按迁移矩阵「DNS 请求/响应包」：对端 endpoint，不是 `domain`。

校验：`logical_schema=passed`，`semantic_review=passed`；物理投影 `not_run`。
