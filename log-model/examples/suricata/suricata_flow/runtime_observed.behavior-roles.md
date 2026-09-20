# suricata_flow / runtime_observed 行为信封角色判定

句式：`192.0.2.128:2750` UDP 到 `203.0.113.28:4789`（VXLAN），1 包后 timeout；探针记 flow 汇总。

| 角色 | 判定 | 证据 |
|---|---|---|
| subject | `endpoint` `192.0.2.128:2750` | src_* |
| object | `endpoint` `203.0.113.28:4789` | dest_*。虽与观察者同 IP，通信对端仍是 endpoint，不升 observer |
| carriers[] | 空 | UDP 进 facets.network |
| observer | `device` oisf / 203.0.113.28 | 与 object IP 相同是镜像拓扑，身份不合并 |
| observation | record，无 assertion | 会话记录不是检测 |

## 迁移裁决

- `behavior.type=flow` / `operation=connect` / `outcome=observed`。
- `state=new` 不是 connection_result=established。
- 字节计数进 source_private。

`mapping_id=suricata.suricata_flow.behavior.v1`。
