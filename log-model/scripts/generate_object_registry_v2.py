#!/usr/bin/env python3
"""Generate object-registry.v2.json — the behavior-model path registry (M2).

Sources of truth (never duplicated here):
  - log-model/docs/main/07-sdm-event-behavior.schema.json   envelope structure
  - log-model/contracts/hybrid-event/object-fields.v1.json  typed-object & assertion fields

Outputs:
  - log-model/contracts/hybrid-event/object-registry.v2.json

Also audits the retired v1 path set against the new registry: every v1 path is
classified as alias-resolved (exact registered target) or left in `unresolved`.
No v1 path is silently renamed. Projection-registry.v2 reads this alias_map;
do not keep a second PATH_MAP.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HYBRID = ROOT / "log-model" / "contracts" / "hybrid-event"
SCHEMA_PATH = ROOT / "log-model" / "docs" / "main" / "07-sdm-event-behavior.schema.json"
FIELDS_PATH = HYBRID / "object-fields.v1.json"
V1_PATH = HYBRID / "object-registry.v1.json"
OUT_PATH = HYBRID / "object-registry.v2.json"

# Explicit old→new field renames inside an otherwise prefix-mapped role.
FIELD_ALIASES = {
    ("process", "cmdline"): ("process", "command_line"),
    ("process", "uid"): ("process", "guid"),
    ("resource", "type"): ("resource", "kind"),
    ("resource", "subtype"): ("resource", "kind"),
    ("endpoint", "ipv4"): ("endpoint", "ip"),
    ("endpoint", "ipv6"): ("endpoint", "ip"),
    ("host", "ipv4"): ("host", "ip"),
    ("host", "ipv6"): ("host", "ip"),
    ("device", "ipv4"): ("device", "ip"),
    ("device", "ipv6"): ("device", "ip"),
    ("device", "ip_addresses[].address"): ("device", "ip"),
}

META_EVENT_ALIASES = {
    "metadata.tenant_id": "meta.tenant_id",
    "metadata.occur_time": "meta.occur_time",
    "metadata.ingest_time": "meta.ingest_time",
    "metadata.event_id": "meta.event_id",
    "metadata.parse_time": "meta.parse_time",
    "metadata.schema_version": "meta.schema_version",
    "metadata.mapping_id": "meta.mapping_id",
    "metadata.data_source.vendor": "meta.data_source.vendor",
    "metadata.data_source.product": "meta.data_source.product",
    "metadata.data_source.category": "meta.data_source.category",
    "metadata.log.type": "meta.source_record.log_type",
    "metadata.log.level": "meta.source_record.log_level",
    "metadata.log.name": "meta.source_record.log_name",
    "metadata.log_id": "meta.source_record.log_id",
    "event.record_kind": "meta.source_record.record_kind",
    "event.domain": "behavior.layer",
    "event.type": "behavior.type",
    "event.operation": "behavior.operation",
    "event.outcome": "behavior.outcome",
    "event.message": "behavior.message",
}

def is_unambiguous_write(spec: dict) -> bool:
    w = spec.get("write")
    return isinstance(w, str) and "." in w and not spec.get("when")


def routing_closest(spec: dict) -> str:
    w = spec.get("write")
    if isinstance(w, str):
        return w
    if w == "split":
        return f"{spec['collector']} | {spec['sensor']}"
    if spec.get("instead"):
        return " | ".join(spec["instead"].values())
    return spec["v1_path"]



PENDING_COLUMN_ROUTING = {
    "severity": {
        "v1_path": "event.severity",
        "write": None,
        "reason": "原始日志等级 vs 检测判断拆分；本列不得默认写入 observation.assertion.severity",
        "instead": {
            "pri_or_syslog": "meta.source_record.log_level",
            "finding_severity": "observation.assertion.severity",
        },
        "top_level_column": "null，除非有获批且独立于 finding 的客观严重度证据",
    },
    "data_src_instance_id": {
        "v1_path": "metadata.data_source.instance_id",
        "write": "split",
        "reason": "采集器 vs 观察者拆分；采集器实例才进 meta.data_source.instance_id",
        "collector": "meta.data_source.instance_id",
        "sensor": "observation.observer",
    },
    "observer_product": {
        "v1_path": "roles.observer.product.name",
        "write": "observation.observer.application.name",
        "when": "observer.entity_type=application",
        "reason": "product 不是类型。检测产品→application.name；安全设备→device，产品身份留 meta.data_source.product",
    },
    "observer_type": {
        "v1_path": "roles.observer.type",
        "write": None,
        "reason": "不是类型。WAF/IDS/EDR 分类进 extensions.source_private.observer_class；角色分类用 entity_type",
    },
    "source_finding_category": {
        "v1_path": "source_finding.category",
        "write": "extensions.source_private.finding_category",
        "reason": "不在 assertion 11 字段内，禁止发明 assertion.category",
    },
    "source_finding_original_id": {
        "v1_path": "source_finding.original_id",
        "write": "extensions.source_private.original_finding_id",
        "reason": "不是 log_id；evidence_refs 指向 source_record，厂商告警 ID 进 source_private",
    },
}

ROUTING_BY_V1 = {spec["v1_path"]: spec for spec in PENDING_COLUMN_ROUTING.values()}


RELATED_ROUTING = {
    "parent_process": {
        "target": "subject.<process> | facets.process.ancestry[]",
        "rationale": "创建者（appear/spawn）是主体。仅血缘（终止/注入/写入/DNS 审计/账号变更）进 ancestry。父进程默认不是载体；仅当真正承载执行时才用 carriers[].carrier_role=parent_process。",
        "status": "routed",
        "evidence": "log-model/examples 10 张行为信封：创建=subject，其余=ancestry，carriers 均为空",
    },
    "grandparent_process": {
        "target": "facets.process.ancestry[]",
        "rationale": "创建链上下文由 ancestry 承接；不进 related、不进 carriers",
        "status": "routed",
    },
    "server_process": {
        "target": "carriers[].<process>",
        "rationale": "被连接服务由监听进程承载，carrier_role=server_process；协议/方向进 facets.network",
        "status": "routed",
        "evidence": "edr_ip_access/inbound_refuse：svchost -k TermService 承载被连接的 RDP 服务",
    },
    "alert_trigger_process": {
        "target": "subject",
        "rationale": "触发检测的进程是行为发起者，直接升格 subject；不再并列 carriers[] 分支",
        "status": "routed",
    },
    "victim": {
        "target": "observation.assertion.victims[]",
        "rationale": "受害者是攻防定性，只保留断言层",
        "status": "routed",
    },
    "login_source": {
        "target": "subject",
        "rationale": "登录来源是发起方，升格 subject；已有更具体主体时来源上下文进 facets.authentication",
        "status": "routed",
    },
    "system_user": {
        "target": "subject.<process|host>",
        "rationale": "属主只作主体对象的嵌套属性（process.user / host 富化），不升独立 user 主体",
        "status": "routed",
    },
    "source_file": {
        "target": "object.<file>",
        "rationale": "被读/被执行的来源文件按受事归客体",
        "status": "routed",
    },
    "resource_account": {
        "target": "extensions.source_private",
        "rationale": "无标准位；M3 判定是否进资源 facet",
        "status": "m3_review",
    },
    "request_authority": {
        "target": "facets.http | certificate.issuer",
        "rationale": "按 HTTP 上下文或证书属性",
        "status": "m3_review",
    },
    "managed_resource": {
        "target": "facets.<domain>",
        "rationale": "受管资源按领域上下文进 facet",
        "status": "m3_review",
    },
    "malware_file": {
        "target": "object.<file>",
        "rationale": "恶意文件实体是行为客体（object.file）；家族命名只进 observation.assertion.malware",
        "status": "routed",
    },
    "execution_host": {
        "target": "extensions.profiles.endpoint_asset.host",
        "rationale": "终裁：执行环境主机归 profiles，不进 carriers。carriers 保留给真正承载行为的实体（如 server_process）；升格需新证据重新评审",
        "status": "routed",
    },
    "connected_peripheral": {
        "target": "facets.peripheral",
        "rationale": "外设域已登记",
        "status": "routed",
    },
    "approver": {
        "target": "subject",
        "rationale": "审批是独立行为事件，拆事件后审批人是该事件的 subject",
        "status": "routed",
    },
}

ROLE_PREFIX = {
    "roles.source.": "subject.",
    "roles.target.": "object.",
    "roles.carriers[].": "carriers[].",
    "roles.observer.": "observation.observer.",
}


def resolve(node: dict, schema: dict) -> dict:
    while "$ref" in node:
        name = node["$ref"].split("/")[-1]
        merged = dict(schema["$defs"][name])
        merged.update({k: v for k, v in node.items() if k != "$ref"})
        node = merged
    return node


def flatten(props: dict, prefix: str, out: list, schema: dict) -> None:
    for key, raw in props.items():
        node = resolve(raw, schema)
        path = prefix + key
        if node.get("type") == "array":
            item = resolve(node.get("items", {}), schema)
            if item.get("properties"):
                flatten(item["properties"], path + "[].", out, schema)
            else:
                out.append(path + "[]")
            continue
        if node.get("properties"):
            flatten(node["properties"], path + ".", out, schema)
            continue
        out.append(path)


def emit_field_list(prefix: str, field_list: list, by_type: dict, out: list) -> None:
    for f in field_list:
        path = prefix + f["name"]
        out.append(path)
        for n in f.get("nested") or []:
            out.append(f"{path}.{n}")
        nt = f.get("nested_type")
        if nt:
            emit_field_list(path + ".", by_type[nt]["fields"], by_type, out)


def registered_prefix(path: str, known: set[str]) -> str | None:
    parts = path.split(".")
    for i in range(len(parts) - 1, 0, -1):
        cand = ".".join(parts[:i])
        if cand in known:
            return cand
    return None


def assertion_from_tokens(field: dict) -> list[str]:
    raw = field.get("from") or ""
    out = []
    for tok in raw.split("/"):
        tok = tok.strip()
        if not tok:
            continue
        out.append(tok if tok.startswith("source_finding.") else "source_finding." + tok)
    return out


def classify_source_finding(old: str, afields: list) -> tuple[str, dict | None]:
    """Return (alias|nested|none, assertion field or None). Exact from only for alias."""
    for f in afields:
        for full in assertion_from_tokens(f):
            if old == full:
                return "alias", f
            if full.endswith("_*"):
                stem = full[:-1]
                extra = old[len(stem):] if old.startswith(stem) else None
                if extra is not None and extra and "." not in extra and "[" not in extra:
                    return "alias", f
            if old.startswith(full + ".") or old.startswith(full + "["):
                return "nested", f
    return "none", None


def main() -> None:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    fields = json.loads(FIELDS_PATH.read_text(encoding="utf-8"))
    v1 = json.loads(V1_PATH.read_text(encoding="utf-8"))
    types = fields["entity_types"]
    type_names = [t["type"] for t in types]
    by_type = {t["type"]: t for t in types}
    carrier_types = [t["type"] for t in types if t["carrier"]]
    observer_types = [t["type"] for t in types if t["observer"]]

    enum = schema["$defs"]["entity_type"]["enum"]
    assert set(enum) == set(type_names), (set(enum) ^ set(type_names))

    paths: list[str] = []
    flatten(schema["properties"]["meta"]["properties"], "meta.", paths, schema)
    paths.append("event_kind")
    flatten(schema["properties"]["behavior"]["properties"], "behavior.", paths, schema)

    def role_slot(prefix: str, allowed: list[str], extra: list[str]) -> None:
        paths.extend(prefix + k for k in ("ref_id", "entity_type", *extra))
        for t in allowed:
            emit_field_list(f"{prefix}{t}.", by_type[t]["fields"], by_type, paths)

    role_slot("subject.", type_names, [])
    role_slot("object.", type_names, [])
    role_slot("carriers[].", carrier_types, ["carrier_role"])

    obs = schema["properties"]["observation"]
    for key, raw in obs["properties"].items():
        if key in ("observer", "assertion"):
            continue
        node = resolve(raw, schema)
        if node.get("type") == "array":
            paths.append(f"observation.{key}[]")
        else:
            paths.append(f"observation.{key}")
    role_slot("observation.observer.", observer_types, [])

    for f in fields["assertion"]["fields"]:
        paths.append("observation.assertion." + f["name"])

    for dom in schema["properties"]["facets"]["properties"]:
        paths.append(f"facets.{dom}")

    flatten(schema["properties"]["extensions"]["properties"], "extensions.", paths, schema)
    for spec in PENDING_COLUMN_ROUTING.values():
        w = spec.get("write")
        if isinstance(w, str) and "." in w and w not in paths:
            paths.append(w)
    assert len(paths) == len(set(paths)), "duplicate paths"
    known = set(paths)

    alias_map: list[dict] = []
    unresolved: list[dict] = []
    afields = fields["assertion"]["fields"]

    for old in v1["logical_paths"]:
        routed = ROUTING_BY_V1.get(old)
        if routed:
            if is_unambiguous_write(routed):
                alias_map.append({
                    "old": old,
                    "new": routed["write"],
                    "note": routed["reason"],
                })
            else:
                unresolved.append({
                    "old": old,
                    "closest": routing_closest(routed),
                    "reason": routed["reason"],
                })
            continue
        hit_role = False
        for pref, new_pref in ROLE_PREFIX.items():
            if not old.startswith(pref):
                continue
            hit_role = True
            rest = old[len(pref):]
            parts = rest.split(".", 1)
            key = parts[0]
            mapped = FIELD_ALIASES.get((key, parts[1] if len(parts) > 1 else ""))
            if mapped:
                t, fname = mapped
                new = f"{new_pref}{t}.{fname}"
                note = "字段更名或地址单值化"
            else:
                new = new_pref + rest
                note = None
            if new in known:
                entry = {"old": old, "new": new}
                if note:
                    entry["note"] = note
                alias_map.append(entry)
            else:
                parent = registered_prefix(new, known)
                if parent:
                    unresolved.append({
                        "old": old, "closest": new,
                        "reason": "已声明嵌套的未登记成员，M3 决定展开或丢弃",
                    })
                else:
                    unresolved.append({
                        "old": old, "closest": new,
                        "reason": "目标字段未登记（候选字段集之外），M3 逐条人工复核",
                    })
            break
        if hit_role:
            continue

        if old.startswith("source_finding."):
            kind, hit = classify_source_finding(old, afields)
            if kind == "alias" and hit:
                alias_map.append({
                    "old": old,
                    "new": "observation.assertion." + hit["name"],
                    "old_write": False,
                })
            elif kind == "nested" and hit:
                unresolved.append({
                    "old": old,
                    "closest": "observation.assertion." + hit["name"],
                    "reason": "source_finding 嵌套主张对象，M3 逐字段复核",
                    "old_write": False,
                })
            else:
                unresolved.append({
                    "old": old, "closest": "observation.assertion.?",
                    "reason": "source_finding 字段无直接断言映射，M3 人工复核",
                    "old_write": False,
                })
            continue

        if old.startswith("roles.related[]."):
            unresolved.append({
                "old": old, "closest": "related_routing",
                "reason": "related 按 relation_type 分流（见 related_routing 字典）",
            })
            continue



        if old in META_EVENT_ALIASES:
            new = META_EVENT_ALIASES[old]
            assert new in known, new
            alias_map.append({"old": old, "new": new})
            continue

        if old.startswith("facets."):
            alias_map.append({
                "old": old, "new": old,
                "note": "facet 域开放，成员不进对象注册表",
            })
            continue

        unresolved.append({
            "old": old, "closest": old,
            "reason": "未分类旧路径，M3 人工复核",
        })

    def added(v2: list[str], v1_types: list[str]) -> list[str]:
        return sorted(set(v2) - set(v1_types))

    def removed(v2: list[str], v1_types: list[str]) -> list[str]:
        return sorted(set(v1_types) - set(v2))

    registry = {
        "registry_version": 2,
        "model": "sdm_event_behavior",
        "event_kind": "behavior",
        "status": "m2-draft",
        "generated_from": [
            "log-model/docs/main/07-sdm-event-behavior.schema.json",
            "log-model/contracts/hybrid-event/object-fields.v1.json",
        ],
        "roles": {
            "subject": {"cardinality": "one", "types": type_names},
            "object": {"cardinality": "one", "types": type_names},
            "carriers": {"cardinality": "many", "types": carrier_types},
            "observer": {"cardinality": "one", "types": observer_types,
                         "nullable_entity_type": True},
        },
        "related_routing": RELATED_ROUTING,
        "pending_column_routing": PENDING_COLUMN_ROUTING,
        "entity_type_upgrade": {
            "by_role": {
                "subject": {
                    "v1": sorted(v1["roles"]["source"]["types"]),
                    "v2": type_names,
                    "added": added(type_names, v1["roles"]["source"]["types"]),
                },
                "object": {
                    "v1": sorted(v1["roles"]["target"]["types"]),
                    "v2": type_names,
                    "added": added(type_names, v1["roles"]["target"]["types"]),
                },
                "carriers": {
                    "v1": sorted(v1["roles"]["carriers"]["types"]),
                    "v2": carrier_types,
                    "added": added(carrier_types, v1["roles"]["carriers"]["types"]),
                },
                "observer": {
                    "v1": sorted(v1["roles"]["observer"]["types"]),
                    "v2": observer_types,
                    "added": added(observer_types, v1["roles"]["observer"]["types"]),
                    "removed": removed(observer_types, v1["roles"]["observer"]["types"]),
                    "note": "v1 product 不是类型，按迁移清单 §3.1 分流 device/application/service",
                },
            },
        },
        "array_reference": {
            "field": "ref_id",
            "scope": "event",
            "pattern": v1["array_reference"]["pattern"],
            "unique_within": "event",
            "applies_to": ["subject", "object", "carriers[]", "observation.observer"],
            "physical_indexes": [],
            "physical_indexes_are_identity": False,
            "note": "v1 role_index/peer_index/relation_index 随 related 容器一并废弃；物理索引 cutover 归 M4",
        },
        "facet_domains": sorted(schema["properties"]["facets"]["properties"]),
        "logical_paths": sorted(paths),
        "v1_compatibility": {
            "v1_registry": "object-registry.v1.json",
            "v1_status": "read-only alias; 写路径禁止指向 v1 路径（迁移清单 §三）",
            "source_finding_write": {
                "root": "source_finding",
                "write": False,
                "write_to": "observation.assertion",
                "reason": "source_finding 不得写入行为信封；检测结论只写 observation.assertion。投影列 source_finding_* 是 assertion 的物理名，不是旧逻辑写路径。",
            },
            "roles_write": {
                "root": "roles",
                "write": False,
                "write_to": {
                    "roles.source": "subject",
                    "roles.target": "object",
                    "roles.carriers": "carriers",
                    "roles.observer": "observation.observer",
                    "roles.related": "related_routing",
                },
                "reason": "旧 roles.* 不得写入行为信封；related 按 related_routing 分流，禁止 facets.related。",
            },
            "alias_map": alias_map,
            "unresolved": unresolved,
        },
    }
    OUT_PATH.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n",
                        encoding="utf-8")

    n_alias, n_unres = len(alias_map), len(unresolved)
    reasons: dict[str, int] = {}
    for u in unresolved:
        tag = re.sub(r"[（(].*", "", u["reason"]).strip()
        reasons[tag] = reasons.get(tag, 0) + 1
    print(f"object-registry.v2.json: {len(paths)} paths "
          f"(subject/object ×{len(type_names)}, carriers ×{len(carrier_types)}, "
          f"observer ×{len(observer_types)}, assertion ×{len(afields)})")
    print(f"v1 audit: {n_alias} alias-resolved, {n_unres} unresolved")
    for k, v in sorted(reasons.items(), key=lambda x: -x[1]):
        print(f"  unresolved[{k}] = {v}")
    dotted = [a for a in alias_map if "…" in a["new"] or "..." in a["new"]]
    assert not dotted, f"placeholder aliases forbidden: {dotted[:3]}"


if __name__ == "__main__":
    main()
