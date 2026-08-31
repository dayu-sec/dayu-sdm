# `edr_powershell_cmd_exec` 字段缺口

## 当前没有缺失的关键进程字段

现有 WPL 经 `wpl-check` 实测输出了 `process_name/path/command_line/guid/id/md5/sha1/sign`、父进程字段、用户 SID、脚本编号和脚本命令。静态规则字段清单没有完整反映公共解析字段，实际映射应以验证输出为准。

## 当前样例为空的字段

- `powershell_payload`：为空，因此不生成 `roles.carriers[].script.content`。
- `context_info`、`user_data`、`report_ipv6`、`custom_group_paths`：为空，不输出占位值。

## 仍需补充的样例

- `powershell_payload` 非空的脚本正文样例；
- 具有明确执行成功或失败结果的样例；
- 能证明脚本具体客体的样例，例如文件、注册表项或网络目标；
- 非 SYSTEM 用户和不同 PowerShell 版本的样例。
