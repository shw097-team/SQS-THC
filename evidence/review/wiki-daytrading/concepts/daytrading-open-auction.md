---
title: 盤前試撮與開盤紀律
created: 2026-08-21
updated: 2026-08-21
type: concept
tags: [daytrading, ob-orderflow, liquidity, market-structure]
sources:
  - raw/daytrading-v3/daytrading-v3-summary.md
  - raw/daytrading-v3/daytrading-v3-sources.md
confidence: high
---

# 盤前試撮與開盤紀律

> 主軸 = 台股當日沖銷（T+0）。**試撮是集合競價資訊，不是成交事實；開盤成交後必須重新評估**（CLM-DOC01-018）。本頁對應交易日時鐘的 `AUCTION_OBSERVATION` / `OPEN_CONFIRMATION` 兩段，流程軸心見 [[daytrading-t0-flow]]。

## 試撮：觀測而非成交

- 08:30 可輸入委託**不等於已成交**；試撮價**不等於**開盤成交價。試撮掛單可撤、價格快速變動，不能當作成交或容量證據（`E_AUCTION_INTENT_AS_FILL`）。
- 事件序列：`BookUpdate(indicative) → cancel/replace updates → opening TradeEvent → OPEN_CONFIRMATION`。**序列缺失即不可推論**；試撮漲停/厚單不代表開盤支撐。
- 試撮只能描述「當時顯示了什麼、何時更新、是否撤除」，不得描述未發生的成交或主體意圖；開盤後收到首批 `TradeEvent` 才進入 OPEN_CONFIRMATION 並以新 book state 重建 MarketObservation。

## 盤前候選池（PREOPEN）

`PREOPEN pool` 只使用 PIT cutoff 前已知資料（前日 close + 已公告 + 最新 rule snapshot）：`OvernightDelta` 標記隔夜事件，`short TTL` 使試撮開始即由新版本 supersede。禁止使用盤後才發布資訊回填盤前候選（look-ahead），也禁止把隔夜新聞當成交保證。試撮/集合競價觀測建立 `OPEN_AUCTION` candidate state，**開盤成交後強制重驗 G3/G4**、未確認者標 `STALE/REJECTED`——此流程屬 [[daytrading-stock-selection]] 的候選池漏斗。

## 開盤後確認與 Order Readiness

- Order Readiness **不採總分**，是 SetupState、MarketObservation、RuleSnapshot、DataFreshnessRecord、RiskEnvelope 同時有效的**合取條件**；任一 hard gate 失敗輸出 `NO_EXECUTION`。
- 開盤價格發現常使 spread、波動、容量異於盤前假設；**不沿用盤前排名與價位**。OPEN_CONFIRMATION 後重算可觀測 execution conditions，只有 setup 未失效、data fresh、spread/capacity 未越界且 pre-risk 通過，才建立 DRAFT OrderIntent；驗證後不可原地修改。
- 開盤紀律的兩條禁區：**把試撮/預估量當成交**、**shorcut（閃電下單/快捷鍵）跳過 validation、risk、ACK、reconciliation**（`E_SHORTCUT_BYPASS_VALIDATION`；ITEM-D08-07 只能縮操作路徑，不能省略檢核）。

## 相關頁

- [[daytrading-t0-flow]]
- [[daytrading-stock-selection]]
- [[daytrading-intraday-exits]]
- [[ict-intraday-microstructure]]
