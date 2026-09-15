# 02 告警主表 `sdm_alert`

> 物理表：`sdm2_log.sdm_alert`
> 主键：`UNIQUE KEY(tenant_id, alert_id)`（无时间分区，ADR-010）
> 列表只查本表。

## 1. 字段

| 分组 | 字段 | 类型 | 必要性 | 说明 |
|---|---|---|---|---|
| 身份 | `alert_id` | `VARCHAR(128)` | 必填 | 由 `tenant_id + dedup_key` 稳定派生，禁止随机 UUID |
| 身份 | `alert_display_id` | `VARCHAR(128)` | 必填 | 可见编号 `ALT-YYYYMMDD-XXXXXXXX`，日期取 `first_seen` 的 UTC 日 |
| 身份 | `tenant_id` | `VARCHAR(128)` | 必填 | 租户 |
| 身份 | `source_alert_id` | `VARCHAR(128)` | 可选 | 源产品原始 ID |
| 身份 | `source_product` | `VARCHAR(128)` | 推荐 | 主来源产品，如 `sdm-rule-engine`、`crowdstrike` |
| 语义 | `alert_name` | `TEXT` | 必填 | 稳定短名，不含本次实体 |
| 语义 | `description` | `TEXT` | 可选 | 稳定规则说明；与 name 去空白标点后相同则写 NULL |
| 语义 | `alert_type` | `VARCHAR(64)` | 必填 | 见枚举 |
| 语义 | `category_code` | `VARCHAR(64)` | 必填 | 告警一级分类编码，供列表筛选；如 `NETWORK_COMMAND_AND_CONTROL`。展示名由编码派生，不落库 |
| 语义 | `event_count` | `BIGINT` | 可选 | 命中事件数 |
| 分数 | `severity` | `VARCHAR(32)` | 必填 | INFO–CRITICAL |
| 分数 | `detection_confidence` | `INT` | 可选 | 规则检出置信度 0–100，出厂后不变 |
| 分数 | `detection_risk_score` | `INT` | 可选 | 规则风险分 0–100，出厂后不变 |
| 状态 | `workflow_status` | `VARCHAR(64)` | 必填 | 默认 NEW |
| 状态 | `verdict` | `VARCHAR(64)` | 必填 | 默认 UNKNOWN；仅策略或人更新 |
| 状态 | `closed_time` | `DATETIME(3)` | 可选 | DATETIME(3) 本地墙钟(+08:00)；进入 CLOSED/SUPPRESSED 时写入；REOPEN 清空；未关单为 NULL |
| 时间 | `created_time` | `DATETIME(3)` | 必填 | DATETIME(3) 本地墙钟(+08:00)；首次生成；更新必须复用 |
| 时间 | `updated_time` | `DATETIME(3)` | 必填 | DATETIME(3) 本地墙钟(+08:00)；任意变更刷新 |
| 时间 | `first_seen` | `DATETIME(3)` | 必填 | DATETIME(3) 本地墙钟(+08:00)；证据最早发生时间 |
| 时间 | `last_seen` | `DATETIME(3)` | 必填 | DATETIME(3) 本地墙钟(+08:00)；证据最晚发生时间 |
| 检测 | `rule_id` | `VARCHAR(128)` | 条件 | `alert_type=DETECTION` 且规则引擎时必填 |
| 检测 | `rule_name` | `TEXT` | 可选 | |
| 检测 | `rule_version` | `VARCHAR(64)` | 推荐 | 回放和误报分析依赖 |
| 检测 | `rule_type` | `VARCHAR(64)` | 可选 | 规则实现类型；非规则告警 NULL |
| 检测 | `detection_engine` | `VARCHAR(128)` | 可选 | |
| 键 | `dedup_key` | `VARCHAR(255)` | 必填 | 写入幂等输入；与 `alert_id` 1:1 |
| 键 | `merge_id` | `VARCHAR(128)` | 可选 | 跨窗口同一现象 |
| 键 | `correlation_id` | `VARCHAR(128)` | 可选 | 故事线 / 关联批次 |
| 键 | `case_id` | `VARCHAR(128)` | 可选 | 当前主案件 ID，一条告警至多一个；MVP 不保留入案历史 |
| 实体 | `primary_entity_id` | `VARCHAR(255)` | 推荐 | 稳定实体 ID；写入服务按 §3 从触发事件派生，规则与接入映射不填写 |
| 实体 | `primary_entity_type` | `VARCHAR(64)` | 推荐 | 与实体表枚举一致；随派生结果 |
| 实体 | `primary_entity_value` | `TEXT` | 推荐 | 列表可读值；随派生结果 |
| 实体 | `primary_entity_role` | `VARCHAR(64)` | 可选 | 主对象的研判角色；随派生结果 |
| 攻击 | `primary_tactic_id` | `VARCHAR(64)` | 可选 | 列表筛选，如 TA0002 |
| 攻击 | `primary_technique_id` | `VARCHAR(64)` | 可选 | 如 T1059 |
| 快照 | `latest_analysis_id` | `VARCHAR(128)` | 可选 | 最新分析行 |
| 快照 | `latest_analysis_conclusion` | `VARCHAR(64)` | 可选 | 最新调查结论，非正式 verdict |
| 快照 | `latest_analysis_confidence` | `INT` | 可选 | 最新调查置信度 |
| 快照 | `latest_analysis_summary` | `TEXT` | 可选 | 短摘要，限 400 字 |
| 快照 | `latest_analysis_time` | `DATETIME(3)` | 可选 | DATETIME(3) 本地墙钟(+08:00) |
| 快照 | `assignee_id` | `VARCHAR(128)` | 可选 | 从 workflow 冗余 |
| 快照 | `ticket_id` | `VARCHAR(128)` | 可选 | 从 workflow 冗余 |
| 扩展 | `extensions` | `VARIANT` | 可选 | 非筛选扩展；不进列表条件 |

