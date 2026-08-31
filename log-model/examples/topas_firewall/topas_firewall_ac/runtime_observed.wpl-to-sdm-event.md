# topas_firewall / topas_firewall_ac 运行时观测候选映射

事件事实：记录源端到目标端的网络连接或访问控制活动。

主体：`source_host_or_ip`；客体：`target_host_or_ip`；载体：`network_protocol_or_session`；观察者：来源产品。

> 状态：candidate，未注册、未批准。仅 WPL 解析事实已确认，SDM 语义仍需人工复核。

| WPL 字段 | 值 | SDM 候选路径 | 状态 |
|---|---|---|---|
| `id` | `NGTOS` | `event_id` | `candidate` |
| `version` | `V3.2294.23041_NGFW.1_R` | `extensions_obj.source_private.version` | `source_private` |
| `time` | `2026-01-23 11:00:00` | `occur_time` | `candidate` |
| `dev` | `TopsecOS_180` | `extensions_obj.source_private.dev` | `source_private` |
| `pri` | `6` | `extensions_obj.source_private.pri` | `source_private` |
| `type` | `ac` | `extensions_obj.source_private.type` | `source_private` |
| `recorder` | `ac` | `extensions_obj.source_private.recorder` | `source_private` |
| `index` | `1050` | `event_id` | `candidate` |
| `vsid` | `0` | `extensions_obj.source_private.vsid` | `source_private` |
| `vsys_name` | `root_vsys` | `extensions_obj.source_private.vsys_name` | `source_private` |
| `policyid` | `15435` | `extensions_obj.source_private.policyid` | `source_private` |
| `policyname` | `fw412144024` | `extensions_obj.source_private.policyname` | `source_private` |
| `protoname` | `UDP` | `protocol` | `candidate` |
| `src` | `203.0.113.109` | `extensions_obj.source_private.src` | `source_private` |
| `sport` | `5246` | `source_port` | `candidate` |
| `dst` | `198.51.100.179` | `extensions_obj.source_private.dst` | `source_private` |
| `dport` | `12222` | `target_port` | `candidate` |
| `action` | `accept` | `outcome` | `candidate` |
| `appname` | `unknown` | `extensions_obj.source_private.appname` | `source_private` |
| `user` | `unknown` | `source_user` | `candidate` |

## 人工语义复核（Topas Firewall）

- 事件事实：防火墙访问控制日志记录 UDP 会话命中策略，action=accept 的厂商枚举含义为允许。
- `event_category=network`，`event_type=network_connection`，`operation=empty`，`outcome=allowed`。
- `pri` 仅进入 `log_level`。
- 文档证据：天融信《防火墙日志规范 v23.2》对应 admin/ac 章节。
