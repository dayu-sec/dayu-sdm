# NGSOC 绕过堡垒机登录服务器样例
> 现行信封：`*.expected-sdm-event.behavior.json`（07 / 2.0）。
> `*.expected-sdm-event.json` 是中间版 55 列对照，不是新写入目标。
>

本目录保存 NGSOC Syslog 告警的原始样例、WPL 实跑输出和预期 SDM2.0 事件。NGSOC 声明 `203.0.113.60` 针对 `203.0.113.11` 产生“绕过堡垒机登录服务器”风险，关注内容明确应用层协议为 SSH；日志没有堡垒机地址、账户、认证方式、端口、会话或登录结果。

## 主体 / 客体 / 载体

- 主体：源端点 `203.0.113.60`；`attackerContent` 独立声明其为来源攻击方。
- 客体：目标端点 `203.0.113.11`；`victimContent` 独立声明其为来源受害方。
- 载体：只知道应用层协议 SSH，没有进程、会话或独立服务实体，`carriers=[]`；SSH 落入 `facets.application.name`。
- 关联实体：未提供堡垒机身份或地址，不构造堡垒机实体。

## 关键决策

- 使用 `finding/identity/user_login` 表达来源登录风险分类；不代表已观测到成功登录。
- `attackResult` 为空，顶层 `outcome=unknown`；`operation` 留空，不推断远程登录子类型。
- `ssh` 来自 `attentionValue` 的明确协议标签，作为应用名称保存，不写入表示 TCP/UDP 的 `network_protocol`。
- 顶层 `severity=error` 由来源 finding 严重度候选字典推测；Syslog PRI 仅写入 `log_level`。
- 无 UUID/seq，原始事件 ID使用完整载荷哈希；真实平台上下文未提供。

## 未决问题

1. 堡垒机地址或资产身份，以及目标服务器与堡垒机的关系。
2. 用户账号、认证方式、端口、会话和实际登录/绕过结果。
3. NGSOC 枚举完整字典和平台接入上下文。

## 候选 finding 字典
- 字典：`qax.ngsoc.device-field-dictionaries.inferred.v1`，状态为 `inferred/partial`，不是厂商确认字典。
- 顶层 `severity=error` 由来源 finding 严重度推测；原值保留在 `source_finding.severity` 和 `source_alert_severity`。
- 顶层 `outcome=unknown`：原始日志没有明确的底层动作结果字段或事件事实
