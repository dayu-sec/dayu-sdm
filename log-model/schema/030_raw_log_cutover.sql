-- raw_msg 拆分割接脚本（2026-08-19）。
-- 前置：
--   1. 已执行 006_raw_log.sql 创建 sdm2_log.raw_log。
--   2. 已确认 Doris 支持 SHA2(expr, 256)（BE 内存吃紧时先单独探针：
--      SELECT SHA2('x', 256);）。
-- 执行顺序：停旧作业 -> 回填 -> 起新作业 -> 验收 -> （验收通过后）删列。
-- 停止与启动之间到达的 Kafka 消息由 v3/raw_log 作业从暂停点继续消费，不丢不重。
-- 实际执行记录（2026-08-19）：按本脚本顺序完成；sdm_event 先 TRUNCATE 清空，
-- 跳过回填步骤，raw_log 列收敛为 raw_msg + raw_msg_digest + digest_algo。

USE sdm2_log;

-- 1. 停止旧的事件作业（v2 同时写 raw_msg 到 sdm_event）。
STOP ROUTINE LOAD FOR sdm_events_load_standard_v2;

-- 2. 存量回填（可选；2026-08-19 实际执行时 sdm_event 已清空，未执行本步）：
--    把 sdm_event.raw_msg 一次性搬入 raw_log，digest 由 SQL 计算。
-- INSERT INTO raw_log (tenant_id, occur_time, event_id, raw_msg, raw_msg_digest, digest_algo)
-- SELECT tenant_id, occur_time, event_id, raw_msg, SHA2(raw_msg, 256), 'sha256'
-- FROM sdm_event
-- WHERE raw_msg IS NOT NULL AND raw_msg <> '';
-- 4. 验收（人工核对后继续）：
--    SELECT COUNT(*) FROM raw_log;
--    SELECT COUNT(*) FROM sdm_event WHERE raw_msg IS NOT NULL AND raw_msg <> '';

-- 5. 从 sdm_event 删除 raw_msg 列（light_schema_change，秒级）。
--    已于 2026-08-19 实际执行：ALTER TABLE sdm2_log.sdm_event DROP COLUMN raw_msg。
--    同批清理：sdm_entity_profile_v / sdm_entity_event_index_mv / sdm_entity_name_map_mv /
--    sdm_entity_profile_mv 已从 sdm2_log 删除。
-- ALTER TABLE sdm_event DROP COLUMN raw_msg;
