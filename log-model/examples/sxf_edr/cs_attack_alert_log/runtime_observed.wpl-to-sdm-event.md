# sxf_edr / cs_attack_alert_log 运行时观测候选映射

事件事实：深信服 SIP 终端攻击告警（EDR adv_threat_log）——主机 WIN-EX03 上 powershell.exe 访问 lemonduck 挖矿域名，alert_level=4。检测声明在 source_finding。

主体：受攻击终端（source.host=host_name/iplist + source.process=powershell.exe）；客体：挖矿 C2（source_finding，target=null）；载体：`none`；观察者：来源产品。

> 状态：candidate，未注册、未批准。WPL 解析事实与深信服 SIP 文档已确认；SR-059 人工复核结论见文末。

| WPL 字段 | 值 | SDM 候选路径 | 状态 |
|---|---|---|---|
| `access_time` | `2026-06-30 04:04:09` | `extensions_obj.source_private.access_time` | `source_private` |
| `symbol` | `adv_threat_log` | `extensions_obj.source_private.symbol` | `source_private` |
| `chars` | `` | `extensions_obj.source_private.chars` | `source_private` |
| `agent_id` | `3815169755` | `extensions_obj.source_private.agent_id` | `source_private` |
| `alert_describe` | `访问 lemonduck 挖矿的通信域名` | `source_finding_obj.title` | `confirmed` |
| `alert_id` | `94882787-9505-49d4-9024-20DC93AF579B` | `extensions_obj.source_private.alert_id` | `source_private` |
| `alert_level` | `4` | `source_finding_obj.severity` | `confirmed` |
| `details` | `[FieldStorage { cur_name: None, value: Owned(Field { meta: Obj, name: "obj", value: Obj(ObjectValue({"action_time": FieldStorage { cur_name: None, value: Owned(Field { meta: Digit, name: "action_time", value: Digit(1676304603062) }) }, "alert_id": FieldStorage { cur_name: None, value: Owned(Field { meta: Chars, name: "alert_id", value: Chars("94882787-9505-49d4-9024-20DC93AF579B") }) }, "attck_id": FieldStorage { cur_name: None, value: Owned(Field { meta: Chars, name: "attck_id", value: Chars("TA0011.T1071 .004") }) }, "command": FieldStorage { cur_name: None, value: Owned(Field { meta: Chars, name: "command", value: Chars("C:\\\\Windows\\\\System32\\\\WindowsPowerShell\\\\v1.0\\\\powershell.EXE -ep bypass -eSQuAGIAZQA=") }) }, "process_name": FieldStorage { cur_name: None, value: Owned(Field { meta: Chars, name: "process_name", value: Chars("powershell.exe") }) }, "process_path": FieldStorage { cur_name: None, value: Owned(Field { meta: Chars, name: "process_path", value: Chars("C:\\\\Windows\\\\System32\\\\WindowsPowerShell\\\\v1.0\\\\powershell.exe") }) }, "relation": FieldStorage { cur_name: None, value: Owned(Field { meta: Digit, name: "relation", value: Digit(1) }) }, "rule_des": FieldStorage { cur_name: None, value: Owned(Field { meta: Chars, name: "rule_des", value: Chars("进程 powershell.exe 访问 lemonduck 挖矿的通信域名") }) }, "rule_name": FieldStorage { cur_name: None, value: Owned(Field { meta: Chars, name: "rule_name", value: Chars("访问 lemonduck 挖矿的通信域名") }) }})) }) }]` | `extensions_obj.source_private.details` | `source_private` |
| `found_time` | `2023-02-13 16:10:03.062` | `occur_time` | `candidate` |
| `host_name` | `WIN-EX03` | `roles_obj.source.host.name` | `confirmed` |
| `iplist` | `203.0.113.70` | `roles_obj.source.host.ip` | `confirmed` |
| `risk_type` | `2` | `extensions_obj.source_private.risk_type` | `source_private` |
| `save_time` | `1676303865000` | `extensions_obj.source_private.save_time` | `source_private` |

## 人工语义复核（SXF EDR，SR-059）

- 事件事实：深信服 SIP 记录终端攻击告警，攻击结论保留 source_finding。
- `event_category=alert`，`event_type=network_connection`，`outcome=unknown`。
- 主体/客体/载体：受攻击终端（source.host+process）/ 挖矿 C2（source_finding，target=null）/ none
- 检测声明：`source_finding_obj`（title/severity/count/rule{name, attck_id}）
- 来源告警等级保留在 `source_finding`，不机械投影顶层 severity。
- 文档证据：深信服 SIP syslog 格式说明 77 版本；WPL 样本已命中。
