# qax_firewall / bh_command_operation_log 运行时观测候选映射

事件事实：用户 `admin` 经堡垒机向目标资源「主机1」(192.xxx.xxx.40) 上传文件「文件 1」，`result=Success`。

主体：`user`；客体：`file`；载体：`none`；关联：`managed_resource`；观察者：来源产品。

> 状态：candidate，未注册、未批准。样本 `logType=YAB_FILE_OPS_LOG`，对应 KB47750 §2.4 文件操作日志；目录名仍为 `bh_command_operation_log`。

| WPL 字段 | 值 | SDM 候选路径 | 状态 |
|---|---|---|---|
| `access_time` | `2026-02-03 16:55:13.733618` | `extensions_obj.source_private.access_time` | `source_private` |
| `logType` | `YAB_FILE_OPS_LOG` | `extensions_obj.source_private.logType` | `source_private` |
| `time` | `2026-01-23 11:00:00` | `occur_time` | `candidate` |
| `user` | `admin` | `source_user` / `roles_obj.source.user.name` | `candidate` |
| `sourceIP` | `192.xxx.xxx.20` | `source_ip` / `roles_obj.source.endpoint.ip` | `candidate` |
| `resource` | `主机1` | `roles_obj.related[0].resource.name` | `candidate` |
| `targetIP` | `192.xxx.xxx.40` | `target_ip` / `roles_obj.related[0].endpoint.ip` | `candidate` |
| `operation` | `Upload` | `operation=upload` | `candidate` |
| `filename` | `文件 1` | `target_file_name` / `roles_obj.target.file.name` | `candidate` |
| `sourcePath` | `` | `extensions_obj.source_private.sourcePath` | `source_private` |
| `targetPath` | `` | `extensions_obj.source_private.targetPath` | `source_private` |
| `size` | `122.5KB` | `extensions_obj.source_private.size` | `source_private` |
| `result` | `Success` | `outcome=success` | `candidate` |
| `prod_name` | `堡垒机` | `extensions_obj.source_private.prod_name` | `source_private` |
| `prod_id` | `f73b12355cd64a4ea36d42ed9c4d1e4e` | `extensions_obj.source_private.prod_id` | `source_private` |
| `prod_version` | `203.0.113.245` | `extensions_obj.source_private.prod_version` | `source_private` |
| `prod_ips` | WPL 数组调试串 | `extensions_obj.source_private.prod_ips` | `source_private` |

## 人工语义复核（KB47750）

- 事件事实：用户 admin 经堡垒机向目标资源「主机1」(192.xxx.xxx.40) 上传文件「文件 1」，result=Success。样例 logType 为 YAB_FILE_OPS_LOG（KB47750 §2.4），与目录名 bh_command_operation_log 不一致。
- event_category：`audit`
- event_type：`file_creation`
- operation：`upload`
- outcome：`success`
- 证据：奇安信堡垒机 192.0.2.70 Syslog 格式说明 KB47750 §2.4；对应 `logType` 为 `YAB_FILE_OPS_LOG`；`result` 文档枚举 Success/Failed。
- 状态：`reviewed_candidate`
