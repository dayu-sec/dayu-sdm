# NGSOC 天眼平台 Nmap 扫描行为样例

原始 JSON 告警来自 `sample.dat:16`。`wpl-check` 对 `ngsoc_threat_alert_send_dp` 实跑成功，输出 138 个字段。来源告警名称为“发现黑客工具Nmap扫描行为”，并观测到 `192.0.2.140:54128` 到 `203.0.113.215:17854` 的网络特征；`packetData` 明确包含 `OPTIONS sip:nm SIP/2.0` 和 `Via: SIP/2.0/TCP`。

## 主体 / 客体 / 载体

- 主体：`192.0.2.140:54128`，通信源端点，并由 `attackerContent` 声明为攻击方。
- 客体：`203.0.113.215:17854`，通信目标端点，并由 `victimContent` 声明为受害方。
- 载体：网络扫描行为；协议 facet 从 packetData 解析为 `TCP`/`SIP`，没有进程、会话或 Nmap 进程身份，`carriers=[]`。

## 关键决策

- `finding/threat/scan_network`，`operation` 留空，顶层 `outcome=observed`。
- `extraFields.appProtocol=UNKNOW` 是厂商哨兵值，原值进入 `extensions.unmapped.app_protocol_original`，不覆盖从 packetData 解析出的 SIP。
- `attackResult=2` 由 NGSOC-4.13.1 厂商字典确认，归一为 `source_finding.attack_result=attempted`。
- `attCk=T1587.004` 作为来源 ATT&CK 技术声明进入 `source_finding.mitre.technique_id`；不据此推断 Nmap 进程。
- 源端 `sipGeo` 为 `保留IP` 和 `0,0` 哨兵值，不写标准 Geo；目标 GeoIP 使用 `dipGeo`。

## 缺口

- Nmap 进程身份、扫描生命周期状态和完整厂商数字字典未提供。
- `packetData` 的 SIP/TCP 解析是受原始载荷支持的派生映射，仍需在运行时解析器中实现。

## 候选 finding 字典
- 字典：`qax.ngsoc.ngsoc_threat_alert_send.vendor_confirmed.v1`，状态为 `vendor_confirmed`，来源格式为 `NGSOC-4.13.1`。
- 顶层 `severity=notice` 由来源 finding 严重度推测；原值保留在 `source_finding.severity` 和 `source_alert_severity`。
- 顶层 `outcome=observed`：按当前设备类型候选字典推测攻击结果
