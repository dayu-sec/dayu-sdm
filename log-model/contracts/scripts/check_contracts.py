"""Validate the SDM2.0 release-control-plane contract surface.

Walks the versioned JSON Schemas under contracts/schemas/ and the golden
fixtures under contracts/fixtures/, then asserts every fixture behaves as its
directory advertises:

  - fixtures/valid/**   must conform to the schema named in their
                        `$contract` field.
  - fixtures/invalid/** must fail validation; if they declare `$expect_keyword`,
                        the failure must mention that keyword.

This checker is stdlib-only on purpose: PEP 668 makes installing `jsonschema`
into the system Python fragile, and the schemas intentionally use a small,
stable subset of JSON Schema (draft 2020-12) we can validate by hand.

Supported subset:
  - type (string or union array), const, enum, pattern
  - required, properties, additionalProperties (false only)
  - items, minItems
  - minLength, maxLength
  - minimum, maximum
  - oneOf
  - $ref (internal `#/$defs/...` only)
  - $defs

`if/then/else`, `allOf`, `anyOf`, dependencies, and contentMediaType are
deliberately out of scope. The service enforces cross-field constraints; the
schema is the first-line shape contract.

Exit code 0 = clean, 1 = drift detected, 2 = checker misconfiguration.

Usage:
    python3 scripts/check_contracts.py
    python3 scripts/check_contracts.py --schema change-manifest
    python3 scripts/check_contracts.py --fixtures-only
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from pathlib import PurePosixPath
from typing import Any

try:
    import yaml  # type: ignore
except ImportError:
    yaml = None

REPO_ROOT = Path(__file__).resolve().parents[3]
SCHEMAS_DIR = REPO_ROOT / "log-model/contracts/schemas"
FIXTURES_DIR = SCHEMAS_DIR / "fixtures"
BUNDLES_DIR = FIXTURES_DIR / "bundles"

CONTRACT_FIELD = "$contract"
EXPECT_FIELD = "$expect_keyword"
COMMENT_FIELDS = (CONTRACT_FIELD, EXPECT_FIELD, "$expect_path", "$note")
SEMVER_RE = re.compile(r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)$")
STANDARDS_CATEGORIES = {
    "event_fields",
    "alert_fields",
    "enums",
    "tables",
    "rules",
    "log_type_profiles",
    "prose",
}
FORBIDDEN_MANIFEST_ARTIFACTS = {"release-meta.yaml", "SHA256SUMS"}


class ValidationError(Exception):
    """Single assertion failure with a JSON-pointer-like path."""

    def __init__(self, path: str, message: str) -> None:
        self.path = path or "/"
        self.message = message
        super().__init__(f"{self.path}: {message}")


def _resolve_ref(ref: str, root_schema: dict[str, Any]) -> dict[str, Any]:
    if not ref.startswith("#/$defs/"):
        raise ValueError(f"unsupported $ref '{ref}' (only internal #/$defs/... is allowed)")
    name = ref[len("#/$defs/"):]
    defs = root_schema.get("$defs") or {}
    if name not in defs:
        raise ValueError(f"$ref target '{ref}' not found in $defs")
    return defs[name]


def _check_type(value: Any, expected: str | list[str]) -> str | None:
    if isinstance(expected, list):
        failures = [_check_type(value, item) for item in expected]
        if any(failure is None for failure in failures):
            return None
        return f"value is {type(value).__name__}, expected one of {expected}"
    if expected == "object":
        return None if isinstance(value, dict) else f"value is {type(value).__name__}, expected object"
    if expected == "array":
        return None if isinstance(value, list) else f"value is {type(value).__name__}, expected array"
    if expected == "string":
        return None if isinstance(value, str) else f"value is {type(value).__name__}, expected string"
    if expected == "integer":
        if isinstance(value, bool) or not isinstance(value, int):
            return f"value is {type(value).__name__}, expected integer"
        return None
    if expected == "number":
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            return f"value is {type(value).__name__}, expected number"
        return None
    if expected == "boolean":
        return None if isinstance(value, bool) else f"value is {type(value).__name__}, expected boolean"
    if expected == "null":
        return None if value is None else f"value is {type(value).__name__}, expected null"
    return f"unsupported type declaration '{expected}'"


def _validate(value: Any, schema: dict[str, Any], root_schema: dict[str, Any], path: str) -> None:
    if not isinstance(schema, dict):
        raise ValidationError(path, f"schema at this path is not an object: {type(schema).__name__}")

    if "$ref" in schema:
        target = _resolve_ref(schema["$ref"], root_schema)
        _validate(value, target, root_schema, path)
        return

    if "const" in schema:
        if value != schema["const"]:
            raise ValidationError(path, f"value {value!r} must equal const {schema['const']!r}")

    if "enum" in schema:
        if value not in schema["enum"]:
            raise ValidationError(path, f"value {value!r} not in enum {schema['enum']}")

    if "type" in schema:
        msg = _check_type(value, schema["type"])
        if msg:
            raise ValidationError(path, msg)

    if isinstance(value, str):
        if "pattern" in schema:
            if not re.fullmatch(schema["pattern"], value):
                raise ValidationError(path, f"string {value!r} does not match pattern {schema['pattern']!r}")
        if "minLength" in schema and len(value) < schema["minLength"]:
            raise ValidationError(path, f"string length {len(value)} < minLength {schema['minLength']}")
        if "maxLength" in schema and len(value) > schema["maxLength"]:
            raise ValidationError(path, f"string length {len(value)} > maxLength {schema['maxLength']}")

    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if "minimum" in schema and value < schema["minimum"]:
            raise ValidationError(path, f"value {value} < minimum {schema['minimum']}")
        if "maximum" in schema and value > schema["maximum"]:
            raise ValidationError(path, f"value {value} > maximum {schema['maximum']}")

    if isinstance(value, list):
        if "minItems" in schema and len(value) < schema["minItems"]:
            raise ValidationError(path, f"array length {len(value)} < minItems {schema['minItems']}")
        if "maxItems" in schema and len(value) > schema["maxItems"]:
            raise ValidationError(path, f"array length {len(value)} > maxItems {schema['maxItems']}")
        if "items" in schema:
            for i, item in enumerate(value):
                _validate(item, schema["items"], root_schema, f"{path}/{i}")

    if isinstance(value, dict):
        if "required" in schema:
            for key in schema["required"]:
                if key not in value:
                    raise ValidationError(path, f"missing required property '{key}'")
        if "properties" in schema:
            for key, prop_value in value.items():
                if key in COMMENT_FIELDS:
                    continue
                if key in schema["properties"]:
                    _validate(prop_value, schema["properties"][key], root_schema, f"{path}/{key}")
                elif schema.get("additionalProperties") is False:
                    raise ValidationError(path, f"additional property '{key}' not allowed")

    if "oneOf" in schema:
        matches = 0
        last_error: Exception | None = None
        for i, sub in enumerate(schema["oneOf"]):
            try:
                _validate(value, sub, root_schema, f"{path}<oneOf[{i}]>")
                matches += 1
            except ValidationError as exc:
                last_error = exc
        if matches == 0:
            raise ValidationError(path, f"matched no oneOf branch (last error: {last_error})")
        if matches > 1:
            raise ValidationError(path, f"matched {matches} oneOf branches; exactly one required")


def validate_instance(value: Any, schema: dict[str, Any]) -> None:
    """Top-level entry: validates `value` against `schema`.

    Raises ValidationError on the first failure. Removes contract-marker
    fields (`$contract`, `$expect_*`, `$note`) from the value before checking
    so fixture files can self-describe.
    """
    cleaned = _strip_comment_fields(value)
    _validate(cleaned, schema, schema, "")


def _semantic_errors(value: Any, schema_name: str) -> list[str]:
    """Validate cross-field rules intentionally kept outside JSON Schema."""
    if not isinstance(value, dict):
        return []
    doc = _strip_comment_fields(value)
    errors: list[str] = []

    def require_semver(path: str, raw: Any) -> None:
        if isinstance(raw, str) and not SEMVER_RE.fullmatch(raw):
            errors.append(f"{path}: non-canonical SemVer {raw!r}")

    def require_standards_path(path: str, raw: Any) -> None:
        if not isinstance(raw, str):
            return
        posix = PurePosixPath(raw)
        parts = posix.parts
        if (
            raw.startswith("/")
            or "\\" in raw
            or any(ord(ch) < 32 or ord(ch) == 127 for ch in raw)
            or not parts
            or parts[0] not in STANDARDS_CATEGORIES
            or any(part in {"", ".", ".."} for part in raw.split("/"))
            or str(posix) != raw
        ):
            errors.append(f"{path}: unsafe or non-canonical standards path {raw!r}")

    def require_release_artifact_path(path: str, raw: Any) -> None:
        if not isinstance(raw, str):
            return
        parts = raw.split("/")
        unsafe = (
            raw.startswith("/")
            or "\\" in raw
            or any(ord(ch) < 32 or ord(ch) == 127 for ch in raw)
            or any(part in {"", ".", ".."} for part in parts)
        )
        allowed = False
        if raw.startswith("standards/"):
            nested = raw[len("standards/"):]
            before = len(errors)
            require_standards_path(path, nested)
            allowed = len(errors) == before
        elif raw in {
            "migrations/upgrade.sql",
            "migrations/rollback.sql",
            "migration-meta.json",
            "validation-report.json",
        }:
            allowed = True
        if unsafe or not allowed:
            message = f"{path}: unsafe or non-allowlisted release artifact path {raw!r}"
            if message not in errors:
                errors.append(message)

    if schema_name == "change-manifest":
        require_semver("/base_release", doc.get("base_release"))
        seen_paths: set[str] = set()
        for index, operation in enumerate(doc.get("documents") or []):
            if not isinstance(operation, dict):
                continue
            item_path = f"/documents/{index}"
            path_value = operation.get("path")
            require_standards_path(f"{item_path}/path", path_value)
            if isinstance(path_value, str):
                if path_value in seen_paths:
                    errors.append(f"{item_path}/path: duplicate document path {path_value!r}")
                seen_paths.add(path_value)
            kind = operation.get("operation")
            base_hash = operation.get("base_sha256")
            content_hash = operation.get("content_sha256")
            well_formed = {
                "add": base_hash is None and content_hash is not None,
                "replace": base_hash is not None and content_hash is not None,
                "delete": base_hash is not None and content_hash is None,
            }.get(kind, False)
            if not well_formed:
                errors.append(f"{item_path}: hash pairing does not match operation {kind!r}")

    elif schema_name == "current-release":
        version = doc.get("version")
        require_semver("/version", version)
        previous = doc.get("previous_version")
        if previous is not None:
            require_semver("/previous_version", previous)
        if isinstance(version, str) and doc.get("release_path") != f"releases/{version}/":
            errors.append("/release_path: must match /version exactly")

    elif schema_name == "release-meta":
        for key in ("version", "parent_version"):
            raw = doc.get(key)
            if raw is not None:
                require_semver(f"/{key}", raw)
        seen_artifacts: set[str] = set()
        for index, artifact in enumerate(doc.get("artifacts") or []):
            if not isinstance(artifact, dict) or not isinstance(artifact.get("path"), str):
                continue
            artifact_path = artifact["path"]
            require_release_artifact_path(f"/artifacts/{index}/path", artifact_path)
            if artifact_path in FORBIDDEN_MANIFEST_ARTIFACTS:
                errors.append(f"/artifacts/{index}/path: checksum topology forbids {artifact_path!r}")
            if artifact_path in seen_artifacts:
                errors.append(f"/artifacts/{index}/path: duplicate artifact {artifact_path!r}")
            seen_artifacts.add(artifact_path)

    elif schema_name == "migration-meta":
        require_semver("/base_release", doc.get("base_release"))
        require_semver("/target_release", doc.get("target_release"))
        require_semver("/compiler_version", doc.get("compiler_version"))
        for index, operation in enumerate(doc.get("operations") or []):
            if isinstance(operation, dict):
                require_standards_path(
                    f"/operations/{index}/document_path", operation.get("document_path")
                )

    elif schema_name == "validation-report":
        require_semver("/base_release", doc.get("base_release"))
        validators = [item for item in (doc.get("validators") or []) if isinstance(item, dict)]
        actual = {
            "passed": sum(item.get("status") == "passed" for item in validators),
            "failed": sum(item.get("status") == "failed" for item in validators),
            "warnings": sum(item.get("status") == "warning" for item in validators),
        }
        if doc.get("counts") != actual:
            errors.append(f"/counts: declared counts {doc.get('counts')!r} != actual {actual!r}")
        expected_status = "failed" if actual["failed"] else "passed"
        if doc.get("status") != expected_status:
            errors.append(f"/status: must be {expected_status!r} for the validator results")
        for index, result in enumerate(validators):
            path_value = result.get("document_path")
            if path_value is not None:
                require_standards_path(f"/validators/{index}/document_path", path_value)

    elif schema_name == "audit-event":
        if doc.get("status") in {"pending", "aborted"} and doc.get("action") != "publish":
            errors.append("/status: pending or aborted is only valid for publish events")

    return errors


def _strip_comment_fields(value: Any) -> Any:
    if isinstance(value, dict):
        return {k: _strip_comment_fields(v) for k, v in value.items() if k not in COMMENT_FIELDS}
    if isinstance(value, list):
        return [_strip_comment_fields(v) for v in value]
    return value


def load_schema(name: str, schemas_dir: Path | None = None) -> dict[str, Any]:
    path = (schemas_dir or SCHEMAS_DIR) / f"{name}.schema.json"
    if not path.is_file():
        raise FileNotFoundError(f"schema {name} not found at {path}")
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)



def list_schemas() -> list[str]:
    if not SCHEMAS_DIR.is_dir():
        return []
    return sorted(p.stem.removesuffix(".schema") for p in SCHEMAS_DIR.glob("*.schema.json"))


class _NoTimestampLoader(getattr(yaml, "SafeLoader", object)):
    """SafeLoader variant that keeps ISO 8601 timestamps as strings.

    The schemas intentionally declare timestamp fields as `type: string` with
    a regex pattern. PyYAML's default `safe_load` coerces ISO 8601 values to
    `datetime.datetime`, which would defeat that contract. Removing the
    implicit resolver keeps the raw string for the validator to pattern-check.
    """


if yaml is not None:
    _NoTimestampLoader.yaml_implicit_resolvers = {
        k: [(tag, regexp) for tag, regexp in v if tag != "tag:yaml.org,2002:timestamp"]
        for k, v in yaml.SafeLoader.yaml_implicit_resolvers.items()
    }


def _load_fixture(path: Path) -> Any:
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".json":
        return json.loads(text)
    if yaml is None:
        raise RuntimeError(f"fixture {path.name} requires PyYAML but it is not installed")
    return yaml.load(text, Loader=_NoTimestampLoader)


def _validate_fixture_against_schema(fixture: Any, schema_name: str) -> list[str]:
    schema = load_schema(schema_name)
    errors: list[str] = []
    try:
        validate_instance(fixture, schema)
    except ValidationError as exc:
        errors.append(f"{exc.path}: {exc.message}")
    except ValueError as exc:
        errors.append(f"(schema resolution) {exc}")
    return errors


def check_fixture(path: Path, expect_valid: bool) -> tuple[bool, str]:
    """Return (ok, detail). For valid fixtures, detail is success note.

    For invalid fixtures, the file's `$contract` selects the schema and the
    optional `$expect_keyword` / `$expect_path` narrow the failure requirement.
    """
    try:
        fixture = _load_fixture(path)
    except Exception as exc:  # noqa: BLE001
        return False, f"could not parse fixture: {exc}"

    if not isinstance(fixture, dict):
        return False, "fixture must be a JSON/YAML object with $contract marker"

    schema_name = fixture.get(CONTRACT_FIELD)
    if not isinstance(schema_name, str):
        return False, f"missing {CONTRACT_FIELD} marker"
    try:
        schema = load_schema(schema_name)
    except FileNotFoundError as exc:
        return False, str(exc)

    caught: list[str] = []
    try:
        validate_instance(fixture, schema)
    except ValidationError as exc:
        caught.append(f"{exc.path}: {exc.message}")
    except ValueError as exc:
        caught.append(f"(schema resolution) {exc}")
    caught.extend(_semantic_errors(fixture, schema_name))

    expect_keyword = fixture.get(EXPECT_FIELD)
    expect_path = fixture.get("$expect_path")

    if expect_valid:
        if caught:
            return False, "expected valid but failed: " + "; ".join(caught)
        return True, "conforms"

    # invalid path
    if not caught:
        return False, "expected invalid but schema accepted it"
    if expect_keyword and not any(expect_keyword in msg for msg in caught):
        return False, f"expected failure mentioning '{expect_keyword}' but got: " + "; ".join(caught)
    if expect_path and not any(expect_path in msg for msg in caught):
        return False, f"expected failure mentioning path '{expect_path}' but got: " + "; ".join(caught)
    return True, "rejected as expected: " + "; ".join(caught)


def check_self_describing_schema(schema_name: str) -> list[str]:
    """Each schema must itself be a valid JSON Schema (subset)."""
    issues: list[str] = []
    try:
        schema = load_schema(schema_name)
    except Exception as exc:  # noqa: BLE001
        return [f"{schema_name}: cannot load: {exc}"]
    if not isinstance(schema, dict):
        return [f"{schema_name}: schema is not an object"]
    for key in ("$id", "title", "type", "properties"):
        if key not in schema:
            issues.append(f"{schema_name}: missing recommended top-level '{key}'")
    if "$defs" in schema and not isinstance(schema["$defs"], dict):
        issues.append(f"{schema_name}: $defs must be an object")
    # Resolve every $ref target
    text = json.dumps(schema)
    for ref in re.findall(r'"\$ref":\s*"([^"]+)"', text):
        try:
            _resolve_ref(ref, schema)
        except ValueError as exc:
            issues.append(f"{schema_name}: {exc}")
    return issues


def _load_bundle_document(reference: str) -> tuple[dict[str, Any], str]:
    path = (FIXTURES_DIR / reference).resolve()
    try:
        path.relative_to(FIXTURES_DIR.resolve())
    except ValueError as exc:
        raise ValueError(f"bundle reference escapes fixtures root: {reference!r}") from exc
    value = _load_fixture(path)
    if not isinstance(value, dict) or not isinstance(value.get(CONTRACT_FIELD), str):
        raise ValueError(f"bundle reference is not a contract fixture: {reference!r}")
    schema_name = value[CONTRACT_FIELD]
    schema = load_schema(schema_name)
    validate_instance(value, schema)
    semantic = _semantic_errors(value, schema_name)
    if semantic:
        raise ValueError(f"bundle member {reference!r} failed semantics: {'; '.join(semantic)}")
    return _strip_comment_fields(value), schema_name


def check_bundle(path: Path, expect_valid: bool) -> tuple[bool, str]:
    """Validate relationships across change, validation, release, migration and pointer fixtures."""
    bundle: Any = None
    try:
        bundle = _load_fixture(path)
        if not isinstance(bundle, dict):
            raise ValueError("bundle fixture must be an object")
        loaded: dict[str, dict[str, Any]] = {}
        for key in ("change_manifest", "validation_report", "release_meta", "migration_meta", "current_release"):
            reference = bundle.get(key)
            if not isinstance(reference, str):
                raise ValueError(f"bundle missing reference {key!r}")
            loaded[key], _ = _load_bundle_document(reference)

        change = loaded["change_manifest"]
        validation = loaded["validation_report"]
        release = loaded["release_meta"]
        migration = loaded["migration_meta"]
        pointer = loaded["current_release"]
        errors: list[str] = []
        if pointer.get("version") != release.get("version"):
            errors.append("current release version does not match release metadata")
        if pointer.get("previous_version") != release.get("parent_version"):
            errors.append("current previous_version does not match release parent_version")
        if change.get("change_id") != release.get("base_change_id"):
            errors.append("release base_change_id does not match change manifest")
        if validation.get("change_id") != change.get("change_id"):
            errors.append("validation change_id does not match change manifest")
        if change.get("base_release") != release.get("parent_version"):
            errors.append("change base_release does not match release parent_version")
        if validation.get("base_release") != change.get("base_release"):
            errors.append("validation base_release does not match change manifest")
        if migration.get("base_release") != release.get("parent_version"):
            errors.append("migration base_release does not match release parent_version")
        if migration.get("target_release") != release.get("version"):
            errors.append("migration target_release does not match release version")
        if change.get("requested_bump") != release.get("requested_bump"):
            errors.append("release requested_bump does not match change manifest")
        rank = {"patch": 0, "minor": 1, "major": 2}
        computed = release.get("computed_min_bump")
        requested = release.get("requested_bump")
        compatibility = release.get("compatibility")
        if any(value not in rank for value in (computed, requested, compatibility)):
            errors.append("release compatibility classes are invalid")
        elif not (rank[computed] <= rank[requested] <= rank[compatibility]):
            errors.append("release compatibility class ordering is invalid")
        parent = release.get("parent_version")
        target = release.get("version")
        if isinstance(parent, str) and isinstance(target, str) and compatibility in rank:
            p_major, p_minor, p_patch = (int(part) for part in parent.split("."))
            if compatibility == "patch":
                expected = f"{p_major}.{p_minor}.{p_patch + 1}"
            elif p_major == 0:
                expected = f"0.{p_minor + 1}.0"
            elif compatibility == "minor":
                expected = f"{p_major}.{p_minor + 1}.0"
            else:
                expected = f"{p_major + 1}.0.0"
            if target != expected:
                errors.append(
                    f"release version {target!r} does not match {compatibility} advancement from {parent!r} ({expected!r})"
                )
    except Exception as exc:  # noqa: BLE001
        errors = [str(exc)]

    expected_keyword = bundle.get("$expect_keyword") if isinstance(bundle, dict) else None
    if expect_valid:
        return (not errors, "cross-file references conform" if not errors else "; ".join(errors))
    if not errors:
        return False, "expected invalid bundle but all cross-file references conformed"
    if expected_keyword and not any(expected_keyword in error for error in errors):
        return False, f"expected failure mentioning {expected_keyword!r}, got: {'; '.join(errors)}"
    return True, "rejected as expected: " + "; ".join(errors)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n", 1)[0])
    parser.add_argument("--schema", help="validate only one schema's fixtures (by stem, e.g. change-manifest)")
    parser.add_argument("--fixtures-only", action="store_true", help="skip schema self-check")
    parser.add_argument("--strict", action="store_true", help="treat schema self-check warnings as failures")
    args = parser.parse_args()

    if not SCHEMAS_DIR.is_dir():
        print(f"error: {SCHEMAS_DIR} not found", file=sys.stderr)
        return 2

    failures = 0
    checked = 0

    # Step 1: schema self-check.
    if not args.fixtures_only:
        for name in list_schemas():
            issues = check_self_describing_schema(name)
            for issue in issues:
                print(f"schema:{issue}")
                if args.strict or "missing" not in issue:
                    failures += 1
            checked += 1
        print(f"schema self-check: {checked} schema(s) inspected")

    # Step 2: fixtures.
    # The retired release-control fixture tree was archived and removed.  The
    # live contract keeps schemas here; fixture validation is optional when a
    # caller supplies a separate fixture tree.
    if not FIXTURES_DIR.is_dir():
        print("fixtures: 0 file(s) checked")
        print("OK: schemas conform")
        return failures and 1 or 0

    fixture_count = 0
    for kind, expect_valid in (("valid", True), ("invalid", False)):
        kind_dir = FIXTURES_DIR / kind
        if not kind_dir.is_dir():
            continue
        for path in sorted(kind_dir.rglob("*")):
            if not path.is_file() or path.suffix not in (".json", ".yaml", ".yml"):
                continue
            if args.schema and path.read_text(encoding="utf-8").find(f'"$contract": "{args.schema}"') == -1 \
                    and f"$contract: {args.schema}" not in path.read_text(encoding="utf-8"):
                continue
            fixture_count += 1
            ok, detail = check_fixture(path, expect_valid)
            label = "OK " if ok else "FAIL"
            print(f"{label} {kind}/{path.relative_to(kind_dir)}: {detail}")
            if not ok:
                failures += 1

    print(f"fixtures: {fixture_count} file(s) checked")

    bundle_count = 0
    if BUNDLES_DIR.is_dir():
        for kind, expect_valid in (("valid", True), ("invalid", False)):
            kind_dir = BUNDLES_DIR / kind
            if not kind_dir.is_dir():
                continue
            for path in sorted(kind_dir.glob("*.yaml")):
                bundle_count += 1
                ok, detail = check_bundle(path, expect_valid)
                label = "OK " if ok else "FAIL"
                print(f"{label} bundles/{kind}/{path.name}: {detail}")
                if not ok:
                    failures += 1
    print(f"cross-file bundles: {bundle_count} file(s) checked")
    if failures:
        print(f"\n{failures} contract drift finding(s); fix fixtures/schemas and rerun", file=sys.stderr)
        return 1
    print("OK: contracts conform")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
