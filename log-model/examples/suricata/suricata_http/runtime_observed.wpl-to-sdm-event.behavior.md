# suricata_http 行为信封映射

样例：`runtime_observed.expected-sdm-event.behavior.json`
`mapping_id=suricata.suricata_http.behavior.v1`
对标：`sxf_probe.flow_web`（信封纠正 outcome）

WPL 尚未编写；下表 `来源` 为 EVE JSON 键。采集是 fluent-bit `json_lines` 包一层，夹具用内层 EVE。

| 来源 | 值 | SDM 路径 | 状态 |
|---|---|---|---|
| `src_ip/dest_ip` | `192.0.2.177 / 192.0.2.72` | `subject/object.endpoint` | mapped |
| `http.http_method` | `POST` | `facets.http.request.method` | mapped |
| `http.status` | `200` | `facets.http.response.status_code` | mapped |
| `http.hostname` | `192.0.2.72` | `facets.http.request.host` | mapped |

校验：`logical_schema` 待跑；`semantic_review=candidate`。
