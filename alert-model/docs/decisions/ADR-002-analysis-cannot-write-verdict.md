# ADR-002 分析行不能直接写正式 verdict

- 状态：已接受
- 日期：2026-08-17

## 背景

草案待定问题 5：AI 是否允许修改主表 `verdict`。Copilot / TIN / Dropzone / XSIAM 的共同做法是：调查先落历史，正式分类由策略或人确认。XSIAM 的 Resolution reason 是关单动作，不是模型直接改检出列。

## 决定

1. 闸门、AI、playbook 只 insert `sdm_analysis`。
2. 主表 `latest_analysis_*` 由服务根据最新分析行回写，表示展示，不是终审。
3. `sdm_alert.verdict` / `sdm_case.verdict` 仅当以下之一成立时更新：
   - 人确认或改结论；
   - 策略命中（例如 `analysis_type=GATE|AI` 且 `conclusion=FALSE_POSITIVE` 且 `analysis_confidence>=阈值` 且告警类型在白名单）。
4. 回写必须记录 `accepted_status` 与策略 ID 或操作者。

## 后果

评测集可以用分析行当预测、人的 `verdict` 当标签。自动关误报是策略，不是模型权限。
