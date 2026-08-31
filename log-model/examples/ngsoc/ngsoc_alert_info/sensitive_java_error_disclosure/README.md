# NGSOC Java 报错信息泄露告警样例

原始 Syslog KV 来自仓库 `log-model/models/wpl/ngsoc/sample.dat:22`。NGSOC 将 `192.0.2.203` 到两个目标 `192.0.2.238:9090`、`203.0.113.108:9090` 的聚合活动声明为 Java 报错信息泄露告警，共 `121` 次命中。来源同时给出请求目标 `192.0.2.169:9090/service/api/resopencard/updateResOpenCradStatu`，但没有 HTTP 方法、scheme、传输协议、响应内容、阻断动作或信息实际泄露结果。

## 主体 / 客体 / 载体

- 主体：通信源端点 `192.0.2.203`；`attackerContent` 独立声明同一 IP 为攻击方。
- 客体：两个并列受害端点。由于 `roles.target` 为单值，按来源数组顺序将 `192.0.2.238:9090` 作为代表 target，不表达主次；`203.0.113.108:9090` 以 `victim` 关系进入 `roles.related`，完整列表进入 `source_finding.entities.victims`。
- 关联实体：URI authority `192.0.2.169:9090` 与两个受害 IP 均不同，以 `request_authority` 关系独立保留，不推断其与受害端点的拓扑绑定。
- 载体：无进程、会话或可独立建模的协议实体，`roles.carriers=[]`；仅保留明确的 HTTP 请求路径。

## 关键映射决策

- 事件归一为 `finding/threat/network_http`，`operation` 为空，`outcome=unknown`；来源告警不证明信息已经泄露。
- 顶层 `severity=error` 由来源 finding 严重度候选字典推测；Syslog PRI 仅写入 `log_level`。
- `ruleId=[]`，而 `ruleName` 同时包含 Java 报错和 Oracle SQL 错误两个检测规则名，因此使用标准 `source_finding.rules[].name` 保存多规则；`relevantRuleName` 单独保存在 `source_private.relevant_rule_name`。
- `10` 个源端口保存在 `extensions.source_private.source_ports`，不生成单一 `source_port`。
- `attCk=[利用面向公众的应用程序]` 只有中文名称，缺少来源技术 ID；保留在 `extensions.unmapped.att_ck_original`，不推断 ATT&CK 编号。
- `relevantAssetsName/Group/NetworkSegmentId` 是来源关联信息，不冒充平台资产、组织或网络分区富化。

## 数据缺口

真实租户、日志 ID、采集时间、解析时间和数据源实例均未提供；除空租户外保持 null。两个受害 IP 与 URI authority 的真实拓扑关系也未提供。详细缺口见同名 `wpl-missing-fields.json`。

## 候选 finding 字典
- 字典：`qax.ngsoc.device-field-dictionaries.inferred.v1`，状态为 `inferred/partial`，不是厂商确认字典。
- 顶层 `severity=error` 由来源 finding 严重度推测；原值保留在 `source_finding.severity` 和 `source_alert_severity`。
- 顶层 `outcome=unknown`：原始日志没有明确的底层动作结果字段或事件事实
