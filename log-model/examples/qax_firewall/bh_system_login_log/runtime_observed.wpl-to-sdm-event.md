# qax_firewall / bh_system_login_log 运行时观测候选映射

事件事实：用户或管理员发起认证/登录相关操作。

主体：`source_user`；客体：`target_device_or_resource`；载体：`observer_product`；观察者：来源产品。

> 状态：candidate，未注册、未批准。仅 WPL 解析事实已确认，SDM 语义仍需人工复核。

| WPL 字段 | 值 | SDM 候选路径 | 状态 |
|---|---|---|---|
| `access_time` | `2026-02-03 16:55:13.733618` | `extensions_obj.source_private.access_time` | `source_private` |
| `logType` | `YAB_SYSTEM_LOGIN_LOG` | `extensions_obj.source_private.logType` | `source_private` |
| `time` | `2026-01-23 11:00:00` | `occur_time` | `candidate` |
| `user` | `admin` | `source_user` | `candidate` |
| `sourceIP` | `192.xxx.xxx.20` | `extensions_obj.source_private.sourceIP` | `source_private` |
| `operation` | `Logged in` | `extensions_obj.source_private.operation` | `source_private` |
| `logonType` | `Web` | `extensions_obj.source_private.logonType` | `source_private` |
| `result` | `Success` | `outcome` | `candidate` |
| `prod_name` | `堡垒机` | `extensions_obj.source_private.prod_name` | `source_private` |
| `prod_id` | `f73b12355cd64a4ea36d42ed9c4d1e4e` | `extensions_obj.source_private.prod_id` | `source_private` |
| `prod_version` | `203.0.113.245` | `extensions_obj.source_private.prod_version` | `source_private` |
| `prod_ips` | `[FieldStorage { cur_name: None, value: Owned(Field { meta: Chars, name: "prod_ips/[0]", value: Chars("10.xxx.xxx.127") }) }, FieldStorage { cur_name: None, value: Owned(Field { meta: Chars, name: "prod_ips/[1]", value: Chars("192.xxx.xxx.55") }) }]` | `extensions_obj.source_private.prod_ips` | `source_private` |

## 人工语义复核（KB47750）

- 事件事实：堡垒机管理员在 Web 等方式发起系统登录，日志给出操作和结果。
- event_category：`auth`
- event_type：`user_login`
- operation：`interactive`
- outcome：`success`
- 证据：奇安信堡垒机 192.0.2.70 Syslog 格式说明 KB47750；对应 `logType` 为 `YAB_SYSTEM_LOGIN_LOG`。
- 状态：`reviewed_candidate`
