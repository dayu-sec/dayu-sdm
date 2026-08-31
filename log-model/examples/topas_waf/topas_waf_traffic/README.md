# topas_waf / topas_waf_traffic SDM2 候选样例

事件事实：来源安全产品生成检测或防护记录；检测声明保存在 source_finding，具体 event_type 待按底层事件事实复核。

- 主体：`unknown`
- 客体：`unknown`
- 载体：`observer_product`
- 观察者：来源安全产品

## 证据与限制

- 原始样本：`log-model/examples/topas_waf/` 第 5 个非空行。
- WPL 规则：`topas_waf_traffic`，运行时解析成功。
- 字段映射和枚举为候选，未知枚举保留原值并报告。
- `outcome=unknown`；没有把 finding 或日志存在机械映射为 observed。
- 顶层 `severity` 为空；来源严重度不机械投影。
- logical/physical/projection 校验保持 partial，等待事件语义人工确认。

## 人工语义复核

- 事件事实：WAF 记录客户端向受保护服务器发起的一次 HTTPS GET 请求及响应状态。
- `event_category=network`
- `event_type=network_http`
- `operation=empty`
- `outcome=unknown`：不将来源处置或 HTTP 状态机械映射为底层动作结果。
- `log_level=emergent`：仅来自 `pri`，不作为安全严重度。
- 文档证据：天融信《waf2.0日志格式文档-v2.0》；`recorder=waf_traffic`，WPL 运行样本已命中。
