# `edr_cs_op_log` 样例（计算系统操作日志）

本目录用于编写和验收天擎 `cs_op_log`（控制台计算系统操作日志）的 OML 与 SDM2.0 映射。

| 文件 | 用途 |
|---|---|
| `data_export.raw-log.json` | 天擎真实原始日志（sample.dat:23） |
| `data_export.wpl-output.json` | 按 parse.wpl `cs_op_log` 规则（:834）抽取的 WPL 输出 |
| `data_export.platform-context.json` | 平台上下文与缺口补齐 |
| `data_export.wpl-missing-fields.json` | WPL 抽取缺口声明（uuid） |
| `data_export.expected-sdm-event.json` | 期望 SDM 事件 |
| `data_export.wpl-to-sdm-event.{json,md}` | 逐字段映射 |

## 事件事实

控制台操作记录显示，操作员账号 `system001` 从 `203.0.113.138` 执行了"设置系统管理/系统设置/数据导出"操作（op_type=106、op_level=1、status=3）。原始日志没有登录动作或会话 ID，因此不解释为登录。天擎 Syslog V1.11 §4.2.1 `operation_audit_log` 定义 `status=3` 为成功。菜单 path 不是导出数据集实体。

## 主体 / 客体 / 载体

- 主体：操作员账号 `system001`（控制台用户，独立用户主体）→ `roles.source.user`
- 客体：无独立导出数据实体 → `roles.target=null`；菜单路径只作为操作对象上下文暂存 `source_private`
- 载体：日志未提供可识别的会话、进程或协议载体，不落 `roles.carriers`；“控制台管理会话”仅是业务背景，不作为观测事实
- 来源 IP：`203.0.113.138` → `roles.source.endpoint.ip`

## 关键映射决策

- `event_category=audit`。
- `event_type=system_audit_log_uncategorized`（06 枚举 #88）：cs_op 无更具体类型。
- `outcome=success`：文档 `status` 1=新发起、2=失败、**3=成功**。
- `op_level=1` 是普通操作等级，不是 SDM `severity`。
- 原始日志 `create_time` 为秒；WPL 的 `time_timestamp` 已将其转换为毫秒，SDM 映射阶段直接使用 WPL 输出的毫秒值作为事件时间。
- 操作字段（path/op_type/op_level/status/asset_id/asset_oid）无标准模型路径，入 `source_private`，README 未决问题中声明。
- `source_original_event_id` 由平台保留原始 uuid（WPL 规则缺口，见 wpl-missing-fields.json）。
- **user + endpoint 建模选择**：`roles.source` 主体为 `entity_type=user`（操作员账号），同时挂 `endpoint.ip` 表达操作来源 IP（05 目录 `roles.source.endpoint.ip` 合法）。这是既有样例（host+endpoint）之外的新模式；若标准模型确认主体为 user 时不宜同挂 endpoint，IP 将改挂 `source_private` 或新增 facet。已提交标准模型维护方确认。
- **原始日志追溯**：`expected-sdm-event.raw_msg` 直接来自 `data_export.raw-log.json` 的原始内容；`platform-context.json` 只保存平台治理值和 WPL 缺口补齐值，不负责生成或保存原始日志内容。
- **source_private 路径约定**：私有扩展字段直接放在 `extensions.source_private.<field>` 下；厂商、产品、日志类型和映射契约已由顶层字段表达。

## 舍弃字段

| 字段 | 原因 |
|---|---|
| `entity_id` | null，空值不落 |
| `request`、`source`、`collect_time` | WPL 规则未抽取；`collect_time` 为采集侧时间，事件时间以 `create_time` 为准 |

## WPL 缺口

- `uuid`：规则 `json()` 抽取列表未包含 `@uuid`，但 event_id 确定性哈希需要它；已声明于 `wpl-missing-fields.json`，建议规则补抽。

## 未决问题

1. `status=3` 已由 Syslog V1.11 §4.2.1 确认为成功；`op_type=106` 仍无业务名，不升 `operation`。
2. 控制台操作对象（path）与 asset 上下文（asset_id/asset_oid）的标准建模路径待定；当前入私有扩展。
3. `system_audit_log_uncategorized` 是否足够，或需要更细的审计事件类型，待审计模型演进决定。

## 当前物理注册表迁移

本目录 expected 已迁移到当前 87 字段物理注册表。原始日志与映射身份未丢失：原文保存在 `*.raw-log.json`，expected 与 raw_log 的关联统一用 `event_id`，mapping 身份保存在对应映射 JSON/Markdown。
