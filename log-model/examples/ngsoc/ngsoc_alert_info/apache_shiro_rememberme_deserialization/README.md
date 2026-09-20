# NGSOC Apache Shiro RememberMe 反序列化漏洞样例
> 现行信封：`*.expected-sdm-event.behavior.json`（07 / 2.0）。
> `*.expected-sdm-event.json` 是中间版 55 列对照，不是新写入目标。
>

本目录保存 NGSOC Syslog 告警的真实原始样例、WPL 结果和预期 SDM2.0 事件。来源样例未携带真实接入上下文，因此 `log_id/ingest_time/parse_time/data_src_instance_id` 保持为空，由运行时接入层赋值。

## 事件事实

NGSOC 声明源地址 `198.51.100.128` 针对目标 `203.0.113.204` 发起 Apache Shiro RememberMe 反序列化漏洞利用企图。日志没有证明代码已经执行成功，也没有证明域名 `ifisp.hnrcc.bank:8008` 解析到该目标 IP。

## 主体 / 客体 / 载体

- 主体：源端点 `198.51.100.128`，同时是 NGSOC 声明的攻击方。
- 客体：目标端点 `203.0.113.204`，同时是 NGSOC 声明的受害方。
- 关联实体：域名 `ifisp.hnrcc.bank`，来源字段为 `domain=["ifisp.hnrcc.bank:8008"]`。
- 载体：缺少协议、HTTP 方法、URI 和会话信息，`carriers=[]`。

## 关键决策

- `record_kind=finding`、`event_domain=threat`。
- `event_type=network_uncategorized`、`operation` 为空；端点可确认，但不能虚构 HTTP 请求或已建立连接。
- `srcIp/dstIp` 只生成事件主体/客体；`attackerContent/victimContent` 独立生成来源检测声明中的攻击方/受害方。
- `domain=ifisp.hnrcc.bank:8008` 保留为关联域名和来源 authority；缺少 DNS 证据时不生成 `target_port` 或受害方端口。
- `attackResult=企图` 映射为 `source_finding.attack_result=attempted`，顶层 `outcome=observed`。
- `killchain=突防利用` 映射为 `source_finding.killchain=exploitation`。
- “反序列化漏洞”和“代码执行”属于来源检测声明，不写成客观的进程执行事实。
- 原始日志没有计数字段，不推断 `source_finding.count=1`。
- 原始日志没有 UUID/seq，`source_original_event_id` 使用完整 raw 载荷哈希，避免同秒同端点告警碰撞。
- Syslog 头没有年份，WPL 的 `update_time=2026-11-28 14:37:53` 只保留审计，不参与业务时间。

## 未决问题

1. NGSOC 严重度、置信度和攻击结果的完整字典。
2. 原始日志未提供协议、HTTP 方法、URI、源端口和网络方向。
3. 真实接入时间、解析时间、日志 ID 和采集实例未随样例提供。

## 候选 finding 字典
- 字典：`qax.ngsoc.device-field-dictionaries.inferred.v1`，状态为 `inferred/partial`，不是厂商确认字典。
- 顶层 `severity=error` 由来源 finding 严重度推测；原值保留在 `source_finding.severity` 和 `source_alert_severity`。
- 顶层 `outcome=observed`：检测到攻击尝试，但不声明动作成功
