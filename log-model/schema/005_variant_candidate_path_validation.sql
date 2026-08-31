-- Validate all 13 first-batch scalar projection reduction candidates.
-- Every case must return matched_rows = 1.

SELECT 'source_mac' AS case_name, COUNT(*) AS matched_rows
FROM sdm2_variant_index_eval.event_variant_with_index
WHERE CAST(`roles_obj`['source']['host']['mac'] AS STRING) = '00-11-22-33-44-55'
UNION ALL
SELECT 'source_account', COUNT(*)
FROM sdm2_variant_index_eval.event_variant_with_index
WHERE CAST(`roles_obj`['source']['account']['name'] AS STRING) = 'alice'
UNION ALL
SELECT 'source_process_name', COUNT(*)
FROM sdm2_variant_index_eval.event_variant_with_index
WHERE CAST(`roles_obj`['source']['process']['name'] AS STRING) = 'powershell.exe'
UNION ALL
SELECT 'target_mac', COUNT(*)
FROM sdm2_variant_index_eval.event_variant_with_index
WHERE CAST(`roles_obj`['target']['endpoint']['mac'] AS STRING) = 'AA-BB-CC-DD-EE-FF'
UNION ALL
SELECT 'target_service', COUNT(*)
FROM sdm2_variant_index_eval.event_variant_with_index
WHERE CAST(`roles_obj`['target']['service']['name'] AS STRING) = 'rdp'
UNION ALL
SELECT 'target_url', COUNT(*)
FROM sdm2_variant_index_eval.event_variant_with_index
WHERE CAST(`roles_obj`['target']['url']['full'] AS STRING) = 'https://example.test/login'
UNION ALL
SELECT 'target_file_name', COUNT(*)
FROM sdm2_variant_index_eval.event_variant_with_index
WHERE CAST(`roles_obj`['target']['file']['name'] AS STRING) = 'payload.exe'
UNION ALL
SELECT 'observer_type', COUNT(*)
FROM sdm2_variant_index_eval.event_variant_with_index
WHERE CAST(`roles_obj`['observer']['type'] AS STRING) = 'endpoint_sensor'
UNION ALL
SELECT 'network_direction', COUNT(*)
FROM sdm2_variant_index_eval.event_variant_with_index
WHERE CAST(`facets_obj`['network']['direction'] AS STRING) = 'W2L'
UNION ALL
SELECT 'application_name', COUNT(*)
FROM sdm2_variant_index_eval.event_variant_with_index
WHERE CAST(`facets_obj`['application']['name'] AS STRING) = 'RDP'
UNION ALL
SELECT 'http_method', COUNT(*)
FROM sdm2_variant_index_eval.event_variant_with_index
WHERE CAST(`facets_obj`['http']['request']['method'] AS STRING) = 'POST'
UNION ALL
SELECT 'http_status', COUNT(*)
FROM sdm2_variant_index_eval.event_variant_with_index
WHERE CAST(`facets_obj`['http']['response']['status_code'] AS INT) = 403
UNION ALL
SELECT 'http_host', COUNT(*)
FROM sdm2_variant_index_eval.event_variant_with_index
WHERE CAST(`facets_obj`['http']['request']['host'] AS STRING) = 'example.test';
