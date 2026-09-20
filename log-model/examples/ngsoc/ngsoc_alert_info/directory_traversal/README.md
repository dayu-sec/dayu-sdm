# NGSOC 目录遍历告警样例
> 现行信封：`*.expected-sdm-event.behavior.json`（07 / 2.0）。
> `*.expected-sdm-event.json` 是中间版 55 列对照，不是新写入目标。
>

原始 Syslog KV 来自仓库 `log-model/models/wpl/ngsoc/sample.dat:52`。NGSOC 声明 `192.0.2.26` 对 `198.51.100.139:17001` 发起目录遍历告警，聚合 `2` 次命中；日志只提供 URI `/hnnx/poserver.zz`，没有 HTTP 方法、传输协议、响应或读取成功结果。

## 主体 / 客体 / 载体

- 主体：通信源端点 `192.0.2.26`，由 `srcIp` 建立 `roles.source`。
- 客体：通信目标端点 `198.51.100.139:17001`，由 `dstIp+dport` 建立 `roles.target`。
- 载体：没有可独立建模的进程、会话或协议实体，`roles.carriers=[]`；URI 集合保存在来源私有扩展。
- 来源声明：`attackerContent/victimContent` 分别进入 `source_finding.attacker/victim`，不与通信角色混作同一来源。

## 关键映射决策

- 事件归一为 `finding/threat/network_http`，`operation` 为空，`outcome=observed`；不将“企图”解释为目录读取成功、失败或已阻断。
- 顶层 `severity=warning` 由来源 finding 严重度候选字典推测；Syslog PRI 仅写入 `log_level`。
- `ruleId=[5520]` 与 `ruleName=[目录遍历攻击(通用)]` 配对写入 `source_finding.rule`；`relevantRuleName=升级-预置-网络探针检测到目录遍历事件` 是关联规则名称，独立保存在 `extensions.source_private.relevant_rule_name`。
- `2` 个源端口保存在 `extensions.source_private.source_ports`，`source_port=null`。
- `1` 个相对 URI 保存在 `request_targets`，不拼造完整 URL；域名字段仅作为 `roles.related`，不声明 DNS 绑定关系。
- `killchain=突防利用 -> exploitation`、`attackResult=企图 -> attempted` 只覆盖当前样例值，完整厂商字典仍待确认。
- 上述两个字典字段的厂商原值同时保留在 `extensions.unmapped.killchain_original` 和 `extensions.unmapped.attack_result_original`，便于后续补全字典。
- `attCk=[利用面向公众的应用程序]` 不是 ATT&CK 技术编号，因此仅保留在 `extensions.unmapped.att_ck_original`。
- `dipGeo` 的地区名称保留，但 `latitude=0.0`、`longitude=0.0` 视为哨兵值，省略标准坐标。
- Syslog 头缺少年份，`update_time=2026-12-18 16:02:00` 是 WPL 推断值；正文 `timestamp=2024-12-18 09:54:52` 在 WPL 输出中仍为 chars，由 SDM 装配按 Asia/Shanghai 转为毫秒事件时间。

## 数据缺口

真实租户、日志 ID、采集时间、解析时间和数据源实例均未提供；除空租户外保持 null。`sipGeo={}` 不构造攻击方 Geo。详细缺口见同名 `wpl-missing-fields.json`。

## 候选 finding 字典
- 字典：`qax.ngsoc.device-field-dictionaries.inferred.v1`，状态为 `inferred/partial`，不是厂商确认字典。
- 顶层 `severity=warning` 由来源 finding 严重度推测；原值保留在 `source_finding.severity` 和 `source_alert_severity`。
- 顶层 `outcome=observed`：检测到攻击尝试，但不声明动作成功
