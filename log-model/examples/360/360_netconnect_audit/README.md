# 360 / 360_netconnect_audit SDM2 候选样例

事件事实：网络连接审计——进程 360hotfix.exe（C:\program files (x86)\360\360safe）从 192.0.2.65:50435 连接 203.0.113.233:8080（protocol=6=TCP），发送 560 字节、接收 211 字节、合计 771 字节。

- 主体：发起进程 → `roles.source.process(360hotfix.exe)`；来源端点 → `roles.source.endpoint(192.0.2.65:50435)`；登录用户 → `roles.source.user(qiushilong)`
- 客体：目标端点 → `roles.target.endpoint(203.0.113.233:8080)`
- 载体：网络协议 → `facets.network.protocol.code=6`；流量 → `facets.network.traffic{bytes_in, bytes_out, total_bytes}`
- 观察者：来源安全产品

## 证据与限制

- 原始样本：`s4-doris/models/wpl/360/sample.dat` 第 9 个非空行。
- WPL 规则：`360_netconnect_audit`，运行时解析成功。
- 字段映射和枚举为候选，未知枚举保留原值并报告。
- `outcome=unknown`；网络连接审计无动作结果字段。
- 顶层 `severity` 为空；来源严重度不机械投影。

## 人工语义复核（360 EPP 文档，SR-048）

- 事件事实：网络连接审计记录进程从源地址端口连接目标地址端口并统计流量。
- event_category：`network`
- event_type：`network_connection`
- operation：`空`
- outcome：`unknown`（网络审计活动，非检测）
- 主体/客体/载体：process / network_endpoint / none
- 审计事实：roles.source.process+endpoint+user / target.endpoint / facets.network.protocol+traffic
- 文档证据：360《终端-EPP-SysLog文档》；当前 WPL 运行样本已命中。

## 当前物理注册表迁移

- expected 已按当前 `sdm_event.yaml` 87 字段物理注册表收敛。
- 源/目标端点入 `roles.source/target.endpoint`；发起进程入 `roles.source.process`。
- 协议与流量入 `facets.network`（registry 已注册路径）。
- `source_finding_obj=null`：网络连接审计活动，非检测告警。
