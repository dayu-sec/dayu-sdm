# sxf_probe / flow_dns 运行时观测候选映射

事件事实：源端发起或接收 DNS 活动。

主体：`source_host_or_ip`；客体：`dns_name_or_server`；载体：`dns_protocol`；观察者：来源产品。

> 状态：candidate，未注册、未批准。仅 WPL 解析事实已确认，SDM 语义仍需人工复核。

| WPL 字段 | 值 | SDM 候选路径 | 状态 |
|---|---|---|---|
| `Questions` | `[FieldStorage { cur_name: None, value: Owned(Field { meta: Obj, name: "obj", value: Obj(ObjectValue({"QClass": FieldStorage { cur_name: None, value: Owned(Field { meta: Digit, name: "QClass", value: Digit(1) }) }, "QName": FieldStorage { cur_name: None, value: Owned(Field { meta: Chars, name: "QName", value: Chars("203.0.113.203.in-addr.arpa") }) }, "QType": FieldStorage { cur_name: None, value: Owned(Field { meta: Digit, name: "QType", value: Digit(12) }) }})) }) }]` | `extensions_obj.source_private.Questions` | `source_private` |
| `aa` | `0` | `extensions_obj.source_private.aa` | `source_private` |
| `ad` | `0` | `extensions_obj.source_private.ad` | `source_private` |
| `afver` | `TS3.0.91.12428 Build20241231` | `extensions_obj.source_private.afver` | `source_private` |
| `ancnt` | `0` | `extensions_obj.source_private.ancnt` | `source_private` |
| `appproto` | `DNS` | `protocol` | `candidate` |
| `arcnt` | `0` | `extensions_obj.source_private.arcnt` | `source_private` |
| `cd` | `0` | `extensions_obj.source_private.cd` | `source_private` |
| `cf` | `128` | `extensions_obj.source_private.cf` | `source_private` |
| `devname` | `SANGFOR STA` | `extensions_obj.source_private.devname` | `source_private` |
| `ds` | `20250522` | `extensions_obj.source_private.ds` | `source_private` |
| `dst_ip` | `192.0.2.123` | `target_ip` | `candidate` |
| `dst_port` | `53` | `target_port` | `candidate` |
| `dzone` | `2` | `extensions_obj.source_private.dzone` | `source_private` |
| `hh` | `20` | `extensions_obj.source_private.hh` | `source_private` |
| `id` | `1` | `event_id` | `candidate` |
| `iptype` | `4` | `extensions_obj.source_private.iptype` | `source_private` |
| `length` | `38` | `extensions_obj.source_private.length` | `source_private` |
| `logid` | `47917011244531` | `extensions_obj.source_private.logid` | `source_private` |
| `logtype` | `dns_request` | `extensions_obj.source_private.logtype` | `source_private` |
| `nscnt` | `0` | `extensions_obj.source_private.nscnt` | `source_private` |
| `opcode` | `0` | `extensions_obj.source_private.opcode` | `source_private` |
| `qclasses` | `1` | `extensions_obj.source_private.qclasses` | `source_private` |
| `qdcnt` | `1` | `extensions_obj.source_private.qdcnt` | `source_private` |
| `qr` | `0` | `extensions_obj.source_private.qr` | `source_private` |
| `qtypes` | `12` | `extensions_obj.source_private.qtypes` | `source_private` |
| `queries` | `203.0.113.203.in-addr.arpa` | `extensions_obj.source_private.queries` | `source_private` |
| `ra` | `0` | `extensions_obj.source_private.ra` | `source_private` |
| `rcode` | `0` | `extensions_obj.source_private.rcode` | `source_private` |
| `rd` | `1` | `extensions_obj.source_private.rd` | `source_private` |
| `src_ip` | `192.0.2.199` | `source_ip` | `candidate` |
| `src_port` | `52040` | `source_port` | `candidate` |
| `szone` | `2` | `extensions_obj.source_private.szone` | `source_private` |
| `tc` | `0` | `extensions_obj.source_private.tc` | `source_private` |
| `transproto` | `UDP` | `protocol` | `candidate` |
| `ts` | `2025-05-22 12:30:11` | `occur_time` | `candidate` |
| `uid` | `Dbe03dedc4d4babf059e8d27a213827cf` | `extensions_obj.source_private.uid` | `source_private` |
| `vendor` | `sangfor` | `extensions_obj.source_private.vendor` | `source_private` |
| `z` | `0` | `extensions_obj.source_private.z` | `source_private` |

## 人工语义复核（SXF Probe）

- 事件事实：探针记录一次 DNS PTR 查询，rcode=0 表示该 DNS 响应无错误。
- `event_category=network`，`event_type=network_dns`，`operation=query`，`outcome=success`。
- 文档证据：深信服《潜伏威胁探针数据接口对外说明 V2.0》；运行样本已命中。
- 未确认的协议数字/命令字典保留原值并 report。
