# suricata_tls / runtime_observed 行为信封角色判定

句式：`203.0.113.170:50716` TLS1.3 连 `198.51.100.198:443`，SNI=nexus.corp.dy-sec.com。

| 角色 | 判定 | 证据 |
|---|---|---|
| subject | endpoint 203.0.113.170:50716 | src_* |
| object | endpoint 198.51.100.198:443 | dest_*；SNI 进 facet 不升 domain |
| observation | record | 握手记录 |

## 迁移裁决

- 对标 flow_dns：名字进 facet。
- JA3/JA4 私有。

`mapping_id=suricata.suricata_tls.behavior.v1`。
