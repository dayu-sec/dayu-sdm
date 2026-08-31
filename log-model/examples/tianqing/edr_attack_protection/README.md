# `edr_attack_protection` 样例（攻击防护日志）

本目录用于编写和验收天擎 `edr_attack_protection`（攻击防护）日志的 OML 与 SDM2.0 映射。

| 文件 | 用途 |
|---|---|
| `iexplore_attack_block.raw-log.json` | 天擎真实原始日志（sample.dat:9） |
| `iexplore_attack_block.wpl-output.json` | WPL 输出（44 字段） |
| `iexplore_attack_block.wpl-missing-fields.json` | 规则缺口（asset_id/subject/object/uuid） |
| `iexplore_attack_block.platform-context.json` | 平台上下文 |
| `iexplore_attack_block.expected-sdm-event.json` | 期望 SDM 事件 |
| `iexplore_attack_block.wpl-to-sdm-event.{json,md}` | 逐字段映射 |

## 事件事实

终端 `Test-shifang-Win7`（192.0.2.71）上攻击防护引擎拦截攻击：攻击主体进程 `iexplore.exe` 试图修改注册表启动项（object=`hkey_local_machine\software\…\run\[testkey:set->testvalue]`），攻击类型 attack_type=2，拦截结果 result=1，触发方式 trigger_mode=20。

## 主体 / 客体 / 载体

- 主体：攻击进程 `iexplore.exe` → `roles.source.process`（规则未抽 subject，raw_log 补齐）
- 客体：注册表启动项 `testkey` → `roles.target.resource{type: registry_value}`；键路径和值数据进入 `facets.registry`
- 载体：无进程载体 → `carriers=[]`；防护引擎为检测方（observer）

## 关键映射决策

- `event_category=alert`、`record_kind=finding`、`event_domain=threat`：防护拦截是来源检测告警，结论入 `source_finding.title`。
- `event_type=registry_modification`：`object` 是注册表启动项 `set`；厂商 `event_type=11`（脚本攻击）留 `source_private`。
- `outcome=denied`：PDF §3.2.3 `result=1` 已拦截。`result` 不进 `finding.status`。
- `source_original_event_id` 无原始事件 ID（guid 为空），用 `attack_time_ms|subject` 派生组合（未决 3）。
- 进程是直接行为主体；终端资产以 `roles.related.host{relation_type: execution_host}` 关联，并由 `profiles.endpoint_asset` 承载资产画像。
- 原始 `object` 中 `\run` 被 JSON 解析为回车字符加 `un`；标准事件按注册表语义纠正为 `\\run`，raw_msg 保留原始证据。

## 未决问题

1. 厂商 `event_type=11`（脚本攻击）与 object=注册表不一致；以 object 为准。
2. `attack_type=2` / `trigger_mode=20` 业务名仍待字典确认。
3. 原始日志无事件 ID，source_original_event_id 用派生组合，跨事件去重依赖 attack_time+subject+host。

## 当前物理注册表迁移

本目录 expected 已迁移到当前 87 字段物理注册表。原始日志与映射身份未丢失：原文保存在 `*.raw-log.json`，expected 与 raw_log 的关联统一用 `event_id`，mapping 身份保存在对应映射 JSON/Markdown。
