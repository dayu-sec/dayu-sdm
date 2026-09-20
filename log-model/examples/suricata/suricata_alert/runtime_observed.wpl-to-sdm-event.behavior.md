# suricata_alert 行为信封映射

样例：`runtime_observed.expected-sdm-event.behavior.json`
`mapping_id=suricata.suricata_alert.behavior.v1`
对标：`topas_ips_attack` / `topas_waf_attack`（detect + assertion）

WPL 尚未编写；下表 `来源` 为 EVE JSON 键。采集是 fluent-bit `json_lines` 包一层，夹具用内层 EVE。

| 来源 | 值 | SDM 路径 | 状态 |
|---|---|---|---|
| `src_ip/dest_ip` | `192.0.2.177 / 192.0.2.72` | `subject/object.endpoint` | mapped |
| `proto` | `TCP` | `facets.network.protocol=tcp` | mapped |
| `http.*` | `POST /ca_report.cgi` | `facets.http.request.*` | mapped |
| `alert.signature` | `ET INFO Python-urllib/...` | `assertion.title` | mapped |
| `alert.signature_id` | `2013031` | `assertion.rule` | mapped |
| `alert.action` | `allowed` | `source_private.alert_action` | source_private |
| `tunnel` | `VXLAN → 203.0.113.28:4789` | `—` | dropped |

校验：`logical_schema` 待跑；`semantic_review=candidate`；未进 allowlist。
