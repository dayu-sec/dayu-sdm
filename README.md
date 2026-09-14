# DAYU-SDM

DAYU Security Data Model（SDM1.0）——面向安全运营的日志与告警数据标准。

- **sdm_event_behavior** 回答「发生了什么」：行为信封 2.0（subject/object/carriers/observation）。
- **sdm_alert** 是检出；**sdm_analysis** 是一次调查；**sdm_case** 是工作单元。
  AI 只追加分析行，正式 `verdict` 由策略或人写。

OCSF 是厂商中立的交换与分类基线；SDM2.0 是 SOC 内部的事件调查、实体角色和告警运营模型。两者分层兼容，不是替代关系。详见 [docs/9.SDM2.0-与OCSF对比分析.md](docs/9.SDM2.0-与OCSF对比分析.md)。

在线演示：[pages/index.html](pages/index.html)。

## 仓库结构

| 目录 | 内容 |
|---|---|
| [log-model/](log-model/) | 日志/事件标准：07 信封、031/032 物理与装载、枚举、厂商映射、事件样例 |
| [alert-model/](alert-model/) | 告警标准（**实验性 v0.2**）：告警/证据/实体/分析/案件/流转 |
| [docs/](docs/) | 跨领域设计文档：字段目录、实体清单、OCSF 分层兼容 |

权威口径：

- 逻辑契约：`log-model/docs/main/07-sdm-event-behavior.schema.json`（`meta.schema_version` = `2.0`）
- 字段目录：`docs/SDM事件模型逻辑契约字段目录.md`
- 物理表：`log-model/schema/031_sdm_event_behavior.sql`



## 快速了解

1. [docs/SDM事件模型逻辑契约字段目录.md](docs/SDM事件模型逻辑契约字段目录.md) —— 现行字段目录。
2. [log-model/docs/main/07-sdm-event-behavior.schema.json](log-model/docs/main/07-sdm-event-behavior.schema.json) —— 行为信封。
3. [alert-model/docs/00-overview.md](alert-model/docs/00-overview.md) —— 告警模型分层。
4. [docs/9.SDM2.0-与OCSF对比分析.md](docs/9.SDM2.0-与OCSF对比分析.md) —— 与 OCSF 的对比。
5. [log-model/examples/](log-model/examples/) —— 脱敏样例（`*.behavior.json`）。

## 存储引擎

物理实现基于 Apache Doris（`sdm_event_behavior` 标量投影 + VARIANT），Kafka 为接入总线。Routine Load SQL 使用占位符，不要填入真实集群地址后提交。


## 版本

见 [CHANGELOG.md](CHANGELOG.md)。标准文档与 schema 均按版本发布。

## 贡献

见 [CONTRIBUTING.md](CONTRIBUTING.md)。新厂商日志映射是最欢迎的贡献类型。样例必须脱敏。

## 许可

Copyright 2026 dayu-sec。Apache License 2.0，见 [LICENSE](LICENSE)。
