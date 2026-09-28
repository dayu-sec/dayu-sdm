"""CWP 行为流水可选增补：权限、身份角色、时间和元数据守护。"""
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[3]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


validator = load("cwp_validator", ROOT / "log-model/scripts/validate_behavior_event.py")
metadata = load("cwp_metadata", ROOT / "log-model/scripts/generate_metadata_backup.py")
SCHEMA = json.loads(validator.SCHEMA.read_text())
FIELDS = json.loads(validator.FIELDS.read_text())
EXAMPLE = ROOT / "log-model/examples/cwp-activity/file-permissions.expected-sdm-event.behavior.json"


class CwpActivityTests(unittest.TestCase):
    def setUp(self):
        self.event = json.loads(EXAMPLE.read_text())

    def test_example(self):
        self.assertEqual(validator.validate_one(EXAMPLE, SCHEMA, FIELDS), [])

    def test_optional_compatibility(self):
        self.event.pop("facets")
        self.event["subject"]["process"].pop("real_group")
        for file in (self.event["subject"]["process"]["file"], self.event["object"]["file"]):
            for key in ("mode", "owner", "group"):
                file.pop(key)
        self.assertEqual(validator.check(self.event, FIELDS), [])

    def test_modes(self):
        file = self.event["object"]["file"]
        for mode in ("0000", "0600", "4755", "2750", "1777", "7777"):
            file["mode"] = mode
            self.assertEqual(validator.check_cwp_activity_extensions(self.event), [])
        for mode in (600, None, "600", "0100600", "-rwsr-xr-x", "8888", "0600+", ""):
            file["mode"] = mode
            self.assertTrue(validator.check_cwp_activity_extensions(self.event), mode)

    def test_identity_strings_and_empty_objects(self):
        file = self.event["object"]["file"]
        for key in ("owner", "group"):
            for identity in ({"uid": "0"}, {"name": "example"}, {"uid": "1000", "name": "example"}):
                file[key] = identity
                self.assertEqual(validator.check_cwp_activity_extensions(self.event), [])
            for identity in ({}, None, {"uid": 0}, {"uid": "0:0"}, {"uid": "-1"},
                             {"uid": "4294967295"}, {"uid": ""}, {"name": " "}, {"id": "1000"}):
                file[key] = identity
                self.assertTrue(validator.check_cwp_activity_extensions(self.event), identity)
            file[key] = {"uid": "0"}

    def test_real_group_is_posix_identity(self):
        process = self.event["subject"]["process"]
        for value in ("0", "1000", "4294967294"):
            process["real_group"] = {"uid": value}
            self.assertEqual(validator.check_cwp_activity_extensions(self.event), [])
        for value in (0, True, "01000", "-1", "4294967295", "S-1-5-18", "unset"):
            process["real_group"] = {"uid": value}
            self.assertTrue(validator.check_cwp_activity_extensions(self.event), value)

    def test_access_time(self):
        file = self.event["facets"]["file"]
        for value in ("1970-01-01T00:00:00Z", "2026-09-28T08:59:00.125+08:00"):
            file["accessed_time"] = value
            self.assertEqual(validator.check_cwp_activity_extensions(self.event), [])
        for value in (0, None, "", "2026-09-28T00:00:00", "2026-02-30T00:00:00Z", "1790000000"):
            file["accessed_time"] = value
            self.assertTrue(validator.check_cwp_activity_extensions(self.event), value)

    def test_all_entity_slots_and_nested_process_file(self):
        invalid_file = {"mode": "-rw-------"}
        nodes = [
            {"subject": {"file": invalid_file}},
            {"object": {"file": invalid_file}},
            {"carriers": [{"process": {"file": invalid_file}}]},
            {"observation": {"observer": {"process": {"file": invalid_file}}}},
            {"observation": {"assertion": {"affected": [{"file": invalid_file}]}}},
        ]
        for node in nodes:
            self.assertTrue(validator.check_cwp_activity_extensions(node))
        self.assertEqual(validator.check_cwp_activity_extensions({"extensions": {"source_private": {"file": invalid_file}}}), [])

    def test_metadata_projection(self):
        rows = {r["path"]: r for r in metadata.logical_fields()}
        for prefix in ("subject", "object", "carriers[]", "observation.observer"):
            self.assertEqual(rows[f"{prefix}.process.real_group.uid"]["base"], "String")
            for key in ("mode", "owner.uid", "owner.name", "group.uid", "group.name"):
                self.assertEqual(rows[f"{prefix}.process.file.{key}"]["base"], "String")
        self.assertEqual(rows["facets.file.accessed_time"]["base"], "Datetime")
        # 后续 CWP 告警评审已批准 egid；真实组仍保持字符串，不被有效组类型覆盖。
        self.assertEqual(rows["subject.process.egid"]["base"], "Bigint")

    def test_typed_fields_and_schema(self):
        entities = {e["type"]: e for e in FIELDS["entity_types"]}
        file = {f["name"]: f for f in entities["file"]["fields"]}
        self.assertEqual(file["mode"]["pattern"], "^[0-7]{4}$")
        self.assertEqual(file["owner"]["nested"], ["uid", "name"])
        self.assertEqual(file["group"]["nested"], ["uid", "name"])
        self.assertEqual(SCHEMA["$defs"]["file_facet"]["properties"]["accessed_time"]["format"], "date-time")


if __name__ == "__main__":
    unittest.main()
