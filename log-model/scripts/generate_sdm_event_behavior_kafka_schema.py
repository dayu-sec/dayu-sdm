#!/usr/bin/env python3
"""Generate the sdm-event-behavior Kafka message Schema from 07.

Tree and field names stay identical to the logical envelope. Only the three
meta timestamps that 032 consumes are rewritten to unix-millisecond integers.
"""

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LOGICAL = ROOT / "docs/main/07-sdm-event-behavior.schema.json"
OUTPUT = ROOT / "docs/main/07-sdm-event-behavior-kafka.schema.json"

TIME_FIELDS = ("occur_time", "ingest_time", "parse_time")


def unix_ms(description: str, required: bool) -> dict:
    schema = {
        "type": "integer" if required else ["integer", "null"],
        "minimum": 0,
        "description": f"{description}。Kafka 物理编码：unix 毫秒 UTC；逻辑契约 07 为 date-time。",
    }
    return schema


def patch_meta_times(schema: dict) -> None:
    meta_props = schema["properties"]["meta"]["properties"]
    required = set(schema["properties"]["meta"]["required"])
    for name in TIME_FIELDS:
        original = meta_props[name]
        meta_props[name] = unix_ms(original["description"].rstrip("。"), name in required)


def build() -> dict:
    schema = copy.deepcopy(json.loads(LOGICAL.read_text(encoding="utf-8")))
    schema["$id"] = "https://sdm2.local/schemas/sdm-event-behavior-kafka.schema.json"
    schema["title"] = "SDM2.0 Behavior Event Kafka Message"
    schema["description"] = (
        "Kafka 写入 sdm_event_behavior 的消息。树形与 07 逻辑信封相同；"
        "仅 meta.occur_time / ingest_time / parse_time 为 unix 毫秒整数。"
        "单对象 JSON（strip_outer_array=false），不得包数组。"
        "暂缓字段与 07 相同，不得出现。"
    )
    patch_meta_times(schema)
    schema["x-sdm2-contract"] = {
        "status": "2.0",
        "target_table": "sdm_event_behavior",
        "logical_schema": "07-sdm-event-behavior.schema.json",
        "routine_load": "schema/032_routine_load_sdm_event_behavior.sql",
        "message_shape": "single_object",
        "strip_outer_array": False,
        "time_encoding": "unix_ms",
        "time_fields": [
            "meta.occur_time",
            "meta.ingest_time",
            "meta.parse_time",
        ],
        "forbidden_legacy_roots": [
            "tenant_id",
            "roles",
            "roles_obj",
            "facets_obj",
            "source_finding",
            "source_finding_obj",
            "extensions_obj",
            "severity",
            "mapping_revision",
            "projection_version",
            "quality_status",
        ],
    }
    return schema


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="verify committed schema is current")
    args = parser.parse_args()
    schema = build()
    text = json.dumps(schema, ensure_ascii=False, indent=2) + "\n"
    if args.check:
        current = OUTPUT.read_text(encoding="utf-8")
        if current != text:
            raise SystemExit(f"{OUTPUT} is stale; rerun without --check")
        return
    OUTPUT.write_text(text, encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT.parent)}")


if __name__ == "__main__":
    main()
