# qax_firewall / bh_command_operation_log SDM2 候选样例

事件事实：用户 `admin` 经堡垒机向目标资源「主机1」(192.xxx.xxx.40) 上传文件「文件 1」，`result=Success`。

- 主体：`user`（admin / 192.xxx.xxx.20）
- 客体：`file`（文件 1）
- 载体：`none`（无 session / protocol / process）
- 关联：`managed_resource`（主机1 / 192.xxx.xxx.40）
- 观察者：来源安全产品

## 证据与限制

- 原始样本：`s4-doris/models/wpl/qax_firewall/sample.dat` 第 4 个非空行。
- WPL 规则：`bh_command_operation_log` 运行时命中，但规则实际匹配 `YAB_FILE_OPS_LOG`；与 `bh_file_operation_log`/`YAB_CMD_OPS_LOG` 对调。本包不改 WPL。
- `event_type=file_creation`，`operation=upload`：KB47750 §2.4 示例 `operation=Upload`，标准 `file_creation+upload` 为 FULL。
- `outcome=success`：文档 `result` 为 Success/Failed；样本 Success。不是 finding，不映射 `observed`。
- 顶层 `severity` 为空；Syslog PRI `<174>` 不写入安全严重度。
- `size=122.5KB` 带单位，不写入 `target_file_size`。
- `sourcePath`/`targetPath` 为空，文件客体只有文件名。
- 样本 `prod_version=203.0.113.245`，文档 192.0.2.70；字段格式一致。
- logical/physical/projection 校验保持 partial，等待审核冻结。

## 人工语义复核

- 事件事实：用户 admin 经堡垒机向目标资源「主机1」(192.xxx.xxx.40) 上传文件「文件 1」，result=Success。样例 logType 为 YAB_FILE_OPS_LOG（KB47750 §2.4），与目录名 bh_command_operation_log 不一致。
- event_category：`audit`
- event_type：`file_creation`
- operation：`upload`
- outcome：`success`
- 证据：奇安信堡垒机 192.0.2.70 Syslog 格式说明 KB47750 §2.4；对应 `logType` 为 `YAB_FILE_OPS_LOG`。
- 状态：`reviewed_candidate`
