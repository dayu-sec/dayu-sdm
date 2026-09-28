# CWP 行为流水核心增补样例

`file-permissions.expected-sdm-event.behavior.json` 为**脱敏构造的契约样例**，不是生产输出。GUID、文件摘要、用户组名称均为测试占位，不证明原始 CWP 已提供这些标识。

## 登记与来源转换条件

| 来源 | 核心落位 | 条件 |
|---|---|---|
| file_perm | object.file.mode | 符号权限转四位八进制字符串，特殊位保留，文件类型位剥离 |
| file_owner | object.file.owner.uid / group.uid | 确认 UID:GID 格式再拆；标识转字符串，名称只在来源明确给出时填写 |
| file_atime | facets.file.accessed_time | 已确认单位/epoch 后转带时区 date-time；不当本次 syscall 发生时间 |
| gid | subject.process.real_group.uid | 来源确认真实 GID 后写入；未知/有效组不代填 |
| proc_perm | subject.process.file.mode | 先确认权限属于可执行映像，不能写为 process.integrity |

样例故意使用不同的进程真实组、映像文件属组与被操作文件属组，以防三个角色被混用；`4755` 仅表达权限位，不推断恶意性、提权成功或操作成功。

## 标准依据与兼容性

- ECS 9.2.0 file.mode：八进制权限；file.uid/owner 与 gid/group：属主/属组；process.real_group：真实组，不是有效组。
- OCSF 1.8.0 file.owner.uid/name、file.accessed_time：沿用对象属性命名；SDM 组标识使用 uid，与既有 user.groups.uid 一致。
- 新增字段均可选，保持 schema_version=2.0。来源迁移须使用新 mapping_id；不改已有 process.user.uid、auid/euid 语义。
- gid 未确认、proc_perm 对象未确认、ctime 是否创建时间等条件仍待来源验证。模型获批不等于这些来源事实已经获证。

验证：`python3 log-model/contracts/scripts/test_cwp_activity_extensions.py`。本次不涉及 egid、argv/argc、CWP 告警或生产部署。
