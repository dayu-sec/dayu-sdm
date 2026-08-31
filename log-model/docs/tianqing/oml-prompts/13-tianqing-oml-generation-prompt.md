# 天擎 SDM2.0 OML 生成提示词

> **[历史记录] ldm_alert 穿透链路已废弃（feature/sdm2-alert-model）**：本文中生成大禹字段 `ldm_alert` 的步骤/映射已从当前交付物删除，仅保留 `sdm_event` finding 阶段有效；SDM2.0 告警模型将重新设计。

> 用途：将下面的“可直接使用的提示词”发送给负责编写 OML 的模型或 Skill。
> 建议每次只处理一个 `log_type`，完成实现、样例验证和评审后再处理下一个。
> 首批推荐顺序：`edr_process_event`、`edr_ip_access`、`edr_file_audit`、`edr_antivirus_virus`、`edr_alert_log`。

## 使用方式

每次使用前，只需要替换提示词中的两个参数：

```text
TARGET_LOG_TYPE=<本次处理的日志类型>
WRITE_CHANGES=true
```

- `WRITE_CHANGES=true`：允许修改对应 OML 配置并执行验证。
- `WRITE_CHANGES=false`：只输出实现方案、阻塞项和拟修改内容，不改文件。

不建议一次要求模型处理全部天擎规则。单类型处理更容易发现时间字段缺失、枚举不完整、数组截断和旧 OML 读取不存在字段等问题。

## 可直接使用的提示词

