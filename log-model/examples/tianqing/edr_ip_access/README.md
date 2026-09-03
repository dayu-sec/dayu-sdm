# `edr_ip_access` 样例

本目录用于验收天擎 `edr_ip_access` 的 OML 组合和 SDM2.0 映射。

| 文件 | 用途 |
|---|---|
| `outbound_open.wpl-output.json` | 出站连接建立的 WPL 输出 |
| `outbound_open.platform-context.json` | 出站样例的平台上下文 |
| `outbound_open.expected-sdm-event.json` | 出站连接建立的期望 SDM 事件 |
| `outbound_open.expected-sdm-event.behavior.json` | M3 行为信封 |
| `outbound_open.behavior-roles.md` | 四角色裁决 |
| `outbound_open.wpl-to-sdm-event.behavior.json` | M3 字段映射 |
| `outbound_open.wpl-to-sdm-event.behavior.md` | 映射评审表 |
| `inbound_refuse.wpl-output.json` | 入站连接拒绝的 WPL 输出 |
| `inbound_refuse.platform-context.json` | 入站样例的平台上下文 |
| `inbound_refuse.expected-sdm-event.behavior.json` | M3 行为信封 |
| `inbound_refuse.behavior-roles.md` | 四角色裁决 |
| `inbound_refuse.wpl-to-sdm-event.behavior.json` | M3 字段映射 |
| `inbound_refuse.wpl-to-sdm-event.behavior.md` | 映射评审表 |
| `inbound_refuse.expected-sdm-event.json` | 入站连接拒绝的期望 SDM 事件 |

约定：

- `event_date_creation` 是事件发生时间，`timestamp` 是天擎上报时间，均为 Unix 毫秒。
- `event_id` 按 `tenant_id|mapping_id|uuid` 的 SHA-256 确定性生成，前缀 `evt-`；不使用占位值。
- `src_ip_addr/src_port` 和 `dst_ip_addr/dst_port` 分别表示网络主动方和目标方；`inout` 只作为方向事实，不改变两端角色。
- 当前进程是连接的承载进程，进入 `roles.carriers[]`，其父进程进入 `roles.related[]`（`ref_id` 按 `process_` + sha256(tenant_id|父进程名|父进程路径) 前 32 位派生），不重复写入来源或目标进程。
- 终端 `computer_name/ip/mac` 是受管主机资产属性；主机 ID 使用 `asset_id`，Profile 通过 `subject_ref.ref_id` 关联该主机。
- `network_protocol` 同时投影顶层标量（小写）和 `facets.network.protocol`。
- `src_host_name` 为 `unknown` 等缺失占位值时，不写入 `source_host` 标量。
- 进程映像元数据（`process_sign`、`process_version`、`process_md5/sha1`、OriginalFilename、内部名）进入 `roles.carriers[].process.file` 标准路径（registry v17，与 target/source 进程 file 同构）；`custom_group_paths` 和资产分组不重复写入私有扩展（分组只在 endpoint_asset Profile 的 ownership.group），`source_private` 不保存映像元数据。
- 事件动作只使用 SDM `network_connection` 允许的 `open`、`refuse` 等枚举；天擎原始 `event_type` 不原样写入标准字段。


## outbound_open 行为信封（M3）

- 主体：`agent.exe`（不是 host+endpoint）
- 客体：`endpoint` `203.0.113.25:443`
- `type=flow` / `operation=connect` / `outcome=observed`（纠正旧 success）
- `mapping_id=tianqing.edr_ip_access.outbound_open.behavior.v1`

## inbound_refuse 行为信封（M3）

- 主体：外部发起 `endpoint` `198.51.100.77`（受管终端降为客体）
- 客体：`endpoint` `198.51.100.118`（端口 3389 进 typed object）
- 载体：`svchost.exe -k TermService`，`carrier_role=server_process`（第一张用 carriers 的卡）
- `type=flow` / `operation=connect` / `outcome=observed`；拒绝进 `facets.network.connection_result`
- `mapping_id=tianqing.edr_ip_access.inbound_refuse.behavior.v1`


## 当前物理注册表迁移

本目录 expected 已迁移到当前 87 字段物理注册表。原始日志与映射身份未丢失：原文保存在 `*.raw-log.json`，expected 与 raw_log 的关联统一用 `event_id`，mapping 身份保存在对应映射 JSON/Markdown。
