# NGSOC 敏感信息泄露 Java 源码泄露样例
> 现行信封：`*.expected-sdm-event.behavior.json`（07 / 2.0）。
> `*.expected-sdm-event.json` 是中间版 55 列对照，不是新写入目标。
>

本目录保存 NGSOC Syslog 告警的原始样例、WPL 输出和预期 SDM2.0 事件。真实接入上下文未随样例提供，相关字段保持空值。

## 事件事实

NGSOC 声明源端点 `192.0.2.52` 针对目标 `192.0.2.234:8080` 产生“敏感信息泄露_Java源码泄露”告警。日志没有 URL、文件路径、请求方法、响应状态或响应内容，不能断言 Java 源码已经被读取或泄露。

## 主体 / 客体 / 载体

- 主体：源端点 `192.0.2.52`；`attackerContent` 独立声明其为来源告警攻击方。
- 客体：目标端点 `192.0.2.234:8080`；`victimContent` 独立声明目标 IP 为来源告警受害方。
- 关联实体：无。`domain=["192.0.2.234:8080"]` 是与目标 IP 匹配的 authority，用于补充目标端口，不构造 domain 实体。
- 载体：缺少协议、HTTP 请求和会话，`carriers=[]`。

## 关键决策

- 使用 `finding/threat/network_uncategorized`，`operation` 留空。
- `attackResult` 和 `killchain` 均为空，不产生来源攻击结果或杀伤链阶段。
- 顶层 `outcome=unknown` 由缺少底层动作结果证据确定，不把告警标题解释为成功泄露。
- 不创建 HTTP 请求、文件读取、源码对象或成功泄露事实。
- 顶层 `severity=error` 由来源 finding 严重度候选字典推测；Syslog PRI 仅写入 `log_level`。
- 顶层及 extensions 结构版本均为 `1`。
- 无计数字段，不推断 `source_finding.count`。
- 无 UUID/seq，原始事件 ID 使用完整载荷哈希。

## 未决问题

1. NGSOC 严重度和置信度完整字典。
2. HTTP 方法、URL、文件路径、响应状态和响应内容。
3. Java 源码是否实际被读取或泄露。
4. 真实接入时间、日志 ID 和采集实例。

## 候选 finding 字典
- 字典：`qax.ngsoc.device-field-dictionaries.inferred.v1`，状态为 `inferred/partial`，不是厂商确认字典。
- 顶层 `severity=error` 由来源 finding 严重度推测；原值保留在 `source_finding.severity` 和 `source_alert_severity`。
- 顶层 `outcome=unknown`：原始日志没有明确的底层动作结果字段或事件事实
