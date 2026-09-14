-- SDM2.0 原始日志表：从事件表拆出的独立原文存储。
-- 身份与 sdm_event_behavior 同构：UNIQUE KEY / HASH / 分区策略一致，同一 event_id 重灌时两表 upsert 行为一致。
-- 同文判定：WHERE digest_algo = ? AND raw_msg_digest = ?
-- dynamic_partition.start / history_partition_num 由 apply 脚本按 DORIS_RETENTION_DAYS 替换，生产默认 30 天。
-- auto_analyze_policy=disable：TEXT raw_msg 全表采样会打满 BE（闵行 2026-09-05）。
CREATE TABLE IF NOT EXISTS __DORIS_DB__.raw_log (
    `tenant_id` VARCHAR(128) NOT NULL COMMENT '租户编号：与 sdm_event_behavior.tenant_id 一致。',
    `occur_time` DATETIME(3) NOT NULL COMMENT '事件发生时间：与 sdm_event_behavior.occur_time 一致，作为分区和主键组成。',
    `event_id` VARCHAR(128) NOT NULL COMMENT '事件编号：与 sdm_event_behavior.event_id 一致，1:1。',
    `raw_msg` STRING NULL COMMENT '原始日志：未经标准化的源日志原文。',
    `raw_msg_digest` VARCHAR(64) NOT NULL COMMENT '原文摘要：原文内容的十六进制摘要，用于同文检测与变更判定。',
    `digest_algo` VARCHAR(16) NOT NULL DEFAULT 'sha256' COMMENT '摘要算法：产生 raw_msg_digest 的算法标识。',
    INDEX `idx_raw_msg` (`raw_msg`) USING INVERTED PROPERTIES ("parser" = "unicode") COMMENT '原文全文检索',
    INDEX `idx_raw_msg_digest` (`raw_msg_digest`) USING INVERTED COMMENT '同文检测 / 去重回查'
)
UNIQUE KEY(`tenant_id`, `occur_time`, `event_id`)
PARTITION BY RANGE(`occur_time`) ()
DISTRIBUTED BY HASH(`tenant_id`, `event_id`) BUCKETS 16
PROPERTIES (
    "enable_unique_key_merge_on_write" = "true",
    "replication_num" = "1",
    "dynamic_partition.enable" = "true",
    "dynamic_partition.time_unit" = "DAY",
    "dynamic_partition.start" = "__DYNAMIC_PARTITION_START__",
    "dynamic_partition.end" = "3",
    "dynamic_partition.prefix" = "p",
    "dynamic_partition.buckets" = "16",
    "dynamic_partition.create_history_partition" = "true",
    "dynamic_partition.history_partition_num" = "__HISTORY_PARTITION_NUM__",
    "bloom_filter_columns" = "event_id,raw_msg_digest",
    "storage_format" = "V3",
    "inverted_index_storage_format" = "V3",
    "light_schema_change" = "true",
    "auto_analyze_policy" = "disable"
);
