# qax_firewall / bh_middleware_log 运行时观测候选映射

事件事实：系统用户 `root` 侧记录中间件 `redis` 的操作内容「start redis service」。无结果字段。

主体：`user`；客体：`middleware_service`；载体：`none`；观察者：来源产品。

> 状态：candidate，未注册、未批准。`content` 自由文本，不升成 `service_start`。

| WPL 字段 | 值 | SDM 候选路径 | 状态 |
|---|---|---|---|
| `access_time` | `2026-02-03 16:55:13.733618` | `extensions_obj.source_private.access_time` | `source_private` |
| `logType` | `YAB_MIDDLE_WARE_LOG` | `extensions_obj.source_private.logType` | `source_private` |
| `time` | `2026-01-23 11:00:00` | `occur_time` | `candidate` |
| `user` | `root` | `source_user` / `roles_obj.source.user.name` | `candidate` |
| `prod_name` | `堡垒机` | `extensions_obj.source_private.prod_name` | `source_private` |
| `prod_id` | `f73b12355cd64a4ea36d42ed9c4d1e4e` | `extensions_obj.source_private.prod_id` | `source_private` |
| `prod_version` | `203.0.113.245` | `extensions_obj.source_private.prod_version` | `source_private` |
| `prod_ips` | WPL 数组调试串 | `extensions_obj.source_private.prod_ips` | `source_private` |
| `middleType` | `redis` | `roles_obj.target.service.name` | `candidate` |
| `content` | `start redis service` | `extensions_obj.source_private.content` | `source_private` |

## 人工语义复核（KB47750）

- 事件事实：系统用户 root 侧记录中间件 redis 的操作内容「start redis service」。content 为自由文本，不升成 service_start；无结果字段，outcome=unknown。
- event_category：`system`
- event_type：`generic_event`
- operation：`空；无充分标准动作证据`
- outcome：`unknown`
- 证据：奇安信堡垒机 192.0.2.70 Syslog 格式说明 KB47750 §2.14；对应 `logType` 为 `YAB_MIDDLE_WARE_LOG`。
- 状态：`reviewed_candidate`
