# 360 / 360_leakfix_system_log SDM2 候选样例

事件事实：终端 `DESKTOP-41B7VL6` 的漏洞修复状态结果显示 `KB5012170` 未修复；这是来源漏洞发现，不扩写为扫描完成或补丁安装动作。

- 主体：无独立行为主体
- 客体：受影响终端 `DESKTOP-41B7VL6`（用户上下文 `admin`）
- 载体：无
- 观察者：360 EPP

## 证据与限制

- 原始样本：`log-model/examples/360/` 第 8 个非空行。
- WPL 规则：`360_leakfix_system_log`，运行时解析成功。
- 字段映射和枚举为候选，未知枚举保留原值并报告。
- `outcome=unknown`；没有把 finding 或日志存在机械映射为 observed。
- 顶层 `severity` 为空；来源严重度不机械投影。
- 文档第 4 节明确说明这是漏洞扫描后上报的“漏洞修复情况结果日志”；本条记录本身没有扫描批次或扫描完成动作，因此保留 `generic_event`。
- `type=unrepaired` 按文档映射为漏洞生命周期状态；样例 `status=unrepaired` 不在文档列出的操作状态枚举中，作为冲突原值保留，不映射顶层 `outcome`。
- 该旧版物理 expected 样例不内嵌 `raw_msg`；原始载荷完整保存在 `runtime_observed.raw-log.json`。
- 未提供独立逻辑五层事件，因此 `logical_schema=not_run`；物理事件通过注册校验，`projection_consistency=partial`。

## 人工语义复核

- 事件事实：终端 DESKTOP-41B7VL6 的漏洞修复状态结果显示 KB5012170 未修复；这是来源漏洞发现，不扩写为扫描完成或补丁安装动作。
- 对应文档：4. 系统漏洞日志（漏洞日志）（6230 及后续版本）；证据状态 `vendor_confirmed_and_observed`。
- 受影响客体为终端 `DESKTOP-41B7VL6`；`KB5012170` 作为漏洞/补丁关联 ID，不冒充 CVE。
- `type=unrepaired` 是文档明确的漏洞状态；`status=unrepaired` 不在文档操作状态枚举中，冲突保留为 `status_raw`。
- 本条没有扫描批次或扫描完成动作，保留 `event_type=generic_event`、`operation=empty`、`outcome=unknown`。
- 来源等级只进入 `source_finding.severity`，顶层 `severity` 保持为空。
