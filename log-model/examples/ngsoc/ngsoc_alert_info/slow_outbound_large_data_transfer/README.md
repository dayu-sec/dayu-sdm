# NGSOC 内部主机对外慢速传输大量数据告警样例
> 现行信封：`*.expected-sdm-event.behavior.json`（07 / 2.0）。
> `*.expected-sdm-event.json` 是中间版 55 列对照，不是新写入目标。
>

原始 Syslog KV 来自仓库 `log-model/models/wpl/ngsoc/sample.dat:34`。NGSOC 聚合观察到 `198.51.100.180` 向 `192.0.2.133:8200` 的 HTTP 相关内到外流量，并由来源规则定性为“慢速传输大量数据”；日志没有传输字节数、持续时间、速率或阈值。

## 主体 / 客体 / 载体

- 主体：通信源端点 `198.51.100.180`。
- 客体：通信目标端点 `192.0.2.133:8200`。
- 载体：`protocol=[http]` 明确的是应用层协议，进入 `facets.network.application_protocol`；没有进程或会话，`roles.carriers=[]`。
- 来源声明：`attackerContent=[]`、`victimContent=[]`，不构造攻击方或受害方；source/target 只表示通信方向。

## 关键映射决策

- 事件归一为 `finding/network/network_connection`，`operation=traffic`，`outcome=observed`。
- `source_finding.behavior=outbound_large_data_transfer`；`transfer_profile={direction: outbound, speed: slow, volume: large}` 只保存标题中的定性标签，不生成数值测量。
- `commDirection=内到外 -> L2W` 是当前值的局部字典，原值同时保留。
- 十个 `sport` 是聚合流量中的来源端口列表，只保存在扩展，不任取一个投影为 `source_port`；唯一 `dport=8200` 可映射为目标端口。
- `protocol=http` 不等于 TCP/UDP，`network_protocol` 保持 null；`天堤TCP流量日志` 只作为来源关联日志类型保留。
- `sipGeo` 和 `dipGeo` 来自 NGSOC 原始字段，进入通信实体 Geo，不标记为平台富化；源 Geo 不覆盖厂商明确的内到外方向。
- 顶层 `severity=warning` 由来源 finding 严重度候选字典推测；Syslog PRI 仅写入 `log_level`。

## 数据缺口

缺少字节数、持续时间、速率、判定窗口和慢速/大量阈值，不能把厂商标签转成定量网络指标。真实平台上下文未提供。

## 候选 finding 字典
- 字典：`qax.ngsoc.device-field-dictionaries.inferred.v1`，状态为 `inferred/partial`，不是厂商确认字典。
- 顶层 `severity=warning` 由来源 finding 严重度推测；原值保留在 `source_finding.severity` 和 `source_alert_severity`。
- 顶层 `outcome=observed`：标题明确声明已检测到慢速传输大量数据行为
