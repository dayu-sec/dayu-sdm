# leadsec / leadsec_vh SDM2 候选样例

事件事实：主机隔离管理操作——管理员 root 将 203.0.113.206 加入黑名单（act=添加，mod=主机隔离），result=0=成功。

- 主体：执行隔离的管理员 → `roles.source.user{name=root}`
- 客体：被隔离主机 → `roles.target.host{ip=203.0.113.206}`
- 载体：无 → `carriers=[]`
- 管理声明：`source_finding_obj{title=dsp_msg, status=act, count}`
- 观察者：来源安全产品

## 证据与限制

- 原始样本：`log-model/examples/leadsec/` 第 16 个非空行。
- WPL 规则：`leadsec_vh`，运行时解析成功。
- 字段映射和枚举为候选，未知枚举保留原值并报告。
- `outcome=success`；result=0 文档枚举含义为成功。
- 顶层 `severity` 为空；来源严重度不机械投影。

## 人工语义复核（Power-V 文档，SR-050）

- 事件事实：主机隔离日志记录将 203.0.113.206 加入黑名单，result=0 的文档枚举含义为成功。
- **event_category：`audit`**（主机隔离是管理员操作记录，非攻击检测告警；与 SR-030 process_log、SR-032 remote_assistance 一致）
- event_type：`network_connection`（黑名单添加的网络隔离语义，候选）
- operation：`空`
- outcome：`success`（result=0=成功）
- 主体/客体/载体：administrator（source.user=root）/ isolated_host（target.host）/ none
- 管理声明：`source_finding_obj`（title=dsp_msg/status=act/count）
- `pri` 仅映射 `log_level`。
- 文档证据：Power-V 192.0.2.120 日志格式手册 VERSION 0.3.0；证据状态 `vendor_confirmed_and_observed`。

## 当前物理注册表迁移

- expected 已按当前 `sdm_event.yaml` 87 字段物理注册表收敛。
- 管理员入 `roles.source.user`；被隔离主机入 `roles.target.host`。
- 管理声明入 `source_finding_obj`（title/status/count）。
