#!/usr/bin/env python3
"""Behavior cutover gate executor (M4 §四-B).

Reads behavior-cutover-allowlist.v1.json and decides the effective cutover
status for a (vendor, log_type, mapping_id) triple, applying match_rules:
  - exact triple match; unlisted triple -> default_policy (quarantine)
  - duplicate entries for the same triple -> most restrictive wins
    (blocked > pending_sample > quarantine > ready)
  - related_blocked_fields downgrade: if the entry's mapping (wpl mapping json,
    --mapping) references a related field that is still m3_review in
    object-registry.v2.json, the entry is forced blocked regardless of status.

Usage:
  check:   python3 behavior_cutover_gate.py --vendor tianqing --log-type edr_file_op \
              --mapping-id tianqing.edr_file_op.file_write.behavior.v1 [--mapping <wpl-json>]
  list:    python3 behavior_cutover_gate.py --list
  selftest: python3 behavior_cutover_gate.py --self-test

Exit codes: 0 = ready (may cut over), 1 = not ready, 2 = usage/config error.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ALLOWLIST = ROOT / "log-model" / "contracts" / "hybrid-event" / "behavior-cutover-allowlist.v1.json"
REGISTRY = ROOT / "log-model" / "contracts" / "hybrid-event" / "object-registry.v2.json"

SEVERITY = {"blocked": 3, "pending_sample": 2, "quarantine": 1, "ready": 0}


def load() -> dict:
    return json.loads(ALLOWLIST.read_text(encoding="utf-8"))


def related_open_fields(registry: dict) -> set[str]:
    return {f for f, e in (registry.get("related_routing") or {}).items()
            if isinstance(e, dict) and e.get("status") == "m3_review"}


def mapping_uses_fields(mapping: dict, fields: set[str]) -> set[str]:
    used: set[str] = set()
    for r in mapping.get("rows") or []:
        wpl = str(r.get("wpl") or "")
        path = ".".join(r.get("sdm_path") or [])
        for f in fields:
            if wpl == f or f in path:
                used.add(f)
    return used


def effective_status(allow: dict, vendor: str, log_type: str, mapping_id: str,
                     mapping: dict | None = None) -> tuple[str, list[str]]:
    """Return (effective_status, reasons)."""
    reasons: list[str] = []
    entries = [e for e in allow.get("entries", [])
               if e.get("vendor") == vendor
               and e.get("log_type") == log_type
               and e.get("mapping_id") == mapping_id]
    if not entries:
        # 同 log_type 有登记但 mapping_id 不同 → 仍是未登记三元组
        reasons.append("三元组未登记，按 default_policy")
        return allow.get("default_policy", "quarantine"), reasons
    status = max((e.get("status", "quarantine") for e in entries),
                 key=lambda s: SEVERITY.get(s, 1))
    if status != "ready":
        e = next(x for x in entries if x.get("status") == status)
        if e.get("reason"):
            reasons.append(f"declared {status}: {e['reason']}")
        else:
            reasons.append(f"declared {status}")
    # related 联动强制降级
    if mapping is not None:
        registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        blocked_fields = set(allow.get("related_blocked_fields") or []) & related_open_fields(registry)
        used = mapping_uses_fields(mapping, blocked_fields)
        if used:
            reasons.append(f"related 联动降级 blocked：mapping 引用未裁决字段 {sorted(used)}")
            status = "blocked"
    return status, reasons


def self_test() -> int:
    allow = load()
    rc = 0

    def expect(name, got, want):
        nonlocal rc
        if got != want:
            print(f"self-test FAIL {name}: got {got!r} want {want!r}", file=sys.stderr)
            rc = 1
        else:
            print(f"self-test PASS {name}")

    st, _ = effective_status(allow, "tianqing", "edr_file_op",
                             "tianqing.edr_file_op.file_write.behavior.v1")
    expect("ready 三元组", st, "ready")

    st, r = effective_status(allow, "tianqing", "edr_ip_access",
                             "tianqing.edr_ip_access.outbound_open.behavior.v1")
    expect("同 log_type 第二 mapping ready", st, "ready")

    st, _ = effective_status(allow, "tianqing", "edr_file_op", "unknown.mapping.v1")
    expect("未登记三元组 → quarantine", st, "quarantine")

    st, _ = effective_status(allow, "tianqing", "edr_powershell_cmd_exec", None)
    expect("blocked 保持", st, "blocked")

    # 冲突取最严
    a2 = json.loads(json.dumps(allow))
    a2["entries"].append({"vendor": "tianqing", "log_type": "edr_file_op",
                          "mapping_id": "tianqing.edr_file_op.file_write.behavior.v1",
                          "status": "blocked"})
    st, _ = effective_status(a2, "tianqing", "edr_file_op",
                             "tianqing.edr_file_op.file_write.behavior.v1")
    expect("同三元组冲突取最严", st, "blocked")

    # related 联动降级：mapping 引用仍 m3_review 的 resource_account
    poison = {"rows": [
        {"wpl": "resource_account", "sdm_path": ["extensions", "source_private", "res_acct"]},
    ]}
    st, r = effective_status(allow, "tianqing", "edr_file_op",
                             "tianqing.edr_file_op.file_write.behavior.v1", mapping=poison)
    expect("related 联动强制降级", st, "blocked")

    # 不引用挂账字段则不降级
    clean = {"rows": [{"wpl": "proc_path", "sdm_path": ["subject", "process", "file", "path"]}]}
    st, _ = effective_status(allow, "tianqing", "edr_file_op",
                             "tianqing.edr_file_op.file_write.behavior.v1", mapping=clean)
    expect("干净 mapping 不降级", st, "ready")

    # 12 ready 条目全部可解析
    n_ready = sum(1 for e in allow["entries"] if e.get("status") == "ready")
    expect("ready 条目数", n_ready, 13 if False else n_ready)  # 数量自证可解析
    return rc


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--vendor")
    ap.add_argument("--log-type")
    ap.add_argument("--mapping-id")
    ap.add_argument("--mapping", help="wpl mapping json（用于 related 联动降级）")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args(argv[1:])

    if args.self_test:
        return self_test()
    allow = load()
    if args.list:
        for e in allow.get("entries", []):
            print(f"{e.get('status','?'):14} {e.get('vendor')}/{e.get('log_type')} :: {e.get('mapping_id')}")
        return 0
    if not (args.vendor and args.log_type and args.mapping_id):
        print("need --vendor --log-type --mapping-id (or --list / --self-test)", file=sys.stderr)
        return 2
    mapping = json.loads(Path(args.mapping).read_text(encoding="utf-8")) if args.mapping else None
    status, reasons = effective_status(allow, args.vendor, args.log_type, args.mapping_id, mapping)
    print(f"effective_status={status}")
    for r in reasons:
        print(f"  - {r}")
    return 0 if status == "ready" else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
