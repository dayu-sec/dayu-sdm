# topas_waf_attack / runtime_observed 行为信封角色判定

句式：客户端 endpoint 对受保护服务器发起 HTTP GET；WAF 判定 SQL 注入并拒绝。

| 角色 | 判定 | 证据 |
|---|---|---|
| subject | `endpoint` `198.51.100.54:64544` | `client_ip` / `sport` / `real_ip` |
| object | `endpoint` `203.0.113.115:80` | `server_ip` / `dport`。旧样例同时挂了 `host.name=test`，违反「只能选一」。HTTP Host 用 raw `host=203.0.113.115`；`server=test` 进 `source_private.server` |
| carriers[] | 空 | 无进程/脚本/会话 ID；`protocol=http` 不是载体 |
| observer | `device`，`vendor=topas_waf`，`ref_id=null` | 安全设备。`product` 不是类型；产品身份留 `meta.data_source.product`。来源 `type=waf` → `extensions.source_private.observer_class` |
| observation | `action=detect`，必有 assertion | `event_type=ATTACK_SQLI`、`msg`/`severity`/`rule_id`/`action=deny` |
| evidence_refs | `source_record:<log_id>` | 原始日志是本条观察的证据；无独立 packet_data |

## 迁移裁决（相对旧物理 expected）

- `behavior.outcome=denied`：新模型区分处置结果与执行结果。证据是 `action=deny` **且** `http_status=403`，不是 finding 标题本身。旧 mapping 的 `outcome=unknown` 把处置当成了「底层动作结果」；本条升级。
- `behavior.operation=http_request`：raw 有 `http_method=GET`、`url`、`http_status`。
- `meta.source_record.log_level=warning` ← `pri`。不得写入顶层 `severity`。
- `observation.assertion.severity=HIGH` ← 来源 `severity=High` 大小写归一；原值 `High` 进 `source_private.original_severity`。
- `data_src_instance_id` 样例为空：不是采集器实例，也不填 observer。
- 未登记 assertion 字段（`count`）进 `source_private.finding_count`，不发明 `assertion.category`。`pri`/`action` 已有标准位，不在 source_private 复写。
- `mapping_id=topas_waf.topas_waf_attack.behavior.v1`：结构与 outcome 语义变化，必须新 mapping_id。

旧 `runtime_observed.expected-sdm-event.json` 保持 interim 物理形，M4 再切投影。
