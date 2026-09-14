# SDM2.0 Kafka 行为信封消息 Schema

机器可校验 Schema：[`07-sdm-event-behavior-kafka.schema.json`](07-sdm-event-behavior-kafka.schema.json)。

> **通道状态**：本文是 `sdm_event_behavior` 的 Kafka 写入契约，目标表 `sdm_event_behavior`（`031` / `032`）。
> 逻辑信封权威仍是 [`07-sdm-event-behavior.schema.json`](07-sdm-event-behavior.schema.json)（冻结 `2.0`）。
> 旧通道 hybrid-v1 见 [`05-sdm-event-kafka-hybrid-schema.md`](05-sdm-event-kafka-hybrid-schema.md)。两条通道不得混写同一 topic。

## 1. 定义目标

行为通道的 Kafka 消息**不是** hybrid-v1 那种「顶层标量投影 + `*_obj`」。
消息树与 07 逻辑信封相同，只改三个时间字段的物理编码：

```text
07 逻辑信封（date-time）
  meta / event_kind / behavior
  subject / object / carriers
  facets / observation / extensions
        |
        | 仅 meta.occur_time / ingest_time / parse_time → unix 毫秒
        v
Kafka 行为消息（单对象 JSON）
  同一棵树
  032 jsonpaths 按路径抽取标量与 VARIANT
```

字段名、嵌套、必填、`additionalProperties: false` 全部跟 07。
不得为 Kafka 再发明一套扁平列名。

## 2. 消息结构

一条 Kafka 消息 = 一个事件对象，**不要包成数组**（`strip_outer_array=false`）。

| 格子 | 职责 |
|---|---|
| `meta` | 租户、event_id、时间、mapping_id、来源 |
| `event_kind` | 固定 `behavior` |
| `behavior` | 层 / 类型 / 操作 / 结果 |
| `subject` / `object` | 发起者 / 承受者；识别不了写 `null` |
| `carriers` | 承载者数组；没有则 `[]` |
| `facets` | 行为细节 |
| `observation` | 观察者与断言 |
| `extensions` | `source_private` / `profiles` / `enrichments` |

必填与 07 相同：`meta`、`event_kind`、`behavior`、`carriers`。
`meta` 必填：`schema_version`、`tenant_id`、`event_id`、`occur_time`、`mapping_id`。

## 3. 与 07 的唯一编码差

| 路径 | 07 逻辑 | Kafka |
|---|---|---|
| `meta.occur_time` | `string` `date-time` | `integer` unix 毫秒，必填 |
| `meta.ingest_time` | `string` `date-time` 或 `null` | `integer` unix 毫秒或 `null`；缺省 032 填 `NOW(3)` |
| `meta.parse_time` | `string` `date-time` 或 `null` | `integer` unix 毫秒或 `null`；缺省 032 填 `NOW(3)` |
| `observation.observed_at` | `date-time` 或 `null` | **仍为 date-time**（032 不转换） |
| 其余字段 | 07 原样 | 07 原样 |

`schema_version` 是字符串 `2.0`，不是整数 `1`。

032 对三个 meta 时间做秒/毫秒自适应 `FROM_UNIXTIME`；写入 ISO 字符串会装载失败。

## 4. 最小消息示例

```json
{
  "meta": {
    "schema_version": "2.0",
    "tenant_id": "tenant01",
    "event_id": "evt-20260810-000001",
    "occur_time": 1734490098000,
    "ingest_time": 1734490099001,
    "parse_time": 1734490099120,
    "mapping_id": "tianqing.edr_ip_access.inbound_refuse.behavior.v1",
    "data_source": {
      "vendor": "tianqing",
      "product": "edr"
    },
    "source_record": {
      "log_id": "log-tianqing-ip-access-0002",
      "log_type": "edr_ip_access",
      "record_kind": "activity"
    }
  },
  "event_kind": "behavior",
  "behavior": {
    "layer": "network",
    "type": "flow",
    "operation": "connect",
    "outcome": "observed"
  },
  "subject": {
    "ref_id": "endpoint::198.51.100.77",
    "entity_type": "endpoint",
    "endpoint": {
      "ip": "198.51.100.77",
      "port": 54321
    }
  },
  "object": {
    "ref_id": "endpoint::203.0.113.20",
    "entity_type": "endpoint",
    "endpoint": {
      "ip": "203.0.113.20",
      "port": 443
    }
  },
  "carriers": [],
  "facets": {
    "network": {
      "protocol": "tcp",
      "direction": "inbound",
      "connection_result": "refused"
    }
  },
  "observation": {
    "action": "record",
    "observer": {
      "entity_type": "application",
      "application": {
        "vendor": "tianqing"
      }
    },
    "evidence_refs": [
      "source_record:log-tianqing-ip-access-0002"
    ]
  },
  "extensions": {
    "source_private": {},
    "profiles": {},
    "enrichments": {}
  }
}
```

示例只展示结构。对象内部属性以 `object-fields.v1.json` 为准，不得在 Kafka 层另开字段。

## 5. 禁止写入

顶层 `additionalProperties: false`。下列旧通道字段写入应校验失败：

| 禁止 | 行为通道位置 |
|---|---|
| `tenant_id` / `occur_time` / `event_id` 顶层扁平 | `meta.*` |
| `source_ip` / `target_ip` / `device_ip` | `subject` / `object` / `observation.observer` |
| `roles` / `roles_obj` | `subject` / `object` / `carriers` |
| `facets_obj` | `facets` |
| `source_finding` / `source_finding_obj` | `observation.assertion` |
| `extensions_obj` | `extensions` |
| 顶层 `severity` | 日志等级 → `meta.source_record.log_level`；检测严重度 → `observation.assertion.severity` |
| `mapping_revision` / `projection_version` / `quality_status` | 07 已禁，Kafka 同样禁 |
| 消息外层数组 | 单对象 |

## 6. 与 hybrid-v1 / 032 的关系

- 旧通道：扁平 62 标量 + 4 个 `*_obj`，见 05K。
- 本通道：整棵 07 树进 Kafka；032 再按 jsonpaths 投影到 `sdm_event_behavior` 标量/VARIANT。Kafka 层没有第二套投影注册表。
- Doris 标量（`subject_ref_id`、`carrier_role` 等）是 032 的表投影，**不是** Kafka 顶层字段。

## 7. 规范来源

- 逻辑信封：`07-sdm-event-behavior.schema.json`
- 字段目录：`docs/SDM事件模型逻辑契约字段目录.md`
- 对象字段：`log-model/contracts/hybrid-event/object-fields.v1.json`
- 装载：`schema/032_routine_load_sdm_event_behavior.sql`
- 写手：`docs/wparse迁移指南-sdm_event到sdm_event_behavior.md`

生成器 `scripts/generate_sdm_event_behavior_kafka_schema.py` 从 07 复制并只改三个时间字段；人工说明不得覆盖 07 的字段名与约束。
