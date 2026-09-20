# suricata_flow 行为信封映射

样例：`runtime_observed.expected-sdm-event.behavior.json`
`mapping_id=suricata.suricata_flow.behavior.v1`
对标：网络会话汇总（无现成 sxf_probe netflow 信封）

WPL 尚未编写；来源列为 EVE JSON 键。夹具用内层 EVE。

| 来源 | 值 | SDM 路径 | 状态 |
|---|---|---|---|
| `src/dest` | `192.0.2.128:2750 → 203.0.113.28:4789` | `subject/object.endpoint` | mapped |
| `proto` | `UDP` | `facets.network.protocol=udp` | mapped |
| `flow.bytes_*` | `92/0` | `source_private` | source_private |

校验待跑。`semantic_review=candidate`。
