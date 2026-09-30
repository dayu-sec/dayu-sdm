# SDM 事件模型逻辑契约字段目录

> 状态：现行权威，`meta.schema_version` = `2.0`。
> 机器契约：`log-model/docs/main/07-sdm-event-behavior.schema.json`。
> 物理表：`sdm_event_behavior`（DDL 031）。旧五层 `sdm_event` 信封已冻结，不作为新写入目标。

## 一、根结构

当前逻辑契约只定义行为内容，`event_kind=behavior`。观察只能依附于行为事件，不能独立成事件；`state` 模型后续单独定义。

```text
sdm_event_behavior
 ├─ meta
 ├─ event_kind: behavior
 ├─ behavior
 ├─ subject                  # 可为 null；按 entity_type 展开 typed object
 ├─ object
 ├─ carriers[]
 ├─ facets
 ├─ observation              # 可选，单对象
 └─ extensions
```

物理落 `sdm_event_behavior`；`sdm_event_state` 暂缓。

## 二、字段目录

### 2.1 `meta`

| 路径 | 类型 | 必填 | 说明 |
|---|---|---:|---|
| `meta.schema_version` | string | 是 | 逻辑契约版本，现行 `2.0` |
| `meta.tenant_id` | string | 是 | 租户标识 |
| `meta.event_id` | string | 是 | 行为事件唯一标识 |
| `meta.occur_time` | datetime | 是 | 行为事实发生时间 |
| `meta.ingest_time` | datetime/null | 否 | 平台接收时间 |
| `meta.parse_time` | datetime/null | 否 | 解析完成时间 |
| `meta.mapping_id` | string | 是 | 不可变映射身份；语义变化必须创建新值 |
| `meta.data_source.vendor` | string/null | 否 | 来源厂商 |
| `meta.data_source.product` | string/null | 否 | 来源产品 |
| `meta.data_source.category` | enum/null | 否 | 来源分类闭集：`auth` / `network` / `audit` / `system` / `alert` / `other` |
| `meta.data_source.instance_id` | string/null | 否 | 接入实例标识；仅表示采集器、连接器、Kafka source 或接入节点，不表示观察者 |
| `meta.source_record.log_id` | string/null | 否 | 来源日志编号 |
| `meta.source_record.record_kind` | enum/null | 否 | 来源记录分类闭集：`activity` / `finding` / `inventory` / `state` / `remediation`；不改变 `event_kind=behavior` |
| `meta.source_record.log_type` | string/null | 否 | 来源日志类型 |
| `meta.source_record.log_level` | string/null | 否 | 原始日志等级；不等同于观察断言严重度 |
| `meta.source_record.log_name` | string/null | 否 | 来源日志名称 |
| `meta.source_record.raw_ref` | string/null | 否 | 原始日志回查引用 |

`meta.data_source` 与 `observation.observer` 必须分开建模：前者回答“消息通过哪个接入链路进入平台”，后者回答“谁实际观察、记录或判断了事件”。如果来源字段表示防火墙、EDR、NGSOC 等产生日志或作出判断的具体实例，应放入 `observation.observer`；如果表示采集器或连接器，则放入 `meta.data_source.instance_id`。两者相同时可以复用同一实例引用，但不得产生两个不同身份。

`mapping_revision`、`projection_version`、`diagnostics` 和 `contract` 不属于事件逻辑字段。

### 2.2 `event_kind`

| 值 | 说明 |
|---|---|
| `behavior` | 有行为主体或可表达为行为事实，表达“谁对谁做了什么” |

`state` 不是本阶段的取值；状态事件类型和字段目录后续单独定义。

### 2.3 行为内容

| 路径 | 类型 | 必填 | 说明 |
|---|---|---:|---|
| `behavior.layer` | enum | 是 | `network`、`system`、`application` |
| `behavior.type` | enum | 否 | `appear`、`read`、`change`、`disappear`、`flow`；来源无法分型时可省略 |
| `behavior.operation` | string/null | 否 | 具体动作，如 `login`、`query`、`write`、`connect` |
| `behavior.outcome` | enum/null | 否 | `allowed`、`denied`、`success`、`failed`、`observed`、`unknown` |
| `behavior.message` | string/null | 否 | 描述行为事实的消息 |

结果语义必须区分：`allowed/denied` 是处置结果，`success/failed` 是执行结果，`observed` 只表示事实被记录，`unknown` 表示来源没有结果。连接建立/DNS 查询/协议状态码（如 `rcode=0`、`connection_established`、`connection_refused`）在 `action=record` 且无 assertion 时不得写成 `success`/`failed` 或 `allowed`/`denied`，应使用 `observed`，协议层结果进对应 facet（如 `facets.network.connection_result`）。

`success`/`failed` 的正向判据：来源字段必须明确陈述**动作本身的执行结果**（如进程退出码、命令执行确认、来源明示的执行成败），且该结果是行为的执行结果而非协议层状态或处置动作。仅有"协议完成/建立/被拒"不构成执行分段；处置动作（拦截、放行）属于 `allowed/denied`，应由 `assertion.conclusion` 支撑。`action=record` 且无 assertion 时默认禁用 `success`/`failed`；确有执行证据的样例，须在映射 writer 中声明证据字段后方可使用。无法满足上述判据时使用 `observed`，来源结果字段进 facet 或 `extensions.source_private`。

### 2.4 `subject`（仅行为，可为 null）

| 路径 | 类型 | 必填 | 说明 |
|---|---|---:|---|
| `subject` | object/null | 否 | 行为主体对象；未采集或无法识别时可省略或为 null |
| `subject.ref_id` | string | 条件必填 | 主体非 null 时的事件内主体引用；主体为 null 时不设置 |
| `subject.entity_type` | enum | 条件必填 | 主体非 null 时必填：user/account/host/endpoint/process/file/service/domain/url/device/resource/application/cloud/container/certificate/script |
| `subject.host` | object/null | 否 | `entity_type=host` 时的主机属性 |
| `subject.process` | object/null | 否 | `entity_type=process` 时的进程属性 |
| `subject.user` | object/null | 否 | `entity_type=user` 时的用户属性 |
| `subject.account` | object/null | 否 | `entity_type=account` 时的账号属性 |
| `subject.endpoint` | object/null | 否 | `entity_type=endpoint` 时的端点属性 |
| `subject.file` | object/null | 否 | `entity_type=file` 时的文件属性 |
| `subject.domain` | object/null | 否 | `entity_type=domain` 时的域名属性 |
| `subject.url` | object/null | 否 | `entity_type=url` 时的 URL 属性 |
| `subject.device` | object/null | 否 | `entity_type=device` 时的设备属性 |
| `subject.resource` | object/null | 否 | `entity_type=resource` 时的资源属性 |
| `subject.service` | object/null | 否 | `entity_type=service` 时的服务属性 |
| `subject.application` | object/null | 否 | `entity_type=application` 时的应用属性 |
| `subject.cloud` | object/null | 否 | `entity_type=cloud` 时的云资源属性 |
| `subject.container` | object/null | 否 | `entity_type=container` 时的容器属性 |
| `subject.certificate` | object/null | 否 | `entity_type=certificate` 时的证书属性 |
| `subject.script` | object/null | 否 | `entity_type=script` 时的脚本属性 |

