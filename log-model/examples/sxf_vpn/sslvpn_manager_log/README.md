# sxf_vpn / sslvpn_manager_log 数据缺口

## 当前状态

`partial`。WPL 中存在 `sslvpn_manager_log` 规则，选择器为 `SVPN-ADMIN`，但当前 `sample.dat` 的非空样本没有一条能命中该规则。

## 已知语义

- 产品：深信服 SSL VPN。
- 预期日志族：管理员日志。
- 观察者：来源 SSL VPN 产品。
- 主体、客体、载体和动作：没有运行时样本，不作推断。

## 所需补充

至少补充一条真实 `SVPN-ADMIN` JSON 日志。补充后应运行：

```bash
wpl-check sample --print --rule-name sslvpn_manager_log --data '<raw>' s4-doris/models/wpl/sxf_vpn/parse.wpl
```

没有匹配样本前，不生成 `wpl-output.json`、`expected-sdm-event.json` 或枚举映射。
