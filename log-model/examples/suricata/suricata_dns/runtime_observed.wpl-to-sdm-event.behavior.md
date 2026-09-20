# suricata_dns 行为信封映射

样例：`runtime_observed.expected-sdm-event.behavior.json`
`mapping_id=suricata.suricata_dns.behavior.v1`
对标：`sxf_probe.flow_dns.behavior.v1`

WPL 尚未编写；下表 `来源` 为 EVE JSON 键。采集是 fluent-bit `json_lines` 包一层，夹具用内层 EVE。

| 来源 | 值 | SDM 路径 | 状态 |
|---|---|---|---|
| `src_ip/dest_ip` | `192.0.2.177 / 203.0.113.194` | `subject/object.endpoint` | mapped |
| `dns.queries[0].rrname` | `ntpupdate.tencentyun.com` | `facets.dns.question.name` | mapped |
| `dns.queries[0].rrtype` | `A` | `facets.dns.question.type` | mapped |
| `dns.rcode` | `NOERROR` | `source_private.dns_rcode` | source_private |
| `dns.id` | `15959` | `source_private.dns_id` | source_private |

校验：`logical_schema` 待跑；`semantic_review=candidate`。
