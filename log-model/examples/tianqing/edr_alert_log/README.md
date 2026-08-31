# `edr_alert_log` 样例

本目录用于验收天擎来源告警进入 `sdm_event`（`record_kind=finding`）的单阶段映射。

> **告警穿透样例已删除（feature/sdm2-alert-model）**：`*.expected-ldm-alert.json`
> 及其链路说明已移除，SDM2.0 告警模型将重新设计。

| 文件 | 用途 |
|---|---|
| `rdp_bruteforce.raw-log.json` | 天擎完整原始告警 |
| `rdp_bruteforce.wpl-output.json` | 现有 WPL 的实际抽取结果 |
| `rdp_bruteforce.platform-context.json` | 平台日志 ID、处理时间、版本和 POC 富化上下文 |
| `rdp_bruteforce.expected-sdm-event.json` | 来源 finding 事件 |
| `rdp_bruteforce.wpl-to-sdm-event.json` | WPL 字段到 SDM 事件的机器可读映射 |
| `rdp_bruteforce.wpl-to-sdm-event.md` | WPL 字段映射中文审查文档 |
| `wpl-missing-fields.md` | WPL 缺失、截断和不可直接读取字段定义 |

处理链路：

```text
raw alert -> WPL -> sdm_event(record_kind=finding)
```

来源日志血缘以 `sdm_event.log_id` 表达；告警侧血缘关联将由重新设计的 SDM2.0 告警模型定义。

本样例的 GeoIP、资产、系统、组织和方向值来自 `poc-fixture`，用于验证富化字段落位，不是天擎原始日志字段。原始 IP 为私网地址，因此不能将这些 Geo 值理解为真实公网 GeoIP 查询结果。

六条均为来源侧检测：`event_category=alert`，行级 `event_type=generic_event`（事实不同，不合成专用类型），`outcome=observed`。PDF 告警 `status` 是分析处置流，不是动作结果。来源严重度只留 `source_finding`。

除 `rdp_bruteforce` 外，本目录已补充以下去重后的天擎原始告警：

| 样例 | 告警事实 | 备注 |
|---|---|---|
| `ip_detection` | IP 日志检测，触发进程为 `curl.exe` | 原始告警没有 `alert_name`，使用描述作为 finding 标题 |
| `malicious_domain_access` | `nslookup.exe` 访问恶意域名 | 保留 IOC、协议和进程链，未虚构攻击源角色 |
| `account_password_change` | 账户 `NetUser` 密码被修改 | 账户名称仅在告警描述中出现，未构造独立用户实体 |
| `remote_process_start` | 检测到 PsExec/远程启动进程 | `risky_source` 仅作为源设备告警字段保留，未直接等同 attacker |
| `remote_login_failed` | 远程登录失败 | `log_type=flow_skylar_edr_alert_log`，作为同一告警族的变体保留 |

`sample.dat` 第 5、6 行内容完全重复，仅生成一份 `remote_process_start` 样例。

这些样例没有从原始告警中虚构 GeoIP、资产系统、组织和攻击方向；大禹告警中的相关字段应由后续平台富化阶段补充。

## `rdp_bruteforce` 样例的特殊说明

- `roles_obj.source` 为空、`source_host` 无投影:本告警的攻击方在 `source_finding.attacker`（203.0.113.31），不是角色级 source；承载/受害主机 `DESKTOP-NU779RJ` 在 `roles_obj.target` + `target_host` 标量。这是语义正确表达，不是字段缺失。
- `operation` 键存在但为 null:与其他样例"无 operation 键"等价，遵循"空值不落库"约定即可，键有无不构成结构差异。
- 该样例为全量富化样例（含攻击方 GeoIP、sip/dip 资产、状态码家族），是 07 分层规则的 L3/L4 层参考实现；新样例按 07 分层规则只启用实际具备的富化层。

## 当前物理注册表迁移

本目录 expected 已迁移到当前 87 字段物理注册表。原始日志与映射身份未丢失：原文保存在 `*.raw-log.json`，expected 与 raw_log 的关联统一用 `event_id`，mapping 身份保存在对应映射 JSON/Markdown。
