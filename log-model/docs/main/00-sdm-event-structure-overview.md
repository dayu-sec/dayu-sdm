# SDM2.0 事件结构概览

> 本文是 `sdm_event` 的快速入门。详细字段以 05 逻辑字段目录（504 路径）与 06 枚举目录为准。

## 一句话

`sdm_event` 是统一事件表：一张表装所有厂商、所有类型的安全事件。
一个事件 = 一段元数据 + 一组角色 + 若干行为维度 + 一份告警声明 + 扩展区。

```
sdm_event
├── 顶层标量（55 物理列）          检索入口：事件身份 / 时间 / 结果 / 热检索投影
├── roles_obj        (VARIANT)     谁 通过什么 对谁 做了什么 + 关联实体
├── facets_obj       (VARIANT)     行为维度：行为怎么发生的细节
├── source_finding_obj (VARIANT)   设备怎么认定的（告警声明，与客观事实分离）
├── extensions_obj    (VARIANT)     私有扩展、画像、富化、未映射（原文在独立 raw_log 表，经 event_id 回查）
```

## 一、顶层标量 — 检索入口

| 类别 | 字段 |
|---|---|
| 事件身份 | tenant_id、event_id、log_id、log_type、event_type、mapping_id、schema_version |
| 时间（Unix 毫秒） | occur_time、ingest_time、parse_time |
| 结果 | record_kind、event_domain、outcome、severity、operation |
| 热检索投影 | source_host、target_host、source_user、source_ip、source_finding_title 等（从 roles/source_finding 投影，对象不得为标量重复创建） |

## 二、roles_obj — 角色区

| 角色 | 可放对象 |
|---|---|
| source（发起方） | host、process、user、account、endpoint、geo、resource |
| carriers[]（载体） | process、script、resource |
| target（被作用方） | host、process、file、user、account、domain、url、endpoint、service、geo、resource |
| related[]（关联实体） | 上述对象皆可，带 relation_type（父进程、关联主机…） |
| observer（观测设备） | product、device、resource |

要点：同一实体只建一个主对象，其他位置用 `ref_id`（如 `process::xxx`）关联，不重复。

## 三、facets_obj — 行为维度区

| 维度 | 内容 |
|---|---|
| network | protocol、direction、connection_state、zone、traffic、nat、session_id |
| file | 文件操作细节 |
| process | injection（注入细节） |
| authentication | auth_type、auth_result、session_id、auth_failure_reason |
| dns | question、answers[]、response |
| http | request、response、client |
| email | from、recipients[]、attachments[]、subject |
| registry | key、value |
| application / container | name / kubernetes |

## 四、source_finding_obj — 告警声明区

| 类别 | 内容 |
|---|---|
| 基本属性 | title、description、severity、status、count、confidence |
| 分类 | category（original + normalized 两级）、original_category |
| 检测 | rule / rules[]、detection_method、protection |
| 攻击框架 | mitre（technique_id、tactics、techniques）、killchain |
| 攻防双方 | attacker / victim / entities[]（仅源告警明确声明时构造） |
| 指标与漏洞 | indicators[]、ioc、malware、vulnerability、weak_password |
| 处置与证据 | remediation、evidence、attention、window、duration |
| 判定结论 | attack_direction、attack_result、compromise_status |

## 关键设计点

1. **告警与事件分离**：设备检测结论进 source_finding，客观行为事实进 roles/facets。
2. **source/target 是观测角色**，不自动等于 attacker/victim。
3. **原始日志分离存储**：原文在独立 `raw_log` 表，`sdm_event` 与其经 `event_id` 1:1 关联（`raw_log_id` 因恒等于 `event_id` 已于 2026-08-26 退役），不参与字段映射。
4. **时间统一 Unix 毫秒 UTC**。身份两列：`event_id` 是标准化事件的唯一标识（平台分配，与 `raw_log` 1:1）；`log_id` 是原始日志身份——来源有稳定 ID 则填来源 ID，否则与 `event_id` 相同。不再单独保留 `source_original_event_id`。
5. **装不下的才进 extensions**：私有扩展 + profiles（资产画像）+ enrichments（富化）+ unmapped。
