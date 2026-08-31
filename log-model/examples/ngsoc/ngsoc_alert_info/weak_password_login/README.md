# NGSOC 弱口令登录样例

本目录保存 NGSOC Syslog KV 告警的真实原始样例、WPL 输出和预期 SDM2.0 事件。

## 事件事实

NGSOC 检测到 `192.0.2.28` 到 `198.51.100.30:28080` 的弱口令登录成功事件。日志没有提供用户名、登录协议、认证方式或来源 UUID。

## 主体 / 客体 / 载体

- 主体：来源端点 `192.0.2.28` -> `roles.source.endpoint`
- 客体：目标端点 `198.51.100.30:28080` -> `roles.target.endpoint`
- 载体：没有协议、进程或会话证据，`carriers=[]`
- 检测主张：`attackerContent/victimContent` 与通信两端一致，进入 `source_finding.attacker/victim`

## 关键决策

- `record_kind=finding`，`event_type=user_login`，因为来源明确声明弱口令登录成功。
- `operation` 留空；缺少远程登录、服务登录等具体方式证据。
- `domain=["198.51.100.30:28080"]` 实际是 IP 与端口，不构造 domain 实体。
- `attackResult=成功` 归一到 `outcome=success`、`source_finding.attack_result=success`。
- `severity=中危`、`confidence=高` 保留在来源检测结论中，不写入 syslog 八级 `event.severity`。
- 原始 Syslog 头没有年份，WPL 将 `Nov 29 09:17:20` 推断为 2026；事件时间使用正文中明确的 `2024-11-29 09:17:13`。

## 未决问题

1. 生产接入层应为 RFC3164 时间补充可信年份。
2. 原始日志缺少 UUID，当前派生 ID 不能完全排除同秒重复告警。
3. 后续样例若提供用户或认证方式，再补充 user 和 authentication 细节。

## 候选 finding 字典
- 字典：`qax.ngsoc.device-field-dictionaries.inferred.v1`，状态为 `inferred/partial`，不是厂商确认字典。
- 顶层 `severity=warning` 由来源 finding 严重度推测；原值保留在 `source_finding.severity` 和 `source_alert_severity`。
- 顶层 `outcome=success`：中文值明确声明成功
