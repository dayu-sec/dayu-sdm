# suricata_tls 行为信封映射

样例：`runtime_observed.expected-sdm-event.behavior.json`
`mapping_id=suricata.suricata_tls.behavior.v1`
对标：无现成包；facets.tls 开放域

WPL 尚未编写；来源列为 EVE JSON 键。夹具用内层 EVE。

| 来源 | 值 | SDM 路径 | 状态 |
|---|---|---|---|
| `src/dest` | `203.0.113.170 → 198.51.100.198:443` | `subject/object.endpoint` | mapped |
| `tls.sni` | `nexus.corp.dy-sec.com` | `facets.tls.sni` | mapped |
| `ja3.hash` | `ceb419f4…` | `source_private` | source_private |

校验待跑。
