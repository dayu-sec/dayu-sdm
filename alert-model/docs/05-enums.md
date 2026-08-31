# 05 枚举

未列出的字段禁止写入方自造枚举。大小写：状态/结论/动作用大写下划线；实体类型和角色用小写下划线。

## 告警 / 案件共用

### `severity`

`INFO` / `LOW` / `MEDIUM` / `HIGH` / `CRITICAL`

平台处置紧急程度。不沿用事件 syslog 小写。

### `workflow_status`

`NEW` / `IN_PROGRESS` / `CONFIRMED` / `SUPPRESSED` / `CLOSED`

### `case_kind`

`INVESTIGATION` / `INCIDENT`

只用于 `sdm_case`。默认 `INVESTIGATION`。`INCIDENT` 表示正式安全事件，不是建案默认值。

### `verdict` / `conclusion`

| 值 | 含义 |
|---|---|
| `UNKNOWN` | 尚无正式结论 |
| `MALICIOUS` | 确认恶意 |
| `SUSPICIOUS` | 可疑，证据不足 |
| `BENIGN` | 行为无害 |
| `FALSE_POSITIVE` | 检测误报 |

### `resolution_reason`

`TRUE_POSITIVE` / `FALSE_POSITIVE` / `SECURITY_TESTING` / `KNOWN_ISSUE` / `DUPLICATE` / `RISK_ACCEPTED`

### `alert_type`

`DETECTION` / `CORRELATION` / `ANOMALY` / `THREAT_INTEL` / `SOURCE_ALERT` / `MANUAL`

外部产品告警导入用 `SOURCE_ALERT`，不要标成 `DETECTION` 却无 `rule_id`。

### `rule_type`

`SINGLE_CONDITION` / `THRESHOLD` / `SEQUENCE` / `ANOMALY` / `THREAT_INTEL` / `CORRELATION`

仅规则引擎填写。

## 证据

### `evidence_type`

`EVENT` / `RAW_LOG` / `SOURCE_ALERT` / `INTEL` / `ASSET` / `USER_INPUT`

### `evidence_role`

`TRIGGER` / `CONTEXT` / `CORROBORATION` / `NEGATIVE` / `ENRICHMENT`

`TRIGGER` 只允许挂在 `subject_type=ALERT` 的证据上。

## 实体

### `entity_type`

`ip` / `host` / `user` / `account` / `process` / `file` / `domain` / `url` / `service`

### `alert_entity_role`

`victim` / `attacker` / `affected` / `indicator` / `observer` / `related` / `primary`

## 分析

### `subject_type`

`ALERT` / `CASE`

分析、流转、证据共用。证据表写在 `sdm_evidence.subject_type`；cite 快照写在 `sdm_analysis_citation.evidence_subject_type`。

### `analysis_type`

`GATE` / `RULE` / `AI` / `HUMAN` / `PLAYBOOK`

### `trigger_mode`

`ALERT` / `CASE` / `REPLAY` / `MANUAL`

### `next_hop`

`CLOSE_CANDIDATE` / `REUSE` / `FULL_AGENT` / `HUMAN`

### `noise_reason`

`EXCLUSION` / `KNOWN_FP` / `DUPLICATE` / `INSUFFICIENT_DATA` / `NONE`

### `accepted_status`

`PENDING` / `ACCEPTED` / `REJECTED` / `SUPERSEDED`

## 成员关系（后续待办）

以下枚举随 `sdm_case_membership` 保留为后续设计，MVP 不使用。

### `sdm_case_membership.action_type`

`ATTACH` / `DETACH` / `MOVE` / `MERGE` / `SPLIT`

与流转 `action_type` 不是同一枚举。

### `membership_reason`

`AUTO_GROUP` / `CORRELATION` / `MANUAL` / `MERGE` / `SPLIT` / `POLICY`

## 流转

### `action_type`

`ASSIGN` / `COMMENT` / `CONFIRM` / `CLOSE` / `SUPPRESS` / `ESCALATE` / `CREATE_TICKET` / `REOPEN` / `PROMOTE_INCIDENT` / `DEMOTE_INCIDENT`

`PROMOTE_INCIDENT` / `DEMOTE_INCIDENT` 只作用于案件，改 `case_kind`，不改 `workflow_status`。

## 案件分数来源

`RULE` / `COMPUTED` / `MANUAL`
