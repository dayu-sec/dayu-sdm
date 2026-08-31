# qax_firewall / bh_host_risk_log 运行时观测候选映射

事件事实：堡垒机报告主机风险：`riskType=risk_user`，`content=system risk account:yabroot`。这是来源发现，不是已完成处置。

主体：`none`；客体：`host`（堡垒机自身）；载体：`none`；关联：系统用户 `root`；观察者：来源产品。

> 状态：candidate，未注册、未批准。`riskType` 文档表与示例冲突。

| WPL 字段 | 值 | SDM 候选路径 | 状态 |
|---|---|---|---|
| `access_time` | `2026-02-03 16:55:13.733618` | `extensions_obj.source_private.access_time` | `source_private` |
| `logType` | `YAB_HOST_RISK_LOG` | `extensions_obj.source_private.logType` | `source_private` |
| `time` | `2026-01-23 11:00:00` | `occur_time` | `candidate` |
| `user` | `root` | `roles_obj.related[0].user.name` | `candidate` |
| `prod_name` | `堡垒机` | `roles_obj.target.host.name` | `candidate` |
| `prod_id` | `f73b12355cd64a4ea36d42ed9c4d1e4e` | `extensions_obj.source_private.prod_id` | `source_private` |
| `prod_version` | `203.0.113.245` | `extensions_obj.source_private.prod_version` | `source_private` |
| `prod_ips` | WPL 数组调试串 | `extensions_obj.source_private.prod_ips` | `source_private` |
| `riskType` | `risk_user` | `source_finding_obj.category` / `title` | `conflicted` |
| `content` | `system risk account:yabroot` | `source_finding_obj.description` | `candidate` |

## 人工语义复核（KB47750）

- 事件事实：堡垒机报告主机风险：riskType=risk_user，content=system risk account:yabroot。这是来源发现，不是已完成处置。文档字段表写 USER/PRODCESS/NET_CONNECT，示例与样本为 risk_user，枚举 conflicted。user=root 是系统用户名，不是主体。
- event_category：`alert`
- event_type：`generic_event`
- operation：`空；无充分标准动作证据`
- outcome：`unknown`
- 证据：奇安信堡垒机 192.0.2.70 Syslog 格式说明 KB47750 §2.12；对应 `logType` 为 `YAB_HOST_RISK_LOG`。
- 状态：`reviewed_candidate`
