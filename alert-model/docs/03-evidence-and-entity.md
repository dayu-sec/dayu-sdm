# 03 证据与实体

## 1. `sdm_evidence`

主体到事实的连接。不复制事件正文。

主体是 **ALERT 或 CASE，二选一**（ADR-014）。检出触发挂在告警上；调查过程新增的日志、情报、人工输入挂在案件上。Case 通过成员告警读取已有 Alert 证据，不把同一条 TRIGGER 再挂一遍。

主键：`UNIQUE KEY(tenant_id, evidence_id)`，租户内唯一，不按告警或案件缩域。  
`evidence_id` 由 `tenant_id + subject_type + subject_id + evidence_type + fact_key + role` 稳定派生（ADR-012 / ADR-014）。禁止 `evid_1` 这种主体内短名。  
`alert_id` / `case_id` 表示挂在哪个主体上，不进主键。同一 `evidence_id` 再展开覆盖同一行。

写入 XOR（Doris 不强制，由服务校验）：

| `subject_type` | `alert_id` | `case_id` |
|---|---|---|
| `ALERT` | 必填 | 必须空 |
| `CASE` | 必须空 | 必填 |

`subject_id`：ALERT 用 `alert_id`，CASE 用 `case_id`。

| 字段 | 类型 | 必要性 | 说明 |
|---|---|---|---|
| `tenant_id` | `VARCHAR(128)` | 必填 | |
| `evidence_id` | `VARCHAR(128)` | 必填 | 租户内唯一；`ev_` + sha256(...) 前 24 位十六进制 |
| `subject_type` | `VARCHAR(32)` | 必填 | ALERT / CASE |
| `alert_id` | `VARCHAR(128)` | 条件 | `subject_type=ALERT` 必填 |
| `case_id` | `VARCHAR(128)` | 条件 | `subject_type=CASE` 必填 |
| `evidence_type` | `VARCHAR(64)` | 必填 | EVENT / RAW_LOG / SOURCE_ALERT / INTEL / ASSET / USER_INPUT |
| `event_id` | `VARCHAR(128)` | 条件 | EVENT 必填 |
| `log_id` | `VARCHAR(128)` | 条件 | RAW_LOG 时与 raw_log_id 至少一个 |
| `raw_log_id` | `VARCHAR(128)` | 推荐 | 平台原始日志主键 |
| `source_alert_original_id` | `VARCHAR(128)` | 条件 | SOURCE_ALERT 必填 |
| `external_ref` | `VARCHAR(255)` | 条件 | INTEL / ASSET |
| `evidence_payload_ref` | `VARCHAR(255)` | 可选 | 非事件载荷 |
| `evidence_role` | `VARCHAR(64)` | 推荐 | TRIGGER / CONTEXT / CORROBORATION / NEGATIVE / ENRICHMENT |
| `evidence_time` | `DATETIME(3)` | 必填 | DATETIME(3) 本地墙钟(+08:00)；证据挂到主体的时间。Alert 触发证据通常等于告警创建时间，Case 新增证据等于收集时间；不进主键 |
| `event_occur_time` | `DATETIME(3)` | 推荐 | DATETIME(3) 本地墙钟(+08:00)；事实发生时间 |
| `event_type` | `VARCHAR(128)` | 推荐 | |
| `evidence_summary` | `TEXT` | 推荐 | 单条证据摘要，不整段复制到告警或案件 description |
| `chain_id` | `VARCHAR(128)` | 可选 | 调查链或首次发现该证据的收集批次；同一次 Case 收集使用同一 ID |
| `sequence_no` | `INT` | 可选 | 同一收集批次内的稳定顺序 |
| `parent_evidence_id` | `VARCHAR(128)` | 可选 | |
| `phase` | `VARCHAR(128)` | 可选 | 收集阶段：INITIAL / FOLLOW_UP / MANUAL |
| `weight` | `DOUBLE` | 可选 | |
| `confidence` | `INT` | 可选 | 单条证据置信度 0–100 |

