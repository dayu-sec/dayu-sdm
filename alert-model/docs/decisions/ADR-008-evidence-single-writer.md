# ADR-008 证据只写子表

- 状态：已接受
- 日期：2026-08-17

## 决定

删除主表 `evidences` VARIANT。规则生成告警时把命中 `event_id` 写入证据表，主表只保留 `event_count`。表名现为 `sdm_evidence`（ADR-014）；本条「只写子表、不双写主表」不变。

避免 Doris 上双写漂移。列表不展示证据数组。
