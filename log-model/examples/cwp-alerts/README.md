# CWP 告警核心字段登记样例

本目录是脱敏构造的契约测试，不是实际日志回放，也不是已上线 OML 输出。

本批五个扩展候选只新增一个 typed process 属性：`egid`。其余复用已登记字段：

| 来源候选 | 核心路径 | 迁移条件 |
|---|---|---|
| 本地提权 egid | 对应进程的 process.egid | 有效 GID；整数，0 保留，unset 哨兵省略 |
| 本地提权 euid | process.euid | 有效 UID，不覆盖真实用户 UID |
| 本地提权 gid | process.real_group.uid | 真实 GID 的规范十进制字符串；来源必须确认真实组语义 |
| 本地提权 proc_file_privilege | process.file.mode | 确认属于映像，符号权限转四位八进制，不含类型位 |
| 木马 file_access_time | facets.file.accessed_time | 确认时间单位/epoch 后转带时区时间；不因位数猜 FILETIME |

`effective-group.expected-sdm-event.behavior.json` 故意使用不同的真实组（1000）、有效组（0）与映像文件属组（1002），仅用于验证角色不能混填。这些数值不描述一次完整的权限变更前后过程；来源告警仍表达 observed，不凭 root 组、SUID/SGID 就推导攻击成功。

`egid` 参考 OCSF 1.8.0 Linux users profile；ECS 9.2 的近义路径为 process.group.id，但 SDM 使用 egid 与既有 euid/auid 保持一致。身份按主机/用户命名空间解释，`real_group.uid` 的现有字符串类型不变。

保持 schema_version=2.0，不改变旧事件必填项。规则迁移另行使用新 mapping_id。测试：`python3 log-model/contracts/scripts/test_cwp_alert_extensions.py`。
