# topas_waf / topas_waf_tamper SDM2 候选样例

事件事实：WAF 网页防篡改检测——受保护站点 test（服务器 198.51.100.54）的 `/config` 文件被删除。recorder=waf_tamper，event=1。

- 主体：无（防篡改检测无主动攻击者主体）
- 客体：受保护资源 → `roles.target.host{name=test, ip=198.51.100.54}` + `roles.target.file{path=/config}`
- 载体：无 → `carriers=[]`
- 检测声明：`source_finding_obj{title, count, action=file_delete, rule.label=domain}`
- 观察者：来源安全产品

## 证据与限制

- 原始样本：`s4-doris/models/wpl/topas_waf/sample.dat` 第 3 个非空行。
- WPL 规则：`topas_waf_tamper`，运行时解析成功。
- 字段映射和枚举为候选，未知枚举保留原值并报告。
- `outcome=unknown`；event=1 是检测事件类型，非底层文件动作结果。
- 顶层 `severity` 为空；`log_level=warning` 仅来自 pri，不作为安全严重度。

## 人工语义复核（waf2.0 文档，SR-042）

- 事件事实：WAF 记录受保护站点文件的网页防篡改检测事件。
- **event 枚举已确认**：waf 文档 TABLE 4 `event` 1=文件删除、2=文件添加、4=文件篡改、9=文件删除|恢复、12=文件篡改|恢复、16=签名错误、18=文件添加|签名错误。本条 event=1=文件删除。
- event_category：`alert`
- event_type：`generic_event`（06 无网页防篡改专用类型；可用 file_deletion 候选待评估）
- operation：`空`
- outcome：`unknown`（不将来源处置或 HTTP 状态机械映射为底层动作结果）
- `log_level=warning`：仅来自 `pri`，不作为安全严重度。
- 主体/客体/载体：none / protected_web_resource（target.host + target.file）/ none
- 检测声明：`source_finding_obj`（title/count/action=file_delete/rule.label=domain）
- 证据：天融信《waf2.0日志格式文档-v2.0》TABLE 4，`recorder=waf_tamper`，WPL 运行样本已命中。

## 当前物理注册表迁移

- expected 已按当前 `sdm_event.yaml` 87 字段物理注册表收敛。
- 受保护站点文件入 `roles.target.file.path`；服务器入 `roles.target.host`。
- 检测声明入 `source_finding_obj`（title/count/action/rule.label）。
