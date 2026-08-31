# sxf_probe / flow_web SDM2 候选样例

事件事实：源端通过 HTTP 访问 Web 资源。

- 主体：`source_host_or_ip`
- 客体：`target_host_or_url`
- 载体：`http_protocol`
- 观察者：来源安全产品

## 证据与限制

- 原始样本：`log-model/examples/sxf_probe/` 第 2 个非空行。
- WPL 规则：`flow_web`，运行时解析成功。
- 字段映射和枚举为候选，未知枚举保留原值并报告。
- `outcome=unknown`；没有把 finding 或日志存在机械映射为 observed。
- 顶层 `severity` 为空；来源严重度不机械投影。
- logical/physical/projection 校验保持 partial，等待事件语义人工确认。

## 人工语义复核

- 事件事实：探针记录一次 HTTP POST 请求及 200 响应。
- `event_category=network`，`event_type=network_http`，`operation=empty`，`outcome=success`。
- 文档证据：深信服《潜伏威胁探针数据接口对外说明 V2.0》；运行样本已命中。
- 未确认的协议数字/命令字典保留原值并 report。
