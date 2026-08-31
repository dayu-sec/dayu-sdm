# sxf_probe / flow_dns SDM2 候选样例

事件事实：源端发起或接收 DNS 活动。

- 主体：`source_host_or_ip`
- 客体：`dns_name_or_server`
- 载体：`dns_protocol`
- 观察者：来源安全产品

## 证据与限制

- 原始样本：`s4-doris/models/wpl/sxf_probe/sample.dat` 第 4 个非空行。
- WPL 规则：`flow_dns`，运行时解析成功。
- 字段映射和枚举为候选，未知枚举保留原值并报告。
- `outcome=unknown`；没有把 finding 或日志存在机械映射为 observed。
- 顶层 `severity` 为空；来源严重度不机械投影。
- logical/physical/projection 校验保持 partial，等待事件语义人工确认。

## 人工语义复核

- 事件事实：探针记录一次 DNS PTR 查询，rcode=0 表示该 DNS 响应无错误。
- `event_category=network`，`event_type=network_dns`，`operation=query`，`outcome=success`。
- 文档证据：深信服《潜伏威胁探针数据接口对外说明 V2.0》；运行样本已命中。
- 未确认的协议数字/命令字典保留原值并 report。
