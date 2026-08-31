# 360 / 360_exthost_netcontrol_illegal_net_log SDM2 候选样例

事件事实：终端网络控制——非法 DNS 联网（illegal_type=dns），终端 zyykylin10（203.0.113.202）访问 www.baidu.com，deal_type=nothing（不处理）。

- 主体：违规联网终端 → `roles.source.host{name=zyykylin10, ip=203.0.113.202}` + `roles.source.endpoint(203.0.113.202, mac)`
- 客体：DNS 域名 → `roles.target.domain{name=www.baidu.com}`
- 载体：无（DNS 语义入 source_finding.rule.label）→ `carriers=[]`
- 检测声明：`source_finding_obj{title, status=deal_type, count, rule.label=illegal_type}`
- 观察者：来源安全产品

## 证据与限制

- 原始样本：`log-model/examples/360/` 第 6 个非空行。
- WPL 规则：`360_exthost_netcontrol_illegal_net_log`，运行时解析成功。
- 字段映射和枚举为候选，未知枚举保留原值并报告。
- `outcome=unknown`；deal_type=nothing=不处理，不解释为允许或成功。
- 顶层 `severity` 为空；来源严重度不机械投影。

## 人工语义复核（360 EPP 文档，SR-045）

- 事件事实：终端网络控制日志记录非法 DNS 联网；deal_type=nothing 不解释为允许或成功。
- **deal_type 枚举已确认**：nothing=不处理、isolate=隔离。本条 nothing。
- event_category：`alert`
- event_type：`network_connection`
- operation：`空`
- outcome：`unknown`（deal_type=nothing=不处理）
- 主体/客体/载体：endpoint_host / domain / dns（illegal_type=dns）
- 检测声明：`source_finding_obj`（title/status/count/rule.label）
- 文档证据：360《终端-EPP-SysLog文档》；当前 WPL 运行样本已命中。

## 当前物理注册表迁移

- expected 已按当前 `sdm_event.yaml` 87 字段物理注册表收敛。
- 违规终端入 `roles.source.host+endpoint`；DNS 域名入 `roles.target.domain`。
- 检测声明入 `source_finding_obj`（title/status/count/rule.label）。
