# `edr_process_inject` 字段缺口

- 当前样例没有明确的成功、失败、允许或阻断字段，因此 `outcome=observed`，不能推断为成功。
- `execute_method_name` 为空；当前依据目标线程地址、线程 ID 和线程参数，将注入方式候选归一为 `remote_thread`，仍需天擎方法枚举确认。
- `injected_dll` 为空，不构造注入文件载体；需要补充 DLL 注入样例验证文件对象的落位。
- 当前只有一个 `Process_Injection` 样例，缺少 `load_library`、`queue_apc` 和失败分支。
- 来源只提供目标进程路径，没有目标进程名称；当前从路径 basename 确定性得到 `TrustedInstaller.exe`。
- `report_ip` 与终端 `ip` 不一致，其语义可能是上报链路地址，不作为事件 source IP。
