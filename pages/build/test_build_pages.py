import unittest

import build_pages


class FieldCoverageTests(unittest.TestCase):
    def test_combined_paths_and_description_are_separate(self):
        text = """### 2.8 `facets`
| dns | `facets.dns.answers[].name` / `.type` / `.class` / `.ttl` | 参照 `facets.dns.question` |
| email | `facets.email.date` / `sender` / `client.user_agent` | 邮件头 |
| network | `facets.network.source_zone` / `facets.network.target_zone` | 区域 |
| network | `facets.network.nat.original/translated.*` | 转换 |
### 2.9 Other
| dns | `facets.dns.not_registered_here` | 忽略 |
"""
        domains = {d["domain"]: d["paths"] for d in build_pages.facet_domains(text)}
        self.assertEqual([p["path"] for p in domains["dns"]], [
            "facets.dns.answers[]." + leaf for leaf in ("name", "type", "class", "ttl")])
        self.assertEqual([p["path"] for p in domains["email"]], [
            "facets.email.date", "facets.email.sender", "facets.email.client.user_agent"])
        self.assertEqual(domains["network"][1]["path"], "facets.network.target_zone")
        self.assertTrue(domains["network"][2]["pattern"])

    def test_registered_nested_fields_are_visible(self):
        types = {t["type"]: t for t in build_pages.object_types()}
        endpoint = {f["name"] for f in types["endpoint"]["displayFields"]}
        self.assertTrue({"geo.country", "system.id", "organization.name"} <= endpoint)
        process = {f["name"] for f in types["process"]["displayFields"]}
        self.assertTrue({"pid", "user.name", "file.hashes.sha256"} <= process)

    def test_network_session_and_traffic_registration(self):
        paths = {p["path"] for d in build_pages.facet_domains() for p in d["paths"]}
        expected = {"facets.network.session." + leaf for leaf in
                    ("start_time", "end_time", "duration_seconds")}
        expected |= {"facets.network.traffic." + leaf for leaf in
                     ("bytes_in", "bytes_out", "total_bytes", "request_bytes",
                      "request_packets", "response_bytes", "response_packets")}
        self.assertTrue(expected <= paths)
        self.assertNotIn("facets.file.remote_path", paths)
        self.assertNotIn("facets.network.nat.type", paths)

    def test_host_core_extensions_are_visible(self):
        paths = {p["path"] for d in build_pages.facet_domains() for p in d["paths"]}
        self.assertTrue({"facets.process.syscall.number", "facets.process.syscall.arch",
                         "facets.process.syscall.return_value", "facets.process.terminal",
                         "facets.authentication.public_key.algorithm",
                         "facets.authentication.public_key.fingerprint.algorithm",
                         "facets.authentication.public_key.fingerprint.value"} <= paths)
        types = {t["type"]: t for t in build_pages.object_types()}
        self.assertTrue({"auid", "euid"} <= {f["name"] for f in types["process"]["displayFields"]})

    def test_http_request_target_fields_are_visible(self):
        paths = {p["path"] for d in build_pages.facet_domains() for p in d["paths"]}
        self.assertTrue({"facets.http.request.path", "facets.http.request.query"} <= paths)

    def test_cwp_activity_extensions_are_visible(self):
        paths = {p["path"] for d in build_pages.facet_domains() for p in d["paths"]}
        self.assertIn("facets.file.accessed_time", paths)
        types = {t["type"]: t for t in build_pages.object_types()}
        file_fields = {f["name"] for f in types["file"]["displayFields"]}
        self.assertTrue({"mode", "owner.uid", "owner.name", "group.uid", "group.name"} <= file_fields)
        process_fields = {f["name"] for f in types["process"]["displayFields"]}
        self.assertTrue({"real_group.uid", "real_group.name", "file.mode", "file.owner.uid", "file.group.uid"} <= process_fields)

    def test_cwp_alert_effective_group_is_visible(self):
        types = {t["type"]: t for t in build_pages.object_types()}
        fields = {f["name"] for f in types["process"]["displayFields"]}
        self.assertTrue({"egid", "euid", "real_group.uid", "file.mode"} <= fields)

    def test_current_dns_record_fields_are_covered(self):
        paths = {p["path"] for d in build_pages.facet_domains() for p in d["paths"]}
        self.assertTrue({"facets.dns.answers[]." + leaf for leaf in
                         ("name", "type", "class", "ttl")} <= paths)


if __name__ == "__main__":
    unittest.main()
