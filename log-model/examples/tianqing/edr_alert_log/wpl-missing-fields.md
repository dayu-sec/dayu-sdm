# `edr_alert_log` WPL 缺失字段定义

> **[历史记录] ldm_alert 穿透链路已废弃（alert-model）**：本文中生成大禹字段 `ldm_alert` 的步骤/映射已从当前交付物删除，仅保留 `sdm_event` finding 阶段有效；SDM2.0 告警模型将重新设计。

本文件依据 `wpl-check sample --rule-name edr_alert_log` 对 RDP 爆破和恶意域名两类真实样例的结果整理。它只描述 WPL 输出缺口，不代表 OML 可以直接读取原始日志字段。

## 1. 原始日志存在但当前输出缺失

| 原始字段 | 当前问题 | 建议 WPL 输出 | 用途 |
|---|---|---|---|
| `description` | 分组解析后只得到 `tmp1/des_ip/tmp2/des_user`，完整正文没有 `description` 输出 | `alert_description` | `source_finding.description`、`ldm_alert.alert_desc` |
| `ioc_alerts` | 仅抽取 `[0][0]` 的若干成员，多组或多项 IOC 会被截断 | `ioc_alerts`，保留完整数组 | 逐项生成 `source_finding.indicators[]` 和告警 IOC 字段 |
| `risky_source` | 只能读取若干子路径，旧 OML 直接 `read(risky_source)` 无稳定对象输出 | `risky_source`，保留完整对象 | 来源产品声明的攻击者信息和处置建议 |

## 2. 已验证为可用、不要重复补充

以下字段虽然旧静态清单曾标记为缺失，但 `wpl-check` 已确认当前规则能够输出：

- `create_time`
- `technique_id`
- `tactic_id`
- `technique`
- `tactic`
- 完整嵌套 `process_details`
- `description_i18n/zh_CN`、`description_i18n/en_US`、`description_i18n/zh_TW`

## 3. 来源样例本身缺失

RDP 爆破样例没有 `compromise_state` 或等价字段，不能由 WPL 补造。`ldm_alert.compromise_status_cd` 需要来源枚举样例、规则判断或平台富化后再填写。

## 4. 描述字段解析风险

当前通过引号位置派生 `des_ip/des_user`。RDP 样例中 `des_ip=203.0.113.31` 正确，但恶意域名样例中相同位置得到 `des_ip=nslookup.exe`、`des_user=blaxaplayer.com`，说明这些别名不是稳定的 IP/用户语义。OML 必须结合 `category_id` 使用，不能把所有 `des_ip` 无条件映射成攻击者或受害者 IP。
