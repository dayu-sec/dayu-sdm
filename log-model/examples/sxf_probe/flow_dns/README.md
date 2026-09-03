# sxf_probe / flow_dns SDM2 样例

事件事实：客户端对 DNS 服务器发起 PTR 查询；探针记录请求（`qr=0`，无应答）。

- 主体：`endpoint` `192.0.2.199:52040`
- 客体：`endpoint` `192.0.2.123:53`（查询名进 `facets.dns.question`，不升 `domain`）
- 载体：无（DNS/UDP 是协议，不是载体）
- 观察者：`device` `vendor=sangfor`；无观察者 IP，不发明 `device.ip`
- 观察：`action=record`；无 assertion

## 文件

| 文件 | 形态 |
|---|---|
| `runtime_observed.expected-sdm-event.json` | interim 物理五层/投影形（M4 前保留） |
| `runtime_observed.expected-sdm-event.behavior.json` | M3 行为信封（07 Schema） |
| `runtime_observed.behavior-roles.md` | 四角色与 outcome 裁决 |
| `runtime_observed.wpl-to-sdm-event.behavior.json` | M3 行为信封字段映射 |
| `runtime_observed.wpl-to-sdm-event.behavior.md` | 映射评审表 |

## 证据与限制

- 原始样本：`log-model/examples/sxf_probe/` 第 4 个非空行。
- WPL 规则：`flow_dns`。
- `outcome=observed`：请求日志，不是成功响应。旧物理样例的 `success`（`rcode=0` 且 `qr=0`）已纠正，见 `behavior-roles.md`。
- 无 PRI、无检测严重度。
- `data_src_instance_id` 为空。
- `mapping_id=sxf_probe.flow_dns.behavior.v1`。

文档证据：深信服《潜伏威胁探针数据接口对外说明 V2.0》；`logtype=dns_request`。
