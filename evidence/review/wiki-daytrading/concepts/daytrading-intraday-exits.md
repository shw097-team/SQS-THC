---
title: 盤中進出場與風險控制
created: 2026-08-21
updated: 2026-08-21
type: concept
tags: [daytrading, method, ob-orderflow, regime]
sources:
  - raw/daytrading-v3/daytrading-v3-summary.md
  - raw/daytrading-v3/daytrading-v3-sources.md
confidence: high
---

# 盤中進出場與風險控制

> 主軸 = 台股當日沖銷（T+0）。盤中進場必須有可反駁的 Setup（precondition／trigger／invalidation／expiry，見 [[ict-context-bias-scenario]] 與 [[ict-daytrading-modules]]）；任何技術資格都不等於下單許可，也不等於已成交。風險收斂由 DOC-09 CH-12/13 管轄，尾盤走 Forced Flatten（見 [[daytrading-t0-flow]] 與 [[tw-ict-risk-gates]]）。

## 進場：Setup 前件與 NO_SETUP

- `Setup precondition → trigger → invalidation → expiry`：缺任一可反駁前件即 `NO_SETUP/UNKNOWN`，後續技術/籌碼/AI 分數**不可補償**（非補償式 gate，DOC-05 CH-06.11）。
- 開盤後才可 armed（`OPEN_CONFIRMATION`，見 [[daytrading-open-auction]]）；盤中 `SetupState` 只要 data/regime 變動即失效，`Setup ARMED ≠ 可送單`。
- 技術結構（BOS/CHoCH、FVG/OB、支撐壓力、分K）作 context/component，不因名稱存在而 bypass 資格；見 [[smc-market-structure]]。

## 盤中監控（Position/Order 分離）

- 每個 ExecutionEvent 經 order state projector + idempotency；只有 `FillRecord` 更新 confirmed position。委託量 ≠ 持倉、cancel request ≠ cancelled（`E_POSITION_ORDER_QTY_CONFLATION`）；partial fill/cancel race/feed gap 時不得誤以為已平倉。
- 未知 order/fill → `UNKNOWN_EXPOSURE`，**禁止增加 exposure**；所有人工 override 建立 IncidentRecord + reason_code。

## 停損/停利/分批/時間退出

- `StopHypothesis` 定義「何種觀測使原假說失效並開始退出」；`TakeProfitPlan` 定義分批與條件；`TimeExit` 定義到期。三者都只產生 OrderIntent，**不等於 FillRecord**（DOC-09 CH-12.3）。
- 移動停損須有事前規則且不得放寬 invalidation；time exit 到期不得因情緒延長。反例：跌破停損後下移「給股票空間」（thesis drift）、送出委託即在日誌標記平倉（execution-state fraud）。`trigger → OrderIntent → ACK → Fill/Partial/Reject → PositionUpdate → residual-risk 重算 → re-plan`。

## 部位與曝險（effective_R / approved_qty）

```text
effective_R   = max(planned_unit_loss, executable_unit_loss, stress_unit_loss)
approved_qty  = min(risk_budget/effective_R, liquidity_capacity, participation_cap,
                    single_name_cap, sector_cap, factor_cap, event_cap, gross/net cap)
```
只用進場價到停損差的」會低估 spread/slippage/impact/部分成交/gap/鎖死，使部位被系統性放大。**不同 ticker ≠ 分散**：ExposureSnapshot 做 single-name/sector/factor/direction/event look-through；缺分類不能當零曝險（DOC-09 CH-12.5）。

## 日損、回撤與 Kill Switch

- `DailyLossRecord` + `DrawdownRecord` 是**獨立 veto**（WARN→REDUCE→STOP→LOCKED）；即使下一筆 setup 再好也不能跨越，不得用預期勝率抵銷已觸發的日損/回撤（CH-12.6）。
- Kill Switch：由 daily loss、drawdown、exposure、data/clock failure、duplicate/unknown order、position mismatch 等觸發，**block new intents → Incident → reconcile → named ResetApproval**。本任務無券商 write，「automatic」僅指 paper/shadow state 轉 `BLOCKED`。
- Safe degrade 不放寬 rule：`NORMAL → OBSERVATION_ONLY → CANCEL/REDUCE_ONLY → STOP`；incident 為 first-class state（DETECTED→CONTAINED→RECONCILING→VERIFIED→CLOSED），重新登入 ≠ 事故閉合。

## 相關頁

- [[daytrading-t0-flow]]
- [[daytrading-open-auction]]
- [[tw-ict-risk-gates]]
- [[ict-context-bias-scenario]]
