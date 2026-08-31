# SDM2.0 Kafka Hybrid 消息 Schema

机器可校验 Schema：[`05-sdm-event-kafka-hybrid.schema.json`](05-sdm-event-kafka-hybrid.schema.json)。

## 1. 定义目标

Kafka 消息沿用 SDM2.0 逻辑 Schema 的字段语义和对象内部结构，但顶层使用 Kafka/Doris
入库字段名。它不是把 512 个逻辑叶子字段全部改名并展平，而是采用“标量投影 + 权威对象”
的混合结构：

```text
SDM2.0 逻辑事件
  metadata
  event
  roles
  facets
  source_finding
  extensions
        |
        | projection-registry.v1.json
        v
Kafka hybrid-v1 消息
  67 个标准顶层标量投影
  roles_obj
  facets_obj
  source_finding_obj
  extensions_obj
```

逻辑 Schema 决定字段含义、类型和对象内部结构；`projection-registry.v1.json` 决定哪些
逻辑路径需要成为 Kafka 顶层字段、物理字段名以及投影方式。

## 2. 消息结构

Kafka 顶层只允许两类字段：

| 类型 | 职责 | 示例 |
|---|---|---|
| 标量投影字段 | 主键、过滤、聚合和高频检索 | `tenant_id`、`event_type`、`source_ip`、`application_name` |
| 权威对象字段 | 保存完整逻辑对象以及未投影的明细、多值字段 | `roles_obj`、`facets_obj`、`source_finding_obj`、`extensions_obj` |

四个对象字段保持逻辑 Schema 的内部结构，只修改对象在 Kafka 顶层的物理名称：

| 逻辑对象 | Kafka 字段 | 约束 |
|---|---|---|
| `roles` | `roles_obj` | 引用逻辑 Schema 的 `roles` 定义 |
| `facets` | `facets_obj` | 引用逻辑 Schema 的 `facets` 定义 |
| `source_finding` | `source_finding_obj` | 引用逻辑 Schema 的 `source_finding` 定义；非 Finding 事件可为 `null` |
| `extensions` | `extensions_obj` | 引用逻辑 Schema 的 `extensions` 定义 |

因此，`roles.source.endpoint.ip` 在 Kafka 中不是只改名为 `source_ip`。规范写入结果是：

```text
roles.source.endpoint.ip
  -> roles_obj.source.endpoint.ip   权威值
  -> source_ip                      高频标量投影
```

两个位置表达同一语义。`roles_obj` 是权威对象，`source_ip` 是查询投影，两者必须一致。

## 3. 字段映射规则

字段名称和投影方式以
`log-model/contracts/hybrid-event/projection-registry.v1.json` 为唯一依据。典型映射如下：

| 逻辑路径 | Kafka 字段 | 投影方式 |
|---|---|---|
| `metadata.tenant_id` | `tenant_id` | `DIRECT` |
| `metadata.occur_time` | `occur_time` | `NORMALIZED` |
| `event.type` | `event_type` | `NORMALIZED` |
| `event.outcome` | `outcome` | `NORMALIZED` |
| `roles.source.endpoint.ip` | `source_ip` | `NORMALIZED` |
| `roles.target.endpoint.port` | `target_port` | `NORMALIZED` |
| `roles.observer.device.ip_addresses[].address` | `device_ip` | `PRIMARY_ONLY` |
| `facets.network.protocol` | `network_protocol` | `NORMALIZED` |
| `facets.application.name` | `application_name` | `DIRECT` |
| `source_finding.severity` | `source_finding_severity` | `DIRECT` |

投影方式含义：

| 投影方式 | 规则 |
|---|---|
| `DIRECT` | 直接复制逻辑值，不改变语义 |
| `NORMALIZED` | 按该字段的标准化规则输出，例如枚举、IP、时间或协议规范化 |
| `PRIMARY_ONLY` | 逻辑值为多值时，只投影注册表定义的主值；完整值仍保留在对象字段中 |
| `DERIVED` | 按已注册且可复现的规则从逻辑对象派生 |
| `DETAIL` | 投影有界明细或摘要，完整明细仍由权威对象或原始日志保存 |

不得仅凭字段名自行创建顶层列。没有进入 projection registry 的逻辑路径只保留在对应
`*_obj` 中。

## 4. 一致性要求

同一字段同时存在于权威对象和标量投影时，写入端必须保证：

1. 标量投影来源于本条消息的权威逻辑对象，不能由另一套独立映射产生。
2. 单值 `DIRECT` 投影必须与对象值相等。
3. `NORMALIZED`、`DERIVED` 投影必须能按注册规则从对象值复现。
4. `PRIMARY_ONLY` 必须使用注册的主值选择规则，不能依赖数组偶然顺序。
5. 对象值缺失时，不能凭空生成对应标量投影；补充值必须同时带有允许的富化来源。

