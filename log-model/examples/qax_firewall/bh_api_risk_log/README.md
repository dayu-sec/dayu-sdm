# qax_firewall / bh_api_risk_log SDM2 候选样例

事件事实：用户 `admin` 从来源地址访问堡垒机 API `/3.0/authService/config`，因后台登录密码错误命中 API 风险检测；来源产品声明该访问已拦截。

- 主体：用户 `admin`（来源地址 `192.xxx.xxx.20`）
- 客体：API 资源 `/3.0/authService/config`
- 载体：HTTP（日志未提供 HTTP 方法）
- 观察者：奇安信堡垒机

## 证据与限制

- 原始样本：`s4-doris/models/wpl/qax_firewall/sample.dat` 第 7 个非空行。
- WPL 规则：`bh_api_risk_log`，运行时解析成功。
- 字段映射和枚举为候选，未知枚举保留原值并报告。
- `outcome=unknown`；没有把 finding 或日志存在机械映射为 observed。
- 顶层 `severity` 为空；来源严重度不机械投影。
- `accessApi` 是相对路径，映射到目标 API 资源及 `facets.http.request.path`，不扩写成完整 URL。
- `result=已拦截`、`ipStatus=封停` 是来源安全控制结论，不作为底层 HTTP `outcome`。
- 该旧版物理 expected 样例不内嵌 `raw_msg`；原始载荷完整保存在 `runtime_observed.raw-log.json`，因此严格样例校验保留一条已解释警告。
- 未提供独立逻辑五层事件，logical/projection 校验保持 partial。

## 人工语义复核

- 事件事实：用户 `admin` 从来源地址访问堡垒机 API `/3.0/authService/config`，因后台登录密码错误命中 API 风险检测；来源产品声明该访问已拦截。
- event_category：`alert`
- event_type：`network_http`
- operation：`空；无充分标准动作证据`
- outcome：`unknown`；来源“已拦截”保存在 `source_finding.action`
- 证据：奇安信堡垒机 192.0.2.70 Syslog 格式说明 KB47750；对应 `logType` 为 `YAB_API_RISK_LOG`。
- 状态：`reviewed_candidate`
