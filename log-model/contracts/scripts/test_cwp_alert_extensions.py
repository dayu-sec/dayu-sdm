"""CWP 告警批准增补：有效组边界、角色复用与元数据类型。"""
import copy
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


validator = load("alert_validator", ROOT / "log-model/scripts/validate_behavior_event.py")
metadata = load("alert_metadata", ROOT / "log-model/scripts/generate_metadata_backup.py")
SCHEMA = json.loads(validator.SCHEMA.read_text())
FIELDS = json.loads(validator.FIELDS.read_text())
EXAMPLE = ROOT / "log-model/examples/cwp-alerts/effective-group.expected-sdm-event.behavior.json"


class CwpAlertTests(unittest.TestCase):
    def setUp(self):
        self.event = json.loads(EXAMPLE.read_text())

    def test_example(self):
        self.assertEqual(validator.validate_one(EXAMPLE, SCHEMA, FIELDS), [])

    def test_optional_old_event(self):
        self.event["subject"]["process"].pop("egid")
        self.assertEqual(validator.check(self.event, FIELDS), [])

    def test_egid_range_root_and_unknown(self):
        for value in (0, 1000, 4294967294):
            self.event["subject"]["process"]["egid"] = value
            self.assertEqual(validator.check(self.event, FIELDS), [])
        for value in (-1, 4294967295, 2**64, "0", "unset", True, None, 0.0):
            self.event["subject"]["process"]["egid"] = value
            self.assertTrue(validator.check(self.event, FIELDS), repr(value))

    def test_group_roles_remain_independent(self):
        process = self.event["subject"]["process"]
        self.assertEqual(process["real_group"]["uid"], "1000")
        self.assertEqual(process["egid"], 0)
        self.assertEqual(process["file"]["group"]["uid"], "1002")
        self.assertEqual(validator.check(self.event, FIELDS), [])
        process["real_group"]["uid"] = 1000
        self.assertTrue(validator.check(self.event, FIELDS))

    def test_all_process_roles(self):
        process = copy.deepcopy(self.event["subject"])
        process["process"]["egid"] = -1
        for event in (
            {"subject": process}, {"object": process}, {"carriers": [process]},
            {"observation": {"observer": process}},
            {"observation": {"assertion": {"affected": [process]}}},
        ):
            self.assertTrue(validator.check_host_extensions(event, FIELDS))
        self.assertEqual(validator.check_host_extensions(
            {"extensions": {"source_private": {"process": {"egid": "unset"}}}}, FIELDS), [])

    def test_registry_and_metadata(self):
        process = next(e for e in FIELDS["entity_types"] if e["type"] == "process")
        field = next(f for f in process["fields"] if f["name"] == "egid")
        self.assertEqual((field["type"], field["minimum"], field["maximum"]), ("integer", 0, 4294967294))
        rows = {r["path"]: r for r in metadata.logical_fields()}
        for prefix in ("subject", "object", "carriers[]", "observation.observer"):
            self.assertEqual(rows[f"{prefix}.process.egid"]["base"], "Bigint")
            self.assertIn("有效 GID", rows[f"{prefix}.process.egid"]["cname"])
            self.assertEqual(rows[f"{prefix}.process.real_group.uid"]["base"], "String")
        self.assertEqual(rows["facets.file.accessed_time"]["base"], "Datetime")
        self.assertIn("subject.process.file.mode", rows)
        self.assertEqual(len([f for f in process["fields"] if f["name"] == "egid"]), 1)


if __name__ == "__main__":
    unittest.main()
