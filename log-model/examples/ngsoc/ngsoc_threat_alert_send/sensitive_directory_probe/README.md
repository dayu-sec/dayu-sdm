# NGSOC 敏感目录/文件探测样例
> 现行信封：`*.expected-sdm-event.behavior.json`（07 / 2.0）。
> `*.expected-sdm-event.json` 是中间版 55 列对照，不是新写入目标。
>

原始 JSON 告警来自 `sample.dat:12`，并已使用 `wpl-check sample --rule-name ngsoc_threat_alert_send_dp` 验证：规则匹配成功，输出 139 个字段。NGSOC 检测到 `192.0.2.201` 对 `198.51.100.157:80` 请求 `/old/swagger.json`，响应码为 `503`。日志证明存在 HTTP 请求和失败响应，但不证明敏感目录或文件已经泄露。

## 主体 / 客体 / 载体

- 主体：`192.0.2.201:34738`，通信源端点。
- 客体：`198.51.100.157:80`，通信目标端点。
- 载体：HTTP 请求/响应上下文进入 `facets.http`；没有进程或会话证据，`carriers=[]`。
- 来源声明的 attacker/victim 与通信 source/target 保持独立且方向不交换。

## 关键决策

- `finding/threat/network_http`，`operation` 留空；目录/文件探测是来源告警标题，不虚构资源读取事实。
- `attackResult=2` 与 `killchain=1` 的厂商数值字典未确认，只将原值保存在 `extensions.unmapped`；`attempted`、`reconnaissance` 仅作为待复核候选，不写标准字段。
- 顶层 `severity=notice` 由来源 finding 严重度候选字典推测；Syslog PRI 仅写入 `log_level`。
- HTTP 方法、路径、User-Agent 和 `503` 响应来自 `extraFields`/`payload`；不从端口反推传输协议。
- 目标 GeoIP 进入 `source_finding.victim.geo`；源 GeoIP 为空，不构造攻击方地理信息。

## 舍弃字段与缺口

- 空数组、展示字段和聚合内部字段不单独落库，原值保留于独立 `raw_log` 原文表（`event_id` 回查）。
- 原始日志没有明确传输协议；完整 NGSOC 数值枚举仍待确认。
- `log_id` 直接投影自 WPL Content；真实 `ingest_time`、`parse_time`、`data_src_instance_id` 未提供，保持 `null`，不得用业务时间或虚构采集器补齐。

## 候选 finding 字典
- 字典：`qax.ngsoc.ngsoc_threat_alert_send.vendor_confirmed.v1`，状态为 `vendor_confirmed`，来源格式为 `NGSOC-4.13.1`。
- 顶层 `severity=notice` 由来源 finding 严重度推测；原值保留在 `source_finding.severity` 和 `source_alert_severity`。
- 顶层 `outcome=observed`：按当前设备类型候选字典推测攻击结果
