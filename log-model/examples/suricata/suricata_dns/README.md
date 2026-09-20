# suricata / suricata_dns SDM2 样例

事件事实：DNS 请求：WarpAxis 向腾讯云 DNS 查询 ntpupdate.tencentyun.com A。

样本：ENT-RDD-OPS-01 `/opt/suricata/logs/eve.json`（2026-09-06，内层 EVE；fluent-bit 外包未写入夹具）。

- 主体/客体：通信五元组 endpoint（VXLAN 外层不升角色）
- 观察者：`device` vendor=`oisf` ip=`203.0.113.28`（OPS Suricata）；采集器走 `meta.data_source.instance_id=fluent_bit_tcp`
- 状态：`m3_behavior_candidate`，**未**写入切流 allowlist
- 无 interim 物理五层 expected（直接行为信封）
- WPL/OML 未写

`mapping_id=suricata.suricata_dns.behavior.v1`。对标 `sxf_probe.flow_dns`。