`category_name` 由 `category_code` 在查询或物化时派生，不落权威列。

## 2. 规则引擎最小写入

必填：`tenant_id`、`alert_id`、`alert_display_id`、`alert_name`、`alert_type`、`category_code`、`severity`、`workflow_status=NEW`、`verdict=UNKNOWN`、`created_time`、`updated_time`、`first_seen`、`last_seen`、`dedup_key`。

`alert_id` 由 `tenant_id + dedup_key` 派生后再写，不要先随机生成再配 `dedup_key`。

检测类另填 `rule_id`、`rule_version`、`detection_engine`。`primary_entity_*` 四列**不由规则填写**，由告警写入服务按 §3 从触发事件统一派生。命中事件写入证据表，至少一条 `TRIGGER`。

**实体与枚举投影规范（2026-08-31 修订：primary_entity 改为服务统一派生）**：

- `primary_entity_*` 由写入服务按 §3 算法从触发事件的 `observation.assertion.victim[]` → `assertion.affected[]` → `object` → `assertion.attacker[]`/`subject` 候选链派生：`entity_type` 取实体表枚举（`host` / `ip` / `user` / `account` / `process` / `file` / `domain` / `url` / `service`），`primary_entity_role` 优先 `victim`，观测受影响方用 `affected`，无合格候选时四列全 NULL（合法兜底）。**禁止**用 `product`（产品不是研判实体）、禁止占位值（`0.0.0.0`、`内网IP范围`、空串）充当 `primary_entity_value`、禁止对全部告警统一 `related` 一刀切——那等于放弃实体视角。
- `alert_type` 写入 `05-enums` 定义的闭合枚举值，禁止透传来源裸数字码（如 `"1"`）；`category_code` 禁止空串——无可靠映射时写 `UNKNOWN`。
- `description` / `rule_type` / `detection_engine` 允许为空，但接入层应尽力回填：`description` ← 来源 `analysis_suggestion` 或规则说明，`rule_type` / `detection_engine` ← 来源 `detection_method` / `rule.label`。

## 3. `primary_entity_*` 统一派生算法

规则与接入映射都**不直接填写**这四列；告警写入服务从 TRIGGER 证据指向的触发事件
（`sdm_event_behavior` 行为信封的 `observation.assertion` 与 `subject`/`object`）
按本节算法派生，一处实现、全部来源复用。规则编写人员的责任收缩到事件侧：

1. 受攻击资产 / 行为对象写 `object`（承受行为的实体：dst、被操作对象）；
2. 设备**明确声明**受害方/受影响方/攻击方时写 `observation.assertion.victim[]` /
   `affected[]` / `attacker[]`——声明优先于观测；不声明就只写 `subject`/`object`；
3. `subject`/`object` 是**行为发起者/承受者**（agency 语义），不自动等于攻击者/受害者；
   攻防定性只认 `assertion` 声明。

