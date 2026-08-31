# NGSOC SQL 注入点探测告警样例

原始 Syslog KV 来自仓库 `log-model/models/wpl/ngsoc/sample.dat:43`。NGSOC 声明 `203.0.113.183` 对 `192.0.2.240:9920` 发起 SQL 注入点探测告警，聚合 `71` 次命中；日志只提供 URI `/rest/query/_q`，没有 HTTP 方法、传输协议、响应或注入执行结果。

## 主体 / 客体 / 载体

- 主体：通信源端点 `203.0.113.183`，由 `srcIp` 建立 `roles.source`。
- 客体：通信目标端点 `192.0.2.240:9920`，由 `dstIp+dport` 建立 `roles.target`。
- 载体：没有可独立建模的进程、会话或协议实体，`roles.carriers=[]`；URI 集合保存在来源私有扩展。
- 来源声明：`attackerContent/victimContent` 分别进入 `source_finding.attacker/victim`，不与通信角色混作同一来源。

## 关键映射决策

- 事件归一为 `finding/threat/network_http`，`operation` 为空，`outcome=observed`；不将“企图”解释为注入执行成功、失败或已阻断。
- 顶层 `severity=error` 由来源 finding 严重度候选字典推测；Syslog PRI 仅写入 `log_level`。
- `ruleId=[304325]` 与 `ruleName=[SQL注入攻击_注入点探测]` 配对写入 `source_finding.rule`；`relevantRuleName=预置-网络探针检测到SQL注入事件` 是关联规则名称，独立保存在 `extensions.source_private.relevant_rule_name`。
- `10` 个源端口保存在 `extensions.source_private.source_ports`，`source_port=null`。
- `1` 个相对 URI 保存在 `request_targets`，不拼造完整 URL；域名字段仅作为 `roles.related`，不声明 DNS 绑定关系。
- `killchain=突防利用 -> exploitation`、`attackResult=企图 -> attempted` 只覆盖当前样例值，完整厂商字典仍待确认。
- 上述两个字典字段的厂商原值同时保留在 `extensions.unmapped.killchain_original` 和 `extensions.unmapped.attack_result_original`，便于后续补全字典。
- `attCk=[端点拒绝服务：服务耗竭洪流]` 不是 ATT&CK 技术编号且与当前 SQL 注入分类不一致，因此仅保留在 `extensions.unmapped.att_ck_original`。
- `dipGeo={}` 且 `sipGeo={}`，没有可信 Geo 信息，不构造攻击方或受害方 Geo。
- Syslog 头缺少年份，`update_time=2026-12-18 16:01:51` 是 WPL 推断值；正文 `timestamp=2024-12-18 00:01:49` 在 WPL 输出中仍为 chars，由 SDM 装配按 Asia/Shanghai 转为毫秒事件时间。

## 数据缺口

真实租户、日志 ID、采集时间、解析时间和数据源实例均未提供；除空租户外保持 null。`sipGeo={}` 不构造攻击方 Geo。详细缺口见同名 `wpl-missing-fields.json`。

## 候选 finding 字典
- 字典：`qax.ngsoc.device-field-dictionaries.inferred.v1`，状态为 `inferred/partial`，不是厂商确认字典。
- 顶层 `severity=error` 由来源 finding 严重度推测；原值保留在 `source_finding.severity` 和 `source_alert_severity`。
- 顶层 `outcome=observed`：检测到攻击尝试，但不声明动作成功
