#!/usr/bin/env python3
"""Validate candidate expected events against the interim 55-col table.

87-col-only leftover keys are reported as PARTIAL (they belong in VARIANT
object columns). Unknown keys outside both contracts are errors.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
# 002_sdm_event.sql (raw_msg inline column era) was retired 2026-08-26; the
# projection registry is the authoritative physical shape now.
LEGACY_FIELDS = ROOT / "log-model/contracts/hybrid-event/projection-registry.v1.json"
ENUMS = ROOT / "log-model/contracts/event_operation_dictionary.json"
DICT = ROOT / "log-model/contracts/event_operation_dictionary.json"
REGISTRY = ROOT / "log-model/contracts/hybrid-event/projection-registry.v1.json"
def interim_columns() -> set[str]:
    registry = json.loads(REGISTRY.read_text())
    columns = {
        entry["column"]
        for entry in registry.get("columns") or []
        if isinstance(entry, dict) and isinstance(entry.get("column"), str)
    }
    for spec in (registry.get("variant_objects") or {}).values():
        if isinstance(spec, dict) and isinstance(spec.get("physical_column"), str):
            columns.add(spec["physical_column"])
    return columns


def legacy_columns() -> set[str]:
    return set(re.findall(r"^- name: ([A-Za-z0-9_]+)$", LEGACY_FIELDS.read_text(), re.M))


def alias_columns() -> set[str]:
    registry = json.loads(REGISTRY.read_text())
    return {
        entry["legacy_column"]
        for entry in registry.get("aliases") or []
        if isinstance(entry, dict) and isinstance(entry.get("legacy_column"), str)
    }


def registry_columns() -> set[str]:
    registry = json.loads(REGISTRY.read_text())
    return {
        entry["column"]
        for entry in registry.get("columns") or []
        if isinstance(entry, dict) and isinstance(entry.get("column"), str)
    }

def enum_values(column: str) -> set[str]:
    text = ENUMS.read_text()
    match = re.search(
        rf"- column: {column}\n(?:(?!\n  - column:).)*?values: \[([^]]+)\]",
        text,
        re.S,
    )
    return {item.strip() for item in match.group(1).split(",")} if match else set()


def valid_event_types() -> set[str]:
    dictionary = json.loads(DICT.read_text())
    out: set[str] = set()
    for row in dictionary.get("mapping_rules") or []:
        if str(row.get("status") or "").upper() == "DEPRECATED":
            continue
        out.update(row.get("event_types") or [])
    return out


def main(args: list[str]) -> int:
    interim = interim_columns()
    allowed = interim | alias_columns()
    omitted = (legacy_columns() | registry_columns()) - allowed
    enums = {name: enum_values(name) for name in ("event_category", "outcome", "severity")}
    event_types = valid_event_types()
    paths: list[Path] = []
    for raw in args:
        path = Path(raw)
        paths += list(path.rglob("*.expected-sdm-event.json")) if path.is_dir() else [path]
    errors: list[str] = []
    partial: list[str] = []
    for path in paths:
        data = json.loads(path.read_text())
        unknown = sorted(set(data) - allowed)
        leftover = [name for name in unknown if name in omitted]
        unexpected = [name for name in unknown if name not in omitted]
        if unexpected:
            errors.append(f"{path}: unknown physical fields {unexpected}")
        if leftover:
            partial.append(
                f"{path}: keys omitted from interim 002 (move into VARIANT): {leftover}"
            )

        for key, values in enums.items():
            value = data.get(key)
            if value not in (None, "") and values and value not in values:
                errors.append(f"{path}: invalid {key}={value}")
        event_type = data.get("event_type")
        if event_types and event_type not in event_types:
            errors.append(f"{path}: invalid event_type={event_type}")
        if data.get("tenant_id") != "":
            errors.append(f"{path}: candidate tenant_id must be empty")
        if not data.get("event_id"):
            errors.append(f"{path}: missing event_id")
        if not data.get("occur_time"):
            partial.append(f"{path}: occur_time unavailable from WPL output")
    for item in errors:
        print("ERROR:", item)
    for item in partial:
        print("PARTIAL:", item)
    print(f"fixtures={len(paths)} errors={len(errors)} partial={len(partial)}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