`subject=null` 只表示主体身份未采集，不表示行为不存在。主体只能选择一个与 `entity_type` 对应的具体对象字段；`geo` 不是独立主体类型，作为 `host` / `endpoint` / `resource` 的可选嵌套。

`ref_id` 统一为 `{entity_type}::{自然键}`：`endpoint::{ip}`（端口只在 typed object，临时端口不参与身份）、`process::{guid}`（无 guid 用 `process::{sha256(小写路径)[:32]}`，Windows 路径大小写不敏感）、`file::{md5}`、`domain::{域名}`、`host::{资产ID}`（与 `host.id` 同一自然键）、`device::{资产ID}`（与 `device.id` 同一自然键）、`account::{账号名}`、`application::{产品名}`。`resource` 无统一自然键，用映射声明的稳定语义键，配对 `resource.id`。同一事件内相同实体必须复用同一 `ref_id`；跨事件的同一实体也必须得到同一 `ref_id`（哈希公式不得随样例漂移）。禁止平行字段 `asset_id`；`endpoint` 的身份就是 `ip`，不登记 `endpoint.id`。资产编号只允许登记在实体 `id`（`host.id` / `device.id` / `resource.id` / `service.id`）或 `{party}.endpoint.asset_id`，同一资产必须同值。

嵌套对象（`geo` / `system` / `organization` / `os` 等）无任何有值叶子时**省略该键**，不得写 `{}`。`未知`、空串、占位 `0` 不构成有值。`geo` 只挂实体对象：`continent_name` / `country` / `country_code` / `province` / `city` / `latitude` / `longitude`；禁止 `facets.network.*.geo`。断言实体数组（`attacker[]` / `victim[]` / `affected[]`）的元素只写身份与角色——`ref_id`、`entity_type` 与同名 typed object；typed object 的叶子必须是 `object-fields.v1.json` 中该类型已登记的叶子，未登记的旧路径按 `wparse-OML字段树迁移处置表.md` 逐条落位。断言实体**允许携带 `geo`，但事实层优先**：同一 `ref_id` 已在 `subject`/`object` 携带 `geo` 时以事实层为准，断言副本只作缺事实层时的兜底，两处同叶子值不一致判错（权威口径见注册表 `assertion.entity_arrays.geo_policy`，旧形状按根级 `geo_leaf_aliases` 归一）。字段名里的 `[]` 是数组记号而非 JSON 键的一部分：物理事件里的键为 `attacker` / `victim` / `affected`。登录用户走 `user`/`account`；CMDB 责任人走 `extensions.profiles.endpoint_asset.ownership.owner`。来源「相关资产列表」不得写入本实体的 `system`。

富化叶子（挂 `subject`/`object` 的 `host`/`endpoint`/`resource`，权威登记在 `object-fields.v1.json`）：

| 路径模式 | 叶子 | 说明 |
|---|---|---|
| `{subject\|object}.host.geo.*` | `continent_name` / `country` / `country_code` / `province` / `city` / `latitude` / `longitude` | 地理位置富化；`endpoint`/`resource` 同形 |
| `{subject\|object}.host.system.*` | `id` / `name` | 所属业务系统（来源或 CMDB 富化） |
| `{subject\|object}.host.organization.*` | `id` / `name` | 所属组织/部门 |
| `{subject\|object}.host.id`、`device.id`、`resource.id` | — | 资产编号，与 `ref_id` 同一自然键；登记位见下 |
| `{subject\|object}.endpoint.asset_id` | — | 资产系统（CMDB/资产中心）里该设备的唯一编号；IP 富化命中后写入，不参与 `ref_id`（端点身份仍是 `ip`），与 `host.id` / `device.id` 同源时必须同值 |
| `{subject\|object}.endpoint.asset_name` / `asset_type` | — | 资产系统里的名称与类型字符串；与 `host.name` / `resource.kind` 同源时必须同值，`asset_type` 是来源归一化值，不得污染 `device.type` 闭集 |

Geo 可选字段补充（host、endpoint、resource 同形）：

| 字段 | 类型 | 含义与取值 |
|---|---|---|
| `geo.continent_name` | string | 大洲名称，统一中文：亚洲、欧洲、非洲、北美洲、南美洲、大洋洲、南极洲；未知省略 |
| `geo.country_code` | string | ISO 3166-1 alpha-2 大写两字母国家/地区代码，如 `CN`、`US`；未知或非标准占位码省略 |

承接既有 IP 富化映射：旧 `{party}.geo.continent.name` → 对应实体的 `geo.continent_name`；旧 `{party}.geo.country.code` → 对应实体的 `geo.country_code`。先按行为角色确定实体，不机械复制旧 roles/source_finding 路径。现有 `geo.country` 继续承载国家/地区名称。本次为可选属性增补，不改变既有字段语义与信封版本 `2.0`。

资产编号与属性落位（`endpoint.asset_*` 与实体字段同源同值）：

| 字段 | 类型 | 含义与取值 |
|---|---|---|
| `{subject\|object}.endpoint.asset_id` | string | 资产系统（CMDB/资产中心）里该设备的唯一编号；IP 富化命中后写入，不参与 `ref_id`（端点身份仍是 `ip`） |
| `{subject\|object}.endpoint.asset_name` | string | 资产系统里的资产名称；与 `host.name`（主机名）口径不同 |
| `{subject\|object}.endpoint.asset_type` | string | 资产系统里的类型字符串（来源归一化值，不是 `device.type` 闭集） |
| `{subject\|object}.host.id` / `device.id` / `resource.id` / `service.id` | string | 同一资产的编号位（见上表） |

