---
title: 台股當沖交易流程與交易日時鐘 (T+0)
created: 2026-08-21
updated: 2026-08-21
type: concept
tags: [daytrading, method, regime, market-structure]
sources:
  - raw/daytrading-v3/daytrading-v3-summary.md
  - raw/daytrading-v3/daytrading-v3-sources.md
confidence: high
---

# 台股當沖交易流程與交易日時鐘 (T+0)

> **主軸確認：本頁描述台股當日沖銷（intraday, T+0）的交易流程，非隔夜持倉。** 普通交易撮合時段為 **09:00–13:30**（Asia/Taipei），交割基線 T+2（DOC-01 CH-01-H2-04）。任何當沖部位若日終無 fresh 留倉批准，一律走 Forced Flatten 並交 DOC-09 Overnight Gate（見 [[daytrading-intraday-exits]] 與 [[tw-ict-risk-gates]]）；**未平倉 ≠ 自動批准留倉**（DOC-08 CH-10.7）。

## 交易日時鐘（五時鐘）

`TradingClock` 把交易日曆、時區、session、狀態生效窗與資料時間欄位綁成同一可驗證物件。**五時鐘**：`event_at`（市場何時發生）、`source_at`（來源何時產生）、`available_at`（系統何時可見）、`decision_asof`（決策何時成立）、`accessed_at`（規則何時被查閱）。用途是讓每次 OrderIntent／TCA／replay 都能回答「在當時究竟知道什麼」；**不能以本機日期或檔案日期代替決策時點**（禁止 `E_CLOCK_SESSION_MISMATCH`）。

## Session 時間軸與狀態

```text
PREVIOUS_CLOSE → PREMARKET_PREP → AUCTION_OBSERVATION → OPEN_CONFIRMATION
→ CONTINUOUS_SESSION → TAIL_REDUCTION → CLOSE_RECONCILIATION → POST_TRADE_REVIEW
```

`TradingDayState` 只能在 session guard 通過後轉移；任何 clock skew、跨日或 RuleSnapshot 過期，把執行平面降為 `SAFE_DEGRADE` / `STOP`。盤前的試撮（8:30 可輸入委託）屬於 `AUCTION_OBSERVATION`，成交與否需等開盤首筆 `TradeEvent` 確認——詳見 [[daytrading-open-auction]]。

## 盤前/開盤 Readiness（合取，非加權分數）

盤前 readiness 是三個**不可互補**的檢查面：`Rule_OK ∧ Data_OK ∧ Risk_OK ∧ No_Unknown_Exposure`。`OperationalHandoff` 把 RuleSnapshot、DataFreshnessRecord、RegimeCard、CandidateCard、SetupCard、RiskEnvelope 與 unresolved incidents 以同一 `decision_asof` 封裝；任一個 hard gate（G1~G6）失敗，SetupState 維持 `BLOCKED/STALE`，**DOC-08 不重算上游 alpha**（不做方向投票、不修分數）。盤前新聞/外盤只是 context，不是交易授權。

## 狀態分離（Strategy / Setup / Order / Position）

- `StrategyState`：策略家族可否運作；`SetupState`：單一假說是否 armed；兩者均不代表已送單。
- **Setup ARM / Order Readiness ≠ 可送單**：OrderIntent 仍需獨立驗證與凍結，驗證後不可原地修改（`E_INTENT_IMMUTABILITY_BREACH`）。
- **Position invariant**：`confirmed_qty = Σ(唯一 confirmed fills) − Σ(唯一 confirmed exits)`；pending 與 unknown 不得混入 confirmed。只有可用唯一 FillRecord 改變 confirmed position。

## 尾盤與 Forced Flatten（T+0 收斂）

尾盤優先序：`停止新增 exposure → 對帳 → 執行已批准減倉 → 處理 unknown → handoff`。Forced Flatten 是 DOC-09 risk owner 的裁決、由 DOC-08 執行，**提交/ACK 成功 ≠ 已平倉**（禁止 `E_FLATTEN_ASSUMED_COMPLETE`）。到 cutoff 仍有 confirmed/pending/unknown 時，建立 IncidentRecord、停止新單、將 PositionState/OrderState/unknowns 交接 DOC-09。Safe degrade 不放寬 rule/risk，只縮減允許動作：`NORMAL → OBSERVATION_ONLY → CANCEL/REDUCE_ONLY → STOP`。

## 相關頁

- [[daytrading-open-auction]]
- [[daytrading-intraday-exits]]
- [[tw-ict-mainline-method]]
- [[tw-ict-risk-gates]]
