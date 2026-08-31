# NGSOC 映射契约

`ngsoc-mapping-contract.v1.json` 是 `qax/ngsoc` 两种日志类型的映射审计契约，适用于 `format_version=1`。

厂商格式文档对照见 [`22-ngsoc-vendor-doc-crosswalk.md`](22-ngsoc-vendor-doc-crosswalk.md)。其中 `ngsoc_threat_alert_send` 按 `NGSOC-4.13.1` 外发格式核对，`ngsoc_alert_info` 仍按独立的历史 KV 格式核对。

接入开发使用的精简字段映射见 [`23-ngsoc-log-mapping-brief.md`](23-ngsoc-log-mapping-brief.md)。

它固定三件事：

- `roles`、`facets` 中的规范路径，以及何时生成 `source_ip`、`target_ip`、`source_port`、`target_port` 标量投影；
- `attackResult`、`killchain`、`compromiseState`、`attCk`、`commDirection` 的字典状态、原值留存和未命中策略；
- `domain` 为纯域名、URI authority 或 `IP:port` 时的解析边界。

当前 interim 物理契约不再提供 `network_direction` 标量列，方向只写 `facets.network.direction`。旧样例中的该键由审计器报告为迁移项，不应继续写入新的事件。

运行审计：

```bash
python3 log-model/scripts/audit_ngsoc_mapping_contract.py
```

样例重新生成后，先应用确定性的契约元数据修复：

```bash
python3 log-model/scripts/repair_ngsoc_mapping_contract.py
python3 log-model/scripts/migrate_ngsoc_retired_scalars.py
python3 log-model/scripts/augment_mapping_outputs.py \
  --root log-model/examples/ngsoc
```

严格审计不使用 `--allow-legacy-scalars`；任何重新出现的 `network_direction` 标量都会使校验失败。
