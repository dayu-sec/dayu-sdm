# edr_ip_access / outbound_open 行为信封角色判定

句式：进程 `agent.exe`（pid 2716）出站连接 `203.0.113.25:443`；无检测断言。

对照：`baidu_tracert` 无进程、无端口，主体是 host。本条有进程和五元组。

| 角色 | 判定 | 证据 |
|---|---|---|
| subject | `process` `agent.exe` | 连接发起进程。旧 expected 把 source 标成 host+endpoint 双类型，进程进 carriers |
| object | `endpoint` `203.0.113.25:443` | `dst_ip_addr`/`dst_port`。`dst_host_name` 不升第二类型 host |
| carriers[] | 空 | 发起进程已是 subject。`execution_host` 仍 `m3_review` |
| ancestry | 父 `services.exe` → `facets.process.ancestry[]` | 与文件写入同一路径哈希 |
| network | `protocol=tcp` `direction=outbound`；源 `198.51.100.211:51532` 进 facet | 源地址不是 process 属性；主体已是进程，不能再挂 endpoint |
| observation | `action=record`，无 assertion | `source_finding_obj=null` |

## 迁移裁决

- `behavior.layer=network` / `type=flow` / `operation=connect` / `outcome=observed`。
- 旧 `outcome=success` 纠正：`connection_established` 是事实记录，不是执行分段（字段目录 2.3）。
- 旧 `operation=open` 归一为矩阵 `connect`。
- 顶层 `severity=info` 删除。
- `occur_time` `1734490012000` → `2024-12-18T02:46:52Z`。
- `mapping_id=tianqing.edr_ip_access.outbound_open.behavior.v1`。

旧 `outbound_open.expected-sdm-event.json` 保持 interim 物理形，M4 再切投影。
