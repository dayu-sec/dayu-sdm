-- [HISTORICAL] ldm_alert DDL (001) has been removed on feature/sdm2-alert-model;
-- this cutover record is kept as executed history.
-- POC 中间版切换脚本。
-- 执行本文件前，必须先运行 010_poc_cutover_precheck.sql 并保存输出。
-- 001_ldm_alert.sql 和 002_sdm_event.sql 在本文件成功后分别执行。

USE sdm2_log;

STOP ROUTINE LOAD FOR sdm_events_load;

DROP VIEW IF EXISTS sdm_account_host_summary_v;
DROP VIEW IF EXISTS sdm_entity_event_expand_v;
DROP VIEW IF EXISTS sdm_session_summary_v;

ALTER TABLE sdm_event RENAME sdm_event_legacy_20260804;
