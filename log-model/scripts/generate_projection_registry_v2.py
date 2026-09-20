#!/usr/bin/env python3
"""Generate projection-registry.v2.json from object-registry.v2 alias_map.

Physical columns, types, keys and the target table stay exactly as v1
(hybrid-v1, 62 columns + 4 VARIANT). Logical re-anchoring sources:
  1. pending_column_routing — unambiguous write → re-anchor; None/split/when → pending
  2. alias_map for everything else

A column is `re-anchored` only when the target path is in logical_paths.
Facet members stay `facet-open`.
"""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HYBRID = ROOT / "log-model" / "contracts" / "hybrid-event"
V1 = HYBRID / "projection-registry.v1.json"
REGV2 = HYBRID / "object-registry.v2.json"
OUT = HYBRID / "projection-registry.v2.json"

def pending_reasons(reg2: dict) -> dict[str, str]:
    out = {}
    for name, spec in (reg2.get("pending_column_routing") or {}).items():
        w = spec.get("write")
        if isinstance(w, str) and "." in w and not spec.get("when"):
            continue
        out[name] = spec["reason"]
    return out


def main() -> None:
    v1 = json.loads(V1.read_text(encoding="utf-8"))
    reg2 = json.loads(REGV2.read_text(encoding="utf-8"))
    known = set(reg2["logical_paths"])
    facet_domains = set(reg2["facet_domains"])
    force_pending = pending_reasons(reg2)
    alias = {}
    for a in reg2["v1_compatibility"]["alias_map"]:
        if "…" in a["new"] or "..." in a["new"]:
            raise SystemExit(f"placeholder alias leaked into projection: {a}")
        alias[a["old"]] = a
    unresolved_by_old = {u["old"]: u for u in reg2["v1_compatibility"]["unresolved"]}

    columns, pending = [], []
    for col in v1["columns"]:
        old_path = col["path"]
        name = col["column"]
        entry = dict(col)
        entry["path_v1"] = old_path

        if name in force_pending:
            entry["path"] = old_path
            entry["status"] = "pending"
            pending.append({"column": name, "path": old_path,
                            "reason": force_pending[name]})
            columns.append(entry)
            continue

        spec = alias.get(old_path)
        if spec is None:
            u = unresolved_by_old.get(old_path)
            entry["path"] = old_path
            entry["status"] = "pending"
            pending.append({
                "column": name, "path": old_path,
                "reason": (u["reason"] if u else
                           "v1 路径不在 alias_map，不得标 re-anchored"),
            })
            columns.append(entry)
            continue

        new_path = spec["new"]
        entry["path"] = new_path
        if new_path in known:
            entry["status"] = "re-anchored"
        elif new_path.startswith("facets."):
            dom = new_path.split(".")[1]
            if dom in facet_domains:
                entry["status"] = "facet-open"
            else:
                entry["status"] = "pending"
                pending.append({"column": name, "path": new_path,
                                "reason": "facet 域未登记"})
        else:
            entry["status"] = "pending"
            pending.append({
                "column": name, "path": new_path,
                "reason": "alias 目标不在 logical_paths，不得标 re-anchored",
            })
        columns.append(entry)

    by_path = defaultdict(list)
    for c in columns:
        if c["status"] == "re-anchored":
            by_path[c["path"]].append(c["column"])
    dual = [{"logical": k, "columns": v,
             "note": "同一逻辑源多物理列（interim 兼容）；M4 收敛到单列"}
            for k, v in sorted(by_path.items()) if len(v) > 1]

    leaked = [c["column"] for c in columns
              if c["status"] == "re-anchored" and c["path"] not in known]
    assert not leaked, leaked
    assert all(c["status"] != "re-anchored" or c["path_v1"] in alias
               for c in columns)

    registry = dict(v1)
    registry.update({
        "registry_version": 2,
        "projection_version": "hybrid-v2-logical (M2 draft)",
        "physical_layer": "unchanged from hybrid-v1 — DDL/列/键不动，cutover 归 M4",
        "alias_source": "object-registry.v2.json#v1_compatibility.alias_map",
        "variant_objects": {
            "roles_obj": {"logical": ["subject", "object", "carriers"],
                          "note": "旧 roles VARIANT 不拆列；M4 决定拆分或保留"},
            "facets_obj": {"logical": ["facets"]},
            "source_finding_obj": {"logical": ["observation.observer", "observation.assertion"],
                                   "note": "含 observer/evidence；M4 决定是否更名 observation_obj"},
            "extensions_obj": {"logical": ["extensions"]},
        },
        "columns": columns,
        "unresolved_projection": pending,
        "dual_projection_notes": dual,
        "cutover_notes": [
            {"columns": [name], "status": "pending", "note": reason}
            for name, reason in force_pending.items()
        ],
    })
    OUT.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n",
                   encoding="utf-8")

    n_ok = sum(1 for c in columns if c["status"] == "re-anchored")
    n_facet = sum(1 for c in columns if c["status"] == "facet-open")
    print(f"projection-registry.v2.json: {len(columns)} columns, "
          f"{n_ok} re-anchored, {n_facet} facet-open, {len(pending)} pending")
    for u in pending:
        print(f"  pending {u['column']} <- {u['path']}")


if __name__ == "__main__":
    main()
