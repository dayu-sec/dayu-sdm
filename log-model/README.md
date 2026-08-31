# log-model

SDM2.0 日志/事件标准：安全设备日志接入与标准化事件存储。

## 范围

- 使用 SDM2.0 五层事件模型保存标准化安全设备日志（`sdm_event`）。
- 使用 `source_finding` 保存设备自身的检测或告警判断。
- 原始日志分离到独立 `raw_log` 表，与 `sdm_event` 经 `event_id` 1:1 关联。

## 目录结构

| 路径 | 内容 |
|---|---|
| [docs/main/](docs/main/) | 权威契约与字段清单：事件结构总览、逻辑字段清单、枚举字典、Kafka hybrid schema |
| [docs/hybrid/](docs/hybrid/) | hybrid 事件（Kafka 载荷）的字段标准与投影规则 |
| [docs/mappings/](docs/mappings/) | 跨来源、跨日志类型复用的通用映射规则（IP 资产富化等） |
| [docs/tianqing/overview/](docs/tianqing/overview/) | 天擎 WPL 输出及 SDM2.0 映射总览 |
| [contracts/](contracts/) | 物理投影注册表（`contracts/hybrid-event/projection-registry.v1.json`，权威契约）、事件操作字典 |
| [schema/](schema/) | Doris DDL、迁移与 Routine Load SQL |
| [scripts/](scripts/) | schema / 字段清单 / 枚举字典生成器与事件校验器 |
| [examples/](examples/) | 各厂商日志的输入与预期 SDM2.0 事件样例 |

## 阅读顺序

1. `docs/main/00-sdm-event-structure-overview.md` —— 事件结构总览。
2. `docs/main/05-sdm-event-logical-field-catalog.md` —— 五层逻辑字段清单（权威）。
3. `docs/main/06-sdm-event-enum-catalog.md` —— 枚举与受控字典。
4. `docs/main/05-sdm-event-kafka-hybrid.schema.json` —— Kafka hybrid 载荷 JSON Schema。
5. `contracts/hybrid-event/projection-registry.v1.json` —— 物理投影注册表（权威）。

## 脚本

- `scripts/generate_sdm_event_ddl.py` —— 从 projection-registry 生成 `sdm_event` DDL。
- `scripts/generate_sdm_event_logical_schema.py` / `generate_sdm_event_logical_catalog.py` / `generate_sdm_event_enum_catalog.py` / `generate_sdm_event_kafka_schema.py` —— 生成逻辑 schema、字段清单、枚举字典、Kafka schema。
- `scripts/validate_candidate_physical_events.py` —— 校验候选事件样例（贡献映射前必跑）。

## 样例

`examples/<vendor>/<log_type>/` 下每个样例包含原始日志输入与预期 SDM2.0 事件输出，
是新厂商映射贡献的参考格式（见仓库根 [CONTRIBUTING.md](../CONTRIBUTING.md)）。
