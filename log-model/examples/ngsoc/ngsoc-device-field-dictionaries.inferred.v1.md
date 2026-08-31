# NGSOC 按设备类型候选字典 v1

状态：`inferred/partial`。本字典来自当前 28 个样例，不是厂商确认字典，也未注册为平台标准。

## 统一结构

每个来源字段只维护“原始枚举值 → 目标字段和值”：

```json
{
  "attackResult": {
    "values": {
      "企图": {
        "projections": {
          "source_finding.attack_result": "attempted",
          "outcome": "observed"
        }
      }
    }
  }
}
```

`preserve_raw_to` 统一声明保留原值的目标路径；`projections` 只写需要归一的枚举。没有出现在这两处的目标字段不得写入。

## 设备选择

| Profile | 设备类型 | 选择器 | 样例数 | 编码形式 |
|---|---|---|---:|---|
| `ngsoc_correlation_engine` | NGSOC 关联分析引擎 | `log_type=ngsoc_alert_info`，来源通常为“关联规则” | 22 | 中文标签 |
| `tianyan_flow_sensor` | 天眼流量传感器 | `extraFields.devName=天眼流量传感器` | 4 | 数值代码 |
| `wangshen_threat_perception` | 网神新一代威胁感知系统 | `extraFields.devName=奇安信网神新一代威胁感知系统` | 2 | 数值代码 |

选择顺序为顶层 `log_type`、设备厂商与名称、fallback。`relevantLogsType` 只作为底层证据类型，不单独决定枚举字典。

## 字段字典

每个设备 profile 下，每个来源字段只占一行；同一字段的多个来源枚举在单元格内合并展示。

`severity` 原值统一保存在 `source_finding.severity` 和 `source_alert_severity`，不在每行重复说明。冲突或未命中的原值统一进入 `extensions.unmapped`。

存在多个目标字段时，枚举结果按“目标字段”列中的顺序一一对应。

| Profile | 来源字段 | 目标字段 | 枚举映射 | 置信度 |
|---|---|---|---|---|
| 关联分析引擎 | `severity` | `severity` | `高危 → error`；`中危 → warning`；`低危 → notice` | 中/中/低 |
| 关联分析引擎 | `attackResult` | `source_finding.attack_result`、`outcome` | `成功 → success/success`；`企图 → attempted/observed` | 高 |
| 关联分析引擎 | `compromiseState` | `source_finding.compromise_status` | `已失陷 → compromised` | 高 |
| 天眼流量传感器 | `severity` | `severity` | `1 → notice`；`2 → warning`；`3 → error` | 中/低/中 |
| 天眼流量传感器 | `attackResult` | `source_finding.attack_result`、`outcome` | `1 → success/success`；`2 → attempted/observed` | 中 |
| 天眼流量传感器 | `compromiseState` | `source_finding.compromise_status` | `true → compromised`；`false → not_compromised` | 高 |
| 网神威胁感知 | `severity` | `severity` | `1 → notice`；`2 → warning`；`3 → error` | 中/低/中 |
| 网神威胁感知 | `attackResult` | `source_finding.attack_result`、`outcome` | `1 → success/success`；`3 → —/unknown` | 低/冲突 |
| 网神威胁感知 | `compromiseState` | `source_finding.compromise_status` | `true → compromised`；`false → not_compromised` | 高 |

## 冲突与回退

- 网神样例中的 `attackResult=3` 与 `compromiseState=false` 同时出现，因此不能复用产品级“3=失陷”推测。
- 未识别设备、未命中值或字段冲突时保留原值；`severity` 留空，`outcome=unknown`，不得猜测正向结果。
- Syslog PRI 只决定 `log_level`，不参与 finding 安全严重度字典。
