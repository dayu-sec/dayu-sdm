# account_changed 行为信封映射

样例：`account_changed.expected-sdm-event.behavior.json`  
`mapping_id=tianqing.edr_account_change.account_changed.behavior.v1`  
旧物理 mapping 保留。

## 相对旧 mapping 的关键纠正

| 来源 | 旧落位 | 新落位 |
|---|---|---|
| `process_*`（lsass.exe） | `roles.source` host+process | `subject.process` 单类型 |
| `account_name` / `account_user` | `target.account` + `target_user` | `object.account.name` |
| `event_type=userinfo_changed` | `user_uncategorized` / operation 空 | `source_private`；`operation` 仍 null |
| `process_parent_*` | `roles.related[]` | `facets.process.ancestry[]` |
| `computer_name` | `roles.source.host` | `profiles.host.name`（无 ip；mac 是脱敏哨兵） |
| `pid=0` | 可能当 pid | 哨兵；用 `process_id=824` |
| `severity=info` | 顶层 | 删除 |

`event_kind=behavior`，`type=change`，`action=record`。

校验：`logical_schema=passed`，`semantic_review=passed`；物理投影 `not_run`。
