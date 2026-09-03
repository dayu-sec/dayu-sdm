# topas_waf / topas_waf_attack SDM2 样例

事件事实：客户端对受保护服务器发起 HTTP GET；WAF 判定 SQL 注入并拒绝（403 / action=deny）。

- 主体：`endpoint` `198.51.100.54:64544`
- 客体：`endpoint` `203.0.113.115:80`（HTTP Host=`203.0.113.115`；`server=test` 进 `source_private.server`，不升第二类型）
- 载体：无（HTTP 协议不是载体）
- 观察者：`device` `vendor=topas_waf`；`type=waf` 进 `source_private.observer_class`
- 观察：`action=detect`；断言不反写主体/客体

## 文件

| 文件 | 形态 |
|---|---|
| `runtime_observed.expected-sdm-event.json` | interim 物理五层/投影形（M4 前保留） |
| `runtime_observed.expected-sdm-event.behavior.json` | M3 行为信封（07 Schema） |
| `runtime_observed.behavior-roles.md` | 四角色与 pending 列裁决 |
| `runtime_observed.wpl-to-sdm-event.behavior.json` | M3 行为信封字段映射 |
| `runtime_observed.wpl-to-sdm-event.behavior.md` | 映射评审表 |

## 证据与限制

- 原始样本：`log-model/examples/topas_waf/` 第 1 个非空行。
- WPL 规则：`topas_waf_attack`。
- `pri=warning` → `meta.source_record.log_level`；不得写入顶层 severity。
- 来源 `severity=High` → `observation.assertion.severity=HIGH`，原值进 `source_private.original_severity`。
- `outcome=denied`：处置结果，证据为 `action=deny` 且 `http_status=403`。相对旧物理样例的 `unknown` 已按行为模型升级，见 `behavior-roles.md`。
- `data_src_instance_id` 为空：无采集器实例，也不填进 observer。
- `packet_data`：本条无。
- `mapping_id=topas_waf.topas_waf_attack.behavior.v1`（语义变化必须新值）。

文档证据：天融信《waf2.0日志格式文档-v2.0》；`recorder=waf_attack`。
