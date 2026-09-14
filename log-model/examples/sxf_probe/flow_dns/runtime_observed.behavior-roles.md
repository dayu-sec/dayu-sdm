# flow_dns / runtime_observed 行为信封角色判定

句式：客户端 `9.9.9.1:52040` 向 `9.9.9.2:53` 发起 DNS PTR 查询 `2.9.9.9.in-addr.arpa`；探针只记录请求。

| 角色 | 判定 | 证据 |
|---|---|---|
| subject | `endpoint` `9.9.9.1:52040` | `src_ip` / `src_port`。旧 `roles.source=null` 是 mapping 未决，不是没有主体 |
| object | `endpoint` `9.9.9.2:53` | `dst_ip` / `dst_port`。流量日志客体是对端服务器（迁移矩阵「DNS 请求/响应包」）；查询名进 `facets.dns.question`，不升第二类型 `domain`（那是解析/审计日志） |
| carriers[] | 空 | `appproto=DNS` / `transproto=UDP` 是协议，进 facets，不是载体 |
| observer | `device` `vendor=sangfor`，`ref_id=null` | `devname=SANGFOR STA` 不是唯一实例，进 `source_private.devname`。样例无观察者 IP，不发明 `device.ip`。产品名留 `meta.data_source.product` |
| observation | `action=record`，无 assertion | `source_finding_obj=null`；`logtype=dns_request` |

## 迁移裁决（相对旧物理 expected）

- `behavior.layer=network` / `type=flow` / `operation=dns_query`。
- `outcome=observed`：`qr=0` 是请求，`ancnt=0` 无应答。`rcode=0` 在查询上不是执行成功。旧 expected / 人工复核的 `success` 把请求码当成响应结果，本条纠正。
- 查询名 `2.9.9.9.in-addr.arpa`、`qtypes=12`→`facets.dns.question.type=PTR`（IANA 标准，不是厂商字典）。无 `answers[]`。
- `transproto=UDP` → `facets.network.protocol=udp`（小写）。`qtypes=12` 原值留 `source_private.qtypes`。
- `src_ip`/`dst_ip`/端口不进 `source_private`（已有标准位）。丢弃 WPL `Questions` 的 FieldStorage 垃圾串。
- `data_src_instance_id` 为空：无采集器实例，也不填 observer。
- 无 PRI、无检测严重度；不写顶层 severity。
- `mapping_id=sxf_probe.flow_dns.behavior.v1`。

旧 `runtime_observed.expected-sdm-event.json` 保持 interim 物理形，M4 再切投影。
