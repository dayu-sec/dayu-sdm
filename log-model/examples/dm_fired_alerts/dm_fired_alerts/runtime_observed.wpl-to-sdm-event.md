# dm_fired_alerts / dm_fired_alerts 运行时观测候选映射

事件事实：来源安全产品生成检测或防护记录；检测声明保存在 source_finding，具体 event_type 待按底层事件事实复核。

主体：`unknown`；客体：`unknown`；载体：`observer_product`；观察者：来源产品。

> 状态：candidate，未注册、未批准。仅 WPL 解析事实已确认，SDM 语义仍需人工复核。

| WPL 字段 | 值 | SDM 候选路径 | 状态 |
|---|---|---|---|
| `ACTION_ID` | `a016e3ec83cf2b680183d05073b5007b` | `extensions_obj.source_private.ACTION_ID` | `source_private` |
| `ACTION_NAME` | `数据归集子系统-数据不可达` | `extensions_obj.source_private.ACTION_NAME` | `source_private` |
| `APP_NAME` | `isoc` | `extensions_obj.source_private.APP_NAME` | `source_private` |
| `CATEGORY` | `故障告警` | `extensions_obj.source_private.CATEGORY` | `source_private` |
| `CONTENT` | `数据归集子系统-数据不可达:上次收数时间为18.12天以前` | `extensions_obj.source_private.CONTENT` | `source_private` |
| `ID` | `a016e3ec8585b5680185fc1cb6570143` | `extensions_obj.source_private.ID` | `source_private` |
| `LATEST_TIME` | `2023-01-29 06:00:18` | `extensions_obj.source_private.LATEST_TIME` | `source_private` |
| `LEVEL` | `1` | `extensions_obj.source_private.LEVEL` | `source_private` |
| `NAME` | `该数据源24小时未更新` | `extensions_obj.source_private.NAME` | `source_private` |
| `RECORDING_TIME` | `2023-01-29 06:00:18.261` | `extensions_obj.source_private.RECORDING_TIME` | `source_private` |
| `SOURCE_SCHEMA` | `ARCANA` | `extensions_obj.source_private.SOURCE_SCHEMA` | `source_private` |
| `SOURCE_TABLE` | `FIRED_ALERTS` | `extensions_obj.source_private.SOURCE_TABLE` | `source_private` |
| `STATUS` | `1` | `outcome` | `candidate` |
| `warp_parse_table` | `FIRED_ALERTS` | `extensions_obj.source_private.warp_parse_table` | `source_private` |
