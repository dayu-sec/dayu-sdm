# SDM2.0 IP 与资产富化映射

## 1. 适用范围

本文定义原始日志标准化为 SDM2.0 后，IP 地理、资产、业务系统、组织和方向信息的落位规则。设计参考 OCSF 的端点位置和设备组织对象、UDM 的角色实体位置与 Asset/Resource 模型，以及 XDM 的 source/target 端点表达。

富化值属于标准角色或检测主张的上下文，不默认写入 `extensions`。`extensions.enrichments` 只保存富化提供方、数据库版本、执行时间、命中方式和置信度等溯源信息。

## 2. 角色判定

| 场景 | IP 语义 | Geo 落位 |
|---|---|---|
| 网络连接、流量等活动日志 | 已观测的通信发起方和目标方 | `roles.source.geo.*`、`roles.target.geo.*` |
| Finding 告警 | 检测产品声明的攻击方和受害方 | `source_finding.attacker.geo.*`、`source_finding.victim.geo.*` |

禁止默认认为 `attacker_ip == sip` 或 `victim_ip == dip`。只有来源契约、产品字段说明或已验证样例明确二者等价时，才允许复用同一 IP 的富化结果。

## 3. Geo 字段映射

下表中的 `{party}` 在活动日志中表示 `roles.source` 或 `roles.target`，在 Finding 中表示 `source_finding.attacker` 或 `source_finding.victim`。

| 来源字段后缀 | SDM2.0 路径 | 类型 | 含义 |
|---|---|---|---|
| `_continent_name` | `{party}.geo.continent.name` | `string` | IP 所在洲名称 |
| `_country_code` | `{party}.geo.country.code` | `string` | ISO 3166-1 Alpha-2 国家或地区代码 |
| `_country_name` | `{party}.geo.country.name` | `string` | 国家或地区名称 |
| `_province_name` | `{party}.geo.region.name` | `string` | 省、州或一级行政区名称 |
| `_city_name` | `{party}.geo.city.name` | `string` | 城市名称 |
| `_latitude` | `{party}.geo.coordinates.latitude` | `number` | 纬度，范围 -90 至 90 |
| `_longitude` | `{party}.geo.coordinates.longitude` | `number` | 经度，范围 -180 至 180 |

## 4. 资产、系统和组织映射

`sip_*` 映射到 `roles.source`，`dip_*` 映射到 `roles.target`，前提是 SIP/DIP 确实代表该活动的 source/target。Finding 的攻击者或受害者若不是已观测通信端点，应先建立相应的角色或关联实体，不能只因字段名为 attacker/victim 就改写 source/target。

Finding 检测主张中的攻击方和受害方资产上下文分别写入 `source_finding.attacker.resource.*` 和 `source_finding.victim.resource.*`。只有已观测活动的 SIP/DIP 才写入 `roles.source.resource.*` 和 `roles.target.resource.*`。

| 来源字段 | SDM2.0 路径 | 处理规则 |
|---|---|---|
| `sip_asset_id` / `dip_asset_id` | `roles.source.resource.id` / `roles.target.resource.id` | 资产中心唯一编号 |
| `sip_asset_name` / `dip_asset_name` | `roles.source.resource.name` / `roles.target.resource.name` | 资产名称 |
| `sip_asset_type` / `dip_asset_type` | `roles.source.resource.type` / `roles.target.resource.type` | 归一化资产类型，保留来源值可写入富化溯源 |
| `sip_system_id` / `dip_system_id` | `roles.source.resource.system.id` / `roles.target.resource.system.id` | 资产所属业务系统编号 |
| `sip_system_name` / `dip_system_name` | `roles.source.resource.system.name` / `roles.target.resource.system.name` | 资产所属业务系统名称 |
| `sip_company_name` / `dip_company_name` | `roles.source.resource.organization.name` / `roles.target.resource.organization.name` | 资产所属组织名称 |

终端和服务器应以 `host` 为主要实体，资产中心编号可同时用于稳定的 `host.id`；Agent、资产分类、组织归属和生命周期快照继续由 `extensions.profiles.endpoint_asset` 管理。安全设备、应用和非主机资产使用 `device`、`application` 或 `resource`，不得强行建模为 host。

## 5. 方向字段

| 来源字段 | SDM2.0 路径 | 判定对象 |
|---|---|---|
| `comm_direction` | `facets.network.direction` | 已观测通信的 source 到 target |
| `attack_direction` | `source_finding.attack_direction` | 检测产品声明的 attacker 到 victim |

两个字段使用同一组规范值，但语义独立：

| 规范值 | 含义 |
|---|---|
| `L2L` | 两端均在受治理的内部网络 |
| `L2W` | 起点在内部网络，终点在外部网络 |
| `W2L` | 起点在外部网络，终点在内部网络 |
| `W2W` | 两端均在外部网络 |
| `unknown` | 缺少边界信息，无法可靠判断 |

中文值“内到内”“内到外”“外到内”“外到外”和历史代码 `L2L`、`L2R`、`R2L`、`R2R` 应在 OML 中归一化。内外网判定必须使用租户维护的网络边界，不应只依赖 RFC 1918 私网段。

## 6. 富化溯源

实际需要审计富化过程时，可在 `extensions.enrichments` 保存下列非业务字段：

- 富化提供方和服务名称；
- GeoIP、CMDB 或资产库版本；
- 富化执行时间；
- 精确匹配、网段匹配或推断等命中方式；
- 匹配置信度和未命中原因。

同一业务值不应在 `extensions.enrichments` 中再复制一份。未命中或无法确认角色时省略字段，不填示例值，也不把未验证值写成标准事实。