```text
你现在负责把天擎 WPL 已抽取的字段，重构为 SDM2.0 中间版本的 OML 输出。

参数：

TARGET_LOG_TYPE=<替换为本次处理的日志类型>
WRITE_CHANGES=true

一、目标

复用现有天擎 WPL，只重构 TARGET_LOG_TYPE 对应的 OML。WPL 负责字段抽取；OML 负责字段拼装、赋值、类型转换、枚举归一、对象构造和必要富化。

最终结果必须符合 sdm2_log.sdm_event 的 55 列中间版本结构：51 个标量投影字段，以及 roles_obj、facets_obj、source_finding_obj、extensions_obj 四个 VARIANT 完整对象字段。

本任务不生成 ldm_alert。平台告警由后续告警生成链路产生，并通过 ldm_alert.log_id_list 关联 sdm_event.log_id。

二、输入位置

仓库：
/Users/cloney/Workspace/SDM2.0

WPL：
/Users/cloney/Config/warp-rule/models/wpl/tianqing

现有 OML：
/Users/cloney/Config/warp-rule/models/oml/tianqing

需要修改的 OML：
/Users/cloney/Config/warp-rule/models/oml/tianqing/<TARGET_LOG_TYPE>/adm.oml

三、权威资料和优先级

必须按以下顺序读取和执行；下位资料不得覆盖上位资料：

1. 物理表 DDL：
   /Users/cloney/Workspace/SDM2.0/log-model/schema/002_sdm_event.sql

2. TARGET_LOG_TYPE 的 WPL 到 SDM2.0 物理映射：
   /Users/cloney/Workspace/SDM2.0/log-model/docs/tianqing/overview/12-tianqing-wpl-to-sdm-event-physical-mapping.md

3. SDM2.0 逻辑字段清单：
   /Users/cloney/Workspace/SDM2.0/log-model/docs/main/05-sdm-event-logical-field-catalog.md

4. SDM2.0 枚举与 event.type + event.operation 受控字典：
   /Users/cloney/Workspace/SDM2.0/log-model/docs/main/06-sdm-event-enum-catalog.md
   /Users/cloney/Workspace/SDM2.0/log-model/contracts/event_operation_dictionary.json

5. TARGET_LOG_TYPE 的 WPL 实际输出字段：
   /Users/cloney/Workspace/SDM2.0/log-model/docs/tianqing/overview/11-tianqing-wpl-source-field-and-sdm-mapping.md
   以及 WPL 源文件本身。

6. Doris 字段说明：
   /Users/cloney/Workspace/SDM2.0/log-model/docs/main/04-sdm-event-doris-field-catalog.md

现有旧 OML 只能用来参考 WarpParse 语法、已有查询富化和来源枚举转换，不能作为字段名称或 SDM 语义的权威来源。

四、开始实现前必须完成的检查

1. 定位 TARGET_LOG_TYPE 的 WPL 规则，列出它实际能够输出的所有别名和类型。
2. 检查现有 OML 的每个 read(...) 是否确实存在对应 WPL 输出。不得继续读取 WPL 没有抽取的字段。
3. 定位至少一条能命中该规则的脱敏样例；如果没有样例，停止写配置并报告阻塞。
4. 确认事件发生时间字段、格式和时区。occur_time 不能用 parse_time、当前时间或平台接收时间代替。
5. 确认来源稳定 ID 和原文。event_id、log_id、source_original_event_id 的职责不得混用，raw_msg 必须承载源日志数据。
6. 检查原始动作、状态、结果、严重度等枚举是否足以形成合法标准值。没有证据时留空或使用文档允许的受控兜底值，不得创造枚举。
7. 检查数组是否被 WPL 用 [0]、[0][0] 截断。存在截断时先报告，不得把首项伪装成完整事实。
8. 先给出检查结论和拟修改字段，再开始编辑；WRITE_CHANGES=false 时到此停止，不修改文件。

五、OML 输出约束

1. 只输出 002_sdm_event.sql 已存在的 55 个物理字段。不得输出旧大禹日志字段作为新表字段。
2. metadata 和 event 的高频字段使用 DDL 中的物理列名。
3. roles、facets、source_finding、extensions 必须构造完整对象，并分别序列化到：
   - roles_obj
   - facets_obj
   - source_finding_obj
   - extensions_obj
4. 某个逻辑路径有标量投影列时，标量列值必须与对应 VARIANT 路径完全一致，不能分别计算出不同值。
5. roles_obj、facets_obj、source_finding_obj 保存标准逻辑字段；天擎私有字段不得混入这些对象。
6. 天擎私有稳定字段放在：
   extensions.source_private.qax.tianqing.<TARGET_LOG_TYPE>.*
7. 终端资产快照优先使用已存在的：
   extensions.profiles.endpoint_asset
   Profile 必须包含可解析的 subject_ref，并引用 roles 中同一终端 host 的 ref_id；不能只写一组孤立资产属性。
8. extensions_obj 必须保留标准 envelope：schema_version、source_private、profiles、enrichments、unmapped。空容器按现行逻辑契约保留。
9. raw_msg 是 sdm_event 当前中间版的原文列，必须装载完整源日志；不得把 raw_msg、payload、原始 JSON 或完整来源数组重复复制到任一 VARIANT。
10. 后期建设独立原始日志存储后，再将 raw_msg 从事件表分离并引入引用字段；本阶段不得提前只存引用。
11. log_content 只保存有界事件摘要，最大 4096 字符，不保存完整原文。
12. 不新增 sdm_alert_evidence，不在 OML 中拼装 ldm_alert。

六、公共赋值规则

以下值只有在部署上下文没有更权威配置时才能采用：

- tenant_id：来自可信租户上下文；缺少可信上下文时使用空字符串，不得虚构租户标识。
- schema_version：1。
- mapping_id：qax.tianqing.<TARGET_LOG_TYPE>。
- data_src_vendor：qax。
- data_src_product：tianqing。
- data_src_category：endpoint_security。
- log_type：TARGET_LOG_TYPE。
- observer_vendor：qax，同时写 roles.observer.device.vendor。
- observer_product：tianqing，同时写 roles.observer.product.name。

data_src_instance_id 必须取采集任务或来源实例 ID，不能直接使用终端 client_id。

ingest_time 和 parse_time 是平台处理时间。只有当前 OML 所处阶段确实拥有这两个时间的生成责任时才赋值，否则交给接入层生成。

七、标识生成规则

- log_id：一条原始安全日志的稳定标识，优先使用采集链路提供的 wp_event_id 或等价稳定值。
- raw_msg：完整源日志原文，由采集链路传入；不得用摘要、事件 ID 或空占位替代。
- source_original_event_id：保存天擎自身稳定事件 ID，例如经确认后的 uuid、guid、alert_id。
- event_id：必须确定性生成。优先使用 tenant_id + mapping_id + source_original_event_id；没有来源事件 ID 时使用 tenant_id + log_id + log_type + 必要子事件序号。
- 重放相同日志必须得到相同 event_id。
- 不得把 asset_id 当作单条事件 ID。

八、事件语义规则

- source 表示行为主动方，target 表示受影响对象，carrier 表示承载行为的进程、协议、应用或会话，observer 表示观察产品。
- 不得把 attacker/victim 机械复制为 source/target。
- 受管终端是行为发生主机还是检测目标，必须根据 TARGET_LOG_TYPE 的事实判断。
- event.record_kind 只能使用 activity、finding、inventory、state、remediation。
- event.outcome 只能使用 success、failed、observed、denied、allowed、unknown。
- event.severity 使用事件/syslog 严重度；天擎告警高、中、低危写入 source_finding.severity，不能混用。
- event.type 必须来自受控字典。
- event.operation 必须是当前 event.type 允许的动作；没有合法组合时留空。
- 来源告警状态、处置状态和检测结果保存在 source_finding，不得直接变成 ldm_alert 的平台处置状态。

九、低频字段处理顺序

对每个未投影字段按以下顺序处理：

1. 已存在的 SDM 标准逻辑路径。
2. 已注册的 endpoint_asset Profile 路径。
3. extensions.source_private.qax.tianqing.<TARGET_LOG_TYPE> 下的稳定私有字段。
4. 明确不保留。

禁止为了方便把所有未映射字段批量复制到 extensions.unmapped。每个保留字段必须说明调查价值和稳定类型。

十、当前接线特别说明

/Users/cloney/Workspace/SDM2.0/log-model/schema/020_routine_load_sdm_event_interim.sql
仍是过渡接线：它读取部分旧扁平字段，并在 Doris 侧派生部分新字段。它不是本次 OML 字段语义的权威来源。

本次先按 55 列 DDL 和四个完整对象生成正确的目标 OML。同时必须输出一份“OML 输出字段与当前 Routine Load 输入字段差异”，至少列出：

- OML 已输出但当前 Routine Load 未消费的字段。
- Routine Load 仍读取的旧字段。
- roles_obj/facets_obj/source_finding_obj/extensions_obj 在 Kafka JSON 中的实际键名。
- 需要后续修改 Routine Load、sink 或序列化配置的项目。

不得为了兼容当前过渡 Routine Load 而破坏 SDM2.0 语义或继续沿用旧大禹字段。

十一、实现和验证

1. 只修改 TARGET_LOG_TYPE 对应的 adm.oml；除非 WPL 缺字段导致任务无法完成，否则不修改 WPL。
2. 如果必须修改 WPL，先停止 OML 编辑，列出缺失字段、原始 JSON 路径、建议别名和影响，等待明确授权。
3. 保持现有项目的 OML 语法和格式约定，每行表达式以分号结束。
4. raw_msg 如需读取只能 take 一次；其他字段使用 read。
5. 时间字段必须明确时区和毫秒/秒单位。
6. 对字符串转整数、IP、布尔值和数组的转换失败提供明确处理，不写虚假默认值。
7. 使用现有工具完成 WPL 语法和样例命中验证，并执行可用的 OML/工程检查。
8. 已知 /Users/cloney/Config/warp-rule/conf/wparse.toml 中 project_remote.infra 可能不被当前 wproj 支持。遇到此问题时，可以使用不修改生产配置的最小临时验证环境；如果仍无法验证，必须报告准确阻塞，不得声称验证通过。
9. 至少生成一条 TARGET_LOG_TYPE 的脱敏目标事件样例，检查 55 列字段名、四个对象结构、标量与对象同步关系以及必要字段。

十二、停止条件

出现以下任一情况时，不得凭猜测完成配置：

- 没有可命中的原始样例。
- 缺少可靠 occur_time。
- WPL 没有输出映射所需字段。
- 关键来源枚举无法解释。
- 稳定 ID 的唯一性范围无法判断。
- 数组被截断且会造成主要事实丢失。
- 无法确定字段表示受管终端、网络主动方还是网络目标方。

停止时给出最小阻塞清单和需要补充的具体资料。

十三、最终输出

完成后按以下顺序返回：

1. TARGET_LOG_TYPE 和事件事实判断。
2. WPL 实际输出字段检查结果，列出旧 OML 读取但 WPL 未输出的字段。
3. 已修改文件的绝对路径。
4. 关键映射摘要：WPL 字段 -> SDM 逻辑路径 -> Doris 字段或 VARIANT 路径。
5. 标识和时间生成规则。
6. 枚举转换表。
7. 一条脱敏的目标事件 JSON。
8. 执行的验证命令和真实结果。
9. OML 输出与当前 Routine Load 的接线差异。
10. 剩余阻塞项和待确认项。

不要输出或修改与 TARGET_LOG_TYPE 无关的 OML，不要顺手重构其他规则。
```

