# leadsec / leadsec_av 运行时观测候选映射

事件事实：管理员 administrator 从 198.51.100.25 新增名为 test 的 AV 策略，result=0 表示操作正常。

主体：`administrator`；客体：`av_policy:test`；载体：`none`；观察者：Leadsec Power-V。

> 状态：candidate，未注册、未批准。仅 WPL 解析事实已确认，SDM 语义仍需人工复核。

| WPL 字段 | 值 | SDM 候选路径 | 状态 |
|---|---|---|---|
| `info` | `av` | `extensions_obj.source_private.info` | `source_private` |
| `devid` | `0` | `extensions_obj.source_private.devid` | `source_private` |
| `date` | `2026-01-23 11:00:00` | `occur_time` | `candidate` |
| `dname` | `themis` | `extensions_obj.source_private.dname` | `source_private` |
| `logtype` | `9` | `extensions_obj.source_private.logtype` | `source_private` |
| `pri` | `5` | `log_level` | `mapped` |
| `ver` | `0.3.0` | `extensions_obj.source_private.ver` | `source_private` |
| `from` | `198.51.100.25` | `roles_obj.source.endpoint.ip + source_ip` | `mapped` |
| `mod` | `av` | `extensions_obj.source_private.mod` | `source_private` |
| `act` | `add` | `roles_obj.target.resource.action` | `mapped` |
| `name` | `test` | `roles_obj.target.resource.name` | `mapped` |
| `result` | `0 → success` | `outcome` | `mapped` |
| `dsp_msg` | `add av policy` | `extensions_obj.source_private.dsp_msg` | `source_private` |
| `user` | `administrator` | `roles_obj.source.user.name + source_user` | `mapped` |
| `fwlog` | `0` | `extensions_obj.source_private.fwlog` | `source_private` |

## 人工语义复核（Leadsec Power-V）

- 事件事实：管理员 administrator 从 198.51.100.25 新增名为 test 的 AV 策略，result=0 表示操作正常。
- `event_category=audit`，`event_type=device_config_update`，`operation=empty`，`outcome=success`。
- `pri` 仅映射 `log_level`；来源 severity 保留在 `source_finding`。
- 文档证据：Power-V 192.0.2.120 日志格式手册 VERSION 0.3.0；证据状态 `vendor_confirmed_and_observed`。
- 对应章节：192.0.2.62「添加一条 av 策略」；`logtype=9` 是设备管理日志，`result=0` 表示正常。
- 主体为当前管理员 `administrator`（操作端 IP `198.51.100.25`）；客体为 AV 策略资源 `test`；无独立载体。
- 2.7.9 的 `logtype=7` 是另一种病毒告警格式，不适用于本样本。
