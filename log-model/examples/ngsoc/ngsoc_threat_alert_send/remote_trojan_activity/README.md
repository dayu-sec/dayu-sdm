# NGSOC 普通远控木马活动事件样例

本目录保存 NGSOC JSON 告警的真实原始样例、WPL 结果和预期 SDM2.0 事件。

## 事件事实

终端 `192.0.2.254:8857` 与外部地址 `203.0.113.121:443` 发生网络通信。NGSOC 将外部地址声明为攻击方、内部终端声明为受害方，并给出“普通远控木马活动事件”检测结论。

## 主体 / 客体 / 载体

- 通信主体：`192.0.2.254:8857`、MAC `00:00:5E:00:53:1E` -> `roles.source.endpoint`
- 通信客体：`203.0.113.121:443`、MAC `00:00:5E:00:53:88` -> `roles.target.endpoint`
- 载体：原始日志没有可确认的进程、会话或传输协议，`carriers=[]`
- 检测主张：攻击方 `203.0.113.121`、受害方 `192.0.2.254` 分别进入 `source_finding.attacker/victim`

`roles.source/target` 描述通信方向，不能为了符合攻击方/受害方结论而交换地址。

## 关键决策

- `record_kind=finding`，因为该日志是 NGSOC 已生成的来源告警。
- 顶层 `log_type=ngsoc_threat_alert_send` 来自接入路由 `ngsoc_threat_alert_send*`；载荷内的 `log_type=ngsoc_alert_info` 是上游载荷分类，保存在 `extensions.source_private.payload_log_type`，两者不得互相覆盖。
- `event_type=network_connection`、`operation=traffic`，因为告警描述明确声明两端发生网络通信，且日志提供源/目标 IP 和端口；“远控木马”是设备检测分类，保留在 `source_finding`，不作为事件动作。
- `commDirection=内到外` 归一为 `facets.network.direction=L2W`。
- `extraFields.smac[0]/dmac[0]` 分别归入通信起点和终点的 `endpoint.mac`，不在 `extensions.source_private` 重复保存。
- `isFromExternal=true`，且外部 `attackerIp` 对应通信目标、内部 `victimIp` 对应通信源，因此攻击方向写入 `source_finding.attack_direction=W2L`；该值不能仅由 `commDirection=内到外` 推导。
- `severity/confidence/attackResult/disposeState` 保留来源值；仅对已有可靠字典的字段做归一，完整字段字典已由 NGSOC-4.13.1 文档确认。
- `sipGeo` 跟随本样例受害方，`dipGeo` 跟随本样例攻击方；不按字段前缀机械归属。
- `extraFields` 只提取端口、MAC 和恶意家族等非空字段，其余内容保留在独立 `raw_log` 原文表（`event_id` 回查）。

## 未决问题

1. NGSOC 严重度、置信度、处置状态和攻击结果的完整枚举。
2. 原始日志未提供明确传输协议，不根据端口 443 推断 TCP 或 HTTPS。

## 候选 finding 字典
- 字典：`qax.ngsoc.ngsoc_threat_alert_send.vendor_confirmed.v1`，状态为 `vendor_confirmed`，来源格式为 `NGSOC-4.13.1`。
- 顶层 `severity=error` 由来源 finding 严重度推测；原值保留在 `source_finding.severity` 和 `source_alert_severity`。
- 顶层 `outcome=success`：按当前设备类型候选字典推测攻击结果
