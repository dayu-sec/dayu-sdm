# log-model

SDM2.0 日志/事件标准：安全设备日志接入与标准化事件存储。

## 范围

- 使用 SDM2.0 行为信封（`meta.schema_version` = `2.0`，`event_kind=behavior`）保存标准化安全设备日志，物理表 `sdm_event_behavior`。
- 客观行为在 `subject` / `object` / `carriers` / `facets`；来源设备自身的检测或告警判断在 `observation.assertion`。
- 原始日志分离到独立 `raw_log` 表，与事件经 `event_id` 1:1 关联。

> 旧五层 `sdm_event`（`metadata` / `event` / `roles` / `source_finding`，hybrid-v1）已退役并从发布管线移除；相关文档与注册表仅作历史对照。

## 目录结构

| 路径 | 内容 |
|---|---|
| [docs/main/](docs/main/) | 权威契约与字段清单：行为信封 JSON Schema（07）、枚举字典（06）、事件结构总览 |
| [docs/hybrid/](docs/hybrid/) | 旧 hybrid 事件（Kafka 载荷）字段标准，历史对照 |
| [docs/mappings/](docs/mappings/) | 跨来源、跨日志类型复用的通用映射规则（IP 资产富化等） |
| [docs/tianqing/overview/](docs/tianqing/overview/) | 天擎 WPL 输出及 SDM2.0 映射总览 |
| [contracts/](contracts/) | 对象字段注册表（`contracts/hybrid-event/object-fields.v1.json`，权威）；旧 `projection-registry.v1.json` 仅对照 |
| [schema/](schema/) | Doris DDL、迁移与 Routine Load SQL（生产行为表 `031`/`032`，原文表 `006`/`027`） |
| [scripts/](scripts/) | 事件校验器、切流 gate 与生成器脚本 |
| [examples/](examples/) | 各厂商日志的输入与预期 SDM2.0 行为信封样例 |

## 阅读顺序

1. `docs/main/00-sdm-event-structure-overview.md` —— 事件结构总览。
2. `docs/main/07-sdm-event-behavior.schema.json` —— 行为信封逻辑契约（权威）。
3. `docs/main/06-sdm-event-enum-catalog.md` —— 枚举与受控字典。
4. `schema/031_sdm_event_behavior.sql` —— 生产行为表 DDL。

## 脚本

- `scripts/validate_behavior_event.py` —— 行为信封样例校验（贡献映射前必跑）。
- `scripts/behavior_cutover_gate.py` —— log_type 切流准入 gate。
- `scripts/generate_*.py` —— 逻辑 schema / 枚举字典等生成器。

## 样例

`examples/<vendor>/<log_type>/` 下每个样例包含原始日志输入与预期 SDM2.0 行为信封输出
（`*.expected-sdm-event.behavior.json`），是新厂商映射贡献的参考格式
（见仓库根 [CONTRIBUTING.md](../CONTRIBUTING.md)）。
