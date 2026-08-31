# `edr_account_change` 样例

本样例来自天擎 WPL `sample.dat` 中的账号变更记录，样例名为 `account_changed`。

事件事实：`lsass.exe` 在主机 `A0XXXXX-NC02` 上执行了账号信息变更，日志将目标账户以 `XXXXXX` 脱敏；原始 `event_type=userinfo_changed` 只能确认修改用户信息（天擎 Syslog V1.11 §3.9.6），不能确认创建、删除或改密。

主体是承载账号变更的主机及其 `lsass.exe` 进程；客体是目标账号 `XXXXXX`；独立操作者用户未提供。无会话/协议，载体 none。父进程 `wininit.exe` 作为关联实体保留。

`event_category=audit`。`event_type` 归一为 `user_uncategorized`（标准无 `account_change`，也不是 `user_change_password`）。`operation` 留空，`outcome=observed` 表示观察到该行为，不代表成功或失败。

`account_name` 映射到 `roles.target.account.name`，同时以 `target_user` 保留热字段；两者均为脱敏值。具体动作枚举和稳定账户标识记录在 `account_changed.wpl-missing-fields.json`。

当前 `parse.wpl` 使用 `time@timestamp`，而真实样例的 `timestamp=0`，通过 `wpl-check` 会在时间解析阶段失败。因此本目录的 `wpl-output.json` 是按当前 WPL 字段清单整理的预期抽取结果，不宣称是本次 `wpl-check` 的成功运行输出；该解析缺口已单独记录。

## 当前物理注册表迁移

本目录 expected 已迁移到当前 87 字段物理注册表。原始日志与映射身份未丢失：原文保存在 `*.raw-log.json`，expected 与 raw_log 的关联统一用 `event_id`，mapping 身份保存在对应映射 JSON/Markdown。
