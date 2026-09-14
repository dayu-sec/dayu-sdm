# edr_net_out_log / baidu_tracert 行为信封角色判定

句式：主机 `DESKTOP-OPCF5JG` 外联 `36.112.17.98`（baidu.com）；无进程字段。天擎只记录，无检测断言。

矩阵：网络访问 → 连接发起端 / `network / connect` / 服务、主机或端点。

| 角色 | 判定 | 证据 |
|---|---|---|
| subject | `host` `DESKTOP-OPCF5JG` | 无进程。矩阵「连接发起端」；本条不能造 process。旧 expected 已是 host |
| object | `endpoint` `36.112.17.98` | `net_out_ip`。`outreach_address=baidu.com` 不升第二客体 domain |
| carriers[] | 空 | 无进程载体。`execution_host` 仍 `m3_review` |
| observer | `application` `tianqing` | 采集器 → `meta.data_source.instance_id` |
| observation | `action=record`，无 assertion | `source_finding_obj=null` |

## 迁移裁决（相对旧物理 expected）

- `behavior.layer=network` / `type=flow` / `operation=connect` / `outcome=observed`。旧 `operation=null` 按矩阵补 `connect`。
- `is_ok=0` 无字典，不得当 `failed`；进 `source_private`。
- 顶层 `severity=info` 删除。
- `occur_time` 用 raw/旧 expected `create_time=1617094697` → `2021-03-30T08:58:17Z`。WPL `create_time=1617093149000` 是资产注册时间，不是事件时间，丢弃。
- `subject.host.ip` 用 WPL `report_ip=10.95.89.3`。raw `client_ip=192.168.129.0` 未进 WPL，不写。
- `tracert` 未进 WPL，不落信封。
- `is_down` 未进 WPL，不从 raw 补。
- 资产库存字段（内存/IE/语言等）不进本事件。
- MAC：`00-0C-29-93-93-51` → `00:0c:29:93:93:51`。
- `mapping_id=tianqing.edr_net_out_log.baidu_tracert.behavior.v1`。

旧 `baidu_tracert.expected-sdm-event.json` 保持 interim 物理形，M4 再切投影。