`TRIGGER` 只允许 `subject_type=ALERT`。Case 新增证据用 `CONTEXT` / `CORROBORATION` / `NEGATIVE` / `ENRICHMENT`，或 `USER_INPUT`。

`NEGATIVE` 表示反向证据（该出现但没出现），AI 研判必须能落这种行，不能只写在自然语言里。案件级反向证据挂 Case，不要塞进某条成员告警。

`parent_evidence_id` 引用的也是租户内唯一的 `evidence_id`。分析不得只存裸短名，见 `sdm_analysis_citation`。

同一 Event 被 Alert 与 Case 各自引用时写两行、两个 `evidence_id`。默认不要为了「案件也能看见」而复制成员告警已有的 TRIGGER。

Case 证据收集发生在案件编组之后、CASE 分析之前。收集器先按当前成员 Alert 汇总已有证据，再围绕实体、时间范围和关联标识检索补充事实；已有 Alert 证据只进入证据包，不复制为 CASE 行，新找到的日志、情报或反向证据才以 `subject_type=CASE` 写入。每次收集生成新的 `chain_id`；已经存在的同主体、同事实、同角色证据保持原行和首次发现批次不变，只追加此前未见的证据关系。

禁止：

- 在 `sdm_case` 上存 `event_ids` 数组
- 给 `sdm_event_behavior` 增加 `case_id`
- 把调查附件挂到随便一条成员告警上冒充 Case 证据

## 2. `sdm_alert_entity`

一条告警多个实体、同一实体多个研判角色。

物理主键即逻辑唯一：`UNIQUE KEY(tenant_id, alert_id, entity_id, alert_entity_role)`。同一告警同一实体同一角色只保留一行。`created_time` 冗余告警创建时间，不进主键。

| 字段 | 类型 | 必要性 | 说明 |
|---|---|---|---|
| `alert_id` | `VARCHAR(128)` | 必填 | |
| `tenant_id` | `VARCHAR(128)` | 必填 | |
| `created_time` | `DATETIME(3)` | 必填 | DATETIME(3) 本地墙钟(+08:00)；冗余告警 created_time，不进主键 |
| `entity_id` | `VARCHAR(255)` | 必填 | 与 SDM 实体 ID 规则对齐 |
| `entity_type` | `VARCHAR(64)` | 必填 | ip / host / user / account / process / file / domain / url / service |
| `alert_entity_role` | `VARCHAR(64)` | 必填 | victim / attacker / affected / indicator / observer / related / primary |
| `event_role_hint` | `VARCHAR(64)` | 可选 | 来源事件角色 source / carrier / target / observer / related |
| `entity_value` | `TEXT` | 推荐 | 可读值 |
| `is_primary` | `BOOLEAN` | 推荐 | 与主表 primary 一致的那一行 |
| `asset_id` | `VARCHAR(128)` | 可选 | 资产中心编号；与事件侧 `host.id` / `device.id` 同一自然键（`ref_id=host::{id}`），禁止另立编号体系 |
| `used_for_grouping` | `BOOLEAN` | 可选 | 自动入案时是否用这个实体去找同一 Case；默认 false |
| `grouping_weight` | `DOUBLE` | 可选 | 这个实体有多「独特」：越少见越适合用来并案。专有主机高，NAT/公共 IP 低 |
| `valid_until` | `DATETIME(3)` | 可选 | 本地墙钟(+08:00)；超过此时间后不再用该实体做自动入案；Kafka 传 unix 毫秒/秒，RL `from_unixtime` 落列 |
| `risk_context` | `VARIANT` | 可选 | 资产重要性、暴露面等研判上下文 JSON；自由结构，不得替代标准列 |

`alert_entity_role` 是研判视角。不确定攻击者时用 `related` / `affected`。

主表 `primary_entity_*` 必须与 `is_primary=true` 的那一行一致。按实体查告警只扫本表。
