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
| `event_role_hint` | `VARCHAR(64)` | 可选 | 来源出处提示，取值见 [05](05-enums.md) `event_role_hint`；仅供追溯，不参与派生与查询 |
| `entity_value` | `TEXT` | 推荐 | 可读值 |
| `is_primary` | `BOOLEAN` | 推荐 | 与主表 primary 一致的那一行 |
| `asset_id` | `VARCHAR(128)` | 可选 | 资产中心编号；与事件侧 `host.id` / `device.id` 同一自然键（`ref_id=host::{id}`），禁止另立编号体系 |
| `used_for_grouping` | `BOOLEAN` | 可选 | 自动入案时是否用这个实体去找同一 Case；默认 false |
| `grouping_weight` | `DOUBLE` | 可选 | 这个实体有多「独特」：越少见越适合用来并案。专有主机高，NAT/公共 IP 低 |
| `valid_until` | `DATETIME(3)` | 可选 | 本地墙钟(+08:00)；超过此时间后不再用该实体做自动入案；Kafka 传 unix 毫秒/秒，RL `from_unixtime` 落列 |
| `risk_context` | `VARIANT` | 可选 | 资产画像、地理位置等研判上下文 JSON；顶层结构固定（§2.6），不得替代标准列 |

`alert_entity_role` 是研判视角。不确定攻击者时用 `related` / `affected`。

主表 `primary_entity_*` 必须与 `is_primary=true` 的那一行一致。按实体查告警只扫本表。

### 2.1 行集合：来源 × 角色

行由**告警写入服务**在 Alert 写入流程内统一展开（[02 §3](02-alert-fields.md) 的候选链 + 本节附加行），
规则与接入映射**不直接写实体表**。来源分两类：触发事件的声明/槽位，与来源产品字段（接入映射
`entity.extra` 逐源声明，未声明不落行）。

| 来源 | 事件侧路径 | `alert_entity_role` | `event_role_hint` | 条件 |
|---|---|---|---|---|
| C1 | `observation.assertion.victim[]` | `victim` | `assertion` | 设备明确声明受害方，最高优先 |
| C2 | `observation.assertion.affected[]` | `affected` | `assertion` | 声明的受影响实体 |
| C3 | `object`（typed object） | `affected` | `object` | 观测承受者；**不得自动升格 `victim`** |
| C4 | `observation.assertion.attacker[]`，其次 `subject` | `attacker` | `assertion` / `subject` | 仅 C1–C3 无候选时可能成为主对象 |
| 附加 | `observation.observer` | `observer` | `observer` | 需要「谁检出的」可查时落行；`application` 不在告警实体九值，取来源设备实体 |
| 附加 | 来源产品字段（映射 `entity.extra` 声明） | `indicator` / `related` | `source_alert_field` | IOC 未登记 `assertion.indicators[]` 前只能走此路径（[07 F4](07-follow-ups.md)） |

同一实体携带多个角色（如既被声明 `attacker` 又是行为 `subject`）时**落多行**，按唯一键区分；
同一实体同一角色只一行。`primary` 不是写入值——主行用 `is_primary=true` 标记，`alert_entity_role`
仍写该行的研判角色。

### 2.2 合并与幂等

- 键：`(tenant_id, alert_id, entity_id, alert_entity_role)`；N 条 `TRIGGER` 证据逐个指向的触发事件
  逐条展开后按该键合并，**不随事件条数复制行**。
- 重复命中同一键：只补空列（`event_role_hint` 保留首次非空值），`risk_context` 深合并，
  `created_time` 保留首次值不更新。
- 迟到事件：可覆盖同一键行的可更新列，`created_time` 不变。
- 每个 `alert_id` 恰好一行 `is_primary=true`；无合格候选时该告警实体表可以没有任何行，
  主表四列同时为 NULL（02 §3.4 兜底）。

### 2.3 写入时序

1. 落 `TRIGGER` 证据（至少一条，指向触发事件）；
2. 按 §2.1 展开实体行并合并；
3. 按 [02 §3](02-alert-fields.md) 选主实体，标记 `is_primary=true`；
4. 回填主表 `primary_entity_id/type/value/role`，与主行完全一致；不一致即写入失败，不得只改主表。

### 2.4 不做的事

