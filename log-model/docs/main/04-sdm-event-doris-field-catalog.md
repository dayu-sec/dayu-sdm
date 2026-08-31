# sdm_event Doris 字段清单

> **已退役 2026-08-26**：本清单是 `metadata.raw_msg` 临时契约（原文直装 sdm_event 列）时期的 55 列物理目录，
> 由 `scripts/generate_sdm_event_assets.py` 生成；该生成器与 `schema/007_sdm_event.sql` DDL 已同日删除。
> 当前契约：原始日志分离到独立 `raw_log` 表（`schema/006_raw_log.sql`，event_id 1:1），`sdm_event` 仅存
> `metadata.raw_log_id` 引用；权威字段清单见 `docs/main/05-sdm-event-logical-field-catalog.md` 与
> `contracts/hybrid-event/projection-registry.v1.json`。以下内容仅作历史对照，不再维护。

> 本清单依据 `log-model/contracts/hybrid-event/projection-registry.v1.json` 生成。
> `sdm_event` 保存五层逻辑事件：51 个核心标量投影列 + 4 个 VARIANT 完整对象列。
> `log_id` 是日志唯一标识，告警表的 `log_id_list` 通过该字段回查日志。

> 当前中间版本使用 `raw_msg` 直接保存源日志数据；原始日志独立存储及引用字段后期再分离。

