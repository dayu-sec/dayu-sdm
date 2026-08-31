# NGSOC 厂商确认字段字典 v1

状态：`vendor_confirmed`。适用格式：`ngsoc_threat_alert_send`，来源格式版本：`NGSOC-4.13.1`。

来源文档：`references/device-logs/奇安信/ngsoc/4.13.1 NGSOC威胁告警syslog外发格式说明.docx`。

该字典不适用于历史 KV 格式 `ngsoc_alert_info`。后者继续使用 `ngsoc-device-field-dictionaries.inferred.v1`，其中文枚举属于兼容映射，不等同于本字典的数值型外发字段。

| 字段 | 厂商值 | 厂商含义 | SDM 归一化 |
|---|---:|---|---|
| `severity` | 1 / 2 / 3 / 4 | 低危 / 中危 / 高危 / 危急 | 仅来源严重度字典确认；顶层 `severity` 投影仍按 SDM 安全严重度策略执行 |
| `confidence` | 1 / 2 / 3 | 低 / 中 / 高 | 来源 finding 置信度 |
| `compromiseState` | false / true | 不涉及 / 已失陷 | `not_compromised` / `compromised` |
| `killchain` | 0-8 | 不涉及、侦查跟踪、武器构建、载荷投递、突防利用、安装植入、通信控制、达成目标、自动获取 | `not_applicable`、`reconnaissance`、`weaponization`、`delivery`、`exploitation`、`installation`、`command_and_control`、`actions_on_objectives`、`automated_collection` |
| `attackResult` | 0 / 1 / 2 / 3 | 不涉及 / 成功 / 企图 / 失败 | `not_applicable` / `success` / `attempted` / `failed` |
| `source` | 0 / 1 / 2 / 3 | 关联规则 / 用户导入 / 上传 / 上级规则下发 | 来源告警来源，保留为来源扩展 |
| `commDirection` | 中文标签 | 内到内、未知、外到内、内到外 | `L2L`、`unknown`、`W2L`、`L2W` |

原始值必须保留在来源 finding 或来源扩展中。该字典确认厂商字段含义，不自动证明每条告警的底层动作结果；`outcome` 仍需结合事件事实判断。
