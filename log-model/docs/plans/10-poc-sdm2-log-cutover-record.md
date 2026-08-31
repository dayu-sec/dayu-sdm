# POC 环境 `sdm_event` 中间版切换记录

> **[历史记录] 本记录涉及的大禹告警表 `ldm_alert` 已在 feature/sdm2-alert-model 分支从交付物删除（SDM2.0 告警模型重新设计中）。文中 `ldm_alert` 相关内容仅描述当时的执行事实，不代表当前交付范围。**

## 1. 切换范围

- Doris 数据库：`sdm2_log`
- 新日志表：`sdm_event`
- 旧日志表保留名：`sdm_event_legacy_20260804`
- 新告警表：`ldm_alert`
- 原有 `sdm_alert`、`sdm_alert_evidence` 和实体派生物理表不做修改。

## 2. 切换前检查结果

| 检查项 | 结果 |
|---|---|
| 旧表数据量 | 9,695,127 行 |
| 事件时间范围 | 2026-05-20 08:56:16 至 2026-07-21 18:46:58 |
| Routine Load | `sdm_events_load`，状态 `PAUSED` |
| 直接依赖视图 | `sdm_account_host_summary_v`、`sdm_entity_event_expand_v`、`sdm_session_summary_v` |
| 实体索引物理表 | `sdm_entity_event_index_mv`，17,003,581 行 |
| 原平台告警表 | `sdm_alert`，1,650 行 |
| 原告警证据表 | `sdm_alert_evidence`，0 行 |

## 3. 切换策略

采用“旧表改名保留、新表使用原名”的方式，不直接删除约 970 万行旧数据。旧 Routine Load 停止，三个依赖旧字段结构的视图暂时下线。新版日志表和大禹告警表分别使用 `sdm_event`、`ldm_alert`。

旧实体索引和画像表不会自动按新版日志更新，在完成新实体展开契约前只能视为历史快照，不能用于验证新写入数据。

## 4. 脚本顺序

1. `010_poc_cutover_precheck.sql`
2. `011_poc_cutover.sql`
3. `002_sdm_event.sql`
4. `001_ldm_alert.sql`
5. `012_poc_cutover_acceptance.sql`

如果新版表尚未接收需要保留的数据，可执行 `013_poc_cutover_rollback.sql` 回退表名；旧 Routine Load 和视图需按原定义重新创建。

## 5. 实际执行结果

2026-08-04 已完成 POC 切换：

| 验收项 | 结果 |
|---|---|
| 旧 Routine Load | 已停止，活动任务列表中不再返回 `sdm_events_load` |
| 旧日志表 | 已改名为 `sdm_event_legacy_20260804`，仍为 9,695,127 行 |
| 新日志表 | `sdm_event` 创建成功，55 列，初始 0 行 |
| 新告警表 | `ldm_alert` 创建成功，532 列，初始 0 行 |
| VARIANT | 4 列类型正确；JSON 文本写入、多层路径读取通过 |
| ARRAY | `log_id_list` 等字段为 Doris `ARRAY`；写入和数组下标读取通过 |
| 日志索引 | 20 个倒排索引可见，其中 3 个为 VARIANT 倒排索引 |
| 动态分区 | 按天分区已创建，当前分区状态为 `NORMAL` |
| 冒烟数据 | 日志和告警各写入 1 条后读取成功，随后清理为 0 行 |

该 Doris 版本不提供 `PARSE_JSON()`，VARIANT 直接写入合法 JSON 文本即可，由 Doris 隐式转换。

## 6. 当前限制

- 新版 Routine Load 尚未创建，Kafka 数据当前不会进入新版 `sdm_event`。
- 三个旧视图已下线；其中账户和会话视图依赖已取消标量投影的 `carrier_session_id`，不能原样恢复。
- `sdm_entity_event_index_mv`、`sdm_entity_name_map_mv` 和 `sdm_entity_profile_mv` 保留的是旧日志生成的历史快照，不会自动包含新版日志。
- 在完成新版日志映射、Routine Load 和查询契约前，不应删除 `sdm_event_legacy_20260804`。

## 7. 新版日志接入

新版 Routine Load 脚本为 `schema/020_routine_load_sdm_event_interim.sql`，任务名为 `sdm_events_load_interim_raw_msg`，使用现有 Kafka topic `sdm_s4_events` 和 broker `10.106.129.101:9092`。

任务初始使用 `OFFSET_END`，只接收部署后的新消息，不会自动重放旧 Routine Load 的历史积压。`schema/021_routine_load_acceptance.sql` 用于检查任务状态、错误数、延迟和落库字段；若需停止，执行 `schema/022_routine_load_stop.sql`。

当前映射将 `schema_version` 固定为 `1`，`mapping_id` 固定为 `interim.sdm_event.v1`，并将旧来源告警字段映射到 `source_finding` 标量字段。真实生产接入前仍需用实际消息样本确认 `roles`、`facets` 和 `source_finding` JSON 路径。

2026-08-05 已完成 POC 原文列迁移：

- 暂停旧任务 `sdm_events_load_interim`，从最终 Kafka offset `36290311` 续接。
- `sdm_event` 新增 `raw_msg STRING`，Routine Load 改为读取 `$.raw_msg`；新任务名为 `sdm_events_load_interim_raw_msg`。
- 旧 `raw_log_id` 暂保留为兼容列，历史数据不被误解释为原文；后续完成备份和下游确认后再删除。
- 已从 Bloom Filter 配置移除 `raw_log_id`。
- 验收时新任务为 `RUNNING`，错误行 0，`raw_msg` 已落库 3,485 行。

2026-08-04 首次接入验收结果：Routine Load 状态为 `RUNNING`，已提交 1 个任务，落库 54 行，错误 0 行，丢弃 0 行，Kafka lag 为 0。新版 `sdm_event` 当前已不再是空表。