| 序号 | 字段名称 | Doris 类型 | 逻辑路径 | 样例 | 字段说明 |
|---:|---|---|---|---|---|
| 1 | `tenant_id` | `VARCHAR(128)` | `metadata.tenant_id` | `tenant01` | 租户编号：事件所属租户或空间。 |
| 2 | `occur_time` | `DATETIME(3)` | `metadata.occur_time` | `2026-08-04 10:15:30.123` | 事件发生时间：标准化事件发生时间，作为分区和主键组成。 |
| 3 | `event_id` | `VARCHAR(128)` | `metadata.event_id` | `evt-20260804-000001` | 事件编号：标准化事件的唯一标识。 |
| 4 | `ingest_time` | `DATETIME(3)` | `metadata.ingest_time` | `2026-08-04 10:15:31.025` | 接收时间：平台接收原始日志的时间。 |
| 5 | `parse_time` | `DATETIME(3)` | `metadata.parse_time` | `2026-08-04 10:15:31.118` | 解析时间：解析和标准化完成的时间。 |
| 6 | `schema_version` | `INT` | `metadata.schema_version` | `1` | 逻辑模型版本：五层逻辑事件模型版本。 |
| 7 | `mapping_id` | `VARCHAR(128)` | `metadata.mapping_id` | `qax.skyeye.flow_webattack` | 映射编号：产生日志标准化结果的映射契约编号。 |
| 8 | `data_src_vendor` | `VARCHAR(128)` | `metadata.data_source.vendor` | `qax` | 来源厂商：产生日志的厂商。 |
| 9 | `data_src_product` | `VARCHAR(128)` | `metadata.data_source.product` | `skyeye` | 来源产品：产生日志的产品或设备产品线。 |
| 10 | `data_src_category` | `VARCHAR(128)` | `metadata.data_source.category` | `web_attack` | 来源日志类别：来源日志的类别。 |
| 11 | `data_src_instance_id` | `VARCHAR(128)` | `metadata.data_source.instance_id` | `skyeye-sensor-01` | 来源实例编号：采集点或来源实例编号。 |
| 12 | `log_type` | `VARCHAR(128)` | `metadata.log.type` | `flow_webattack` | 日志类型：来源日志类型或子类型。 |
| 13 | `log_level` | `VARCHAR(64)` | `metadata.log.level` | `high` | 日志等级：来源日志等级。 |
| 14 | `log_name` | `VARCHAR(255)` | `metadata.log.name` | `Web 攻击日志` | 日志名称：来源日志名称。 |
| 15 | `log_id` | `VARCHAR(128)` | `metadata.log_id` | `log-20260804-000001` | 日志编号：原始安全日志的稳定唯一标识，供告警回查。 |
| 16 | `raw_msg` | `STRING` | `metadata.raw_msg` | `{"event_type":"web_attack","src_ip":"198.51.100.23"}` | 原始日志：当前阶段直接装载源日志数据；后期建设独立原始日志存储后再分离。 |
| 17 | `source_original_event_id` | `VARCHAR(128)` | `metadata.original_event_id` | `source-event-98765` | 来源原始事件编号：来源系统保留的原始事件编号。 |
| 18 | `record_kind` | `VARCHAR(32)` | `event.record_kind` | `finding` | 记录种类：事件记录种类，如 activity、finding、inventory。 |
| 19 | `event_domain` | `VARCHAR(64)` | `event.domain` | `network` | 事件领域：事件所属的粗粒度业务领域。 |
| 20 | `event_type` | `VARCHAR(128)` | `event.type` | `web_attack` | 事件类型：事件的标准化行为类型。 |
| 21 | `operation` | `VARCHAR(64)` | `event.operation` | `exploit` | 操作：事件执行的通用动作。 |
| 22 | `outcome` | `VARCHAR(64)` | `event.outcome` | `blocked` | 结果：操作或事件的结果。 |
| 23 | `severity` | `VARCHAR(64)` | `event.severity` | `high` | 严重级别：标准化事件严重级别。 |
| 24 | `log_content` | `VARCHAR(4096)` | `event.message` | `检测到 SQL 注入攻击并已阻断` | 事件消息：事件消息或有界摘要。 |
| 25 | `source_ip` | `VARCHAR(64)` | `roles.source.endpoint.ip` | `198.51.100.23` | 源 IP：发起方网络端点 IP 地址。 |
| 26 | `source_port` | `INT` | `roles.source.endpoint.port` | `52314` | 源端口：发起方网络端口。 |
| 27 | `source_user` | `VARCHAR(255)` | `roles.source.user.name` | `attacker` | 源用户：发起方用户名称。 |
| 28 | `source_host` | `VARCHAR(255)` | `roles.source.host.name` | `external-host` | 源主机：发起方主机名称。 |
| 29 | `carrier_process_name` | `VARCHAR(255)` | `roles.carriers[].process.name` | `curl` | 载体进程名称：行为链主载体进程名称。 |
| 30 | `carrier_process_guid` | `VARCHAR(128)` | `roles.carriers[].process.uid` | `proc-7f8a9b10` | 载体进程 GUID：行为链主载体进程唯一标识。 |
| 31 | `carrier_process_pid` | `VARCHAR(64)` | `roles.carriers[].process.pid` | `23841` | 载体进程 PID：行为链主载体进程号。 |
| 32 | `target_ip` | `VARCHAR(64)` | `roles.target.endpoint.ip` | `203.0.113.58` | 目标 IP：目标网络端点 IP 地址。 |
| 33 | `target_port` | `INT` | `roles.target.endpoint.port` | `443` | 目标端口：目标网络端口。 |
| 34 | `target_user` | `VARCHAR(255)` | `roles.target.user.name` | `www-data` | 目标用户：目标用户名称。 |
| 35 | `target_host` | `VARCHAR(255)` | `roles.target.host.name` | `web-server-01` | 目标主机：目标主机名称。 |
| 36 | `target_domain` | `VARCHAR(255)` | `roles.target.domain.name` | `portal.example.com` | 目标域名：目标域名，按域名规范化规则投影。 |
| 37 | `target_file_path` | `VARCHAR(4096)` | `roles.target.file.path` | `/var/www/html/login.php` | 目标文件路径：目标文件完整路径。 |
| 38 | `target_file_sha256` | `VARCHAR(128)` | `roles.target.file.hashes.sha256` | `a3f1c2d4e5f678901234567890abcdef1234567890abcdef1234567890abcdef` | 目标文件 SHA-256：目标文件 SHA-256 哈希。 |
| 39 | `observer_product` | `VARCHAR(128)` | `roles.observer.product.name` | `天眼` | 观察者产品：采集或观察产品名称。 |
| 40 | `observer_vendor` | `VARCHAR(128)` | `roles.observer.device.vendor` | `奇安信` | 观察者厂商：采集设备厂商。 |
| 41 | `device_ip` | `VARCHAR(64)` | `roles.observer.device.ip_addresses[].address` | `203.0.113.61` | 设备 IP：采集设备主地址的 IP。 |
| 42 | `network_protocol` | `VARCHAR(64)` | `facets.network.protocol` | `tcp` | 网络协议：网络通信协议。 |
| 43 | `network_session_id` | `VARCHAR(128)` | `facets.network.session_id` | `session-20260804-000123` | 网络会话编号：网络会话唯一标识。 |
| 44 | `k8s_namespace` | `VARCHAR(128)` | `facets.container.kubernetes.namespace` | `security-prod` | Kubernetes 命名空间：容器所属 Kubernetes 命名空间。 |
| 45 | `k8s_pod_name` | `VARCHAR(255)` | `facets.container.kubernetes.pod.name` | `portal-web-7d9f8c6b5-x2k4p` | Kubernetes Pod 名称：容器 Pod 名称。 |
| 46 | `source_finding_title` | `VARCHAR(1024)` | `source_finding.title` | `SQL 注入攻击` | 来源检测标题：来源设备或规则产生的检测标题。 |
| 47 | `source_finding_severity` | `VARCHAR(64)` | `source_finding.severity` | `高危` | 来源检测严重级别：来源检测结果的原始严重级别。 |
| 48 | `source_finding_category` | `VARCHAR(128)` | `source_finding.category` | `Web 攻击` | 来源检测分类：来源检测结果的分类。 |
| 49 | `source_finding_signature_id` | `VARCHAR(128)` | `source_finding.rule.signature_id` | `WEB-SQLI-001` | 来源检测签名编号：触发来源检测的规则或签名编号。 |
| 50 | `source_finding_action` | `VARCHAR(128)` | `source_finding.action` | `block` | 来源检测动作：来源检测结果关联的处置动作。 |
| 51 | `source_finding_original_id` | `VARCHAR(128)` | `source_finding.original_id` | `alert-origin-98765` | 来源检测原始编号：来源检测系统中的原始编号。 |
| 52 | `roles_obj` | `VARIANT` | `roles` | `{"source":{"endpoint":{"ip":"198.51.100.23"}},"target":{"endpoint":{"ip":"203.0.113.58"}}}` | roles 完整逻辑对象，保存未投影的多值和详细字段。 |
| 53 | `facets_obj` | `VARIANT` | `facets` | `{"network":{"protocol":"tcp"},"http":{"request":{"method":"GET"}}}` | facets 完整逻辑对象，保存未投影的多值和详细字段。 |
| 54 | `source_finding_obj` | `VARIANT` | `source_finding` | `{"title":"SQL 注入攻击","severity":"高危","action":"block"}` | source_finding 完整逻辑对象，保存未投影的多值和详细字段。 |
| 55 | `extensions_obj` | `VARIANT` | `extensions` | `{"schema_version":1,"source_private":{"qax":{"skyeye":{}}}}` | extensions 完整逻辑对象，保存未投影的多值和详细字段。 |

## 物理边界

- 标量列是查询加速投影，不替代五层逻辑对象。
- `roles_obj`、`facets_obj`、`source_finding_obj`、`extensions_obj` 是逻辑对象权威存储。
- `roles_obj`、`facets_obj` 和 `source_finding_obj` 使用 V3 倒排索引承接低频标量路径过滤；`extensions_obj` 不建立全路径索引。
- legacy alias 只读，不作为日志写入字段。
- 事件唯一键为 `tenant_id + occur_time + event_id`，按 `occur_time` 日分区。
