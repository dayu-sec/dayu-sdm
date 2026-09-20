# edr_dns_access / dns_query 行为信封角色判定

句式：进程 `svchost.exe`（pid 7064）查询域名 `kv501.prod.do.dsp.mp.microsoft.com`，应答 `203.0.113.28`；天擎只记录，无检测断言。

对照：深信服 `flow_dns` 是流量包（`type=flow`，客体=对端 endpoint）。本条是终端 DNS 审计（`type=read`，客体=`domain`）。

| 角色 | 判定 | 证据 |
|---|---|---|
| subject | `process` `svchost.exe` / guid `b4342e1c…` | 查询进程。旧 expected 把 source 标成 `host`、进程进 carriers，违反「只能选一」；矩阵：查询进程或主机，进程更具体 |
| object | `domain` `kv501.prod.do.dsp.mp.microsoft.com` | `dns_host_name`。应答 IP 不升第二客体 |
| carriers[] | 空 | 查询进程已是 subject，不重复进载体。`execution_host` 仍 `m3_review`；终端进 `profiles.endpoint_asset.host` |
| ancestry | 父 `services.exe` → `facets.process.ancestry[]` | `process_parent_*`；无 guid，`ref_id=process::{sha256(path)[:32]}` |
| dns facet | `question.type=A`，`answers[].address`，`response.code=0` | `dns_typed=1`→A（IANA）；`dns_query_status=0` 是协议码，不是执行成功 |
| observer | `application` `tianqing` | 采集器 → `meta.data_source.instance_id` |
| observation | `action=record`，无 assertion | `source_finding_obj=null` |

## 迁移裁决（相对旧物理 expected）

- `behavior.layer=network` / `type=read` / `operation=dns_query` / `outcome=observed`。
- 旧 `outcome=success` 纠正：`dns_query_status=0` 与流量包 `rcode=0` 同类，`record` 无 assertion 不得用执行分段。
- 顶层 `severity=info` 删除。
- `occur_time` `1732787327581` → `2024-11-28T09:48:47.581Z`。
- 应答 `203.0.113.28` 只进 `facets.dns.answers[]`，不写 `target_ip`。
- `report_ip` 与 `ip` 同值，不进 `source_private`。
- MAC：`00-00-5E-00-53-79` → `00:00:5E:00:53:23`。
- `mapping_id=tianqing.edr_dns_access.dns_query.behavior.v1`。

旧 `dns_query.expected-sdm-event.json` 保持 interim 物理形，M4 再切投影。
