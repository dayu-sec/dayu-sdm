# NGSOC 端口扫描样例

本目录保存 NGSOC Syslog 告警的原始样例、WPL 实跑输出和预期 SDM2.0 事件。日志声明源端 `203.0.113.69` 对两个目标 `198.51.100.151`、`203.0.113.23` 产生端口扫描企图，但没有端口、协议、扫描方法或响应结果。

## 主体 / 客体 / 载体

- 主体：源端点 `203.0.113.69`，`attackerContent` 独立声明其为攻击方。
- 客体：两个并列目标端点，来源没有声明主次。由于事件层 `roles.target` 是单值，按来源数组顺序选择第一项作为代表 `target`，不表达语义主次；第二项以 `roles.related[0].relation_type=victim` 保留，完整两个目标同时写入 `source_finding.entities.victims`。
- 载体：缺少协议、进程、会话和扫描方法，`carriers=[]`。

## 关键决策

- 使用 `finding/threat/scan_network`；缺少扫描生命周期状态，`operation` 留空，且没有足够证据生成 `facets.network.scan`。
- `attackResult=企图` 映射为来源声明 `attempted`，顶层 `outcome=observed`。
- `killchain=侦查跟踪` 映射为 `reconnaissance`。
- 顶层 `severity=warning` 由来源 finding 严重度候选字典推测；Syslog PRI 仅写入 `log_level`。
- 无 UUID/seq，原始事件 ID 使用完整载荷哈希；真实平台上下文未提供。

## 未决问题

1. 两个目标的端口、协议、扫描方法和响应结果。
2. 运行时多目标在单值 `roles.target` 投影后的查询约定。
3. NGSOC 枚举完整字典和平台接入上下文。

## 候选 finding 字典
- 字典：`qax.ngsoc.device-field-dictionaries.inferred.v1`，状态为 `inferred/partial`，不是厂商确认字典。
- 顶层 `severity=warning` 由来源 finding 严重度推测；原值保留在 `source_finding.severity` 和 `source_alert_severity`。
- 顶层 `outcome=observed`：检测到攻击尝试，但不声明动作成功
