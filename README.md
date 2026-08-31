# DAYU-SDM

DAYU Security Data Model（SDM1.0）——面向安全运营的日志与告警数据标准。

- **sdm_event** 回答「发生了什么」：五层逻辑事件模型，标准化安全设备日志。
- **sdm_alert** 是检出；**sdm_analysis** 是一次调查；**sdm_case** 是工作单元。
  AI 只追加分析行，正式 `verdict` 由策略或人写。

OCSF 是厂商中立的交换与分类基线；SDM2.0 是 SOC 内部的事件调查、实体角色和告警运营模型。两者分层兼容，不是替代关系。详见 [docs/9.SDM2.0-与OCSF对比分析.md](docs/9.SDM2.0-与OCSF对比分析.md)。

在线演示：[pages/index.html](pages/index.html)。

## 仓库结构

| 目录 | 内容 |
|---|---|
| [log-model/](log-model/) | 日志/事件标准：Doris DDL、Kafka hybrid 契约、逻辑字段清单、枚举字典、厂商映射、事件样例 |
| [alert-model/](alert-model/) | 告警标准（**实验性 v0.2**）：告警/证据/实体/分析/案件/流转契约、DDL、枚举、样例 |
| [docs/](docs/) | 跨领域设计文档：实体清单、概念研究、五层逻辑对象与字段投影、与 OCSF 对比 |

权威口径：

- 逻辑字段：504 条核心叶子路径（`log-model/docs/main/05-sdm-event-logical-field-catalog.md`）
- 物理投影：hybrid-v1，`log-model/schema/007_sdm_event.sql`（由 `projection-registry.v1.json` 生成）
- 早期 87 列宽表与 002/raw_msg 临时契约已退役

## 快速了解

1. [docs/10.SDM2.0-日志五层逻辑对象与字段投影设计.md](docs/10.SDM2.0-日志五层逻辑对象与字段投影设计.md) —— 核心设计。
2. [log-model/docs/main/05-sdm-event-logical-field-catalog.md](log-model/docs/main/05-sdm-event-logical-field-catalog.md) —— 事件逻辑字段清单（权威）。
3. [alert-model/docs/00-overview.md](alert-model/docs/00-overview.md) —— 告警模型分层与阅读顺序。
4. [docs/9.SDM2.0-与OCSF对比分析.md](docs/9.SDM2.0-与OCSF对比分析.md) —— 与 OCSF 的对比。
5. [log-model/examples/](log-model/examples/) / [alert-model/examples/](alert-model/examples/) —— 脱敏后的输入/输出样例。

## 存储引擎

物理实现基于 Apache Doris（`sdm_event` 采用 hybrid 投影：标量列 + VARIANT），
Kafka 为接入总线。逻辑模型不绑定具体引擎。Routine Load SQL 使用 `__KAFKA_BROKERS__` 等占位符，不要填入真实集群地址后提交回本仓库。

## 版本

见 [CHANGELOG.md](CHANGELOG.md)。标准文档与 schema 均按版本发布。

## 贡献

见 [CONTRIBUTING.md](CONTRIBUTING.md)。新厂商日志映射是最欢迎的贡献类型。样例必须脱敏。

## 许可

Copyright 2026 dayu-sec。Apache License 2.0，见 [LICENSE](LICENSE)。
