# 告警模型样例

| 目录 | 说明 |
|---|---|
| [reverse_shell/](reverse_shell/) | 规则引擎 `DETECTION` 写入形状（手写；含 Alert / Case 两类证据） |
| [ngsoc_alert_info/](ngsoc_alert_info/) | NGSOC `sdm_event` finding 导入为 `SOURCE_ALERT`（22 条，脚本生成） |
| [ngsoc_alert_info/sql_injection_attempt/alert.detail.json](ngsoc_alert_info/sql_injection_attempt/alert.detail.json) | 告警详情查询聚合（读模型） |
| [ngsoc_alert_info/cases/sql_injection_11_1_68_18/case.detail.json](ngsoc_alert_info/cases/sql_injection_11_1_68_18/case.detail.json) | 案件详情查询聚合（读模型） |
