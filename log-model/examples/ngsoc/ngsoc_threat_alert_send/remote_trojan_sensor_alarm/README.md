# NGSOC SkyEye 平台普通远控木马告警样例
> 现行信封：`*.expected-sdm-event.behavior.json`（07 / 2.0）。
> `*.expected-sdm-event.json` 是中间版 55 列对照，不是新写入目标。
>

原始 JSON 告警来自 `sample.dat:14`，`wpl-check` 对 `ngsoc_threat_alert_send_dp` 实跑成功，输出 144 个字段。观测到 `192.0.2.254:24617` 到 `203.0.113.121:443` 的网络通信；来源告警声明外部地址为 attacker、内部地址为 victim，但没有 HTTP、进程或传输协议证据。

## 主体 / 客体 / 载体

- 通信主体：`192.0.2.254:24617`，带 MAC，进入 `roles.source`。
- 通信客体：`203.0.113.121:443`，带 MAC，进入 `roles.target`。
- 来源声明：`attackerContent=203.0.113.121`、`victimContent=192.0.2.254`，进入 `source_finding`，不交换通信 source/target。
- 载体：无可确认进程、会话或协议，`carriers=[]`，不生成 HTTP facet。

## 关键决策

- `finding/threat/network_connection`，`operation=traffic`，顶层 `outcome=success`。
- IOC `203.0.113.121:443` 和恶意家族 `Generic Trojan` 保留在 `source_finding`。
- `attackResult=1` 由 NGSOC-4.13.1 厂商字典确认，归一为 `source_finding.attack_result=success`。
- 目标 GeoIP跟随来源 attacker；源端保留保留 IP GeoIP，不把端口 443 推断为 TCP/HTTPS。

## 候选 finding 字典
- 字典：`qax.ngsoc.ngsoc_threat_alert_send.vendor_confirmed.v1`，状态为 `vendor_confirmed`，来源格式为 `NGSOC-4.13.1`。
- 顶层 `severity=error` 由来源 finding 严重度推测；原值保留在 `source_finding.severity` 和 `source_alert_severity`。
- 顶层 `outcome=success`：按当前设备类型候选字典推测攻击结果
