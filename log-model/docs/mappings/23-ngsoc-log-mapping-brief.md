# NGSOC 日志映射简表

## 1. 输入与路由

| `log_type` | 输入格式 | 来源版本 | WPL | OML |
|---|---|---|---|---|
| `ngsoc_alert_info` | Syslog KV，中文枚举 | 历史兼容格式 | 1 条规则 | `ngsoc_alert_info/adm.oml` |
| `ngsoc_threat_alert_send` | JSON，数值枚举 | `NGSOC-4.13.1` | 2 条兼容规则 | `ngsoc_threat_alert_send/adm.oml` |

当前实现是 **1 份 `parse.wpl`（3 条规则）+ 2 份 OML**。推荐目标结构是按两类格式拆成 **2 份 WPL、2 份 OML**；JSON 的两条 WPL 规则仅兼容字段类型和时间表现差异，输出同一个 `log_type`。

## 2. 核心字段映射

| NGSOC 字段 | SDM2.0 字段 | 规则 |
|---|---|---|
| `timestamp` | `occur_time` | 事件首次发生时间；按来源时区转换 |
| `uuid` | `source_original_event_id`、`source_alert_original_id`、`source_finding.original_id` | 来源稳定告警 ID；分别作为事件回源标量、告警回源投影和 finding 对象字段 |
| `name` | `source_alert_name` | 来源告警名称 |
| `ruleCategoryName` | `source_alert_category` | 来源告警分类 |
| `ruleId` | `source_alert_signature_id` | 单值时投影；多值保留在 finding/扩展 |
| `severity` | `source_alert_severity`、`source_finding.severity` | 始终保留原值；顶层 `severity` 仅经安全严重度字典归一 |
| Syslog PRI | `log_level` | `<14>` 对应 `info`；不得写入安全 `severity` |
| `attackResult` | `source_finding.attack_result` | 保留检测结论；仅在动作结果语义明确时投影 `outcome` |
| `compromiseState` | `source_finding.compromise_status` | 与 `attackResult` 独立 |
| `killchain` | `source_finding.killchain` | 按格式专属字典归一 |
| `srcIp` / `sport` | `roles.source.endpoint`、`source_ip/source_port` | 唯一值才生成标量投影 |
| `dstIp` / `dport` | `roles.target.endpoint`、`target_ip/target_port` | 唯一值才生成标量投影 |
| `attackerContent` / `attackerIp` | `source_finding.attacker` | 来源检测声明；不等同于 `source` |
| `victimContent` / `victimIp` | `source_finding.victim` | 来源检测声明；不等同于 `target` |
| `protocol` | `facets.network.protocol`、`carrier_protocol` | 仅用于 TCP/UDP 等明确传输协议 |
| `appProtocol` / `appName` | `facets.application.name`、`carrier_app_name` | 仅用于 HTTP/DNS 等明确应用协议或应用名称 |
| `commDirection` | `facets.network.direction` | 通信方向；不得直接当作攻击方向 |
| `domain` / `uri` | target、finding IOC 或 related | 只有被访问目标明确时写 `target_domain/target_url`；否则按 IOC/关联实体保留 |
| `httpMethod` / `httpRspCode` | `http_method` / `http_status` | 优先读取 `extraFields` 中的单值 |
| `fileMd5` / `fileSha1` / `fileSha256` | 目标文件哈希字段 | 只有文件客体明确时投影 |
| `disposeState` / `ticketState` | 来源 finding/扩展 | 不得生成 `outcome` 或 `operation` |
| 其他 `extraFields` | `extensions.source_private.*` | 逐字段登记；物理写入 `extensions_obj`，禁止整体复制 |

## 3. 区域对象映射

### 3.1 顶层标量

