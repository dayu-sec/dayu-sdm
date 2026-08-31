# ADR-013 Case 不是 Incident

- 状态：已接受
- 日期：2026-08-17

## 背景

`sdm_case` 同时被写成「是不是同一场攻击」和「人的待办」。编组、误报复核、演练都会开 Case，若 Case 即 Incident，误报会自动进入安全事件口径。

MVP 中「同一场攻击」由 `correlation_id` / `merge_id` 回答；未来需要审计成员变更时，再由 `sdm_case_membership` 补充历史。另拆一张 `sdm_incident` 会复制分派、分析、成员和 SLA。

## 选项

1. Incident == Case。开案即事件。
2. 独立 `sdm_incident`，Case 只做调查，事件另挂成员。
3. 同一张 `sdm_case`。默认 `case_kind=INVESTIGATION`。Incident 是升级，不是建案副作用。

## 决定

选 3。不建 `sdm_incident`。

| 问题 | 对象 |
|---|---|
| 谁来办、SLA、叙事 | `sdm_case` |
| 是不是同一场攻击 | 当前：`correlation_id` / `merge_id`；未来历史：`sdm_case_membership` |
| 是否正式安全事件 | `sdm_case.case_kind` |

规则：

1. 新建 Case（含自动编组）一律 `INVESTIGATION`。AI、闸门、编组不得写 `INCIDENT`。
2. 升为 `INCIDENT` 只允许人，或策略（须有 `policy_id`）。写 `promoted_time` / `promoted_by`，并追加 workflow `PROMOTE_INCIDENT`。
3. 误报、无害、演练、复核都停在 `INVESTIGATION`，关单即可。已升级的可 `DEMOTE_INCIDENT` 退回。
4. `verdict=FALSE_POSITIVE` / `BENIGN` 或 `resolution_reason` 为测试/已知问题/误报时，禁止同时保持 `INCIDENT`：关单或降级须先把 `case_kind` 改回 `INVESTIGATION`。
5. 对外 OCSF Incident Finding 只投影 `case_kind=INCIDENT` 的行。

## 后果

值守队列看所有 Case。IR / 监管口径只看 `INCIDENT`。编组仍可把误报和真攻击放进同一个调查 Case，但不会因此多报一起事件。
