---
title: 風險 Gate 與當沖執行邊界 (DOC-06/07)
created: 2026-08-21
updated: 2026-08-21
type: concept
tags: [daytrading, liquidity, regime, method, ob-orderflow]
sources:
  - raw/tw-ict-v3/TW-ICT_專業技術文檔_v3.0_DOC-05_2026-07-29_r2.md
  - raw/tw-ict-v3/TW-ICT_專業技術文檔_v3.0_DOC-06_2026-07-29_r2.md
  - raw/tw-ict-v3/TW-ICT_專業技術文檔_v3.0_DOC-07_2026-07-29_r2.md
confidence: high
---

# 風險 Gate 與當沖執行邊界

> 主軸 = 台股當日沖銷（intraday, T+0）。所有技術資格、風險授權、OrderIntent 都必須分離 object ID／owner／version／expiry；且**非補償式 gate**：任何後端 score、setup confidence、未實現獲利都不得補償前端 veto。日終無 fresh `OvernightDecision` 的 `intraday-only` 部位一律 `FORCED_FLATTEN`，不允許自然留倉改隔日沖（見 [[tw-ict-mainline-method]]）。

## 非補償式 Gate 原則

- DOC-05（CH-11/12）reducer：Rule→Data→Eligibility→Capability→Liquidity/Cost/Capacity/Borrow→Evidence→Score。**後段永不補償前段 veto**。
- DOC-06（CH-15）R83 `SetupQualificationRouter` 逐 gate 非補償判定：`QUALIFIED/OBSERVE/RESEARCH_ONLY/REJECTED/NO_TRADE/WAIT/ROUTE_BACK/BLOCK`。
- DOC-07 R06/R86 下游 risk veto 可拒絕已 QUALIFIED setup；QUALIFIED 不代表可下單。

## Document 邊界（誰不能越權）

| 決策物件 | Owner | 內容限制 |
| --- | --- | --- |
| TradeHypothesis | DOC-05/R79 | 研究假說：前提、trigger、失效、期限 |
| SetupDecision | DOC-06/R83 | 技術資格，不含 size/order |
| RiskAuthorization | DOC-07 risk owner | 獨立許可；缺則 NO_TRADE |
| OrderIntent | DOC-07 execution owner | `send_enabled=false`，phase 內行動意圖 |

## 停損 / 退出（DOC-07 CH-17.3/17.4）

`StopPlan` 區分：technical Invalidation、structural invalidation、monetary stop、catastrophic stop、time/session stop、portfolio stop、kill-switch stop。**Stop-widening 預設非法**（`no_widen=true`；進場後移往更不利位置、延 long time stop、averaging down 均預設 `VETO`，須全新 RiskAuthorization + 完整 exposure 重算）。退出用 `ManagementTree`（target、partial、trailing、break-even、time exit、event exit、emergency exit）；break-even 不=「無風險」，time exit 到期不得主觀延長。

## 部位、曝險與日損 Gate（CH-17.5/17.6）

`PositionState` 生命週期 `FLAT → PENDING_ENTRY → PARTIALLY_OPEN → OPEN → REDUCING → EXIT_PENDING → FLAT_RECONCILED/INCIDENT`。`PortfolioExposure` 聚合 single-name、sector、factor、direction、shared catalyst/supply-chain、liquidity/borrow concentration。**多 ticker ≠ 分散**。`EXPOSURE_LIMIT/CORRELATION_LIMIT/CONCENTRATION_UNKNOWN` 均可獨立 VETO。`DailyLossState` 分 realized/unrealized/fees/slippage；狀態階梯 `NORMAL → WARN → REDUCE → STOPPED → LOCKED → REVIEWED → RESET`；`STOPPED/LOCKED` 下，下一筆 setup 再好也不能跨越。Risk of Ruin 不是單一閉式數字，而以 stress scenario 降級。

## 最低 StressScenario 集（CH-17.6）

spread widening、slippage shock、partial fill、no fill、gap against position、limit lock、liquidity evaporation、borrow recall、event surprise、data outage、stale rule、order timeout、duplicate event、correlated selloff、tail event。

## Kill Switch 與 Overnight Gate（CH-17.7 / CH-16）

- **Kill Switch：** 具 scope/trigger/threshold/state/reset authority；由 daily loss、drawdown、exposure、data/clock failure、duplicate/unknown orders、position mismatch、security finding、borrow/settlement risk 或 tail event 觸發。`trigger → ACTIVE/LOCKED → block new intents → … → IncidentRecord → reconcile → postmortem → named ResetApproval → COOLDOWN/CLEARED`。本任務無券商 write，故「automatic」僅指 paper/shadow state 轉 `BLOCKED`。
- **Overnight Gate：** `TAIL` 階段為風險收斂截止區，執行 risk reduction、Overnight Gate 或 `FORCED_FLATTEN`；**不允許把當沖未出場自然留倉改隔日沖**（見 DOC-07 16.2 TAIL row 反例「當沖未出場自然改隔日沖」→ 未核准→FORCED_FLATTEN）。

## 相關頁
- [[tw-ict-mainline-method]]
- [[ict-context-bias-scenario]]