| 来源 | 目标 | 说明 |
|---|---|---|
| 平台上下文 | `tenant_id`、`data_src_instance_id`、`ingest_time`、`parse_time` | 不从日志正文生成 |
| `timestamp` | `occur_time` | 事件首次发生时间 |
| `uuid` | `source_original_event_id`、`source_alert_original_id` | 同一来源告警 ID 的两个合法回源投影；不替代 `log_id` |
| 稳定采集位置 | `log_id` | 标识原始日志记录，不从 `uuid` 无条件复制 |
| 确定性哈希 | `event_id` | 输入至少包含 tenant、mapping、来源事件或日志 ID |
| 路由常量 | `mapping_id`、`log_type`、`data_src_*`、`observer_*` | 按两类输入格式固定 |
| 事件事实 | `event_type`、`operation`、`outcome` | 按告警实际描述选择；无证据留空或 `unknown` |
| 来源严重度字典 | `severity` | 与 PRI 的 `log_level` 分离 |
| 对象唯一值 | `source_*`、`target_*`、`carrier_*`、`http_*` | 仅作为对象区的热检索投影 |

### 3.2 `roles_obj`

| 区域对象 | NGSOC 来源 | 主要路径 | 条件 |
|---|---|---|---|
| `observer` | 常量 `qax/ngsoc`；经证据确认的 NGSOC 设备名、序列号和地址 | `roles.observer.device.*`、`roles.observer.product.*` | 始终建立产品；`devIp` 不默认作为 observer IP |
| `source` | `srcIp/sport/srcUser/srcMac` | `roles.source.endpoint.*`、`roles.source.user.*` | 表示行为发起方，不自动等于 attacker |
| `target` | `dstIp/dport/dstUser/hostName`，以及经事件事实确认的 `domain/uri` | `roles.target.endpoint.*`、`user.*`、`domain.*`、`url.*`、`host.*` | 表示行为被作用方，不自动等于 victim；domain/URI 不按字段名机械归入 target |
| `target.file` | `fileName/filePath/fileMd5/fileSha1/fileSha256/hashType` | `roles.target.file.*` | 只有事件事实明确存在文件客体时建立 |
| `carriers[]` | `processName/processId/processCommand/processPath` | `roles.carriers[].process.*` | 只有进程承载行为且字段非空时建立 |
| `related[]` | `proxyIp/relevantAssets*`，以及角色已确认的 `devIp/domain/uri` | `roles.related[]` | 仅在关系类型可说明时建立，否则进入 finding 或来源扩展 |

### 3.3 `facets_obj`

| 区域对象 | NGSOC 来源 | 主要路径 | 条件 |
|---|---|---|---|
| `network` | `srcIp/dstIp/sport/dport/protocol/commDirection` | `facets.network.source/target/protocol/direction` | 网络证据存在时；`protocol` 仅接收传输协议，方向只描述通信 |
| `http` | `uri/url/httpMethod/httpRspCode/httpUserAgent/httpXff`，以及 `payload.httpReq*/httpRsp*` | `facets.http.request.*`、`response.*`、`client.*` | HTTP 字段或报文明示时建立 |
| `dns` | `domain/dnsARecord/dnsAddr` | `facets.dns.question/answers` | 只有 DNS 查询或响应事实明确时建立；普通告警域名不自动生成 DNS facet |
| `file` | 文件字段及来源动作 | `facets.file.*` | 只有文件操作类型明确时建立 |
| `authentication` | `authType/userName/srcUser/dstUser` 加明确登录结果 | `facets.authentication.*` | `attackResult=企图` 不能单独生成认证结果 |
| `application` | `appName/appProtocol` | `facets.application.name` | 应用语义明确时建立；不得回填到传输协议 |

### 3.4 `source_finding_obj`

