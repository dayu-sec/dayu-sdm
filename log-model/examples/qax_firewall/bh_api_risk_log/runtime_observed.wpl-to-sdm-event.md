# qax_firewall / bh_api_risk_log 运行时观测候选映射

事件事实：用户 `admin` 从来源地址访问堡垒机 API `/3.0/authService/config`，因后台登录密码错误命中 API 风险检测；来源产品声明该访问已拦截。

主体：`user`；客体：`api_resource`；载体：`http`；观察者：奇安信堡垒机。

> 状态：candidate，未注册、未批准。仅 WPL 解析事实已确认，SDM 语义仍需人工复核。

| WPL 字段 | 值 | SDM 候选路径 | 状态 |
|---|---|---|---|
| `access_time` | `2026-02-03 16:55:13.733618` | `extensions_obj.source_private.access_time` | `source_private` |
| `logType` | `YAB_API_RISK_LOG` | `extensions_obj.source_private.logType` | `source_private` |
| `time` | `2026-01-23 11:00:00` | `occur_time` | `candidate` |
| `souceIp` | `192.xxx.xxx.20` | `roles_obj.source.endpoint.ip + source_ip` | `mapped` |
| `user` | `admin` | `roles_obj.source.user.name + source_user` | `mapped` |
| `prod_name` | `堡垒机` | `extensions_obj.source_private.prod_name` | `source_private` |
| `prod_id` | `f73b12355cd64a4ea36d42ed9c4d1e4e` | `extensions_obj.source_private.prod_id` | `source_private` |
| `prod_version` | `203.0.113.245` | `extensions_obj.source_private.prod_version` | `source_private` |
| `prod_ips` | `[FieldStorage { cur_name: None, value: Owned(Field { meta: Chars, name: "prod_ips/[0]", value: Chars("10.xxx.xxx.127") }) }, FieldStorage { cur_name: None, value: Owned(Field { meta: Chars, name: "prod_ips/[1]", value: Chars("192.xxx.xxx.55") }) }]` | `extensions_obj.source_private.prod_ips` | `source_private` |
| `ipStatus` | `封停` | `source_finding_obj.status + extensions_obj.source_private.ipStatus` | `mapped_with_raw_preserved` |
| `accessApi` | `/3.0/authService/config` | `roles_obj.target.resource.name + facets_obj.http.request.path` | `mapped` |
| `result` | `已拦截` | `source_finding_obj.action` | `mapped` |
| `content` | `登录系统后台，密码错误` | `source_finding_obj.description` | `mapped` |

## 人工语义复核（KB47750）

- 事件事实：用户 `admin` 从来源地址访问堡垒机 API `/3.0/authService/config`，因后台登录密码错误命中 API 风险检测；来源产品声明该访问已拦截。
- event_category：`alert`
- event_type：`network_http`；`accessApi` 明确给出被访问 API 路径，HTTP 方法未知，因此 operation 保持为空。
- operation：`空；无充分标准动作证据`
- outcome：`unknown`；`result=已拦截` 是来源安全控制结论，写入 `source_finding.action`，不替代底层 HTTP 动作结果。
- 证据：奇安信堡垒机 192.0.2.70 Syslog 格式说明 KB47750；对应 `logType` 为 `YAB_API_RISK_LOG`。
- 状态：`reviewed_candidate`
