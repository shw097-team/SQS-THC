---
title: 五分支 Scenario-Trend 與當日當沖合適度
created: 2026-08-21
updated: 2026-08-21
type: concept
tags: [daytrading, scenario, bias, liquidity]
sources:
  - raw/market-trend/台股市場&趨勢_專業技術文檔_v2.0_DOC-03_2026-07-25_r1.md
  - raw/market-trend/台股市場&趨勢_專業技術文檔_v2.0_DOC-08_2026-07-25_r1.md
  - raw/market-trend/台股市場&趨勢_專業技術文檔_v2.0_DOC-07_2026-07-25_r1.md
confidence: high
---

# 五分支 Scenario-Trend 與當日當沖合適度

> 本頁鎖定當日沖銷兩個相扣的市場問題：（1）**五分支 Scenario-Trend**——如何把 macro/事件/外部訊號編譯成五分支情境容器（Base/Bull/Bear/Unknown/Tail）而非單點方向；（2）**當日當沖合適度**——市場條件組合決定「今天適不適合當沖、做到哪一級」的條件式授權。兩者都「先給 prior、再給授權」，都不給下單指令。摘要見 `market-trend-summary`(raw/Layer-1)。

## 五分支 Scenario-Trend：外部 prior → 內部確認 → 五分支容器
- 本冊每一章的通用 pattern 是**「情境分支/狀態轉移」**：任何 macro/事件/外部訊號都輸出 `base/bull/bear（+unknown/tail）分支 + probability + invalidation + expiry`，不輸出單點方向（DOC-03 MacroRegime：`growth_state/inflation_state/labor_state/policy` 各自保存 state、probability、dissent、invalidation）。
- DOC-03 的 `RateScenarioTree` 至少有 base/bull/bear 三分支，每分支含 `meeting_path_bp / terminal_rate / condition / invalidation`；DOC-04 提供美元/全球流動性金融條件 prior；DOC-06 把它們接成 `TaiwanMacroBridge`：外部衝擊 **`→ 五時鐘校準 → US/Asia 分解 → ADR/FX/政策/出口/產業映射 → 台股內部確認 → TAIWAN_CONFIRM 或 DIVERGENCE`**。
- **外部方向與台股內部不同時，保留 divergence，不把矛盾平均掉**；出現時序/權利/owner/ADR 正規化硬錯誤 → `TRANSMISSION_BREAK`（撤銷依賴物件、對下游 NACK）。
- 上位對接（見 [[tw-ict-mainline-method]]）：五分支容器收斂進主鏈的 `ScenarioTree`（Base/Bull/Bear/Unknown/Tail），每支有 guards、invalidation、expiry 與 legal action；material trigger 只建立新版本 `BranchSwitch`，不得回寫 T0。參考 [[ict-context-bias-scenario]]。

## 當日當沖合適度 = 條件組合授權（不是「今天買什麼」）
DOC-07/08 把「適不適合當沖」拆成可審計的市場條件，輸出授權而非訊號：
- **盤勢級別授權**（DOC-07 H2-5）：在 TREND_BROAD 全參與、RANGE 用 SETUP_ALLOWED_WITH_GATES、極端/資料不足用 RISK_REDUCE 或 **NO_TRADE**。參見 [[tw-market-index-structure]]。
- **流動性/可成交量 Size Veto**（DOC-08 SC-08-03）：流動性分層、可成交量的 Size Veto，缺乏可成交性的標的/時段不可交易。
- **波動/缺口/反轉事前分類鎖**（DOC-08 SC-08-04）：波動、缺口與反轉須在事前分類（事前分類鎖），不做事後貼標籤。
- **極端行情/價格鎖定/No-Trade**（DOC-08 SC-08-05）：跌停家數極端、價格鎖定、流動性失真 → No-Trade，**不因恐慌「抄底」**。
- **時段轉換/隔夜跳空 Freshness**（DOC-08 SC-08-06）：時段轉換、隔夜跳空後資訊 freshness 失效，當沖決策需重新確認。
- **槓桿/信用壓力**（DOC-09）：維持率↓+波動↑+流動性惡化 → `leverage_vulnerability`/`SQUEEZE_RISK`，見 [[tw-funds-and-news-flow]]。

> 核心原則：當沖合適度是**「條件組合下的授權金箍」**——資料可比較、分母完整、反證不存在，才允許到對應等級；缺任一項即保守降級。No-Trade 與 kill-switch 治理見 [[tw-ict-risk-gates]]；盤中微結構可成交性見 [[ict-intraday-microstructure]]。

## 相關頁
- `market-trend-summary`(raw/Layer-1)、[[tw-market-index-structure]]、[[tw-funds-and-news-flow]]
- [[tw-ict-mainline-method]]、[[ict-context-bias-scenario]]、[[tw-ict-risk-gates]]