| 区域对象 | NGSOC 来源 | 主要路径 | 说明 |
|---|---|---|---|
| 基本属性 | `uuid/name/severity/confidence/times` | `original_id/title/severity/confidence/count` | 保留来源告警声明；UUID 同时生成合法回源标量投影 |
| 分类与规则 | `ruleCategoryName/ruleId/ruleName/relevantRuleName` | `category.original/rule/rules[]` | 多值保持数组 |
| 判定结论 | `attackResult/compromiseState/killchain` | `attack_result/compromise_status/killchain` | 使用格式专属字典 |
| attacker | `attackerIp/attackerContent` | `attacker.endpoint.*` | 来源明确声明时建立；不复制 source 端口 |
| victim | `victimIp/victimContent` | `victim.endpoint.*` | 来源明确声明时建立；不复制 target 端口 |
| IOC | `ioc/iocType` | `ioc` 或 `indicators[]` | 按 IOC 类型解析 IP、域名、哈希等 |
| MITRE | `attCk` | `mitre.technique_id/techniques[]` | 只有合法 `Txxxx[.xxx]` 才作为技术 ID |
| 恶意软件 | `malwareName/maliciousFamily/virusName` | `malware.*` | 去除 `无/none` 等哨兵值 |
| 漏洞 | `cve/cnnvd/vulnName/vulnDesc/vulnHarm` | `vulnerability.*` | 字段非空且语义明确时建立 |
| 处置与关注 | `solution/operateAdvice/attentionValue/disposeState` | `remediation/attention/status` | 来源状态不投影为事件 `outcome` |
| 攻击方向 | attacker/victim 的独立网络归属证据 | `attack_direction` | 不由 `commDirection` 机械复制 |

### 3.5 `extensions_obj`

| 子区域 | 来源 | 用途 |
|---|---|---|
| `source_private` | `seq/source/ticketState/occurDays/relevantLogsType`，以及角色未确认的 `devIp/domain/uri` | SDM 无等价路径但有调查价值的来源事实 |
| `profiles` | 已注册的设备或资产画像 | 跨事件复用的稳定画像；通过 `ref_id` 关联角色实体 |
| `enrichments` | GeoIP、资产、组织、系统等平台补充信息 | 必须标明平台来源，不能伪装成 WPL 原值 |
| `unmapped` | 未知枚举或语义冲突原值 | 临时保留并进入复核；不得作为长期 catch-all |

原文保存在独立 `raw_log` 表，经 `event_id` 回查，不复制到 `extensions_obj`。

## 4. 枚举

`ngsoc_threat_alert_send` 按厂商 `NGSOC-4.13.1` 字典映射：

| NGSOC 字段 | 原值 -> SDM2.0 值 | SDM2.0 路径 |
|---|---|---|
| `severity` | `1 -> notice`、`2 -> warning`、`3 -> error`、`4 -> crit` | `severity`；原值保留到 `source_alert_severity`、`source_finding.severity` |
| `confidence` | `1 -> low`、`2 -> medium`、`3 -> high` | `source_finding.confidence` |
| `attackResult` | `0 -> not_applicable`、`1 -> success`、`2 -> attempted`、`3 -> failed` | `source_finding.attack_result` |
| `compromiseState` | `false -> not_compromised`、`true -> compromised` | `source_finding.compromise_status` |
| `killchain` | `0 -> not_applicable`、`1 -> reconnaissance`、`2 -> weaponization`、`3 -> delivery`、`4 -> exploitation`、`5 -> installation`、`6 -> command_and_control`、`7 -> actions_on_objectives`、`8 -> automated_collection` | `source_finding.killchain` |

`attackResult` 不直接生成顶层 `outcome`。`ngsoc_alert_info` 的中文枚举使用独立的历史兼容映射。

## 5. 固定规则

- `tenant_id`、`data_src_instance_id`、`ingest_time` 和 `parse_time` 来自平台上下文，不从日志正文猜测。
- `event_id`、`log_id` 和 `source_original_event_id` 各自独立，不得复用同一动态值冒充。
- `record_kind=finding` 不自动生成 `outcome=observed`。
- source/target 表示事件事实角色；attacker/victim 表示来源检测声明。
- 空字符串、`none`、`无`、`unknown` 等哨兵值不作为正常实体或检索字段落库。
- 当前映射尚未注册为 approved manifest；本文件是现有样例和厂商文档的实现说明。
