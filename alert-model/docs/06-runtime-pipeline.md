# 06 运行时流程

## 1. 写入后漏斗

```
告警落库 sdm_alert
  │
  ├─ 等待可选窗口 2–5 分钟（迟到证据）
  │
  └─ GATE（代码，analysis_type=GATE, trigger_mode=ALERT）
        排除 / FP 指纹 / 同 dedup 已有结论 / 缺字段 / 高危加塞
        写 next_hop + conclusion 建议
        │
        ├─ CLOSE_CANDIDATE + 策略命中
        │     分析行 ACCEPTED，verdict 回写，workflow CLOSE
        │     到此结束，不进入自动案件编组；后续仍可人工入案
        │
        └─ REUSE / FULL_AGENT / HUMAN
              先执行案件编组（§1.1）
              再收集 Case 证据并生成证据包（§1.2）
              ├─ REUSE：证据指纹未变化时引用 reuses_analysis_id
              ├─ FULL_AGENT：AI 调查并展开 sdm_analysis_citation
              └─ HUMAN：证据包对人工可见，等待处理
```

案件编组固定在 GATE 之后。只有未被策略自动关单的 `REUSE` / `FULL_AGENT` / `HUMAN` 告警进入自动编组，避免已识别的 FP / BENIGN 噪声先进入调查 Case。`FULL_AGENT` 默认不改正式 `verdict`，输出仍是 conclusion、confidence、cited evidence_id 和不超过 400 字的摘要。

### 1.1 案件编组

案件编组采用「查找候选 Case -> 选择主 Case -> 告警入案」流程。`merge_id` / `correlation_id` 是关联信号，不直接代表 Case，也不直接触发 Case 合并。所有比较都必须先满足同一 `tenant_id`；NULL 和空字符串不参与 `correlation_id` / `merge_id` 相等匹配。

```
待编组 Alert
  │
  ├─ 查找符合状态规则的候选 Case
  │     1. 非空 correlation_id 精确相等                         强关联
  │     2. 非空 merge_id 与 Case 当前成员告警精确相等           较强关联
  │     3. 受限的主实体 + 同规则 + 15 分钟窗口                  弱关联
  │
  ├─ 无候选
  │     创建 case_kind=INVESTIGATION 的 Case
  │     设置 Alert.case_id
  │
  ├─ 一个候选
  │     设置 Alert.case_id 加入该 Case
  │
  └─ 多个候选
        按匹配等级、last_seen DESC、created_time ASC、case_id ASC
        依次确定唯一主 Case
        当前 Alert 只设置主 Case 快照
        不自动执行 Case MERGE
```

匹配等级依次为「非空 `correlation_id` 精确命中 > 非空 `merge_id` 精确命中 > 受限弱关联」。排序只使用上面明确的字段，最终用 `case_id` 兜底，禁止依赖无序查询结果。该规则保证相同输入快照得到相同结果；v0.2 没有持久化完整候选集合，因此不承诺事后重放当时的候选决策。

弱关联只有同时满足以下条件才成为自动入案候选：

1. `primary_entity_id` 非空且精确相等；
2. `primary_entity_role` 为 `victim` 或 `affected`；
3. `primary_entity_type` 在租户白名单中，默认仅 `host` / `user` / `account`；
4. `rule_id` 非空且精确相等；
5. Alert 与 Case 的 `last_seen` 相差不超过 15 分钟（DATETIME(3) 直接比较）；租户可以缩短窗口，不得放宽到无限窗口。

攻击者 IP、公共域名、NAT 地址、共享或服务账号即使短时间重复出现，也不得仅凭该实体自动编入同一 Case。租户应从弱关联实体类型白名单移除共享身份；只有同一实体但不满足上述约束时，仅记关联指标，不设置 `case_id`。

候选 Case 的状态资格如下：

| Case 状态 | 自动入案规则 |
|---|---|
| `INVESTIGATION` + `NEW` / `IN_PROGRESS` | 允许强、较强或受限弱关联 |
| `INVESTIGATION` + `CONFIRMED` | 仅允许非空 `correlation_id` 或 `merge_id` 精确命中 |
| `INCIDENT` 且未关闭 | 仅允许非空 `correlation_id` 精确命中，或租户显式配置的入案策略 |
| `SUPPRESSED` / `CLOSED` | 排除，不参与自动候选 |

多候选时，未选中的 Case ID、匹配等级、选中的主 Case 和 Alert ID 只写结构化应用日志并计入歧义匹配指标；v0.2 不把它作为可操作的“合并建议”落入业务表。需要人工处理的合并建议对象与 Case 谱系后续设计。

