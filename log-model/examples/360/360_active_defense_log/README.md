# 360 / 360_active_defense_log SDM2 候选样例

事件事实：终端主动防御（HIPS）——局域网攻击来源 198.51.100.44（进程 `cat ~/.ssh/`）对受保护终端 TEST-PC-01（risk_ip 203.0.113.19）的检测，hips_type=2=文件防护，hips_desc「360文档保护已经开启」。

- 主体：攻击端点 → `roles.source.endpoint(198.51.100.44)` + `roles.source.process(cat ~/.ssh/)`
- 客体：受保护终端 → `roles.target.host(TEST-PC-01)` + `roles.target.endpoint(203.0.113.19)`
- 载体：无 → `carriers=[]`
- 检测声明：`source_finding_obj{title=hips_desc, count, outcome, original_outcome}`
- 观察者：来源安全产品

## 证据与限制

- 原始样本：`log-model/examples/360/` 第 1 个非空行。
- WPL 规则：`360_active_defense_log`，运行时解析成功。
- 字段映射和枚举为候选，未知枚举保留原值并报告。
- `outcome=unknown`；hips_result_type=0=其他，非明确已阻止/允许。
- 顶层 `severity` 为空；来源严重度不机械投影。

## 人工语义复核（360 EPP 文档，SR-043）

- 事件事实：终端主动防御日志记录风险来源、攻击进程和受保护终端。
- **hips_result_type 枚举已确认**：0=其他、1=已阻止、2=已允许、3=自动允许、4=自动阻止、5=未处理、6=已清除。本条 0=其他。
- **hips_type 枚举已确认**：0=HIPS防护、1=进程防护、2=文件防护、3=注册表防护、4=网络防护、5=DNS防护、6=局域网防护、7=驱动防护。本条 2=文件防护。
- event_category：`alert`
- event_type：`network_connection`（局域网攻击来源语义，候选）
- operation：`空`
- outcome：`unknown`（hips_result_type=0=其他）
- 主体/客体/载体：attack_endpoint / protected_host / none
- 检测声明：`source_finding_obj`（title/count/outcome/original_outcome）
- 文档证据：360《终端-EPP-SysLog文档》；当前 WPL 运行样本已命中。

## 当前物理注册表迁移

- expected 已按当前 `sdm_event.yaml` 87 字段物理注册表收敛。
- 攻击来源入 `roles.source.endpoint+process`；受保护终端入 `roles.target.host+endpoint`。
- 检测声明入 `source_finding_obj`（title/count/outcome/original_outcome）。
