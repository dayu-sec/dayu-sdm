# `edr_process_event` 样例

这组样例用于编写和验收 OML：

| 文件 | 用途 |
|---|---|
| `process_creation.raw-log.json` | 天擎真实原始日志（wpl 抽取源，sample.dat） |
| `process_creation.wpl-output.json` | WPL 已抽取结果，模拟 OML 的字段输入 |
| `process_creation.platform-context.json` | 测试夹具提供的租户、日志 ID、采集实例和处理时间 |
| `process_creation.expected-sdm-event.json` | interim 物理五层/投影形（M4 前保留） |
| `process_creation.expected-sdm-event.behavior.json` | M3 行为信封（07 Schema）；见 `process_creation.behavior-roles.md` |
| `process_creation.behavior-roles.md` | 四角色与 pending 列裁决 |
| `process_creation.wpl-to-sdm-event.behavior.json` | M3 行为信封字段映射 |
| `process_creation.wpl-to-sdm-event.behavior.md` | 映射评审表 |
| `process_terminate.raw-log.json` | 天擎真实原始日志（wpl 抽取源，sample.dat） |
| `process_terminate.wpl-output.json` | WPL 抽取结果 |
| `process_terminate.platform-context.json` | 测试夹具自行生成的进程结束事件平台上下文 |
| `process_terminate.expected-sdm-event.json` | 进程结束事件的期望 SDM2.0 事件 |
| `process_terminate.expected-sdm-event.behavior.json` | M3 行为信封（07 Schema）；见 `process_terminate.behavior-roles.md` |
| `process_terminate.behavior-roles.md` | 四角色与 pending 列裁决 |
| `process_terminate.wpl-to-sdm-event.behavior.json` | M3 行为信封字段映射 |
| `process_terminate.wpl-to-sdm-event.behavior.md` | 映射评审表 |

约定（仅约束 interim 物理 `*.expected-sdm-event.json`，行为信封以 `*.behavior-roles.md` 为准）：

- `event_date_creation` 是事件时间，Unix 毫秒。
- `uuid` 是来源原始事件 ID。
- 所有时间字段（`occur_time`、`ingest_time`、`parse_time` 及 roles 对象内 `created_time`/`terminated_time`）统一为 Unix 毫秒，按 UTC 落库（routine load `timezone=Etc/UTC`）。
- WPL 输出包含采集链路传递的 `raw_msg` 源日志原文；缺少的平台治理字段已经在 `platform-context.json` 中补齐。
- `tenant_id` 样例中为空（平台注入）；`data_src_instance_id` 固定为 `collector-tianqing-poc-01`。
- `log_id` 使用按样例固定的稳定测试值；`raw_msg` 装载源日志数据，不使用 ID 或摘要代替。
- `ingest_time`、`parse_time` 固定为事件发生后的测试处理时间。
- 当前进程进入 `roles.target.process`，`process_user` 进入该进程的 `user.name`。
- 当前进程的 SID、用户会话编号、创建/结束时间、工作目录、完整性级别、映像哈希、OriginalFilename、版本和签名主体进入标准 `roles.target.process` 对象。
- 创建事件中，直接父进程是创建主体，进入 `roles.source.process`；祖父进程进入 `roles.related[]`，关系类型为 `grandparent_process`。
- 终止事件无法证明父进程执行了终止，`roles.source` 只表示发生环境主机；父进程和祖父进程进入 `roles.related[]`，关系类型分别为 `parent_process`、`grandparent_process`。
- 两类事件的 `roles.carriers` 均为空，也不生成 `carrier_process_*` 标量投影；父链不再重复保存在来源私有扩展中。
- 终端 IP 是主机属性，写入 `roles.source.host.ip`，不写 `source_ip`。
- 终端 MAC 是受管主机资产属性，写入 `roles.source.host.mac`，不写 `roles.source.endpoint.mac`，也不在来源私有扩展中重复保存。
- `env_version` 写入 endpoint_asset Profile 的 `agent.version`，`asset_oid` 写入 `ownership.organization.id`。
- `asset_id` 写入 `roles.source.host.id`；Profile 只通过 `subject_ref.ref_id` 关联主机，不重复保存版本、角色、实体类型、观察时间、资产 ID/名称和事件来源。
- `task_id`、`sub_task_id`、`logger`、原始 `type`、`custom_group_paths` 和空版权字段不落库；`source_private` 只保留空 envelope。
- 两个 expected 文件中的 `event_id` 按 `tenant_id|mapping_id|uuid` 的 SHA-256 确定性生成。

## process_creation 行为信封（M3）

- 主体：父进程 `svchost.exe`（不是 host；旧 expected 的 host+process 双类型作废）
- 客体：新进程 `WmiPrvSE.exe`
- 载体：空。`execution_host` 仍是 `m3_review`，不在本条冻结；终端属性进 `profiles.endpoint_asset.host`
- 祖父：`facets.process.ancestry[]`
- 观察：`action=record`，无 assertion；采集器实例留 `meta.data_source.instance_id`
- `outcome=observed`；无顶层 severity
- `mapping_id=tianqing.edr_process_event.process_creation.behavior.v1`

## process_terminate 行为信封（M3）

- 主体：`null`。日志证明不了终止者；父进程只是血缘，主机只是执行环境
- 客体：被终止进程 `conhost.exe`
- 载体：空。`execution_host` 仍 `m3_review`
- 血缘：父 `gpupdate.exe` + 祖父 `svchost.exe` → `facets.process.ancestry[]`
- 观察：`action=record`，无 assertion
- `type=disappear` / `operation=terminate` / `outcome=observed`；无顶层 severity
- `mapping_id=tianqing.edr_process_event.process_terminate.behavior.v1`



## 当前物理注册表迁移

本目录 expected 已迁移到当前 87 字段物理注册表。原始日志与映射身份未丢失：原文保存在 `*.raw-log.json`，expected 与 raw_log 的关联统一用 `event_id`，mapping 身份保存在对应映射 JSON/Markdown。
