# sxf_vpn / sslvpn_user_log 运行时观测候选映射

事件事实：远程用户 `gyzcxt006` 从 `198.51.100.3` 成功注销 SSL VPN。

主体：`user`；客体：`none`；载体：`none`；观察者：来源产品。

> 状态：candidate，`sample_inferred`。WPL 未抽 `userName` / `clientInfo.ip` / `vip`。AC XLSX 不是本 JSON 手册。

| WPL 字段 | 值 | SDM 候选路径 | 状态 |
|---|---|---|---|
| `time` | `2026-01-30 17:55:24` | `occur_time` | `candidate` |
| `symbol` | `SVPN-USR` | `extensions_obj.source_private.symbol` | `source_private` |
| `actionResult` | `success` | `outcome=success` | `sample_inferred` |
| `id` | `25502369695` | `extensions_obj.source_private.id` | `source_private` |
| `logSubType` | `logout` | 支撑 `event_type=user_logout` | `sample_inferred` |
| `msg` | Log out successfully | `source_ip` / 文案 virtualIP | `sample_inferred` |
| `msgid` | `1888641` | `extensions_obj.source_private.msgid` | `source_private` |
| `rcip` | `` | `extensions_obj.source_private.rcip` | `source_private` |
| `timeStamp` | `1769766924` | `extensions_obj.source_private.timeStamp` | `source_private` |
| `type` | `userlog` | `extensions_obj.source_private.type` | `source_private` |
| `groupId` | `1035` | `extensions_obj.source_private.groupId` | `source_private` |
| `groupPath` | `/国有资产监管信息系统国有企业用户` | `extensions_obj.source_private.groupPath` | `source_private` |

原始 JSON 未进 WPL：`userInfo.userName=gyzcxt006` → `source_user`；`clientInfo.ip`；`clientInfo.vip=192.0.2.54`（与 msg `virtualIP=192.0.2.31` 并存）。

## 人工语义复核（SXF VPN）

- 事件事实：远程用户 gyzcxt006 从 198.51.100.3 成功注销 SSL VPN。无网关标识、无 session id。
- event_category：`auth`
- event_type：`user_logout`
- operation：`remote_service`
- outcome：`success`
- 证据：当前 SVPN-USR JSON 的 `logSubType`/`actionResult`；AC XLSX 仅为旁证。
- 状态：`reviewed_sample_inferred`