## 首批调用参数

### 进程事件

```text
TARGET_LOG_TYPE=edr_process_event
WRITE_CHANGES=true
```

重点检查：`uuid`、`event_date_creation`、原始 `event_type` 枚举、当前进程与父进程链、`process_id` 和 `pid` 的优先级。

### IP 访问

```text
TARGET_LOG_TYPE=edr_ip_access
WRITE_CHANGES=true
```

重点检查：source/target 网络角色、`dst_port` 字符串转整数、连接方向、`network_connection` 合法 operation。

### 文件审计

```text
TARGET_LOG_TYPE=edr_file_audit
WRITE_CHANGES=true
```

重点检查：文件动作枚举、文件完整路径组合、文件大小单位、上传 URL 和移动存储关联设备。

### 病毒检测

```text
TARGET_LOG_TYPE=edr_antivirus_virus
WRITE_CHANGES=true
```

重点检查：`file_alarm_time`、病毒检测与查杀动作、来源危险等级、终端作为检测目标、文件哈希。

### 来源告警

```text
TARGET_LOG_TYPE=edr_alert_log
WRITE_CHANGES=false
```

当前建议先只分析，不写配置。已知 WPL 没有抽取旧 OML 使用的 `create_time`，无法可靠生成 `occur_time`；`ioc_alerts[0][0]` 还存在数组首项截断。

## 预期产出边界

这个提示词用于生成或重构 OML，不授权以下工作：

- 修改 Doris 表结构。
- 修改 `ldm_alert` 字段。
- 创建或修改 Routine Load。
- 部署 WarpParse。
- 修改 Kafka topic 或 sink。
- 将候选映射登记为已批准标准。

OML 完成后，应单独评审接线差异，再决定是否更新 Routine Load 或输出序列化配置。
