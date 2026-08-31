# ADR-001 主表变瘦

- 状态：已接受
- 日期：2026-08-17

## 背景

55 列草案把实体、证据数组、工单、处置、调查摘要都放在 `sdm_alert`。对照 OCSF Detection Finding、Sentinel SecurityAlert、XSIAM Issue、Dropzone 报告对象，检出主对象应只支撑列表和首屏。

## 选项

1. 维持 55 列宽表，子表可选。
2. 主表只保留检出 + 一个主实体 + 最新调查快照；多值进子表。

## 决定

选 2。

从主表权威中移除：`attacker_*` / `victim_*` 十二列、`evidences` VARIANT、`disposition_status`、`ticket_status`、规则侧 `summary`（与 description 合并）、必填的 `source_systems` 数组、必填的 `category_name`。

列表仍可冗余：`primary_entity_*`、`latest_analysis_conclusion` / `summary` / `confidence` / `time`、`assignee_id`、`ticket_id`、`case_id`。

## 后果

- 写入路径要同时写子表；规则最小契约变短。
- 旧 55 列 DDL 视为兼容投影，不作为 v0.2 权威。
