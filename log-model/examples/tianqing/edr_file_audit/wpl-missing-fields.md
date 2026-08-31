# `edr_file_audit` 字段缺口

- 当前样例只有 `transfer_method=upload_to_site`，缺少下载、复制、移动、删除和访问等动作样例。
- `result=0`、`operation_type=0`、`behavior=0`、`audit_type=2`、`handle=0`、`transfer_channel=4` 均缺少天擎枚举说明，不参与结果或事件类型推断。
- 来源没有稳定事件 ID；`file_id` 是文件标识，不能写入 `source_original_event_id`。当前测试事件 ID 基于稳定 `log_id` 生成。
- `local_file_path` 只有文件名，没有本地目录；不能补造完整本地路径。
- `upload_url` 为空，无法构造目标 URL、域名或网络端点。
- 当前 228 个 WPL 字段中大部分属于终端资产快照和 20 个分组节点，不复制到事件扩展。
- 需要确认 `file_size` 的单位；当前按常见语义候选解释为字节。
