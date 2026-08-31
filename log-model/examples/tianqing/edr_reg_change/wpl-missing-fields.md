# `edr_reg_change` 字段缺口

- 当前样例没有成功、失败、允许或阻断字段，因此 `outcome=observed`。
- 当前只有 `registry_set_value` 样例，需要补充键创建、键删除、值删除和键重命名样例。
- `registry_value_details` 与 `registry_value_details_new` 均为 `2`，按字段命名候选解释为变更前后值；需要天擎字段说明确认。
- `registry_value_type=4` 按 Windows 注册表标准类型映射为 `reg_dword`，其他类型代码仍需真实样例覆盖。
- `registry_key_path_renamed` 为空，不输出重命名路径。
- `report_ip` 与终端 `ip` 不一致，其语义可能是上报链路地址，不作为事件 source IP。
