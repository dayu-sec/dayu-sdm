# 360 / 360_exthost_device_violation_log 运行时观测候选映射

事件事实：终端 WIN-EX02 尝试同时使用有线和无线网络，命中违规网络控制策略并执行 blockandalarm。

主体：`endpoint_host`；客体：`network_access_policy`；载体：`none`；观察者：360 EPP。

> 状态：candidate，未注册、未批准。仅 WPL 解析事实已确认，SDM 语义仍需人工复核。

| WPL 字段 | 值 | SDM 候选路径 | 状态 |
|---|---|---|---|
| `asset_username` | `hsakdjklas#@$%阿利克水泥钉金卡三年` | `extensions_obj.source_private.asset_username` | `source_private` |
| `clientip` | `203.0.113.37` | `device_ip/device_ipv4` | `mapped` |
| `computername` | `WIN-EX02` | `roles_obj.source.host.name + source_host` | `mapped` |
| `ctime` | `2026-01-23 03:00:00` | `occur_time` | `candidate` |
| `deal_type` | `blockandalarm` | `outcome + roles_obj.target.resource.action` | `mapped` |
| `description` | `DESKTOP-SKNR6QR上尝试有线无线网卡共用` | `source_finding_obj.title` | `mapped` |
| `event_type` | `wired_wifi_together_banned` | `roles_obj.target.resource.id` | `mapped` |
| `group_id` | `5` | `extensions_obj.source_private.group_id` | `source_private` |
| `id` | `1` | `extensions_obj.source_private.id` | `source_private` |
| `is_xc` | `2` | `extensions_obj.source_private.is_xc` | `source_private` |
| `local_ip` | `203.0.113.202` | `roles_obj.source.host.ip + source_ip` | `mapped` |
| `type` | `360exthost_device_violation_log` | `extensions_obj.source_private.type` | `source_private` |
| `ltime` | `2026-01-23 03:00:00` | `extensions_obj.source_private.ltime` | `source_private` |
| `m2` | `454500abe01bf30bdd352190f352e39dd6576a932baa` | `extensions_obj.source_private.m2` | `source_private` |
| `mac` | `00-00-5E-00-53-52` | `roles_obj.source.host.mac` | `mapped` |
| `os_type` | `Windows 10 Pro` | `roles_obj.source.host.os.name` | `mapped` |
| `plat_id` | `2` | `extensions_obj.source_private.plat_id` | `source_private` |
| `sysmaclist` | `00:00:5E:00:53:69;` | `extensions_obj.source_private.sysmaclist` | `source_private` |
| `username` | `WIN-EX02\\Administrator` | `roles_obj.source.user.name + source_user` | `mapped` |

## 人工语义复核（360 EPP）

- 事件事实：终端 WIN-EX02 尝试同时使用有线和无线网络，命中违规网络控制策略并执行 blockandalarm。
- 对应文档：32. 违规网络控制审计（7000 及后续版本）；证据状态 `vendor_confirmed_and_observed`。
- 主体为终端 `WIN-EX02`（本机 IP `203.0.113.202`），用户上下文为 `WIN-EX02\\Administrator`。
- 客体为命中的违规网络控制策略 `wired_wifi_together_banned`；样本没有具体网卡标识，不构造虚假网卡对象。
- `deal_type=blockandalarm` 保留来源原值，并映射 `outcome=denied` 和策略动作 `block_and_alarm`。
- 当前标准没有专用违规网络控制 event_type，因此保留 `event_type=generic_event`、`operation=empty`。
- `clientip=203.0.113.37` 是客户端通讯 IP，投影设备管理地址；行为源 IP 使用文档定义的 `local_ip`。
