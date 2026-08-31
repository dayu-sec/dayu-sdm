# ADR-004 实体进子表

- 状态：已接受
- 日期：2026-08-17

## 背景

主表摊平 attacker/victim 只能表达一对实体，且把研判角色焊死在列名上。Sentinel / OCSF / XSIAM 都是「一个主对象 + 多值实体」。

## 决定

- 主表只保留 `primary_entity_id` / `type` / `value` / `role`。MVP 就必须计算稳定 `entity_id`，禁止「ID 一律 NULL、只写可读值」。
- 全部实体写入 `sdm_alert_entity`，逻辑唯一 `(alert_id, tenant_id, entity_id, alert_entity_role)`。
- 旧 12 列可作为只读兼容投影，规则和新服务不再作为权威写入。

## 后果

按主机/用户查告警走实体表。不确定攻击者时标 `related` 或 `affected`，不填 attacker。