MVP 自动编组只为未入案 Alert 设置 `case_id`。Alert 已有 `case_id` 时保持原归属；`MOVE` 、Case 级 `MERGE` / `SPLIT` 以及谱系处理在 `sdm_case_membership` 落地后再实现。

v0.2 由 Case Service 作为 `sdm_alert.case_id` 的唯一写入者。MVP 不写成员历史，不承诺回放入案轨迹；后续启用时按 [07 F3](07-follow-ups.md#f3-case-成员历史延后) 一并落地 CAS / Outbox / 对账。

### 1.2 案件证据收集

新建 Case，或成员集合相对最近一次已完成收集发生实质变化时，进入 2–5 分钟 debounce 队列。证据收集完成后才触发 CASE 分析；重复投递、幂等重试和仅更新时间刷新不重复收集。

```
Case 当前成员
  │
  ├─ 汇总成员 Alert 的已有 Evidence                   只读，不复制
  │
  ├─ 生成受限检索范围
  │     tenant + 实体 + 时间窗口 + 规则 / correlation_id
  │
  ├─ 查询 sdm_event / raw log
  │     按 event_id / raw_log_id 去重，限制条数与 Token
  │
  ├─ 新发现的关联事实写 sdm_evidence
  │     subject_type=CASE
  │     role=CONTEXT / CORROBORATION / NEGATIVE / ENRICHMENT
  │     同一次收集共用 chain_id
  │
  └─ 生成 Case 证据包
        成员 Alert Evidence + Case 自有 Evidence
        → AI / 人工研判 → sdm_analysis_citation
```

首次收集由确定性代码执行，不依赖 AI：默认以 Case 的 `first_seen` / `last_seen` 向前后扩展受限时间窗口，并使用成员告警的 `victim` / `affected` 主体、规则和强关联标识生成查询。禁止只凭攻击者 IP、公共域名、NAT 地址或共享账号无限扩展。每次查询必须限定 `tenant_id`、最大时间跨度、最大返回条数和证据包 Token；未知 `occur_time` 不参与时间推断。

AI 可以提出 FOLLOW_UP 检索请求，但只能调用受控查询模板。此前未见的补充事实使用新的 `chain_id` 和 `phase=FOLLOW_UP` 追加；已存在的同主体、同事实、同角色证据保持原行不变。补充完成后产生新的 CASE 分析；人工补证使用 `phase=MANUAL`。成员 Alert 的已有 TRIGGER 不复制为 CASE Evidence，新检索到的日志才挂 Case。

已有可复用结论且证据指纹未变化时走 REUSE；证据包发生实质变化时必须新增分析行。编组开案不是宣告 Incident；案件轮可以 `SUPERSEDED` 单条告警轮的 benign。

## 2. 闸门顺序（全代码）

1. 租户 allowlist  
2. FP 指纹（`tenant + rule_id + 规范化实体/命令行`）  
3. 同 `dedup_key` 已有 ACCEPTED 分析 → REUSE  
4. 缺 `event_id` 或主实体且类型要求有实体 → INSUFFICIENT_DATA / HUMAN  
5. `severity` 为 HIGH/CRITICAL 且主实体为高价值资产 → FULL_AGENT 或 HUMAN  
6. 其余 → FULL_AGENT 或按租户默认 HUMAN  

命令行规范化：小写、去多余空白与引号、路径分隔统一、数字与 hash 换占位符后再哈希。

## 3. Token 与限流

- 默认禁止长文。Agent 输出契约即分析表字段；引用的 `evidence_id` 必须是租户内唯一 ID，由服务写入 `sdm_analysis_citation`。案件轮可同时引用成员告警证据和本案自有证据；调查中新找到的事实先写入 `sdm_evidence`（`subject_type=CASE`），再 cite，不要回写到某条成员告警上。
- `token_in` / `token_out` / `duration_ms` 必填（Agent 行）。  
- 租户配额用尽：新告警只跑 GATE，或排队；不得丢告警。  
- 同类告警复用优先于再调模型。  
- 案件叙事每个 Case 一篇，不按成员告警乘。

## 4. MSS

- 所有表带 `tenant_id`（客户）。  
- 闸门配置、指纹、策略按租户隔离。  
- 值守 SLA 看告警轮是否产出分析行；MDR 调查 SLA 看 Case；IR / 监管口径只看 `case_kind=INCIDENT`。
- 给客户的报告导出分析行 + 引用证据，不导出内部 GATE 细节也可产品化隐藏。
