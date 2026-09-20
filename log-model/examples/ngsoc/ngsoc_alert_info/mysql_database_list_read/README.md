# NGSOC MySQL 读取数据库列表样例
> 现行信封：`*.expected-sdm-event.behavior.json`（07 / 2.0）。
> `*.expected-sdm-event.json` 是中间版 55 列对照，不是新写入目标。
>

本目录保存 NGSOC Syslog 告警的原始样例、WPL 实跑输出和预期 SDM2.0 事件。NGSOC 声明 `203.0.113.91` 针对 `198.51.100.100` 发生“MySQL 读取数据库列表”敏感操作并标记成功，但日志没有端口、协议、SQL、数据库名、列表内容或响应证据。

## 主体 / 客体 / 载体

- 主体：源端点 `203.0.113.91`；`attackerContent` 独立声明其为来源攻击方。
- 客体：目标端点 `198.51.100.100`；`victimContent` 独立声明其为来源受害方。
- 载体：没有进程、协议、端口、会话或独立数据库服务实体，`carriers=[]`。
- 关联实体：无。

## 关键决策

- 使用 `finding/threat/network_uncategorized`；MySQL 和读取数据库列表只作为来源 finding 内容，不生成 `resource_read` 或数据库 facet。
- `attackResult=成功` 映射为 `source_finding.attack_result=success`，顶层 `outcome=success`，不声明数据库列表已被验证读取。
- `killchain=突防利用` 映射为 `exploitation`。
- 顶层 `severity=warning` 由来源 finding 严重度候选字典推测；Syslog PRI 仅写入 `log_level`。
- 无 UUID/seq，原始事件 ID 使用完整载荷哈希；真实平台上下文未提供。

## 舍弃字段

- `symbol=qax.ngsoc:` 是固定解析标记，无独立检索价值，不落库。
- `compromiseState` 为空，不生成失陷状态。
- `ioc`、`domain`、`url` 的 WPL 输出均为空数组字符串，不构造 IOC、域名、URL 或数据库服务实体。

## WPL 与来源缺口

- 当前 WPL 已抽取样例中全部有值的业务字段，没有额外 WPL 抽取缺口。
- 原始日志本身不含数据库名、SQL、返回列表、响应证据、端口、协议、会话或服务信息，因此不能构造数据库读取事实。
- 日志类型识别只使用 `name` 和 `ruleCategoryName`；`srcIp`、`dstIp` 的基数异常只影响对应角色装配，并进入 review。

## 平台上下文与富化

- 样例未提供真实 `tenant_id`、`log_id`、`ingest_time`、`parse_time` 和 `data_src_instance_id`；expected 使用空字符串或 `null`，运行时由接入层赋值。
- 没有资产、组织、系统、GeoIP 等平台富化，`extensions.profiles` 和 `extensions.enrichments` 为空。
- 未命中字典的非空 `killchain`、`attackResult` 原值分别保留到 `extensions.unmapped.killchain`、`extensions.unmapped.attack_result`；当前样例均命中，所以 `extensions.unmapped={}`。

## 未决问题

1. 目标数据库服务、端口、协议和数据库名。
2. SQL 请求、返回列表及响应证据。
3. NGSOC 枚举完整字典和平台接入上下文。

## 候选 finding 字典
- 字典：`qax.ngsoc.device-field-dictionaries.inferred.v1`，状态为 `inferred/partial`，不是厂商确认字典。
- 顶层 `severity=warning` 由来源 finding 严重度推测；原值保留在 `source_finding.severity` 和 `source_alert_severity`。
- 顶层 `outcome=success`：中文值明确声明成功
