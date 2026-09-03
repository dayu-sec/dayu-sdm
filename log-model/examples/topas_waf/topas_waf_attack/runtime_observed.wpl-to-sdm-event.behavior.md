# topas_waf_attack 行为信封映射

样例：`runtime_observed.expected-sdm-event.behavior.json`  
`mapping_id=topas_waf.topas_waf_attack.behavior.v1`  
旧物理 mapping 保留为 `runtime_observed.wpl-to-sdm-event.json`。

## 相对旧 mapping 的关键纠正

| 来源 | 旧落位 | 新落位 |
|---|---|---|
| `pri` | source_private | `meta.source_record.log_level` |
| `severity=High` | 顶层 `severity` | `assertion.severity=HIGH` + `original_severity` |
| `action=deny` | `outcome=unknown` | `assertion.conclusion=deny`；`outcome=denied`（deny **且** HTTP 403） |
| `client_ip` / `server_ip` | `source_ip` / `target_ip` | `subject.endpoint` / `object.endpoint` |
| `host` | source_private | `facets.http.request.host`（raw Host，不是 `server=test`） |
| `url` / `http_method` / `http_status` | 私有或扁平列 | `facets.http.*` |
| `type=waf` | source_private.type | `observer_class` |
| `msg` | source_private | `assertion.title`，不进 `behavior.message` |
| `id=ngtos` / `rule_id` 当 event_id | 错误候选 | 丢弃 / `assertion.rule` |

`event_kind=behavior`，`record_kind=finding`，`observation.action=detect`。

校验：`logical_schema=passed`，`semantic_review=passed`；物理投影 `not_run`。
