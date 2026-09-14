# edr_ip_access / inbound_refuse 行为信封角色判定

句式：外部 `198.51.100.77:55321` 入站连接 `10.95.208.20:3389` 被拒；无检测断言、无策略字段。

对照：`outbound_open` 出站、发起进程可见。本条入站，发起端只有地址。

| 角色 | 判定 | 证据 |
|---|---|---|
| subject | `endpoint` `198.51.100.77` | 连接发起端。无进程信息，不造 process；临时端口 55321 只进 typed object |
| object | `endpoint` `10.95.208.20` | 被连接的受管终端，端口 3389 进 typed object |
| carriers[] | `process` `svchost.exe -k TermService`，`carrier_role=server_process` | 被连接服务由该进程承载。第一张真正使用 carriers 的卡；协议/方向进 facet 不进载体 |
| ancestry | 父 `services.exe` → `facets.process.ancestry[]` | 统一哈希 `process::4370b35e…` |
| network | `protocol=tcp` `direction=inbound` `connection_result=refused` | 拒绝是协议层结果，可查询 facet，不是 outcome |
| observer | `application` `tianqing` | 采集器 → `meta.data_source.instance_id` |
| observation | `action=record`，无 assertion | 无策略/规则字段，不能证明 EDR 处置 |

## 迁移裁决（相对旧物理 expected）

- `behavior.layer=network` / `type=flow` / `operation=connect` / `outcome=observed`。
- 旧 `outcome=failed` 纠正：`connection_refused` 与 `connection_established` 同为协议层结果，与 outbound 卡对称，均 `observed`；拒绝事实进 `facets.network.connection_result`。
- 旧 `operation=refuse` 归一为矩阵 `connect`（行为是连接尝试，refused 是结果）。
- 主体从受管 host 改为外部发起 endpoint；受管终端降为 object。
- 顶层 `severity=info` 删除。
- `occur_time` `1734490098000` → `2024-12-18T02:48:18Z`。
- `mapping_id=tianqing.edr_ip_access.inbound_refuse.behavior.v1`。

旧 `inbound_refuse.expected-sdm-event.json` 保持 interim 物理形，M4 再切投影。
