# sxf_vpn / sslvpn_user_log SDM2 候选样例

事件事实：远程用户 `gyzcxt006` 从访问 IP `198.51.100.3` 成功注销 SSL VPN。

- 主体：`user`（gyzcxt006 / 198.51.100.3）
- 客体：`none`（日志无网关标识）
- 载体：`none`（无 session id）
- 观察者：来源安全产品

## 证据与限制

- 原始样本：`s4-doris/models/wpl/sxf_vpn/sample.dat` 第 1 个非空行。
- WPL 规则：`sslvpn_user_log` 命中，但未抽 `userInfo.userName`、`clientInfo.ip`、`clientInfo.vip`。
- `source_user` / 角色用户名来自原始 JSON，记入 `wpl-missing-fields.json`。
- `source_ip` 来自 `msg` 的 accessIP。
- `clientInfo.vip=192.0.2.54` 与 `msg virtualIP=192.0.2.31` 并存，不静默合并。
- `logSubType=logout`、`actionResult=success` 支撑 `user_logout` / `success`，证据 `sample_inferred`。
- AC「登陆注销」表字段不同，只作旁证。
- 未知 `logSubType` 不得套用本条结果。
- logical/physical/projection 校验保持 partial。

## 人工语义复核

- 事件事实：远程用户 gyzcxt006 从 198.51.100.3 成功注销 SSL VPN。无网关标识、无 session id。
- event_category：`auth`
- event_type：`user_logout`
- operation：`remote_service`
- outcome：`success`
- 证据状态：`sample_inferred`
- 状态：`reviewed_sample_inferred`
