# topas_ips / topas_ips_virus SDM2 候选样例

事件事实：恶意软件检测——源端点 198.51.100.96:20 经 FTP STOR 向 203.0.113.228:49946 传输恶意 EXE 文件（code哼red2.exe，md5=13296f…574，大小 8192）。recorder=virus，op=alert。

- 主体：源端点 → `roles.source.endpoint(198.51.100.96:20)`
- 客体：被传输恶意文件 → `roles.related[].file`（malware_file）；接收端点 → `roles.target.endpoint(203.0.113.228:49946)`
- 载体：网络协议 → `facets.network.protocol.code=TCP` + `direction=c2s`；应用 → `facets.application.name=ftp`
- 检测声明：`source_finding_obj{original_id=sid, title, count=repeat, action=op, rule{signature_id=sid, label=rule}}`
- 观察者：来源安全产品

## 证据与限制

- 原始样本：`log-model/examples/topas_ips/` 第 2 个非空行。
- WPL 规则：`topas_ips_virus`，运行时解析成功。
- 字段映射和枚举为候选，未知枚举保留原值并报告。
- `outcome=unknown`；op=alert 是来源处置，不是已确认的底层动作结果。
- 顶层 `severity` 为空；来源严重度不机械投影。

## 人工语义复核（TopIDP v3，SR-041）

- 事件事实：恶意软件检测日志是来源发现；op=alert 仅保留来源处置。
- event_category：`alert`
- event_type：`generic_event`（06 无恶意软件检测专用类型）
- operation：`空`
- outcome：`unknown`（op=alert 是来源处置）
- 主体/客体/载体：source_endpoint / malware_file（related）+ target_endpoint / network_protocol
- 检测声明：`source_finding_obj`（title/rule/count/action）
- 证据：TopIDP v3 §3.4.4 恶意软件日志，`recorder=virus`；WPL 运行样本已命中。

## 当前物理注册表迁移

- expected 已按当前 `sdm_event.yaml` 87 字段物理注册表收敛。
- 热字段 `source_ip/target_ip` 保留标量投影；完整端点对象在 `roles_obj`。
- 协议与应用类型入 `facets_obj`（registry 已注册路径）。
- 恶意文件入 `roles.related[].file`（relation_type=malware_file）。
