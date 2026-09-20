#!/usr/bin/env python3
"""Generate the hybrid-v1 Kafka message Schema from the projection registry."""

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parent
REGISTRY = REPO / "log-model/contracts/hybrid-event/projection-registry.v1.json"
POLICY = REPO / "log-model/contracts/hybrid-event/version-policy.v1.json"
LOGICAL_SCHEMA = ROOT / "docs/main/05-sdm-event-logical.schema.json"
OUTPUT = ROOT / "docs/main/05-sdm-event-kafka-hybrid.schema.json"


def nullable(schema):
    return {"oneOf": [schema, {"type": "null"}]}


def string_schema(max_length):
    return {"type": "string", "maxLength": max_length}


def column_schema(column, allow_null=True):
    data_type = column["type"]
    if data_type == "INT":
        base = {"type": "integer"}
    elif data_type == "DATETIME(3)":
        base = {
            "oneOf": [
                {"type": "integer", "minimum": 0, "description": "Unix epoch milliseconds"},
                {"type": "string", "format": "date-time"},
            ]
        }
    else:
        match = re.fullmatch(r"VARCHAR\((\d+)\)", data_type)
        if not match:
            raise ValueError(f"Unsupported registry type: {data_type}")
        base = string_schema(int(match.group(1)))
    base["description"] = f"投影自 {column['path']}；{column['projection']}"
    return nullable(base) if allow_null else base


def object_schema(logical_name, physical_name, allow_null):
    canonical = {
        "$ref": f"05-sdm-event-logical.schema.json#/properties/{logical_name}"
    }
    overflow = {
        "type": "object",
        "additionalProperties": False,
        "required": ["$ref", "byte_size"],
        "properties": {
            "$ref": {"type": "string", "pattern": "^overflow://"},
            "byte_size": {"type": "integer", "minimum": 1},
        },
    }
    choices = [canonical, overflow]
    if allow_null:
        choices.append({"type": "null"})
    return {
        "oneOf": choices,
        "description": f"{logical_name} 的权威物理对象列 {physical_name}",
    }


def main():
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    policy = json.loads(POLICY.read_text(encoding="utf-8"))
    if not LOGICAL_SCHEMA.exists():
        raise FileNotFoundError(f"Generate logical schema first: {LOGICAL_SCHEMA}")

    non_nullable = {
        name
        for name, rule in registry["projection_rules"]["by_column"].items()
        if rule.get("nullable") is False
    }
    properties = {
        column["column"]: column_schema(
            column,
            allow_null=column["column"] not in non_nullable,
        )
        for column in registry["columns"]
    }
    for logical_name, config in registry["variant_objects"].items():
        physical_name = config["physical_column"]
        properties[physical_name] = object_schema(
            logical_name,
            physical_name,
            allow_null=logical_name == "source_finding",
        )

    properties["schema_version"] = {
        "enum": policy["schema_versions"],
        "description": "允许的 Kafka 事件 Schema 版本",
    }
    for identity in ("tenant_id", "event_id", "mapping_id"):
        properties[identity]["minLength"] = 1

    object_columns = [
        value["physical_column"]
        for value in registry["variant_objects"].values()
    ]
    required = sorted(non_nullable | set(object_columns))
    aliases = sorted(alias["legacy_column"] for alias in registry["aliases"])
    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://sdm2.local/interim/schemas/sdm-event-kafka-hybrid.schema.json",
        "title": "SDM2.0 Hybrid-v1 Kafka Event",
        "description": (
            "Kafka 写入 sdm_event_target 的混合物理行。顶层为热检索投影，"
            "四个 *_obj 字段保存权威逻辑对象。"
        ),
        "type": "object",
        "additionalProperties": False,
        "required": required,
        "properties": properties,
        "x-sdm2-contract": {
            "status": "interim",
            "target_table": registry["target_table"],
            "projection_version": registry["projection_version"],
            "projection_registry_version": registry["registry_version"],
            "canonical_scalar_count": len(registry["columns"]),
            "canonical_object_count": len(object_columns),
            "forbidden_legacy_aliases": aliases,
            "logical_schema": "05-sdm-event-logical.schema.json",
        },
    }
    OUTPUT.write_text(json.dumps(schema, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        f"wrote {OUTPUT} with {len(registry['columns'])} scalar columns "
        f"and {len(object_columns)} object columns"
    )


if __name__ == "__main__":
    main()