来源字段 `asset_id` / `asset_name` / `asset_type` 按行为角色判定实体后写入对应编号与属性位；`asset_oid` 属组织上下文，归 `organization.id`，或留 `extensions.source_private`。判不出实体角色时兜底留 `extensions.source_private.asset_*`。同一事件内 `endpoint.asset_*` 与实体字段（`host.id` / `host.name` / `device.type` / `resource.kind`）若同时存在，必须同值。

CMDB 责任人、Agent、生命周期不在上表：归 `extensions.profiles.endpoint_asset`。

操作系统与设备属性（同一权威登记）：

| 路径模式 | 叶子 | 说明 |
|---|---|---|
| `{subject\|object}.host.os.*` | `name` / `type` / `version` / `bit` / `build` | 操作系统；`bit` 为 32/64 位数（对齐 OCSF `os.cpu_bits`），`build` 为构建号 |
| `{subject\|object}.device.type` | 闭集 | `server` / `desktop` / `laptop` / `tablet` / `mobile` / `virtual` / `iot` / `browser` / `firewall` / `switch` / `hub` / `router` / `ids` / `ips` / `load_balancer` / `other` |
| `{subject\|object}.application.vendor`、`resource.vendor` | — | 厂商；应用厂商对齐 OCSF `application.product.vendor_name` |
| `{subject\|object}.service.id` | — | 服务编号，映射声明的稳定键 |
| `{subject\|object}.host.hw_info.*` | `cores` / `ram_size` / `serial_number` / `vendor_name` / `model` / `bios_ver` / `bios_date` | 硬件画像，解析侧写入；对齐 OCSF `device.hw_info` |
| `{subject\|object}.host.network_interfaces[].*` | `name` / `ip` / `mac` / `hostname` | 网卡列表；对齐 OCSF `network_interface` |
| `{subject\|object}.process.file.*` | `internal_name` / `signatures[].{algorithm,certificate,digest,state}` / `company_name` / `product` / `version` / `desc` | 映像属性；对齐 OCSF `file` 同名子字段 |
| `{subject\|object}.process.integrity` | — | 完整性级别（Windows）；对齐 OCSF `process.integrity` / UDM `integrity_level_rid` |
| `{subject\|object}.file.mode` | string，可选 | 四位八进制 POSIX 权限，参考 ECS file.mode；含特殊权限位，不含文件类型位或 ACL；process.file 同形 |
| `{subject\|object}.file.owner.*` / `.group.*` | `uid` / `name` | 文件属主/属组，字符串标识与名称分开；参考 OCSF owner 与 ECS 属组语义，process.file 同形 |
| `{subject\|object}.process.real_group.*` | `uid` / `name` | 进程真实组，参考 ECS process.real_group；不是有效组、登录会话或附加组全集 |
| `{subject\|object}.process.egid` | integer，可选 | 观测时进程有效 GID，参考 OCSF Linux process.egid；同样适用于 process 载体、观察者与断言实体，见下文 |
| `{subject\|object}.process.auid` / `.euid` | integer，可选 | 审计登录 UID / 观测时有效 UID；对齐 OCSF Linux `process.auid/euid`。同样适用于 process 载体、观察者与断言实体，详见下文 |
| `{subject\|object}.process.created_time` / `terminated_time` / `working_directory` | — | 进程起止时刻与工作目录；对齐 OCSF `process.created_time` / `terminated_time` / `working_directory` |
| `{subject\|object}.user.groups[].*` | `name` / `uid` / `type` | 所属组；对齐 OCSF `group` 对象与 UDM `user.group_identifiers` |
| `observation.assertion.kill_chain[].*` | `phase` | Cyber Kill Chain 阶段；对齐 OCSF `kill_chain_phase`，来源字符串须归一 |

#### 主机进程身份补充（可选属性，2.0 兼容增补）

`process.auid` 是 audit 子系统在登录时赋予、可跨 su/sudo 保留的登录身份；`process.euid` 是观测时有效身份。两者均为整数 0..4294967294，真实 root=0 必须保留；来源 `-1`、`4294967295`、`unset` 和未知值省略，不填 0。数值字符串须验证后转整数；不得把布尔值当 UID。

UID 依赖主机/用户命名空间，来源须关联实际主机，不能当跨主机全局用户身份。auid 不等于 process.user.uid，也不是会话 ID；euid 不代表“变更后 UID”。**不改变既有 process.user.uid 的属主语义**，不同来源须声明其身份角色，不能因 ECS process.user 表示有效用户就覆写 SDM 既有真实 UID 映射。

