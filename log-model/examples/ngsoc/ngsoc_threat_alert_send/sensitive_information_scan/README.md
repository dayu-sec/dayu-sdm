# NGSOC 敏感信息扫描（机器学习）样例

原始 JSON 告警来自 `sample.dat:13`。`wpl-check` 对 `ngsoc_threat_alert_send_dp` 实跑成功，输出 139 个字段。来源声明 `192.0.2.201` 对 `198.51.100.157:80` 请求 `/WEB-INF/web.xml`，响应码为 `503`；日志证明探测请求和失败响应，不证明敏感信息已经泄露。

## 主体 / 客体 / 载体

- 主体：`192.0.2.201:34162`，通信源端点，并由来源 `attackerContent` 声明为攻击方。
- 客体：`198.51.100.157:80`，通信目标端点，并由来源 `victimContent` 声明为受害方。
- 载体：HTTP 请求/响应进入 `facets.http`；方法、路径和响应码来自 `extraFields`，User-Agent 因 `extraFields.httpUserAgent` 为空而从 `payload.httpReqHeader` 提取，`carriers=[]`。

## 关键决策

- `finding/threat/network_http`，`operation` 留空，顶层 `outcome=observed`。
- `attackResult=2` 由 NGSOC-4.13.1 厂商字典确认，归一为 `source_finding.attack_result=attempted`。
- 顶层 `severity=notice` 由来源 finding 严重度候选字典推测；Syslog PRI 仅写入 `log_level`。
- 目标 GeoIP 进入 `source_finding.victim.geo`；不从端口推断传输协议。

## 缺口

- 真实平台上下文未提供：`ingest_time`、`parse_time`、`data_src_instance_id` 保持 `null`。
- 完整 NGSOC 数值字典和传输协议仍待确认。

## 候选 finding 字典
- 字典：`qax.ngsoc.ngsoc_threat_alert_send.vendor_confirmed.v1`，状态为 `vendor_confirmed`，来源格式为 `NGSOC-4.13.1`。
- 顶层 `severity=notice` 由来源 finding 严重度推测；原值保留在 `source_finding.severity` 和 `source_alert_severity`。
- 顶层 `outcome=observed`：按当前设备类型候选字典推测攻击结果
