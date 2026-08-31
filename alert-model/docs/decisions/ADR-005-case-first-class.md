# ADR-005 Case 一等对象

- 状态：已接受
- 日期：2026-08-17

## 背景

草案用 `incident_ids` VARIANT 和 `correlation_id` 兼案件。XSIAM、Sentinel、Elastic、Splunk ES 8 都把 Case/Incident 做成工作对象：分数、分派、SLA、AI 叙事挂在案件上。

## 决定

新增 `sdm_case`。告警用 `case_id` 指向**当前**主案件（可空）。MVP 只维护该快照，不保留成员变更历史。

成员增删、合并、拆分、迁移的权威历史设计保留在 `sdm_case_membership`（ADR-011 / F3），但延后实施，不进入 MVP 建表和读写链路。

`correlation_id` 仍表示关联批次/故事线，可以先于案件存在；案件服务根据关联结果创建或合并案件。

`merge_id` 只解决跨窗口同一检测现象，不代替案件。

## 后果

列表「待办工作」以案件为准；MSS 值守仍可按告警交货。优先级分挂在案件，不改写告警上的规则风险分。

Case 不是 Incident。默认调查待办；是否安全事件见 `case_kind`（ADR-013）。
