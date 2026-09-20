# suricata_alert / runtime_observed 行为信封角色判定

句式：WarpAxis `192.0.2.177:58542` 向腾讯元数据 `192.0.2.72:80` POST `/ca_report.cgi`（UA=Python-urllib/2.6）；Suricata 命中 ET INFO 2013031，未丢包。

| 角色 | 判定 | 证据 |
|---|---|---|
| subject | `endpoint` `192.0.2.177:58542` | 内层 `src_ip`/`src_port` |
| object | `endpoint` `192.0.2.72:80` | 内层 `dest_*`；HTTP host 进 facet，不另升 url 类型 |
| carriers[] | 空 | TCP/HTTP 是协议，进 facets |
| observer | `device` oisf / `203.0.113.28`，`ref_id=null` | 无资产 ID；`in_iface=eth0` 私有。产品名留 data_source |
| observation | `action=detect`，有 assertion，无 conclusion | `alert.action=allowed` 只表示 IDS 未 drop |

## 迁移裁决

- `behavior.layer=network` / `type=flow` / `operation=http_request`（本条 `app_proto=http`）。
- `outcome=observed`：不把 `alert.action=allowed` 写成 `assertion.conclusion=allow`（校验器会强制 `outcome=allowed`，语义是处置放行，不是「规则命中但未拦截」）。
- 检测：`assertion.title=signature`，`rule=signature_id`，`severity=Informational`（ET metadata），`confidence=High`。
- VXLAN `tunnel` 丢弃，不进入主客体。
- `flow_id` 私有；关联键契约暂缓。

`mapping_id=suricata.suricata_alert.behavior.v1`。
