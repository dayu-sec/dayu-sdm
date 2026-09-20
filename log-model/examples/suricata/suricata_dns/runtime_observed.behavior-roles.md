# suricata_dns / runtime_observed 行为信封角色判定

句式：`192.0.2.177:57305` 向 `203.0.113.194:53` 发起 DNS A 查询 `ntpupdate.tencentyun.com`；探针只记录 request。

| 角色 | 判定 | 证据 |
|---|---|---|
| subject | `endpoint` `192.0.2.177:57305` | src_* |
| object | `endpoint` `203.0.113.194:53` | 对端 DNS 服务器；`rrname` 进 `facets.dns.question`，不升 domain |
| carriers[] | 空 | UDP/DNS 是协议 |
| observer | `device` oisf / `203.0.113.28` | 同 alert |
| observation | `action=record`，无 assertion | 流量记录不是检测 |

## 迁移裁决

- 对标 `sxf_probe.flow_dns`：客体是 endpoint，查询名进 facet。
- `outcome=observed`：`dns.type=request`。请求上的 `rcode=NOERROR` 不进 `success`，也不写 `facets.dns.response.code`。
- `dns.id` 私有，不当 event_id。
- **response**：EVE `src` 是 DNS 服务器。OML 交换主客体，使 `subject` 始终为查询发起方、`object` 为 DNS 服务器（与 request 同一语义）。

`mapping_id=suricata.suricata_dns.behavior.v1`。
