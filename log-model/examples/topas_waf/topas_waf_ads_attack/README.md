# topas_waf / topas_waf_ads_attack 数据缺口

## 当前状态

`partial`。WPL 中存在 `topas_waf_ads_attack` 规则，选择器为 `recorder=ads_attack`，但当前 `sample.dat` 的非空样本没有一条能命中该规则。

## 已知语义

- 产品：天融信 TopWAF 2.0。
- 文档日志族：DDoS/应用防护攻击日志。
- 观察者：来源 WAF 产品。
- 攻击事实、处置结果和严重度：没有运行时匹配样本，不作投影。

## 所需补充

至少补充一条真实 `recorder="ads_attack"` 日志，并用以下命令验证：

```bash
wpl-check sample --print --rule-name topas_waf_ads_attack --data '<raw>' log-model/models/wpl/topas_waf/parse.wpl
```

没有匹配样本前，不生成 `wpl-output.json`、`expected-sdm-event.json` 或枚举映射。
