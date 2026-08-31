# NGSOC VPN 多物理地址登录成功告警样例

原始 Syslog KV 来自仓库 `s4-doris/models/wpl/ngsoc/sample.dat:40`。NGSOC 声明用户 `秦锦` 在 12 小时内从两个 IP、两个 MAC 登录 VPN 成功；这是聚合 finding，不是两条可独立还原的 VPN 登录 activity。

## 主体 / 客体 / 载体

- 主体：用户 `秦锦`，来自 `userName`；投影为 `source_user`。
- 客体：标题明确指向 VPN 服务，但 `dstIp` 为空且两个关联资产没有登录关联键，因此仅建立通用 `VPN` service，不绑定具体网关。
- 载体：认证行为由 `facets.authentication` 表达；没有会话 ID、进程或独立载体实体，`roles.carriers=[]`。
- 关联实体：`attackerContent` 在此日志类型中是交替的 IP/MAC 列表，与 `srcIp` 顺序一致后配成两个 `login_source` endpoint，并按 IP 关联 `sipGeo`。

## 关键映射决策

- 事件归一为 `finding/identity/user_login`，`operation=remote`，顶层 `outcome=success`。
- `facets.authentication.auth_result=success` 来自标题“登录成功”和 `eventType=login` 的联合局部字典；它不把 finding 顶层结果改成 success。
- `authType=[auth_local_pass|auth_hid|auth_emm]` 是一个来源组合值，直接进入 `auth_type`，同时保留原值；完整厂商字典仍待确认。
- `authType` 内部的 `|` 属于字段值，WPL 解析 KV 时只能在下一个 `字段名=` 前切分，不能把每个 `|` 都当作字段分隔符。
- `attackerContent` 不构造攻击方，因为该字段在本日志类型中混合保存登录来源 IP 和 MAC。
- 两个 `devIp` 作为 observer 地址数组保存，不任取一个投影为主设备 IP；两个 `relevantAssetsName` 只作为来源关联资产保留。
- `commDirection=未知` 不归一为网络方向，仅保留原值。
- 顶层 `severity=warning` 由来源 finding 严重度候选字典推测；Syslog PRI 仅写入 `log_level`。

## 数据缺口

缺少两次登录各自的时间、会话、账号 UID、原始 VPN 日志以及登录到具体网关的关联关系，因此不能拆分 activity，也不能将两个关联资产任意指定为目标。真实平台上下文未提供。

## 候选 finding 字典
- 字典：`qax.ngsoc.device-field-dictionaries.inferred.v1`，状态为 `inferred/partial`，不是厂商确认字典。
- 顶层 `severity=warning` 由来源 finding 严重度推测；原值保留在 `source_finding.severity` 和 `source_alert_severity`。
- 顶层 `outcome=success`：标题明确声明登录成功，且 eventType=login