生产端建议先构造并校验逻辑事件，再由统一 projector 生成 Kafka 消息，避免对象和顶层
标量分别维护造成漂移。

## 5. 必填字段和版本治理

hybrid-v1 消息至少要求：

```text
tenant_id
occur_time
event_id
schema_version
mapping_id
mapping_revision
projection_version
quality_status
roles_obj
facets_obj
source_finding_obj
extensions_obj
```

其中：

- `schema_version` 标识逻辑模型版本，当前允许值为 `1`。
- `projection_version` 标识逻辑到物理的投影版本，当前为 `hybrid-v1`。
- `mapping_revision` 标识实际使用的映射修订版本。
- `quality_status` 当前允许 `ok`、`partial`、`needs_review`、
  `overflow_reference`、`quarantined`。
- `source_finding_obj` 为必备对象列，但非 Finding 事件允许值为 `null`。

## 6. 最小消息示例

```json
{
  "tenant_id": "tenant01",
  "occur_time": 1786352400000,
  "event_id": "evt-20260810-000001",
  "schema_version": 1,
  "mapping_id": "qax.ngsoc.ngsoc_alert_info",
  "mapping_revision": "ngsoc-alert-info-v1",
  "projection_version": "hybrid-v1",
  "quality_status": "ok",
  "record_kind": "finding",
  "event_domain": "threat",
  "event_type": "network_intrusion",
  "severity": "crit",
  "source_ip": "192.0.2.103",
  "target_ip": "203.0.113.124",
  "target_port": 53,
  "application_name": "DNS",
  "roles_obj": {
    "source": {
      "endpoint": {
        "ip": "192.0.2.103"
      }
    },
    "target": {
      "endpoint": {
        "ip": "203.0.113.124",
        "port": 53
      }
    }
  },
  "facets_obj": {
    "application": {
      "name": "DNS"
    },
    "dns": {
      "question": {
        "name": "test.example"
      }
    }
  },
  "source_finding_obj": {
    "title": "公网 IP 地理位置富化验证",
    "severity": "4"
  },
  "extensions_obj": {
    "schema_version": 1,
    "source_private": {},
    "profiles": {},
    "enrichments": {},
    "unmapped": {}
  }
}
```

示例只展示最小结构和少量投影字段，不代表生产消息只能包含这些字段。

## 7. 扩展与超限处理

`extensions_obj` 只允许以下扩展根：

```text
source_private
profiles
enrichments
unmapped
```

标准字段不能复制到 `extensions_obj`。扩展对象最大深度为 8，最大路径数为 256。

对象超过 inline 大小限制时，使用版本策略定义的 `overflow://` 引用，并将
`quality_status` 设置为 `overflow_reference`。当前限制为：

| 对象 | 最大字节数 |
|---|---:|
| `roles_obj` | 16384 |
| `facets_obj` | 32768 |
| `source_finding_obj` | 32768 |
| `extensions_obj` | 65536 |
| 四个对象合计 | 131072 |

## 8. 禁止写入的兼容别名

以下字段只用于旧数据读取兼容，不能由 Kafka producer 写入：

| 旧字段 | 标准字段 |
|---|---|
| `event_category` | `event_domain` |
| `carrier_protocol` | `network_protocol` |
| `source_alert_name` | `source_finding_title` |
| `source_alert_severity` | `source_finding_severity` |
| `source_alert_category` | `source_finding_category` |
| `source_alert_signature_id` | `source_finding_signature_id` |
| `source_alert_action` | `source_finding_action` |
| `source_alert_original_id` | `source_finding_original_id` |
| `extension` | `extensions_obj` |

JSON Schema 顶层使用 `additionalProperties: false`，写入未知字段或旧别名应校验失败。

## 9. 与当前中间版本的关系

本 Schema 描述标准 `hybrid-v1` Kafka 写入契约，共 67 个标量字段和 4 个对象字段。
当前 `01-interim-contract.md` 和旧 Routine Load 描述的是经过裁剪的 55 列中间表契约，且
部分实现仍使用 `roles`、`facets`、`source_finding`、`extensions` 或旧兼容字段名。

两者不能混合作为同一个 Kafka 消息版本使用。采用本 Schema 前，producer、Kafka topic
版本、Routine Load/Doris 表结构和测试夹具必须一起切换到 `hybrid-v1`；旧消息应继续由旧版
入口消费，或经过显式迁移后再写入。

## 10. 规范来源

- 逻辑结构：`05-sdm-event-logical.schema.json`
- 逻辑字段目录：`05-sdm-event-logical-field-catalog.md`
- 物理投影：`log-model/contracts/hybrid-event/projection-registry.v1.json`
- 版本与兼容策略：`log-model/contracts/hybrid-event/version-policy.v1.json`

生成器 `scripts/generate_sdm_event_kafka_schema.py` 根据上述注册表生成机器 Schema；人工说明
不得覆盖注册表中的字段名、类型、投影方式和版本策略。
