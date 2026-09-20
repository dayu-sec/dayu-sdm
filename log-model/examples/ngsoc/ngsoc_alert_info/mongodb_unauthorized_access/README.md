# NGSOC MongoDB 未授权访问样例
> 现行信封：`*.expected-sdm-event.behavior.json`（07 / 2.0）。
> `*.expected-sdm-event.json` 是中间版 55 列对照，不是新写入目标。
>

本目录保存 NGSOC Syslog KV 的真实 MongoDB 未授权访问告警、WPL 结果和预期 SDM2.0 事件。原始数据来自 `sample.dat:21`。

## 事件事实

NGSOC 检测到 `192.0.2.140` 对 `198.51.100.213:27017` 的 MongoDB 未授权访问成功事件，共聚合 `170` 次命中。日志没有提供用户名、认证方式、应用协议或会话标识。

## 主体 / 客体 / 载体

- 主体：来源端点 `192.0.2.140` -> `roles.source.endpoint`
- 客体：目标端点 `198.51.100.213:27017` 及 MongoDB 服务 -> `roles.target`
- 载体：只确认网络通信，缺少进程、会话和协议证据
- 检测主张：`attackerContent/victimContent` 进入 `source_finding.attacker/victim`

## 关键决策

- `event_type=network_connection`、`operation=traffic`，表达可确认的网络通信事实。
- 不映射为 `user_login` 或 `user_resource_access`，因为日志没有用户、认证或具体资源证据。
- “未授权访问”进入 `source_finding.behavior=unauthorized_access`，不替代客观事件类型。
- `attackResult=成功` 归一为顶层 `outcome=success` 和 `source_finding.attack_result=success`。
- `roles.target.service.name=mongodb` 由明确的告警名称和目标端口 27017共同确认，不据端口推断传输协议。
- 多个源端口保留在 `extensions.source_private.source_ports`，不投影虚假的单一 `source_port`。

## WPL 缺口

`sport/dport/relevantLogsType` 当前由 WPL 输出为数组字符串，需要在 SDM 装配前结构化拆分。

## 未决问题

1. NGSOC 严重度、置信度和处置状态的完整枚举。
2. RFC3164 Syslog 头缺少年份，事件时间使用正文 `timestamp`。

## 候选 finding 字典
- 字典：`qax.ngsoc.device-field-dictionaries.inferred.v1`，状态为 `inferred/partial`，不是厂商确认字典。
- 顶层 `severity=error` 由来源 finding 严重度推测；原值保留在 `source_finding.severity` 和 `source_alert_severity`。
- 顶层 `outcome=success`：中文值明确声明成功
