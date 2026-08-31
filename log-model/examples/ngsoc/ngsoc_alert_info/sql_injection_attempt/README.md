# NGSOC SQL 注入攻击企图样例

本目录保存 NGSOC Syslog KV 的真实 SQL 注入告警、WPL 结果和预期 SDM2.0 事件。原始数据来自 `sample.dat:18`。

## 事件事实

NGSOC 检测到 `192.0.2.238` 对 `192.0.2.146:80` 的 HTTP SQL 注入企图，共聚合 `18` 次命中。日志提供多个 URI、域名和源端口，但没有 HTTP 方法、传输协议或阻断结果。

## 主体 / 客体 / 载体

- 主体：来源端点 `192.0.2.238` -> `roles.source.endpoint`
- 客体：目标端点 `192.0.2.146:80` -> `roles.target.endpoint`
- 载体：HTTP 请求上下文 -> `facets.http`；没有进程或会话证据
- 检测主张：`attackerContent/victimContent` 进入 `source_finding.attacker/victim`

## 关键决策

- `record_kind=finding`、`event_domain=threat`。
- `event_type=network_http`，因为来源明确为网页漏洞利用日志且包含 HTTP URI；`operation` 留空，因为当前受控字典不允许为 `network_http` 填动作。
- `attackResult=企图` 写为 `source_finding.attack_result=attempted`；顶层 `outcome=observed`，不把企图误判为成功、失败或阻断。
- `source_finding.behavior=sql_injection` 保存来源检测行为。
- 多 URI、多域名和多源端口均保留集合，不压缩成单个 `target.url.full` 或 `source_port`。
- `dipGeo` 跟随目标 IP；`sipGeo` 为空，不构造攻击方地理信息。

## WPL 缺口

`uri/domain/sport/dport/relevantLogsType` 当前由 WPL 输出为 JSON 风格数组字符串，SDM 装配前需要结构化拆分。缺口详见 `sql_injection_attempt.wpl-missing-fields.json`。

## 未决问题

1. NGSOC 严重度、置信度和处置状态的完整枚举。
2. RFC3164 Syslog 头缺少年份，事件时间使用正文 `timestamp`。

## 候选 finding 字典
- 字典：`qax.ngsoc.device-field-dictionaries.inferred.v1`，状态为 `inferred/partial`，不是厂商确认字典。
- 顶层 `severity=error` 由来源 finding 严重度推测；原值保留在 `source_finding.severity` 和 `source_alert_severity`。
- 顶层 `outcome=observed`：检测到攻击尝试，但不声明动作成功
