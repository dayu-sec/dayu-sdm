#!/usr/bin/env python3
"""Patch/generate metadata-service backup JSON (MetadataBackupDTO v1.0.0).

Reads a POC `metadata-backup-*.json` and aligns it to the four-layer
import contract (logical standard + physical DAM/shape + binds).
Does NOT invent a full catalog from scratch.

  --fix-operators     align type.supported_operators with t_operator.code
  --upsert-behavior   refresh sdm2_log_sdm_event_behavior logical fields
                      (07 + object-fields) and 031 physical DAM (39 columns,
                      6 VARIANT shapes); drop frozen sdm_event hybrid

Write path always: drop unbound leftover infos on raw_log,
drop t_physical_column (scanned_at 不是 *_time，JDBC 绑不上 timestamptz).

Usage:
  python3 log-model/scripts/generate_metadata_backup.py \\
    --baseline draft/metadata-backup-20260914-073225.json \\
    --out draft/metadata-backup-20260914-behavior.json \\
    --fix-operators --upsert-behavior
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DDL_031 = ROOT / "log-model" / "schema" / "031_sdm_event_behavior.sql"

# MetadataPersistenceService.TABLE_ORDER — import clears then inserts these.
TABLE_ORDER = [
    "t_operator",
    "t_data_business_type_base",
    "t_data_business_type_platform",
    "t_definitive_standard",
    "t_definitive_standard_content",
    "t_data_standard",
    "t_data_standard_info",
    "t_data_standard_version",
    "t_business_type_category",
    "t_business_type",
    "t_data_standard_business_type_mapping",
    "t_dam_meta",
    "t_dam_column_shape",
    "t_physical_column",
    "t_topic_table",
]

HYBRID_TOPIC_CODES = ("sdm2_log_raw_log",)
SYNTHETIC_DAM_TABLES = ()
VARIANT_COLUMNS = (
    "subject_detail", "object_detail", "carriers",
    "facets", "observation_detail", "extensions",
)
LEGACY_EVENT_DICTS = (
    "SDM_EVENT_TYPE", "SDM_EVENT_OPERATION", "SDM_EVENT_DOMAIN",
    "SDM_FINDING_ACTION", "SDM_FINDING_SEVERITY", "SDM_FINDING_CATEGORY",
)


BACKUP_VERSION = "1.0.0"
ID_NS = 2_706_030_000_000_000_000  # reserved; below POC 2606030… / 2095… ranges

OPERATOR_ALIASES = {
    "NOT_CONTAINS": "NOT CONTAINS",
    "NOT_BETWEEN": "NOT BETWEEN",
    "STARTS_WITH": "STARTS WITH",
    "ENDS_WITH": "ENDS WITH",
    "IS_NULL": "IS NULL",
    "IS_NOT_NULL": "IS NOT NULL",
    "NEQ": "NE",  # only used when rewriting type JSON if NE exists
}

OBJECT_FIELDS = ROOT / "log-model" / "contracts" / "hybrid-event" / "object-fields.v1.json"

# 字段目录 2.8 ∪ 12 张行为卡实测 facet；name 带 [] 表示数组。
TYPICAL_FACETS = [
    ("facets.network.connection_result", "连接结果", "协议层连接结果；不是 behavior.outcome"),
    ("facets.network.protocol", "网络协议", "网络协议"),
    ("facets.network.direction", "网络方向", "网络方向"),
    ("facets.network.packet_metadata", "包级元数据", "从报文解析出的包级元数据；不承载完整原始报文"),
    ("facets.network.session_id", "网络会话", "网络领域会话属性"),
    ("facets.network.src_ip", "源 IP", "网络侧面源地址；身份仍以角色对象为准"),
    ("facets.network.src_port", "源端口", "网络侧面源端口"),
    ("facets.process.ancestry[].ref_id", "祖先引用", "创建链进程引用"),
    ("facets.process.ancestry[].entity_type", "祖先类型", "创建链实体类型"),
    ("facets.process.ancestry[].name", "祖先进程名", "创建链进程名"),
    ("facets.process.ancestry[].path", "祖先路径", "创建链进程路径"),
    ("facets.process.ancestry[].pid", "祖先 PID", "创建链进程 ID"),
    ("facets.process.ancestry[].command_line", "祖先命令行", "创建链命令行"),
    ("facets.process.injection.method", "注入方法", "进程注入手法"),
    ("facets.process.injection.target_thread.id", "目标线程", "注入目标线程 ID"),
    ("facets.process.injection.target_thread.address", "目标线程地址", "注入目标线程地址"),
    ("facets.process.injection.target_thread.arguments", "目标线程参数", "注入目标线程参数"),
    ("facets.process.injection.target_thread.module_path", "目标模块路径", "注入目标模块路径"),
    ("facets.authorization.approvers[].ref_id", "审批人引用", "授权链审批人"),
    ("facets.dns.answers[]", "DNS 应答", "DNS 应答和别名"),
    ("facets.dns.answers[].address", "DNS 应答地址", "DNS 应答地址"),
    ("facets.dns.question.name", "DNS 查询名", "DNS 查询名"),
    ("facets.dns.question.type", "DNS 查询类型", "DNS 查询类型"),
    ("facets.dns.response.code", "DNS 响应码", "DNS 响应码"),
    ("facets.dns.header.opcode", "DNS 操作码", "DNS header opcode"),
    ("facets.dns.header.authoritative", "DNS AA", "权威应答标志"),
    ("facets.dns.header.truncated", "DNS TC", "截断标志"),
    ("facets.dns.header.recursion_desired", "DNS RD", "期望递归标志"),
    ("facets.ics.function_code", "工控功能码", "ICS 功能码；协议名走 network.application_protocol"),
    ("facets.ics.function_name", "工控功能名", "ICS 功能码可读名"),
    ("facets.ics.address", "工控地址", "线圈/寄存器/数据块地址"),
    ("facets.http.request.method", "HTTP 方法", "HTTP 请求方法"),
    ("facets.http.request.host", "HTTP 主机", "HTTP Host"),
    ("facets.http.request.path", "HTTP 路径", "HTTP 请求路径"),
    ("facets.http.request.referer", "HTTP Referer", "HTTP Referer"),
    ("facets.http.request.user_agent", "User-Agent", "HTTP User-Agent"),
    ("facets.http.response.status_code", "HTTP 状态码", "HTTP 响应状态码"),
    ("facets.email.recipients[]", "邮件收件人", "邮件收件人"),
    ("facets.email.attachments[]", "邮件附件", "邮件附件"),
    ("facets.registry.key.path", "注册表键路径", "注册表键路径"),
    ("facets.registry.value.name", "注册表值名", "注册表值名"),
    ("facets.registry.value.current.data", "注册表当前值", "注册表当前数据"),
]

# 07 信封叶子（不展开 entity_ref 的 typed 对象；那些走 object-fields）。
ENVELOPE_LEAVES = [
    ("meta.schema_version", "契约版本", "逻辑契约版本"),
    ("meta.tenant_id", "租户", "租户标识"),
    ("meta.event_id", "事件编号", "行为事件唯一标识"),
    ("meta.occur_time", "发生时间", "行为事实发生时间"),
    ("meta.ingest_time", "接入时间", "平台接收时间"),
    ("meta.parse_time", "解析时间", "解析完成时间"),
    ("meta.mapping_id", "映射身份", "不可变映射身份；语义变化必须创建新值"),
    ("meta.data_source.vendor", "来源厂商", "来源厂商"),
    ("meta.data_source.product", "来源产品", "来源产品"),
    ("meta.data_source.category", "来源类别", "来源分类"),
    ("meta.data_source.instance_id", "采集实例", "接入实例标识；仅采集器/连接器，不表示观察者"),
    ("meta.source_record.log_id", "来源日志编号", "来源日志编号"),
    ("meta.source_record.record_kind", "记录种类", "来源记录分类或兼容路由值"),
    ("meta.source_record.log_type", "日志类型", "来源日志类型"),
    ("meta.source_record.log_level", "原始日志等级", "原始日志等级；不等同于观察断言严重度"),
    ("meta.source_record.log_name", "日志名称", "来源日志名称"),
    ("meta.source_record.raw_ref", "原文引用", "原始日志回查引用"),
    ("event_kind", "事件种类", "当前唯一实现值 behavior"),
    ("behavior.layer", "行为层次", "行为观测层次"),
    ("behavior.type", "行为类型", "五类闭集：appear/read/change/disappear/flow"),
    ("behavior.operation", "行为动作", "具体动作，如 login、query、write、connect"),
    ("behavior.outcome", "行为结果", "allowed/denied=处置；success/failed=执行；observed=记录；unknown=无结果"),
    ("behavior.message", "行为描述", "行为事实描述消息"),
    ("subject.ref_id", "主体引用", "主体实体引用"),
    ("subject.entity_type", "主体类型", "主体实体类型"),
    ("object.ref_id", "客体引用", "客体实体引用"),
    ("object.entity_type", "客体类型", "客体实体类型"),
    ("carriers[].ref_id", "载体引用", "载体实体引用（数组）"),
    ("carriers[].entity_type", "载体类型", "载体实体类型（数组）"),
    ("carriers[].carrier_role", "载体角色", "载体在事件中的角色（数组）"),
    ("observation.observation_id", "观察编号", "观察记录 ID"),
    ("observation.observer.ref_id", "观察者引用", "观察者引用；身份未知时为 null"),
    ("observation.observer.entity_type", "观察者类型", "观察者实体类型；身份未知时为 null"),
    ("observation.action", "观察动作", "record/detect/assess"),
    ("observation.evidence_refs[]", "证据引用", "指向事实事件、原始日志或证据对象的引用（数组）"),
    ("observation.assertion.attack_direction", "攻击方向", "攻击者到受害者相对租户网络边界的方向：L2L/L2W/W2L/W2W/unknown；来源断言，不复制通信方向"),
    ("observation.assertion.title", "断言标题", "检测标题"),
    ("observation.assertion.severity", "检测严重度", "检测严重度；与 source_record.log_level 分轨"),
    ("observation.assertion.confidence", "置信度", "置信度；按来源契约保留，不强制 0-100"),
    ("observation.assertion.category", "检测分类", "来源检测分类名"),
    ("observation.assertion.category_code", "检测分类码", "来源检测分类码"),
    ("observation.assertion.rule", "断言规则", "规则/特征 ID"),
    ("observation.assertion.conclusion", "断言结论", "来源处置结论"),
    ("observation.assertion.mitre", "ATT&CK", "ATT&CK 战术/技术；子字段 tactic/technique/technique_id"),
    ("observation.assertion.vulnerability", "漏洞", "漏洞（CVE 等）"),
    ("observation.assertion.malware", "恶意软件", "恶意软件家族/名称"),
    ("observation.assertion.attacker[].ref_id", "攻击者引用", "断言攻击者引用；不覆盖 subject"),
    ("observation.assertion.attacker[].entity_type", "攻击者类型", "断言攻击者类型"),
    ("observation.assertion.victim[].ref_id", "受害者引用", "断言受害者引用；不覆盖 object"),
    ("observation.assertion.victim[].entity_type", "受害者类型", "断言受害者类型"),
    ("observation.assertion.affected[].ref_id", "受影响引用", "断言受影响对象引用"),
    ("observation.assertion.affected[].entity_type", "受影响类型", "断言受影响对象类型"),
    ("extensions.source_private", "来源私有", "来源私有字段；不含诊断信息"),
    ("extensions.profiles", "画像", "画像或平台上下文"),
    ("extensions.enrichments", "富化", "富化结果"),
]

REQUIRED_PATHS = {
    "meta.schema_version", "meta.tenant_id", "meta.event_id", "meta.occur_time",
    "meta.mapping_id", "event_kind", "behavior.layer",
    "observation.observation_id", "observation.action", "observation.evidence_refs[]",
}
PK_PATHS = {"meta.tenant_id", "meta.occur_time", "meta.event_id"}
DEFAULT_PATHS = {
    "meta.occur_time", "meta.event_id", "meta.tenant_id", "meta.mapping_id",
    "meta.data_source.vendor", "behavior.type", "behavior.outcome",
    "subject.ref_id", "object.ref_id", "observation.assertion.title",
}
SLOT_CNAME = {
    "subject": "主体",
    "object": "客体",
    "carriers": "载体",
    "observation.observer": "观察者",
}
LEAF_CNAME = {
    "continent_name": "大洲名称",
    "country_code": "国家或地区代码",
    "name": "名",
    "uid": "标识",
    "domain": "域",
    "ip": "IP",
    "mac": "MAC",
    "port": "端口",
    "pid": "PID",
    "guid": "GUID",
    "command_line": "命令行",
    "path": "路径",
    "size": "大小",
    "md5": "MD5",
    "sha1": "SHA1",
    "sha256": "SHA256",
    "full": "URL",
    "query": "查询串",
    "vendor": "厂商",
    "model": "型号",
    "serial_number": "序列号",
    "kind": "种类",
    "version": "版本",
    "provider": "厂商",
    "account": "账号",
    "region": "区域",
    "id": "ID",
    "image": "镜像",
    "namespace": "命名空间",
    "serial": "序列号",
    "subject": "主体",
    "issuer": "颁发者",
    "not_after": "过期时间",
    "interpreter": "解释器",
    "type": "类型",
    "os": "操作系统",
    "hashes": "哈希",
    "user": "用户",
    "file": "文件",
    "data": "数据",
}


def path_code(path: str) -> str:
    return "sdm_event_behavior__" + path.replace("[]", "").replace(".", "_")


def path_leaf(path: str) -> str:
    return path.replace("[]", "").rsplit(".", 1)[-1]


def infer_base(path: str) -> str:
    leaf = path_leaf(path)
    if leaf in ("occur_time", "ingest_time", "parse_time", "not_after"):
        return "Datetime"
    if leaf in ("port", "pid", "size", "status", "status_code") or leaf.endswith("_port"):
        return "Int"
    if leaf in ("message", "command_line", "query", "full", "user_agent", "arguments"):
        return "Text"
    if leaf in (
        "source_private", "profiles", "enrichments", "packet_metadata",
        "mitre",
    ) or path in (
        "facets.dns.answers[]", "facets.email.recipients[]", "facets.email.attachments[]",
        "observation.evidence_refs[]",
    ):
        return "JSON"
    return "String"


def path_tags(path: str) -> list[str]:
    tags: list[str] = []
    if path.startswith("subject."):
        tags += ["SUBJECT", "SOURCE"]
    elif path.startswith("object."):
        tags += ["OBJECT", "TARGET"]
    elif path.startswith("observation.observer"):
        tags += ["OBSERVER"]
    elif path.startswith("observation.assertion"):
        tags += ["FINDING"]
    elif path.startswith("behavior."):
        tags += ["EVENT"]
    elif path.startswith("meta.data_source") or path.startswith("meta.source_record"):
        tags += ["LOG_SOURCE"]
    elif path.startswith("facets.network"):
        tags += ["NETWORK"]
    elif path.startswith("extensions."):
        tags += ["EXTENSION"]
    if ".process." in path or path.startswith("carriers[].process.") or "ancestry" in path:
        tags += ["PROCESS"]
    leaf = path_leaf(path)
    if leaf in ("occur_time", "ingest_time", "parse_time"):
        tags += ["TIME", "TIME_RANGE", "SORT"]
    if leaf == "tenant_id":
        tags += ["TENANT", "HEADER"]
    if leaf in ("event_id", "ref_id", "entity_type", "mapping_id", "log_id", "outcome", "type", "layer", "carrier_role"):
        tags += ["EXACT"]
    if leaf == "ip" or leaf.endswith("_ip"):
        tags += ["IP"]
    if ".user." in path or path.endswith(".user") or ".account." in path:
        tags += ["USER"]
    if infer_base(path) != "JSON":
        tags += ["SEARCHABLE"]
        if leaf in ("name", "path", "title", "message", "product", "log_name"):
            tags += ["FUZZY"]
    seen: set[str] = set()
    out: list[str] = []
    for t in tags:
        if t not in seen:
            seen.add(t)
            out.append(t)
    return out or ["SEARCHABLE"]


def logical_fields() -> list[dict]:
    """07 信封叶子 + object-fields 按槽位展开 + 字段目录/样例 facet。"""
    rows: list[dict] = []
    seen: set[str] = set()

    def add(path: str, cname: str, description: str) -> None:
        if path in seen:
            return
        seen.add(path)
        base = infer_base(path)
        rows.append({
            "path": path,
            "cname": cname,
            "description": description,
            "base": base,
            "tags": path_tags(path),
            "nullable": path not in REQUIRED_PATHS,
            "pri_key": path in PK_PATHS,
            "time_field": path_leaf(path) in ("occur_time", "ingest_time", "parse_time"),
            "default_column": path in DEFAULT_PATHS,
            "searchable": base != "JSON",
            "aggregatable": base not in ("JSON", "Text"),
            "sortable": path in PK_PATHS or path_leaf(path) in ("occur_time", "ingest_time", "parse_time"),
            "length": 128 if base == "String" else None,
        })

    for path, cname, desc in ENVELOPE_LEAVES:
        add(path, cname, desc)
    for path, cname, desc in TYPICAL_FACETS:
        add(path, cname, desc)

    spec = json.loads(OBJECT_FIELDS.read_text(encoding="utf-8"))
    by_type = {e["type"]: e for e in spec["entity_types"]}

    def expand(etype: str, prefix: str, slot_label: str, depth: int = 0) -> None:
        if depth > 2 or etype not in by_type:
            return
        ent = by_type[etype]
        title = ent.get("title") or etype
        for f in ent.get("fields") or []:
            name = f["name"]
            meaning = f.get("meaning") or name
            path = f"{prefix}{name}"
            short = LEAF_CNAME.get(name, name)
            cname = f"{slot_label}{title}{short}"
            if f.get("nested_type"):
                expand(f["nested_type"], path + ".", slot_label + title, depth + 1)
            elif f.get("nested"):
                parent_short = LEAF_CNAME.get(name, name)
                for n in f["nested"]:
                    add(
                        f"{path}.{n}",
                        f"{slot_label}{title}{parent_short}{LEAF_CNAME.get(n, n)}",
                        meaning,
                    )
            else:
                add(path, cname, meaning)

    for etype, ent in by_type.items():
        expand(etype, f"subject.{etype}.", SLOT_CNAME["subject"])
        expand(etype, f"object.{etype}.", SLOT_CNAME["object"])
        if ent.get("carrier"):
            expand(etype, f"carriers[].{etype}.", SLOT_CNAME["carriers"])
        if ent.get("observer"):
            expand(etype, f"observation.observer.{etype}.", SLOT_CNAME["observation.observer"])

    # 031 VARIANT 顶层对象也登记为逻辑字段：检索字段列表经
    # DamMeta(kind=2) INNER JOIN DataStandardInfo 取 cname，缺 info 行的
    # DAM 列会被整行丢弃（metadata-service SearchConfigRepository）。
    for path, cname, desc in (
        ("subject", "主体对象", "subject typed object；33 标量之外的完整对象"),
        ("object", "客体对象", "object typed object"),
        ("carriers", "载体对象", "carriers[] 含 carrier_role"),
        ("facets", "行为维度", "领域行为上下文（network/dns/http/ics/…）"),
        ("observation", "观察详情", "observer typed object、assertion、evidence_refs"),
        ("extensions", "扩展", "source_private/profiles/enrichments"),
    ):
        add(path, cname, desc)

    return rows



def stable_id(code: str, ns: int = ID_NS) -> int:
    h = hashlib.sha1(code.encode("utf-8")).hexdigest()
    return ns + (int(h[:12], 16) % 90_000_000_000_000)


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def parse_031(path: Path) -> list[dict]:
    text = path.read_text(encoding="utf-8")
    cols = []
    for m in re.finditer(
        r"`(\w+)`\s+(VARCHAR\((\d+)\)|DATETIME(?:\((\d+)\))?|VARIANT)\s+(NOT NULL|NULL)?"
        r"(?:\s+COMMENT\s+'([^']*)')?",
        text,
    ):
        name, typ, vlen, dprec, nulls, comment = m.groups()
        if name.startswith("idx_"):
            continue
        nullable = nulls != "NOT NULL"
        if typ.startswith("VARCHAR"):
            base, length = "String", int(vlen)
        elif typ.startswith("DATETIME"):
            base, length = "Datetime", None
        else:
            base, length = "JSON", None
        cols.append({
            "name": name,
            "base": base,
            "length": length,
            "nullable": nullable,
            "comment": comment or "",
            "pri_key": name in ("tenant_id", "occur_time", "event_id"),
            "time_field": name in ("occur_time", "ingest_time", "parse_time"),
        })
    if len(cols) < 30:
        raise SystemExit(f"031 parse got {len(cols)} columns, expected ~39")
    return cols


def index_by(rows: list[dict], key: str) -> dict:
    return {r[key]: r for r in rows if r.get(key) is not None}

def validate(backup: dict) -> list[str]:
    issues = []
    tables = backup.get("tables") or {}
    if backup.get("version") != BACKUP_VERSION:
        issues.append(f"version {backup.get('version')!r} != {BACKUP_VERSION}")
    optional = {"t_physical_column"}
    for t in TABLE_ORDER:
        if t not in tables and t not in optional:
            issues.append(f"missing table {t}")
    op_codes = {r["code"] for r in tables.get("t_operator") or []}
    for r in tables.get("t_data_business_type_base") or []:
        try:
            op = json.loads(r["operator"])
        except Exception as e:
            issues.append(f"operator JSON {r.get('code')}: {e}")
            continue
        for o in [op.get("default_operator"), *(op.get("supported_operators") or [])]:
            if o and o not in op_codes:
                issues.append(f"type {r.get('code')} uses operator {o!r} not in t_operator")
    std_ids = {r["id"] for r in tables.get("t_data_standard") or []}
    base_ids = {r["id"] for r in tables.get("t_data_business_type_base") or []}
    for r in tables.get("t_data_standard_info") or []:
        if r.get("category_id") not in std_ids:
            issues.append(f"info {r.get('code')} category_id orphan")
        if r.get("data_business_type_id") and r["data_business_type_id"] not in base_ids:
            issues.append(f"info {r.get('code')} type_id orphan")
    info_ids = {r["id"] for r in tables.get("t_data_standard_info") or []}
    bt_ids = {r["id"] for r in tables.get("t_business_type") or []}
    for r in tables.get("t_data_standard_business_type_mapping") or []:
        if r["data_standard_info_id"] not in info_ids:
            issues.append("mapping info orphan")
            break
        if r["business_type_id"] not in bt_ids:
            issues.append("mapping business_type orphan")
            break
    dam_cols = {r["id"] for r in tables.get("t_dam_meta") or [] if r.get("kind") == 2}
    dam_tables = {r["id"] for r in tables.get("t_dam_meta") or [] if r.get("kind") == 1}
    for r in tables.get("t_dam_column_shape") or []:
        if r.get("root_column_id") not in dam_cols:
            issues.append(f"shape {r.get('path')} root orphan")
            break
        if r.get("data_standard_info_id") and r["data_standard_info_id"] not in info_ids:
            issues.append(f"shape {r.get('path')} info orphan")
            break
    for r in tables.get("t_topic_table") or []:
        if r.get("topic_id") not in std_ids:
            issues.append("topic_table topic orphan")
            break
        if r.get("dam_table_id") not in dam_tables:
            issues.append("topic_table dam table orphan")
            break
    for r in tables.get("t_dam_meta") or []:
        if r.get("data_standard_info_id") and r["data_standard_info_id"] not in info_ids:
            issues.append(f"dam {r.get('name')} info orphan")
            break
    return issues


def bound_info_ids(tables: dict) -> set:
    ids = set()
    for r in tables.get("t_dam_meta") or []:
        i = r.get("data_standard_info_id")
        if i is not None:
            ids.add(i)
    for r in tables.get("t_dam_column_shape") or []:
        i = r.get("data_standard_info_id")
        if i is not None:
            ids.add(i)
    return ids


def strip_synthetic_dam_table(tables: dict, table_name: str) -> dict:
    """Remove DAM table/columns/shapes/topic bind. Logical infos stay."""
    dam = tables.get("t_dam_meta") or []
    table_ids = {r["id"] for r in dam if r.get("kind") == 1 and r.get("name") == table_name}
    col_ids = {r["id"] for r in dam if r.get("kind") == 2 and r.get("pid") in table_ids}
    drop_dam = table_ids | col_ids
    tables["t_dam_meta"] = [r for r in dam if r["id"] not in drop_dam]
    dropped_shapes = 0
    kept_shapes = []
    for s in tables.get("t_dam_column_shape") or []:
        if s.get("root_column_id") in col_ids:
            dropped_shapes += 1
        else:
            kept_shapes.append(s)
    tables["t_dam_column_shape"] = kept_shapes
    dropped_topics = 0
    kept_topics = []
    for r in tables.get("t_topic_table") or []:
        if r.get("dam_table_id") in table_ids:
            dropped_topics += 1
        else:
            kept_topics.append(r)
    tables["t_topic_table"] = kept_topics
    return {
        "tables": len(table_ids),
        "columns": len(col_ids),
        "shapes": dropped_shapes,
        "topic_binds": dropped_topics,
    }


def prune_unbound_topic_infos(tables: dict, topic_code: str) -> dict:
    """Drop logical fields on a hybrid topic that are not bound to DAM col/shape."""
    std = next((r for r in tables.get("t_data_standard") or [] if r.get("code") == topic_code), None)
    if std is None:
        return {"dropped": 0, "names": []}
    bound = bound_info_ids(tables)
    drop_ids = set()
    names = []
    for r in tables.get("t_data_standard_info") or []:
        if r.get("category_id") == std["id"] and r["id"] not in bound:
            drop_ids.add(r["id"])
            names.append(r.get("name"))
    tables["t_data_standard_info"] = [
        r for r in tables.get("t_data_standard_info") or [] if r["id"] not in drop_ids
    ]
    tables["t_data_standard_business_type_mapping"] = [
        r for r in tables.get("t_data_standard_business_type_mapping") or []
        if r["data_standard_info_id"] not in drop_ids
    ]
    return {"dropped": len(drop_ids), "names": names}


def layer_issues(backup: dict) -> list[str]:
    issues = []
    tables = backup.get("tables") or {}
    for r in tables.get("t_dam_meta") or []:
        name = str(r.get("name") or "")
        if r.get("kind") == 2 and ("." in name or "[]" in name):
            issues.append(f"DAM column {name} looks like a logical path")
            break
    dam_tables = [r for r in tables.get("t_dam_meta") or [] if r.get("kind") == 1 and r.get("name") == "sdm_event_behavior"]
    if dam_tables:
        tid = dam_tables[0]["id"]
        ncols = sum(1 for r in tables.get("t_dam_meta") or [] if r.get("kind") == 2 and r.get("pid") == tid)
        if ncols != 39:
            issues.append(f"DAM sdm_event_behavior has {ncols} columns, expected 39")
        variants = {
            r["name"] for r in tables.get("t_dam_meta") or []
            if r.get("kind") == 2 and r.get("pid") == tid and r.get("name") in VARIANT_COLUMNS
        }
        if variants != set(VARIANT_COLUMNS):
            issues.append(f"DAM missing VARIANT columns: {set(VARIANT_COLUMNS) - variants}")
        if any(r.get("kind") == 1 and r.get("name") == "sdm_event" for r in tables.get("t_dam_meta") or []):
            issues.append("DAM still has frozen sdm_event table")
    return issues

def comment_logical_path(comment: str, col_name: str) -> str | None:
    if col_name in VARIANT_COLUMNS:
        return None
    if not comment:
        return None
    c = comment.replace("，", ",").replace("；", ";").replace("：", ":")
    c = c.split(",")[0].split(";")[0].split(":")[0].strip()
    c = c.split()[0] if c else c
    if c.startswith("carriers[0]."):
        return "carriers[]." + c.split(".", 1)[1]
    if re.match(r"^[a-z][a-z0-9_.\[\]]*$", c):
        return c
    return None




def physical_type(col: dict) -> str:
    if col["base"] == "String":
        return f"varchar({col['length'] or 128})"
    if col["base"] == "Datetime":
        return "datetime(3)"
    return "variant"


def object_field_names() -> list[str]:
    spec = json.loads(OBJECT_FIELDS.read_text(encoding="utf-8"))
    names: list[str] = []
    seen: set[str] = set()
    def walk(fields: list, prefix: str = "") -> None:
        for f in fields or []:
            name = f["name"]
            path = f"{prefix}{name}" if prefix else name
            if f.get("nested_type"):
                continue
            if f.get("nested"):
                for n in f["nested"]:
                    leaf = f"{path}.{n}"
                    if leaf not in seen:
                        seen.add(leaf)
                        names.append(leaf)
            elif path not in seen:
                seen.add(path)
                names.append(path)
    for ent in spec["entity_types"]:
        walk(ent.get("fields") or [])
    return names


def drop_legacy_hybrid_event(tables: dict) -> dict:
    """Remove frozen sdm_event logical standard, DAM, shapes, topic bind, old dicts."""
    std = next((r for r in tables.get("t_data_standard") or [] if r.get("code") == "sdm2_log_sdm_event"), None)
    dropped_infos = 0
    if std:
        info_ids = {r["id"] for r in tables.get("t_data_standard_info") or [] if r.get("category_id") == std["id"]}
        dropped_infos = len(info_ids)
        tables["t_data_standard_info"] = [
            r for r in tables.get("t_data_standard_info") or [] if r["id"] not in info_ids
        ]
        tables["t_data_standard_business_type_mapping"] = [
            r for r in tables.get("t_data_standard_business_type_mapping") or []
            if r["data_standard_info_id"] not in info_ids
        ]
        tables["t_data_standard_version"] = [
            r for r in tables.get("t_data_standard_version") or []
            if r.get("data_standard_id") != std["id"]
        ]
        tables["t_data_standard"] = [
            r for r in tables.get("t_data_standard") or [] if r["id"] != std["id"]
        ]
    dam_drop = strip_synthetic_dam_table(tables, "sdm_event")
    dict_ids = {
        r["id"] for r in tables.get("t_definitive_standard") or []
        if r.get("code") in LEGACY_EVENT_DICTS
    }
    dropped_dict_vals = 0
    if dict_ids:
        dropped_dict_vals = sum(
            1 for r in tables.get("t_definitive_standard_content") or []
            if r.get("category_id") in dict_ids
        )
        tables["t_definitive_standard_content"] = [
            r for r in tables.get("t_definitive_standard_content") or []
            if r.get("category_id") not in dict_ids
        ]
        tables["t_definitive_standard"] = [
            r for r in tables.get("t_definitive_standard") or [] if r["id"] not in dict_ids
        ]
    return {
        "infos": dropped_infos,
        "dam": dam_drop,
        "dicts": len(dict_ids),
        "dict_values": dropped_dict_vals,
    }


def upsert_behavior_physical(backup: dict, ddl: Path) -> dict:
    """031 39 columns as DAM; VARIANT internals as shapes; topic bind to behavior standard."""
    tables = backup["tables"]
    now = now_iso()
    cols = parse_031(ddl)
    db = next(r for r in tables["t_dam_meta"] if r.get("kind") == 0 and r.get("name") == "sdm2_log")
    std = next(r for r in tables["t_data_standard"] if r.get("code") == "sdm2_log_sdm_event_behavior")
    info_by_code = {r["code"]: r for r in tables["t_data_standard_info"] if r.get("category_id") == std["id"]}

    stripped = strip_synthetic_dam_table(tables, "sdm_event_behavior")
    table_id = stable_id("dam:table:sdm2_log.sdm_event_behavior")
    tables["t_dam_meta"].append({
        "id": table_id,
        "pid": db["id"],
        "name": "sdm_event_behavior",
        "cname": "行为事件",
        "description": "sdm_event_behavior 生产表（031；33 标量 + 6 VARIANT）",
        "data_standard_info_id": None,
        "business_type_code": None,
        "owner": db.get("owner") or "dysec",
        "kind": 1,
        "status": None,
        "last_modify": None,
        "last_access": None,
        "create_user": "sdm2-generate_metadata_backup",
        "update_user": "",
        "create_time": now,
        "update_time": now,
        "trcname": None,
        "physical_type": None,
        "nestable": None,
    })

    bound = 0
    col_ids: dict[str, int] = {}
    variant_logical = {
        "subject_detail": "subject",
        "object_detail": "object",
        "observation_detail": "observation",
        "carriers": "carriers",
        "facets": "facets",
        "extensions": "extensions",
    }
    for col in cols:
        cid = stable_id(f"dam:col:sdm2_log.sdm_event_behavior.{col['name']}")
        col_ids[col["name"]] = cid
        if col["name"] in variant_logical:
            logical = variant_logical[col["name"]]
        else:
            logical = comment_logical_path(col.get("comment") or "", col["name"])
        info = info_by_code.get(path_code(logical)) if logical else None
        if info:
            bound += 1
        variant = col["name"] in VARIANT_COLUMNS
        # 检索界面显示的中文名取 t_dam_meta.cname（SearchConfigRepository
        # SELECT dm.cname → MetadataFieldDTO.cname）。注释首段是逻辑路径，
        # 不是中文；必须用关联 info 行的 cname。
        cname = (info or {}).get("cname") or (col.get("comment") or col["name"]).split("，")[0].split(",")[0][:64]
        tables["t_dam_meta"].append({
            "id": cid,
            "pid": table_id,
            "name": col["name"],
            "cname": cname,
            "description": col.get("comment") or "",
            "data_standard_info_id": info["id"] if info else None,
            "business_type_code": "JSON" if variant else col["base"],
            "owner": None,
            "kind": 2,
            "status": None,
            "last_modify": None,
            "last_access": None,
            "create_user": "sdm2-generate_metadata_backup",
            "update_user": "",
            "create_time": now,
            "update_time": now,
            "trcname": None,
            "physical_type": physical_type(col),
            "nestable": variant,
        })

    shape_specs: list[tuple[str, str, str | None]] = []
    for path, cname, _desc in TYPICAL_FACETS:
        shape_specs.append(("facets", path, path))
    for path in (
        "extensions.source_private", "extensions.profiles", "extensions.enrichments",
    ):
        shape_specs.append(("extensions", path, path))
    shape_specs.extend([
        ("observation_detail", "observation_detail.observer", None),
        ("observation_detail", "observation_detail.evidence_refs", "observation.evidence_refs[]"),
        ("carriers", "carriers.carrier_role", "carriers[].carrier_role"),
    ])
    for name in object_field_names():
        shape_specs.append(("subject_detail", f"subject_detail.{name}", None))
        shape_specs.append(("object_detail", f"object_detail.{name}", None))

    n_shapes = 0
    for root_name, path, logical in shape_specs:
        root_id = col_ids.get(root_name)
        if root_id is None:
            continue
        info = info_by_code.get(path_code(logical)) if logical else None
        segment = path.rsplit(".", 1)[-1]
        tables["t_dam_column_shape"].append({
            "id": stable_id(f"dam:shape:sdm2_log.sdm_event_behavior.{path}"),
            "root_column_id": root_id,
            "parent_id": None,
            "segment": segment,
            "path": path,
            "cname": None,
            "trcname": None,
            "description": None,
            "data_standard_info_id": info["id"] if info else None,
            "physical_type": None,
            "ordinal_position": None,
            "create_user": "sdm2-generate_metadata_backup",
            "update_user": "",
            "create_time": now,
            "update_time": now,
            "nestable": True,
        })
        n_shapes += 1

    tables["t_topic_table"] = [
        r for r in tables.get("t_topic_table") or []
        if r.get("topic_id") != std["id"]
    ]
    tables["t_topic_table"].append({
        "id": stable_id("topic:sdm2_log_sdm_event_behavior"),
        "topic_id": std["id"],
        "dam_table_id": table_id,
        "create_time": now,
        "update_time": now,
    })
    return {
        "columns": len(cols),
        "bound_scalars": bound,
        "shapes": n_shapes,
        "stripped_prior": stripped,
    }


def align_layers(backup: dict) -> dict:
    tables = backup["tables"]
    for t in ("t_dam_column_shape", "t_physical_column", "t_topic_table"):
        tables.setdefault(t, [])
    stripped = {name: strip_synthetic_dam_table(tables, name) for name in SYNTHETIC_DAM_TABLES}
    pruned = {code: prune_unbound_topic_infos(tables, code) for code in HYBRID_TOPIC_CODES}
    return {"stripped_dam": stripped, "pruned_infos": pruned}



def fix_operators(backup: dict) -> int:
    tables = backup["tables"]
    op_codes = {r["code"] for r in tables["t_operator"]}
    n = 0
    for r in tables["t_data_business_type_base"]:
        op = json.loads(r["operator"])
        changed = False

        def canon(o: str) -> str:
            if o in op_codes:
                return o
            alt = OPERATOR_ALIASES.get(o)
            if alt and alt in op_codes:
                return alt
            if o == "NEQ" and "NE" in op_codes:
                return "NE"
            return o

        new_default = canon(op["default_operator"])
        new_supported = [canon(x) for x in op["supported_operators"]]
        # drop dups, keep order
        seen = set()
        deduped = []
        for x in new_supported:
            if x not in seen:
                seen.add(x)
                deduped.append(x)
        if new_default != op["default_operator"] or deduped != op["supported_operators"]:
            op["default_operator"] = new_default
            op["supported_operators"] = deduped
            r["operator"] = json.dumps(op, ensure_ascii=False, separators=(",", ":"))
            n += 1
    return n

def ensure_agency_tags(tables: dict, now: str) -> None:
    """Add SUBJECT/OBJECT under log_field_class if missing."""
    cat = next(r for r in tables["t_business_type_category"] if r["code"] == "log_field_class")
    by_name = {r["name"]: r for r in tables["t_business_type"]}
    specs = [
        ("SUBJECT", "主体", "行为发起者（agency）；不是攻击者"),
        ("OBJECT", "客体", "行为承受者（agency）；不是受害者"),
    ]
    for name, cname, desc in specs:
        if name in by_name:
            continue
        tables["t_business_type"].append({
            "id": stable_id(f"btype:{name}"),
            "category_id": cat["id"],
            "name": name,
            "cname": cname,
            "description": desc,
            "is_delete": False,
            "create_user": "sdm2-generate_metadata_backup",
            "update_user": "",
            "create_time": now,
            "update_time": now,
        })


def upsert_behavior(backup: dict, ddl: Path | None = None) -> dict:
    """Insert/replace sdm_event_behavior as logical search fields (07 + object-fields).

    Does not write t_dam_meta / t_dam_column_shape. 07 paths are not physical columns.
    """
    del ddl
    tables = backup["tables"]
    fields = logical_fields()
    now = now_iso()
    ensure_agency_tags(tables, now)
    types = {r["code"]: r["id"] for r in tables["t_data_business_type_base"]}
    btypes = {r["name"]: r["id"] for r in tables["t_business_type"]}
    parent = next(r for r in tables["t_data_standard"] if r["code"] == "sdm2_log")

    std_id = stable_id("std:sdm2_log_sdm_event_behavior")

    old_info_ids = {
        r["id"] for r in tables["t_data_standard_info"]
        if str(r.get("code") or "").startswith("sdm_event_behavior__")
    }
    tables["t_data_standard"] = [
        r for r in tables["t_data_standard"] if r.get("code") != "sdm2_log_sdm_event_behavior"
    ]
    tables["t_data_standard_info"] = [
        r for r in tables["t_data_standard_info"] if r["id"] not in old_info_ids
    ]
    tables["t_data_standard_version"] = [
        r for r in tables["t_data_standard_version"] if r.get("data_standard_id") != std_id
    ]
    tables["t_data_standard_business_type_mapping"] = [
        r for r in tables["t_data_standard_business_type_mapping"]
        if r["data_standard_info_id"] not in old_info_ids
    ]
    stripped = strip_synthetic_dam_table(tables, "sdm_event_behavior")

    tables["t_data_standard"].append({
        "id": std_id,
        "name": "行为事件",
        "description": "sdm_event_behavior 逻辑信封字段（2.0；07 + object-fields）。无物理表，不写 DAM。",
        "pid": parent["id"],
        "is_leaf": True,
        "code": "sdm2_log_sdm_event_behavior",
        "create_time": now,
        "update_time": now,
    })

    template = next(
        r for r in tables["t_data_standard_info"]
        if r.get("code") == "sdm_event__occur_time"
    )

    new_mappings = []
    for i, col in enumerate(fields, start=1):
        code = path_code(col["path"])
        info_id = stable_id(f"info:{code}")
        base_name = col["base"] if col["base"] in types else "String"
        base_id = types[base_name]
        row = dict(template)
        row.update({
            "id": info_id,
            "code": code,
            "name": col["path"],
            "cname": col["cname"],
            "alias_name": col["cname"],
            "category_id": std_id,
            "def_standard_id": None,
            "data_business_type_id": base_id,
            "default_value": None,
            "is_nullable": col["nullable"],
            "pri_key": col["pri_key"],
            "rules": None,
            "min_value": None,
            "max_value": None,
            "data_len": col["length"],
            "data_accuracy": 3 if base_name == "Datetime" else None,
            "measurement": None,
            "description": col["description"],
            "publish_time": None,
            "sort_sign": i,
            "is_publish": True,
            "create_user": "sdm2-generate_metadata_backup",
            "update_user": "",
            "create_time": now,
            "update_time": now,
            "is_delete": False,
            "is_searchable": col["searchable"],
            "is_aggregatable": col["aggregatable"],
            "is_sortable": col["sortable"],
            "is_returned": True,
            "is_default_column": col["default_column"],
            "is_time_field": col["time_field"],
            "is_suggestable": False,
            "nestable": base_name == "JSON",
        })
        tables["t_data_standard_info"].append(row)

        for tag in col["tags"]:
            bt_id = btypes.get(tag)
            if not bt_id:
                continue
            new_mappings.append({
                "id": stable_id(f"map:{code}:{tag}"),
                "data_standard_info_id": info_id,
                "business_type_id": bt_id,
                "create_time": now,
                "update_time": now,
            })

    tables["t_data_standard_business_type_mapping"].extend(new_mappings)
    digest = hashlib.sha256(
        json.dumps([c["path"] for c in fields], separators=(",", ":")).encode()
    ).hexdigest()[:16]
    tables["t_data_standard_version"].append({
        "id": stable_id("ver:sdm_event_behavior"),
        "data_standard_id": std_id,
        "version_hash": digest,
        "version": "2.0",
        "update_time": now,
        "create_user": "sdm2-generate_metadata_backup",
    })
    return {
        "standard_id": std_id,
        "fields": len(fields),
        "mappings": len(new_mappings),
        "stripped_dam": stripped,
    }


_ISO_Z = re.compile(r"^(\d{4}-\d{2}-\d{2})T(\d{2}:\d{2}:\d{2}(?:\.\d+)?)Z$")
# 服务 convertTimestampValue 只认 * _time / *Time；84 会导入 t_physical_column.scanned_at（timestamptz）
TIMESTAMPTZ_KEYS = {"scanned_at", "last_modify", "last_access"}


def coerce_timestamptz(backup: dict) -> int:
    """Turn ISO-Z strings on timestamptz columns into 'YYYY-MM-DD HH:MM:SS.ffffff+00'."""
    n = 0
    for rows in backup["tables"].values():
        for row in rows or []:
            for k in TIMESTAMPTZ_KEYS:
                v = row.get(k)
                if not isinstance(v, str):
                    continue
                m = _ISO_Z.match(v)
                if not m:
                    continue
                row[k] = f"{m.group(1)} {m.group(2)}+00"
                n += 1
    return n

def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--baseline", required=True, help="POC 导出的 metadata-backup-*.json")
    ap.add_argument("--out", help="输出路径（默认 stdout）")
    ap.add_argument("--ddl", default=str(DDL_031), help="031 DDL（兼容保留，不再驱动数据标准）")
    ap.add_argument("--fix-operators", action="store_true")
    ap.add_argument("--upsert-behavior", action="store_true",
                    help="刷新行为事件逻辑字段 + 031 DAM；去掉冻结 sdm_event")
    ap.add_argument("--validate-only", action="store_true")
    args = ap.parse_args(argv[1:])

    backup = json.loads(Path(args.baseline).read_text(encoding="utf-8"))
    before = validate(backup)
    print(f"baseline issues: {len(before)}")
    for x in before[:12]:
        print(f"  - {x}")

    if args.validate_only:
        return 1 if before else 0

    if args.fix_operators:
        n = fix_operators(backup)
        print(f"fixed operator JSON on {n} base types")

    if args.upsert_behavior:
        stats = upsert_behavior(backup, Path(args.ddl))
        print(f"upserted sdm_event_behavior logical: {stats}")
        dropped = drop_legacy_hybrid_event(backup["tables"])
        print(f"dropped legacy sdm_event: {json.dumps(dropped, ensure_ascii=False)}")
        phys = upsert_behavior_physical(backup, Path(args.ddl))
        print(f"upserted sdm_event_behavior DAM: {json.dumps(phys, ensure_ascii=False)}")


    aligned = align_layers(backup)
    print(f"aligned layers: {json.dumps(aligned, ensure_ascii=False)}")
    for code, info in aligned["pruned_infos"].items():
        if info["names"]:
            print(f"  pruned {code}: {info['names']}")

    ntz = coerce_timestamptz(backup)
    print(f"coerced timestamptz strings: {ntz}")

    dropped = backup["tables"].pop("t_physical_column", None)
    if dropped is not None:
        print(f"dropped t_physical_column ({len(dropped)} rows); scanned_at is timestamptz and not a *_time column")

    for t in TABLE_ORDER:
        if t == "t_physical_column":
            continue
        backup["tables"].setdefault(t, [])

    backup["exportTime"] = now_iso()
    backup["version"] = BACKUP_VERSION

    after = validate(backup) + layer_issues(backup)
    print(f"output issues: {len(after)}")
    for x in after[:12]:
        print(f"  - {x}")
    if after:
        print("refusing to write: output still has contract issues", file=sys.stderr)
        return 1

    text = json.dumps(backup, ensure_ascii=False, indent=2)
    if args.out:
        Path(args.out).write_text(text + "\n", encoding="utf-8")
        print(f"wrote {args.out} ({len(text)} bytes)")
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
