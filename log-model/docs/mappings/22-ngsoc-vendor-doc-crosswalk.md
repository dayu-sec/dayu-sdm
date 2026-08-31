# NGSOC 厂商文档对照审计

## 1. 审计范围

本审计以 `references/device-logs/奇安信/ngsoc/4.13.1 NGSOC威胁告警syslog外发格式说明.docx` 为厂商参考基线，对照仓库现有 NGSOC 原始日志、WPL/OML 和样例映射。

文档元数据明确为：文档编号 `V1.0`、版本编号 `NGSOC-4.13.1`、日期 `2023-07-12`。因此这里的 `4.13.1` 是厂商格式版本标识，不是仓库映射的 `format_version`；仓库当前 `format_version=1` 仍表示本地映射契约版本。

现有样例分为两类：

| 日志类型 | 样例数量 | 与文档的关系 | 处理结论 |
|---|---:|---|---|
| `ngsoc_threat_alert_send` | 6 | 文档标题直接描述的 NGSOC 威胁告警 Syslog 外发格式；其中包含 JSON 外发样例 | 作为本轮强约束对象 |
| `ngsoc_alert_info` | 22 | 历史 KV 告警格式；字段有较多同名项，但文档未证明它与该 KV 格式完全等价 | 只做同源字段核验，不直接套用外发格式 |

> 样例数量按当前 `examples/ngsoc` 目录中的样例目录统计；`ngsoc_threat_alert_send` 中部分样例的 `raw-log.json` 是完整 JSON，部分只保存 `raw_msg`，因此不能把“文档字段存在”误写成“每个样例均已观测”。

## 2. 文档确认的字段契约

下列内容由厂商文档直接给出，优先级高于此前仅依据样例归纳的候选字典：

| 原始字段 | 文档类型/必填 | 文档语义或枚举 | SDM 对照结论 |
|---|---|---|---|
| `uuid` | UUID / 是 | 告警标识 | 可作为 `source_original_event_id` 候选；不得直接替代 `event_id` |
| `seq` | Long / 是 | 告警序列 | 来源私有字段；不能当作全局事件 ID |
| `name` | String / 是 | 告警名称 | `source_alert_name` |
| `timestamp` | LocalDateTime / 是 | 首次告警时间 | `occur_time` 候选；需确认时区口径 |
| `latestTimestamp` | LocalDateTime / 是 | 最新一次告警时间 | 来源 finding 扩展；不能覆盖首次发生时间 |
| `devIp` | List<String> / 否 | 数据源 IP | 设备/观察者地址候选，不能按 `source_ip` 处理 |
| `srcIp` / `dstIp` | List<String> / 否 | 源 IP / 目的 IP | 多值时进入角色集合；仅唯一值时可投影 `source_ip` / `target_ip` |
| `confidence` | Short / 是 | 1 低、2 中、3 高 | 文档确认的置信度字典；原值须保留，标准化结果放来源 finding |
| `compromiseState` | Boolean / 是 | false 不涉及、true 已失陷 | 文档确认布尔语义；不得把空值或 finding 记录机械转为已失陷 |
| `killchain` | Short / 是 | 0 不涉及、1-8 攻击链阶段 | 文档确认数值字典；此前中文值是 KV 兼容表示，不能反推 JSON 数值格式 |
| `attackResult` | Short / 是 | 0 不涉及、1 成功、2 企图、3 失败 | 文档确认来源攻击结果；只有底层动作语义成立时才投影顶层 `outcome` |
| `severity` | Short / 是 | 1 低危、2 中危、3 高危、4 危急 | 文档确认来源告警严重度；与 Syslog PRI 的 `log_level` 分离 |
| `ioc` / `iocType` | List / 否 | IOC 及类型 | 来源 finding/扩展；按值类型解析，不复制完整原文 |
| `domain` / `uri` | List / 否 | 域名 / URI | 继续使用现有域名、URI authority 和 `IP:port` 解析边界 |
| `times` | Integer / 是 | 告警发生次数 | 来源 finding 扩展；不等同于重复事件条数 |
| `source` | Short / 是 | 0 关联规则、1 用户导入、2 上传、3 上级规则下发 | 来源告警来源字典，不能写入 `operation` |
| `disposeState` / `ticketState` | Short/Integer / 是 | 处置和工单状态 | 平台处置状态，不属于 `sdm_event` 的底层动作结果 |
| `ruleCategoryName` / `relevantRuleName` | String / 是 | 告警类型 / 检测规则 | `source_alert_category`、来源规则扩展候选 |
| `victimContent` / `attackerContent` | List<String> / 否 | 受害者 / 攻击者 | 只有文档声明支持时建立 attacker/victim 关系；SDM source/target 仍按事件事实判定 |
| `attCk` | List<String> / 否 | ATT&CK | 保留到 MITRE 技术 ID；中文名称需另行字典核验 |
| `commDirection` | List<String> / 否 | 内到内、未知、外到内、内到外 | 来源方向；写 `facets.network.direction`，不恢复旧标量 |
| `extraFields` | Map<String,List<String>> / 是 | 可配置扩展字段 | 允许的源扩展入口；必须按字段名登记，禁止 catch-all 原文复制 |

