# edr_attack_protection / iexplore_attack_block 行为信封角色判定

句式：进程 `iexplore.exe` 试图 `set` 注册表启动项 `testkey`；攻击防护拦截（`result=1`）。

对照：WAF 是网络 `read`+`denied`。本条是终端注册表 `change`+`denied`。

| 角色 | 判定 | 证据 |
|---|---|---|
| subject | `process` `iexplore.exe` | raw `subject`。WPL 未抽；无 pid/guid，`ref_id` 弱 |
| object | `resource` `testkey` / `kind=registry_value` | raw `object`（`set->testvalue`）。登记字段是 `kind` 不是 `type`；路径进 `facets.registry` |
| carriers[] | 空 | 无进程载体。`execution_host` 仍 `m3_review`；终端进 profiles |
| observer | `application` `tianqing` | 防护引擎是检测方；采集器 → `meta.data_source.instance_id` |
| observation | `action=detect`，`assertion.title/conclusion` | 旧 `source_finding`；`conclusion=deny` 对齐 `outcome=denied` |
| 断言 | 不反写主体/客体 | iexplore 仍是事实层 subject，不是 `assertion.attacker[]` |

## 迁移裁决（相对旧物理 expected）

- `behavior.layer=system` / `type=change` / `operation=set` / `outcome=denied`。
- `record_kind=finding`。无检测严重度，不写 `assertion.severity`，删顶层 `severity=info`。
- `occur_time` 用 WPL `attack_time=1617357947536` → `2021-04-02T10:05:47.536Z`。WPL `create_time` 是资产注册。
- raw `object` 里 `\run` 被 JSON 吃成回车；facet 路径纠正为 `\\run`。
- 厂商 `event_type=11`（脚本攻击）与注册表客体不一致，留 `vendor_event_type`。
- `attack_type=2` / `trigger_mode=20` 无字典，私有。
- `mapping_id=tianqing.edr_attack_protection.iexplore_attack_block.behavior.v1`。

旧 `iexplore_attack_block.expected-sdm-event.json` 保持 interim 物理形，M4 再切投影。
