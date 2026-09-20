# suricata / suricata_tls SDM2 样例

事件事实：TLS 握手：WAF 访问 nexus.corp.dy-sec.com（TLS 1.3）。

样本：ENT-RDD-OPS-01 `/opt/suricata/logs/eve.json`（2026-09-06，内层 EVE）。当前实时链路进 miss，本夹具补规范。

状态：`m3_behavior_candidate`，未进 allowlist。无 interim 物理五层。WPL/OML 未写。

`mapping_id=suricata.suricata_tls.behavior.v1`。对标 TLS 会话。
