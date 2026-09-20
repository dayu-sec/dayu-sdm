> **历史对照**：本文是中间版本五层逻辑路径清单（metadata / event / roles / source_finding，504 条）。
> 现行权威：`docs/SDM事件模型逻辑契约字段目录.md` + `07-sdm-event-behavior.schema.json`（`2.0`）。
> 新写入不得按本文路径落库。

# SDM2.0 事件逻辑字段清单

> 权威来源：`object-registry.v1.json` registry v22。
> 本清单包含当前中间版本采用的 504 条核心逻辑叶子路径，不是 Doris 物理列清单。
> 2026-08-28 移除 `mapping_revision`、`projection_version`、`quality_status` 三个治理字段：物理表 007、Routine Load 026、Kafka 消息均不再包含。
> 已删减的 13 个低频标量投影仍保留其逻辑路径，由 `roles_obj` 或 `facets_obj` 权威存储。
> 2026-08-26 修订：原始日志已分离至独立 `raw_log` 表（event_id 1:1 关联），取消 `metadata.raw_log_id` → `metadata.raw_msg` 的临时替换，恢复标准注册表路径 `metadata.raw_log_id`。
> 2026-08-26 修订：删除 `metadata.raw_log_id`——其值恒等于 `event_id` 属冗余列，事件↔raw_log 关联统一用 `event_id`，来源日志身份用 `log_id`。
> 2026-08-26 修订：删除 `metadata.original_event_id`——来源稳定 ID 写入 `log_id`，否则 `log_id` 与 `event_id` 相同。
> `extensions.profiles.endpoint_asset` 的 19 条 Profile 路径单独治理，不计入本清单。

## 分层统计

| 层 | 字段数 | 职责 |
|---|---:|---|
| `metadata` | 15 | 接入来源、时间、标识和治理信息 |
| `event` | 7 | 事件种类、领域、行为、结果和严重度 |
| `roles` | 253 | 发起方、目标方、观察方、载体和关联对象 |
| `facets` | 89 | 网络、HTTP、邮件、认证、容器等事件维度 |
| `source_finding` | 140 | 来源设备自身的检测或告警判断 |

## 核心逻辑字段

