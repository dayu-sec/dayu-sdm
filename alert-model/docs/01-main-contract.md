# 01 主契约

## 1. 设计边界

- 告警不写回事件表。事件不持有处置状态或研判结论。
- 告警和案件都通过 `sdm_evidence` 引用事实，不复制完整事件。证据主体是 ALERT 或 CASE，二选一（ADR-014）。禁止 `sdm_case.event_ids`，禁止 `sdm_event_behavior.case_id`。
- 主表只服务列表、筛选、排序、聚合、详情首屏。
- 多值、历史、多角色一律进子表。
- 对外交换可投影 OCSF Detection Finding / Incident Finding；对内不把 OCSF JSON 当物理表。Incident Finding 只投影 `case_kind=INCIDENT`。
- Case 是调查待办，不是安全事件。编组开案不等于宣告 Incident（ADR-013）。

## 2. 身份与分组键

| 键 | 对象 | 作用 | 谁生成 |
|---|---|---|---|
| `alert_id` | 告警 | 平台主键，不复用源产品 ID | 由 `tenant_id + dedup_key` 稳定派生：`alert_` + `sha256(tenant_id \|\| 0x1F \|\| dedup_key)` 前 24 位十六进制。禁止随机 UUID |
| `alert_display_id` | 告警 | 给人看的稳定编号 | 按 `ALT-{first_seen 的 UTC 日期 YYYYMMDD}-{dedup_key SHA1 前 8 位}` |
| `source_alert_id` | 告警 | 源产品原始 ID，仅引用 | 接入层 |
| `dedup_key` | 告警 | 同一规则、同一窗口、同一聚合维度的幂等键；与 `alert_id` 1:1 | 规则声明字段，平台统一哈希；必须含 `tenant_id`、`rule_id`、稳定维度、窗口或执行身份 |
| `merge_id` | 告警 | 跨窗口仍是同一安全现象；不需要归并为 `NULL` | 规则从 dedup 字段去掉窗口/事件 ID/批次后哈希 |
| `correlation_id` | 告警 | 关联批次或故事线，可先于 Case 存在 | 关联引擎 |
| `case_id` | 案件 | 工作单元主键；告警上的 `case_id` 是当前主案件 ID | 案件服务 |
| `analysis_id` | 调查 | 一次分析的主键，只追加 | 闸门 / 研判 / 人 |
| `evidence_id` | 证据 | 租户内唯一的证据行 | `ev_` + sha256(tenant + subject_type + subject_id + type + fact_key + role) 前 24 位十六进制 |
| `entity_id` | 实体 | 与 SDM 实体 ID 规则对齐 | 实体服务或告警写入时按规则计算 |

`tenant_id` 进入所有表主键或前缀，用于隔离、权限、归档。

**dedup_key 构成约束（2026-08-26 修订）**：dedup_key 的可变部分只允许「时间窗」与「稳定聚合维度」。**禁止包含事件级标识**（`event_id`、`log_id`、来源原始编号、批内自增序号）——任何事件级成分都会让每条事件自成一键，聚合归零，直接违反本键的设计目的（POC 实测教训：dedup_key 尾接事件 id 后 15,632 条事件产生 15,632 条告警，96.9% `event_count=1`）。

接入告警直通（规则告警未做平台再检测）场景，推荐构成：

```
dedup_key = tenant_id | rule_id（或 source_product|log_type|signature_id）| victim 实体值 | truncate(first_seen, 窗口)
```

- `victim 实体值` 取 primary_entity 统一派生算法（[02 §3](02-alert-fields.md)）在受害/受影响候选中的首选稳定值（优先 host，其次 ip/user；占位值如 `0.0.0.0`、`内网IP范围`、空串不得作为聚合维度）。无合格受害实体时该维度留空，按规则 × 时间窗聚合；**不得改用攻击者实体值充当受害维度**。
- 时间窗默认 5 分钟，接入规则可按来源设备语义声明覆盖；同窗再命中走「更新同一逻辑告警」路径刷新 `last_seen` / `event_count`。
- 单一规则 × 单受害实体 × 时间窗 是告警风暴的最小坍缩单元，窗口内的多条事件以证据（TRIGGER）形式追加。

## 3. 状态分层

