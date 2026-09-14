# ADR-014 证据按主体挂载，Case 可直挂事实指针

- 状态：已接受
- 日期：2026-08-18
- 修订：[ADR-012](ADR-012-stable-evidence-cite.md)（租户内唯一 `evidence_id` 与只追加 cite 仍有效；归属从「必挂告警」改为 ALERT | CASE 二选一）

## 背景

v0.2 前半把证据做成告警子表：`sdm_alert_evidence.alert_id` 必填，`evidence_id` 哈希含 `alert_id`，cite 也强制记 `alert_id`。Case 成员只有告警。调查中新找到的日志、情报、人工输入不能成为 Case 自己的证据，只能寄生到某条成员告警上，或再造一条假检出。

Case 是工作单元，不是事实源。把 `event_ids` 塞进 `sdm_case`，或给不可变的 `sdm_event_behavior` 加 `case_id`，都会把调查过程写进错误的对象。

新系统无需兼容旧表名。

## 选项

1. 维持证据只挂告警。调查附件继续寄生在成员告警上。
2. `sdm_case` 增加 `event_ids` 数组，或给 `sdm_event_behavior` 增加 `case_id`。
3. 证据泛化为主体关系：`sdm_evidence.subject_type = ALERT | CASE`，ALERT 与 CASE 二选一。分析 cite 记来源主体快照，不强制 `alert_id`。

## 决定

选 3。

```
Alert ──▶ Evidence ──▶ Event
Case  ──▶ Evidence ──▶ Event
Case Analysis ──▶ Cite ──▶ 任意 Evidence
```

1. 表改名为 `sdm_evidence`、`sdm_analysis_citation`。主键仍是 `(tenant_id, evidence_id)` 与 `(tenant_id, analysis_id, evidence_id)`。
2. `subject_type` 必填，取值 `ALERT` / `CASE`。`alert_id` 与 `case_id` 条件必填且互斥：ALERT 必须有 `alert_id`、`case_id` 为空；CASE 必须有 `case_id`、`alert_id` 为空。Doris 不强制 XOR，由写入服务校验。
3. 检出触发与检出上下文仍挂在 Alert 下。Case 通过成员告警读取，**不把同一条 TRIGGER 再挂一遍**。
4. 调查过程新增的日志、威胁情报、资产、人工输入挂在 Case 下。`TRIGGER` 只允许 `subject_type=ALERT`。
5. 证据仍只保存事实指针、角色和摘要，不复制事件正文。禁止 `sdm_case.event_ids`，禁止 `sdm_event_behavior.case_id`。
6. 同一 Event 被 Alert 与 Case 各自引用时写两行，两个 `evidence_id`。哈希含主体：

   `ev_` + `sha256(tenant_id || 0x1F || subject_type || 0x1F || subject_id || 0x1F || evidence_type || 0x1F || fact_key || 0x1F || role)` 前 24 位十六进制。

   `subject_id`：ALERT 用 `alert_id`，CASE 用 `case_id`。`fact_key` 规则同 ADR-012。
7. `sdm_analysis_citation` 的来源快照是 `evidence_subject_type` + 对应的 `alert_id` / `case_id`，加上当时的指针摘要。案件轮可以同时引用 Alert 证据和 Case 证据。cite 上的主体是证据归属，不是分析行自己的 `subject_type`。
8. 成员关系不变：Case 工作项仍是告警（`sdm_alert.case_id`）。证据是引用关系，不是成员。

## 后果

- 告警详情查 `subject_type=ALERT AND alert_id=?`。
- 案件自有证据查 `subject_type=CASE AND case_id=?`。
- 案件可见证据 = 成员告警的 Alert 证据 ∪ 本案 Case 证据。
- 归档：Alert 证据随告警；Case 证据随案件。未归档分析仍引用的证据行先留，或接受 cite 摘要自足（同 ADR-012）。
- 案件合并或成员迁移不改已有 `evidence_id`，也不把 Alert 证据改写成 Case 证据。
