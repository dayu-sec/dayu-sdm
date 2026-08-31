# ADR-007 BENIGN 与 FALSE_POSITIVE

- 状态：已接受
- 日期：2026-08-17

## 背景

ASIM 区分 False Positive 与 Benign Positive。Dropzone 用 benign/suspicious/malicious 描述行为；「规则不该报」是另一句话。

## 决定

`verdict` / `conclusion` 同时保留二者：

- `BENIGN`：行为发生且符合环境正常（差旅、批准备份）。
- `FALSE_POSITIVE`：检测逻辑误报，应回流规则。
- `SUSPICIOUS`：证据不够。
- `MALICIOUS`：确认恶意。
- `UNKNOWN`：尚未正式结论。

规则默认写 `UNKNOWN`。自动关单优先 FP 白名单；BENIGN 也可关，但不计入「规则误报」统计。