触发事件判定：`observation.action ∈ {detect, assess}`（此时 `assertion` 必有）；
`record` 事件是纯事实记录，不构成告警触发。

### 3.1 候选收集（按声明强度，强在前）

| 序 | 来源（事件侧路径） | `alert_entity_role` | 判定 |
|---|---|---|---|
| C1 | `observation.assertion.victim[]`（typed entity） | `victim` | 设备明确声明的受害方，最高优先 |
| C2 | `observation.assertion.affected[]`（typed entity） | `affected` | 声明的受影响实体 |
| C3 | `object`（`object_entity_type` + `object_detail`） | `affected` | **观测受影响方；观测角色不得自动升格 victim**。网络穿透类告警（WAF/IDS/探针/流量）的默认判定即此条：object 就是受影响资产，机械可判，不需要逐设备猜 |
| C4 | `observation.assertion.attacker[]`，其次 `subject` | `attacker` | 仅当 C1–C3 无任何候选时才可能成为主对象；用 `subject` 兜底前须确认无 `attacker[]` 声明（subject 是发起者，可能是自卫方） |

**事件实体类型 → 告警实体枚举映射**（告警实体表九值；事件侧 16 值）：

| 事件 `entity_type` | 告警 `entity_type` | 取值 |
|---|---|---|
| `endpoint` | `ip` | `endpoint.ip`（去端口） |
| `host` | `host` | `host.name`（仅 IP 无名时降级 `ip`） |
| `user` / `account` | 同名 | `.name` |
| `process` / `service` / `domain` | 同名 | `.name`（domain 取小写） |
| `file` | 同名 | `file.path`，无路径用 `file.name` |
| `url` | 同名 | `url.full` |
| 其余 7 值（`device`/`resource`/`application`/`cloud`/`container`/`certificate`/`script`） | 不映射，跳过 | 需要时先扩告警实体枚举再修订本表 |

IOC 不作为主对象兜底：`assertion` 未登记 `indicators` 字段，IOC 类候选不进
primary 派生（需要恢复时先在 `object-fields` 登记 `assertion.indicators[]`，
见 07-follow-ups F4）。

### 3.2 过滤与纠正

- 占位值剔除：`0.0.0.0`、`内网IP范围`、空串、`unknown`、`-`（不区分大小写、去首尾空白后比较）。
- 类型纠正：`host` 候选只有 IP 值、无主机名凭证时降级为 `ip`——禁止 `entity_type=host` 挂 IP 值。
- `observation.observer` 不参与主对象竞争。

### 3.3 排序（确定性；与 `sdm_alert_entity` 行同源）

```text
sort_key = (role_rank, type_rank, hint_rank, entity_value 升序)
role_rank: victim=0, affected=1, attacker=2, related=3
type_rank: host=0, user=1, account=2, service=3, ip=4, domain=5, 其余=9
hint_rank: assertion=0, object=1, subject=2, 未声明=9
```

`hint_rank` 是**算法内部概念**，不落库：候选按来源排序（声明 `assertion` = 0、承受者 `object` = 1、
发起者 `subject` = 2、未命中 = 9）。落库列 `sdm_alert_entity.event_role_hint` 是另一回事——它写
**来源出处**（`assertion` / `subject` / `object` / `carrier` / `observer` / `source_alert_field`，
见 [05](05-enums.md)），仅供追溯，不参与排序、派生或查询。

### 3.4 输出与兜底

- `primary_entity_type` / `primary_entity_value` / `primary_entity_role` 取排序首选行。
- `primary_entity_id`：`ip` / `domain` 用 `"{type}:{value}"`（全局域）；`host` / `user` / `account` / `service` 用 `"{type}:{tenant}:{value}"`（租户域）；未列其余类型沿用租户域格式。
- 一致性：被选实体必须在 `sdm_alert_entity` 存在 `is_primary=true` 行，主表四列与该行完全一致（[03](03-evidence-and-entity.md)）。
- **兜底**：无合格候选 → 四列全 NULL。NULL 是合法兜底而不是失败；禁止为凑数编造实体、把 `product` 当实体、或借攻击者实体值顶替受害维度（`dedup_key` 同理，见 [01](01-main-contract.md)）。
- 参考实现：`alert-model/scripts/project_primary_entity.py`。写入服务照此实现；`dedup_key` 的 victim 实体值直接复用本算法在受害/受影响候选中的首选值。
