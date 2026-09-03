# baidu_tracert 行为信封映射

样例：`baidu_tracert.expected-sdm-event.behavior.json`  
`mapping_id=tianqing.edr_net_out_log.baidu_tracert.behavior.v1`  
旧物理 mapping 保留。

## 相对旧 mapping 的关键纠正

| 来源 | 旧落位 | 新落位 |
|---|---|---|
| `name` / `report_ip` / `mac` | `roles.source.host` | `subject.host`（无进程） |
| `net_out_ip` | `roles.target.endpoint` | `object.endpoint` |
| `outreach_address` | source_private | 保持私有，不升 domain |
| `operation` | null | writer `connect`（矩阵） |
| `is_ok=0` | source_private | 保持；不得当 `failed` |
| WPL `create_time` | 可能当 occur_time | 资产注册时间，丢弃；occur_time 用 raw unix 秒 |
| 内存/IE/语言等 | 可能进 profiles | 丢弃，非本事件事实 |
| `severity=info` | 顶层 | 删除 |

`event_kind=behavior`，`type=flow`，`action=record`。

校验：`logical_schema=passed`，`semantic_review=passed`；物理投影 `not_run`。
