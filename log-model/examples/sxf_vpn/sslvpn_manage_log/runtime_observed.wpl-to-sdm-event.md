# sxf_vpn / sslvpn_manage_log 运行时观测候选映射

事件事实：本地 IKE 服务 `Isakmp_Server` 与网关 `Sangfor_Azure` 的第一阶段 SA 协商失败，连接未建立。

主体：`local_ike_endpoint`；客体：`vpn_gateway`；载体：`none`；观察者：来源产品。

> 状态：candidate，`sample_inferred`。AC XLSX 不是本 SVPN JSON 手册。其他 `SVPN-SYSTEM` 消息不得套用本条 `outcome=failed`。

| WPL 字段 | 值 | SDM 候选路径 | 状态 |
|---|---|---|---|
| `time` | `2026-01-30 17:55:43` | `occur_time` | `candidate` |
| `symbol` | `SVPN-SYSTEM` | `extensions_obj.source_private.symbol` | `source_private` |
| `deviceID` | `` | `extensions_obj.source_private.deviceID` | `source_private` |
| `id` | `25502388389` | `extensions_obj.source_private.id` | `source_private` |
| `logLevel` | `warn` | `log_level` | `candidate` |
| `module` | `Dlan` | `extensions_obj.source_private.module` | `source_private` |
| `msg` | 第一阶段 SA 协商失败 | `roles` 名称 + `outcome=failed` | `sample_inferred` |
| `msgid` | `1888642` | `extensions_obj.source_private.msgid` | `source_private` |
| `timeStamp` | `1769766943` | `extensions_obj.source_private.timeStamp` | `source_private` |
| `type` | `syslog` | `extensions_obj.source_private.type` | `source_private` |

## 人工语义复核（SXF VPN）

- 事件事实：本地 IKE 服务 Isakmp_Server 与网关 Sangfor_Azure 的第一阶段 SA 协商失败，连接未建立。站点 IKE，不是远程用户客户端。无 session id，不编造载体。
- event_category：`network`
- event_type：`network_connection`
- operation：`空`
- outcome：`failed`
- 证据：当前 SVPN-SYSTEM JSON 样本文案；AC XLSX 仅为旁证。
- 状态：`reviewed_sample_inferred`
