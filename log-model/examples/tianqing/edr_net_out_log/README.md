# `edr_net_out_log` 样例（天擎网络外发日志）

本目录用于编写和验收天擎 `edr_net_out_log` 日志的 OML 与 SDM2.0 映射。

| 文件 | 用途 |
|---|---|
| `baidu_tracert.raw-log.json` | 天擎真实原始日志 |
| `baidu_tracert.wpl-output.json` | WPL 输出 |
| `baidu_tracert.wpl-missing-fields.json` | 规则缺口与故意不抽字段 |
| `baidu_tracert.platform-context.json` | 平台上下文 |
| `baidu_tracert.expected-sdm-event.json` | 期望 SDM 事件 |
| `baidu_tracert.wpl-to-sdm-event.{json,md}` | 逐字段映射 |
| `baidu_tracert.expected-sdm-event.behavior.json` | M3 行为信封（07 Schema）；见 `baidu_tracert.behavior-roles.md` |
| `baidu_tracert.behavior-roles.md` | 四角色与 pending 列裁决 |
| `baidu_tracert.wpl-to-sdm-event.behavior.json` | M3 行为信封字段映射 |
| `baidu_tracert.wpl-to-sdm-event.behavior.md` | 映射评审表 |

## 事件事实

终端对外访问 baidu.com（198.51.100.207）的网络外发检测：is_ok=0、is_down=0、is_vpn=0，附 tracert 路由跟踪文本。

## 主体 / 客体 / 载体

- 主体：发起外联的终端 `DESKTOP-OPCF5JG` → `roles.source.host`；资产画像继续通过 profiles 关联
- 客体：外发目标 `198.51.100.207` → `roles.target.endpoint`（net_out_ip）
- 载体：无进程载体 → `carriers=[]`

## 关键映射决策

- `record_kind=activity`、`event_domain=network`：网络外发检测为网络活动记录。
- `event_type=network_connection`（06 #35）。
- outreach_address（baidu.com）与 tracert 无标准路径，入 source_private。
- `source_original_event_id` 无 uuid，派生组合兜底。


## baidu_tracert 行为信封（M3）

- 主体：`host` `DESKTOP-OPCF5JG`（无进程字段）
- 客体：`endpoint` `198.51.100.207`；`baidu.com` 留 source_private
- 载体：空
- `type=flow` / `operation=connect` / `outcome=observed`
- `mapping_id=tianqing.edr_net_out_log.baidu_tracert.behavior.v1`

## 未决问题

1. is_ok/is_down/is_vpn 枚举待确认
2. tracert 文本较长，是否截断存储待定
3. 原始日志无事件 ID，派生组合兜底

## 当前物理注册表迁移

本目录 expected 已迁移到当前 87 字段物理注册表。原始日志与映射身份未丢失：原文保存在 `*.raw-log.json`，expected 与 raw_log 的关联统一用 `event_id`，mapping 身份保存在对应映射 JSON/Markdown。
