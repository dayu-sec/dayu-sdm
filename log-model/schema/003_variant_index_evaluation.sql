-- Doris VARIANT inverted-index evaluation for the interim sdm_event design.
-- Isolated database and idempotent rows; does not touch sdm2_log.sdm_event.

CREATE DATABASE IF NOT EXISTS sdm2_variant_index_eval;

CREATE TABLE IF NOT EXISTS sdm2_variant_index_eval.event_variant_no_index (
    `id` BIGINT NOT NULL,
    `tenant_id` VARCHAR(128) NOT NULL,
    `occur_time` DATETIME(3) NOT NULL,
    `log_type` VARCHAR(128) NOT NULL,
    `roles_obj` VARIANT NULL,
    `facets_obj` VARIANT NULL,
    `source_finding_obj` VARIANT NULL
)
UNIQUE KEY(`id`)
DISTRIBUTED BY HASH(`id`) BUCKETS 1
PROPERTIES (
    "enable_unique_key_merge_on_write" = "true",
    "replication_num" = "1",
    "light_schema_change" = "true"
);

CREATE TABLE IF NOT EXISTS sdm2_variant_index_eval.event_variant_with_index (
    `id` BIGINT NOT NULL,
    `tenant_id` VARCHAR(128) NOT NULL,
    `occur_time` DATETIME(3) NOT NULL,
    `log_type` VARCHAR(128) NOT NULL,
    `roles_obj` VARIANT NULL,
    `facets_obj` VARIANT NULL,
    `source_finding_obj` VARIANT NULL,
    INDEX `idx_roles_obj` (`roles_obj`) USING INVERTED,
    INDEX `idx_facets_obj` (`facets_obj`) USING INVERTED,
    INDEX `idx_source_finding_obj` (`source_finding_obj`) USING INVERTED
)
UNIQUE KEY(`id`)
DISTRIBUTED BY HASH(`id`) BUCKETS 1
PROPERTIES (
    "enable_unique_key_merge_on_write" = "true",
    "replication_num" = "1",
    "inverted_index_storage_format" = "V3",
    "light_schema_change" = "true"
);

INSERT INTO sdm2_variant_index_eval.event_variant_no_index VALUES
(
    1,
    'tenant01',
    '2026-08-04 10:15:30.123',
    'edr_alert_log',
    '{"source":{"endpoint":{"mac":"00-11-22-33-44-55"},"account":{"name":"alice"},"process":{"name":"powershell.exe"}},"target":{"endpoint":{"mac":"AA-BB-CC-DD-EE-FF"},"service":{"name":"rdp"},"url":{"full":"https://example.test/login"},"file":{"name":"payload.exe"}},"observer":{"type":"endpoint_sensor"}}',
    '{"network":{"direction":"W2L"},"application":{"name":"RDP"},"http":{"request":{"method":"POST","host":"example.test"},"response":{"status_code":403}},"container":{"kubernetes":{"namespace":"security-prod","pod":{"name":"edr-agent-0"}}}}',
    '{"title":"检测到远程 RDP 爆破","severity":"high","category":"credential_access","action":"block","original_id":"alert-001","mitre":{"technique_id":"T1110"},"indicators":[{"type":"ipv4","value":"10.46.178.15"}]}'
),
(
    2,
    'tenant01',
    '2026-08-04 10:16:30.123',
    'edr_antivirus_virus',
    '{"source":{"endpoint":{"mac":"00-11-22-33-44-66"},"account":{"name":"bob"},"process":{"name":"scanner.exe"}},"target":{"file":{"name":"clean.txt"}},"observer":{"type":"antivirus_engine"}}',
    '{"network":{"direction":"internal"},"application":{"name":"antivirus"}}',
    '{"title":"病毒查杀完成","severity":"low","category":"malware","action":"quarantine","original_id":"alert-002","malware":{"name":"EICAR","type":"test_file"},"indicators":[{"type":"md5","value":"44d88612fea8a8f36de82e1278abb02f"}]}'
);

INSERT INTO sdm2_variant_index_eval.event_variant_with_index
SELECT * FROM sdm2_variant_index_eval.event_variant_no_index;

SELECT COUNT(*) AS no_index_rows
FROM sdm2_variant_index_eval.event_variant_no_index;

SELECT COUNT(*) AS with_index_rows
FROM sdm2_variant_index_eval.event_variant_with_index;

SELECT
    `id`,
    CAST(`roles_obj`['source']['account']['name'] AS STRING) AS source_account,
    CAST(`facets_obj`['http']['response']['status_code'] AS INT) AS http_status,
    CAST(`source_finding_obj`['mitre']['technique_id'] AS STRING) AS technique_id
FROM sdm2_variant_index_eval.event_variant_with_index
ORDER BY `id`;
