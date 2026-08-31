#!/usr/bin/env python3
"""Generate the Chinese SDM2.0 logical event field catalog."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
OBJECT_REGISTRY = REPO / "log-model/contracts/hybrid-event/object-registry.v1.json"
PROFILE_REGISTRY = REPO / "log-model/contracts/hybrid-event/profile-registry.v1.json"
OUTPUT = ROOT / "docs/main/05-sdm-event-logical-field-catalog.md"
EXCLUDED_PATHS = {
    "metadata.mapping_revision",
    "metadata.projection_version",
    "metadata.quality_status",
}
INTERIM_PATH_OVERRIDES = {}

REQUIRED_PATHS = {
    "metadata.schema_version", "metadata.mapping_id", "metadata.tenant_id",
    "metadata.event_id", "metadata.occur_time", "event.record_kind", "event.domain",
    "event.type",
}

BOOLEAN_FIELDS = {"is_primary", "is_attack_alert", "targeted_attack"}
INTEGER_FIELDS = {
    "schema_version",
    "port", "status_code", "size", "count", "duration", "duration_ms", "length",
    "offset", "hit_count", "attack_bytes", "attack_packets", "port_count",
    "target_count", "interval_ms", "total_bytes", "total_packets", "bytes_in",
    "bytes_out", "packets_in", "packets_out",
}
NUMBER_FIELDS = {"value", "latitude", "longitude"}
DATETIME_FIELDS = {
    "occur_time", "ingest_time", "parse_time", "created_time", "modified_time",
    "published_time", "start_time", "end_time", "observed_time", "install_time",
    "first_seen_time", "last_seen_time", "status_time",
}
ARRAY_FIELDS = {
    "intermediaries", "tactics", "techniques", "recipients", "cc", "ports",
}

SEGMENTS = {
    "metadata": "治理元数据", "event": "事件语义", "roles": "事件角色",
    "facets": "事件维度", "source_finding": "来源检测结果", "extensions": "扩展",
    "source": "发起方", "target": "目标方", "observer": "观察方", "carriers": "行为载体",
    "related": "关联对象", "endpoint": "网络端点", "user": "用户", "account": "账号",
    "host": "主机", "process": "进程", "file": "文件", "service": "服务",
    "resource": "资源", "device": "设备", "product": "产品", "application": "应用",
    "network": "网络", "http": "HTTP", "email": "邮件", "container": "容器",
    "authentication": "认证", "dns": "DNS", "tls": "TLS", "database": "数据库",
    "injection": "进程注入", "target_thread": "目标线程", "key": "注册表键",
    "previous": "变更前", "current": "变更后",
    "geo": "地理位置", "nat": "NAT", "original": "转换前", "translated": "转换后",
    "request": "请求", "response": "响应", "traffic": "流量", "scan": "扫描",
    "rule": "规则", "rules": "规则列表", "category": "分类", "malware": "恶意软件",
    "ioc": "威胁指标", "vulnerability": "漏洞", "evidence": "证据", "attacker": "攻击方",
    "victim": "受害方", "mitre": "MITRE ATT&CK", "entities": "关联实体",
    "indicators": "指标列表", "window": "检测窗口", "metrics": "指标度量",
    "protection": "防护", "threshold": "阈值", "data_source": "数据来源", "log": "日志描述",
    "payload_refs": "载荷引用", "source_private": "来源私有字段", "profiles": "扩展画像",
    "enrichments": "富化结果", "unmapped": "未映射字段", "endpoint_asset": "终端资产画像",
    "group": "分组", "os": "操作系统", "hashes": "哈希", "kubernetes": "Kubernetes",
    "signatures": "签名列表",
    "script": "脚本",
    "subtype": "子类型", "attack": "攻击", "attackers": "攻击方列表", "victims": "受害方列表",
    "affected": "受影响对象列表", "attachments": "附件列表", "auth": "认证", "cdn": "CDN",
    "endpoints": "端点列表", "family": "家族", "match": "匹配", "normalized": "标准化分类",
    "original": "原始分类", "level1": "一级", "level2": "二级", "attention": "关注信息",
    "city": "城市", "country": "国家", "region": "区域", "cluster": "集群", "pod": "Pod",
    "continent": "洲", "coordinates": "经纬度", "organization": "组织", "system": "所属系统",
    "owner": "所有者", "permission": "权限", "rate": "速率", "location": "位置",
    "application": "应用", "browser": "浏览器", "intermediaries": "中间节点",
}

LEAVES = {
    "tenant_id": "租户编号", "occur_time": "事件发生时间", "ingest_time": "接收时间",
    "event_id": "事件编号", "parse_time": "解析时间", "schema_version": "结构版本",
    "mapping_id": "映射编号", "mapping_revision": "映射修订版本",
    "projection_version": "投影版本", "quality_status": "质量状态", "vendor": "厂商",
    "product": "产品", "category": "分类", "instance_id": "实例编号", "type": "类型",
    "level": "级别", "name": "名称", "log_id": "日志编号",
    "original_event_id": "来源原始事件编号", "system": "系统", "third_party_tenant_uuid": "第三方租户 UUID",
    "record_kind": "记录种类", "domain": "领域", "operation": "操作", "outcome": "结果",
    "severity": "严重级别", "message": "事件消息", "ip": "IP 地址", "ipv4": "IPv4 地址",
    "ipv6": "IPv6 地址", "port": "端口", "mac": "MAC 地址", "pid": "进程号",
    "uid": "唯一标识", "guid": "GUID", "cmdline": "命令行", "path": "路径",
    "id": "编号", "ref_id": "事件内引用编号", "entity_type": "实体类型",
    "relation_type": "关系类型", "is_primary": "是否主对象", "full": "完整值",
    "size": "大小", "mime_type": "MIME 类型", "created_time": "创建时间",
    "modified_time": "修改时间", "md5": "MD5", "sha1": "SHA-1", "sha256": "SHA-256",
    "value": "值", "serial_number": "序列号", "address": "地址", "model": "型号",
    "protocol": "协议", "direction": "方向", "session_id": "会话编号", "method": "方法",
    "status_code": "状态码", "headers": "头信息", "query": "查询参数", "referer": "来源页面",
    "user_agent": "用户代理", "recipients": "收件人", "sender": "发件人", "from": "邮件作者",
    "cc": "抄送人", "subject": "主题", "message_id": "邮件编号", "description": "描述",
    "status": "状态", "count": "数量", "behavior": "行为", "killchain": "杀伤链",
    "detection_method": "检测方式", "remediation": "处置建议", "compromise_status": "失陷状态",
    "attack_result": "攻击结果", "action": "动作", "original_id": "来源原始编号",
    "signature_id": "签名编号", "label": "标签", "policy_id": "策略编号",
    "policy_name": "策略名称", "technique_id": "技术编号", "cve": "CVE 编号",
    "confidence": "置信度", "duration": "持续时间", "duration_ms": "持续毫秒数",
    "start_time": "开始时间", "end_time": "结束时间", "ports": "端口列表",
    "port_count": "端口数量", "target_count": "目标数量", "interval_ms": "时间间隔（毫秒）",
    "total_bytes": "总字节数", "total_packets": "总包数", "bytes_in": "入方向字节数",
    "bytes_out": "出方向字节数", "packets_in": "入方向包数", "packets_out": "出方向包数",
    "unit": "单位", "vendor_id": "厂商编号", "product_id": "产品编号",
    "instance_path": "实例路径", "version": "版本", "external_id": "外部编号",
    "code": "代码", "content": "内容", "body": "正文", "addresses": "地址列表",
    "alert": "告警", "bytes": "字节数", "campaign": "攻击活动", "client": "客户端",
    "cnnvd": "CNNVD 编号", "connection_state": "连接状态", "directory": "目录",
    "extension": "扩展名", "failure_reason": "失败原因", "forwarded_for": "转发来源",
    "hash_type": "哈希类型", "hit_count": "命中次数", "impact": "影响",
    "is_attack_alert": "是否攻击告警", "item_id": "规则项编号", "length": "长度",
    "matched_content": "命中内容", "mode": "模式", "namespace": "命名空间",
    "offset": "偏移量", "packets": "包数", "weak_password": "弱密码",
    "platform": "平台", "published_time": "发布时间", "question": "查询问题", "answers": "应答列表",
    "reason": "原因", "result": "结果", "state": "状态", "tactics": "战术列表",
    "targeted_attack": "是否定向攻击", "techniques": "技术列表", "title": "标题",
    "tree_info": "进程树信息", "validity_evidence": "有效性证据", "zone": "区域",
    "working_directory": "工作目录", "integrity": "完整性级别",
    "terminated_time": "结束时间", "original_name": "原始文件名称", "internal_name": "内部名称",
    "company_name": "厂商名称", "signer": "签名主体",
    "latitude": "纬度", "longitude": "经度", "attack_direction": "攻击方向",
    "language": "语言", "command": "命令",
    "arguments": "参数", "module_path": "模块路径", "data": "数据", "renamed_path": "重命名后路径",
}

EXAMPLES = {
    "ip": "198.51.100.23", "ipv4": "198.51.100.23", "ipv6": "2001:db8::23",
    "port": "443", "mac": "00:11:22:33:44:55", "severity": "high", "status_code": "403",
    "record_kind": "finding", "domain": "threat", "operation": "detect", "outcome": "blocked",
    "occur_time": "2026-08-04T10:15:30.123Z", "ingest_time": "2026-08-04T10:15:31.025Z",
    "parse_time": "2026-08-04T10:15:31.118Z", "schema_version": "1",
    "mapping_id": "qax.skyeye.flow_webattack", "event_id": "evt-20260804-000001",
    "log_id": "log-20260804-000001",
    "method": "GET", "protocol": "tcp", "direction": "W2L",
    "sha256": "a3f1...cdef", "md5": "d41d8cd98f00b204e9800998ecf8427e",
    "is_primary": "true", "count": "3", "size": "1024", "pid": "23841",
}

PATH_EXAMPLES = {
    "metadata.data_source.vendor": "qax", "metadata.data_source.product": "skyeye",
    "metadata.data_source.category": "security_device", "metadata.data_source.instance_id": "skyeye-sensor-01",
    "metadata.log.type": "flow_webattack", "metadata.log.level": "high", "metadata.log.name": "Web 攻击日志",
    "event.type": "web_attack", "event.message": "检测到 SQL 注入攻击并已阻断",
    "roles.source.endpoint.device.type": "workstation", "roles.source.geo.city.name": "北京市",
    "roles.source.geo.country.name": "中国", "roles.source.geo.region.name": "北京",
    "roles.source.geo.continent.name": "亚洲", "roles.source.geo.country.code": "CN",
    "roles.source.geo.coordinates.latitude": "39.9042", "roles.source.geo.coordinates.longitude": "116.4074",
    "roles.source.host.os.type": "linux", "roles.source.host.os.name": "Ubuntu",
    "roles.source.host.os.version": "22.04", "roles.target.host.os.name": "Ubuntu Server",
    "roles.source.host.mac": "00:50:56:81:e8:1c",
    "roles.source.process.path": "C:\\Windows\\System32\\svchost.exe",
    "roles.source.process.cmdline": "svchost.exe -k DcomLaunch",
    "roles.target.process.working_directory": "C:\\Windows\\System32\\",
    "roles.target.process.integrity": "System",
    "roles.target.process.terminated_time": "2024-12-18T02:46:43.718Z",
    "roles.target.process.file.hashes.sha1": "356a192b7913b04c54574d18c28d46e6395428ab",
    "roles.target.process.file.original_name": "Wmiprvse.exe",
    "roles.target.process.file.internal_name": "Wmiprvse.exe",
    "roles.source.process.file.original_name": "svchost.exe",
    "roles.source.process.file.internal_name": "svchost.exe",
    "roles.source.process.file.signatures[].signer": "Microsoft Windows Publisher",
    "roles.carriers[].process.created_time": "2024-12-17T20:10:07.744+08:00",
    "roles.carriers[].script.id": "12e821ca-0d5c-409a-8bbf-fa39567d4d70",
    "roles.carriers[].script.language": "powershell",
    "roles.carriers[].script.command": "$global:?",
    "roles.carriers[].script.content": "$Res = 0; Write-Host $Res",
    "roles.related[].process.file.original_name": "GPUpdate.exe",
    "roles.related[].process.file.internal_name": "GPUpdate.exe",
    "roles.related[].process.file.signatures[].signer": "Microsoft Windows",
    "roles.target.process.file.company_name": "Microsoft Corporation",
    "roles.target.process.file.product.name": "Microsoft Windows Operating System",
    "roles.target.process.file.description": "WMI Provider Host",
    "roles.target.process.file.version": "10.0.19041.3636",
    "roles.target.process.file.signatures[].signer": "Microsoft Windows Publisher",
    "roles.target.process.file.signatures[].status": "verified",
    "roles.target.process.user.session_id": "0",
    "roles.target.host.os.type": "linux", "roles.target.host.os.version": "22.04",
    "roles.target.domain.name": "portal.example.com", "roles.target.url.full": "https://portal.example.com/login?id=1%27",
    "roles.related[].domain.name": "cdn.example.com", "roles.related[].url.full": "https://cdn.example.com/app.js",
    "roles.target.geo.city.name": "上海市", "roles.observer.product.name": "天眼",
    "roles.target.geo.continent.name": "亚洲", "roles.target.geo.country.code": "CN",
    "roles.target.geo.country.name": "中国", "roles.target.geo.region.name": "上海",
    "roles.target.geo.coordinates.latitude": "31.2304", "roles.target.geo.coordinates.longitude": "121.4737",
    "roles.source.resource.system.id": "SYS-004", "roles.source.resource.system.name": "财务系统",
    "roles.source.resource.organization.id": "ORG-001", "roles.source.resource.organization.name": "示例集团财务部",
    "roles.target.resource.system.id": "SYS-005", "roles.target.resource.system.name": "审计系统",
    "roles.target.resource.organization.id": "ORG-002", "roles.target.resource.organization.name": "示例集团安全部",
    "roles.observer.device.vendor": "奇安信", "roles.observer.device.type": "network_sensor",
    "roles.observer.type": "security_sensor", "facets.application.name": "HTTPS",
    "facets.http.request.host": "portal.example.com", "facets.http.request.query": "id=1%27",
    "facets.http.request.referer": "https://portal.example.com/", "facets.http.request.user_agent": "Mozilla/5.0",
    "facets.http.request.headers": "Host: portal.example.com", "facets.http.response.headers": "Content-Type: text/html",
    "facets.email.sender": "security@example.com", "facets.email.from": "soc@example.com",
    "facets.email.subject": "安全告警通知", "facets.email.message_id": "<20260804.0001@example.com>",
    "facets.container.kubernetes.namespace": "security-prod", "facets.container.kubernetes.pod.name": "portal-web-7d9f8c6b5-x2k4p",
    "facets.container.kubernetes.cluster.name": "prod-cluster", "facets.container.kubernetes.container.name": "portal-web",
    "facets.dns.question.name": "portal.example.com", "facets.dns.question.type": "A",
    "facets.dns.answers[].address": "23.196.37.171", "facets.dns.response.code": "0",
    "facets.process.injection.method": "remote_thread",
    "facets.process.injection.target_thread.id": "17716",
    "facets.process.injection.target_thread.address": "140701423552944",
    "facets.process.injection.target_thread.arguments": "718250356736",
    "facets.process.injection.target_thread.module_path": "C:\\Windows\\servicing\\TrustedInstaller.exe",
    "facets.registry.key.path": "\\REGISTRY\\MACHINE\\SYSTEM\\ControlSet001\\Services\\wuauserv",
    "facets.registry.key.renamed_path": "\\REGISTRY\\MACHINE\\SYSTEM\\ControlSet001\\Services\\wuauserv-new",
    "facets.registry.value.name": "Start", "facets.registry.value.type": "reg_dword",
    "facets.registry.value.previous.data": "3", "facets.registry.value.previous.size": "4",
    "facets.registry.value.current.data": "2", "facets.registry.value.current.size": "4",
    "facets.authentication.auth_type": "password",
    "facets.authentication.auth_result": "failed", "facets.authentication.auth_failure_reason": "invalid_password",
    "facets.network.application_protocol": "https", "facets.network.connection_state": "established",
    "source_finding.title": "SQL 注入攻击", "source_finding.description": "请求参数命中 SQL 注入检测规则",
    "source_finding.status": "active", "source_finding.behavior": "sql_injection",
    "source_finding.killchain": "initial_access", "source_finding.detection_method": "signature",
    "source_finding.remediation": "阻断来源 IP 并检查目标应用", "source_finding.compromise_status": "not_compromised",
    "source_finding.attack_result": "blocked", "source_finding.action": "block",
    "source_finding.attack_direction": "W2L",
    "source_finding.attacker.geo.continent.name": "北美洲",
    "source_finding.attacker.geo.country.code": "US", "source_finding.attacker.geo.country.name": "美国",
    "source_finding.attacker.geo.region.name": "California", "source_finding.attacker.geo.city.name": "Mountain View",
    "source_finding.attacker.geo.coordinates.latitude": "37.422", "source_finding.attacker.geo.coordinates.longitude": "-122.085",
    "source_finding.victim.geo.continent.name": "北美洲",
    "source_finding.victim.geo.country.code": "US", "source_finding.victim.geo.country.name": "美国",
    "source_finding.victim.geo.region.name": "Ohio", "source_finding.victim.geo.city.name": "Columbus",
    "source_finding.victim.geo.coordinates.latitude": "39.9819", "source_finding.victim.geo.coordinates.longitude": "-82.9048",
    "source_finding.attacker.resource.id": "AST-0008", "source_finding.attacker.resource.name": "攻击源终端-01",
    "source_finding.attacker.resource.type": "terminal", "source_finding.attacker.resource.system.id": "SYS-004",
    "source_finding.attacker.resource.system.name": "财务系统",
    "source_finding.attacker.resource.organization.name": "示例集团财务部",
    "source_finding.victim.resource.id": "AST-0010", "source_finding.victim.resource.name": "日志审计设备",
    "source_finding.victim.resource.type": "security_device", "source_finding.victim.resource.system.id": "SYS-005",
    "source_finding.victim.resource.system.name": "审计系统",
    "source_finding.victim.resource.organization.name": "示例集团安全部",
    "source_finding.original_id": "alert-origin-98765", "source_finding.malware.name": "ChinaChopper",
    "source_finding.malware.type": "webshell", "source_finding.malware.family": "WebShell",
    "source_finding.rule.signature_id": "WEB-SQLI-001", "source_finding.rule.id": "rule-1001",
    "source_finding.rule.label": "SQL 注入", "source_finding.rule.policy_id": "policy-web-01",
    "source_finding.rule.policy_name": "Web 攻击防护策略", "source_finding.rule.status": "enabled",
    "source_finding.rule.version": "2026.08", "source_finding.ioc.value": "198.51.100.23",
    "source_finding.ioc.type": "ipv4", "source_finding.ioc.source": "threat_intelligence",
    "source_finding.ioc.status": "malicious", "source_finding.mitre.technique_id": "T1190",
    "source_finding.mitre.tactics": "[initial-access]", "source_finding.mitre.techniques": "[T1190]",
    "source_finding.vulnerability.cve": "CVE-2024-12345", "source_finding.vulnerability.cnnvd": "CNNVD-202401-1234",
    "source_finding.vulnerability.name": "WebPortal 远程代码执行漏洞",
    "source_finding.vulnerability.type": "remote_code_execution",
    "source_finding.vulnerability.description": "攻击者可通过构造请求执行任意代码",
    "source_finding.vulnerability.impact": "远程代码执行", "source_finding.vulnerability.remediation": "升级至安全版本",
    "facets.network.scan.type": "port_scan", "facets.network.scan.method": "syn",
    "facets.network.scan.ports[]": "[22,80,443]", "facets.network.scan.port_count": "3",
    "facets.network.scan.target_count": "12", "facets.network.scan.interval_ms": "5000",
    "facets.network.traffic.total_bytes": "8192", "facets.network.traffic.total_packets": "24",
    "facets.network.traffic.bytes_in": "2048", "facets.network.traffic.bytes_out": "6144",
    "facets.network.traffic.packets_in": "8", "facets.network.traffic.packets_out": "16",
    "facets.network.traffic.rate.value": "1024", "facets.network.traffic.rate.unit": "bytes_per_second",
    "facets.network.traffic.interval_ms": "1000", "source_finding.window.duration_ms": "300000",
}

PATH_MEANINGS = {
    "facets.registry.key.path": "被操作的注册表键完整路径",
    "facets.registry.key.renamed_path": "注册表键重命名后的完整路径",
    "facets.registry.value.name": "被操作的注册表值名称",
    "facets.registry.value.type": "注册表值的数据类型",
    "facets.registry.value.previous.data": "注册表值变更前的数据",
    "facets.registry.value.previous.size": "注册表值变更前的数据字节数",
    "facets.registry.value.current.data": "注册表值变更后的数据",
    "facets.registry.value.current.size": "注册表值变更后的数据字节数",
    "facets.process.injection.method": "进程注入方式",
    "facets.process.injection.target_thread.id": "被注入目标线程编号",
    "facets.process.injection.target_thread.address": "被注入目标线程入口地址",
    "facets.process.injection.target_thread.arguments": "传递给被注入目标线程的参数",
    "facets.process.injection.target_thread.module_path": "被注入目标线程关联的模块路径",
    "metadata.data_source.vendor": "数据来源厂商", "metadata.data_source.product": "数据来源产品",
    "metadata.data_source.category": "数据来源类别", "metadata.data_source.instance_id": "数据来源实例编号",
    "metadata.log.type": "来源日志类型", "metadata.log.level": "来源日志等级", "metadata.log.name": "来源日志名称",
    "metadata.source.tenant_id": "来源系统租户编号", "metadata.source.system": "来源系统名称",
    "metadata.source.category": "来源系统类别", "metadata.source.vendor": "来源系统厂商",
    "metadata.payload_refs[].http.request_body": "HTTP 请求正文引用",
    "metadata.payload_refs[].http.response_body": "HTTP 响应正文引用",
    "event.domain": "事件所属领域", "event.type": "标准化事件类型",
    "roles.source.host.mac": "来源主机的 MAC 地址",
    "roles.carriers[].process.created_time": "载体进程创建时间",
    "roles.carriers[].script.id": "载体脚本编号",
    "roles.carriers[].script.language": "载体脚本语言",
    "roles.carriers[].script.command": "载体脚本命令或表达式",
    "roles.carriers[].script.content": "载体脚本正文",
    "roles.source.geo.continent.name": "发起方 IP 所在洲名称",
    "roles.source.geo.country.code": "发起方 IP 所在国家或地区的 ISO 3166-1 Alpha-2 代码",
    "roles.source.geo.country.name": "发起方 IP 所在国家或地区名称",
    "roles.source.geo.region.name": "发起方 IP 所在省、州或一级行政区名称",
    "roles.source.geo.city.name": "发起方 IP 所在城市名称",
    "roles.source.geo.coordinates.latitude": "发起方 IP 地理位置纬度",
    "roles.source.geo.coordinates.longitude": "发起方 IP 地理位置经度",
    "roles.target.geo.continent.name": "目标方 IP 所在洲名称",
    "roles.target.geo.country.code": "目标方 IP 所在国家或地区的 ISO 3166-1 Alpha-2 代码",
    "roles.target.geo.country.name": "目标方 IP 所在国家或地区名称",
    "roles.target.geo.region.name": "目标方 IP 所在省、州或一级行政区名称",
    "roles.target.geo.city.name": "目标方 IP 所在城市名称",
    "roles.target.geo.coordinates.latitude": "目标方 IP 地理位置纬度",
    "roles.target.geo.coordinates.longitude": "目标方 IP 地理位置经度",
    "source_finding.attack_direction": "检测产品认定的攻击方到受害方方向",
    "source_finding.attacker.geo.continent.name": "检测主张中攻击方 IP 所在洲名称",
    "source_finding.attacker.geo.country.code": "检测主张中攻击方 IP 所在国家或地区的 ISO 3166-1 Alpha-2 代码",
    "source_finding.attacker.geo.country.name": "检测主张中攻击方 IP 所在国家或地区名称",
    "source_finding.attacker.geo.region.name": "检测主张中攻击方 IP 所在省、州或一级行政区名称",
    "source_finding.attacker.geo.city.name": "检测主张中攻击方 IP 所在城市名称",
    "source_finding.attacker.geo.coordinates.latitude": "检测主张中攻击方 IP 地理位置纬度",
    "source_finding.attacker.geo.coordinates.longitude": "检测主张中攻击方 IP 地理位置经度",
    "source_finding.victim.geo.continent.name": "检测主张中受害方 IP 所在洲名称",
    "source_finding.victim.geo.country.code": "检测主张中受害方 IP 所在国家或地区的 ISO 3166-1 Alpha-2 代码",
    "source_finding.victim.geo.country.name": "检测主张中受害方 IP 所在国家或地区名称",
    "source_finding.victim.geo.region.name": "检测主张中受害方 IP 所在省、州或一级行政区名称",
    "source_finding.victim.geo.city.name": "检测主张中受害方 IP 所在城市名称",
    "source_finding.victim.geo.coordinates.latitude": "检测主张中受害方 IP 地理位置纬度",
    "source_finding.victim.geo.coordinates.longitude": "检测主张中受害方 IP 地理位置经度",
    "source_finding.attacker.resource.id": "检测主张中攻击方资产编号",
    "source_finding.attacker.resource.name": "检测主张中攻击方资产名称",
    "source_finding.attacker.resource.type": "检测主张中攻击方资产类型",
    "source_finding.attacker.resource.system.id": "检测主张中攻击方资产所属业务系统编号",
    "source_finding.attacker.resource.system.name": "检测主张中攻击方资产所属业务系统名称",
    "source_finding.attacker.resource.organization.name": "检测主张中攻击方资产所属组织名称",
    "source_finding.victim.resource.id": "检测主张中受害方资产编号",
    "source_finding.victim.resource.name": "检测主张中受害方资产名称",
    "source_finding.victim.resource.type": "检测主张中受害方资产类型",
    "source_finding.victim.resource.system.id": "检测主张中受害方资产所属业务系统编号",
    "source_finding.victim.resource.system.name": "检测主张中受害方资产所属业务系统名称",
    "source_finding.victim.resource.organization.name": "检测主张中受害方资产所属组织名称",
    "roles.source.resource.system.id": "发起方资产所属业务系统编号",
    "roles.source.resource.system.name": "发起方资产所属业务系统名称",
    "roles.source.resource.organization.id": "发起方资产所属组织编号",
    "roles.source.resource.organization.name": "发起方资产所属组织名称",
    "roles.target.resource.system.id": "目标方资产所属业务系统编号",
    "roles.target.resource.system.name": "目标方资产所属业务系统名称",
    "roles.target.resource.organization.id": "目标方资产所属组织编号",
    "roles.target.resource.organization.name": "目标方资产所属组织名称",
    "roles.target.process.user.session_id": "目标进程运行用户的会话编号",
    "facets.network.protocol": "网络传输协议", "facets.network.protocol.code": "网络协议代码",
    "facets.network.direction": "网络通信方向", "facets.network.session_id": "网络会话编号",
    "facets.network.application_protocol": "应用层协议", "facets.network.connection_state": "网络连接状态",
    "facets.network.intermediaries": "网络中间节点列表", "facets.network.intermediaries[].ip": "网络中间节点 IP 地址",
    "facets.network.zone.name": "网络区域名称",
    "facets.network.scan.type": "网络扫描类型", "facets.network.scan.method": "网络扫描方法",
    "facets.network.scan.ports[]": "扫描端口列表", "facets.network.scan.port_count": "扫描端口数量",
    "facets.network.scan.target_count": "扫描目标数量", "facets.network.scan.interval_ms": "扫描时间间隔（毫秒）",
    "facets.network.traffic.total_bytes": "网络流量总字节数", "facets.network.traffic.total_packets": "网络流量总包数",
    "facets.network.traffic.bytes_in": "入方向流量字节数", "facets.network.traffic.bytes_out": "出方向流量字节数",
    "facets.network.traffic.packets_in": "入方向网络包数", "facets.network.traffic.packets_out": "出方向网络包数",
    "facets.network.traffic.rate.value": "网络流量速率值", "facets.network.traffic.rate.unit": "网络流量速率单位",
    "facets.network.traffic.interval_ms": "网络流量统计间隔（毫秒）",
    "facets.authentication.auth_type": "认证方式", "facets.authentication.auth_result": "认证结果",
    "facets.authentication.auth_failure_reason": "认证失败原因", "facets.authentication.session_id": "认证会话编号",
    "facets.http.request.method": "HTTP 请求方法", "facets.http.request.host": "HTTP 请求主机",
    "facets.http.request.headers": "HTTP 请求头", "facets.http.request.query": "HTTP 请求查询参数",
    "facets.http.request.referer": "HTTP 请求来源页面", "facets.http.request.user_agent": "HTTP 用户代理",
    "facets.http.response.status_code": "HTTP 响应状态码", "facets.http.response.headers": "HTTP 响应头",
    "facets.email.sender": "邮件实际发件人", "facets.email.from": "邮件作者地址",
    "facets.email.recipients[]": "邮件收件人列表", "facets.email.cc": "邮件抄送人列表",
    "facets.email.subject": "邮件主题", "facets.email.message_id": "邮件消息编号",
    "facets.dns.question.name": "DNS 查询域名",
    "facets.dns.question.type": "DNS 查询记录类型",
    "facets.dns.answers[].address": "DNS 应答地址",
    "facets.dns.response.code": "DNS 应答状态代码",
    "source_finding.window.start_time": "检测窗口开始时间", "source_finding.window.end_time": "检测窗口结束时间",
    "source_finding.window.duration_ms": "检测窗口持续时间（毫秒）",
    "source_finding.evidence.match.value": "检测证据匹配值", "source_finding.evidence.match.length": "检测证据匹配长度",
    "source_finding.evidence.match.offset": "检测证据匹配偏移量",
    "source_finding.evidence.http.location.code": "HTTP 检测证据位置代码",
    "source_finding.evidence.http.location.name": "HTTP 检测证据位置名称",
    "source_finding.evidence.http.matched_content": "HTTP 检测证据命中内容",
    "source_finding.threshold.value": "告警触发阈值", "source_finding.threshold.unit": "告警阈值单位",
    "source_finding.vulnerability.id": "漏洞编号", "source_finding.vulnerability.cve": "漏洞 CVE 编号",
    "source_finding.vulnerability.cnnvd": "漏洞 CNNVD 编号", "source_finding.vulnerability.description": "漏洞描述",
    "source_finding.vulnerability.impact": "漏洞影响", "source_finding.vulnerability.name": "漏洞名称",
    "source_finding.vulnerability.remediation": "漏洞修复建议", "source_finding.vulnerability.type": "漏洞类型",
    "source_finding.entities.attackers[].endpoint.ip": "关联攻击方 IP 地址",
    "source_finding.entities.attackers[].ref_id": "关联攻击方引用编号",
    "source_finding.entities.attackers[].entity_type": "关联攻击方实体类型",
    "source_finding.entities.victims[].ref_id": "关联受害方引用编号",
    "source_finding.entities.victims[].entity_type": "关联受害方实体类型",
    "source_finding.entities.affected[].ref_id": "关联受影响对象引用编号",
    "source_finding.entities.affected[].entity_type": "关联受影响对象实体类型",
    "source_finding.indicators[].source": "威胁指标来源",
    "source_finding.malware.family_id": "恶意软件家族编号",
    "roles.related[].user.domain": "关联用户所属域",
    "roles.related[].domain.name": "关联域名",
    "roles.related[].url.full": "关联完整 URL",
}


def clean_segment(segment):
    return segment.replace("[]", "")


def logical_type(path):
    leaf = clean_segment(path.split(".")[-1])
    if path == "facets.network.scan.ports[]":
        base = "integer"
    elif leaf in BOOLEAN_FIELDS:
        base = "boolean"
    elif leaf in INTEGER_FIELDS:
        base = "integer"
    elif leaf in {"latitude", "longitude"}:
        base = "number"
    elif leaf in NUMBER_FIELDS and path.startswith(("facets.network.traffic.rate", "source_finding.threshold")):
        base = "number"
    elif leaf in DATETIME_FIELDS or leaf.endswith("_time"):
        base = "string(datetime)"
    else:
        base = "string"
    if path.endswith("[]") or leaf in ARRAY_FIELDS:
        return f"array<{base}>"
    return base


def cardinality(path):
    if path.endswith("[]"):
        return "多值"
    if "[]" in path:
        return "多值对象成员"
    return "单值"


def meaning(path):
    if path in PATH_MEANINGS:
        return PATH_MEANINGS[path]
    parts = [clean_segment(part) for part in path.split(".")]
    leaf = parts[-1]
    leaf_name = LEAVES.get(leaf, leaf.replace("_", " "))
    if path.startswith("facets.network.nat."):
        qualifiers = {
            "original": "NAT 转换前", "translated": "NAT 转换后",
            "source": "源", "target": "目标",
        }
        context = "".join(qualifiers.get(part, "") for part in parts[3:-1])
        separator = " " if leaf_name.startswith(("IP", "IPv4", "IPv6", "MAC")) else ""
        return f"{context}{separator}{leaf_name}"
    if path.startswith("roles."):
        role_names = {"source": "发起方", "target": "目标方", "observer": "观察方", "carriers": "载体", "related": "关联对象"}
        role = role_names.get(parts[1], "")
        entity = SEGMENTS.get(parts[-2], "")
        if entity and entity not in {role, "哈希", "操作系统", "分组"}:
            return f"{role}{entity}{leaf_name}"
        return f"{role}{leaf_name}"
    if path.startswith("source_finding.entities."):
        entity_group = {"attackers": "关联攻击方实体", "victims": "关联受害方实体", "affected": "关联受影响实体"}.get(parts[2], "关联实体")
        return f"{entity_group}{leaf_name}"
    if path.startswith("source_finding.indicators[]."):
        return f"威胁指标{leaf_name}"
    if path.startswith("source_finding.rules[]."):
        return f"命中规则{leaf_name}"
    if leaf not in {"name", "id", "type", "status", "value", "code", "version", "category"}:
        return leaf_name
    parent = parts[-2] if len(parts) > 1 else ""
    parent_name = SEGMENTS.get(parent, LEAVES.get(parent, parent.replace("_", " ")))
    return f"{parent_name}{leaf_name}"


def example(path):
    leaf = clean_segment(path.split(".")[-1])
    value = PATH_EXAMPLES.get(path) or EXAMPLES.get(leaf)
    if value is None:
        if ".user.name" in path:
            value = "alice"
        elif ".account.name" in path:
            value = "svc_web"
        elif ".host.name" in path:
            value = "web-server-01"
        elif ".process.name" in path:
            value = "curl"
        elif ".process.path" in path:
            value = "/usr/bin/curl"
        elif ".process.cmdline" in path:
            value = "curl https://portal.example.com/login"
        elif ".file.name" in path or ".attachments[].name" in path:
            value = "login.php"
        elif ".file.path" in path:
            value = "/var/www/html/login.php"
        elif ".service.name" in path:
            value = "https"
        elif ".device.name" in path:
            value = "skyeye-sensor-01"
        elif ".device.model" in path:
            value = "NS-5000"
        elif ".device.serial_number" in path:
            value = "SN202608040001"
        elif ".resource.name" in path:
            value = "production-web-service"
        elif ".resource.type" in path:
            value = "cloud_service"
        elif ".resource.subtype" in path:
            value = "web_application"
        elif ".resource.vendor" in path:
            value = "Alibaba Cloud"
        elif ".resource.product" in path:
            value = "ECS"
        elif ".group.name" in path:
            value = "生产环境"
        elif ".os.name" in path:
            value = "Ubuntu"
        elif ".os.type" in path:
            value = "linux"
        elif ".os.version" in path:
            value = "22.04"
        elif leaf in DATETIME_FIELDS or leaf.endswith("_time"):
            value = "2026-08-04T10:15:30.123Z"
        elif leaf == "uid":
            value = "uid-1001"
        elif leaf == "guid":
            value = "7f8a9b10-1234-5678-9abc-def012345678"
        elif leaf == "cmdline":
            value = "curl https://portal.example.com/login"
        elif leaf == "path":
            value = "/var/www/html/login.php"
        elif leaf == "mime_type":
            value = "text/x-php"
        elif leaf == "sha1":
            value = "356a192b7913b04c54574d18c28d46e6395428ab"
        elif leaf == "full":
            value = "https://portal.example.com/login"
        elif leaf == "entity_type":
            value = "host"
        elif leaf == "relation_type":
            value = "communicates_with"
        elif leaf == "ref_id":
            value = "host_target_01"
        elif leaf == "type":
            value = "network_sensor"
        elif leaf == "status":
            value = "active"
        elif leaf == "category":
            value = "web_attack"
        elif leaf == "level":
            value = "high"
        elif leaf == "vendor":
            value = "qax"
        elif leaf == "product":
            value = "skyeye"
        elif leaf == "name":
            value = "portal-web"
        elif leaf.endswith("_id"):
            value = f"{leaf[:-3]}-001"
        elif leaf.endswith("_name"):
            value = f"{leaf[:-5]}-name-01"
        elif leaf.endswith("_code") or leaf == "code":
            value = "CODE-01"
        elif logical_type(path) == "boolean":
            value = "true"
        elif logical_type(path) in {"integer", "number"}:
            value = "1"
        else:
            value = f"{leaf.replace('_', '-')}-01"
    if logical_type(path).startswith("array<") and not value.startswith("["):
        return f"[{value}]"
    return value


def main():
    registry = json.loads(OBJECT_REGISTRY.read_text(encoding="utf-8"))
    profile_registry = json.loads(PROFILE_REGISTRY.read_text(encoding="utf-8"))
    paths = [
        INTERIM_PATH_OVERRIDES.get(path, path)
        for path in registry["logical_paths"]
        if path not in EXCLUDED_PATHS
    ]
    if len(paths) != 504:
        raise ValueError(f"Expected 504 interim logical paths, found {len(paths)}")
    counts = {}
    for path in paths:
        layer = path.split(".")[0]
        counts[layer] = counts.get(layer, 0) + 1

    lines = [
        "# SDM2.0 事件逻辑字段清单", "",
        f"> 权威来源：`object-registry.v1.json` registry v{registry['registry_version']}。",
        f"> 本清单包含当前中间版本采用的 {len(paths)} 条核心逻辑叶子路径，不是 Doris 物理列清单。",
        "> 2026-08-28 移除 `mapping_revision`、`projection_version`、`quality_status` 三个治理字段：物理表 007、Routine Load 026、Kafka 消息均不再包含。",
        "> 已删减的 13 个低频标量投影仍保留其逻辑路径，由 `roles_obj` 或 `facets_obj` 权威存储。",
        "> 2026-08-26 修订：原始日志已分离至独立 `raw_log` 表（event_id 1:1 关联），取消 `metadata.raw_log_id` → `metadata.raw_msg` 的临时替换，恢复标准注册表路径 `metadata.raw_log_id`。",
        "> 2026-08-26 修订：删除 `metadata.raw_log_id`——其值恒等于 `event_id` 属冗余列，事件↔raw_log 关联统一用 `event_id`，来源日志身份用 `log_id`。",
        "> 2026-08-26 修订：删除 `metadata.original_event_id`——来源稳定 ID 写入 `log_id`，否则 `log_id` 与 `event_id` 相同。",
        f"> `extensions.profiles.endpoint_asset` 的 {len(profile_registry['profiles']['endpoint_asset']['logical_paths'])} 条 Profile 路径单独治理，不计入本清单。", "",
        "## 分层统计", "",
        "| 层 | 字段数 | 职责 |", "|---|---:|---|",
        f"| `metadata` | {counts.get('metadata', 0)} | 接入来源、时间、标识和治理信息 |",
        f"| `event` | {counts.get('event', 0)} | 事件种类、领域、行为、结果和严重度 |",
        f"| `roles` | {counts.get('roles', 0)} | 发起方、目标方、观察方、载体和关联对象 |",
        f"| `facets` | {counts.get('facets', 0)} | 网络、HTTP、邮件、认证、容器等事件维度 |",
        f"| `source_finding` | {counts.get('source_finding', 0)} | 来源设备自身的检测或告警判断 |", "",
        "## 核心逻辑字段", "",
        "| 序号 | 所在层 | 逻辑路径 | 逻辑类型 | 基数 | 必填 | 样例 | 字段含义 |",
        "|---:|---|---|---|---|---|---|---|",
    ]
    for index, path in enumerate(paths, 1):
        layer = path.split(".")[0]
        required = "Y" if path in REQUIRED_PATHS else "N"
        lines.append(
            f"| {index} | `{layer}` | `{path}` | `{logical_type(path)}` | {cardinality(path)} | "
            f"{required} | `{example(path)}` | {meaning(path)} |"
        )
    profile = profile_registry["profiles"]["endpoint_asset"]
    lines.extend([
        "", "## Profile 边界", "",
        f"`{profile['logical_path']}` 由 Profile registry v{profile_registry['registry_version']} 单独管理，",
        f"当前包含 {len(profile['logical_paths'])} 条路径。它表达终端资产相对 host 的增量快照，不属于 {len(paths)} 条中间版本核心事件路径。", "",
        "## 使用约束", "",
        "- 路径包含 `[]` 表示数组对象或数组值；数组内叶子字段按每个成员解释。",
        "- 必填标记依据当前 JSON Schema；事件类型契约可以对特定事件增加条件必填字段。",
        "- 样例仅说明值形态，不构成枚举定义或默认值。",
        "- 逻辑字段是否存在与是否物化为 Doris 标量列是两个独立决策。", "",
    ])
    OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUTPUT} with {len(paths)} interim logical paths")


if __name__ == "__main__":
    main()
