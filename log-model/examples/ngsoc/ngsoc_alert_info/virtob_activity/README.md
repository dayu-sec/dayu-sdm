# NGSOC Virtob 网络蠕虫 DNS 告警样例

原始 Syslog KV 来自仓库 `log-model/models/wpl/ngsoc/sample.dat:45`。NGSOC 观测 `203.0.113.159` 与 `192.0.2.179` 的 DNS 相关通信，域名 IOC 为 `fei9988.3322.org`，恶意家族为 `Virtob`，聚合 `60` 次命中；没有 DNS 应答、传输协议或蠕虫传播成功证据。

## 主体 / 客体 / 载体

- 主体：通信源端点 `203.0.113.159`，也是来源 `victimContent` 声明的受害主机。
- 客体：DNS 通信对端 `192.0.2.179`，无端口证据，不构造端口。
- 载体：协议字段明确为 DNS；没有请求/响应方向、进程或会话，域名仅作为关联实体和来源 IOC 保留，`roles.carriers=[]`。
- 来源声明：`attackerContent=[]`，不构造攻击方实体；`dipGeo` 仅作为通信目标 Geo 扩展保留。

## 关键映射决策

- 事件归一为 `finding/threat/network_dns`，`operation=traffic`，`outcome=observed`；没有请求/响应方向证据，不赋值 `query` 或 `response`。
- 顶层 `severity=error` 由来源 finding 严重度候选字典推测；Syslog PRI 仅写入 `log_level`。
- `ruleId` 为空字符串，仅将 `ruleName=Virtob` 作为来源规则名称；`relevantRuleName` 独立保存。
- `killchain=通信控制 -> command_and_control`、`attackResult=企图 -> attempted`、`compromiseState=已失陷 -> compromised` 只覆盖当前值，原值同时保留。
- 上述三个来源 finding 字典字段的原值分别保存在 `extensions.unmapped.killchain_original`、`attack_result_original` 和 `compromise_state_original`；`commDirection` 原值保存在 `comm_direction_original`，便于后续补全字典。
- `attCk` 为空，不构造 ATT&CK 技术实体。
- Syslog 头缺少年份，`update_time=2026-12-18 16:01:53` 是 WPL 推断值；正文 `timestamp=2024-12-18 00:01:33` 在 WPL 输出中仍为 chars，由 SDM 装配按 Asia/Shanghai 转为毫秒事件时间。

## 数据缺口

真实租户、日志 ID、采集时间、解析时间和数据源实例均未提供；除空租户外保持 null。详细缺口见同名 `wpl-missing-fields.json`。

## 候选 finding 字典
- 字典：`qax.ngsoc.device-field-dictionaries.inferred.v1`，状态为 `inferred/partial`，不是厂商确认字典。
- 顶层 `severity=error` 由来源 finding 严重度推测；原值保留在 `source_finding.severity` 和 `source_alert_severity`。
- 顶层 `outcome=observed`：检测到攻击尝试，但不声明动作成功
