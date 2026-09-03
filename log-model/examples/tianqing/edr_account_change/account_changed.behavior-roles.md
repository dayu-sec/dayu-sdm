# edr_account_change / account_changed 行为信封角色判定

句式：进程 `lsass.exe`（pid 824）变更账号 `XXXXXX`（脱敏）；日志只说 `userinfo_changed`，不能确认创建/删除/改密。天擎只记录，无检测断言。

| 角色 | 判定 | 证据 |
|---|---|---|
| subject | `process` `lsass.exe` / guid `f4cdcc09…` | 执行变更的进程。旧 expected 把 source 标成 host 且并列 process |
| object | `account` `XXXXXX` | `account_name` / `account_user`。不是独立 user 主体；无稳定账户 id |
| carriers[] | 空 | 无会话/协议。`execution_host` 仍 `m3_review` |
| ancestry | 父 `wininit.exe` → `facets.process.ancestry[]` | WPL path `C:\WINDOWS\...`，`ref_id=process::{sha256(path)[:32]}` |
| observer | `application` `tianqing` | 采集器 → `meta.data_source.instance_id` |
| observation | `action=record`，无 assertion | `source_finding_obj=null` |

## 迁移裁决（相对旧物理 expected）

- `behavior.layer=system` / `type=change` / `operation=null` / `outcome=observed`。不能发明 `modify`/`change_password`。
- `event_type=userinfo_changed` 进 `source_private`，不升标准 operation。
- 顶层 `severity=info` 删除。
- `occur_time` `1629440451126` → `2021-08-20T06:20:51.126Z`。
- `mac=XX-XX-XX-XX-XX-XX`、空 `ip`/`report_ip` 不写。`pid=0` 哨兵，pid 用 `process_id=824`。
- `timestamp=0`、空 `gid`/`group_name`/`env_version` 丢弃；agent.version 用 platform `edr-8.0`。
- `mapping_id=tianqing.edr_account_change.account_changed.behavior.v1`。

旧 `account_changed.expected-sdm-event.json` 保持 interim 物理形，M4 再切投影。
