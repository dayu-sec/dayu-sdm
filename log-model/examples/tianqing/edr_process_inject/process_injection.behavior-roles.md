# edr_process_inject / process_injection 行为信封角色判定

句式：进程 `services.exe`（pid 720）向 `TrustedInstaller.exe`（pid 6688）注入远程线程；天擎只记录，无检测断言。

| 角色 | 判定 | 证据 |
|---|---|---|
| subject | `process` `services.exe` / guid `9b131f03…` | 注入进程。旧 expected 把 source 标成 `host` 且并列 `host+process`，违反「只能选一」 |
| object | `process` `TrustedInstaller.exe` / guid `a6a4e1ff…` | `target_process_*`。矩阵：被注入进程 |
| carriers[] | 空 | 注入进程已是 subject。`execution_host` 仍 `m3_review`；终端进 `profiles.endpoint_asset.host` |
| ancestry | 父 `wininit.exe` → `facets.process.ancestry[]` | `process_parent_*`；无 guid，`ref_id=process::{sha256(path)[:32]}` |
| thread | `facets.process.injection.target_thread` | 矩阵：目标线程进 process facet，不升第二进程实体 |
| observer | `application` `tianqing` | 采集器 → `meta.data_source.instance_id` |
| observation | `action=record`，无 assertion | `source_finding_obj=null` |

## 迁移裁决（相对旧物理 expected）

- `behavior.layer=system` / `type=change` / `operation=inject` / `outcome=observed`。
- 旧 `operation=remote_thread` 降为 `facets.process.injection.method`（开放动作名用矩阵 `inject`）。
- 顶层 `severity=info` 删除。
- `occur_time` `1732787303894` → `2024-11-28T09:48:23.894Z`。
- `ip=192.0.2.206` 进 `profiles.host.ip`；`report_ip=203.0.113.45` 进 `source_private`（不同地址）。
- `execute_method_name`、`injected_dll` 为空，丢弃。
- MAC：`00-00-5E-00-53-C6` → `00:00:5E:00:53:CB`。
- `mapping_id=tianqing.edr_process_inject.process_injection.behavior.v1`。

旧 `process_injection.expected-sdm-event.json` 保持 interim 物理形，M4 再切投影。
