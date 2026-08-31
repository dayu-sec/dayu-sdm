# SDM2.0 日志中间版本契约

> **告警线已移除（feature/sdm2-alert-model 分支）**：大禹/QAX 穿透告警表
> `ldm_alert` 及其字段清单、血缘规则已从本契约删除，SDM2.0 告警模型将重新设计。
> 历史版本（含 §3 血缘关联与 §5 大禹字段规则）见 git 历史（如 `727b4de` 的
> `docs/main/01-interim-contract.md`）。

## 1. 范围

本中间版本使用 SDM2.0 五层事件模型保存标准化安全设备日志。当前只覆盖日志接入和查询。

## 2. 物理对象

| 对象 | 职责 |
|---|---|
| `sdm_event` | 一条标准化安全日志事实。设备自身的检测结果保存到 `source_finding`。 |

本中间版本不创建 `sdm_alert`、`sdm_alert_evidence`，也不创建大禹穿透告警表。

`sdm_event` 采用 49 个核心标量列和 4 个 VARIANT 完整对象列，共 53 列。中间版本暂不保存
`mapping_revision`、`projection_version` 和 `quality_status` 物理列；另将已通过 Doris 路径查询
验证的 13 个低频标量投影降级到 `roles_obj` 或 `facets_obj`。保留 `schema_version` 和
`mapping_id` 分别标识逻辑模型版本与映射契约。质量检测和隔离流程落地后，再评估增加
`quality_status`。

`roles_obj`、`facets_obj` 和 `source_finding_obj` 使用 Doris V3 倒排索引承接低频标量路径
过滤；`extensions_obj` 不建立无约束的全路径索引。数组任意成员查询不依赖当前 VARIANT
下标方案，需要主值投影或窄关系表。

## 3. 事件语义

- `sdm_event` 回答“观察到了什么”。
- `sdm_event.source_finding` 保存设备自身的检测或告警判断。
- 告警工作流、案件和调查历史不属于本中间版本范围。

## 4. 标准来源

- 物理契约：`log-model/contracts/hybrid-event/projection-registry.v1.json`
  （逻辑路径 → `sdm_event` 物理列投影，当前权威）。
- 字段清单：`docs/main/05-sdm-event-logical-field-catalog.md`（权威）、
  `docs/main/06-sdm-event-enum-catalog.md`。
- 原始日志：独立 `raw_log` 表（`schema/006_raw_log.sql`），`sdm_event` 与其经 `event_id` 1:1 关联（`metadata.raw_log_id` 恒等于 `event_id`，已于 2026-08-26 判定冗余退役）；
  旧 `schema/002_sdm_event.sql`（`metadata.raw_msg` 临时契约）与 `docs/main/04-sdm-event-doris-field-catalog.md`
  已于 2026-08-26 退役（04 保留退役说明）。
- 87 列 POC 字段文档已移除；当前只接受五层契约。
