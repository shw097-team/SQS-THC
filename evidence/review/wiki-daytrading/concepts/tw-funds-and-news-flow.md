---
title: 資金面與訊息面 (Funds Flow & News/Event)
created: 2026-08-21
updated: 2026-08-21
type: concept
tags: [liquidity, regime, bias]
sources:
  - raw/market-trend/台股市場&趨勢_專業技術文檔_v2.0_DOC-09_2026-07-25_r1.md
  - raw/market-trend/台股市場&趨勢_專業技術文檔_v2.0_DOC-05_2026-07-25_r1.md
  - raw/market-trend/台股市場&趨勢_專業技術文檔_v2.0_DOC-06_2026-07-25_r1.md
confidence: high
---

# 資金面與訊息面

> 當日沖銷的市場條件除了「指數/盤勢（靜態位置）」，還有兩個動態驅動：**資金面**（法人/信用/衍生品怎麼變動）與**訊息面**（事件/外溢/題材怎麼進來）。本頁把兩者編譯成可反證、會過期的決策物件（Actor-flow Kernel、EventCard、TaiwanMacroBridge），且**任何單一數字或單一消息都不得翻譯為多空**。來源摘要見 `market-trend-summary`(raw/Layer-1)、`market-trend-sources`(raw/Layer-1)。

## 資金面（DOC-09：Actor-flow, Leverage and Derivatives Kernel）
核心機制鏈：`InstitutionalFlowCard → LeverageCrowdingCard → FuturesStructureMap → OptionsRiskMap → FlowAndPositioningState → Anti-Single-Factor Gate → typed 跨冊 handoff`。
- **三大法人**（外資及陸資/投信/自營）：日報是**集合分類後的交易結果，不是逐一機構的真實意圖**（可能含被動追蹤、ETF 申贖/換股、套利、造市、避險）。最低資料契約是市場別/標的範圍/幣別/交易日/發布時點/修訂狀態/classification version，缺任一只能 `OBSERVATION_ONLY`。
- **口徑先分離、再做假說競爭**：外資現貨賣超 vs 期貨淨空 vs 台積電部位可互抵/避險並存；「外資淨空=看空」是禁止命題。流量→衍生值（1/3/5/20 日累積、同向天數、z-score）→候選狀態 `ACCUMULATION/DISTRIBUTION/HEDGED/MIXED`；confounder（被動換股、結算、除權息）未解時狀態上限 `MIXED`。
- **融資融券/借券**：融資=存量非流量、融券、借券、借券賣出是**不同生成機制**；分點只是交易據點代理，**不揭露最終受益人**（KP-18）。維持率必 nullable + 公式版本；槓桿分支 `build/pressure/forced-liquidation/covering/squeeze`；維持率↓+波動↑+流動性↓ → `SQUEEZE_RISK`/`leverage_vulnerability`。`crowding_score` 只排序研究注意力，非交易分數。
- **台指期/基差/轉倉**：最小單位是「某一契約的某一 session 觀察」，近月/次月/季月不可無條件串續；夜盤依交易所歸屬映射。`observed_basis = futures − spot`；OI 變化不揭示主動/被動，roll 以近月↓次月↑觀察。**「逆價差=看空」「OI 增=空方加碼」為禁止命題**。
- **選擇權/波動/結算**：選擇權風險結構與結算事件窗口；到期/結算扭曲 → `SETTLEMENT_DISTORTION`。流向與避險假說 → `HEDGED`，事件結束先回 `MIXED` 再重估。

## 訊息面（DOC-05 事件、DOC-06 外溢、DOC-10/14 題材）
- **地緣風險與事件分類（DOC-05）**：事件本體/法域/正式文本以五時鐘契約正規化，分類 ≠ 方向；事件要經正規化、狀態轉移與 supersession 管理，確保「舊事件被新文本取代」。
- **外部市場外溢（DOC-06 TaiwanMacroBridge）**：美股/費半/ADR/日韓中港/美元/美債/VIX/油價/政策**最多建立外部 prior**，必須通過五時鐘＋台灣內部確認（廣度/成交值/價格/流動性/法人/風格）才能成為有效市場/產業層傳導物件；「美股漲所以台股必漲」是禁止命題。外部 vs 台股分歧保留 `DIVERGENCE`。
- **題材熱度/輪動（DOC-10/14）**：盤後 session、PCB/被動/記憶體/光通訊等題材熱度是**被動/跨產業機制**，多族群事件共現是 confounder；「題材熱度≠長週期」「重複題材≠認證」；需以群組成員與市場分母明確才可成 style evidence（見 [[tw-market-index-structure]] 的 StyleMap）。

## 與當沖決策的關係
資金/訊息是當沖 bias 與五分支 scenario 的**外部 prior 與 counter-evidence 來源**（見 [[tw-scenario-daytrading-suitability]]、[[ict-context-bias-scenario]]）；No-Trade/風險邊界見 [[tw-ict-risk-gates]]。

## 相關頁
- `market-trend-summary`(raw/Layer-1)、`market-trend-sources`(raw/Layer-1)
- [[tw-market-index-structure]]、[[tw-scenario-daytrading-suitability]]
- [[tw-ict-mainline-method]]、[[ict-context-bias-scenario]]、[[tw-ict-risk-gates]]
