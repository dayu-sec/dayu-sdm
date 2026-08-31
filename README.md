# DAYU-SDM

DAYU Security Data Model（SDM2.0）——面向安全运营的日志与告警数据标准。

- **sdm_event** 回答"发生了什么"：五层逻辑事件模型，标准化安全设备日志。
- **sdm_alert** 是检出；**sdm_analysis** 是一次调查；**sdm_case** 是工作单元。
  AI 只追加分析行，正式 `verdict` 由策略或人写。

🎬 **在线演示**：[presentation/index.html](presentation/index.html)——标准总览、日志标准、告警标准三套介绍页。

## 仓库结构

| 目录 | 内容 |
|---|---|
| [log-model/](log-model/) | 日志/事件标准：Doris DDL、Kafka hybrid 契约、逻辑字段清单、枚举字典、厂商映射、事件样例 |
| [alert-model/](alert-model/) | 告警标准：告警/证据/实体/分析/案件/流转契约（ADR）、DDL、枚举、样例 |
| [docs/](docs/) | 跨领域设计文档：实体清单、概念研究、五层逻辑对象与字段投影设计、与 OCSF 对比分析、基准测试方案 |

## 快速了解

1. [docs/10.SDM2.0-日志五层逻辑对象与字段投影设计.md](docs/10.SDM2.0-日志五层逻辑对象与字段投影设计.md) —— 核心设计。
2. [log-model/docs/main/05-sdm-event-logical-field-catalog.md](log-model/docs/main/05-sdm-event-logical-field-catalog.md) —— 事件逻辑字段清单（权威）。
3. [alert-model/docs/00-overview.md](alert-model/docs/00-overview.md) —— 告警模型分层与阅读顺序。
4. [docs/9.SDM2.0-与OCSF对比分析.md](docs/9.SDM2.0-与OCSF对比分析.md) —— 与 OCSF 的对比。
5. [log-model/examples/](log-model/examples/) / [alert-model/examples/](alert-model/examples/) —— 各厂商日志到 SDM2.0 的输入/输出样例。

## 存储引擎

物理实现基于 Apache Doris（`sdm_event` 采用 hybrid 投影：标量列 + VARIANT），
Kafka 为接入总线。逻辑模型不绑定具体引擎。

## 版本

见 [CHANGELOG.md](CHANGELOG.md)。标准文档与 schema 均按版本发布。

## 贡献

见 [CONTRIBUTING.md](CONTRIBUTING.md)。新厂商日志映射是最欢迎的贡献类型。

## 许可

Apache License 2.0，见 [LICENSE](LICENSE)。
