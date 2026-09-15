# Changelog

本仓库按标准版本发布，每次发布打 tag（`vX.Y.Z`）并在此记录变更。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，
版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)：

- 标准语义或 schema 破坏性变更 → 主版本
- 新增字段/枚举/表/厂商映射 → 次版本
- 文档修正与澄清 → 修订版本

## [Unreleased]

### Changed

- 介绍页与文档地图改为行为信封 2.0（`sdm_event_behavior` / 07 Schema）。
- 公开权威为字段目录 + 07 / 07K / 031。
- 公开仓移除五层 `sdm_event` / hybrid-v1 对照文件；手册枚举只保留 07 闭合枚举。
- 告警标准页同步上游口径：上游事实层改 `sdm_event_behavior`；来源告警投影物理列改
  `assertion_*` / `observation_detail`、`subject_detail` / `object_detail`、`facets`，
  实体候选链按 02 §3 收敛；实体表 `valid_until` 改 `DATETIME(3)`，
  `asset_id` / `risk_context` 语义补全；接入样例事件改为 2.0 信封。

### Added

- 首次公开发布：日志模型（log-model）、告警模型（alert-model）、
  跨领域设计文档（docs/）。
- 2.0 行为样例补发（脱敏）：`log-model/examples/ngsoc/ngsoc_alert_info/sql_injection_attempt/`
  与 `alert-model/examples/tianqing_rdp_chain/sdm-events/` 的 `*.expected-sdm-event.behavior.json`。

### Fixed

- 告警页接入样例「查看原文件」链接：修正指向仓外的 `../../log-model/...` 相对路径，
  补齐样例所指的 2.0 行为样例文件。

### Security

- 样例与介绍页脱敏：口令、邮箱、真实域名/主机、公网 IP、会话 Cookie。
- 导出流水线去掉 POC SQL、客户容量实测、内部路径引用。
