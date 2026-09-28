# 主机核心增补契约样例

这两个文件是**脱敏构造的契约测试样例**，不是生产日志或已部署规则输出。公钥指纹使用全零摘要编码，仅验证形状，不是真实凭据。

- `core-extensions.expected-sdm-event.behavior.json`：auid=1000、euid=0 与既有 user.uid 分开；syscall=257 配 AUDIT_ARCH=c000003e，返回 3 是来源系统调用返回值，不是进程退出码或攻击成功。terminal=pts/2 是执行上下文。
- `ssh-public-key.expected-sdm-event.behavior.json`：认证用户公钥；ED25519 是密钥算法，SHA256 是摘要算法，value 不含 SHA256: 前缀。用户仍为 account carrier，不放入 facet 身份字段。

来源转换契约：audit.syscall_no → facets.process.syscall.number；audit_arch → syscall.arch；audit.exit_code（实际 syscall exit）→ syscall.return_value；audit.auid/euid → 对应进程实体 auid/euid；auth.tty → facets.process.terminal；auth.key_fp 须解析尾串后拆出公钥算法/摘要算法/指纹值。此处未实现来源解析器，也未改变已有 mapping_id。

未知 UID 与无终端占位省略；不以默认 0 表示缺失。SSH 未识别指纹算法保留私有，不写伪造算法。长参数、argv/argc、GID、文件权限不在本次新增范围。

可选增补兼容信封 2.0，无 DDL 标量列变更。路径登记见逻辑字段目录与 object-fields.v1.json；验证见 contracts/scripts/test_host_core_extensions.py。
