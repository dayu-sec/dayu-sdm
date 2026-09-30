"""facets.http.request.path/query：HTTP request-target 上下文边界与登记一致性守护。"""
import copy
import importlib.util
import json
import re
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[3]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


validator = load("http_target_validator", ROOT / "log-model/scripts/validate_behavior_event.py")
metadata = load("http_target_metadata", ROOT / "log-model/scripts/generate_metadata_backup.py")
build_pages = load("http_target_build_pages", ROOT / "pages/build/build_pages.py")
SCHEMA = json.loads(validator.SCHEMA.read_text())
FIELDS = json.loads(validator.FIELDS.read_text())
EXAMPLES = ROOT / "log-model/examples/http-request-target"
CATALOG = ROOT / "docs/SDM事件模型逻辑契约字段目录.md"

# TYPICAL_FACETS 中的既有漂移：与本轮 HTTP request-target 无关，需要单独议题处理。
# 只允许这个清单保留；新增未登记路径必须补 §2.8 或先移除，不得继续往这里追加。
KNOWN_DRIFT = {
    "facets.network.src_ip",                # 地址属于主体/客体，不应是 facet
    "facets.network.src_port",
    "facets.registry.value.current.data",
}


def catalog_facet_paths() -> set[str]:
    """字段目录 §2.8 的 facet 路径（复用页面渲染用的解析器，含 [] / .* 通配写法）。"""
    return {p["path"] for d in build_pages.facet_domains() for p in d["paths"]}


def covered(path: str, rows: set[str]) -> bool:
    """目录条目可写父对象[]、通配 .* 或完整路径；子叶子以父条目为前缀即算已登记。"""
    for row in rows:
        base = row.replace("[]", "")
        if base.endswith(".*"):
            if path.startswith(base[:-2]):
                return True
        elif path == row or path.startswith(base + ".") or path.startswith(base + "["):
            return True
    return False


class HttpRequestTargetTests(unittest.TestCase):
    def setUp(self):
        self.event = json.loads(
            (EXAMPLES / "request-target.expected-sdm-event.behavior.json").read_text())

    def request(self):
        return self.event["facets"]["http"]["request"]

    def test_examples(self):
        for p in EXAMPLES.glob("*.expected-sdm-event.behavior.json"):
            self.assertEqual(validator.validate_one(p, SCHEMA, FIELDS), [], str(p))

    def test_events_without_new_fields_still_valid(self):
        self.request().pop("path")
        self.request().pop("query")
        self.event.pop("object")
        self.assertEqual(validator.check_http_request_target_extensions(self.event), [])

    def test_path_must_be_origin_form(self):
        for bad in ("search", "example.com:443", "", 5, True):
            self.request()["path"] = bad
            self.assertTrue(validator.check_http_request_target_extensions(self.event), bad)
        self.request()["path"] = "*"       # OPTIONS 星号形式保留原值
        self.assertEqual(validator.check_http_request_target_extensions(self.event), [])
        self.request()["path"] = "/search"

    def test_path_must_not_carry_query(self):
        self.request()["path"] = "/search?q=1"
        self.assertTrue(validator.check_http_request_target_extensions(self.event))

    def test_query_has_no_leading_question_mark(self):
        self.request()["query"] = "?q=1"
        self.assertTrue(validator.check_http_request_target_extensions(self.event))
        self.request()["query"] = "q=xmr%2Epool&sort=desc"

    def test_fragment_is_not_a_separator(self):
        for name, value in (("path", "/a#b"), ("query", "q=1#b")):
            bad = copy.deepcopy(self.event)
            bad["facets"]["http"]["request"][name] = value
            self.assertTrue(validator.check_http_request_target_extensions(bad), (name, value))

    def test_does_not_duplicate_object_url(self):
        bad = copy.deepcopy(self.event)
        bad["object"] = {"ref_id": "url::https://portal.example.com/search",
                         "entity_type": "url",
                         "url": {"full": "https://portal.example.com/search?q=1"}}
        self.assertTrue(validator.check_http_request_target_extensions(bad))
        ok = copy.deepcopy(bad)
        ok["facets"]["http"]["request"].pop("path")
        ok["facets"]["http"]["request"].pop("query")
        self.assertEqual(validator.check_http_request_target_extensions(ok), [])

    def test_empty_values_are_omitted_not_written(self):
        for name in ("path", "query"):
            bad = copy.deepcopy(self.event)
            bad["facets"]["http"]["request"][name] = ""
            self.assertTrue(validator.check_http_request_target_extensions(bad), name)

    def test_catalog_lists_both_leaves(self):
        rows = catalog_facet_paths()
        self.assertIn("facets.http.request.path", rows)
        self.assertIn("facets.http.request.query", rows)

    def test_metadata_facets_are_registered(self):
        """生成器不得自行发明字段目录未登记的 facet（既有漂移除外，见 KNOWN_DRIFT）。"""
        rows = catalog_facet_paths()
        missing = {path for path, _cname, _desc in metadata.TYPICAL_FACETS if not covered(path, rows)}
        self.assertEqual(missing - KNOWN_DRIFT, set())

    def test_metadata_refresh_includes_new_leaves(self):
        from unittest.mock import patch
        backup = {"tables": {
            "t_data_business_type_base": [{"code": "String", "id": 1}],
            "t_business_type": [],
            "t_data_standard": [{"code": "sdm2_log", "id": 3}],
            "t_data_standard_info": [{"code": "sdm_event_behavior__meta_occur_time", "id": 4}],
            "t_data_standard_version": [],
            "t_data_standard_business_type_mapping": [],
        }}
        with patch.object(metadata, "ensure_agency_tags"), \
                patch.object(metadata, "strip_synthetic_dam_table", return_value={}):
            metadata.upsert_behavior(backup, Path("unused"))
            codes = {r["code"] for r in backup["tables"]["t_data_standard_info"]}
        self.assertTrue({"sdm_event_behavior__facets_http_request_path",
                         "sdm_event_behavior__facets_http_request_query"} <= codes)


if __name__ == "__main__":
    unittest.main()
