# SQL注入 · 192.0.2.146

由 `correlation_id` 编组的调查案件，不是 Incident。

- `case_id`: `case_59782e57543384097b85dcfc`
- `correlation_id`: `corr_42aaea032af935ce`
- 成员数: 4

查询聚合见 [`case.detail.json`](case.detail.json)（不是物理表）。成员只放列表投影，点进某条再查该告警的 `alert.detail.json`。`sdm_evidence.json` 只含本案自有证据，成员告警 TRIGGER 仍挂在各告警上。

成员：

- `sql_injection_sleep_function` / `alert_b8394e3bb27f24b31765a384` / SQL注入攻击_SLEEP休眠函数注入
- `sql_injection_attempt` / `alert_27d1706a8d1dbf0cfa17b465` / SQL注入攻击
- `sql_injection_comment_bypass` / `alert_281a9f5389ac9b2cfcb7288e` / SQL注入攻击_注释字符绕过
- `mssql_waitfor_delay_sql_injection` / `alert_d7d70bb58dbddda778c058b6` / MSSQL Waitfor语句SQL注入攻击
