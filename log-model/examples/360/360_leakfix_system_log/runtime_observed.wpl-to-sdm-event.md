# 360 / 360_leakfix_system_log 运行时观测候选映射

事件事实：终端 `DESKTOP-41B7VL6` 的漏洞修复状态结果显示 `KB5012170` 未修复；这是来源漏洞发现，不扩写为扫描完成或补丁安装动作。

主体：`none`；客体：`affected_endpoint_host`；载体：`none`；观察者：360 EPP。

> 状态：`candidate_reviewed_not_registered`。语义已按厂商文档与运行样本复核，但尚未注册为正式标准映射。

| WPL 字段 | 值 | SDM 候选路径 | 状态 |
|---|---|---|---|
| `asset_username` | `hsakdjklas#@$%阿利克水泥钉金卡三年` | `extensions_obj.source_private.asset_username` | `source_private` |
| `clientip` | `203.0.113.37` | `roles_obj.target.host.ip + target_ip` | `mapped` |
| `computername` | `DESKTOP-41B7VL6` | `roles_obj.target.host.name + target_host` | `mapped` |
| `ctime` | `2026-01-23 11:00:00` | `occur_time` | `candidate` |
| `deleted` | `0` | `extensions_obj.source_private.deleted` | `source_private` |
| `id` | `25366` | `source_finding_obj.original_id` | `mapped` |
| `ignoredate` | `test-ignoredate` | `extensions_obj.source_private.ignoredate` | `source_private` |
| `inactivity` | `test-inactivity` | `extensions_obj.source_private.inactivity` | `source_private` |
| `installdate` | `2026-01-23 11:00:00` | `extensions_obj.source_private.installdate` | `source_private` |
| `is_xc` | `2` | `extensions_obj.source_private.is_xc` | `source_private` |
| `kbid` | `KB5012170` | `source_finding_obj.vulnerabilities[0].id` | `mapped` |
| `type` | `unrepaired` | `source_finding_obj.status + vulnerabilities[0].type` | `mapped` |
| `ltime` | `2026-01-23 11:00:00` | `extensions_obj.source_private.ltime` | `source_private` |
| `m2` | `d44c516424161ff6d943dd0da127b34ec736cf5029a0` | `extensions_obj.source_private.m2` | `source_private` |
| `mtime` | `2026-01-23 11:00:00` | `extensions_obj.source_private.mtime` | `source_private` |
| `name` | `test-name` | `source_finding_obj.title + vulnerabilities[0].name` | `mapped` |
| `name_md5` | `3d87ad735bbf64e096acd98814424e4a` | `extensions_obj.source_private.name_md5` | `source_private` |
| `plat_id` | `1` | `extensions_obj.source_private.plat_id` | `source_private` |
| `publishdate` | `2026-01-23 11:00:00` | `extensions_obj.source_private.publishdate` | `source_private` |
| `repair_suggestions` | `test-repair_suggestions` | `source_finding_obj.vulnerabilities[0].remediation` | `mapped` |
| `severitylevel` | `高危漏洞` | `source_finding_obj.severity` | `mapped` |
| `severitylevel_detail` | `0` | `extensions_obj.source_private.severitylevel_detail` | `source_private` |
| `status` | `unrepaired` | `extensions_obj.source_private.status_raw` | `conflicted` |
| `status_code` | `test-status_code` | `extensions_obj.source_private.status_code` | `source_private` |
| `summary` | `test-summary` | `source_finding_obj.vulnerabilities[0].description` | `mapped` |
| `sysmaclist` | `00:00:5E:00:53:19` | `roles_obj.target.host.mac` | `mapped` |
| `updateid` | `33263bb7-a99d-45ec-93c2-2bbef2e97449` | `extensions_obj.source_private.updateid` | `source_private` |
| `username` | `admin` | `roles_obj.target.user.name + target_user` | `mapped` |
| `vendors` | `test-vendors` | `extensions_obj.source_private.vendors` | `source_private` |

## 人工语义复核（360 EPP）

- 事件事实：终端 DESKTOP-41B7VL6 的漏洞修复状态结果显示 KB5012170 未修复；这是来源漏洞发现，不扩写为扫描完成或补丁安装动作。
- 对应文档：4. 系统漏洞日志（漏洞日志）（6230 及后续版本）；证据状态 `vendor_confirmed_and_observed`。
- 受影响客体为终端 `DESKTOP-41B7VL6`；`KB5012170` 作为漏洞/补丁关联 ID，不冒充 CVE。
- `type=unrepaired` 是文档明确的漏洞状态；`status=unrepaired` 不在文档操作状态枚举中，冲突保留为 `status_raw`。
- 本条没有扫描批次或扫描完成动作，保留 `event_type=generic_event`、`operation=empty`、`outcome=unknown`。
- 来源等级只进入 `source_finding.severity`，顶层 `severity` 保持为空。
