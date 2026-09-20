# suricata_anomaly 行为信封映射

样例：`runtime_observed.expected-sdm-event.behavior.json`
`mapping_id=suricata.suricata_anomaly.behavior.v1`
对标：无现成包；协议解析失败记录

WPL 尚未编写；来源列为 EVE JSON 键。夹具用内层 EVE。

| 来源 | 值 | SDM 路径 | 状态 |
|---|---|---|---|
| `src/dest` | `192.0.2.128:80 → 203.0.113.170:33942` | `subject/object.endpoint` | mapped |
| `anomaly.event` | `REQUEST_HEADER_INVALID` | `source_private` | source_private |

校验待跑。