| 字段 | 对象 | 含义 | 谁写 |
|---|---|---|---|
| `workflow_status` | 告警 / 案件 | 流程：NEW / IN_PROGRESS / CONFIRMED / SUPPRESSED / CLOSED | 工作流 |
| `case_kind` | 案件 | 调查还是事件：INVESTIGATION / INCIDENT | 默认 INVESTIGATION；升/降级由人或策略写 |
| `verdict` | 告警 / 案件 | 正式有效性：UNKNOWN / MALICIOUS / SUSPICIOUS / BENIGN / FALSE_POSITIVE | 策略或人；分析行只建议 |
| `conclusion` | 分析行 | 这一次调查的结论，枚举与 `verdict` 相同 | 闸门 / AI / 人 / playbook |
| `resolution_reason` | 案件（可选冗余到告警关闭时） | 关单原因，对齐 XSIAM：TP / FP / TESTING / KNOWN / DUPLICATE / RISK_ACCEPTED | 关闭动作 |

关闭 ≠ 无风险。误报 ≠ 已处置。`FALSE_POSITIVE` 不是 `workflow_status`。

`BENIGN`：行为真实但无害（出差登录、批准的备份）。  
`FALSE_POSITIVE`：检测本不该报。两者都可关单，回流检测工程的优先是 FP。

## 4. 分数分层

| 字段 | 含义 | 谁写 | 何时变 |
|---|---|---|---|
| `severity` | 处置紧急程度 INFO–CRITICAL | 规则或案件策略 | 规则初值；案件可覆盖展示用优先级，但不改检出 severity |
| `detection_confidence` | 检出有多可信 0–100 | 规则 | 出厂后不变 |
| `detection_risk_score` | 规则给出的风险 0–100 | 规则 | 出厂后不变 |
| `analysis_confidence` | 这一次调查有多确定 0–100 | 分析行 | 每行自己的值 |
| `priority_score` | 案件排序分 0–100 | 案件服务（规则分 + 资产 + 编组 + 历史关单） | 案件创建和更新时重算 |

禁止用同一列既表示「规则出厂分」又表示「现在排第几」。

## 5. 文案分层

| 字段 | 内容 | 可否含本次实体 |
|---|---|---|
| `alert_name` | 稳定短名 | 否 |
| `description` | 稳定的规则说明，可空 | 否 |
| `latest_analysis_summary` | 最新一次调查的短摘要 | 可以 |

不再单独要求规则填写与 `description` 近义的 `summary`。通知默认：`alert_name` + `primary_entity_value` + 最新分析摘要。

## 6. 写入原则

1. 告警首次写入：`verdict=UNKNOWN`，`workflow_status=NEW`，规则不得把检出假设写成正式 `verdict`（除非产品明确配置「规则即终审」的检测类型）。
2. 更新同一逻辑告警（同 `dedup_key`）：派生出同一 `alert_id`，刷新 `last_seen`、`event_count`、`updated_time`，追加证据，不新开分析也可。`created_time` 以首次为准（部分列更新，或载荷带回首次值）。
3. 分析只 insert，不 update 结论列。重跑新 `analysis_id`。引用的证据写入 `sdm_analysis_citation`（`evidence_id` + 当时的主体快照与摘要），禁止分析行里只存裸短名。接受流与此矛盾，见 [07 F1](07-follow-ups.md)。
4. 正式 `verdict` 回写必须带策略 ID 或人工 `analysis_id`。决策账尚未落表，见 [07 F2](07-follow-ups.md)。
5. 主表列表冗余由写入服务维护，以子表最新行准。
6. 进入 `CLOSED` / `SUPPRESSED` 时写 `closed_time`；`REOPEN` 清空 `closed_time`。未关闭对象禁止物理删除。
7. MVP 仅由案件服务维护 `sdm_alert.case_id` 当前快照，不写 `sdm_case_membership`，不提供成员变更历史。启用迁移、合并、拆分前必须落地 [07 F3](07-follow-ups.md)。
8. 新建 Case 必须 `case_kind=INVESTIGATION`。升为 `INCIDENT` 只允许人或带 `policy_id` 的策略，并写 workflow `PROMOTE_INCIDENT`。误报/无害/演练不得保持 `INCIDENT`。

## 7. 查询

