# `edr_dns_access` 字段缺口

- 当前样例没有 DNS 服务器地址、源端口、目标端口和传输协议，不能补造 UDP/53 网络五元组。
- `dns_typed=1` 按 DNS 标准类型代码映射为 A 记录；仍需补充 AAAA、CNAME、MX、TXT 等真实样例。
- `dns_query_status=0` 且存在应答，当前映射为成功；非零状态码需要天擎枚举或更多样例确认。
- `dns_query_results` 当前只有单个 IPv4 字符串；需要补充多应答、IPv6、CNAME 链和空应答样例。
- `dns_host_name_md5` 可由查询名称稳定计算，不重复保存。
