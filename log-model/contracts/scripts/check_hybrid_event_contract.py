"""Validate SDM2.0 hybrid-event Schema, registries, aliases, and fixtures."""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

from check_contracts import ValidationError, load_schema, validate_instance

REPO_ROOT = Path(__file__).resolve().parents[3]
CONTRACT_ROOT = REPO_ROOT / "log-model/contracts/hybrid-event"
LIVE_SCHEMAS_DIR = REPO_ROOT / "log-model/contracts/schemas"





REGISTRY_PATH = CONTRACT_ROOT / "projection-registry.v1.json"
OBJECT_REGISTRY_PATH = CONTRACT_ROOT / "object-registry.v1.json"
PROFILE_REGISTRY_PATH = CONTRACT_ROOT / "profile-registry.v1.json"
VERSION_POLICY_PATH = CONTRACT_ROOT / "version-policy.v1.json"
FIXTURES_DIR = CONTRACT_ROOT / "fixtures"
PROJECTION_TYPES = {"DIRECT", "NORMALIZED", "DERIVED", "PRIMARY_ONLY", "REFERENCE_ONLY", "NOT_PROJECTED", "DETAIL"}
ACCESS_TYPES = {"KEY", "LOOKUP", "DIMENSION", "MEASURE", "DETAIL", "SPARSE", "RELATION", "RAW_REFERENCE"}
VERSION_RE = re.compile(r"^[A-Za-z0-9._-]+$")
REQUIRED_MULTI_OBJECT_PATHS = {
    "roles.related[].ref_id",
    "roles.related[].entity_type",
    "roles.related[].relation_type",
    "roles.related[].endpoint.ip",
    "roles.related[].host.id",
    "roles.related[].file.hashes.sha256",
    "source_finding.entities.attackers[].ref_id",
    "source_finding.entities.victims[].ref_id",
    "source_finding.entities.affected[].ref_id",
    "source_finding.indicators[].type",
    "source_finding.indicators[].value",
    "source_finding.rules[].id",
    "source_finding.rules[].signature_id",
}
RESOURCE_FIELDS = (
    "id", "name", "type", "subtype", "vendor", "product", "external_id",
    "group.id", "group.name",
)
RESOURCE_ROLE_PATHS = (
    "roles.source", "roles.carriers[]", "roles.target", "roles.observer", "roles.related[]",
)
REQUIRED_MULTI_OBJECT_PATHS.update(
    f"{role}.resource.{field}"
    for role in RESOURCE_ROLE_PATHS
    for field in RESOURCE_FIELDS
)
REQUIRED_MULTI_OBJECT_PATHS.update({
    "source_finding.window.start_time",
    "source_finding.window.end_time",
    "source_finding.window.duration_ms",
    "facets.network.scan.type",
    "facets.network.scan.method",
    "facets.network.scan.ports[]",
    "facets.network.scan.port_count",
    "facets.network.scan.target_count",
    "facets.network.scan.interval_ms",
    "facets.network.traffic.total_bytes",
    "facets.network.traffic.total_packets",
    "facets.network.traffic.bytes_in",
    "facets.network.traffic.bytes_out",
    "facets.network.traffic.packets_in",
    "facets.network.traffic.packets_out",
    "facets.network.traffic.rate.value",
    "facets.network.traffic.rate.unit",
    "facets.network.traffic.interval_ms",
    "roles.related[].device.id",
    "roles.related[].device.name",
    "roles.related[].device.type",
    "roles.related[].device.vendor",
    "roles.related[].device.model",
    "roles.related[].device.serial_number",
    "roles.related[].device.instance_path",
    "roles.related[].device.vendor_id",
    "roles.related[].device.product_id",
})
RELATED_ENTITY_SLOTS = {
    "user", "account", "host", "endpoint", "process", "file", "service",
    "domain", "url", "device", "resource", "application", "cloud", "container", "certificate",
}
REQUIRED_ENDPOINT_ASSET_PROFILE_PATHS = {
    "extensions.profiles.endpoint_asset.subject_ref.ref_id",
    "extensions.profiles.endpoint_asset.asset.type",
    "extensions.profiles.endpoint_asset.asset.category",
    "extensions.profiles.endpoint_asset.asset.criticality",
    "extensions.profiles.endpoint_asset.agent.id",
    "extensions.profiles.endpoint_asset.agent.fingerprint_id",
    "extensions.profiles.endpoint_asset.agent.version",
    "extensions.profiles.endpoint_asset.agent.install_time",
    "extensions.profiles.endpoint_asset.agent.status",
    "extensions.profiles.endpoint_asset.ownership.organization.id",
    "extensions.profiles.endpoint_asset.ownership.organization.name",
    "extensions.profiles.endpoint_asset.ownership.group.id",
    "extensions.profiles.endpoint_asset.ownership.group.name",
    "extensions.profiles.endpoint_asset.ownership.owner.id",
    "extensions.profiles.endpoint_asset.ownership.owner.name",
    "extensions.profiles.endpoint_asset.lifecycle.first_seen_time",
    "extensions.profiles.endpoint_asset.lifecycle.last_seen_time",
    "extensions.profiles.endpoint_asset.lifecycle.status",
    "extensions.profiles.endpoint_asset.lifecycle.status_time",
}


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"{path}: root must be an object")
    return value


