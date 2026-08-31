# qax_firewall / bh_his_session_record_log 运行时观测候选映射

事件事实：堡垒机登记用户 `admin` 对运维资源 `DefaultRegion_Linux_10.xxx.xxx.78_22` 的历史 SSH 会话（运维账户 `root`）及回放地址；不把历史记录扩写成当场网络连接。

主体：`user`；客体：`managed_resource`；载体：`recorded_session`；关联：运维账户 `root`；观察者：来源产品。

> 状态：candidate，未注册、未批准。`account` 不得写入 `source_user`。

| WPL 字段 | 值 | SDM 候选路径 | 状态 |
|---|---|---|---|
| `access_time` | `2026-02-03 16:55:13.733618` | `extensions_obj.source_private.access_time` | `source_private` |
| `logType` | `YAB_HISTORY_SESSION_LOG` | `extensions_obj.source_private.logType` | `source_private` |
| `startTime` | `2026-01-23 11:00:00` | `occur_time` | `candidate` |
| `endTime` | `2026-01-23 11:00:00` | `extensions_obj.source_private.endTime` | `source_private` |
| `user` | `admin` | `source_user` / `roles_obj.source.user.name` | `candidate` |
| `sourceIP` | `10.xxx.xxx.30` | `source_ip` | `candidate` |
| `resource` | `DefaultRegion_Linux_10.xxx.xxx.78_22` | `roles_obj.target.resource.name` | `candidate` |
| `targetIP` | `10.xxx.xxx.78` | `target_ip` | `candidate` |
| `protocol` | `SSH` | `carrier_protocol` | `candidate` |
| `account` | `root` | `roles_obj.related[0].user.name` | `candidate` |
| `historySession` | 回放 URL（含 WPL 吞入的 prod_name） | `roles_obj.carriers[0].session.url` | `candidate` |
| `prod_id` | `a4a1a7d27403424eae9fda6c6747c625` | `extensions_obj.source_private.prod_id` | `source_private` |
| `prod_version` | `V3.4.44.0` | `extensions_obj.source_private.prod_version` | `source_private` |
| `prod_ips` | WPL 数组调试串 | `extensions_obj.source_private.prod_ips` | `source_private` |

## 人工语义复核（KB47750）

- 事件事实：堡垒机登记用户 admin 对运维资源 DefaultRegion_Linux_10.xxx.xxx.78_22 的历史 SSH 会话（运维账户 root）及回放地址；不把历史记录扩写成当场发生的网络连接。account 不是 source_user。
- event_category：`audit`
- event_type：`generic_event`
- operation：`空；无充分标准动作证据`
- outcome：`unknown`
- 证据：奇安信堡垒机 192.0.2.70 Syslog 格式说明 KB47750 §2.6；对应 `logType` 为 `YAB_HISTORY_SESSION_LOG`。
- 状态：`reviewed_candidate`