- 不写 `case_id` / `analysis_id` 关联；Case 侧实体不进本表。
- 不因 IOC 自动升格 `victim`；`indicator` 与 `victim` 是不同语义的行。
- 不为凑数造实体，不用 `product` 当实体；`entity_type` 不在九值时整行丢弃。
- 不对全部告警统一 `related` 一刀切。

### 2.5 可选列的生产者

| 列 | 谁写 | 来源 | 缺失时 | 更新策略 |
|---|---|---|---|---|
| `used_for_grouping` | 写入服务 | 规则：`role ∈ {victim, affected}` 且 `entity_type ∈ {host, user, account}` | `false` | 每次重算 |
| `grouping_weight` | 写入服务 | 接入映射 `entity.grouping_weights`（host/user/account 0.85、service 0.4、ip 内网 0.35 / 外网 0.1、domain 0.2） | 映射未声明该项写 NULL | 每次重算 |
| `valid_until` | 写入服务 | 情报类实体有效期（Kafka 传 unix 毫秒/秒，RL `from_unixtime` 落列） | NULL（永不过期） | 覆盖 |
| `asset_id` | 资产富化服务 | 资产中心编号，与事件侧 `host.id` / `device.id` 同一自然键（`ref_id=host::{id}`） | NULL | 富化回填 |
| `risk_context` | 富化 / 研判写入 | `extensions.enrichments` 与资产画像 | NULL | 深合并 |

未实现上述生产者时一律写 NULL / 默认值，**禁止编造**；`asset_id` 未接通前保持 NULL，
不得把 `entity_value` 复制进来充数。

### 2.6 `risk_context` 逻辑模型（VARIANT 固定结构）

`risk_context` 自由结构指**顶层键固定、叶子自由**。结构对齐日志侧富化口径
（`log-model/docs/mappings/21-sdm-event-ip-asset-enrichment-mapping.md`）：业务值进语义子对象，
溯源进 `enrichments`，两者不混写。

```json
{
  "geo": {
    "country":       { "code": "US", "name": "美国" },
    "region":        { "name": "纽约州" },
    "city":          { "name": "New York" },
    "coordinates":   { "latitude": 40.7128, "longitude": -74.006 }
  },
  "asset": {
    "id":             "2868257359929541780",
    "name":           "DESKTOP-FIN-0457",
    "type":           "endpoint",
    "system":         { "id": "...", "name": "..." },
    "organization":   { "id": "...", "name": "财务部终端" }
  },
  "enrichments": {
    "geo.ip_geo": {
      "provider": "geo.ip_geo", "database": "poc-geo-20260805",
      "matched_at": "2026-08-05T10:00:00+08:00",
      "match_method": "precise", "confidence": "high"
    },
    "asset.v_asset_subject_exclude_biz": {
      "provider": "asset.v_asset_subject_exclude_biz", "database": "poc-cmdb-20260805",
      "matched_at": "2026-08-05T10:00:00+08:00",
      "match_method": "asset_id", "confidence": "high"
    }
  }
}
```

| 顶层键 | 语义 | 对齐事件侧 | 适用实体类型 |
|---|---|---|---|
| `geo` | IP/域名地理位置 | `{party}.geo.*`（21 §3：country/region/city/coordinates/continent 同构） | ip / domain |
| `asset` | 资产画像 | `{party}.resource.*` + `extensions.profiles.endpoint_asset`（id/name/type/system/organization 同构） | host / service / device 类 |
| `enrichments` | 富化溯源，按 provider 键控 | `extensions.enrichments`（21 §6：provider / database / matched_at / match_method / confidence / miss_reason） | 全部 |

约束：

- 业务值不进 `enrichments`，溯源字段不进 `geo` / `asset`（与事件侧同规）。
- `asset.id` 与标准列 `asset_id` 必须一致；不一致即写入失败。编号的权威落位是标准列，
  `asset` 子对象承载编号之外的画像（名称、类型、系统、组织、暴露面等）。
- 无命中的子对象整体省略，**禁止空 `{}`**（与事件侧 object 规则一致）；未命中可在
  `enrichments.{provider}.miss_reason` 记录原因。
- 深合并按 §2.2：同一键行重复写入时 `geo` / `asset` 逐叶覆盖补空，
  `enrichments` 按 provider 键保留各来源溯源。
- 值必须来自实际富化结果；未接通富化服务时整列保持 NULL，不得用事件样例值或私网推断充数。