本次新增字段参考 [OCSF 1.8 Linux users](https://github.com/ocsf/ocsf-schema/blob/1.8.0/extensions/linux/profiles/linux_users.json)。host 批次登记 auid/euid；随后 CWP 行为流水评审增补 real_group、文件权限与属主、访问时刻（见下）。后续 CWP 告警评审登记 egid（见下），argc 仍不在已批准扩展范围。

#### 文件权限、属主与进程真实组（CWP 行为流水评审增补）

所有新属性可选，适用于对应类型的主体、客体、载体、观察者与断言实体；`process.file` 复用同一 file 定义，不新增实体类型。保持信封 2.0，旧事件不要求补字段，来源映射变更须用新 mapping_id。

- `file.mode` 采用 [ECS 9.2 file.mode](https://github.com/elastic/ecs/blob/v9.2.0/schemas/file.yml) 的八进制字符串语义，SDM 规范为四位：`-rw-------` → `0600`，`-rwsr-xr-x` → `4755`。Linux st_mode（如 `0104755`）必须先分离类型位，再保留低 12 位权限；符号权限的 s/S/t/T 要区分 execute 位。真实 `0000` 是合法权限，未知不填 `0000`；数字 600、符号原串、含类型位的长八进制串均不得直接写入。mode 不声称覆盖 ACL/扩展属性，也不由 SUID 位推定恶意性。
- `file.owner.uid/name` 参考 [OCSF 1.8 file.owner](https://github.com/ocsf/ocsf-schema/blob/1.8.0/objects/file.json)，`file.group.uid/name` 承接 ECS `file.gid/group` 的组身份语义，命名沿 SDM 既有 user.groups.uid。两者是仅含 uid/name 的嵌套身份，不把整个 user 对象或组织画像复制进去。uid 为非空字符串、name 为非空名称，至少一项有值；只有数字标识时不编造名字。Linux UID/GID 转规范十进制字符串，`0` 保留，`-1`/`4294967295`/unset 省略；跨平台目录标识可保留来源字符串，但不猜测为本机 UID。`0:0` 复合值须明确来源为 UID:GID 后拆分，不能整体填 uid/name。
- `process.real_group.uid/name` 参考 [ECS 9.2 process.real_group](https://github.com/elastic/ecs/blob/v9.2.0/schemas/group.yml)，uid 沿本项目组标识命名而非照搬 ECS id。uid 是主机/用户命名空间内真实 GID 的规范十进制字符串（0..4294967294），不是整数或带前导零表示。它不是有效组、保存组、附加组列表或 Linux audit 的登录身份；来源 gid 语义未确认时仍留私有。只有一个 root 样例不足以证明真实/有效组等价。
- `file.owner/group` 属于被操作文件；`process.real_group` 属于执行进程；`process.file.mode` 属于进程映像文件。三者不得互相代填。文件 mode/属主/属组反映本次观察的状态，不自动表示操作前后变化，不自动证明操作成功。
- 这些自然键都需主机/目录命名空间上下文；不改变 file/ref_id 或 process/ref_id 的现行身份规则。**OCSF file.uid 是文件本身标识，ECS file.uid 是属主 UID**，本模型明确采用 file.owner.uid，禁止新增含义不清的 file.uid 或旧 owner.id 别名。

#### CWP 告警评审增补：有效组与复用字段

- 新增 `process.egid`，参考 [OCSF 1.8 Linux users profile](https://github.com/ocsf/ocsf-schema/blob/1.8.0/extensions/linux/profiles/linux_users.json) 的有效组 ID。类型与既有 `process.euid/auid` 一致，为 integer 0..4294967294；真实 root 组 `0` 保留，`-1`、`4294967295`、unset、空值省略，不能用 0 代替未知；布尔值与未转换数值字符串均不接受。
- `egid` 表达**观测时有效组**，不是凭据变更后的状态。`real_group.uid` 仍为真实组的规范十进制字符串，不能因两者在某条样例中相等而删除一项，也不能改动真实组字段类型。UID/GID 都依赖主机/用户命名空间；没有对应上下文时不能构造全局组身份。
- 有效组不等于文件属组 `file.group.uid`、进程真实组 `process.real_group.uid` 或附加组列表；不新增含义模糊的 `process.group`，也不把来源 user_group 名称凭空配给 egid。ECS 的 `process.group.id` 表示有效组，此处采用 OCSF egid 命名以避免与 SDM 既有对象树冲突。
- 本批其余四个候选复用已登记字段：木马 `file_access_time` → `facets.file.accessed_time`（先确认 FILETIME/其他编码）；提权 `euid` → 对应 `process.euid`；`gid` → `process.real_group.uid`（先确认真实组语义）；`proc_file_privilege` → `process.file.mode`（符号权限转八进制）。不为每个厂商新增同义路径。
- 这些值是来源证据，不由 euid/egid=0、SUID 权限或记录的处理状态自动推导攻击成功。新样例见 `log-model/examples/cwp-alerts/`，为脱敏构造的结构测试，不宣称来源具备同样完整证据或解析规则已经上线。

本次是行为信封 2.0 的可选 typed object 增补，无新实体类型、必填字段或 Doris 标量列；对象叶子权威为 object-fields.v1.json。07 的开放 process typed object 无需重复维护该属性；校验器按注册表检查身份范围，实际来源迁移仍须使用新 mapping_id。

### 2.5 `object`

| 路径 | 类型 | 必填 | 说明 |
|---|---|---:|---|
| `object` | object/null | 否 | 主要客体对象；未采集、无法识别或不适用时可省略或为 null |
| `object.ref_id` | string | 条件必填 | 客体非 null 时的主要客体引用 |
| `object.entity_type` | enum | 条件必填 | 客体非 null 时必填的主要客体实体类型 |
| `object.host` / `object.process` / `object.user` | object/null | 否 | 与 `object.entity_type` 对应的具体实体属性 |
| `object.account` / `object.endpoint` / `object.file` | object/null | 否 | 与 `object.entity_type` 对应的具体实体属性 |
| `object.service` / `object.domain` / `object.url` | object/null | 否 | 与 `object.entity_type` 对应的具体实体属性 |
| `object.resource` / `object.application` / `object.cloud` | object/null | 否 | 与 `object.entity_type` 对应的具体实体属性 |
| `object.container` / `object.device` / `object.certificate` | object/null | 否 | 与 `object.entity_type` 对应的具体实体属性 |

`object` 保持单数。多个同等客体优先拆成多条事件；来源明确表达集合语义时，才增加受治理的集合型扩展。不能用空对象 `{}` 表示未知，未知统一使用 `null` 或省略该键。具体对象字段必须与 `entity_type` 一致。`object` 的 `geo` / `id` / `system` / `organization` 规则与 `subject` 相同，跟 `entity_type` 走，不强制写成 `host`。

### 2.6 `carriers[]`（仅行为）

| 路径 | 类型 | 必填 | 说明 |
|---|---|---:|---|
| `carriers[]` | array | 是 | 承载或执行行为的实体，可为空 |
| `carriers[].ref_id` | string | 是 | 载体引用 |
| `carriers[].entity_type` | enum | 是 | 载体实体类型 |
| `carriers[].carrier_role` | string | 是 | 载体关系，如 `parent_process`、`script_engine` |
| `carriers[].host/process/file/script` | object/null | 否 | 与 `entity_type` 对应的载体属性 |
| `carriers[].application/service/resource/container` | object/null | 否 | 与 `entity_type` 对应的载体属性 |
| `carriers[].account` | object/null | 否 | 与 `entity_type=account` 对应的载体属性（`name`） |

协议、方向和具有明确领域语义的会话值不放入 `carriers[]`，进入对应 `facets`；跨域关联键模型暂缓定义。

**登录/认证类事件的账号落位**：被登录账号是日志记录的事实，不是观察者的判断。当同一事件的两端地址已按角色占用 `subject.endpoint` / `object.endpoint`（登录来源与登录目标主机），账号没有第二个角色位，此时统一写成**载体**：`carriers[]` 元素 `entity_type=account`、`carrier_role=principal`、`ref_id=account::{账号名}`，属性对象只写 `account.name`。据此：

- 不得把被登录账号写进 `observation.assertion.affected[]`（`assertion` 承载来源主张，不承载日志已记录的事实）；
- 不得写进 `facets`（`facets` 不承载实体身份，见 §2.8）；
- 来源确实额外声明了"受影响账号"时，那是断言，按 §2.10 写 `assertion.affected[]`，与事实层的账号载体并存但语义不同；
- 事件里没有两端地址冲突时，账号仍可正常作为 `subject`/`object`（`account::{账号名}` 为登记自然键）。

### 2.7 `state`（暂缓）

状态字段、状态客体规则和 `sdm_event_state` 物理表不属于本阶段逻辑契约，后续单独定义。

### 2.8 `facets`

`facets` 只承载有明确领域语义的行为上下文，不是实体对象。07 Schema 登记 16 个候选域，内部为开放对象（不进 `object-fields.v1`）。禁止 `facets.related`。

身份键仍在 `subject` / `object` / `carriers`：进程、文件、域名、URL、容器实体不因进入 facet 而改类型。登录/认证账号同理是实体：按 §2.6 走 `carriers[]`（`entity_type=account`），不登记为 facet 叶子，也不以字符串形式落在 `facets.authentication.*`。

`facets.http.request.path` / `facets.http.request.query` 是 HTTP 事务上下文的例外说明：它们承载本次请求的 request-target 组成，**不是 URL 实体身份**。来源只给出相对 request-target（如 `/a/b?x=1`）时，不得据此补全 scheme/authority 写成 `object.url.full`；只有来源明确给出绝对 URL 且该 URL 被裁定为事件主要客体时，才走 `object.url.full/path/query`。同一事实不得在 facet 与 `object.url` 两处重复表达。

拆分只按**第一个 `?`** 切分，保留原始百分号编码，不做 URL decode、路径归一化、参数排序或大小写转换。request-target 不含 fragment，`#` 不是分隔符：出现字面 `#`、CONNECT 的 authority-form、OPTIONS 的 `*`、空值与其它异常形态时不得臆造拆分，原值保留在 `extensions.source_private` 或 raw_log。多值 request-target（如来源 `urls[]`）不取第一个充当唯一事实；原数组保留在来源私有区或拆成多条事件。

`facets.http.request.query` 常含 token、会话与个人身份信息，按敏感 HTTP 数据执行字段级访问控制与展示遮罩；不得为检索便利做 URL decode 或键值展开；超长或敏感值由来源契约决定是否截断，禁止静默截断。

两个叶子无值时**省略**。已知实现差距（2026-09-30 实测）：warp-parse 写入链不在 facet 层省略空值，同结构的 `facets.http.request.host` / `.method` 同样如此，落库可能是空串；**查询侧须把空串与缺失一并视为无值**，待引擎支持条件字段后收敛。

这两个叶子是开放 facet 域内的可选补登记，不改 07 结构、无物理列、无必填与闭集变更，保持 `meta.schema_version=2.0`；映射开始实际写入时必须换新的 `mapping_id`。

16 域：`network`、`http`、`dns`、`tls`、`email`、`process`、`file`、`authentication`、`authorization`、`registry`、`application`、`container`、`database`、`peripheral`、`cloud`、`ics`。

典型路径（∪ 字段目录既有行、06 开放/闭合字段、迁移矩阵、05 仍标 facet-open 的路径）。未列叶子须先有已验证样例再补，不得发明。

| 域 | 路径 | 说明 |
|---|---|---|
| network | `facets.network.connection_result` | 协议层连接结果（established/refused 等）；不是 `behavior.outcome` |
| network | `facets.network.protocol` | 传输层或来源协议标识 |
| network | `facets.network.direction` | 网络方向，未闭合 |
| network | `facets.network.application_protocol` | 应用层协议（如 https）；与 `protocol` 分轨 |
| network | `facets.network.packet_metadata` | 解析出的包级元数据；不承载完整原文 |
| network | `facets.network.session_id` | 网络领域会话；跨域关联键暂缓 |
| network | `facets.network.session.start_time` | string/date-time；网络流会话开始时刻，带时区，推荐 UTC；不是日志生成时间或认证会话开始时间 |
| network | `facets.network.session.end_time` | string/date-time；网络流会话结束时刻，带时区，推荐 UTC；未结束或未知时省略，不以日志时间代填 |
| network | `facets.network.session.duration_seconds` | number，非负秒数，可含小数；来源报告的网络会话时长，或在来源缺失时由有效起止时刻派生；精度与冲突规则见下文 |
| network | `facets.network.traffic.bytes_in` | integer，非负字节数；相对于来源契约明确标识的被监控通信端的接收量，不是采集器或任意接口的入流量 |
| network | `facets.network.traffic.bytes_out` | integer，非负字节数；与 bytes_in 相同被监控通信端的发送量，方向参照和统计范围必须一致 |
| network | `facets.network.traffic.total_bytes` | integer，非负字节数；同一统计范围的双向总量；来源缺失时仅可由完整且同口径的两方向计数求和 |
| network | `facets.network.traffic.request_bytes` | integer，非负字节数；网络会话发起方到响应方的方向计数，不是单次 HTTP 请求正文长度 |
| network | `facets.network.traffic.request_packets` | integer，非负包数；与 request_bytes 同方向、同统计范围 |
| network | `facets.network.traffic.response_bytes` | integer，非负字节数；网络会话响应方到发起方的方向计数，不是单次 HTTP 响应正文长度 |
| network | `facets.network.traffic.response_packets` | integer，非负包数；与 response_bytes 同方向、同统计范围 |
| network | `facets.network.nat.original/translated.*` | NAT 原/译地址与端口，由来源契约映射 |
| network | `facets.network.source_zone` | 源网络区域，字符串；对齐 OCSF `device.zone`，不建 `.id` 对象 |
| network | `facets.network.target_zone` | 目的网络区域，字符串；对齐 OCSF `network_endpoint.zone`，不建 `.id` 对象 |
| http | `facets.http.request.method` | HTTP 请求方法 |
| http | `facets.http.request.host` | HTTP 请求主机 |
| http | `facets.http.request.path` | HTTP request-target 的 path 部分；只按第一个 `?` 拆分，不含 query 与 fragment，保留原始编码；只有 origin-form（`/…`）与 OPTIONS 的 `*` 才写 |
| http | `facets.http.request.query` | HTTP request-target 中 `?` 后的原始查询串，不含前导 `?`；保留原始编码与参数顺序；可能含凭证与个人信息，按敏感字段治理 |
| http | `facets.http.request.user_agent` | User-Agent |
| http | `facets.http.request.referer` | Referer |
| http | `facets.http.request.forwarded_for[].ip` | X-Forwarded-For 链 |
| http | `facets.http.response.status_code` | HTTP 响应状态码 |
| dns | `facets.dns.question.name` | DNS 查询名 |
| dns | `facets.dns.question.type` | 查询记录类型 |
| dns | `facets.dns.question.class` | 查询类别（QCLASS） |
| dns | `facets.dns.answers[]` | 应答记录数组（RFC1035 Resource Record；对齐 OCSF `dns_resource_record` 与 UDM `Dns.ResourceRecord`） |
| dns | `facets.dns.answers[].name` / `.type` / `.class` / `.ttl` | 应答记录名、类型、类别、TTL |
| dns | `facets.dns.answers[].address` | 应答地址（`RData` 归一；非地址型应答放 `extensions.source_private`） |
| dns | `facets.dns.response.code` | 应答状态码（如 rcode）；不是 `behavior.outcome` |
| dns | `facets.dns.header.opcode` | DNS 操作码；隧道/投毒/放大判定用 |
| dns | `facets.dns.header.authoritative` | AA 权威应答标志 |
| dns | `facets.dns.header.truncated` | TC 截断标志 |
| dns | `facets.dns.header.recursion_desired` | RD 期望递归标志；`transaction_id` 是关联键，本阶段不登记 |
| tls | `facets.tls` | 握手细节（版本、套件、证书指纹等）；叶子随已验证样例补登记 |
| email | `facets.email.from` | 发件人（身份实体仍在 subject/object） |
| email | `facets.email.subject` | 邮件主题 |
| email | `facets.email.recipients[]` | 收件人 |
| email | `facets.email.cc[]` | 抄送 |
| email | `facets.email.attachments[]` | 附件（文件实体在 object/carriers） |
| process | `facets.process.ancestry[]` | 父进程与创建链；进程身份在 subject/carriers |
| process | `facets.process.syscall.number` | integer，0..4294967295；系统调用编号，必须同时有 syscall.arch，不凭编号跨 ABI 解码 |
| process | `facets.process.syscall.arch` | string；来源 ABI 编码，如 Linux AUDIT_ARCH=c000003e/aarch64 对应编码；不是主机 OS 位数 |
| process | `facets.process.syscall.return_value` | integer，有符号 64 位；系统调用返回值（fd/字节数/负 errno 等），不是进程退出码 |
| process | `facets.process.terminal` | string；本次执行/会话的终端名称，如 pts/2；无终端及未知占位省略，不当 session_id |
| process | `facets.process.injection.method` | 注入方式 |
| process | `facets.process.injection.target_thread.*` | 被注入线程编号、入口、模块路径 |
| file | `facets.file` | 本次文件操作上下文；文件身份在 subject/object.file，叶子随样例补登记 |
| authentication | `facets.authentication.auth_type` | 认证方式，未闭合 |
| authentication | `facets.authentication.public_key.algorithm` | string，可选；认证用户公钥的密钥算法，如 ED25519/RSA，不是摘要算法 |
| authentication | `facets.authentication.public_key.fingerprint.algorithm` | string；本阶段闭集 SHA256/MD5，指纹非空时必填；未知算法留私有 |
| authentication | `facets.authentication.public_key.fingerprint.value` | string；去除算法前缀的指纹值：SHA256 为无 padding Base64，MD5 为小写冒号分隔十六进制 |
| authentication | `facets.authentication.session.start_time` | 认证会话开始时刻，来自来源 |
| authentication | `facets.authentication.session.end_time` | 认证会话结束时刻，来自来源；时长由区间派生 |
| authentication | `facets.authentication.auth_result` | 认证结果，不是 `behavior.outcome` |
| authentication | `facets.authentication.auth_failure_reason` | 失败原因 |
| authentication | `facets.authentication.session_id` | 认证会话编号 |
| authorization | `facets.authorization.approvers[]` | 审批人与授权链 |
| registry | `facets.registry.key.path` | 被操作键路径 |
| registry | `facets.registry.key.renamed_path` | 重命名后路径 |
| registry | `facets.registry.value.name` | 值名称 |
| registry | `facets.registry.value.type` | 值类型，闭合枚举见 06 |
| application | `facets.application.name` | 应用层名称（如 ssh/HTTPS）；应用实体用 `entity_type=application` |
| container | `facets.container.kubernetes.namespace` | 命名空间 |
| container | `facets.container.kubernetes.pod.name` | Pod 名 |
| container | `facets.container.kubernetes.pod.id` | Pod 编号 |
| container | `facets.container.kubernetes.cluster.id` | 集群编号 |
| container | `facets.container.kubernetes.cluster.name` | 集群名 |
| container | `facets.container.kubernetes.container.id` | 容器编号 |
| container | `facets.container.kubernetes.container.name` | 容器名 |
| database | `facets.database.name` | 库名 |
| database | `facets.database.type` | 库类型 |
| database | `facets.database.user.name` | 数据库用户（账号实体仍可在角色上） |
| database | `facets.database.statement` | SQL 或语句文本 |
| peripheral | `facets.peripheral.device` | 接入的 USB/网卡等外设；外设身份也可用 `entity_type=device` |
| cloud | `facets.cloud` | 云控制面操作细节（账号、区域、API）；叶子随已验证样例补登记 |
| dns | `facets.dns.packet_length` | 报文长度 |
| dns | `facets.dns.question_count` | 问题区记录数（RFC1035 计数） |
| dns | `facets.dns.answer_count` | 应答区记录数（RFC1035 计数） |
| dns | `facets.dns.authority_count` | 权威区记录数（RFC1035 计数） |
| dns | `facets.dns.additional_count` | 附加区记录数（RFC1035 计数） |
| dns | `facets.dns.header.query_response` | QR 查询/响应标志，与已登记的 `opcode` / `truncated` / `recursion_desired` / `authoritative` 同族 |
| dns | `facets.dns.header.recursion_available` | RA 递归可用标志，同族 |
| dns | `facets.dns.header.authentic_data` | AD 权威数据标志，同族 |
| dns | `facets.dns.header.checking_disabled` | CD 禁止检查标志，同族 |
| email | `facets.email.date` | 邮件头 Date，明确格式及时区 |
| email | `facets.email.sender` | 邮件头 Sender；信封发件人用 `envelope_from` |
| email | `facets.email.envelope_from` | SMTP 信封发件人（MAIL FROM） |
| email | `facets.email.message_id` | 邮件消息编号（Message-ID） |
| email | `facets.email.mime_version` | MIME 版本 |
| email | `facets.email.client.user_agent` | 邮件客户端 User-Agent |
| email | `facets.email.smtp.helo` | SMTP HELO 标识 |
| email | `facets.email.smtp.last_command` | 会话内最后一条 SMTP 命令 |
| email | `facets.email.smtp.last_reply_code` | 最后一次 SMTP 响应码 |
| email | `facets.email.smtp.last_reply_message` | 最后一次 SMTP 响应消息 |
| email | `facets.email.smtp.transfer_depth` | SMTP 转发深度（来源 `trans_depth`） |
| http | `facets.http.duration` | 请求耗时 |
| http | `facets.http.request.content_type` | 请求 Content-Type |
| http | `facets.http.request.headers` | 请求头 |
| http | `facets.http.response.headers` | 响应头 |
| file | `facets.file.created_time` | 文件创建时间戳（文件身份仍在 subject/object.file） |
| file | `facets.file.modified_time` | 文件修改时间戳（文件身份仍在 subject/object.file） |
| file | `facets.file.accessed_time` | string/date-time，带时区；本次记录观察到的文件最近访问时刻，参考 OCSF file.accessed_time / ECS file.accessed；未知省略 |
| authorization | `facets.authorization.level` | 审批/授权级别 |
| ics | `facets.ics.function_code` | 工控功能码；协议名走 `facets.network.application_protocol`（modbus/s7/iec104） |
| ics | `facets.ics.function_name` | 功能码来源可读名 |
| ics | `facets.ics.address` | 线圈/寄存器/数据块地址；无样例不登记 asdu_type |

完整原始报文不进 facet：用 `meta.source_record.raw_ref` 或 `observation.evidence_refs[]`。无法解析且必须保留的原字段进 `extensions.source_private`。


#### 文件访问时刻口径

`accessed_time` 沿现行 created_time/modified_time 的 file facet 组织方式登记，不平行新增 typed file.accessed_time。该时间关联本事件所描述文件操作的目标文件；有多个文件时必须在来源映射中明确作用对象，不能取任意文件的 atime 混填。

来源 Unix 秒/毫秒或 FILETIME 必须按经确认的单位和 epoch 转为带时区的 date-time（推荐 UTC），不能按位数猜测；空串、缺失、未设置哨兵省略，epoch 0 若确为真实时刻可以保留。时间精度按来源保留。它不是告警发现、接收/插入时间或 syscall 发生时刻；atime 受 noatime/relatime 与文件系统更新策略影响，不能据此声称每次读取均被记录。访问时间可早于事件时间，不施加必须等于事件时间的校验。

`file_ctime` 仍需来源确认：POSIX ctime 是元数据变更时间，不因此次访问时间登记就获准写 created_time。结构测试见 `log-model/examples/cwp-activity/` 与 `log-model/contracts/scripts/test_cwp_activity_extensions.py`；样例为脱敏构造，不宣称真实解析已上线。

#### 主机系统调用、终端与认证公钥口径

本次登记来自 host 私有字段评审，均为可选增补，保持信封版本 2.0；未使用新字段的旧事件保持兼容。**更新来源映射语义须使用新 mapping_id**，不是将原私有字段原样复制到核心。

- syscall 对象出现时，number 与 arch 必须成对。arch 保留来源 ABI 编码，如 Linux `c000003e`；ABI 大小写/前导零可按来源规则归一，但不能只由主机架构推断调用 ABI（兼容进程可能不同）。未知编码不猜调用名。本阶段不登记 name/errno，也不凭 audit key 推调用动作。
- return_value 保留来源有符号返回值：openat 返回 3 可能是 fd，read 返回 128 可能是读入字节数，-13 可能是负 errno。**不得写成进程退出码**；行为结果仍按独立来源 success/失败证据判断，不能因正数或零就自动声称攻击成功。
- terminal 表达执行/会话上下文，参考 OCSF `process.session.terminal`，在 SDM 放 process facet，不承载实体身份。`(none)`、`?`、空串等无终端占位省略；来源 `unknown`/`none` 亦不作为实际终端名。不能从 pts/2 编造 ECS tty 设备主次编号。
- public_key 只表达**用于该次用户认证的公钥指纹**，不记录公私钥材料。区分 ED25519 等密钥算法与 SHA256 等摘要算法；从 sshd 尾串提取失败时暂留原字段，不将整段文本写成 fingerprint.value。SHA256 值必须是 32 字节摘要的标准 Base64 去尾部 `=`；MD5 值为 16 字节小写冒号分隔十六进制。不能替换成服务器 host key、TLS 证书指纹或 SSH 流量指纹。
- syscall 字段参考 [Auditbeat 9.2 auditd.data.syscall/arch/exit](https://github.com/elastic/beats/blob/v9.2.0/auditbeat/module/auditd/_meta/fields.yml)，它是产品模块先例，不宣称 ECS 核心已有 syscall；公钥指纹参考 [OCSF fingerprint](https://github.com/ocsf/ocsf-schema/blob/1.8.0/objects/fingerprint.json) 的算法/值分离结构，**SDM 的 authentication.public_key 挂载位由本次评审登记**，不是现成 OCSF/ECS 路径。
- 结构样例与边界测试见 `log-model/examples/host/`、`log-model/contracts/scripts/test_host_core_extensions.py`。这些是脱敏构造的契约测试，不宣称新解析规则已上线。

#### 网络会话与流量口径

上述网络字段为可选单值。无值时省略或为 null，真实零值保留；禁止用默认 0 表示未知。本次为开放 facet 叶子补登记，不改变行为信封 2.0 或既有对象结构。

- **会话时间**：统一为带时区的 date-time；来源 Unix 时间戳须按已确认单位转换，不得仅按位数猜单位或时区。认证、运维登录会话不因字段名包含 session 就进入 network。end_time 不早于 start_time；无有效结束时间不计算时长。
- **时长**：优先保留已确认单位的来源报告值；来源缺失且起止有效时才按秒派生。来源时长与区间差异超过来源精度容差时，保留来源事实并在验证记录中报告冲突，不静默覆盖。来源版本、精度容差和是否派生由来源映射契约记录；未确认单位的 duration 不直接映射。
- **方向参照**：bytes_in/out 以来源契约标识的被监控通信端为参照；request/response 以会话发起方/响应方为参照。两组不是别名；只有角色对应关系有证据时才可转换，禁止无条件复制。接口入出计数、方向不明的计数不能直接映射。
- **统计范围**：来源映射契约必须注明会话累计量或指定观察区间增量、区间边界、计数层次（如链路层、IP 层、应用载荷）和是否包含重传。未确认项须明确标记未知，禁止跨口径汇总；会话累计快照不能直接累加，单次应用请求量不混入会话计数。
- **总量**：原日志有总量时保留其值；若与同范围两方向之和冲突，报告冲突，不覆盖或强行配平。任一方向缺失、范围不一致或计数层次未知时不派生总量。不能把 bytes_in/out 与 request/response 四项一起相加。
- **证据边界**：360 netconnect_audit 的接收 211、发送 560、总量 771 支持三项字节字段；深信服探针 V2.0 netflow 的请求 571 字节/6 包、响应 421 字节/5 包和 session_time=0 支持方向计数及秒级时长；Suricata flow 样例的带时区起止时刻相差 5 秒，支持时间字段及派生规则。字段登记不等于所有来源映射均已验收，计数层次与累计/增量口径仍须逐来源确认。

`facets.file.remote_path` 暂不登记：须先区分远程文件身份路径（优先使用 object.file.path）与独立操作上下文，并补有值样例。`facets.network.nat.type` 暂不登记：须补有值样例、类型字典及原/译地址端点对应关系；不能仅由存在转换地址推断 SNAT/DNAT。

### 2.9 关联键（暂缓）

跨域的 session、trace、flow、connection、transaction、parent_event、story 等非实体关联键不属于本阶段逻辑契约。具有明确领域语义的会话值可保留在对应 facet；统一 `correlation` 结构和索引方式后续单独定义。实体身份键仍由 `subject`、`object`、`carriers` 承担。

### 2.10 `observation`

当前每条事件最多一个观察对象：

| 路径 | 类型 | 必填 | 说明 |
|---|---|---:|---|
| `observation.observation_id` | string | 是 | 观察记录 ID |
| `observation.observer` | object | 是 | 观察者实体 |
| `observation.observer.ref_id` | string/null | 是 | 观察者引用；观察者身份未知时为 null |
| `observation.observer.entity_type` | enum/null | 是 | 观察者实体类型；身份未知时为 null |
| `observation.observer.<typed_object>` | object/null | 条件必填 | 与 `entity_type` 对应的对象属性，支持 host、endpoint、process、user、account、device、application、service、resource 等类型 |
| `observation.action` | enum | 是 | `record`、`detect`、`assess` |
| `observation.assertion` | object/null | 否 | 观察者的判断；`detect/assess` 时必须有。声明角色为 `attacker[]`/`victim[]`，受影响对象为 `affected[]`；**日志本身已记录的实体（如被登录账号）不进断言**——它们按 §2.6 走 `carriers[]`，`affected[]` 只承载来源额外声明的影响关系 |
| `observation.assertion.kill_chain` | array/null | 否 | Cyber Kill Chain 阶段；元素子字段 `phase`；对齐 OCSF `kill_chain_phase`，来源字符串须归一 |
| `observation.assertion.category` | string/null | 否 | 来源检测分类名；原值保留，不发明平行 tactic/technique |
| `observation.assertion.attack_direction` | string | 否 | 攻击者到受害者的内外网方向；`L2L` / `L2W` / `W2L` / `W2W` / `unknown`；来源断言，不反写通信方向 |
| `observation.assertion.category_code` | string/null | 否 | 来源检测分类码 |
| `observation.assertion.mitre` | object/null | 否 | ATT&CK；子字段 `tactic` / `technique` / `technique_id`，禁止平行 `assertion.tactic` |
| `observation.evidence_refs[]` | array | 是 | 指向事实事件、原始日志或证据对象的引用 |

`evidence_refs[]` 引用格式（G1 终稿裁决 Q8-b，闭合 scheme）：

```
^(source_record|event|evidence):[A-Za-z0-9._:+/-]+$
```

| 前缀 | 指向 | 解析 |
|---|---|---|
| `source_record:{log_id}` | 来源日志记录 | 回查走 `meta.event_id → raw_log`（raw_log 键是 event_id，log_id 是溯源记号） |
| `event:{event_id}` | 另一条事实事件 | 直接按 event_id 查事件表 |
| `evidence:{证据对象键}` | 外部证据存储（PCAP/样本/截图等） | 由证据存储侧定义键空间；事件内不存证据本体 |

非空数组；每条必须匹配上述格式（校验器机器强制）。语义归属：证据属于观察
（`observation`），与 `observer`/`action`/`assertion` 同级。

`observation.observer` 使用与 `subject`、`object` 一致的 typed object 结构。观察设备或观察主机的地址统一放在对应对象的 `ip` 中，例如 `observation.observer.device.ip` 或 `observation.observer.host.ip`；不得另设 `device_ip` 等同义字段。多地址表达由后续对象注册表统一定义。事件通信双方的地址仍属于主体或客体对象，不放入观察者对象。

旧 `source_finding` 的标题、严重度、置信度、分类、规则、攻击者、受害者、受影响对象、MITRE、漏洞、恶意软件和处置结论均进入 `observation.assertion`。断言不覆盖事实层主体、客体或行为结果。置信度按来源契约保留（高/中/低或数值），不在 Schema 强制 0-100。

### 2.11 `extensions`

| 路径 | 说明 |
|---|---|
| `extensions.source_private` | 来源私有字段 |
| `extensions.profiles` | 画像或平台上下文 |
| `extensions.enrichments` | 富化结果 |

扩展不得承载诊断信息、未解释的标准事实或可替代标准字段的第二份值。

### 方向字段迁移口径

- `comm_direction` → `facets.network.direction`：已观测通信源到目标的方向，不新增同义字段。
- `attacker_direction` / `attack_direction` / 旧 `source_finding.attack_direction` → `observation.assertion.attack_direction`：来源声明的攻击者到受害者方向；不得从通信方向无条件复制。
- 攻击方向闭合值：`L2L` 内到内、`L2W` 内到外、`W2L` 外到内、`W2W` 外到外、`unknown` 未知。来源 `L2R/R2L/R2R` 仅在 R 确指外部网络时分别归一为 `L2W/W2L/W2W`。通信方向可沿用这一归一词表，现行开放字段不因此收紧。
- 内外网以租户维护的网络边界为准，不能仅凭私网地址判断。无来源依据时省略攻击方向；来源明确未知或无法判定时用 `unknown`，原始值可保留在 `extensions.source_private`。
- 多攻击者/受害者仅在来源明确给出事件级统一方向时填写；不同实体对方向冲突时，不任取一对，不新增未登记的实体对结构。

此次补充为可选断言字段，承接既有语义，既有信封版本保持 `2.0`。
