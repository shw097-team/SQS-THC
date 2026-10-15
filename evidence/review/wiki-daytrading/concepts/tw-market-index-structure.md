---
title: 大盤指數與盤勢分級 (Market Index & Regime)
created: 2026-08-21
updated: 2026-08-21
type: concept
tags: [daytrading, market-structure, regime]
sources:
  - raw/market-trend/台股市場&趨勢_專業技術文檔_v2.0_DOC-07_2026-07-25_r1.md
confidence: high
---

# 大盤指數與盤勢分級

> 當日沖銷的第一道市場條件不是「指數漲跌」，而是**可審計的市場層事實**：大盤指數（加權/櫃買/分層）、盤勢分級（regime enum）、broad 市況（廣度/成交值/流動性/集中度）。DOC-07 把它們編譯成 read-only 的 `MarketState → BreadthDashboard → StyleMap → TaiwanMarketRegimeCard`，任何當沖 bias 都必須先掛在這些市場條件上，且**不得把市場 context 升格為個股指令**。來源摘要見 `market-trend-summary`(raw/Layer-1)、`market-trend-sources`(raw/Layer-1)。

## 大盤指數：不是一根線，是三層 universe
- **TAIEX 與 TPEx 是不同 universe、不同方法、不同市場層級的觀察，不可直接相加。** 指數水準、報酬、成分、權重、基期都須以 `as_of` 版本保存；**歷史集中度禁止用今天成分/權重回填**（PIT 契約，DOC-07 H2-2.1）。
- **市場分層至少分開**：TWSE／TPEx、size bucket（大型/中小）、sector/group、liquidity bucket。大型/中小不是媒體標籤，而是由版本化 market-cap 或 index membership 定義（H2-2.2）。
- **分散在不同 segment 各自計算**價格/breadth/turnover/concentration，再以明確權重合成；不同分母只在 RegimeCard 的 evidence list 相遇，**不在原始計算時混合**。
- **分層判讀必須主動找 counter-evidence**：指數 vs 等權重、TWSE vs TPEx、價格 vs 成交值、領先群 vs 市場中位數的背離。typed divergence：`INDEX_UP_BREADTH_DOWN`、`TWSE_TPEX_DIVERGENCE`、`TOP_WEIGHT_DOMINANCE`、`LOW_LIQUIDITY_ROTATION`（H2-2.3）。

## 盤勢分級：Regime Enum + 授權範圍
公示化分級（同 DOC-07 H2-4/H2-5）：
- **TREND_BROAD** — 指數與 TPEx/breadth/turnover/style 共同改善才成立；缺任一項最多 MORE_DATA/低 confidence。
- **TREND_NARROW** — 指數趨勢成立但集中度上升、廣度收縮（如「拉積盤」、指數漲而 median 報酬負）。
- **RANGE_BROAD / RANGE_NARROW** — 區間市況，按廣度/參與度再分。
- **CAPITULATION** — 對價格+breadth collapse+turnover spike+limit constraints 的**描述，不是買點**；不能直接跳 TREND_BROAD，須先經穩定/再確認（TRANSITION_REPAIR）。
- **UNKNOWN/INVALID** — 資料缺分母、版本衝突、evidence conflict 未解時降級。
- 授權輸出只有五級：`READ_ONLY_CONTEXT` / `SETUP_ALLOWED_WITH_GATES` / `MORE_DATA` / `RISK_REDUCE` / **`NO_TRADE`**；risk veto 優先於 consumer。狀態機用 **hysteresis + minimum persistence** 防單日噪音反覆切換（H2-5.2）。

## broad 市況：廣度、成交值、流動性、集中度
- **BreadthDashboard 的核心不是一個上漲家數，而是「可審計分母」**：eligible/advance/decline/unchanged/suspended、advance-decline、advance ratio、median return、equal-weight return、new-high/new-low（可得時）、turnover、coverage。守恆式 `advance+decline+unchanged+excluded = PIT universe count`，不守恆即 `ERR-BREADTH-002`（H2-3.1）。
- **價格上漲、廣度改善、成交值擴散、可成交性是四個不同訊號**（H2-3.2）：廣度改善但成交值集中於少數權值→仍可能窄幅；成交值放大但 median 惡化→可能換手/去槓桿；縮量上漲→低 confidence。單日巨量只是 evidence，**不是 reversal label**。
- **集中度**（H2-4.1）：top-1/5/10 weights、index contribution、turnover concentration、HHI（=Σwᵢ²）、Effective N（=1/HHI）描述**權重集中**，不描述因果/估值/未來報酬。台積電 proxy 只在完整權重不可得時產生 `NARROW_WARNING`，不得輸出全市場結論。
- **極端行情優先級**：HALTED / SESSION_INVALID / DATA_INVALID 高於任何 regime；輸出只能是 `CURRENT_DATA_REQUIRED` / `MORE_DATA` / `RISK_REDUCE` / `NO_TRADE`（H2-3.3）。

## 與當沖決策鏈的關係
盤勢分級是 MTF Bias 的外部先驗層（`外部 prior → 台股內部確認`）。TREND/RANGE/CAPITULATION 對應的上位五分支見 [[tw-scenario-daytrading-suitability]]；市場條件對當沖的授權 gating 規則見 [[tw-ict-risk-gates]]。指數/市場分層的 SMC 結構視角另見 [[smc-market-structure]]。

## 相關頁
- `market-trend-summary`(raw/Layer-1)、`market-trend-sources`(raw/Layer-1)
- [[tw-scenario-daytrading-suitability]]、[[tw-funds-and-news-flow]]
- [[tw-ict-mainline-method]]、[[ict-context-bias-scenario]]
