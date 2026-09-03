# `edr_dns_access` 样例

本目录保存天擎 DNS 查询日志的真实原始样例、现有 WPL 实际输出、测试平台上下文和预期 SDM2.0 事件。

| 文件 | 用途 |
|---|---|
| `dns_query.raw-log.json` | 天擎 `sample.dat` 第 41 条完整原始日志 |
| `dns_query.wpl-output.json` | 当前 WPL 经 `wpl-check` 验证后的 40 个输出字段 |
| `dns_query.platform-context.json` | 测试夹具提供的平台治理字段 |
| `dns_query.expected-sdm-event.json` | interim 物理五层/投影形（M4 前保留） |
| `dns_query.expected-sdm-event.behavior.json` | M3 行为信封（07 Schema）；见 `dns_query.behavior-roles.md` |
| `dns_query.behavior-roles.md` | 四角色与 pending 列裁决 |
| `dns_query.wpl-to-sdm-event.json` | WPL 字段到 SDM 事件的机器可读映射（interim） |
| `dns_query.wpl-to-sdm-event.md` | WPL 字段映射中文审查文档（interim） |
| `dns_query.wpl-to-sdm-event.behavior.json` | M3 行为信封字段映射 |
| `dns_query.wpl-to-sdm-event.behavior.md` | 映射评审表 |
| `wpl-missing-fields.md` | 当前样例、枚举和协议字段缺口 |

约定（interim 物理 `*.expected-sdm-event.json` 仍按下述旧角色；行为信封以 `dns_query.behavior-roles.md` 为准）：

主体是发起查询的受管终端及其 NETWORK SERVICE 用户，载体是 `svchost.exe`，客体是被查询域名。DNS 应答 IP 位于 `facets.dns.answers[]`，不作为事件 target IP。

## dns_query 行为信封（M3）

- 主体：查询进程 `svchost.exe`（不是 host；旧 expected 的 host+carrier 作废）
- 客体：`domain` `kv501.prod.do.dsp.mp.microsoft.com`
- 载体：空。`execution_host` 仍 `m3_review`；终端进 `profiles.endpoint_asset.host`
- `type=read` / `operation=dns_query` / `outcome=observed`（纠正旧 `success`）
- 对照流量包 `sxf_probe/flow_dns`：本条客体是 domain，不是对端 endpoint
- `mapping_id=tianqing.edr_dns_access.dns_query.behavior.v1`


## 当前物理注册表迁移

本目录 expected 已迁移到当前 87 字段物理注册表。原始日志与映射身份未丢失：原文保存在 `*.raw-log.json`，expected 与 raw_log 的关联统一用 `event_id`，mapping 身份保存在对应映射 JSON/Markdown。
