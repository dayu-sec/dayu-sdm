# NGSOC SQL 注入攻击选择语句样例

本目录保存 NGSOC Syslog 告警的原始样例、WPL 实跑输出和预期 SDM2.0 事件。真实接入上下文未随样例提供，相关字段保持空值。

## 事件事实

NGSOC 声明源端点 `198.51.100.228` 针对目标端点 `198.51.100.208` 产生“SQL注入攻击_选择语句”企图告警。日志没有协议、HTTP 请求、URI、SQL 载荷或数据库响应，不能断言选择语句已经到达或被数据库执行。

## 主体 / 客体 / 载体

- 主体：源端点 `198.51.100.228`；`attackerContent` 独立声明其为来源告警攻击方。
- 客体：目标端点 `198.51.100.208`；`victimContent` 独立声明其为来源告警受害方。
- 关联实体：域名 `ebssweb.hnrcc.bank`。缺少 DNS 证据，不声明它解析到目标 IP。
- 载体：缺少协议、请求、会话和应用信息，`carriers=[]`。

## 关键决策

- 使用 `finding/threat/network_uncategorized`，`operation` 留空。
- `attackResult=企图` 仅映射为来源声明 `attempted`；顶层 `outcome=observed` 由 finding 事件语义确定，不读取来源攻击结果。
- `killchain=突防利用` 映射为 `exploitation`。
- 不创建 HTTP 请求、SQL 载荷、数据库访问或选择语句执行事实。
- 顶层 `severity=error` 由来源 finding 严重度候选字典推测；Syslog PRI 仅写入 `log_level`。
- 顶层及 extensions 结构版本均为 `1`。
- 无计数字段，不推断 `source_finding.count`。
- 无 UUID/seq，原始事件 ID 使用完整载荷哈希。

## 未决问题

1. NGSOC 严重度、置信度、攻击结果和杀伤链完整字典。
2. 域名和目标 IP 的解析或应用归属关系。
3. HTTP 请求、SQL 载荷和数据库响应证据。
4. 真实接入时间、日志 ID 和采集实例。

## 候选 finding 字典
- 字典：`qax.ngsoc.device-field-dictionaries.inferred.v1`，状态为 `inferred/partial`，不是厂商确认字典。
- 顶层 `severity=error` 由来源 finding 严重度推测；原值保留在 `source_finding.severity` 和 `source_alert_severity`。
- 顶层 `outcome=observed`：检测到攻击尝试，但不声明动作成功
