# NGSOC SQL 注释字符绕过告警样例
> 现行信封：`*.expected-sdm-event.behavior.json`（07 / 2.0）。
> `*.expected-sdm-event.json` 是中间版 55 列对照，不是新写入目标。
>

原始 Syslog KV 来自仓库 `log-model/models/wpl/ngsoc/sample.dat:26`。NGSOC 声明 `192.0.2.238` 对 `192.0.2.146:80` 发起带 SQL 注释字符绕过的 PostgreSQL `pg_sleep(5)` 注入企图，聚合 `8` 次命中；日志没有 HTTP 方法、传输协议、响应、阻断或 SQL 执行结果。

## 主体 / 客体 / 载体

- 主体：通信源端点 `192.0.2.238`，由 `srcIp` 建立 `roles.source`。
- 客体：通信目标端点 `192.0.2.146:80`，由 `dstIp+dport` 建立 `roles.target`。
- 载体：没有可独立建模的进程、会话或协议实体，`roles.carriers=[]`；URI 集合保存在来源私有扩展。
- 来源声明：`attackerContent/victimContent` 分别进入 `source_finding.attacker/victim`，不与通信角色混作同一来源。

## 关键映射决策

- 事件归一为 `finding/threat/network_http`，`operation` 为空，`outcome=observed`；不将“企图”解释为已执行、失败或已阻断。
- 顶层 `severity=error` 由来源 finding 严重度候选字典推测；Syslog PRI 仅写入 `log_level`。
- `ruleId=[304481]` 与 `ruleName=[SQL注入攻击_注释字符绕过]` 配对写入 `source_finding.rule`；`relevantRuleName=预置-网络探针检测到SQL注入事件` 是关联规则名称，独立保存在 `extensions.source_private.relevant_rule_name`。
- `8` 个源端口保存在 `extensions.source_private.source_ports`，`source_port=null`。
- `8` 个相对 URI 保存在 `request_targets`，不拼造单一 URL；两个域名仅作为 `roles.related`，没有证据将其绑定到目标 IP。
- `killchain=突防利用 -> exploitation`、`attackResult=企图 -> attempted` 只覆盖当前样例值，完整厂商字典仍待确认。
- 上述两个字典字段的厂商原值同时保留在 `extensions.unmapped.killchain_original` 和 `extensions.unmapped.attack_result_original`，便于后续补全字典。
- `attCk=[端点拒绝服务：服务耗竭洪流]` 不是 ATT&CK 技术编号且与 SQL 注入语义冲突，因此仅保留在 `extensions.unmapped.att_ck_original`。
- Syslog 头缺少年份，`update_time=2026-12-18 16:01:09` 是 WPL 推断值；正文 `timestamp=2024-12-18 15:28:09` 在 WPL 输出中仍为 chars，由 SDM 装配按 Asia/Shanghai 转为毫秒事件时间。

## 数据缺口

真实租户、日志 ID、采集时间、解析时间和数据源实例均未提供；除空租户外保持 null。`sipGeo={}` 不构造攻击方 Geo。详细缺口见同名 `wpl-missing-fields.json`。

## 候选 finding 字典
- 字典：`qax.ngsoc.device-field-dictionaries.inferred.v1`，状态为 `inferred/partial`，不是厂商确认字典。
- 顶层 `severity=error` 由来源 finding 严重度推测；原值保留在 `source_finding.severity` 和 `source_alert_severity`。
- 顶层 `outcome=observed`：检测到攻击尝试，但不声明动作成功
