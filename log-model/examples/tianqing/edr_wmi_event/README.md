# `edr_wmi_event` 样例

本目录用于验收天擎 `edr_wmi_event` 的 OML。样例取自 `sample.dat` 中真实的 `wmi_execute` 记录。

| 文件 | 用途 |
|---|---|
| `wmi_execute.raw-log.json` | 天擎完整原始日志 |
| `wmi_execute.wpl-output.json` | WPL 已抽取字段 |
| `wmi_execute.platform-context.json` | 平台处理上下文 |
| `wmi_execute.expected-sdm-event.json` | 期望 SDM2.0 事件 |
| `wmi_execute.wpl-to-sdm-event.json` | WPL 字段到 SDM 事件的机器可读映射 |
| `wmi_execute.wpl-to-sdm-event.md` | WPL 字段映射中文审查文档 |

约定：

- `event_type=wmi_execute` 暂映射为 `event.type=process_uncategorized`，没有受控 operation 时留空，`outcome=observed`。
- 受管终端进入 `roles.source.host`；WMI 服务进程 `process_*` 进入 `roles.carriers[].process`；父进程进入 `roles.related[]`。
- `wmi_filter_wql`、命名空间、WMI 操作和 consumer 字段进入 `extensions_obj.source_private`。当前 WQL 是查询事实，不构造虚假的文件、网络或进程目标。
- 原始日志中的 `source_process_*` 未被 WPL 规则抽取，因此不进入期望事件；它是后续 WPL 完善的输入缺口。
- `task_id`、`sub_task_id`、`logger`、原始 `type`、空 `payload` 和空的 consumer 字段不落库。

## 需要补充的数据

### 原始日志已有、WPL 尚未抽取

以下字段应补充到 `edr_wmi_event` 的 WPL 输出，用于恢复真正的 WMI 请求主体：

| 字段 | 含义 | 预期用途 |
|---|---|---|
| `source_process_name` | 发起 WMI 请求的进程名 | `roles.source.process.name` |
| `source_process_guid` | 发起进程稳定标识 | `roles.source.process.uid` |
| `source_process_id` | 发起进程 PID | `roles.source.process.pid` |
| `source_process_path` | 发起进程路径 | `roles.source.process.path` |
| `source_process_command_line` | 发起进程完整命令行 | `roles.source.process.cmdline` |
| `source_process_md5` | 发起进程映像 MD5 | `roles.source.process.file.hashes.md5` |
| `source_thread_id` | 发起 WMI 调用的线程 ID | 调用线程上下文，标准路径待确认 |
| `source_thread_module_path` | 发起线程所在模块路径 | 调查上下文，空值不输出 |
| `execute_method_name` | WMI 执行方法名称，例如 `WQL` | WMI 私有对象中的执行方法 |
| `execute_method_type` | WMI 执行方法类型，例如 `WmiQuery` | WMI 私有对象中的执行类型 |

补齐后，主体应由 `source_process_*` 构造；当前 `process_*` 仍表示 Winmgmt 服务载体，不能与主体进程合并。

### 需要更多原始样例确认

当前样例的下列字段为空，需要收集非空样例后才能完成 WMI 客体和永久事件订阅映射：

| 字段 | 需要确认的内容 |
|---|---|
| `wmi_namespace` | 实际 WMI 命名空间，例如是否为 `root\\SecurityCenter2` |
| `wmi_operation` | WMI 原始操作枚举及其与标准 operation 的对应关系 |
| `wmi_filter_name` | WMI Filter 的稳定名称和唯一性范围 |
| `wmi_consumer_name` | WMI Consumer 名称 |
| `wmi_consumer_type` | Consumer 类型及完整枚举 |
| `wmi_consumer_destination` | Consumer 执行目标或命令的结构和含义 |
| `wmi_wql_extend` | 扩展 WQL 的结构、与 `wmi_filter_wql` 的关系 |

### 客体的中间表达

当前 WQL 已明确查询 `__InstanceOperationEvent`，最低限度可以将客体表示为：

```json
{
  "ref_id": "resource_wmi_instance_operation_event",
  "entity_type": "resource",
  "resource": {
    "type": "wmi_query",
    "name": "__InstanceOperationEvent"
  }
}
```

完整 WQL 继续保存在 `extensions_obj.source_private.filter_wql`。在命名空间和具体 WMI 对象未确认前，不推断 `root\\SecurityCenter2`，也不把三个 `ISA` 条件类拆成独立目标实体。

## 当前物理注册表迁移

本目录 expected 已迁移到当前 87 字段物理注册表。原始日志与映射身份未丢失：原文保存在 `*.raw-log.json`，expected 与 raw_log 的关联统一用 `event_id`，mapping 身份保存在对应映射 JSON/Markdown。