文档还列出了 HTTP、文件、进程、邮件、漏洞、资产等扩展字段，例如 `httpMethod`、`httpRspCode`、`fileMd5`、`fileSha256`、`processName`、`mailSubject`、`cve`、`assetName`。这些字段应按“标准字段优先、来源扩展其次”的顺序逐项核对，不能仅因出现在 `extraFields` 就全部进入事件表。

## 3. 与现有实现的差异

### 3.1 已有实现可以保留的部分

- `ngsoc_threat_alert_send` 已被单独建模，未与 `ngsoc_alert_info` 共用稳定 `log_type`。
- 当前映射契约已经要求保留 `attackResult`、`killchain`、`compromiseState`、`attCk`、`commDirection` 原值并报告未知枚举。
- 当前契约已禁止把 Syslog PRI 直接当安全严重度，并将方向放在 `facets.network.direction`。
- `domain`、URI authority 和 `IP:port` 的解析边界与文档字段定义相容。

### 3.2 需要修订或补证的部分

| 项目 | 现状 | 文档对照后的处理 |
|---|---|---|
| 格式版本 | 样例/规则使用本地 `format_version=1`，未记录 `NGSOC-4.13.1` | 在来源资料和映射审计元数据中记录 `source_format_version=NGSOC-4.13.1`；不改本地 manifest 身份 |
| `severity` | 既有 WPL/OML 兼容数字和中文，并将数字 1-4 转为内部值 | 数字 1-4 的来源字典已获文档确认；中文值只作为 KV 历史兼容输入，不应作为 JSON 外发格式契约 |
| `attackResult` | 同时兼容数字和中文 | JSON 外发基线优先采用 0-3 数字；中文只保留为 `ngsoc_alert_info` 兼容路径 |
| `killchain` | 现有规则存在中文到数字转换，且 `自动获取` 的历史映射需复核 | 文档确认 `8=自动获取`；不得把 8 映射成 1，历史兼容转换应单独标记并复核 |
| `compromiseState` | 既有规则将 `true` 转为内部代码 3 | 文档只确认布尔语义；内部代码属于本地标准化，不得声称是厂商值 |
| 必填字段 | `extraFields`、`timestamp` 等在文档中必填，但部分样例或 WPL 输出缺失 | 在样例缺口文件中区分“文档要求但输入缺失”和“该样例未保留原始字段” |
| `disposeState`、`ticketState` | 与检测事件字段混在同一原始对象中 | 仅作为来源/平台状态扩展，不能生成 `outcome` 或 `operation` |
| 多值角色投影 | 既有契约规定唯一值才投影标量 | 继续保留；多值字段必须留在角色数组或扩展，不丢弃其他值 |

## 4. 对既有样例的整理分层

后续重整建议按以下顺序执行：

1. `ngsoc_threat_alert_send`：以 `NGSOC-4.13.1` 为来源格式版本，逐样例核对字段类型、数字枚举、必填字段和 `extraFields`；先修订映射文档与缺口声明，再决定是否调整 WPL/OML。
2. `ngsoc_alert_info`：维持独立的 KV 格式基线，使用现有 22 个样例验证字段同名但不假设类型相同；单独记录中文枚举、空值表现、数组序列化和字段缺失。
3. 共享字段：只有在两个格式的语义、类型和缺失策略都一致时，才提升到共享映射契约；否则保留格式专属转换。

## 5. 当前结论

- 这份文档足以把 `ngsoc_threat_alert_send` 中上述核心字段的来源枚举从“样例推断”升级为“厂商文档确认”。
- 它不能直接证明 `ngsoc_alert_info` 的 KV 字段类型和枚举完全相同；两者必须继续分开维护。
- 当前最重要的实现风险是 `killchain=8` 的错误兼容映射、格式版本没有进入映射元数据，以及将处置状态误当作事件结果。
- 本轮只完成对照审计，没有修改 WPL、OML、标准契约或既有样例的事实内容；后续修改应以本审计为依据逐项落地并重新运行样例校验。
