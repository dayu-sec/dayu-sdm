# `edr_firewall` 样例（天擎防火墙日志）

本目录用于编写和验收天擎 `edr_firewall` 日志的 OML 与 SDM2.0 映射。

| 文件 | 用途 |
|---|---|
| `qq_rule_hit.raw-log.json` | 天擎真实原始日志 |
| `qq_rule_hit.wpl-output.json` | WPL 输出 |
| `qq_rule_hit.wpl-missing-fields.json` | 规则缺口与故意不抽字段 |
| `qq_rule_hit.platform-context.json` | 平台上下文 |
| `qq_rule_hit.expected-sdm-event.json` | 期望 SDM 事件 |
| `qq_rule_hit.wpl-to-sdm-event.{json,md}` | 逐字段映射 |

## 事件事实

终端 192.0.2.71:49881 访问 198.51.100.21:80（*.qq.com）命中防火墙规则 test（c68176f6-…），方向 2、协议 1、放行 permission=0、累计拦截 2 次。

## 主体 / 客体 / 载体

- 主体：发起端 `192.0.2.71:49881` → `roles.source.endpoint`（src_ip 规则已抽，端口未抽）
- 客体：接收端 `198.51.100.21:80` → `roles.target.endpoint`（dst_ip 规则已抽，端口/hostname 未抽）
- 载体：无进程载体 → `carriers=[]`；协议/方向入 facets.network

## 关键映射决策

- `record_kind=activity`、`event_category=network`、`event_domain=network`：防火墙连接处理为网络活动记录。
- `event_type=network_connection`（06 #35）。
- 防火墙规则 → `source_finding.rule{signature_id, label}`（规则是检测声明）。
- `outcome=denied`：PDF §3.3.1 permission="0"="拒绝"，本条 permission=0。
- direction/protocol 原始值入 `facets.network`（registry 已注册）。

## 未决问题

1. direction（2=流出）/protocol（1=TCP）枚举已由 PDF §3.3.1 确认，原始值入 facets.network，未归一化
2. 原始日志无事件 ID，派生组合兜底

## 当前物理注册表迁移

本目录 expected 已迁移到当前 87 字段物理注册表。原始日志与映射身份未丢失：原文保存在 `*.raw-log.json`，expected 与 raw_log 的关联统一用 `event_id`，mapping 身份保存在对应映射 JSON/Markdown。
