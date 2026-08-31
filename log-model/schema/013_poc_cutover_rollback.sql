-- 仅在新版 sdm_event 尚未接收需要保留的数据时执行回退。

USE sdm2_log;

DROP TABLE IF EXISTS sdm_event;
ALTER TABLE sdm_event_legacy_20260804 RENAME sdm_event;

-- 旧 Routine Load 已被 STOP，不能 RESUME；如需恢复旧写入，重新执行
-- 旧 87 列 Routine Load 已移除；本文件仅保留切换历史说明。
-- 旧视图按原定义重新执行：
-- log-model/poc-runtime/schema/002_ui_serving_views.sql
-- sdm_entity_event_expand_v 需从切换前保存的 SHOW CREATE VIEW 输出恢复。
