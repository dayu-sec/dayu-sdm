# NGSOC 目录列表泄露样例

本目录保存 NGSOC Syslog 告警的真实原始样例、WPL 结果和预期 SDM2.0 事件。来源样例未携带真实接入上下文，因此 `log_id/ingest_time/parse_time/data_src_instance_id` 保持为空，由运行时接入层赋值。

## 事件事实

NGSOC 声明源端点 `203.0.113.176` 针对目标端点 `192.0.2.2` 产生“目录列表泄露”告警。日志中的 `attackResult=成功` 是设备检测结论，不足以证明目标目录内容确实被读取或泄露。

## 主体 / 客体 / 载体

- 主体：源端点 `203.0.113.176`；同时由 `attackerContent` 独立声明为来源告警中的攻击方。
- 客体：目标端点 `192.0.2.2`；同时由 `victimContent` 独立声明为来源告警中的受害方。
- 载体：缺少协议、HTTP 方法、会话和规范化 URI，`carriers=[]`。
- 关联实体：无。`domain=["192.0.2.2"]` 是与 `dstIp` 重复的 IP 值，不构造 domain 实体。

## 关键决策

- `record_kind=finding`、`event_domain=threat`、`event_type=network_uncategorized`，`operation` 为空。
- `srcIp/dstIp` 生成事件 source/target；`attackerContent/victimContent` 独立生成 `source_finding.attacker/victim`，不因值相同而合并来源。
- `attentionValue=URI资源 : /` 只保存在 `source_finding.attention.content`，不虚构 HTTP 请求、URL 或 URI facet。
- `attackResult=成功` 映射为 `source_finding.attack_result=success`；顶层 `outcome=success`。
- `killchain=侦查跟踪` 映射为 `source_finding.killchain=reconnaissance`。
- 顶层 `severity=error` 由来源 finding 严重度候选字典推测；Syslog PRI 仅写入 `log_level`。
- 顶层及 `extensions_obj` 的 `schema_version=1`，与当前五层逻辑事件契约一致。
- 原始日志没有计数字段，不推断 `source_finding.count=1`。
- 原始日志没有 UUID/seq，`source_original_event_id` 使用完整 raw 载荷哈希。
- Syslog 头没有年份，WPL 的 `update_time=2026-11-29 09:17:17` 只用于审计，不参与业务时间。

## 未决问题

1. NGSOC 严重度、置信度、攻击结果和杀伤链的完整字典。
2. 原始日志未提供协议、HTTP 方法、规范化 URI、源端口和网络方向。
3. 真实接入时间、解析时间、日志 ID 和采集实例未随样例提供。

## 候选 finding 字典
- 字典：`qax.ngsoc.device-field-dictionaries.inferred.v1`，状态为 `inferred/partial`，不是厂商确认字典。
- 顶层 `severity=error` 由来源 finding 严重度推测；原值保留在 `source_finding.severity` 和 `source_alert_severity`。
- 顶层 `outcome=success`：中文值明确声明成功
