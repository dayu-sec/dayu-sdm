# sxf_probe / flow_web 运行时观测候选映射

事件事实：源端通过 HTTP 访问 Web 资源。

主体：`source_host_or_ip`；客体：`target_host_or_url`；载体：`http_protocol`；观察者：来源产品。

> 状态：candidate，未注册、未批准。仅 WPL 解析事实已确认，SDM 语义仍需人工复核。

| WPL 字段 | 值 | SDM 候选路径 | 状态 |
|---|---|---|---|
| `DSReq` | `20250522` | `extensions_obj.source_private.DSReq` | `source_private` |
| `DSRsp` | `20250522` | `extensions_obj.source_private.DSRsp` | `source_private` |
| `HHReq` | `10` | `extensions_obj.source_private.HHReq` | `source_private` |
| `HHRsp` | `10` | `extensions_obj.source_private.HHRsp` | `source_private` |
| `afver` | `TS3.0.91.12428 Build20241231` | `extensions_obj.source_private.afver` | `source_private` |
| `appproto` | `HTTP` | `protocol` | `candidate` |
| `cookie` | `JSESSIONID=g545C2Tm9w183JfWFN52xgLaR7jLmiY85q8sU3mxGsUqCoaKXBkR!701969372` | `extensions_obj.source_private.cookie` | `source_private` |
| `devname` | `SANGFOR STA` | `extensions_obj.source_private.devname` | `source_private` |
| `ds` | `20250522` | `extensions_obj.source_private.ds` | `source_private` |
| `dst_ip` | `198.51.100.58` | `target_ip` | `candidate` |
| `dst_ip_req` | `198.51.100.58` | `extensions_obj.source_private.dst_ip_req` | `source_private` |
| `dst_ip_rsp` | `203.0.113.225` | `extensions_obj.source_private.dst_ip_rsp` | `source_private` |
| `dst_port` | `80` | `target_port` | `candidate` |
| `dst_port_req` | `80` | `extensions_obj.source_private.dst_port_req` | `source_private` |
| `dst_port_rsp` | `65127` | `extensions_obj.source_private.dst_port_rsp` | `source_private` |
| `duration` | `31` | `extensions_obj.source_private.duration` | `source_private` |
| `dzone` | `2` | `extensions_obj.source_private.dzone` | `source_private` |
| `expires` | `` | `extensions_obj.source_private.expires` | `source_private` |
| `hh` | `10` | `extensions_obj.source_private.hh` | `source_private` |
| `host` | `jh.tszscq.org` | `extensions_obj.source_private.host` | `source_private` |
| `iptype` | `4` | `extensions_obj.source_private.iptype` | `source_private` |
| `logid` | `47879314647529` | `extensions_obj.source_private.logid` | `source_private` |
| `logtype` | `http_session` | `extensions_obj.source_private.logtype` | `source_private` |
| `method` | `POST` | `http_method` | `candidate` |
| `referer` | `http://jh.tszscq.org/tskjjh/login/login!qtlogin.do` | `extensions_obj.source_private.referer` | `source_private` |
| `req_body` | `username=baijie661102&password=661102&yzm=7966` | `extensions_obj.source_private.req_body` | `source_private` |
| `req_body_len` | `46` | `extensions_obj.source_private.req_body_len` | `source_private` |
| `req_content_type` | `application/x-www-form-urlencoded` | `extensions_obj.source_private.req_content_type` | `source_private` |
| `req_head` | `POST /tskjjh/login/login!check.do?t=0.2378349116086358 HTTP/1.1\r\nHost: jh.tszscq.org\r\nConnection: keep-alive\r\nContent-Length: 46\r\nAccept: */*\r\nOrigin: http://jh.tszscq.org\r\nX-Requested-With: XMLHttpRequest\r\nUser-Agent: Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36\r\nContent-Type: application/x-www-form-urlencoded\r\nReferer: http://jh.tszscq.org/tskjjh/login/login!qtlogin.do\r\nAccept-Encoding: gzip, deflate\r\nAccept-Language: zh-CN,zh;q=0.8\r\nCookie: JSESSIONID=g545C2Tm9w183JfWFN52xgLaR7jLmiY85q8sU3mxGsUqCoaKXBkR!701969372\r\n\r\n` | `extensions_obj.source_private.req_head` | `source_private` |
| `req_len` | `628` | `extensions_obj.source_private.req_len` | `source_private` |
| `req_ts` | `1747879314120` | `extensions_obj.source_private.req_ts` | `source_private` |
| `rsp_body` | `5` | `extensions_obj.source_private.rsp_body` | `source_private` |
| `rsp_body_len` | `1` | `extensions_obj.source_private.rsp_body_len` | `source_private` |
| `rsp_content_type` | `` | `extensions_obj.source_private.rsp_content_type` | `source_private` |
| `rsp_head` | `HTTP/1.1 200 OK\r\nDate: Thu, 22 Nov 2018 01:38:16 GMT\r\nContent-Length: 1\r\nContent-Language: zh-CN\r\n\r\n` | `extensions_obj.source_private.rsp_head` | `source_private` |
| `rsp_len` | `101` | `extensions_obj.source_private.rsp_len` | `source_private` |
| `rsp_ts` | `1747879314123` | `extensions_obj.source_private.rsp_ts` | `source_private` |
| `server` | `` | `extensions_obj.source_private.server` | `source_private` |
| `src_ip` | `203.0.113.225` | `source_ip` | `candidate` |
| `src_ip_req` | `203.0.113.225` | `extensions_obj.source_private.src_ip_req` | `source_private` |
| `src_ip_rsp` | `198.51.100.58` | `extensions_obj.source_private.src_ip_rsp` | `source_private` |
| `src_port` | `65127` | `source_port` | `candidate` |
| `src_port_req` | `65127` | `extensions_obj.source_private.src_port_req` | `source_private` |
| `src_port_rsp` | `80` | `extensions_obj.source_private.src_port_rsp` | `source_private` |
| `status_code` | `200` | `extensions_obj.source_private.status_code` | `source_private` |
| `szone` | `2` | `extensions_obj.source_private.szone` | `source_private` |
| `transproto` | `TCP` | `protocol` | `candidate` |
| `ts` | `2025-05-22 02:01:54` | `occur_time` | `candidate` |
| `uid` | `3789395679` | `extensions_obj.source_private.uid` | `source_private` |
| `uri` | `/tskjjh/login/login!check.do?t=0.2378349116086358` | `extensions_obj.source_private.uri` | `source_private` |
| `user_agent` | `Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36` | `extensions_obj.source_private.user_agent` | `source_private` |
| `vendor` | `sangfor` | `extensions_obj.source_private.vendor` | `source_private` |

## 人工语义复核（SXF Probe）

- 事件事实：探针记录一次 HTTP POST 请求及 200 响应。
- `event_category=network`，`event_type=network_http`，`operation=empty`，`outcome=success`。
- 文档证据：深信服《潜伏威胁探针数据接口对外说明 V2.0》；运行样本已命中。
- 未确认的协议数字/命令字典保留原值并 report。
