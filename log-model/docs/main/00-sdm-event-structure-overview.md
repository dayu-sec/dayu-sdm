# SDM2.0 事件结构概览

> 本文是行为信封 **2.0** 的快速入门。权威字段以 [逻辑契约字段目录](../../../docs/SDM事件模型逻辑契约字段目录.md) 与 [07 Schema](07-sdm-event-behavior.schema.json) 为准；闭合枚举见 [06](06-sdm-event-enum-catalog.md)。
> 物理表 `sdm_event_behavior`（DDL 031）。旧五层 `sdm_event` 已冻结。

## 一句话

一条行为事件 = **某主体，经载体，对客体做了一次行为，发生在某切面里，被某观察者记录。**

```
sdm_event_behavior
├── meta                 身份证：租户、event_id、时间、mapping_id、来源
├── event_kind           当前唯一值 behavior（state 暂缓）
├── behavior             层 / 类型 / 动作 / 结果 / 消息
├── subject / object     谁对谁；识别不了写 null
├── carriers[]           载体；没有则 []
├── facets               行为怎么发生的细节
├── observation          谁观察、怎么认定（assertion 不改写事实）
└── extensions           source_private / profiles / enrichments
```

原文在独立 `raw_log`，经 `event_id` 1:1 回查。Kafka 与 07 同树，仅三个时间为 unix 毫秒。

## 一、meta — 身份证

| 类别 | 字段 |
|---|---|
| 身份 | tenant_id、event_id、schema_version=`2.0`、mapping_id |
| 时间 | occur_time、ingest_time、parse_time |
| 来源 | data_source.*、source_record.log_id / log_type / record_kind / log_level |

`event_id` 是标准化事件唯一标识，与 `raw_log` 1:1。`log_id` 是来源日志身份。

## 二、行为句式 — 谁通过什么对谁

| 角色 | 含义 |
|---|---|
| subject | 行为主体（发起者或执行者），可为 null |
| object | 主要客体（直接作用对象），单对象，可为 null |
| carriers[] | 实际承载行为的实体（进程、脚本、代理） |
| observation.observer | 只观察 / 记录 / 判断，不参与行为 |

每个角色是 16 值 `entity_type` + 对应 typed object。同一实体用 `ref_id` 去重。禁止通用 `related`。

## 三、facets — 行为维度

契约登记的 domain（network / http / dns / file / process / authentication / email 等）。切面叶子不是闭合枚举；全量路径见字段目录 2.8。

## 四、observation — 观察与断言

| 格子 | 内容 |
|---|---|
| observer | 设备、引擎、人或 AI |
| action | 观察者做了什么（detect / assess / block 等） |
| assertion | 判断：title、severity、attackers[] / victims[] 是来源主张，不是 subject/object 的第二份 |

`observation.assertion` 不等于平台 `sdm_alert`。

## 关键设计点

1. **事实与判断分离**：客观行为在 subject / object / carriers / facets；判断只在 observation.assertion。
2. **subject/object 是 agency 角色**，不自动等于 attacker/victim。
3. **原文分离**：`raw_log` 存原文，行为表不存 `raw_msg`。
4. **逻辑信封权威**：032 标量是检索锚点，不替代 typed object。
5. **装不下的才进 extensions**：私有扩展 + 资产画像 + 富化。
