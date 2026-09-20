# suricata / stats — 不进行为信封

`event_type=stats` 是引擎计数（uptime/capture/decoder），没有通信主体/客体，也不是检测。

SDM2.0 当前 `event_kind` 只有 `behavior`；`state` 模型暂缓。因此 **不写** `expected-sdm-event.behavior.json`，**不进** `sdm_event_behavior`。

处置：继续 miss / 丢弃 / 观测文件。不要用二代整包 `log_type=suricata` 兜底。

样本：OPS eve.json 2026-09-06，已删减 decoder 细节。
