# iexplore_attack_block 行为信封映射

样例：`iexplore_attack_block.expected-sdm-event.behavior.json`  
`mapping_id=tianqing.edr_attack_protection.iexplore_attack_block.behavior.v1`  
旧物理 mapping 保留。

## 相对旧 mapping 的关键纠正

| 来源 | 旧落位 | 新落位 |
|---|---|---|
| raw `subject=iexplore.exe` | `roles.source.process` | `subject.process`（WPL 未抽） |
| raw `object` 注册表 | `resource.type=registry_value` | `resource.kind`；路径进 `facets.registry` |
| `result=1` | `outcome=denied` | 保持 denied；`assertion.conclusion=deny` |
| `source_finding` | 事实层 | `observation.assertion`；`action=detect` |
| 终端 host | `related.execution_host` | `profiles`；不冻结 carriers |
| `severity=info` | 顶层 | 删除；无检测严重度 |
| 厂商 `event_type=11` | 可能当脚本攻击 | `vendor_event_type` 私有 |

WPL 44 字段多数是资产库存，丢弃。主体/客体来自 raw。

校验：`logical_schema=passed`，`semantic_review=passed`；物理投影 `not_run`。
