#!/usr/bin/env python3
"""Validate a behavior-envelope expected event (M3).

Checks:
  1. 07 JSON Schema (if jsonschema is installed)
  2. severity split (log_level vs assertion.severity vs top-level severity)
  3. observation.action / assertion pairing
  4. evidence_refs non-empty when observation 存在
  5. packet_data 只允许 facets 或 source_private
  6. unknown roles 用 null，不得 {}
  7. entity_type 与 typed object 一对一
  8. assertion 字段 ⊆ object-fields.v1
  9. behavior.outcome 处置/执行/记录分段：record 无 assertion 时只允许 observed/unknown；conclusion 与 allowed/denied 对齐
 10. source_finding / roles 不得写入行为信封

无参数时校验 log-model/examples 下全部 *.expected-sdm-event.behavior.json，
并对照同前缀的 *.wpl-to-sdm-event.behavior.json（若存在）。
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCHEMA = ROOT / "log-model" / "docs" / "main" / "07-sdm-event-behavior.schema.json"
FIELDS = ROOT / "log-model" / "contracts" / "hybrid-event" / "object-fields.v1.json"

ROLE_KEYS = ("subject", "object")
TYPED = (
    "user", "account", "host", "endpoint", "process", "file", "service",
    "domain", "url", "device", "resource", "application", "cloud",
    "container", "certificate", "script",
)
FORBIDDEN_PACKET = "packet_data"


def walk(obj, path=""):
    if isinstance(obj, dict):
        for k, v in obj.items():
            p = f"{path}.{k}" if path else k
            yield p, v
            yield from walk(v, p)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            p = f"{path}[]"
            yield p, v
            yield from walk(v, p)


def fail(errors: list[str], msg: str) -> None:
    errors.append(msg)


DENY_CONCLUSION = {"deny", "denied", "block", "blocked", "drop", "reject"}
ALLOW_CONCLUSION = {"allow", "allowed", "pass", "permit", "accept"}
EXEC_CONCLUSION = {"success", "succeed", "succeeded", "fail", "failed", "error",
                   "complete", "completed", "exit"}
DISPOSITION_OUTCOME = {"allowed", "denied"}
EXECUTION_OUTCOME = {"success", "failed"}
RECORD_FORBIDDEN_OUTCOME = DISPOSITION_OUTCOME | EXECUTION_OUTCOME
PROTOCOL_STATUS_PATHS = {"facets.network.connection_result", "facets.dns.rcode"}
EVIDENCE_REF_RE = re.compile(r"^(source_record|event|evidence):[A-Za-z0-9._:+/-]+$")


def natural_key(et: str, typed: dict | None):
    """按字段目录 §2.4 公式计算自然键；typed 信息不足时返回 None（无法核验，跳过）。"""
    if not isinstance(typed, dict):
        return None
    if et == "process":
        guid = typed.get("guid")
        if guid:
            return ("guid", str(guid).lower())
        path = (typed.get("file") or {}).get("path")
        if path:
            import hashlib
            return ("sha256path", hashlib.sha256(str(path).lower().encode()).hexdigest()[:32])
        return None
    if et == "file":
        md5 = (typed.get("hashes") or {}).get("md5")
        return ("md5", str(md5).lower()) if md5 else None
    if et == "domain":
        name = typed.get("name")
        return ("name", str(name).lower()) if name else None
    if et == "endpoint":
        return ("ip", str(typed.get("ip"))) if typed.get("ip") else None
    if et == "account":
        return ("name", str(typed.get("name"))) if typed.get("name") else None
    # host=资产ID / resource=声明语义键 / 其余无统一定义，无法从信封核验
    return None


def check_ref_formula(where: str, node: dict, err: list[str]) -> tuple | None:
    """校验单节点 ref_id 是否符合自然键公式；返回 (entity_type, natural) 供一致性检查。"""
    et = node.get("entity_type")
    rid = node.get("ref_id")
    if not et or not rid:
        return None
    typed = node.get(et) if isinstance(node.get(et), dict) else None
    nk = natural_key(et, typed)
    if nk is None:
        return None
    expected = f"{et}::{nk[1]}"
    if str(rid) != expected:
        fail(err, f"{where}.ref_id 不符公式：entity_type={et} 的自然键应得 {expected!r}，当前 {rid!r}（字段目录 §2.4）")
    return (et, nk[1])


def check_ref_consistency(where: str, node: dict, ident_map: dict, err: list[str]) -> None:
    """事件内/跨事件：同一 (entity_type, 自然键) 必须复用同一 ref_id；同一 ref_id 不得指向不同实体。"""
    ident = check_ref_formula(where, node, err)
    if ident is None:
        return
    rid = str(node["ref_id"])
    prev = ident_map.get(("id", ident))
    if prev is not None and prev != rid:
        fail(err, f"{where}: 实体 {ident} 此前 ref_id={prev!r}，当前 {rid!r}（公式不得漂移）")
    else:
        ident_map[("id", ident)] = rid
    prev_ident = ident_map.get(("rid", rid))
    if prev_ident is not None and prev_ident != ident:
        fail(err, f"{where}: ref_id={rid!r} 已绑定实体 {prev_ident}，当前 {ident}（ref_id 不得复用给不同实体）")
    else:
        ident_map[("rid", rid)] = ident


def check(event: dict, fields: dict, ident_map: dict | None = None) -> list[str]:
    err: list[str] = []
    ident_map = ident_map if ident_map is not None else {}
    if event.get("event_kind") != "behavior":
        fail(err, "event_kind 必须是 behavior")

    meta = event.get("meta") or {}
    obs = event.get("observation")
    assertion = (obs or {}).get("assertion") if obs else None
    action = (obs or {}).get("action") if obs else None
    outcome = (event.get("behavior") or {}).get("outcome")

    if not meta.get("mapping_id"):
        fail(err, "meta.mapping_id 必填；语义变化必须换新值")

    if "severity" in event:
        fail(err, "顶层不得出现 severity；日志等级走 meta.source_record.log_level，检测判断走 assertion.severity")

    if action in ("detect", "assess") and not assertion:
        fail(err, f"action={action} 必须有 observation.assertion")
    if action == "record" and assertion:
        fail(err, "action=record 不应设置 assertion")
    if obs is not None:
        refs = obs.get("evidence_refs")
        if not refs:
            fail(err, "observation 必须有非空 evidence_refs")
        for j, ref in enumerate(refs or []):
            if not isinstance(ref, str) or not EVIDENCE_REF_RE.match(ref):
                fail(err, f"evidence_refs[{j}]={ref!r} 不符 URI scheme "
                     f"^(source_record|event|evidence):…（字段目录 §2.10，G1 Q8-b）")

    if isinstance(assertion, dict):
        conclusion = assertion.get("conclusion")
        if conclusion is not None:
            cl = str(conclusion).lower()
            if cl in DENY_CONCLUSION and outcome != "denied":
                fail(err, f"assertion.conclusion={conclusion!r} 是处置拒绝，outcome 必须是 denied，当前 {outcome!r}")
            if cl in ALLOW_CONCLUSION and outcome != "allowed":
                fail(err, f"assertion.conclusion={conclusion!r} 是处置允许，outcome 必须是 allowed，当前 {outcome!r}")
    if outcome in DISPOSITION_OUTCOME and (not isinstance(assertion, dict)
                                            or assertion.get("conclusion") is None):
        fail(err, f"outcome={outcome!r} 是处置分段，必须有 assertion.conclusion 支撑（字段目录 §2.3）")
    if outcome in EXECUTION_OUTCOME:
        conclusion = assertion.get("conclusion") if isinstance(assertion, dict) else None
        cl = str(conclusion).lower() if conclusion is not None else None
        if cl not in EXEC_CONCLUSION:
            fail(err, f"outcome={outcome!r} 是执行分段，须有动作本身成败证据："
                 f"assertion.conclusion ∈ {sorted(EXEC_CONCLUSION)}"
                 f"（协议状态 connection_result/rcode 不构成执行分段，字段目录 §2.3）")
    if action == "record" and not assertion and outcome in RECORD_FORBIDDEN_OUTCOME:
        fail(err, "action=record 且无 assertion 时只允许 observed/unknown，不得使用处置或执行分段 "
             f"(allowed/denied/success/failed)，当前 {outcome!r}")

    for role in ROLE_KEYS:
        val = event.get(role, None)
        if val == {}:
            fail(err, f"{role} 不得用空对象 {{}} 表示未知，应使用 null")
        if isinstance(val, dict):
            et = val.get("entity_type")
            present = [k for k in TYPED if val.get(k)]
            if et and present != [et]:
                fail(err, f"{role} entity_type={et} 但 typed object={present}（只能选一）")
            if not val.get("ref_id"):
                fail(err, f"{role} 非 null 时必须有 ref_id")
            elif not str(val["ref_id"]).startswith(f"{et}::"):
                fail(err, f"{role}.ref_id 必须是 {et}:: 前缀，当前 {val['ref_id']!r}")
            if et == "endpoint" and ":" in str(val["ref_id"]).split("::", 1)[1]:
                fail(err, f"{role}.ref_id 端点身份不带端口（端口进 typed object）: {val['ref_id']!r}")
            check_ref_consistency(role, val, ident_map, err)

    observer = (obs or {}).get("observer") if obs else None
    if observer == {}:
        fail(err, "observer 不得用空对象 {}")
    if isinstance(observer, dict):
        et = observer.get("entity_type")
        present = [k for k in TYPED if observer.get(k)]
        if et and present != [et]:
            fail(err, f"observer entity_type={et} 但 typed object={present}（只能选一）")
        if "product" in observer:
            fail(err, "observer.product 不是类型；检测产品走 application，设备走 device")
        if "type" in observer:
            fail(err, "observer.type 已废除；分类走 entity_type 或 source_private.observer_class")
        rid = observer.get("ref_id")
        if rid and et and not str(rid).startswith(f"{et}::"):
            fail(err, f"observer.ref_id 必须是 {et}:: 前缀，当前 {rid!r}")
        device = observer.get("device") or {}
        host = observer.get("host") or {}
        if "device_ip" in observer or device.get("ip_addresses") or host.get("ip_addresses"):
            fail(err, "观察者地址必须是 device.ip / host.ip 单值")
        check_ref_consistency("observation.observer", observer, ident_map, err)

    carriers = event.get("carriers")
    if not isinstance(carriers, list):
        fail(err, "carriers 必须是数组（可为空）")
    else:
        for i, c in enumerate(carriers):
            if not isinstance(c, dict):
                fail(err, f"carriers[{i}] 必须是对象")
                continue
            et = c.get("entity_type")
            if et in {"network", "session", "protocol"}:
                fail(err, f"carriers[{i}].entity_type={et} 不是载体；协议/会话进 facets")
            if "protocol" in c or "session_id" in c:
                fail(err, f"carriers[{i}] 含 protocol/session_id，应进 facets")
            if et and not str(c.get("ref_id", "")).startswith(f"{et}::"):
                fail(err, f"carriers[{i}].ref_id 必须是 {et}:: 前缀，当前 {c.get('ref_id')!r}")
            check_ref_consistency(f"carriers[{i}]", c, ident_map, err)
    ancestry = ((event.get("facets") or {}).get("process") or {}).get("ancestry") or []
    for i, a in enumerate(ancestry):
        if not str(a.get("ref_id", "")).startswith("process::"):
            fail(err, f"facets.process.ancestry[{i}].ref_id 必须是 process:: 前缀，当前 {a.get('ref_id')!r}")
        check_ref_consistency(f"facets.process.ancestry[{i}]", a, ident_map, err)

    registered = {f["name"] for f in fields["assertion"]["fields"]}
    if isinstance(assertion, dict):
        extra = [k for k in assertion if k not in registered]
        if extra:
            fail(err, f"assertion 未登记字段 {extra}；进 source_private 或先登记")

    for p, v in walk(event):
        leaf = p.split(".")[-1]
        if leaf == FORBIDDEN_PACKET:
            if not (p.startswith("facets.") or p.startswith("extensions.source_private")):
                fail(err, f"packet_data 出现在 {p}，只允许 facets 或 extensions.source_private")
        if leaf in {"source_finding", "source_finding_obj"}:
            fail(err, f"source_finding 不得写入行为信封: {p}")
        if p in {"roles", "roles_obj"}:
            fail(err, f"旧 roles 不得写入行为信封: {p}")

    forbidden_root = ("diagnostics", "correlation", "mapping_revision",
                      "projection_version", "contract", "status",
                      "source_finding", "source_finding_obj", "roles", "roles_obj")
    for k in forbidden_root:
        if k in event:
            fail(err, f"暂缓或旧字段进入行为事件: {k}")
    return err


def check_mapping(event: dict, mapping: dict) -> list[str]:
    err: list[str] = []
    mid = (event.get("meta") or {}).get("mapping_id")
    if mapping.get("mapping_id") and mid and mapping["mapping_id"] != mid:
        fail(err, f"mapping_id 不一致: envelope={mid} mapping={mapping['mapping_id']}")
    outcome = (event.get("behavior") or {}).get("outcome")
    for w in mapping.get("writer_rules") or []:
        if w.get("target") == "behavior.outcome" and outcome is not None and w.get("value") != outcome:
            fail(err, f"writer outcome={w.get('value')!r} 与信封 {outcome!r} 不一致")

    # 协议状态不得充当执行分段证据（PROTOCOL_STATUS_PATHS 的实际使用点）：
    # 同一 wpl 源字段既写协议状态 facet、又写 assertion.conclusion / behavior.outcome，
    # 且信封 outcome ∈ 执行段 → 拒。防止把 connection_result/rcode 改写成 success/failed。
    if outcome in EXECUTION_OUTCOME:
        proto_sources: set[str] = set()
        for r in mapping.get("rows") or []:
            path = ".".join(r.get("sdm_path") or [])
            if any(path == p or path.endswith("." + p)
                   for p in PROTOCOL_STATUS_PATHS):
                proto_sources.add(r.get("wpl"))
        for r in mapping.get("rows") or []:
            path = ".".join(r.get("sdm_path") or [])
            if r.get("wpl") in proto_sources and (
                    path.endswith("assertion.conclusion") or path == "behavior.outcome"):
                fail(err, f"wpl 字段 {r.get('wpl')!r} 同时写入协议状态 facet 与 "
                     f"{path}，outcome={outcome!r} 是执行分段——协议状态不构成执行证据（字段目录 §2.3）")
    return err

def _record_event(outcome, extra_obs=None, extra_root=None):
    ev = {
        "event_kind": "behavior",
        "meta": {"mapping_id": "t.behavior.v1"},
        "behavior": {"layer": "network", "type": "flow", "outcome": outcome},
        "subject": None,
        "object": None,
        "carriers": [],
        "observation": {
            "action": "record",
            "observer": {"ref_id": None, "entity_type": None},
            "evidence_refs": ["source_record:x"],
        },
    }
    if extra_obs:
        ev["observation"].update(extra_obs)
    if extra_root:
        ev.update(extra_root)
    return ev


def self_test(fields: dict) -> int:
    cases = [
        ("record+success", _record_event("success"), "执行分段"),
        ("record+denied", _record_event("denied"), "处置或执行分段"),
        ("deny+unknown", {
            "event_kind": "behavior",
            "meta": {"mapping_id": "t.behavior.v1"},
            "behavior": {"layer": "network", "type": "read", "outcome": "unknown"},
            "subject": None,
            "object": None,
            "carriers": [],
            "observation": {
                "action": "detect",
                "observer": {"ref_id": None, "entity_type": "device", "device": {"vendor": "x"}},
                "assertion": {"conclusion": "deny"},
                "evidence_refs": ["source_record:x"],
            },
        }, "denied"),
        ("packet_data", _record_event("observed", extra_root={"subject": {
            "ref_id": "endpoint::1", "entity_type": "endpoint",
            "endpoint": {"ip": "198.51.100.25", "packet_data": "x"},
        }}), "packet_data"),
        ("host.ip_addresses", _record_event("observed", extra_obs={"observer": {
            "ref_id": None, "entity_type": "host", "host": {"ip_addresses": ["198.51.100.25"]},
        }}), "device.ip / host.ip"),
        ("ref_id 前缀", _record_event("observed", extra_root={"subject": {
            "ref_id": "process_abc", "entity_type": "process", "process": {"name": "x"},
        }}), "process:: 前缀"),
        ("endpoint ref_id 带端口", _record_event("observed", extra_root={"object": {
            "ref_id": "endpoint::203.0.113.162:443", "entity_type": "endpoint",
            "endpoint": {"ip": "203.0.113.162", "port": 443},
        }}), "不带端口"),
        ("process ref_id 公式漂移", _record_event("observed", extra_root={"subject": {
            "ref_id": "process::RANDOM_VALUE", "entity_type": "process",
            "process": {"guid": "d22b3fbcb9e77cb86834f6a18e2e0f68", "name": "svchost.exe"},
        }}), "不符公式"),
        ("process 无guid哈希公式", _record_event("observed", extra_root={"subject": {
            "ref_id": "process::00000000000000000000000000000000", "entity_type": "process",
            "process": {"name": "x", "file": {"path": "C:\\Windows\\System32\\svchost.exe"}},
        }}), "不符公式"),
        ("denied 无 conclusion", {
            "event_kind": "behavior",
            "meta": {"mapping_id": "t.behavior.v1"},
            "behavior": {"layer": "network", "type": "flow", "outcome": "denied"},
            "subject": None, "object": None, "carriers": [],
            "observation": {
                "action": "assess", "observer": {"ref_id": None, "entity_type": None},
                "assertion": {"title": "t"},
                "evidence_refs": ["source_record:x"],
            },
        }, "assertion.conclusion 支撑"),
        ("success 仅协议状态", {
            "event_kind": "behavior",
            "meta": {"mapping_id": "t.behavior.v1"},
            "behavior": {"layer": "network", "type": "flow", "outcome": "success"},
            "subject": None, "object": None, "carriers": [],
            "facets": {"network": {"connection_result": "connection_established"}},
            "observation": {
                "action": "assess", "observer": {"ref_id": None, "entity_type": None},
                "assertion": {"title": "t"},
                "evidence_refs": ["source_record:x"],
            },
        }, "成败证据"),
        ("evidence_refs 非法", _record_event("observed", extra_obs={
            "evidence_refs": ["raw-log-xyz"],
        }), "URI scheme"),
    ]
    rc = 0
    for name, ev, needle in cases:
        if ev is None:
            continue
        err = check(ev, fields)
        hit = any(needle in x for x in err)
        if not hit:
            print(f"self-test FAIL {name}: expected {needle!r} in {err}", file=sys.stderr)
            rc = 1
        else:
            print(f"self-test PASS {name}")
    # packet_data 不得双报
    pkt = [x for x in check(cases[3][1], fields) if "packet_data" in x]
    if len(pkt) != 1:
        print(f"self-test FAIL packet_data-once: {pkt}", file=sys.stderr)
        rc = 1
    else:
        print("self-test PASS packet_data-once")
    ok = _record_event("observed")
    if check(ok, fields):
        print(f"self-test FAIL record+observed should pass: {check(ok, fields)}", file=sys.stderr)
        rc = 1
    else:
        print("self-test PASS record+observed")
    # 跨事件：同一实体两个 ref_id → 第二个事件必须报漂移
    xmap: dict = {}
    e1 = _record_event("observed", extra_root={"subject": {
        "ref_id": "process::d22b3fbcb9e77cb86834f6a18e2e0f68", "entity_type": "process",
        "process": {"guid": "d22b3fbcb9e77cb86834f6a18e2e0f68", "name": "a"},
    }})
    e2 = _record_event("observed", extra_root={"subject": {
        "ref_id": "process::ffffffffffffffffffffffffffffffff", "entity_type": "process",
        "process": {"guid": "d22b3fbcb9e77cb86834f6a18e2e0f68", "name": "a"},
    }})
    check(e1, fields, xmap)
    err2 = check(e2, fields, xmap)
    if not any("公式不得漂移" in x for x in err2):
        print(f"self-test FAIL 跨事件 ref_id 漂移: {err2}", file=sys.stderr)
        rc = 1
    else:
        print("self-test PASS 跨事件 ref_id 漂移")
    # 映射级：协议状态源不得喂执行分段（评审反例：conclusion=success + 唯一证据 connection_result）
    poison = {
        "event_kind": "behavior", "meta": {"mapping_id": "t.behavior.v1"},
        "behavior": {"layer": "network", "type": "flow", "outcome": "success"},
        "subject": None, "object": None, "carriers": [],
        "facets": {"network": {"connection_result": "connection_established"}},
        "observation": {"action": "assess", "observer": {"ref_id": None, "entity_type": None},
                        "assertion": {"title": "t", "conclusion": "success"},
                        "evidence_refs": ["source_record:x"]},
    }
    poison_map = {"mapping_id": "t.behavior.v1", "rows": [
        {"wpl": "event_type", "sdm_path": ["facets", "network", "connection_result"]},
        {"wpl": "event_type", "sdm_path": ["observation", "assertion", "conclusion"]},
        {"wpl": "event_type", "sdm_path": ["behavior", "outcome"]},
    ]}
    merr = check_mapping(poison, poison_map)
    if not any("协议状态不构成执行证据" in x for x in merr):
        print(f"self-test FAIL 协议状态喂执行分段: {merr}", file=sys.stderr)
        rc = 1
    else:
        print("self-test PASS 协议状态喂执行分段")
    return rc



def resolve_ref(node: dict, schema: dict) -> dict:
    if "$ref" not in node:
        return node
    name = node["$ref"].split("/")[-1]
    merged = dict(schema["$defs"][name])
    merged.update({k: v for k, v in node.items() if k != "$ref"})
    return merged


def check_schema_lite(obj, schema: dict, node: dict | None = None, path: str = "$") -> list[str]:
    """required + additionalProperties:false + $ref + const/enum/type. No format/allOf."""
    err: list[str] = []
    node = resolve_ref(node or schema, schema)
    if "anyOf" in node:
        if obj is None and any(
            resolve_ref(a, schema).get("type") == "null" for a in node["anyOf"]
        ):
            return err
        sub = [a for a in node["anyOf"] if resolve_ref(a, schema).get("type") != "null"]
        if len(sub) == 1:
            return check_schema_lite(obj, schema, sub[0], path)
        return err
    types = node.get("type")
    if obj is None:
        if types == "null" or (isinstance(types, list) and "null" in types):
            return err
        if "enum" in node and None in node["enum"]:
            return err
        return err
    if "const" in node and obj != node["const"]:
        return [f"schema: {path} 应为 {node['const']!r}"]
    if "enum" in node and obj not in node["enum"]:
        return [f"schema: {path}={obj!r} 不在枚举 {node['enum']}"]
    expected = types if isinstance(types, list) else ([types] if types else None)
    if expected:
        py = {dict: "object", list: "array", str: "string", bool: "boolean",
              int: "integer", float: "number", type(None): "null"}
        tname = py.get(type(obj))
        if tname == "integer" and "number" in expected:
            pass
        elif tname not in expected:
            return [f"schema: {path} 类型 {tname} 不在 {expected}"]
    if types == "object" or "properties" in node or node.get("additionalProperties") is False:
        if not isinstance(obj, dict):
            return err
        props = node.get("properties") or {}
        for k in node.get("required") or []:
            if k not in obj:
                err.append(f"schema: 缺 {path}.{k}")
        if node.get("additionalProperties") is False:
            extra = sorted(set(obj) - set(props))
            if extra:
                err.append(f"schema: {path} 多余字段 {extra}")
        for k, v in obj.items():
            if k in props:
                err.extend(check_schema_lite(v, schema, props[k], f"{path}.{k}"))
    return err




def discover() -> list[Path]:
    return sorted((ROOT / "log-model" / "examples").rglob("*.expected-sdm-event.behavior.json"))


def mapping_path(event_path: Path) -> Path:
    return event_path.with_name(
        event_path.name.replace(".expected-sdm-event.behavior.json", ".wpl-to-sdm-event.behavior.json")
    )


def validate_one(path: Path, schema: dict, fields: dict, ident_map: dict | None = None) -> list[str]:
    event = json.loads(path.read_text(encoding="utf-8"))
    errors: list[str] = []
    try:
        import jsonschema
        validator = jsonschema.Draft202012Validator(schema)
        for e in validator.iter_errors(event):
            errors.append(f"schema: {e.message} @ {list(e.absolute_path)}")
    except ImportError:
        errors.extend(check_schema_lite(event, schema))
    errors.extend(check(event, fields, ident_map))
    mp = mapping_path(path)
    if mp.is_file():
        mapping = json.loads(mp.read_text(encoding="utf-8"))
        errors.extend(check_mapping(event, mapping))
    return errors


def main(argv: list[str]) -> int:
    fields = json.loads(FIELDS.read_text(encoding="utf-8"))
    if len(argv) >= 2 and argv[1] == "--self-test":
        return self_test(fields)
    if len(argv) == 1:
        paths = discover()
        if not paths:
            print("no *.expected-sdm-event.behavior.json under log-model/examples", file=sys.stderr)
            return 2
    else:
        paths = [Path(a) for a in argv[1:]]

    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    rc = 0
    ident_map: dict = {}  # 批量模式跨事件：同一实体 ref_id 必须稳定
    for path in paths:
        errors = validate_one(path, schema, fields, ident_map)
        schema_failed = any(x.startswith("schema:") for x in errors)
        schema_status = "failed" if schema_failed else "passed"
        semantic = "failed" if errors else "passed"
        print(f"{path}: logical_schema={schema_status} semantic_review={semantic}")
        for e in errors:
            print(f"  - {e}")
        if errors:
            rc = 1
    return rc


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
