# SDM2.0 IP 与资产富化映射

## 1. 适用范围

本文定义原始日志标准化为 SDM2.0 行为信封（`07-sdm-event-behavior.schema.json`，`meta.schema_version=2.0`）后，IP 地理、资产、业务系统、组织和方向信息的落位规则。设计参考 OCSF 的端点位置和设备组织对象、UDM 的角色实体位置与 Asset/Resource 模型，以及 XDM 的 source/target 端点表达。

富化值属于标准角色或检测主张的上下文，不默认写入 `extensions`。`extensions.enrichments` 只保存富化提供方、数据库版本、执行时间、命中方式和置信度等溯源信息。

## 2. 角色判定

行为信封只有行为角色 `subject` / `object` / `carriers[]` / `observation.observer`，没有通信角色；通信方向归 `facets.network.*`。

| 场景 | IP 语义 | 富化落位 |
|---|---|---|
| 网络连接、流量等活动日志 | 已观测的通信发起方和目标方 | `subject.*` / `object.*`（按行为角色判定，不是按 IP 方向） |
| 检测告警（finding） | 检测产品声明的攻击方和受害方 | `observation.assertion.attacker[]` / `victim[]` 所辖实体 |

禁止默认认为 `attacker_ip == sip` 或 `victim_ip == dip`，也不因字段名含 `attacker` / `victim` 就改写事实层。只有来源契约、产品字段说明或已验证样例明确二者等价时，才允许复用同一 IP 的富化结果。

## 3. Geo 字段映射

下表中的 `{party}` 表示已确定的角色对象（`subject` / `object` / `carriers[]`，或断言实体 `observation.assertion.attacker[]` / `victim[]`），`{entity}` 是该角色下的具体实体对象（`host` / `endpoint` / `resource`）。

| 来源字段后缀 | SDM2.0 路径 | 类型 | 含义 |
|---|---|---|---|
| `_continent_name` | `{party}.{entity}.geo.continent_name` | `string` | IP 所在洲名称，统一中文 |
| `_country_code` | `{party}.{entity}.geo.country_code` | `string` | ISO 3166-1 Alpha-2 国家或地区代码，大写 |
| `_country_name` | `{party}.{entity}.geo.country` | `string` | 国家或地区名称 |
| `_province_name` | `{party}.{entity}.geo.province` | `string` | 省、州或一级行政区名称 |
| `_city_name` | `{party}.{entity}.geo.city` | `string` | 城市名称 |
| `_latitude` | `{party}.{entity}.geo.latitude` | `number` | 纬度，范围 -90 至 90 |
| `_longitude` | `{party}.{entity}.geo.longitude` | `number` | 经度，范围 -180 至 180 |

`geo` 只挂实体对象：禁止 `facets.network.*.geo`，禁止在 `observation.assertion` 下再拷贝一份 `endpoint.geo`。无命中时省略整个 `geo`，不得写空对象。

## 4. 资产、系统和组织映射

资产编号只有两个登记位，同一资产必须同值：实体 `id`（`host.id` / `device.id` / `resource.id` / `service.id`）与端点 `endpoint.asset_id`。端点身份仍是 `ip`（`ref_id=endpoint::{ip}`），`asset_id` 不参与 `ref_id`。

| 来源字段 | SDM2.0 路径 | 处理规则 |
|---|---|---|
| `*_asset_id`（IP 富化命中） | `{party}.{entity}.endpoint.asset_id`；判定为终端主机时同写 `{party}.host.id` | 资产系统（CMDB/资产中心）唯一编号；两处同时存在必须同值 |
| `asset_id`（来源自带，未富化） | 同上；判不出实体角色时兜底留 `extensions.source_private.asset_id` | 先按行为角色确定实体，不机械沿用旧 `roles.*` / `source_finding.*` 路径 |
| `*_asset_name` | `{party}.{entity}.endpoint.asset_name`；判定为终端主机时同写 `{party}.host.name` | 资产系统里的资产名称；与主机名口径不同，来源同名时同值 |
| `*_asset_type` | `{party}.{entity}.endpoint.asset_type`；判定出实体后按需归一写 `device.type` / `resource.kind` | 来源归一化类型字符串，不是闭集枚举 |
| `*_system_id` / `*_system_name` | `{party}.{entity}.system.id` / `{party}.{entity}.system.name` | 资产所属业务系统 |
| `*_company_name` | `{party}.{entity}.organization.name` | 资产所属组织名称 |
| `asset_oid` | `organization.id` 或 `extensions.source_private.asset_oid` | 组织上下文，不是资产身份 |

终端和服务器以 `host` 为主要实体；安全设备、应用和非主机资产使用 `device`、`application` 或 `resource`，不得强行建模为 host。

`endpoint` 下不再挂 `resource` 对象：旧 `{party}.endpoint.resource.*` 的子键按上表迁到 `endpoint.asset_id`、实体 `id`、`system.*`、`organization.*`，对象本身不再登记（见 `docs/wparse-OML字段树迁移处置表.md`）。

Agent、资产分类、组织归属和生命周期快照由 `extensions.profiles.endpoint_asset` 管理，不占实体字段。

## 5. 方向字段

| 来源字段 | SDM2.0 路径 | 判定对象 |
|---|---|---|
| `comm_direction` | `facets.network.direction` | 已观测通信的 source 到 target |
| `attacker_direction` / `attack_direction` | `observation.assertion.attack_direction` | 检测产品声明的 attacker 到 victim |

两个字段语义独立，不能互相复制：攻击方向是来源断言，不得从通信方向无条件推导；缺少依据时省略，来源明确未知或无法判定时写 `unknown`。

| 规范值 | 含义 |
|---|---|
| `L2L` | 两端均在受治理的内部网络 |
| `L2W` | 起点在内部网络，终点在外部网络 |
| `W2L` | 起点在外部网络，终点在内部网络 |
| `W2W` | 两端均在外部网络 |
| `unknown` | 缺少边界信息，无法可靠判断 |

中文值“内到内”“内到外”“外到内”“外到外”和历史代码 `L2L`、`L2R`、`R2L`、`R2R` 应在 OML 中归一化：`R` 确指外部网络时，`L2R` → `L2W`、`R2L` → `W2L`、`R2R` → `W2W`。内外网判定必须使用租户维护的网络边界，不应只依赖 RFC 1918 私网段。

## 6. 富化溯源

实际需要审计富化过程时，可在 `extensions.enrichments` 保存下列非业务字段：

- 富化提供方和服务名称；
- GeoIP、CMDB 或资产库版本；
- 富化执行时间；
- 精确匹配、网段匹配或推断等命中方式；
- 匹配置信度和未命中原因。

同一业务值不应在 `extensions.enrichments` 中再复制一份。未命中或无法确认角色时省略字段，不填示例值，也不把未验证值写成标准事实。
