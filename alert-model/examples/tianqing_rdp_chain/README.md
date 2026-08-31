# 样例：天擎 RDP 爆破攻击链（POC 已写入）

一个虚构终端在 2026-08-20（UTC）09:55–10:09 的完整攻击链，共 11 条天擎日志：
6 条 `edr_alert_log` 告警 + 5 条行为佐证日志。已写入 POC Doris 库 `sdm2_log`。

生成器：`alert-model/scripts/build_tianqing_alert_examples.py`
（`--write-poc` 写入；表为唯一键，重复执行幂等覆盖）。
映射标准：`alert-model/standards/tianqing-source-alert-mapping.json`。

## 场景与时间线

| 时刻 (UTC) | 类型 | 日志 | 说明 |
|---|---|---|---|
| 09:55:00 | 告警 | `edr_alert_log` rdp_bruteforce | 203.0.113.1 RDP 爆破（T1110，LOW） |
| 09:58:20 | 告警 | `edr_alert_log` remote_login_failed | 同源 IP 远程登录失败（T1110，MEDIUM） |
| 10:02:10 | 告警 | `edr_alert_log` account_password_change | 账户 NetUser 被改密（T1098，LOW） |
| 10:03:30 | 佐证 | `edr_process_event` process_creation | cmd.exe(6585) 创建 curl.exe(5041) |
| 10:04:00 | 告警 | `edr_alert_log` remote_process_start | PsExec 横向移动（T1570，HIGH） |
| 10:05:00 | 佐证 | `edr_powershell_cmd_exec` | PowerShell 从 203.0.113.15 拉取 a.ps1 |
| 10:06:00 | 佐证 | `edr_process_inject` | services.exe 注入 TrustedInstaller.exe |
| 10:06:40 | 佐证 | `edr_dns_access` dns_query | nslookup 解析 blaxaplayer.com → 203.0.113.15 |
| 10:07:10 | 告警 | `edr_alert_log` malicious_domain_access | 恶意域名 C2（T1041，HIGH，AridViper IOC） |
| 10:07:40 | 佐证 | `edr_file_op` file_write | curl.exe 落盘 C:\Users\Public\update.exe |
| 10:09:00 | 告警 | `edr_alert_log` ip_detection | 203.0.113.15 远控木马回连（T1071，HIGH） |

- 统一终端：`DESKTOP-FIN-0457` / 192.0.2.111 / mid、mac、gid、asset_id 见 `scenario.json`
- 攻击源：203.0.113.1；C2：blaxaplayer.com（203.0.113.15）
- 佐证日志进程链与告警 `process_details` 交叉一致（curl.exe pid 5041/md5 eac53dda…、
  cmd.exe pid 6585、nslookup.exe pid 5683/md5 f2e3950c…）

## POC 落库（库 `sdm2_log`）

| 表 | 行数 | 内容 |
|---|---|---|
| `sdm_event` | 11 | 告警类 record_kind=finding，佐证类 record_kind=event；tenant01 |
| `raw_log` | 11 | 改写后原始日志全文（sha256 摘要） |
| `sdm_alert` | 6 | SOURCE_ALERT 导入，全部 `verdict=UNKNOWN`、`case_id=NULL` |
| `sdm_evidence` | 18 | 每告警 TRIGGER(EVENT) + CONTEXT(SOURCE_ALERT) + CONTEXT(RAW_LOG) |
| `sdm_alert_entity` | 12 | victim host（主实体，参与编组）+ attacker/indicator |

六条告警共享 `correlation_id = corr_926d90ade77366dc`
（family=tianqing_rdp_bruteforce_chain，首末 14 分钟 < 15 分钟窗），
按 `docs/06-runtime-pipeline.md` §1.1 案件编组规则走 correlation_id 强关联，
必然归入同一 Case。佐证日志只写 `sdm_event`，由 Case Service 证据收集
（§1.2）按 tenant+host+时间窗检索——验证查询：

```sql
SELECT COUNT(*) FROM sdm_event
WHERE tenant_id='tenant01'
  AND (target_host='DESKTOP-FIN-0457' OR source_host='DESKTOP-FIN-0457')
  AND occur_time BETWEEN '2026-08-20 09:50:00' AND '2026-08-20 10:15:00';
-- 11：6 告警事件 + 5 佐证事件全部可检索
```

## 边界（与后续流程的分工）

- 不写 `case_id`、`sdm_case`、`sdm_analysis`、`sdm_workflow_action`：
  编组、研判、处置由 Case Service 与告警轮负责。
- `verdict` 恒 UNKNOWN；天擎侧 `status` 只进 `extensions.source_finding`。
- INSERT 通道写入的 VARIANT 列子列不可下钻（cast 整列 JSON 可读），
  与库内既有 ngsoc 行为一致；生产 Routine Load 通道不受影响。
