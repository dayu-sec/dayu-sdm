# HTTP request-target 契约样例

本目录是**脱敏构造的契约测试样例**，不是生产日志，也不宣称解析规则已经上线。域名、路径与查询串均为示例值。

- `request-target.expected-sdm-event.behavior.json`：一次 HTTP 事务。`path=/search`、`query=q=xmr%2Epool&sort=desc` 来自同一条 request-target，`host=portal.example.com` 是 Host 头，两端 endpoint 仍占 subject/object。

## 语义边界

`facets.http.request.path` / `facets.http.request.query` 承载**本次 HTTP 事务的 request-target 上下文**，不是 URL 实体身份：

| 输入（来源 request-target） | path | query | 说明 |
|---|---|---|---|
| `/a/b` | `/a/b` | 省略 | origin-form |
| `/a/b?x=1&y=2` | `/a/b` | `x=1&y=2` | 只按第一个 `?` 拆分 |
| `*` | `*` | 省略 | OPTIONS 星号形式，保留原值 |
| `example.com:443` | 不写 | 不写 | CONNECT authority-form，原值留 `extensions.source_private` |
| `/a#b`、空串、其它异常 | 不写 | 不写 | request-target 不含 fragment；异常形态不臆造拆分 |

- 只按第一个 `?` 拆分，**不把 `#` 当分隔符**；出现字面 `#` 视为异常，原值留 `extensions.source_private.http_url` 或 raw_log。
- 不 URL decode、不做路径归一化、不排序参数、不改变大小写；保留原始百分号编码。
- 来源给出绝对 URL 且 URL 被裁定为事件主要客体时走 `object.url.full/path/query`；**同一事实不得**同时写在 facet 与 `object.url`。
- 多值 request-target（如 `urls[]`）不得只取第一个；原数组留 `extensions.source_private`，或拆成多条事件。

## 敏感数据

`query` 常含 token、session、邮箱、手机号、签名参数。升到标准 facet 后进入通用查询与展示面，须按敏感 HTTP 数据执行字段级访问控制与展示遮罩；不得为检索便利做 URL decode 或键值展开。超长或敏感查询串保留原文证据引用，标准 facet 是否截断由来源契约明确，禁止静默截断。

## 版本

`path` / `query` 是开放 facet 域内的可选叶子补登记，不改 07 结构、无 DDL 标量列、无必填与闭集变更，保持 `meta.schema_version=2.0`。映射开始实际写入这两个叶子时，相关 OML 必须换新的 `mapping_id`。

## 已知实现差距

2026-09-30 本地实测（warp-parse 0.27.1-alpha）：写入链不在 facet 层省略空值，非 origin-form（`*`、CONNECT authority-form）与空值情形下 `path` / `query` 落库为**空串**；同结构的 `facets.http.request.host` / `.method` 行为一致。查询侧须把空串与缺失一并视为无值。

拆分实现见 `warp-rule/models/oml/suricata/{suricata_http,suricata_alert,suricata_fileinfo}/adm.oml`（`url()` 管道 + 占位 base），原串继续保留在 `extensions.source_private.http_url`；WPL 无法承担该拆分（实测 `take()` 不支持嵌套 JSON 路径字段，`{...}` 分隔符模式未实现）。

验证：`python3 log-model/contracts/scripts/test_http_request_target_extension.py`。