| 序号 | 所在层 | 逻辑路径 | 逻辑类型 | 基数 | 必填 | 样例 | 字段含义 |
|---:|---|---|---|---|---|---|---|
| 1 | `metadata` | `metadata.tenant_id` | `string` | 单值 | Y | `tenant-001` | 租户编号 |
| 2 | `metadata` | `metadata.occur_time` | `string(datetime)` | 单值 | Y | `2026-08-04T10:15:30.123Z` | 事件发生时间 |
| 3 | `metadata` | `metadata.ingest_time` | `string(datetime)` | 单值 | N | `2026-08-04T10:15:31.025Z` | 接收时间 |
| 4 | `metadata` | `metadata.event_id` | `string` | 单值 | Y | `evt-20260804-000001` | 事件编号 |
| 5 | `metadata` | `metadata.parse_time` | `string(datetime)` | 单值 | N | `2026-08-04T10:15:31.118Z` | 解析时间 |
| 6 | `metadata` | `metadata.schema_version` | `integer` | 单值 | Y | `1` | 结构版本 |
| 7 | `metadata` | `metadata.mapping_id` | `string` | 单值 | Y | `qax.skyeye.flow_webattack` | 映射编号 |
| 8 | `metadata` | `metadata.data_source.vendor` | `string` | 单值 | N | `qax` | 数据来源厂商 |
| 9 | `metadata` | `metadata.data_source.product` | `string` | 单值 | N | `skyeye` | 数据来源产品 |
| 10 | `metadata` | `metadata.data_source.category` | `string` | 单值 | N | `security_device` | 数据来源类别 |
| 11 | `metadata` | `metadata.data_source.instance_id` | `string` | 单值 | N | `skyeye-sensor-01` | 数据来源实例编号 |
| 12 | `metadata` | `metadata.log.type` | `string` | 单值 | N | `flow_webattack` | 来源日志类型 |
| 13 | `metadata` | `metadata.log.level` | `string` | 单值 | N | `high` | 来源日志等级 |
| 14 | `metadata` | `metadata.log.name` | `string` | 单值 | N | `Web 攻击日志` | 来源日志名称 |
| 15 | `metadata` | `metadata.log_id` | `string` | 单值 | N | `log-20260804-000001` | 日志编号 |
| 16 | `event` | `event.record_kind` | `string` | 单值 | Y | `finding` | 记录种类 |
| 17 | `event` | `event.domain` | `string` | 单值 | Y | `threat` | 事件所属领域 |
| 18 | `event` | `event.type` | `string` | 单值 | Y | `web_attack` | 标准化事件类型 |
| 19 | `event` | `event.operation` | `string` | 单值 | N | `detect` | 操作 |
| 20 | `event` | `event.outcome` | `string` | 单值 | N | `blocked` | 结果 |
| 21 | `event` | `event.severity` | `string` | 单值 | N | `high` | 严重级别 |
| 22 | `event` | `event.message` | `string` | 单值 | N | `检测到 SQL 注入攻击并已阻断` | 事件消息 |
| 23 | `roles` | `roles.source.endpoint.ip` | `string` | 单值 | N | `198.51.100.23` | 发起方网络端点IP 地址 |
| 24 | `roles` | `roles.source.endpoint.ipv4` | `string` | 单值 | N | `198.51.100.23` | 发起方网络端点IPv4 地址 |
| 25 | `roles` | `roles.source.endpoint.ipv6` | `string` | 单值 | N | `2001:db8::23` | 发起方网络端点IPv6 地址 |
| 26 | `roles` | `roles.source.endpoint.port` | `integer` | 单值 | N | `443` | 发起方网络端点端口 |
| 27 | `roles` | `roles.source.endpoint.mac` | `string` | 单值 | N | `00:00:5E:00:53:65` | 发起方网络端点MAC 地址 |
| 28 | `roles` | `roles.source.host.mac` | `string` | 单值 | N | `00:00:5E:00:53:23` | 来源主机的 MAC 地址 |
| 29 | `roles` | `roles.source.user.name` | `string` | 单值 | N | `alice` | 发起方用户名称 |
| 30 | `roles` | `roles.source.account.name` | `string` | 单值 | N | `svc_web` | 发起方账号名称 |
| 31 | `roles` | `roles.source.host.name` | `string` | 单值 | N | `web-server-01` | 发起方主机名称 |
| 32 | `roles` | `roles.source.host.id` | `string` | 单值 | N | `id-01` | 发起方主机编号 |
| 33 | `roles` | `roles.source.process.name` | `string` | 单值 | N | `curl` | 发起方进程名称 |
| 34 | `roles` | `roles.source.process.pid` | `string` | 单值 | N | `23841` | 发起方进程进程号 |
| 35 | `roles` | `roles.source.process.uid` | `string` | 单值 | N | `uid-1001` | 发起方进程唯一标识 |
| 36 | `roles` | `roles.source.process.path` | `string` | 单值 | N | `C:\Windows\System32\svchost.exe` | 发起方进程路径 |
| 37 | `roles` | `roles.source.process.cmdline` | `string` | 单值 | N | `svchost.exe -k DcomLaunch` | 发起方进程命令行 |
| 38 | `roles` | `roles.source.process.user.name` | `string` | 单值 | N | `alice` | 发起方用户名称 |
| 39 | `roles` | `roles.source.process.file.hashes.md5` | `string` | 单值 | N | `d41d8cd98f00b204e9800998ecf8427e` | 发起方MD5 |
| 40 | `roles` | `roles.source.process.file.hashes.sha1` | `string` | 单值 | N | `356a192b7913b04c54574d18c28d46e6395428ab` | 发起方SHA-1 |
| 41 | `roles` | `roles.source.process.file.original_name` | `string` | 单值 | N | `svchost.exe` | 发起方文件原始文件名称 |
| 42 | `roles` | `roles.source.process.file.internal_name` | `string` | 单值 | N | `svchost.exe` | 发起方文件内部名称 |
| 43 | `roles` | `roles.source.process.file.signatures[].signer` | `string` | 多值对象成员 | N | `Microsoft Windows Publisher` | 发起方签名列表签名主体 |
| 44 | `roles` | `roles.source.geo.city.name` | `string` | 单值 | N | `北京市` | 发起方 IP 所在城市名称 |
| 45 | `roles` | `roles.source.geo.continent.name` | `string` | 单值 | N | `亚洲` | 发起方 IP 所在洲名称 |
| 46 | `roles` | `roles.source.geo.country.code` | `string` | 单值 | N | `CN` | 发起方 IP 所在国家或地区的 ISO 3166-1 Alpha-2 代码 |
| 47 | `roles` | `roles.source.endpoint.device.type` | `string` | 单值 | N | `workstation` | 发起方设备类型 |
| 48 | `roles` | `roles.source.geo.country.name` | `string` | 单值 | N | `中国` | 发起方 IP 所在国家或地区名称 |
| 49 | `roles` | `roles.source.geo.region.name` | `string` | 单值 | N | `北京` | 发起方 IP 所在省、州或一级行政区名称 |
| 50 | `roles` | `roles.source.geo.coordinates.latitude` | `number` | 单值 | N | `39.9042` | 发起方 IP 地理位置纬度 |
| 51 | `roles` | `roles.source.geo.coordinates.longitude` | `number` | 单值 | N | `116.4074` | 发起方 IP 地理位置经度 |
| 52 | `roles` | `roles.source.host.os.type` | `string` | 单值 | N | `linux` | 发起方类型 |
| 53 | `roles` | `roles.carriers[].process.name` | `string` | 多值对象成员 | N | `curl` | 载体进程名称 |
| 54 | `roles` | `roles.carriers[].process.pid` | `string` | 多值对象成员 | N | `23841` | 载体进程进程号 |
| 55 | `roles` | `roles.carriers[].process.uid` | `string` | 多值对象成员 | N | `uid-1001` | 载体进程唯一标识 |
| 56 | `roles` | `roles.carriers[].process.guid` | `string` | 多值对象成员 | N | `7f8a9b10-1234-5678-9abc-def012345678` | 载体进程GUID |
| 57 | `roles` | `roles.carriers[].process.cmdline` | `string` | 多值对象成员 | N | `curl https://portal.example.com/login` | 载体进程命令行 |
| 58 | `roles` | `roles.carriers[].process.path` | `string` | 多值对象成员 | N | `/usr/bin/curl` | 载体进程路径 |
| 59 | `roles` | `roles.carriers[].process.created_time` | `string(datetime)` | 多值对象成员 | N | `2024-12-17T20:10:07.744+08:00` | 载体进程创建时间 |
| 60 | `roles` | `roles.carriers[].process.user.name` | `string` | 多值对象成员 | N | `alice` | 载体用户名称 |
| 61 | `roles` | `roles.carriers[].process.user.id` | `string` | 多值对象成员 | N | `id-01` | 载体用户编号 |
| 62 | `roles` | `roles.carriers[].process.file.hashes.md5` | `string` | 多值对象成员 | N | `d41d8cd98f00b204e9800998ecf8427e` | 载体MD5 |
| 63 | `roles` | `roles.carriers[].process.file.hashes.sha1` | `string` | 多值对象成员 | N | `356a192b7913b04c54574d18c28d46e6395428ab` | 载体SHA-1 |
| 64 | `roles` | `roles.carriers[].process.file.hashes.sha256` | `string` | 多值对象成员 | N | `a3f1...cdef` | 载体SHA-256 |
| 65 | `roles` | `roles.carriers[].process.file.original_name` | `string` | 多值对象成员 | N | `original-name-01` | 载体文件原始文件名称 |
| 66 | `roles` | `roles.carriers[].process.file.internal_name` | `string` | 多值对象成员 | N | `internal-name-01` | 载体文件内部名称 |
| 67 | `roles` | `roles.carriers[].process.file.company_name` | `string` | 多值对象成员 | N | `company-name-01` | 载体文件厂商名称 |
| 68 | `roles` | `roles.carriers[].process.file.product.name` | `string` | 多值对象成员 | N | `portal-web` | 载体产品名称 |
| 69 | `roles` | `roles.carriers[].process.file.description` | `string` | 多值对象成员 | N | `description-01` | 载体文件描述 |
| 70 | `roles` | `roles.carriers[].process.file.version` | `string` | 多值对象成员 | N | `version-01` | 载体文件版本 |
| 71 | `roles` | `roles.carriers[].process.file.signatures[].signer` | `string` | 多值对象成员 | N | `signer-01` | 载体签名列表签名主体 |
| 72 | `roles` | `roles.carriers[].process.file.signatures[].status` | `string` | 多值对象成员 | N | `active` | 载体签名列表状态 |
| 73 | `roles` | `roles.carriers[].script.id` | `string` | 多值对象成员 | N | `12e821ca-0d5c-409a-8bbf-fa39567d4d70` | 载体脚本编号 |
| 74 | `roles` | `roles.carriers[].script.language` | `string` | 多值对象成员 | N | `powershell` | 载体脚本语言 |
| 75 | `roles` | `roles.carriers[].script.command` | `string` | 多值对象成员 | N | `$global:?` | 载体脚本命令或表达式 |
| 76 | `roles` | `roles.carriers[].script.content` | `string` | 多值对象成员 | N | `$Res = 0; Write-Host $Res` | 载体脚本正文 |
| 77 | `roles` | `roles.target.endpoint.ip` | `string` | 单值 | N | `198.51.100.23` | 目标方网络端点IP 地址 |
| 78 | `roles` | `roles.target.endpoint.ipv4` | `string` | 单值 | N | `198.51.100.23` | 目标方网络端点IPv4 地址 |
| 79 | `roles` | `roles.target.endpoint.ipv6` | `string` | 单值 | N | `2001:db8::23` | 目标方网络端点IPv6 地址 |
| 80 | `roles` | `roles.target.endpoint.port` | `integer` | 单值 | N | `443` | 目标方网络端点端口 |
| 81 | `roles` | `roles.target.endpoint.mac` | `string` | 单值 | N | `00:00:5E:00:53:65` | 目标方网络端点MAC 地址 |
| 82 | `roles` | `roles.target.user.name` | `string` | 单值 | N | `alice` | 目标方用户名称 |
| 83 | `roles` | `roles.target.host.name` | `string` | 单值 | N | `web-server-01` | 目标方主机名称 |
| 84 | `roles` | `roles.target.host.id` | `string` | 单值 | N | `id-01` | 目标方主机编号 |
| 85 | `roles` | `roles.target.host.mac` | `string` | 单值 | N | `00:00:5E:00:53:65` | 目标方主机MAC 地址 |
| 86 | `roles` | `roles.target.host.os.name` | `string` | 单值 | N | `Ubuntu Server` | 目标方名称 |
| 87 | `roles` | `roles.target.host.os.type` | `string` | 单值 | N | `linux` | 目标方类型 |
| 88 | `roles` | `roles.target.service.name` | `string` | 单值 | N | `https` | 目标方服务名称 |
| 89 | `roles` | `roles.target.service.port` | `integer` | 单值 | N | `443` | 目标方服务端口 |
| 90 | `roles` | `roles.target.domain.name` | `string` | 单值 | N | `portal.example.com` | 目标方名称 |
| 91 | `roles` | `roles.target.url.full` | `string` | 单值 | N | `https://portal.example.com/login?id=1%27` | 目标方完整值 |
| 92 | `roles` | `roles.target.geo.city.name` | `string` | 单值 | N | `上海市` | 目标方 IP 所在城市名称 |
| 93 | `roles` | `roles.target.geo.continent.name` | `string` | 单值 | N | `亚洲` | 目标方 IP 所在洲名称 |
| 94 | `roles` | `roles.target.geo.country.code` | `string` | 单值 | N | `CN` | 目标方 IP 所在国家或地区的 ISO 3166-1 Alpha-2 代码 |
| 95 | `roles` | `roles.target.geo.country.name` | `string` | 单值 | N | `中国` | 目标方 IP 所在国家或地区名称 |
| 96 | `roles` | `roles.target.geo.region.name` | `string` | 单值 | N | `上海` | 目标方 IP 所在省、州或一级行政区名称 |
| 97 | `roles` | `roles.target.geo.coordinates.latitude` | `number` | 单值 | N | `31.2304` | 目标方 IP 地理位置纬度 |
| 98 | `roles` | `roles.target.geo.coordinates.longitude` | `number` | 单值 | N | `121.4737` | 目标方 IP 地理位置经度 |
| 99 | `roles` | `roles.target.file.path` | `string` | 单值 | N | `/var/www/html/login.php` | 目标方文件路径 |
| 100 | `roles` | `roles.target.file.name` | `string` | 单值 | N | `login.php` | 目标方文件名称 |
| 101 | `roles` | `roles.target.file.size` | `integer` | 单值 | N | `1024` | 目标方文件大小 |
| 102 | `roles` | `roles.target.file.mime_type` | `string` | 单值 | N | `text/x-php` | 目标方文件MIME 类型 |
| 103 | `roles` | `roles.target.file.created_time` | `string(datetime)` | 单值 | N | `2026-08-04T10:15:30.123Z` | 目标方文件创建时间 |
| 104 | `roles` | `roles.target.file.hashes.md5` | `string` | 单值 | N | `d41d8cd98f00b204e9800998ecf8427e` | 目标方MD5 |
| 105 | `roles` | `roles.target.file.hashes.sha1` | `string` | 单值 | N | `356a192b7913b04c54574d18c28d46e6395428ab` | 目标方SHA-1 |
| 106 | `roles` | `roles.target.file.hashes.sha256` | `string` | 单值 | N | `a3f1...cdef` | 目标方SHA-256 |
| 107 | `roles` | `roles.target.process.name` | `string` | 单值 | N | `curl` | 目标方进程名称 |
| 108 | `roles` | `roles.target.process.pid` | `string` | 单值 | N | `23841` | 目标方进程进程号 |
| 109 | `roles` | `roles.target.process.uid` | `string` | 单值 | N | `uid-1001` | 目标方进程唯一标识 |
| 110 | `roles` | `roles.target.process.path` | `string` | 单值 | N | `/usr/bin/curl` | 目标方进程路径 |
| 111 | `roles` | `roles.target.process.cmdline` | `string` | 单值 | N | `curl https://portal.example.com/login` | 目标方进程命令行 |
| 112 | `roles` | `roles.target.process.created_time` | `string(datetime)` | 单值 | N | `2026-08-04T10:15:30.123Z` | 目标方进程创建时间 |
| 113 | `roles` | `roles.target.process.working_directory` | `string` | 单值 | N | `C:\Windows\System32\` | 目标方进程工作目录 |
| 114 | `roles` | `roles.target.process.integrity` | `string` | 单值 | N | `System` | 目标方进程完整性级别 |
| 115 | `roles` | `roles.target.process.terminated_time` | `string(datetime)` | 单值 | N | `2024-12-18T02:46:43.718Z` | 目标方进程结束时间 |
| 116 | `roles` | `roles.target.process.tree_info` | `string` | 单值 | N | `tree-info-01` | 目标方进程进程树信息 |
| 117 | `roles` | `roles.target.process.user.name` | `string` | 单值 | N | `alice` | 目标方用户名称 |
| 118 | `roles` | `roles.target.process.user.id` | `string` | 单值 | N | `id-01` | 目标方用户编号 |
| 119 | `roles` | `roles.target.process.user.session_id` | `string` | 单值 | N | `0` | 目标进程运行用户的会话编号 |
| 120 | `roles` | `roles.target.process.file.hashes.md5` | `string` | 单值 | N | `d41d8cd98f00b204e9800998ecf8427e` | 目标方MD5 |
| 121 | `roles` | `roles.target.process.file.hashes.sha1` | `string` | 单值 | N | `356a192b7913b04c54574d18c28d46e6395428ab` | 目标方SHA-1 |
| 122 | `roles` | `roles.target.process.file.hashes.sha256` | `string` | 单值 | N | `a3f1...cdef` | 目标方SHA-256 |
| 123 | `roles` | `roles.target.process.file.original_name` | `string` | 单值 | N | `Wmiprvse.exe` | 目标方文件原始文件名称 |
| 124 | `roles` | `roles.target.process.file.internal_name` | `string` | 单值 | N | `Wmiprvse.exe` | 目标方文件内部名称 |
| 125 | `roles` | `roles.target.process.file.company_name` | `string` | 单值 | N | `Microsoft Corporation` | 目标方文件厂商名称 |
| 126 | `roles` | `roles.target.process.file.product.name` | `string` | 单值 | N | `Microsoft Windows Operating System` | 目标方产品名称 |
| 127 | `roles` | `roles.target.process.file.description` | `string` | 单值 | N | `WMI Provider Host` | 目标方文件描述 |
| 128 | `roles` | `roles.target.process.file.version` | `string` | 单值 | N | `10.0.19041.3636` | 目标方文件版本 |
| 129 | `roles` | `roles.target.process.file.signatures[].signer` | `string` | 多值对象成员 | N | `Microsoft Windows Publisher` | 目标方签名列表签名主体 |
| 130 | `roles` | `roles.target.process.file.signatures[].status` | `string` | 多值对象成员 | N | `verified` | 目标方签名列表状态 |
| 131 | `roles` | `roles.target.file.hashes.value` | `string` | 单值 | N | `value-01` | 目标方值 |
| 132 | `roles` | `roles.target.service.id` | `string` | 单值 | N | `id-01` | 目标方服务编号 |
| 133 | `roles` | `roles.observer.product.name` | `string` | 单值 | N | `天眼` | 观察方产品名称 |
| 134 | `roles` | `roles.observer.device.id` | `string` | 单值 | N | `id-01` | 观察方设备编号 |
| 135 | `roles` | `roles.observer.device.name` | `string` | 单值 | N | `skyeye-sensor-01` | 观察方设备名称 |
| 136 | `roles` | `roles.observer.device.vendor` | `string` | 单值 | N | `奇安信` | 观察方设备厂商 |
| 137 | `roles` | `roles.observer.device.type` | `string` | 单值 | N | `network_sensor` | 观察方设备类型 |
| 138 | `roles` | `roles.observer.device.serial_number` | `string` | 单值 | N | `SN202608040001` | 观察方设备序列号 |
| 139 | `roles` | `roles.observer.device.ip` | `string` | 单值 | N | `198.51.100.23` | 观察方设备IP 地址 |
| 140 | `roles` | `roles.observer.device.ipv4` | `string` | 单值 | N | `198.51.100.23` | 观察方设备IPv4 地址 |
| 141 | `roles` | `roles.observer.device.ipv6` | `string` | 单值 | N | `2001:db8::23` | 观察方设备IPv6 地址 |
| 142 | `roles` | `roles.observer.device.ip_addresses[].address` | `string` | 多值对象成员 | N | `address-01` | 观察方地址 |
| 143 | `roles` | `roles.observer.device.model` | `string` | 单值 | N | `NS-5000` | 观察方设备型号 |
| 144 | `roles` | `roles.observer.type` | `string` | 单值 | N | `security_sensor` | 观察方类型 |
| 145 | `roles` | `roles.related[].ref_id` | `string` | 多值对象成员 | N | `host_target_01` | 关联对象事件内引用编号 |
| 146 | `roles` | `roles.related[].entity_type` | `string` | 多值对象成员 | N | `host` | 关联对象实体类型 |
| 147 | `roles` | `roles.related[].relation_type` | `string` | 多值对象成员 | N | `communicates_with` | 关联对象关系类型 |
| 148 | `roles` | `roles.related[].is_primary` | `boolean` | 多值对象成员 | N | `true` | 关联对象是否主对象 |
| 149 | `roles` | `roles.related[].endpoint.ip` | `string` | 多值对象成员 | N | `198.51.100.23` | 关联对象网络端点IP 地址 |
| 150 | `roles` | `roles.related[].endpoint.ipv4` | `string` | 多值对象成员 | N | `198.51.100.23` | 关联对象网络端点IPv4 地址 |
| 151 | `roles` | `roles.related[].endpoint.ipv6` | `string` | 多值对象成员 | N | `2001:db8::23` | 关联对象网络端点IPv6 地址 |
| 152 | `roles` | `roles.related[].endpoint.port` | `integer` | 多值对象成员 | N | `443` | 关联对象网络端点端口 |
| 153 | `roles` | `roles.related[].endpoint.mac` | `string` | 多值对象成员 | N | `00:00:5E:00:53:65` | 关联对象网络端点MAC 地址 |
| 154 | `roles` | `roles.related[].user.name` | `string` | 多值对象成员 | N | `alice` | 关联对象用户名称 |
| 155 | `roles` | `roles.related[].user.uid` | `string` | 多值对象成员 | N | `uid-1001` | 关联对象用户唯一标识 |
| 156 | `roles` | `roles.related[].user.domain` | `string` | 多值对象成员 | N | `threat` | 关联用户所属域 |
| 157 | `roles` | `roles.related[].account.name` | `string` | 多值对象成员 | N | `svc_web` | 关联对象账号名称 |
| 158 | `roles` | `roles.related[].host.name` | `string` | 多值对象成员 | N | `web-server-01` | 关联对象主机名称 |
| 159 | `roles` | `roles.related[].host.id` | `string` | 多值对象成员 | N | `id-01` | 关联对象主机编号 |
| 160 | `roles` | `roles.related[].host.ip` | `string` | 多值对象成员 | N | `198.51.100.23` | 关联对象主机IP 地址 |
| 161 | `roles` | `roles.related[].host.ipv4` | `string` | 多值对象成员 | N | `198.51.100.23` | 关联对象主机IPv4 地址 |
| 162 | `roles` | `roles.related[].host.ipv6` | `string` | 多值对象成员 | N | `2001:db8::23` | 关联对象主机IPv6 地址 |
| 163 | `roles` | `roles.related[].host.os.name` | `string` | 多值对象成员 | N | `Ubuntu` | 关联对象名称 |
| 164 | `roles` | `roles.related[].host.os.type` | `string` | 多值对象成员 | N | `linux` | 关联对象类型 |
| 165 | `roles` | `roles.related[].host.os.version` | `string` | 多值对象成员 | N | `22.04` | 关联对象版本 |
| 166 | `roles` | `roles.related[].process.name` | `string` | 多值对象成员 | N | `curl` | 关联对象进程名称 |
| 167 | `roles` | `roles.related[].process.pid` | `string` | 多值对象成员 | N | `23841` | 关联对象进程进程号 |
| 168 | `roles` | `roles.related[].process.uid` | `string` | 多值对象成员 | N | `uid-1001` | 关联对象进程唯一标识 |
| 169 | `roles` | `roles.related[].process.path` | `string` | 多值对象成员 | N | `/usr/bin/curl` | 关联对象进程路径 |
| 170 | `roles` | `roles.related[].process.cmdline` | `string` | 多值对象成员 | N | `curl https://portal.example.com/login` | 关联对象进程命令行 |
| 171 | `roles` | `roles.related[].process.file.hashes.md5` | `string` | 多值对象成员 | N | `d41d8cd98f00b204e9800998ecf8427e` | 关联对象MD5 |
| 172 | `roles` | `roles.related[].process.file.original_name` | `string` | 多值对象成员 | N | `GPUpdate.exe` | 关联对象文件原始文件名称 |
| 173 | `roles` | `roles.related[].process.file.internal_name` | `string` | 多值对象成员 | N | `GPUpdate.exe` | 关联对象文件内部名称 |
| 174 | `roles` | `roles.related[].process.file.signatures[].signer` | `string` | 多值对象成员 | N | `Microsoft Windows` | 关联对象签名列表签名主体 |
| 175 | `roles` | `roles.related[].file.path` | `string` | 多值对象成员 | N | `/var/www/html/login.php` | 关联对象文件路径 |
| 176 | `roles` | `roles.related[].file.name` | `string` | 多值对象成员 | N | `login.php` | 关联对象文件名称 |
| 177 | `roles` | `roles.related[].file.size` | `integer` | 多值对象成员 | N | `1024` | 关联对象文件大小 |
| 178 | `roles` | `roles.related[].file.mime_type` | `string` | 多值对象成员 | N | `text/x-php` | 关联对象文件MIME 类型 |
| 179 | `roles` | `roles.related[].file.created_time` | `string(datetime)` | 多值对象成员 | N | `2026-08-04T10:15:30.123Z` | 关联对象文件创建时间 |
| 180 | `roles` | `roles.related[].file.modified_time` | `string(datetime)` | 多值对象成员 | N | `2026-08-04T10:15:30.123Z` | 关联对象文件修改时间 |
| 181 | `roles` | `roles.related[].file.hashes.md5` | `string` | 多值对象成员 | N | `d41d8cd98f00b204e9800998ecf8427e` | 关联对象MD5 |
| 182 | `roles` | `roles.related[].file.hashes.sha1` | `string` | 多值对象成员 | N | `356a192b7913b04c54574d18c28d46e6395428ab` | 关联对象SHA-1 |
| 183 | `roles` | `roles.related[].file.hashes.sha256` | `string` | 多值对象成员 | N | `a3f1...cdef` | 关联对象SHA-256 |
| 184 | `roles` | `roles.related[].service.name` | `string` | 多值对象成员 | N | `https` | 关联对象服务名称 |
| 185 | `roles` | `roles.related[].service.id` | `string` | 多值对象成员 | N | `id-01` | 关联对象服务编号 |
| 186 | `roles` | `roles.related[].service.port` | `integer` | 多值对象成员 | N | `443` | 关联对象服务端口 |
| 187 | `roles` | `roles.related[].domain.name` | `string` | 多值对象成员 | N | `cdn.example.com` | 关联域名 |
| 188 | `roles` | `roles.related[].url.full` | `string` | 多值对象成员 | N | `https://cdn.example.com/app.js` | 关联完整 URL |
| 189 | `facets` | `facets.email.recipients[]` | `array<string>` | 多值 | N | `[recipients-01]` | 邮件收件人列表 |
| 190 | `facets` | `facets.email.attachments[].name` | `string` | 多值对象成员 | N | `login.php` | 附件列表名称 |
| 191 | `facets` | `facets.network.protocol` | `string` | 单值 | N | `tcp` | 网络传输协议 |
| 192 | `facets` | `facets.network.direction` | `string` | 单值 | N | `W2L` | 网络通信方向 |
| 193 | `facets` | `facets.network.session_id` | `string` | 单值 | N | `session-001` | 网络会话编号 |
| 194 | `facets` | `facets.network.nat.original.ip` | `string` | 单值 | N | `198.51.100.23` | NAT 转换前 IP 地址 |
| 195 | `facets` | `facets.network.nat.original.ipv4` | `string` | 单值 | N | `198.51.100.23` | NAT 转换前 IPv4 地址 |
| 196 | `facets` | `facets.network.nat.original.ipv6` | `string` | 单值 | N | `2001:db8::23` | NAT 转换前 IPv6 地址 |
| 197 | `facets` | `facets.network.nat.translated.ip` | `string` | 单值 | N | `198.51.100.23` | NAT 转换后 IP 地址 |
| 198 | `facets` | `facets.network.nat.translated.ipv4` | `string` | 单值 | N | `198.51.100.23` | NAT 转换后 IPv4 地址 |
| 199 | `facets` | `facets.network.nat.translated.ipv6` | `string` | 单值 | N | `2001:db8::23` | NAT 转换后 IPv6 地址 |
| 200 | `facets` | `facets.application.name` | `string` | 单值 | N | `HTTPS` | 应用名称 |
| 201 | `facets` | `facets.http.request.method` | `string` | 单值 | N | `GET` | HTTP 请求方法 |
| 202 | `facets` | `facets.http.response.status_code` | `integer` | 单值 | N | `403` | HTTP 响应状态码 |
| 203 | `facets` | `facets.http.request.host` | `string` | 单值 | N | `portal.example.com` | HTTP 请求主机 |
| 204 | `facets` | `facets.http.request.forwarded_for[].ip` | `string` | 多值对象成员 | N | `198.51.100.23` | IP 地址 |
| 205 | `facets` | `facets.container.kubernetes.namespace` | `string` | 单值 | N | `security-prod` | 命名空间 |
| 206 | `facets` | `facets.container.kubernetes.pod.name` | `string` | 单值 | N | `portal-web-7d9f8c6b5-x2k4p` | Pod名称 |
| 207 | `facets` | `facets.container.kubernetes.pod.id` | `string` | 单值 | N | `id-01` | Pod编号 |
| 208 | `facets` | `facets.container.kubernetes.cluster.id` | `string` | 单值 | N | `id-01` | 集群编号 |
| 209 | `facets` | `facets.container.kubernetes.cluster.name` | `string` | 单值 | N | `prod-cluster` | 集群名称 |
| 210 | `facets` | `facets.container.kubernetes.container.id` | `string` | 单值 | N | `id-01` | 容器编号 |
| 211 | `facets` | `facets.container.kubernetes.container.name` | `string` | 单值 | N | `portal-web` | 容器名称 |
| 212 | `facets` | `facets.dns.question.name` | `string` | 单值 | N | `portal.example.com` | DNS 查询域名 |
| 213 | `facets` | `facets.dns.question.type` | `string` | 单值 | N | `A` | DNS 查询记录类型 |
| 214 | `facets` | `facets.dns.answers[].address` | `string` | 多值对象成员 | N | `203.0.113.28` | DNS 应答地址 |
| 215 | `facets` | `facets.dns.response.code` | `string` | 单值 | N | `0` | DNS 应答状态代码 |
| 216 | `facets` | `facets.process.injection.method` | `string` | 单值 | N | `remote_thread` | 进程注入方式 |
| 217 | `facets` | `facets.process.injection.target_thread.id` | `string` | 单值 | N | `17716` | 被注入目标线程编号 |
| 218 | `facets` | `facets.process.injection.target_thread.address` | `string` | 单值 | N | `140701423552944` | 被注入目标线程入口地址 |
| 219 | `facets` | `facets.process.injection.target_thread.arguments` | `string` | 单值 | N | `718250356736` | 传递给被注入目标线程的参数 |
| 220 | `facets` | `facets.process.injection.target_thread.module_path` | `string` | 单值 | N | `C:\Windows\servicing\TrustedInstaller.exe` | 被注入目标线程关联的模块路径 |
| 221 | `facets` | `facets.registry.key.path` | `string` | 单值 | N | `\REGISTRY\MACHINE\SYSTEM\ControlSet001\Services\wuauserv` | 被操作的注册表键完整路径 |
| 222 | `facets` | `facets.registry.key.renamed_path` | `string` | 单值 | N | `\REGISTRY\MACHINE\SYSTEM\ControlSet001\Services\wuauserv-new` | 注册表键重命名后的完整路径 |
| 223 | `facets` | `facets.registry.value.name` | `string` | 单值 | N | `Start` | 被操作的注册表值名称 |
| 224 | `facets` | `facets.registry.value.type` | `string` | 单值 | N | `reg_dword` | 注册表值的数据类型 |
| 225 | `facets` | `facets.registry.value.previous.data` | `string` | 单值 | N | `3` | 注册表值变更前的数据 |
| 226 | `facets` | `facets.registry.value.previous.size` | `integer` | 单值 | N | `4` | 注册表值变更前的数据字节数 |
| 227 | `facets` | `facets.registry.value.current.data` | `string` | 单值 | N | `2` | 注册表值变更后的数据 |
| 228 | `facets` | `facets.registry.value.current.size` | `integer` | 单值 | N | `4` | 注册表值变更后的数据字节数 |
| 229 | `facets` | `facets.email.sender` | `string` | 单值 | N | `security@example.com` | 邮件实际发件人 |
| 230 | `facets` | `facets.email.subject` | `string` | 单值 | N | `安全告警通知` | 邮件主题 |
| 231 | `facets` | `facets.http.client.browser.type` | `string` | 单值 | N | `network_sensor` | 浏览器类型 |
| 232 | `facets` | `facets.http.request.cdn.endpoints[].ip` | `string` | 多值对象成员 | N | `198.51.100.23` | IP 地址 |
| 233 | `facets` | `facets.http.request.cdn.endpoints[].ipv4` | `string` | 多值对象成员 | N | `198.51.100.23` | IPv4 地址 |
| 234 | `facets` | `facets.http.request.cdn.endpoints[].ipv6` | `string` | 多值对象成员 | N | `2001:db8::23` | IPv6 地址 |
| 235 | `facets` | `facets.http.request.headers` | `string` | 单值 | N | `Host: portal.example.com` | HTTP 请求头 |
| 236 | `facets` | `facets.http.request.query` | `string` | 单值 | N | `id=1%27` | HTTP 请求查询参数 |
| 237 | `facets` | `facets.http.request.referer` | `string` | 单值 | N | `https://portal.example.com/` | HTTP 请求来源页面 |
| 238 | `facets` | `facets.http.request.user_agent` | `string` | 单值 | N | `Mozilla/5.0` | HTTP 用户代理 |
| 239 | `facets` | `facets.http.response.headers` | `string` | 单值 | N | `Content-Type: text/html` | HTTP 响应头 |
| 240 | `facets` | `facets.network.intermediaries` | `array<string>` | 单值 | N | `[intermediaries-01]` | 网络中间节点列表 |
| 241 | `facets` | `facets.network.intermediaries[].ip` | `string` | 多值对象成员 | N | `198.51.100.23` | 网络中间节点 IP 地址 |
| 242 | `facets` | `facets.network.protocol.code` | `string` | 单值 | N | `CODE-01` | 网络协议代码 |
| 243 | `facets` | `facets.network.traffic.total_bytes` | `integer` | 单值 | N | `8192` | 网络流量总字节数 |
| 244 | `facets` | `facets.network.traffic.total_packets` | `integer` | 单值 | N | `24` | 网络流量总包数 |
| 245 | `facets` | `facets.network.zone.name` | `string` | 单值 | N | `portal-web` | 网络区域名称 |
| 246 | `source_finding` | `source_finding.title` | `string` | 单值 | N | `SQL 注入攻击` | 标题 |
| 247 | `source_finding` | `source_finding.severity` | `string` | 单值 | N | `high` | 严重级别 |
| 248 | `source_finding` | `source_finding.original_severity` | `string` | 单值 | N | `original-severity-01` | original severity |
| 249 | `source_finding` | `source_finding.category` | `string` | 单值 | N | `web_attack` | 来源检测结果分类 |
| 250 | `source_finding` | `source_finding.category.original.code` | `string` | 单值 | N | `CODE-01` | 原始分类代码 |
| 251 | `source_finding` | `source_finding.category.original.name` | `string` | 单值 | N | `portal-web` | 原始分类名称 |
| 252 | `source_finding` | `source_finding.category.normalized.level1.code` | `string` | 单值 | N | `CODE-01` | 一级代码 |
| 253 | `source_finding` | `source_finding.category.normalized.level1.name` | `string` | 单值 | N | `portal-web` | 一级名称 |
| 254 | `source_finding` | `source_finding.category.normalized.level2.code` | `string` | 单值 | N | `CODE-01` | 二级代码 |
| 255 | `source_finding` | `source_finding.category.normalized.level2.name` | `string` | 单值 | N | `portal-web` | 二级名称 |
| 256 | `source_finding` | `source_finding.description` | `string` | 单值 | N | `请求参数命中 SQL 注入检测规则` | 描述 |
| 257 | `source_finding` | `source_finding.status` | `string` | 单值 | N | `active` | 来源检测结果状态 |
| 258 | `source_finding` | `source_finding.count` | `integer` | 单值 | N | `3` | 数量 |
| 259 | `source_finding` | `source_finding.behavior` | `string` | 单值 | N | `sql_injection` | 行为 |
| 260 | `source_finding` | `source_finding.killchain` | `string` | 单值 | N | `initial_access` | 杀伤链 |
| 261 | `source_finding` | `source_finding.detection_method` | `string` | 单值 | N | `signature` | 检测方式 |
| 262 | `source_finding` | `source_finding.remediation` | `string` | 单值 | N | `阻断来源 IP 并检查目标应用` | 处置建议 |
| 263 | `source_finding` | `source_finding.compromise_status` | `string` | 单值 | N | `not_compromised` | 失陷状态 |
| 264 | `source_finding` | `source_finding.attack_result` | `string` | 单值 | N | `blocked` | 攻击结果 |
| 265 | `source_finding` | `source_finding.attacker.endpoint.ip` | `string` | 单值 | N | `198.51.100.23` | IP 地址 |
| 266 | `source_finding` | `source_finding.attacker.endpoint.ipv4` | `string` | 单值 | N | `198.51.100.23` | IPv4 地址 |
| 267 | `source_finding` | `source_finding.attacker.endpoint.ipv6` | `string` | 单值 | N | `2001:db8::23` | IPv6 地址 |
| 268 | `source_finding` | `source_finding.attacker.endpoint.port` | `integer` | 单值 | N | `443` | 端口 |
| 269 | `source_finding` | `source_finding.attacker.geo.continent.name` | `string` | 单值 | N | `北美洲` | 检测主张中攻击方 IP 所在洲名称 |
| 270 | `source_finding` | `source_finding.attacker.geo.country.code` | `string` | 单值 | N | `US` | 检测主张中攻击方 IP 所在国家或地区的 ISO 3166-1 Alpha-2 代码 |
| 271 | `source_finding` | `source_finding.attacker.geo.country.name` | `string` | 单值 | N | `美国` | 检测主张中攻击方 IP 所在国家或地区名称 |
| 272 | `source_finding` | `source_finding.attacker.geo.region.name` | `string` | 单值 | N | `California` | 检测主张中攻击方 IP 所在省、州或一级行政区名称 |
| 273 | `source_finding` | `source_finding.attacker.geo.city.name` | `string` | 单值 | N | `Mountain View` | 检测主张中攻击方 IP 所在城市名称 |
| 274 | `source_finding` | `source_finding.attacker.geo.coordinates.latitude` | `number` | 单值 | N | `37.422` | 检测主张中攻击方 IP 地理位置纬度 |
| 275 | `source_finding` | `source_finding.attacker.geo.coordinates.longitude` | `number` | 单值 | N | `-122.085` | 检测主张中攻击方 IP 地理位置经度 |
| 276 | `source_finding` | `source_finding.attacker.resource.id` | `string` | 单值 | N | `AST-0008` | 检测主张中攻击方资产编号 |
| 277 | `source_finding` | `source_finding.attacker.resource.name` | `string` | 单值 | N | `攻击源终端-01` | 检测主张中攻击方资产名称 |
| 278 | `source_finding` | `source_finding.attacker.resource.type` | `string` | 单值 | N | `terminal` | 检测主张中攻击方资产类型 |
| 279 | `source_finding` | `source_finding.attacker.resource.system.id` | `string` | 单值 | N | `SYS-004` | 检测主张中攻击方资产所属业务系统编号 |
| 280 | `source_finding` | `source_finding.attacker.resource.system.name` | `string` | 单值 | N | `财务系统` | 检测主张中攻击方资产所属业务系统名称 |
| 281 | `source_finding` | `source_finding.attacker.resource.organization.name` | `string` | 单值 | N | `示例集团财务部` | 检测主张中攻击方资产所属组织名称 |
| 282 | `source_finding` | `source_finding.victim.endpoint.ip` | `string` | 单值 | N | `198.51.100.23` | IP 地址 |
| 283 | `source_finding` | `source_finding.victim.endpoint.ipv4` | `string` | 单值 | N | `198.51.100.23` | IPv4 地址 |
| 284 | `source_finding` | `source_finding.victim.endpoint.ipv6` | `string` | 单值 | N | `2001:db8::23` | IPv6 地址 |
| 285 | `source_finding` | `source_finding.victim.geo.continent.name` | `string` | 单值 | N | `北美洲` | 检测主张中受害方 IP 所在洲名称 |
| 286 | `source_finding` | `source_finding.victim.geo.country.code` | `string` | 单值 | N | `US` | 检测主张中受害方 IP 所在国家或地区的 ISO 3166-1 Alpha-2 代码 |
| 287 | `source_finding` | `source_finding.victim.geo.country.name` | `string` | 单值 | N | `美国` | 检测主张中受害方 IP 所在国家或地区名称 |
| 288 | `source_finding` | `source_finding.victim.geo.region.name` | `string` | 单值 | N | `Ohio` | 检测主张中受害方 IP 所在省、州或一级行政区名称 |
| 289 | `source_finding` | `source_finding.victim.geo.city.name` | `string` | 单值 | N | `Columbus` | 检测主张中受害方 IP 所在城市名称 |
| 290 | `source_finding` | `source_finding.victim.geo.coordinates.latitude` | `number` | 单值 | N | `39.9819` | 检测主张中受害方 IP 地理位置纬度 |
| 291 | `source_finding` | `source_finding.victim.geo.coordinates.longitude` | `number` | 单值 | N | `-82.9048` | 检测主张中受害方 IP 地理位置经度 |
| 292 | `source_finding` | `source_finding.victim.resource.id` | `string` | 单值 | N | `AST-0010` | 检测主张中受害方资产编号 |
| 293 | `source_finding` | `source_finding.victim.resource.name` | `string` | 单值 | N | `日志审计设备` | 检测主张中受害方资产名称 |
| 294 | `source_finding` | `source_finding.victim.resource.type` | `string` | 单值 | N | `security_device` | 检测主张中受害方资产类型 |
| 295 | `source_finding` | `source_finding.victim.resource.system.id` | `string` | 单值 | N | `SYS-005` | 检测主张中受害方资产所属业务系统编号 |
| 296 | `source_finding` | `source_finding.victim.resource.system.name` | `string` | 单值 | N | `审计系统` | 检测主张中受害方资产所属业务系统名称 |
| 297 | `source_finding` | `source_finding.victim.resource.organization.name` | `string` | 单值 | N | `示例集团安全部` | 检测主张中受害方资产所属组织名称 |
| 298 | `source_finding` | `source_finding.attack_direction` | `string` | 单值 | N | `W2L` | 检测产品认定的攻击方到受害方方向 |
| 299 | `source_finding` | `source_finding.malware.name` | `string` | 单值 | N | `ChinaChopper` | 恶意软件名称 |
| 300 | `source_finding` | `source_finding.malware.type` | `string` | 单值 | N | `webshell` | 恶意软件类型 |
| 301 | `source_finding` | `source_finding.malware.family_id` | `string` | 单值 | N | `family-001` | 恶意软件家族编号 |
| 302 | `source_finding` | `source_finding.rule.signature_id` | `string` | 单值 | N | `WEB-SQLI-001` | 签名编号 |
| 303 | `source_finding` | `source_finding.rule.id` | `string` | 单值 | N | `rule-1001` | 规则编号 |
| 304 | `source_finding` | `source_finding.rule.label` | `string` | 单值 | N | `SQL 注入` | 标签 |
| 305 | `source_finding` | `source_finding.rule.policy_id` | `string` | 单值 | N | `policy-web-01` | 策略编号 |
| 306 | `source_finding` | `source_finding.action` | `string` | 单值 | N | `block` | 动作 |
| 307 | `source_finding` | `source_finding.original_id` | `string` | 单值 | N | `alert-origin-98765` | 来源原始编号 |
| 308 | `source_finding` | `source_finding.ioc.value` | `string` | 单值 | N | `198.51.100.23` | 威胁指标值 |
| 309 | `source_finding` | `source_finding.evidence.match.value` | `string` | 单值 | N | `value-01` | 检测证据匹配值 |
| 310 | `source_finding` | `source_finding.mitre.technique_id` | `string` | 单值 | N | `T1190` | 技术编号 |
| 311 | `source_finding` | `source_finding.vulnerability.cve` | `string` | 单值 | N | `CVE-2024-12345` | 漏洞 CVE 编号 |
| 312 | `source_finding` | `source_finding.vulnerability.id` | `string` | 单值 | N | `id-01` | 漏洞编号 |
| 313 | `source_finding` | `source_finding.action.code` | `string` | 单值 | N | `CODE-01` | 动作代码 |
| 314 | `source_finding` | `source_finding.affected_platform` | `string` | 单值 | N | `affected-platform-01` | affected platform |
| 315 | `source_finding` | `source_finding.attention.content` | `string` | 单值 | N | `content-01` | 内容 |
| 316 | `source_finding` | `source_finding.attention.type` | `string` | 单值 | N | `network_sensor` | 关注信息类型 |
| 317 | `source_finding` | `source_finding.campaign` | `string` | 单值 | N | `campaign-01` | 攻击活动 |
| 318 | `source_finding` | `source_finding.category_code` | `string` | 单值 | N | `CODE-01` | category code |
| 319 | `source_finding` | `source_finding.category_level2` | `string` | 单值 | N | `category-level2-01` | category level2 |
| 320 | `source_finding` | `source_finding.category_level2_code` | `string` | 单值 | N | `CODE-01` | category level2 code |
| 321 | `source_finding` | `source_finding.confidence` | `string` | 单值 | N | `confidence-01` | 置信度 |
| 322 | `source_finding` | `source_finding.duration` | `integer` | 单值 | N | `1` | 持续时间 |
| 323 | `source_finding` | `source_finding.entities.attackers[].endpoint.ip` | `string` | 多值对象成员 | N | `198.51.100.23` | 关联攻击方 IP 地址 |
| 324 | `source_finding` | `source_finding.entities.attackers[].ref_id` | `string` | 多值对象成员 | N | `host_target_01` | 关联攻击方引用编号 |
| 325 | `source_finding` | `source_finding.entities.attackers[].entity_type` | `string` | 多值对象成员 | N | `host` | 关联攻击方实体类型 |
| 326 | `source_finding` | `source_finding.entities.victims[].ref_id` | `string` | 多值对象成员 | N | `host_target_01` | 关联受害方引用编号 |
| 327 | `source_finding` | `source_finding.entities.victims[].entity_type` | `string` | 多值对象成员 | N | `host` | 关联受害方实体类型 |
| 328 | `source_finding` | `source_finding.entities.affected[].ref_id` | `string` | 多值对象成员 | N | `host_target_01` | 关联受影响对象引用编号 |
| 329 | `source_finding` | `source_finding.entities.affected[].entity_type` | `string` | 多值对象成员 | N | `host` | 关联受影响对象实体类型 |
| 330 | `source_finding` | `source_finding.indicators[].id` | `string` | 多值对象成员 | N | `id-01` | 威胁指标编号 |
| 331 | `source_finding` | `source_finding.indicators[].type` | `string` | 多值对象成员 | N | `network_sensor` | 威胁指标类型 |
| 332 | `source_finding` | `source_finding.indicators[].value` | `string` | 多值对象成员 | N | `value-01` | 威胁指标值 |
| 333 | `source_finding` | `source_finding.indicators[].status` | `string` | 多值对象成员 | N | `active` | 威胁指标状态 |
| 334 | `source_finding` | `source_finding.indicators[].source` | `string` | 多值对象成员 | N | `source-01` | 威胁指标来源 |
| 335 | `source_finding` | `source_finding.indicators[].confidence` | `string` | 多值对象成员 | N | `confidence-01` | 威胁指标置信度 |
| 336 | `source_finding` | `source_finding.rules[].id` | `string` | 多值对象成员 | N | `id-01` | 命中规则编号 |
| 337 | `source_finding` | `source_finding.rules[].signature_id` | `string` | 多值对象成员 | N | `signature-001` | 命中规则签名编号 |
| 338 | `source_finding` | `source_finding.rules[].name` | `string` | 多值对象成员 | N | `portal-web` | 命中规则名称 |
| 339 | `source_finding` | `source_finding.rules[].version` | `string` | 多值对象成员 | N | `version-01` | 命中规则版本 |
| 340 | `source_finding` | `source_finding.rules[].policy_id` | `string` | 多值对象成员 | N | `policy-001` | 命中规则策略编号 |
| 341 | `source_finding` | `source_finding.rules[].policy_name` | `string` | 多值对象成员 | N | `policy-name-01` | 命中规则策略名称 |
| 342 | `source_finding` | `source_finding.rules[].status` | `string` | 多值对象成员 | N | `active` | 命中规则状态 |
| 343 | `source_finding` | `source_finding.evidence.http.location.code` | `string` | 单值 | N | `CODE-01` | HTTP 检测证据位置代码 |
| 344 | `source_finding` | `source_finding.evidence.http.location.name` | `string` | 单值 | N | `portal-web` | HTTP 检测证据位置名称 |
| 345 | `source_finding` | `source_finding.evidence.http.matched_content` | `string` | 单值 | N | `matched-content-01` | HTTP 检测证据命中内容 |
| 346 | `source_finding` | `source_finding.evidence.match.length` | `integer` | 单值 | N | `1` | 检测证据匹配长度 |
| 347 | `source_finding` | `source_finding.evidence.match.offset` | `integer` | 单值 | N | `1` | 检测证据匹配偏移量 |
| 348 | `source_finding` | `source_finding.file.hash_type` | `string` | 单值 | N | `hash-type-01` | 哈希类型 |
| 349 | `source_finding` | `source_finding.hit_count` | `integer` | 单值 | N | `1` | 命中次数 |
| 350 | `source_finding` | `source_finding.ioc.id` | `string` | 单值 | N | `id-01` | 威胁指标编号 |
| 351 | `source_finding` | `source_finding.ioc.source` | `string` | 单值 | N | `threat_intelligence` | source |
| 352 | `source_finding` | `source_finding.ioc.status` | `string` | 单值 | N | `malicious` | 威胁指标状态 |
| 353 | `source_finding` | `source_finding.ioc.type` | `string` | 单值 | N | `ipv4` | 威胁指标类型 |
| 354 | `source_finding` | `source_finding.is_attack_alert` | `boolean` | 单值 | N | `true` | 是否攻击告警 |
| 355 | `source_finding` | `source_finding.malware.family` | `string` | 单值 | N | `WebShell` | family |
| 356 | `source_finding` | `source_finding.malware.family_label` | `string` | 单值 | N | `family-label-01` | family label |
| 357 | `source_finding` | `source_finding.metrics.attack_bytes` | `integer` | 单值 | N | `1` | attack bytes |
| 358 | `source_finding` | `source_finding.metrics.attack_packets` | `integer` | 单值 | N | `1` | attack packets |
| 359 | `source_finding` | `source_finding.mitre.tactics` | `array<string>` | 单值 | N | `[initial-access]` | 战术列表 |
| 360 | `source_finding` | `source_finding.mitre.techniques` | `array<string>` | 单值 | N | `[T1190]` | 技术列表 |
| 361 | `source_finding` | `source_finding.original_category` | `string` | 单值 | N | `original-category-01` | original category |
| 362 | `source_finding` | `source_finding.original_category_code` | `string` | 单值 | N | `CODE-01` | original category code |
| 363 | `source_finding` | `source_finding.original_killchain` | `string` | 单值 | N | `original-killchain-01` | original killchain |
| 364 | `source_finding` | `source_finding.protection.type.code` | `string` | 单值 | N | `CODE-01` | 类型代码 |
| 365 | `source_finding` | `source_finding.protection.type.name` | `string` | 单值 | N | `portal-web` | 类型名称 |
| 366 | `source_finding` | `source_finding.published_time` | `string(datetime)` | 单值 | N | `2026-08-04T10:15:30.123Z` | 发布时间 |
| 367 | `source_finding` | `source_finding.rule.item_id` | `string` | 单值 | N | `item-001` | 规则项编号 |
| 368 | `source_finding` | `source_finding.rule.policy_name` | `string` | 单值 | N | `Web 攻击防护策略` | 策略名称 |
| 369 | `source_finding` | `source_finding.rule.status` | `string` | 单值 | N | `enabled` | 规则状态 |
| 370 | `source_finding` | `source_finding.rule.version` | `string` | 单值 | N | `2026.08` | 规则版本 |
| 371 | `source_finding` | `source_finding.targeted_attack` | `boolean` | 单值 | N | `true` | 是否定向攻击 |
| 372 | `source_finding` | `source_finding.threshold.unit` | `string` | 单值 | N | `unit-01` | 告警阈值单位 |
| 373 | `source_finding` | `source_finding.threshold.value` | `number` | 单值 | N | `1` | 告警触发阈值 |
| 374 | `source_finding` | `source_finding.validity_evidence` | `string` | 单值 | N | `validity-evidence-01` | 有效性证据 |
| 375 | `source_finding` | `source_finding.victim.type` | `string` | 单值 | N | `network_sensor` | 受害方类型 |
| 376 | `source_finding` | `source_finding.vulnerability.cnnvd` | `string` | 单值 | N | `CNNVD-202401-1234` | 漏洞 CNNVD 编号 |
| 377 | `source_finding` | `source_finding.vulnerability.description` | `string` | 单值 | N | `攻击者可通过构造请求执行任意代码` | 漏洞描述 |
| 378 | `source_finding` | `source_finding.vulnerability.impact` | `string` | 单值 | N | `远程代码执行` | 漏洞影响 |
| 379 | `source_finding` | `source_finding.vulnerability.name` | `string` | 单值 | N | `WebPortal 远程代码执行漏洞` | 漏洞名称 |
| 380 | `source_finding` | `source_finding.vulnerability.remediation` | `string` | 单值 | N | `升级至安全版本` | 漏洞修复建议 |
| 381 | `source_finding` | `source_finding.vulnerability.type` | `string` | 单值 | N | `remote_code_execution` | 漏洞类型 |
| 382 | `source_finding` | `source_finding.weak_password` | `string` | 单值 | N | `weak-password-01` | 弱密码 |
| 383 | `facets` | `facets.network.nat.original.source.ip` | `string` | 单值 | N | `198.51.100.23` | NAT 转换前源 IP 地址 |
| 384 | `facets` | `facets.network.nat.original.source.port` | `integer` | 单值 | N | `443` | NAT 转换前源端口 |
| 385 | `facets` | `facets.network.nat.original.target.ip` | `string` | 单值 | N | `198.51.100.23` | NAT 转换前目标 IP 地址 |
| 386 | `facets` | `facets.network.nat.original.target.port` | `integer` | 单值 | N | `443` | NAT 转换前目标端口 |
| 387 | `facets` | `facets.network.nat.translated.source.ip` | `string` | 单值 | N | `198.51.100.23` | NAT 转换后源 IP 地址 |
| 388 | `facets` | `facets.network.nat.translated.source.port` | `integer` | 单值 | N | `443` | NAT 转换后源端口 |
| 389 | `facets` | `facets.network.nat.translated.target.ip` | `string` | 单值 | N | `198.51.100.23` | NAT 转换后目标 IP 地址 |
| 390 | `facets` | `facets.network.nat.translated.target.port` | `integer` | 单值 | N | `443` | NAT 转换后目标端口 |
| 391 | `roles` | `roles.source.user.uid` | `string` | 单值 | N | `uid-1001` | 发起方用户唯一标识 |
| 392 | `roles` | `roles.target.user.uid` | `string` | 单值 | N | `uid-1001` | 目标方用户唯一标识 |
| 393 | `roles` | `roles.source.user.domain` | `string` | 单值 | N | `threat` | 发起方用户领域 |
| 394 | `roles` | `roles.target.user.domain` | `string` | 单值 | N | `threat` | 目标方用户领域 |
| 395 | `facets` | `facets.authentication.auth_type` | `string` | 单值 | N | `password` | 认证方式 |
| 396 | `facets` | `facets.authentication.auth_result` | `string` | 单值 | N | `failed` | 认证结果 |
| 397 | `facets` | `facets.authentication.auth_failure_reason` | `string` | 单值 | N | `invalid_password` | 认证失败原因 |
| 398 | `facets` | `facets.authentication.session_id` | `string` | 单值 | N | `session-001` | 认证会话编号 |
| 399 | `facets` | `facets.network.application_protocol` | `string` | 单值 | N | `https` | 应用层协议 |
| 400 | `facets` | `facets.network.connection_state` | `string` | 单值 | N | `established` | 网络连接状态 |
| 401 | `roles` | `roles.target.file.owner.id` | `string` | 单值 | N | `id-01` | 目标方所有者编号 |
| 402 | `roles` | `roles.target.file.owner.name` | `string` | 单值 | N | `portal-web` | 目标方所有者名称 |
| 403 | `roles` | `roles.target.file.group.id` | `string` | 单值 | N | `id-01` | 目标方编号 |
| 404 | `roles` | `roles.target.file.group.name` | `string` | 单值 | N | `生产环境` | 目标方名称 |
| 405 | `roles` | `roles.target.file.permission.mode` | `string` | 单值 | N | `mode-01` | 目标方权限模式 |
| 406 | `roles` | `roles.target.file.directory` | `string` | 单值 | N | `directory-01` | 目标方文件目录 |
| 407 | `roles` | `roles.target.file.extension` | `string` | 单值 | N | `extension-01` | 目标方文件扩展名 |
| 408 | `roles` | `roles.target.file.modified_time` | `string(datetime)` | 单值 | N | `2026-08-04T10:15:30.123Z` | 目标方文件修改时间 |
| 409 | `roles` | `roles.source.host.ip` | `string` | 单值 | N | `198.51.100.23` | 发起方主机IP 地址 |
| 410 | `roles` | `roles.source.host.ipv4` | `string` | 单值 | N | `198.51.100.23` | 发起方主机IPv4 地址 |
| 411 | `roles` | `roles.source.host.ipv6` | `string` | 单值 | N | `2001:db8::23` | 发起方主机IPv6 地址 |
| 412 | `roles` | `roles.target.host.ip` | `string` | 单值 | N | `198.51.100.23` | 目标方主机IP 地址 |
| 413 | `roles` | `roles.target.host.ipv4` | `string` | 单值 | N | `198.51.100.23` | 目标方主机IPv4 地址 |
| 414 | `roles` | `roles.target.host.ipv6` | `string` | 单值 | N | `2001:db8::23` | 目标方主机IPv6 地址 |
| 415 | `facets` | `facets.email.from` | `string` | 单值 | N | `soc@example.com` | 邮件作者地址 |
| 416 | `facets` | `facets.email.attachments[].hashes.md5` | `string` | 多值对象成员 | N | `d41d8cd98f00b204e9800998ecf8427e` | MD5 |
| 417 | `facets` | `facets.email.attachments[].hashes.sha256` | `string` | 多值对象成员 | N | `a3f1...cdef` | SHA-256 |
| 418 | `roles` | `roles.target.account.name` | `string` | 单值 | N | `svc_web` | 目标方账号名称 |
| 419 | `roles` | `roles.observer.device.os.name` | `string` | 单值 | N | `Ubuntu` | 观察方名称 |
| 420 | `roles` | `roles.observer.device.os.type` | `string` | 单值 | N | `linux` | 观察方类型 |
| 421 | `roles` | `roles.observer.device.os.version` | `string` | 单值 | N | `22.04` | 观察方版本 |
| 422 | `roles` | `roles.source.host.os.version` | `string` | 单值 | N | `22.04` | 发起方版本 |
| 423 | `roles` | `roles.target.host.os.version` | `string` | 单值 | N | `22.04` | 目标方版本 |
| 424 | `facets` | `facets.email.cc` | `array<string>` | 单值 | N | `[cc-01]` | 邮件抄送人列表 |
| 425 | `facets` | `facets.email.message_id` | `string` | 单值 | N | `<20260804.0001@example.com>` | 邮件消息编号 |
| 426 | `roles` | `roles.source.host.os.name` | `string` | 单值 | N | `Ubuntu` | 发起方名称 |
| 427 | `roles` | `roles.source.resource.id` | `string` | 单值 | N | `id-01` | 发起方资源编号 |
| 428 | `roles` | `roles.source.resource.name` | `string` | 单值 | N | `production-web-service` | 发起方资源名称 |
| 429 | `roles` | `roles.source.resource.type` | `string` | 单值 | N | `cloud_service` | 发起方资源类型 |
| 430 | `roles` | `roles.source.resource.subtype` | `string` | 单值 | N | `web_application` | 发起方资源subtype |
| 431 | `roles` | `roles.source.resource.vendor` | `string` | 单值 | N | `Alibaba Cloud` | 发起方资源厂商 |
| 432 | `roles` | `roles.source.resource.product` | `string` | 单值 | N | `ECS` | 发起方资源产品 |
| 433 | `roles` | `roles.source.resource.external_id` | `string` | 单值 | N | `external-001` | 发起方资源外部编号 |
| 434 | `roles` | `roles.source.resource.group.id` | `string` | 单值 | N | `id-01` | 发起方编号 |
| 435 | `roles` | `roles.source.resource.group.name` | `string` | 单值 | N | `生产环境` | 发起方名称 |
| 436 | `roles` | `roles.source.resource.system.id` | `string` | 单值 | N | `SYS-004` | 发起方资产所属业务系统编号 |
| 437 | `roles` | `roles.source.resource.system.name` | `string` | 单值 | N | `财务系统` | 发起方资产所属业务系统名称 |
| 438 | `roles` | `roles.source.resource.organization.id` | `string` | 单值 | N | `ORG-001` | 发起方资产所属组织编号 |
| 439 | `roles` | `roles.source.resource.organization.name` | `string` | 单值 | N | `示例集团财务部` | 发起方资产所属组织名称 |
| 440 | `roles` | `roles.carriers[].resource.id` | `string` | 多值对象成员 | N | `id-01` | 载体资源编号 |
| 441 | `roles` | `roles.carriers[].resource.name` | `string` | 多值对象成员 | N | `production-web-service` | 载体资源名称 |
| 442 | `roles` | `roles.carriers[].resource.type` | `string` | 多值对象成员 | N | `cloud_service` | 载体资源类型 |
| 443 | `roles` | `roles.carriers[].resource.subtype` | `string` | 多值对象成员 | N | `web_application` | 载体资源subtype |
| 444 | `roles` | `roles.carriers[].resource.vendor` | `string` | 多值对象成员 | N | `Alibaba Cloud` | 载体资源厂商 |
| 445 | `roles` | `roles.carriers[].resource.product` | `string` | 多值对象成员 | N | `ECS` | 载体资源产品 |
| 446 | `roles` | `roles.carriers[].resource.external_id` | `string` | 多值对象成员 | N | `external-001` | 载体资源外部编号 |
| 447 | `roles` | `roles.carriers[].resource.group.id` | `string` | 多值对象成员 | N | `id-01` | 载体编号 |
| 448 | `roles` | `roles.carriers[].resource.group.name` | `string` | 多值对象成员 | N | `生产环境` | 载体名称 |
| 449 | `roles` | `roles.target.resource.id` | `string` | 单值 | N | `id-01` | 目标方资源编号 |
| 450 | `roles` | `roles.target.resource.name` | `string` | 单值 | N | `production-web-service` | 目标方资源名称 |
| 451 | `roles` | `roles.target.resource.type` | `string` | 单值 | N | `cloud_service` | 目标方资源类型 |
| 452 | `roles` | `roles.target.resource.subtype` | `string` | 单值 | N | `web_application` | 目标方资源subtype |
| 453 | `roles` | `roles.target.resource.vendor` | `string` | 单值 | N | `Alibaba Cloud` | 目标方资源厂商 |
| 454 | `roles` | `roles.target.resource.product` | `string` | 单值 | N | `ECS` | 目标方资源产品 |
| 455 | `roles` | `roles.target.resource.external_id` | `string` | 单值 | N | `external-001` | 目标方资源外部编号 |
| 456 | `roles` | `roles.target.resource.group.id` | `string` | 单值 | N | `id-01` | 目标方编号 |
| 457 | `roles` | `roles.target.resource.group.name` | `string` | 单值 | N | `生产环境` | 目标方名称 |
| 458 | `roles` | `roles.target.resource.system.id` | `string` | 单值 | N | `SYS-005` | 目标方资产所属业务系统编号 |
| 459 | `roles` | `roles.target.resource.system.name` | `string` | 单值 | N | `审计系统` | 目标方资产所属业务系统名称 |
| 460 | `roles` | `roles.target.resource.organization.id` | `string` | 单值 | N | `ORG-002` | 目标方资产所属组织编号 |
| 461 | `roles` | `roles.target.resource.organization.name` | `string` | 单值 | N | `示例集团安全部` | 目标方资产所属组织名称 |
| 462 | `roles` | `roles.observer.resource.id` | `string` | 单值 | N | `id-01` | 观察方资源编号 |
| 463 | `roles` | `roles.observer.resource.name` | `string` | 单值 | N | `production-web-service` | 观察方资源名称 |
| 464 | `roles` | `roles.observer.resource.type` | `string` | 单值 | N | `cloud_service` | 观察方资源类型 |
| 465 | `roles` | `roles.observer.resource.subtype` | `string` | 单值 | N | `web_application` | 观察方资源subtype |
| 466 | `roles` | `roles.observer.resource.vendor` | `string` | 单值 | N | `Alibaba Cloud` | 观察方资源厂商 |
| 467 | `roles` | `roles.observer.resource.product` | `string` | 单值 | N | `ECS` | 观察方资源产品 |
| 468 | `roles` | `roles.observer.resource.external_id` | `string` | 单值 | N | `external-001` | 观察方资源外部编号 |
| 469 | `roles` | `roles.observer.resource.group.id` | `string` | 单值 | N | `id-01` | 观察方编号 |
| 470 | `roles` | `roles.observer.resource.group.name` | `string` | 单值 | N | `生产环境` | 观察方名称 |
| 471 | `roles` | `roles.related[].resource.id` | `string` | 多值对象成员 | N | `id-01` | 关联对象资源编号 |
| 472 | `roles` | `roles.related[].resource.name` | `string` | 多值对象成员 | N | `production-web-service` | 关联对象资源名称 |
| 473 | `roles` | `roles.related[].resource.type` | `string` | 多值对象成员 | N | `cloud_service` | 关联对象资源类型 |
| 474 | `roles` | `roles.related[].resource.subtype` | `string` | 多值对象成员 | N | `web_application` | 关联对象资源subtype |
| 475 | `roles` | `roles.related[].resource.vendor` | `string` | 多值对象成员 | N | `Alibaba Cloud` | 关联对象资源厂商 |
| 476 | `roles` | `roles.related[].resource.product` | `string` | 多值对象成员 | N | `ECS` | 关联对象资源产品 |
| 477 | `roles` | `roles.related[].resource.external_id` | `string` | 多值对象成员 | N | `external-001` | 关联对象资源外部编号 |
| 478 | `roles` | `roles.related[].resource.group.id` | `string` | 多值对象成员 | N | `id-01` | 关联对象编号 |
| 479 | `roles` | `roles.related[].resource.group.name` | `string` | 多值对象成员 | N | `生产环境` | 关联对象名称 |
| 480 | `source_finding` | `source_finding.window.start_time` | `string(datetime)` | 单值 | N | `2026-08-04T10:15:30.123Z` | 检测窗口开始时间 |
| 481 | `source_finding` | `source_finding.window.end_time` | `string(datetime)` | 单值 | N | `2026-08-04T10:15:30.123Z` | 检测窗口结束时间 |
| 482 | `source_finding` | `source_finding.window.duration_ms` | `integer` | 单值 | N | `300000` | 检测窗口持续时间（毫秒） |
| 483 | `facets` | `facets.network.scan.type` | `string` | 单值 | N | `port_scan` | 网络扫描类型 |
| 484 | `facets` | `facets.network.scan.method` | `string` | 单值 | N | `syn` | 网络扫描方法 |
| 485 | `facets` | `facets.network.scan.ports[]` | `array<integer>` | 多值 | N | `[22,80,443]` | 扫描端口列表 |
| 486 | `facets` | `facets.network.scan.port_count` | `integer` | 单值 | N | `3` | 扫描端口数量 |
| 487 | `facets` | `facets.network.scan.target_count` | `integer` | 单值 | N | `12` | 扫描目标数量 |
| 488 | `facets` | `facets.network.scan.interval_ms` | `integer` | 单值 | N | `5000` | 扫描时间间隔（毫秒） |
| 489 | `facets` | `facets.network.traffic.bytes_in` | `integer` | 单值 | N | `2048` | 入方向流量字节数 |
| 490 | `facets` | `facets.network.traffic.bytes_out` | `integer` | 单值 | N | `6144` | 出方向流量字节数 |
| 491 | `facets` | `facets.network.traffic.packets_in` | `integer` | 单值 | N | `8` | 入方向网络包数 |
| 492 | `facets` | `facets.network.traffic.packets_out` | `integer` | 单值 | N | `16` | 出方向网络包数 |
| 493 | `facets` | `facets.network.traffic.rate.value` | `number` | 单值 | N | `1024` | 网络流量速率值 |
| 494 | `facets` | `facets.network.traffic.rate.unit` | `string` | 单值 | N | `bytes_per_second` | 网络流量速率单位 |
| 495 | `facets` | `facets.network.traffic.interval_ms` | `integer` | 单值 | N | `1000` | 网络流量统计间隔（毫秒） |
| 496 | `roles` | `roles.related[].device.id` | `string` | 多值对象成员 | N | `id-01` | 关联对象设备编号 |
| 497 | `roles` | `roles.related[].device.name` | `string` | 多值对象成员 | N | `skyeye-sensor-01` | 关联对象设备名称 |
| 498 | `roles` | `roles.related[].device.type` | `string` | 多值对象成员 | N | `network_sensor` | 关联对象设备类型 |
| 499 | `roles` | `roles.related[].device.vendor` | `string` | 多值对象成员 | N | `qax` | 关联对象设备厂商 |
| 500 | `roles` | `roles.related[].device.model` | `string` | 多值对象成员 | N | `NS-5000` | 关联对象设备型号 |
| 501 | `roles` | `roles.related[].device.serial_number` | `string` | 多值对象成员 | N | `SN202608040001` | 关联对象设备序列号 |
| 502 | `roles` | `roles.related[].device.instance_path` | `string` | 多值对象成员 | N | `instance-path-01` | 关联对象设备实例路径 |
| 503 | `roles` | `roles.related[].device.vendor_id` | `string` | 多值对象成员 | N | `vendor-001` | 关联对象设备厂商编号 |
| 504 | `roles` | `roles.related[].device.product_id` | `string` | 多值对象成员 | N | `product-001` | 关联对象设备产品编号 |

## Profile 边界

`extensions.profiles.endpoint_asset` 由 Profile registry v2 单独管理，
当前包含 19 条路径。它表达终端资产相对 host 的增量快照，不属于 504 条中间版本核心事件路径。

## 使用约束

- 路径包含 `[]` 表示数组对象或数组值；数组内叶子字段按每个成员解释。
- 必填标记依据当前 JSON Schema；事件类型契约可以对特定事件增加条件必填字段。
- 样例仅说明值形态，不构成枚举定义或默认值。
- 逻辑字段是否存在与是否物化为 Doris 标量列是两个独立决策。
