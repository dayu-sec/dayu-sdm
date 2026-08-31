# 文档导航

本目录按文档职责组织，文件名前的编号仅保留原有形成顺序，不再用于表达目录层级。

| 目录 | 内容 |
|---|---|
| `main/` | 中间版本契约、Doris 字段清单、逻辑字段清单和枚举字典 |
| `analysis/` | 检索字段等分析材料 |
| `assessments/` | 技术评估和验证报告 |
| `plans/` | POC 切换方案与执行记录 |
| `mappings/` | 跨来源、跨日志类型复用的通用映射规则 |
| `tianqing/overview/` | 天擎 WPL 输出及 SDM2.0 映射总览 |
| `tianqing/field-traces/` | 天擎各日志类型的样例字段追踪和映射结论 |
| `tianqing/oml-prompts/` | 可交给 OML 编写模型或 Skill 的自包含提示词 |

新增天擎日志类型时，字段追踪放入 `tianqing/field-traces/`，对应提示词放入 `tianqing/oml-prompts/`；不要再直接写入 `docs/` 根目录。
