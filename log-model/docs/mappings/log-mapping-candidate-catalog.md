# SDM2.0 日志映射候选目录

生成时间：2026-08-13T02:12:52.590213+00:00

本目录是候选/可评审结果，不是已批准 mapping manifest；不修改 WPL、OML 或标准注册表。

| 日志源 | log_type 数 | 已复用/复核 | partial |
|---|---:|---:|---:|
| `360` | 9 | 0 | 0 |
| `dm_fired_alerts` | 1 | 0 | 1 |
| `dm_terminal` | 1 | 0 | 0 |
| `leadsec` | 5 | 0 | 0 |
| `qax_firewall` | 12 | 0 | 0 |
| `sxf_edr` | 4 | 0 | 0 |
| `sxf_firewall` | 13 | 0 | 0 |
| `sxf_probe` | 4 | 0 | 0 |
| `sxf_vpn` | 3 | 0 | 0 |
| `tianqing` | 24 | 24 | 0 |
| `topas_firewall` | 2 | 0 | 0 |
| `topas_ips` | 9 | 0 | 0 |
| `topas_waf` | 5 | 0 | 0 |

合计：13 个日志源，92 个 log_type。

## 状态定义

- `reused_and_reviewed`：已有天擎样例映射，纳入标准复核。
- `candidate`：有 WPL/样本或文档，已生成候选字段与枚举信号。
- `partial`：缺样本、缺直接文档或存在格式不匹配，不能宣称完整确认。

## 证据与边界

- 枚举选择器保留为 `field_mappings.<source_field>.values.<source_value>.projections` 的候选信号，未知值统一保留原值并报告。
- 没有可信租户上下文时默认 `tenant_id=""`。
- `topas_waf4` 按 `topas_waf` 处理；`jhpt_api_access_log` 排除。
