# Suricata 行为信封 mapping 草案

状态：`m3_behavior_candidate`。未改冻结契约，未写入 `behavior-cutover-allowlist`。

样本：ENT-RDD-OPS-01 `eve.json`（2026-09-06）。采集是 fluent-bit JSON 包一层，夹具用内层 EVE。WPL 未写。

不复活二代 metadata `log_type=suricata` 整包。

| log_type | mapping_id | 对标 | observation | outcome | 夹具 |
|---|---|---|---|---|---|
| `suricata_alert` | `suricata.suricata_alert.behavior.v1` | topas_ips_attack | detect | observed | `examples/suricata/suricata_alert/` |
| `suricata_dns` | `suricata.suricata_dns.behavior.v1` | sxf_probe.flow_dns | record | observed | `examples/suricata/suricata_dns/` |
| `suricata_http` | `suricata.suricata_http.behavior.v1` | sxf_probe.flow_web | record | observed | `examples/suricata/suricata_http/` |
| `suricata_flow` | `suricata.suricata_flow.behavior.v1` | 会话汇总 | record | observed | `examples/suricata/suricata_flow/` |
| `suricata_fileinfo` | `suricata.suricata_fileinfo.behavior.v1` | 协议文件元数据 | record | observed | `examples/suricata/suricata_fileinfo/` |
| `suricata_anomaly` | `suricata.suricata_anomaly.behavior.v1` | 协议解析异常 | record | observed | `examples/suricata/suricata_anomaly/` |
| `suricata_tls` | `suricata.suricata_tls.behavior.v1` | facets.tls | record | observed | `examples/suricata/suricata_tls/` |

不进行为信封：

| EVE | 原因 |
|---|---|
| `stats` | 引擎计数，无主体/客体；`state` 模型暂缓。夹具仅 raw+README：`examples/suricata/suricata_stats/` |
| `ssh` | 近窗 1 条，`pending_sample` |

约束：`alert.action=allowed` 不得写成 `assertion.conclusion=allow`。`anomaly.event` 不是 IDS signature，不得 `detect`。`flow_id` 不作跨事件关联键。不复活二代整包 `log_type=suricata`。
