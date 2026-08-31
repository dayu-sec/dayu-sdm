# 贡献指南

感谢关注 DAYU-SDM。本仓库是标准本体：schema、契约、字段清单、枚举与样例。

## 最欢迎的贡献

1. **新厂商/产品日志映射**：按 `log-model/docs/mappings/` 现有文档的结构，
   提供原始日志样本、字段映射表和预期 SDM2.0 事件（参考 `log-model/examples/`）。
2. **映射纠错**：对现有映射提出证据支持的修正（引用厂商文档或真实样本）。
3. **文档澄清**与**新枚举值申请**。

## 提交前须知

- 样例日志必须来自测试环境或彻底脱敏：不得包含真实客户 IP、主机名、账号、域名。
- 事件样例必须能通过 `log-model/scripts/validate_candidate_physical_events.py` 校验。
- schema 变更必须同时更新对应字段清单/枚举文档与 CHANGELOG。
- 不接受二进制厂商文档（xlsx/pdf）；映射结论以 Markdown/JSON 呈现。

## 流程

1. Fork 并从 `main` 切分支。
2. 提交 PR，说明变更类型（映射/字段/枚举/文档）与证据来源。
3. 破坏性 schema 变更需在 issue 中先讨论并被接受。

## 行为准则

保持专业、对事不对人。
