# `edr_remote_assistance_file_transfer` 样例（天擎远程协助文件传输日志）

本目录用于编写和验收天擎 `edr_remote_assistance_file_transfer` 日志的 OML 与 SDM2.0 映射。

| 文件 | 用途 |
|---|---|
| `mirrordriver_transfer.raw-log.json` | 天擎真实原始日志 |
| `mirrordriver_transfer.wpl-output.json` | WPL 输出 |
| `mirrordriver_transfer.wpl-missing-fields.json` | 规则缺口与故意不抽字段 |
| `mirrordriver_transfer.platform-context.json` | 平台上下文 |
| `mirrordriver_transfer.expected-sdm-event.json` | 期望 SDM 事件 |
| `mirrordriver_transfer.wpl-to-sdm-event.{json,md}` | 逐字段映射 |

## 事件事实

管理员 admin 通过远程协助传输文件 MirrorDriver.7z（348857 字节）：方向 file_transfer_direction=1、结果 file_transfer_result=1。

## 主体 / 客体 / 载体

- 主体：协助管理员 `admin` → `roles.source.user`（admin_name，规则未抽）
- 客体：传输文件 `MirrorDriver.7z` → `roles.target.file`（file_name/file_size，规则未抽）；受控终端作为 `roles.related.host`
- 载体：远程协助会话（无进程字段，未声明为已观测载体）→ `carriers=[]`

## 关键映射决策

- `record_kind=activity`、`event_domain=endpoint`：文件传输为文件活动记录。
- `event_type=file_copy`（06 #19）：文件传输语义。
- 传输细节（direction/result/initiator）入 source_private。
- `source_original_event_id` = params_id（会话参数 ID，唯一）。

## 未决问题

1. file_transfer_direction/file_transfer_result 枚举待确认（1=成功?）
2. file_copy 的 operation 枚举与传输方向映射待确认
3. 原始日志无事件 ID，params_id 兜底

## 当前物理注册表迁移

本目录 expected 已迁移到当前 87 字段物理注册表。原始日志与映射身份未丢失：原文保存在 `*.raw-log.json`，expected 与 raw_log 的关联统一用 `event_id`，mapping 身份保存在对应映射 JSON/Markdown。
