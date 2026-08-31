# `edr_dns_access` 样例

本目录保存天擎 DNS 查询日志的真实原始样例、现有 WPL 实际输出、测试平台上下文和预期 SDM2.0 事件。

| 文件 | 用途 |
|---|---|
| `dns_query.raw-log.json` | 天擎 `sample.dat` 第 41 条完整原始日志 |
| `dns_query.wpl-output.json` | 当前 WPL 经 `wpl-check` 验证后的 40 个输出字段 |
| `dns_query.platform-context.json` | 测试夹具提供的平台治理字段 |
| `dns_query.expected-sdm-event.json` | 预期的 `sdm_event` 物理行 |
| `dns_query.wpl-to-sdm-event.json` | WPL 字段到 SDM 事件的机器可读映射 |
| `dns_query.wpl-to-sdm-event.md` | WPL 字段映射中文审查文档 |
| `wpl-missing-fields.md` | 当前样例、枚举和协议字段缺口 |

主体是发起查询的受管终端及其 NETWORK SERVICE 用户，载体是 `svchost.exe`，客体是被查询域名。DNS 应答 IP 位于 `facets.dns.answers[]`，不作为事件 target IP。

## 当前物理注册表迁移

本目录 expected 已迁移到当前 87 字段物理注册表。原始日志与映射身份未丢失：原文保存在 `*.raw-log.json`，expected 与 raw_log 的关联统一用 `event_id`，mapping 身份保存在对应映射 JSON/Markdown。
