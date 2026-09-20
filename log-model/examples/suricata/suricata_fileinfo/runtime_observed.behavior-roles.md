# suricata_fileinfo / runtime_observed 行为信封角色判定

句式：元数据服务 `192.0.2.72:80` 向 `192.0.2.128` 返回 `/heart_report.cgi` 74 字节；探针记 fileinfo。

| 角色 | 判定 | 证据 |
|---|---|---|
| subject | `endpoint` 192.0.2.72:80 | 文件字节发送方 src_* |
| object | `file` `/heart_report.cgi` size=74 | fileinfo.filename/size；无哈希不编造 md5 |
| carriers[] | 空 | HTTP 进 facets |
| observation | record | 不是检测 |

## 迁移裁决

- 与同 URL 的 suricata_http 拆事件，不合并。
- dest_ip 进 source_private.http_peer。

`mapping_id=suricata.suricata_fileinfo.behavior.v1`。
