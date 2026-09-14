# log-model

SDM2.0 日志/事件标准：安全设备日志接入与标准化行为事件存储。

## 范围

- 行为信封 2.0（`event_kind=behavior`）写入 `sdm_event_behavior`。
- 观察判断在 `observation.assertion`，不改写 subject / object / facets。
- 原文在独立 `raw_log`，与行为事件经 `event_id` 1:1 关联。


## 目录结构

| 路径 | 内容 |
|---|---|
| [docs/main/](docs/main/) | 07 信封、Kafka 行为消息、枚举、结构概览 |
| [docs/mappings/](docs/mappings/) | 跨来源通用映射规则 |
| [contracts/](contracts/) | object-fields、object-registry.v2、切流 allowlist |
| [schema/](schema/) | 031/032 行为表与装载、006 raw_log |
| [scripts/](scripts/) | 行为信封校验器与切流 gate |
| [examples/](examples/) | 厂商样例（`*.expected-sdm-event.behavior.json`） |

## 阅读顺序

1. `docs/main/00-sdm-event-structure-overview.md` —— 事件结构总览。
2. `../docs/SDM事件模型逻辑契约字段目录.md` —— 现行字段目录。
3. `docs/main/07-sdm-event-behavior.schema.json` —— 行为信封机器契约。
4. `docs/main/07-sdm-event-behavior-kafka-schema.md` —— Kafka 消息（07 同树，三时间为 unix ms）。
5. `docs/main/06-sdm-event-enum-catalog.md` —— 闭合枚举。
6. `schema/031_sdm_event_behavior.sql` —— 物理表。

## 脚本

- `scripts/validate_behavior_event.py` —— 校验行为信封样例。
- `scripts/behavior_cutover_gate.py` —— 切流准入。

## 样例

`examples/<vendor>/<log_type>/` 下每个样例包含原始日志输入与预期行为信封输出，
是新厂商映射贡献的参考格式（见仓库根 [CONTRIBUTING.md](../CONTRIBUTING.md)）。
