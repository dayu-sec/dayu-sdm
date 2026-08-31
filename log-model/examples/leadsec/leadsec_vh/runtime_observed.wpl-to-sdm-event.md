# leadsec / leadsec_vh 运行时观测候选映射

事件事实：主机隔离管理操作（recorder=block_monitor）——管理员 root 将 203.0.113.206 加入黑名单，result=0=成功。管理声明在 source_finding。

主体：`administrator`（source.user=root）；客体：`isolated_host`（target.host=203.0.113.206）；载体：`none`；观察者：来源产品。

> 状态：candidate，未注册、未批准。WPL 解析事实与 Power-V 文档已确认；SR-050 人工复核结论见文末。

| WPL 字段 | 值 | SDM 候选路径 | 状态 |
|---|---|---|---|
| `info` | `block_monitor` | `extensions_obj.source_private.info` | `source_private` |
| `devid` | `0` | `extensions_obj.source_private.devid` | `source_private` |
| `date` | `2026-01-23 11:00:00` | `occur_time` | `candidate` |
| `dname` | `themis` | `extensions_obj.source_private.dname` | `source_private` |
| `logtype` | `15` | `extensions_obj.source_private.logtype` | `source_private` |
| `pri` | `5` | `extensions_obj.source_private.pri` | `source_private` |
| `ver` | `0.3.0` | `extensions_obj.source_private.ver` | `source_private` |
| `mod` | `主机隔离` | `extensions_obj.source_private.mod` | `source_private` |
| `act` | `添加` | `source_finding_obj.status` | `confirmed` |
| `result` | `0` | `outcome`（0=成功 -> success） | `confirmed` |
| `user` | `root` | `roles_obj.source.user.name` | `confirmed` |
| `dsp_msg` | `主机隔离：添加黑名单，ip为10.1.5.200 ` | `source_finding_obj.title` | `confirmed` |
| `fwlog` | `0` | `extensions_obj.source_private.fwlog` | `source_private` |

## 人工语义复核（Leadsec Power-V，SR-050）

- 事件事实：主机隔离日志记录将 203.0.113.206 加入黑名单，result=0 的文档枚举含义为成功。
- **event_category=`audit`**（主机隔离是管理员操作记录，非攻击检测告警；与 SR-030/032 一致）
- `event_type=network_connection`，`operation=empty`，`outcome=success`（result=0=成功）。
- 主体/客体/载体：administrator（source.user=root）/ isolated_host（target.host）/ none
- 管理声明：`source_finding_obj`（title=dsp_msg/status=act/count）
- `pri` 仅映射 `log_level`。
- 文档证据：Power-V 192.0.2.120 日志格式手册 VERSION 0.3.0；证据状态 `vendor_confirmed_and_observed`。
