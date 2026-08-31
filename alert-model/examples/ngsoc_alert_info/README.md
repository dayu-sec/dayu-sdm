# NGSOC `sdm_event` → 告警各表

把 `log-model/examples/ngsoc/ngsoc_alert_info/` 里的 22 条 `*.expected-sdm-event.json` 写成 v0.2 告警表行。

源事件是 `record_kind=finding`：来源侧声称这是告警，**不是**平台 `sdm_alert`。本目录演示接入层如何把它落成平台告警。

再生：

```bash
python3 alert-model/scripts/build_ngsoc_alert_examples.py
```

## 每个样例写了什么

| 文件 | 表 | 含义 |
|---|---|---|
| `sdm_alert.json` | `sdm_alert` | 平台检出，`alert_type=SOURCE_ALERT` |
| `sdm_evidence.json` | `sdm_evidence` | 本条告警的 ALERT 证据：事件 / 源告警 / 原始日志，不复制正文 |
| `sdm_alert_entity.json` | `sdm_alert_entity` | 研判角色，不是事件 `source/target` |
| `sdm_analysis.json` | `sdm_analysis` | GATE + 告警轮 AI + 案件轮 AI；`verdict` 仍为 UNKNOWN |
| `sdm_analysis_citation.json` | `sdm_analysis_citation` | 各分析行引用的 `evidence_id` 与主体快照 |
| `sdm_case.json` | `sdm_case` | 闸门放行后自动开的 `INVESTIGATION` |
| `mapping.json` | — | 源路径与写入假设 |
| `README.md` | — | 该条摘要 |

分表 JSON 是写入形状。查询详情由 API 并行查子表后组装，不是物理表。代表性读模型：

- 告警详情：[sql_injection_attempt/alert.detail.json](sql_injection_attempt/alert.detail.json)
- 案件详情：[cases/sql_injection_11_1_68_18/case.detail.json](cases/sql_injection_11_1_68_18/case.detail.json)

告警详情只嵌 `subject_type=ALERT` 的分析，案件用 `case_ref` 指针。案件详情的 `members` 是列表投影，案件叙事只出现一次。

共享案件另见 [cases/sql_injection_11_1_68_18/](cases/sql_injection_11_1_68_18/)。该目录的 `sdm_evidence.json` 只含本案自有证据（`subject_type=CASE`），不含成员告警 TRIGGER。

未写 `sdm_workflow_action`：没有分派、关单或升事件动作。
未把 AI `conclusion` 回写成正式 `verdict`。

快照时点：告警入库 → GATE → 编组开案 → 告警轮 Agent → 案件 debounce 后一篇案件叙事。

## 映射要点

| 来源 | 去向 | 规则 |
|---|---|---|
| 空 `tenant_id` | 所有表 `tenant_id` | 样例补 `tenant01` |
| `source_finding.title` | `alert_name` | 稳定短名；不含本次实体 |
| `source_finding.original_id` | `source_alert_id`、`dedup_key` | `tenant01\|ngsoc\|{original_id}` |
| — | `alert_id` | `alert_` + sha256(`tenant \|\| 0x1F \|\| dedup_key`) 前 24 位 |
| — | `alert_display_id` | `ALT-{first_seen UTC 日}-{dedup_key SHA1 前 8 位}` |
| `source_finding.severity` | `severity` | 高危→HIGH，中危→MEDIUM；不沿用事件 syslog 小写 |
| `source_finding.confidence` | `detection_confidence` | 高=80，中=60，低=40 |
| 分类信号 | `category_code` | UDM SecurityCategory，见下表 |
| `occur_time` | `first_seen` / `event_occur_time` | |
| `latest_timestamp` 或 `occur_time` | `last_seen` | |
| `ingest_time` 或 `occur_time` | `created_time` | |
| `source_finding.count` | `event_count` | 缺省 1 |
| `source_finding.rule.id/label` | `rule_id` / `rule_name` | 源产品规则，不是平台规则引擎 |
| `event_id` | 证据 `EVENT` + `TRIGGER` | 至少一条 TRIGGER |
| 源告警 ID | 证据 `SOURCE_ALERT` + `CONTEXT` | |
| `log_id`（若有） | 证据 `RAW_LOG` + `CONTEXT` | |
| `source_finding.attacker/victim` | 实体角色 | 覆盖事件 source/target |
| IOC 域名 | `indicator` | 不作为主对象 |
| 观测设备 | `observer` | 不作为主对象 |
| 无攻击者/受害者（外传、VPN） | `affected` / `related` | 不确定时不用 attacker |

`alert_type` 固定 `SOURCE_ALERT`。即使 NGSOC 内部是关联规则，也不写成平台 `DETECTION`。

`verdict` / `case.verdict` 固定 `UNKNOWN`。GATE 只写 `next_hop`；Agent 只写 `conclusion` / `analysis_confidence` / 摘要 / cite。

`case_kind` 固定 `INVESTIGATION`。编组开案不是 Incident。

GATE 在编组前写入，故 `GATE.case_id` 为空（分析只追加）。告警轮 AI 已在编组之后，带 `case_id`。告警 `latest_analysis_*` 指向告警轮 AI；案件 `latest_analysis_*` 指向案件轮 AI。

## 分类

| 信号 | `category_code` | ATT&CK |
|---|---|---|
| 端口扫描 | `NETWORK_RECON` | TA0043 / T1046 |
| 远控木马 / C2 | `NETWORK_COMMAND_AND_CONTROL` | TA0011 / T1071 |
| 网络蠕虫 | `SOFTWARE_MALICIOUS` | TA0011 / T1071 |
| SQL 注入 / 反序列化 / 代码执行 / 目录遍历 | `EXPLOIT` | TA0001 / T1190 |
| 未授权访问 / 读库 | `ACL_VIOLATION` | TA0001 或 TA0007 |
| 弱口令 / 堡垒机绕过 / VPN 多 MAC | `AUTH_VIOLATION` | T1110 / T1078 |
| 源码或报错泄露 / 目录列表 | `DATA_AT_REST` | T1552 / T1083 |
| 慢速大量外传 | `DATA_EXFILTRATION` | TA0010 / T1041 |

来源 `ruleCategoryName` 只进 `extensions.source_finding.category_original`，不直接当 `category_code`。

## 实体与编组

主对象优先：`victim` > `affected` > `attacker`；同角色时 `target` 优先于 `related`。

`used_for_grouping=true` 仅 `host` / `user` / `account` 且角色为 `victim` / `affected`。攻击者 IP、公共域名、NAT 不自动并案。

弱关联自动入案要求：主对象为 `host` / `user` / `account`，且 `rule_id` 相同，且 15 分钟窗口。本批 SQL 注入主对象是 `ip`、规则也不同，弱关联不能并案。

同受害 IP `192.0.2.146`、同一攻击源 `192.0.2.238`、同一 15 分钟窗口的四条 SQL 注入，由关联引擎写入同一 `correlation_id`，再按强关联编进一个 Case：

- `sql_injection_sleep_function`
- `sql_injection_attempt`
- `sql_injection_comment_bypass`
- `mssql_waitfor_delay_sql_injection`

`sql_injection_probe`、`sql_injection_select_statement` 受害 IP 不同，各自一案。

案件轮只写一篇叙事，cite 四条告警的 TRIGGER 证据，并另挂一条本案 `INTEL` 证据（源 IP 情报），不把 TRIGGER 再挂到 Case 上，也不按成员告警乘。

## 索引

见 [manifest.json](manifest.json)。
