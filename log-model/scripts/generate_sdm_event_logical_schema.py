#!/usr/bin/env python3
"""Generate the interim SDM2.0 logical event JSON Schema from its field catalog."""

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "docs/main/05-sdm-event-logical-field-catalog.md"
OUTPUT = ROOT / "docs/main/05-sdm-event-logical.schema.json"
ROW = re.compile(
    r"^\|\s*\d+\s*\|\s*`[^`]+`\s*\|\s*`(?P<path>[^`]+)`\s*\|"
    r"\s*`(?P<type>[^`]+)`\s*\|[^|]*\|\s*(?P<required>[YN])\s*\|"
    r"\s*`(?P<example>[^`]*)`\s*\|\s*(?P<description>.*?)\s*\|$"
)


class Node:
    def __init__(self):
        self.children = {}
        self.array = False
        self.leaf_schema = None
        self.item_leaf_schema = None
        self.required = False


def scalar_schema(type_name, description=None):
    mapping = {
        "string": {"type": "string"},
        "string(datetime)": {"type": "string", "format": "date-time"},
        "integer": {"type": "integer"},
        "number": {"type": "number"},
        "boolean": {"type": "boolean"},
    }
    schema = dict(mapping[type_name])
    if description:
        schema["description"] = description
    return schema


def value_schema(type_name, description):
    if type_name.startswith("array<") and type_name.endswith(">"):
        item_type = type_name[6:-1]
        return {
            "type": "array",
            "items": scalar_schema(item_type),
            "description": description,
        }
    return scalar_schema(type_name, description)


def add_path(root, path, type_name, required, description):
    parts = path.split(".")
    node = root
    traversed = []
    for index, raw_part in enumerate(parts):
        is_array = raw_part.endswith("[]")
        part = raw_part[:-2] if is_array else raw_part
        child = node.children.setdefault(part, Node())
        child.array = child.array or is_array
        traversed.append(child)
        node = child
        if index == len(parts) - 1:
            if is_array:
                item_type = type_name[6:-1] if type_name.startswith("array<") else type_name
                node.item_leaf_schema = scalar_schema(item_type, description)
            else:
                node.leaf_schema = value_schema(type_name, description)
    if required:
        for item in traversed:
            item.required = True


def object_schema(node):
    properties = {name: emit(child) for name, child in sorted(node.children.items())}
    schema = {
        "type": "object",
        "additionalProperties": False,
        "properties": properties,
    }
    required = sorted(name for name, child in node.children.items() if child.required)
    if required:
        schema["required"] = required
    return schema


def emit(node):
    object_value = object_schema(node) if node.children else None

    if node.array:
        variants = []
        if node.item_leaf_schema:
            variants.append({"type": "array", "items": node.item_leaf_schema})
        if object_value:
            variants.append({"type": "array", "items": object_value})
        if node.leaf_schema:
            variants.insert(0, node.leaf_schema)
        return variants[0] if len(variants) == 1 else {"oneOf": variants}

    if node.leaf_schema and object_value:
        return {"oneOf": [node.leaf_schema, object_value]}
    if node.leaf_schema:
        return node.leaf_schema
    if object_value:
        return object_value
    raise ValueError("Empty schema node")


def load_catalog():
    rows = []
    for line in CATALOG.read_text(encoding="utf-8").splitlines():
        match = ROW.match(line)
        if not match:
            continue
        rows.append(match.groupdict())
    if len(rows) != 504:
        raise ValueError(f"Expected 504 catalog rows, found {len(rows)}")
    return rows


def main():
    tree = Node()
    for row in load_catalog():
        add_path(
            tree,
            row["path"],
            row["type"],
            row["required"] == "Y",
            row["description"],
        )

    generated = object_schema(tree)
    properties = {
        "schema_version": {
            "type": "integer",
            "const": 1,
            "description": "逻辑事件根结构版本",
        },
        **generated["properties"],
        "extensions": {
            "type": "object",
            "additionalProperties": False,
            "required": ["schema_version", "source_private", "profiles", "enrichments", "unmapped"],
            "properties": {
                "schema_version": {"type": "integer", "const": 1},
                "source_private": {"type": "object", "additionalProperties": True},
                "profiles": {"type": "object", "additionalProperties": True},
                "enrichments": {"type": "object", "additionalProperties": True},
                "unmapped": {"type": "object", "additionalProperties": True},
            },
        },
    }
    properties["roles"]["required"] = ["source", "carriers", "target", "observer", "related"]

    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://sdm2.local/interim/schemas/sdm-event-logical.schema.json",
        "title": "SDM2.0 Interim Logical Event",
        "description": (
            "由 object-registry.v1 registry v22 与 05-sdm-event-logical-field-catalog.md "
            "生成的中间版本逻辑事件 Schema。"
        ),
        "type": "object",
        "additionalProperties": False,
        "required": ["schema_version", "metadata", "event", "roles", "facets", "extensions"],
        "properties": properties,
        "x-sdm2-contract": {
            "status": "interim",
            "logical_leaf_path_count": 504,
            "object_registry_version": 22,
            "catalog": "05-sdm-event-logical-field-catalog.md",
            "base_schema": "log-model/contracts/schemas/sdm-event-logical.schema.json",
            "excluded_governance_paths": [],
        },
    }
    OUTPUT.write_text(json.dumps(schema, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT} from 504 logical paths")


if __name__ == "__main__":
    main()
