# suricata_http / runtime_observed 行为信封角色判定

句式：`192.0.2.177:58542` POST `192.0.2.72/ca_report.cgi`，HTTP 200；探针记录会话，无检测断言。

| 角色 | 判定 | 证据 |
|---|---|---|
| subject | `endpoint` `192.0.2.177:58542` | src_* |
| object | `endpoint` `192.0.2.72:80` | 对端；host/url 进 http facet |
| carriers[] | 空 | TCP/HTTP 进 facets |
| observer | `device` oisf / `203.0.113.28` | 同 alert |
| observation | `action=record`，无 assertion | 与同 flow 的 alert 拆成两条事件 |

## 迁移裁决

- 对标 `flow_web`，但信封 `outcome=observed`：HTTP 200 只进 `facets.http.response.status_code`。
- 与 `suricata_alert` 可共享 `flow_id`（本条 338363756588625），关联键暂缓，仅私有对照。

`mapping_id=suricata.suricata_http.behavior.v1`。
