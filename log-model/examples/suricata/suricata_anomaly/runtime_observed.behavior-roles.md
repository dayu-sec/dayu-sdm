# suricata_anomaly / runtime_observed 行为信封角色判定

句式：`192.0.2.128:80` 与 `203.0.113.170:33942` TCP，引擎报 HTTP REQUEST_HEADER_INVALID。

| 角色 | 判定 | 证据 |
|---|---|---|
| subject | endpoint 192.0.2.128:80 | src_* |
| object | endpoint 203.0.113.170:33942 | dest_* |
| observation | record，无 assertion | 引擎协议异常 ≠ IDS 规则命中 |

## 迁移裁决

- 不把 anomaly.event 写成 assertion.title/detect。
- `http.anomaly.count` 进私有或丢弃。

`mapping_id=suricata.suricata_anomaly.behavior.v1`。
