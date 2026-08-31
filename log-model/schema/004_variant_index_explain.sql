-- Run after 003_variant_index_evaluation.sql.
-- Compare the no-index and indexed plans for the same predicates.

EXPLAIN
SELECT `id`
FROM sdm2_variant_index_eval.event_variant_no_index
WHERE CAST(`roles_obj`['source']['account']['name'] AS STRING) = 'alice';

EXPLAIN
SELECT `id`
FROM sdm2_variant_index_eval.event_variant_with_index
WHERE CAST(`roles_obj`['source']['account']['name'] AS STRING) = 'alice';

EXPLAIN
SELECT `id`
FROM sdm2_variant_index_eval.event_variant_with_index
WHERE CAST(`facets_obj`['http']['response']['status_code'] AS INT) = 403;

EXPLAIN
SELECT `id`
FROM sdm2_variant_index_eval.event_variant_with_index
WHERE CAST(`source_finding_obj`['mitre']['technique_id'] AS STRING) = 'T1110';

-- Compatibility probe: Doris 4.1.0-rc03 retains the array as a value, but
-- VARIANT['indicators'][0] does not descend into an array element and returns NULL.
EXPLAIN
SELECT `id`
FROM sdm2_variant_index_eval.event_variant_with_index
WHERE CAST(`source_finding_obj`['indicators'][0]['value'] AS STRING) = '10.46.178.15';

SELECT 'roles_string' AS case_name, COUNT(*) AS matched_rows
FROM sdm2_variant_index_eval.event_variant_with_index
WHERE CAST(`roles_obj`['source']['account']['name'] AS STRING) = 'alice'
UNION ALL
SELECT 'facets_integer', COUNT(*)
FROM sdm2_variant_index_eval.event_variant_with_index
WHERE CAST(`facets_obj`['http']['response']['status_code'] AS INT) = 403
UNION ALL
SELECT 'finding_nested_string', COUNT(*)
FROM sdm2_variant_index_eval.event_variant_with_index
WHERE CAST(`source_finding_obj`['mitre']['technique_id'] AS STRING) = 'T1110'
UNION ALL
SELECT 'finding_array_member_unsupported', COUNT(*)
FROM sdm2_variant_index_eval.event_variant_with_index
WHERE CAST(`source_finding_obj`['indicators'][0]['value'] AS STRING) = '10.46.178.15';
