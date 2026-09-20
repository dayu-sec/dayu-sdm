# suricata_fileinfo 行为信封映射

样例：`runtime_observed.expected-sdm-event.behavior.json`
`mapping_id=suricata.suricata_fileinfo.behavior.v1`
对标：topas_ips_audit_file（文件元数据，非病毒检出）

WPL 尚未编写；来源列为 EVE JSON 键。夹具用内层 EVE。

| 来源 | 值 | SDM 路径 | 状态 |
|---|---|---|---|
| `src_ip` | `192.0.2.72` | `subject.endpoint` | mapped |
| `fileinfo.filename` | `/heart_report.cgi` | `object.file.name` | mapped |
| `fileinfo.size` | `74` | `object.file.size` | mapped |

校验待跑。