def validate_limits(limits: Any, label: str) -> list[str]:
    errors: list[str] = []
    required = {"roles", "facets", "source_finding", "extensions", "combined"}
    if not isinstance(limits, dict):
        return [f"{label}: limits_bytes must be an object"]
    if set(limits) != required:
        errors.append(f"{label}: limits_bytes keys must equal {sorted(required)}")
    for name, value in limits.items():
        if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
            errors.append(f"{label}: limit {name!r} must be a positive integer")
    if not errors:
        object_limits = [limits[name] for name in required - {"combined"}]
        if limits["combined"] < max(object_limits) or limits["combined"] > sum(object_limits):
            errors.append(f"{label}: combined limit must be between max(object limits) and their sum")
    return errors


def validate_object_registry(object_registry: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    version = object_registry.get("registry_version")
    if isinstance(version, bool) or not isinstance(version, int) or version < 1:
        errors.append("object registry version must be a positive integer")
    related = (object_registry.get("roles") or {}).get("related") or {}
    if related.get("cardinality") != "many":
        errors.append("roles.related cardinality must equal many")
    array_reference = object_registry.get("array_reference") or {}
    if array_reference.get("field") != "ref_id" or not array_reference.get("pattern"):
        errors.append("array_reference must define the stable ref_id field and pattern")

    paths = object_registry.get("logical_paths")
    if not isinstance(paths, list) or not paths:
        return errors + ["object registry logical_paths must be a non-empty array"]
    invalid = [path for path in paths if not isinstance(path, str) or not path]
    if invalid:
        errors.append("object registry logical_paths must contain non-empty strings")
    if len(paths) != len(set(str(path) for path in paths)):
        errors.append("object registry logical_paths must not contain duplicates")
    missing = sorted(REQUIRED_MULTI_OBJECT_PATHS - set(paths))
    if missing:
        errors.append(f"object registry missing multi-object paths: {missing}")
    return errors


def validate_profile_registry(profile_registry: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if profile_registry.get("registry_version") != 2:
        errors.append("profile registry version must equal 2")
    profile = (profile_registry.get("profiles") or {}).get("endpoint_asset") or {}
    if profile.get("profile_id") != "endpoint_asset":
        errors.append("endpoint_asset profile_id must equal endpoint_asset")
    if profile.get("logical_path") != "extensions.profiles.endpoint_asset":
        errors.append("endpoint_asset logical_path is not canonical")
    if profile.get("schema_ref") != "#/$defs/endpoint_asset_profile":
        errors.append("endpoint_asset schema_ref must target the logical event Schema definition")
    subject = profile.get("subject") or {}
    expected_subject = {
        "entity_types": ["host"],
        "roles": ["source", "target", "related"],
        "reference_field": "ref_id",
        "require_resolvable": True,
    }
    if subject != expected_subject:
        errors.append("endpoint_asset subject must be a resolvable host in source, target, or related")
    paths = profile.get("logical_paths")
    if not isinstance(paths, list) or set(paths) != REQUIRED_ENDPOINT_ASSET_PROFILE_PATHS:
        errors.append("endpoint_asset logical_paths must equal the governed v2 Profile paths")
    elif len(paths) != len(set(paths)):
        errors.append("endpoint_asset logical_paths must not contain duplicates")
    merge = profile.get("snapshot_merge") or {}
    if (
        merge.get("semantics") != "event_snapshot"
        or merge.get("ordering_field") != "metadata.occur_time"
        or merge.get("field_strategy") != "latest_non_null"
        or merge.get("absence_means_delete") is not False
    ):
        errors.append("endpoint_asset snapshot_merge policy is not canonical")
    return errors


def parse_iso_timestamp(raw: Any, path: str, errors: list[str]) -> datetime | None:
    if raw is None:
        return None
    try:
        return datetime.fromisoformat(str(raw).replace("Z", "+00:00"))
    except ValueError:
        errors.append(f"{path}: invalid ISO-8601 timestamp {raw!r}")
        return None


def validate_multi_object_semantics(value: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    related = ((value.get("roles") or {}).get("related") or [])
    related_by_ref: dict[str, dict[str, Any]] = {}
    for index, member in enumerate(related):
        if not isinstance(member, dict) or "ref_id" not in member:
            continue
        ref_id = str(member["ref_id"])
        if ref_id in related_by_ref:
            errors.append(f"/roles/related/{index}/ref_id: duplicate ref_id {ref_id!r}")
            continue
        related_by_ref[ref_id] = member
        entity_type = member.get("entity_type")
        populated_slots = sorted(slot for slot in RELATED_ENTITY_SLOTS if member.get(slot) is not None)
        if populated_slots != [entity_type]:
            errors.append(
                f"/roles/related/{index}: entity_type {entity_type!r} must match exactly one populated entity slot; got {populated_slots}"
            )
        if entity_type == "resource" and isinstance(member.get("resource"), dict):
            resource = member["resource"]
            identities = (resource.get("id"), resource.get("name"), resource.get("external_id"))
            if not any(isinstance(item, str) and item.strip() for item in identities):
                errors.append(
                    f"/roles/related/{index}/resource: canonical resource requires id, name, or external_id"
                )

    entities = ((value.get("source_finding") or {}).get("entities") or {})
    for group in ("attackers", "victims", "affected"):
        for index, reference in enumerate(entities.get(group) or []):
            if not isinstance(reference, dict):
                continue
            ref_id = reference.get("ref_id")
            target = related_by_ref.get(str(ref_id))
            path = f"/source_finding/entities/{group}/{index}"
            if target is None:
                errors.append(f"{path}/ref_id: unresolved related ref_id {ref_id!r}")
                continue
            declared_type = reference.get("entity_type")
            if declared_type is not None and declared_type != target.get("entity_type"):
                errors.append(
                    f"{path}/entity_type: {declared_type!r} does not match related entity_type {target.get('entity_type')!r}"
                )

    window = ((value.get("source_finding") or {}).get("window") or {})
    parsed_times: dict[str, datetime] = {}
    for field in ("start_time", "end_time"):
        raw_time = window.get(field)
        parsed = parse_iso_timestamp(raw_time, f"/source_finding/window/{field}", errors)
        if parsed is not None:
            parsed_times[field] = parsed
    if set(parsed_times) == {"start_time", "end_time"}:
        try:
            if parsed_times["start_time"] > parsed_times["end_time"]:
                errors.append("/source_finding/window: start_time must not occur after end_time")
        except TypeError:
            errors.append("/source_finding/window: start_time and end_time must use compatible timezone forms")

    profile = ((((value.get("extensions") or {}).get("profiles") or {}).get("endpoint_asset")) or {})
    if profile:
        subject = profile.get("subject_ref") or {}
        subject_ref = subject.get("ref_id")
        matches: list[dict[str, Any]] = []
        roles = value.get("roles") or {}
        for role in ("source", "target"):
            candidate = roles.get(role) or {}
            if candidate.get("ref_id") == subject_ref and candidate.get("host") is not None:
                matches.append(candidate)
        matches.extend(
            candidate for candidate in (roles.get("related") or [])
            if isinstance(candidate, dict)
            and candidate.get("ref_id") == subject_ref
            and candidate.get("entity_type") == "host"
            and candidate.get("host") is not None
        )
        if len(matches) != 1:
            errors.append(
                "/extensions/profiles/endpoint_asset/subject_ref: must resolve to exactly one event host"
            )

        profile_times: dict[str, datetime] = {}
        agent = profile.get("agent") or {}
        lifecycle = profile.get("lifecycle") or {}
        time_values = {
            "agent/install_time": agent.get("install_time"),
            "lifecycle/first_seen_time": lifecycle.get("first_seen_time"),
            "lifecycle/last_seen_time": lifecycle.get("last_seen_time"),
            "lifecycle/status_time": lifecycle.get("status_time"),
        }
        for field, raw_time in time_values.items():
            parsed = parse_iso_timestamp(
                raw_time, f"/extensions/profiles/endpoint_asset/{field}", errors
            )
            if parsed is not None:
                profile_times[field] = parsed
        first_seen = profile_times.get("lifecycle/first_seen_time")
        last_seen = profile_times.get("lifecycle/last_seen_time")
        if first_seen is not None and last_seen is not None:
            try:
                if first_seen > last_seen:
                    errors.append(
                        "/extensions/profiles/endpoint_asset/lifecycle: first_seen_time must not occur after last_seen_time"
                    )
            except TypeError:
                errors.append(
                    "/extensions/profiles/endpoint_asset/lifecycle: first_seen_time and last_seen_time must use compatible timezone forms"
                )
    return errors


def validate_registry(registry: dict[str, Any], object_registry: dict[str, Any], policy: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if registry.get("registry_version") != 1:
        errors.append("registry_version must equal 1")
    if registry.get("schema_version") not in policy.get("schema_versions", []):
        errors.append("schema_version is not allowed by version policy")
    projection_version = registry.get("projection_version")
    if projection_version not in policy.get("projection_versions", []):
        errors.append("projection_version is not allowed by version policy")
    if not isinstance(projection_version, str) or not VERSION_RE.fullmatch(projection_version):
        errors.append("projection_version is not canonical")

    errors.extend(validate_limits(registry.get("limits_bytes"), "registry"))
    policy_limits = (policy.get("extension_envelope") or {}).get("limits_bytes")
    if registry.get("limits_bytes") != policy_limits:
        errors.append("registry limits do not match version policy")

    rules = registry.get("projection_rules")
    if not isinstance(rules, dict):
        errors.append("projection_rules must be an object")
        rules = {}
    defaults = rules.get("defaults") or {}
    required_defaults = {"normalizer", "primary_selection", "conflict_priority", "nullable", "event_types"}
    if not isinstance(defaults, dict) or not required_defaults.issubset(defaults):
        errors.append(f"projection_rules.defaults must define {sorted(required_defaults)}")
    normalizers = set(rules.get("normalizers") or [])
    overrides = rules.get("by_column") or {}
    if not isinstance(overrides, dict):
        errors.append("projection_rules.by_column must be an object")
        overrides = {}

    allowed_paths = set(object_registry.get("logical_paths") or [])
    columns = registry.get("columns")
    if not isinstance(columns, list) or not columns:
        return errors + ["columns must be a non-empty array"]
    seen_columns: set[str] = set()
    seen_pairs: set[tuple[str, str]] = set()
    for index, entry in enumerate(columns):
        label = f"columns[{index}]"
        if not isinstance(entry, dict):
            errors.append(f"{label}: entry must be an object")
            continue
        column = entry.get("column")
        path = entry.get("path")
        if not isinstance(column, str) or not column:
            errors.append(f"{label}: column must be non-empty")
        elif column in seen_columns:
            errors.append(f"{label}: duplicate target column {column!r}")
        else:
            seen_columns.add(column)
        if path not in allowed_paths:
            errors.append(f"{label}: unknown logical path {path!r}")
        pair = (str(path), str(column))
        if pair in seen_pairs:
            errors.append(f"{label}: duplicate logical authority {pair!r}")
        seen_pairs.add(pair)
        if entry.get("projection") not in PROJECTION_TYPES:
            errors.append(f"{label}: unsupported projection type {entry.get('projection')!r}")
        effective = {**defaults, **(overrides.get(column) or {})}
        if effective.get("normalizer") not in normalizers:
            errors.append(f"{label}: normalizer {effective.get('normalizer')!r} is not registered")
        if entry.get("projection") == "PRIMARY_ONLY" and not effective.get("primary_selection"):
            errors.append(f"{label}: PRIMARY_ONLY projection requires primary_selection")
        if not isinstance(effective.get("conflict_priority"), list) or not effective.get("conflict_priority"):
            errors.append(f"{label}: conflict_priority must be non-empty")
        if not isinstance(effective.get("event_types"), list) or not effective.get("event_types"):
            errors.append(f"{label}: event_types applicability must be non-empty")
        if not isinstance(effective.get("nullable"), bool):
            errors.append(f"{label}: nullable must be boolean")
        access = entry.get("access")
        if not isinstance(access, list) or not access or any(item not in ACCESS_TYPES for item in access):
            errors.append(f"{label}: access tags are invalid")
        sql_type = entry.get("type")
        if not isinstance(sql_type, str) or not re.fullmatch(r"(?:VARCHAR\([0-9]+\)|DATETIME\(3\)|INT|BIGINT|VARIANT)", sql_type):
            errors.append(f"{label}: incompatible or unknown target type {sql_type!r}")

    variants = registry.get("variant_objects")
    expected = {"roles": {"physical_column": "roles_obj"}, "facets": {"physical_column": "facets_obj"}, "source_finding": {"physical_column": "source_finding_obj"}, "extensions": {"physical_column": "extensions_obj"}}
    if variants != expected:
        errors.append("variant_objects must declare the four canonical objects with physical columns (roles_obj/facets_obj/source_finding_obj/extensions_obj)")
    writable_targets = seen_columns | set(m["physical_column"] for m in (variants or {}).values())
    seen_aliases: set[str] = set()
    for index, alias in enumerate(registry.get("aliases") or []):
        label = f"aliases[{index}]"
        if not isinstance(alias, dict):
            errors.append(f"{label}: alias must be an object")
            continue
        legacy = alias.get("legacy_column")
        target = alias.get("target_column")
        if not isinstance(legacy, str) or legacy in seen_aliases:
            errors.append(f"{label}: duplicate or invalid legacy alias {legacy!r}")
        else:
            seen_aliases.add(legacy)
        if target not in writable_targets:
            errors.append(f"{label}: target column {target!r} does not exist")
        if alias.get("read_only") is not True:
            errors.append(f"{label}: legacy alias must be read_only")
        if legacy in writable_targets:
            errors.append(f"{label}: legacy alias must not be independently writable")
    return errors


def validate_event_fixture(path: Path, expect_valid: bool) -> list[str]:
    value = load_json(path)
    schema = load_schema("sdm-event-logical", schemas_dir=LIVE_SCHEMAS_DIR)
    caught: list[str] = []
    try:
        validate_instance(value, schema)
        semantic_errors = validate_multi_object_semantics(value)
        if semantic_errors:
            caught.extend(semantic_errors)
    except (ValidationError, ValueError) as exc:
        caught.append(str(exc))
    if expect_valid and caught:
        return [f"{path}: expected valid: {'; '.join(caught)}"]
    if not expect_valid and not caught:
        return [f"{path}: expected invalid but validation passed"]
    return []


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", type=Path, default=REGISTRY_PATH)
    args = parser.parse_args()
    try:
        registry = load_json(args.registry)
        object_registry = load_json(OBJECT_REGISTRY_PATH)
        profile_registry = load_json(PROFILE_REGISTRY_PATH)
        policy = load_json(VERSION_POLICY_PATH)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    errors = validate_object_registry(object_registry)
    errors.extend(validate_profile_registry(profile_registry))
    errors.extend(validate_registry(registry, object_registry, policy))
    for path in sorted((FIXTURES_DIR / "valid").glob("*.json")):
        if path.name == "registry.json":
            fixture = load_json(path)
            fixture["variant_objects"] = {"roles": {"physical_column": "roles_obj"}, "facets": {"physical_column": "facets_obj"}, "source_finding": {"physical_column": "source_finding_obj"}, "extensions": {"physical_column": "extensions_obj"}}
            fixture_errors = validate_registry(fixture, object_registry, policy)
            errors.extend(f"{path}: {error}" for error in fixture_errors)
        else:
            errors.extend(validate_event_fixture(path, True))
    for path in sorted((FIXTURES_DIR / "invalid").glob("*.json")):
        if "registry" in path.name:
            fixture_errors = validate_registry(load_json(path), object_registry, policy)
            if not fixture_errors:
                errors.append(f"{path}: expected invalid registry but validation passed")
        else:
            errors.extend(validate_event_fixture(path, False))

    if errors:
        for error in errors:
            print(f"FAIL {error}")
        return 1
    print(f"hybrid event contracts valid: {len(registry['columns'])} projections, {len(registry.get('aliases') or [])} aliases")
    # P2-1：契约校验与生成资产 freshness 合并（避免 "contracts valid" 误读为全链路一致）
    renderer = Path(__file__).resolve().parent / "render_hybrid_event_assets.py"
    result = subprocess.run([sys.executable, str(renderer), "--check"], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"FAIL generated assets stale:\n{result.stdout}{result.stderr}")
        return 1
    print("generated hybrid assets fresh")
    ddl_gen = REPO_ROOT / "log-model/scripts/generate_sdm_event_ddl.py"
    result = subprocess.run([sys.executable, str(ddl_gen), "--check"], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"FAIL hybrid production DDL not retired:\n{result.stdout}{result.stderr}")
        return 1
    print("hybrid production DDL retired (007/026 absent)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