| 场景 | 查什么 |
|---|---|
| 告警列表 | 只查 `sdm_alert` |
| 案件列表 | 只查 `sdm_case` |
| 安全事件列表 | `sdm_case` 且 `case_kind=INCIDENT` |
| 告警详情 | 主表 + 并行 evidence / entity / analysis / workflow |
| 案件当前成员 | `sdm_alert.case_id` |
| 入案 / 迁移历史 | MVP 不提供；后续由 `sdm_case_membership` 承载 |
| 按实体查告警 | `sdm_alert_entity` → `alert_id` |
| 告警证据 | `sdm_evidence` 且 `subject_type=ALERT`、`alert_id=?` |
| 案件自有证据 | `sdm_evidence` 且 `subject_type=CASE`、`case_id=?` |
| 案件可见证据 | 成员告警的 Alert 证据 ∪ 本案 Case 证据 |
| 证据回查 | evidence.`event_id` → `sdm_event_behavior` |
| 研判历史 | `sdm_analysis`；列表用 `latest_analysis_*` |
| 分析引用了哪些证据 | `sdm_analysis_citation` → `evidence_id`（租户内唯一，不随 Case 成员改） |

## 8. 物理约定

- 库：`sdm2_log`
- 所有时刻列均为 `DATETIME(3)`，**UTC**，毫秒精度。与 `sdm_event_behavior.occur_time` 同一存储时区，跨表可直接比较。Kafka 传 unix 毫秒/秒，RL `timezone=Etc/UTC` + `from_unixtime` 落列。`duration_ms`/`token_in`/`token_out` 是时长或计数，保持 `BIGINT`，不是时刻。
- 物理 Unique Key = 业务身份（ADR-010），时间列不进主键：
  - `sdm_alert`：`(tenant_id, alert_id)`
  - `sdm_evidence`：`(tenant_id, evidence_id)`
  - `sdm_analysis_citation`：`(tenant_id, analysis_id, evidence_id)`
  - `sdm_alert_entity`：`(tenant_id, alert_id, entity_id, alert_entity_role)`
  - `sdm_analysis`：`(tenant_id, analysis_id)`
  - `sdm_case`：`(tenant_id, case_id)`
  - `sdm_workflow_action`：`(tenant_id, workflow_id)`
- 工作对象表不做 `PARTITION BY RANGE(时间)`。Doris 分区列必须进 Unique Key，会拆开身份。时间筛选走倒排索引。
- `DISTRIBUTED BY HASH` 列必须是 Unique Key 的子集。按 `alert_id` 查询靠倒排，不能把非主键列拿来分桶。
- `alert_id` 由 `dedup_key` 派生，一张表只有一个 Unique Key，不再另建幂等表。
- 多值不用 Doris ARRAY，用表或 VARIANT 对象；筛选列必须是物理列
- `updated_time` 只做 Unique 表 sequence，表示谁更新，不保护 `created_time`
- 归档按行：`closed_time` 超过租户保留期，且主体已关闭，且告警未挂在未关闭案件上；子表随主体删。
- 部署版本戳记：`sdm2-deploy/files/scripts/apply_prod_schema.sh`（Job 仓）每次 apply 成功后，向本次覆盖的每张表写入表属性
  `sdm2.schema_release` / `sdm2.schema_git_sha` / `sdm2.applied_from`（`helm` 或 `node-direct`）/ `sdm2.applied_at`。
  查询方式：`SHOW CREATE TABLE <db>.<table>` 读属性块（该 Doris 版本**不支持** `SHOW TABLE PROPERTIES`，145 上会报语法错）。
  数据版本以行内 `schema_version` / `projection_version` /
  `mapping_revision` 为准，与表属性分工：行版本回答「数据按哪个契约产出」，表属性回答「现场表结构由哪个发布建立」。
  升级 preflight 以 `sdm2.schema_seq`（CI 写入的 git commit 数，单调递增）比较目标与现场：
  install（无戳记）/ replay（相等）/ upgrade（落后，执行 pending migrations）/ downgrade（超前，需
  `SDM2_ALLOW_DOWNGRADE=1`）/ foreign（分支构建或手工戳记等不可比较谱系，需 `SDM2_FORCE_MIGRATIONS=1`）。
- migrations 契约：增量变更放 `log-model/schema/migrations/vX.Y.Z__YYYYMMDDhhmmss_描述.sql`，
  文件名版本号决定执行序（`sort -V`）；累积携带——每个 release 包含历史全部 migration；
  每条必须幂等可重入（`ADD COLUMN IF NOT EXISTS` 等守卫），已覆盖的按 deployed seq 跳过。
  现场只答「现在是什么」；「经历过哪些版本」查 git tag 与 CI 日志，不做逐条执行账本。
