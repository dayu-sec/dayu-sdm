"""主机核心增补：边界、可选兼容、页面与元数据投影守护。"""
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


validator = load("host_validator", ROOT / "log-model/scripts/validate_behavior_event.py")
metadata = load("host_metadata", ROOT / "log-model/scripts/generate_metadata_backup.py")
SCHEMA = json.loads(validator.SCHEMA.read_text())
FIELDS = json.loads(validator.FIELDS.read_text())
EXAMPLES = ROOT / "log-model/examples/host"


class HostExtensionsTests(unittest.TestCase):
    def setUp(self):
        self.event = json.loads((EXAMPLES / "core-extensions.expected-sdm-event.behavior.json").read_text())
        self.ssh = json.loads((EXAMPLES / "ssh-public-key.expected-sdm-event.behavior.json").read_text())

    def test_examples(self):
        for p in EXAMPLES.glob("*.expected-sdm-event.behavior.json"):
            self.assertEqual(validator.validate_one(p, SCHEMA, FIELDS), [], str(p))

    def test_old_events_do_not_require_new_fields(self):
        self.event.pop("facets")
        for key in ("auid", "euid"):
            self.event["subject"]["process"].pop(key)
        self.assertEqual(validator.check(self.event, FIELDS), [])

    def test_uid_bounds_and_root_zero(self):
        for field in ("auid", "euid"):
            for value in (0, 1000, 4294967294):
                self.event["subject"]["process"][field] = value
                self.assertEqual(validator.check_host_extensions(self.event, FIELDS), [])
            for value in (-1, 4294967295, "0", True, None):
                bad = copy.deepcopy(self.event)
                bad["subject"]["process"][field] = value
                self.assertTrue(validator.check_host_extensions(bad, FIELDS), (field, value))
            self.event["subject"]["process"][field] = 0

    def test_uid_on_carrier_and_assertion(self):
        for root in ("carriers", "observation"):
            bad = copy.deepcopy(self.event)
            process = {"process": {"euid": -1}}
            bad[root] = [process] if root == "carriers" else {"assertion": {"affected": [process]}}
            self.assertTrue(validator.check_host_extensions(bad, FIELDS))

    def test_syscall_pair_and_signed_return(self):
        call = self.event["facets"]["process"]["syscall"]
        for value in (-13, 0, 3, 128, -(2**63), 2**63 - 1):
            call["return_value"] = value
            self.assertEqual(validator.check_host_extensions(self.event, FIELDS), [])
        for value in (2**63, -(2**63)-1, "-13", False):
            call["return_value"] = value
            self.assertTrue(validator.check_host_extensions(self.event, FIELDS))
        call.pop("return_value")
        call.pop("arch")
        self.assertTrue(validator.check_host_extensions(self.event, FIELDS))
        call["arch"] = "c000003e"
        call["exit_code"] = 0
        self.assertTrue(validator.check_host_extensions(self.event, FIELDS))

    def test_terminal(self):
        for val in ("", "(none)", "?", None, 0):
            self.event["facets"]["process"]["terminal"] = val
            self.assertTrue(validator.check_host_extensions(self.event, FIELDS))

    def test_public_key_fingerprint(self):
        key = self.ssh["facets"]["authentication"]["public_key"]
        key["fingerprint"] = {"algorithm": "MD5", "value": ":".join(["ab"] * 16)}
        self.assertEqual(validator.check_host_extensions(self.ssh, FIELDS), [])
        for fp in ({}, {"algorithm": "SHA1", "value": "a" * 40},
                   {"algorithm": "SHA256", "value": "SHA256:" + "A" * 43},
                   {"algorithm": "MD5", "value": "AB:" * 15 + "AB"},
                   {"algorithm": "SHA256", "value": "B" * 43}):
            key["fingerprint"] = fp
            self.assertTrue(validator.check_host_extensions(self.ssh, FIELDS), fp)

    def test_metadata_fields_and_types(self):
        rows = {r["path"]: r for r in metadata.logical_fields()}
        for prefix in ("subject.process", "object.process", "carriers[].process", "observation.observer.process"):
            for key in ("auid", "euid"):
                self.assertEqual(rows[f"{prefix}.{key}"]["base"], "Bigint")
        for key in ("number", "return_value"):
            self.assertEqual(rows[f"facets.process.syscall.{key}"]["base"], "Bigint")
        for path in ("facets.process.syscall.arch", "facets.process.terminal",
                     "facets.authentication.public_key.algorithm",
                     "facets.authentication.public_key.fingerprint.algorithm",
                     "facets.authentication.public_key.fingerprint.value"):
            self.assertIn(path, rows)

    def test_metadata_refresh_accepts_behavior_only_baseline(self):
        from unittest.mock import patch
        backup = {"tables": {
            "t_data_business_type_base": [{"code": "String", "id": 1}, {"code": "Bigint", "id": 2}],
            "t_business_type": [],
            "t_data_standard": [{"code": "sdm2_log", "id": 3}],
            "t_data_standard_info": [{"code": "sdm_event_behavior__meta_occur_time", "id": 4}],
            "t_data_standard_version": [],
            "t_data_standard_business_type_mapping": [],
        }}
        with patch.object(metadata, "ensure_agency_tags"), patch.object(metadata, "strip_synthetic_dam_table", return_value={}):
            metadata.upsert_behavior(backup, Path("unused"))
            first = {r["code"]: r["id"] for r in backup["tables"]["t_data_standard_info"]}
            metadata.upsert_behavior(backup, Path("unused"))
            second = {r["code"]: r["id"] for r in backup["tables"]["t_data_standard_info"]}
        self.assertEqual(first, second)
        self.assertIn("sdm_event_behavior__facets_process_syscall_return_value", second)

    def test_schema_documents_same_paths(self):
        defs = SCHEMA["$defs"]
        self.assertEqual(set(defs["process_facet"]["properties"]["syscall"]["properties"]),
                         {"number", "arch", "return_value"})
        self.assertEqual(defs["authentication_facet"]["properties"]["public_key"]
                         ["properties"]["fingerprint"]["required"], ["algorithm", "value"])


if __name__ == "__main__":
    unittest.main()
