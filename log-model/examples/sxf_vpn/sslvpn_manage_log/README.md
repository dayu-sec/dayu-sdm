# sxf_vpn / sslvpn_manage_log SDM2 候选样例

事件事实：本地 IKE 服务 `Isakmp_Server` 与网关 `Sangfor_Azure` 的第一阶段 SA 协商失败，连接未建立。

- 主体：`local_ike_endpoint`（Isakmp_Server，不是 VPN 用户）
- 客体：`vpn_gateway`（Sangfor_Azure，从 msg 抽取）
- 载体：`none`（无 session id）
- 观察者：来源安全产品

## 证据与限制

- 原始样本：`log-model/examples/sxf_vpn/` 第 2 个非空行。
- WPL 规则：`sslvpn_manage_log` 命中 `SVPN-SYSTEM`；规则名是管理日志，样本是系统 IKE 日志。
- `outcome=failed`、角色名称来自 `msg` 中文，证据 `sample_inferred`。
- 仓库仅有 AC 外置 syslog XLSX，与本 JSON 格式不同，只作旁证。
- `logLevel=warn` 只进 `log_level`，不进 `severity`。
- 其他 `SVPN-SYSTEM` 行（如 portal injection）不得套用本条结果。
- logical/physical/projection 校验保持 partial。

## 人工语义复核

- 事件事实：本地 IKE 服务 Isakmp_Server 与网关 Sangfor_Azure 的第一阶段 SA 协商失败，连接未建立。站点 IKE，不是远程用户客户端。无 session id，不编造载体。
- event_category：`network`
- event_type：`network_connection`
- operation：`空`
- outcome：`failed`
- 证据状态：`sample_inferred`
- 状态：`reviewed_sample_inferred`
