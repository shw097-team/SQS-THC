---
title: ICT 盤中微結構 — 試撮／大單／分K／PO3／AMD／Market Profile
created: 2026-08-21
updated: 2026-08-21
type: concept
tags: [daytrading, ict-module, market-structure, liquidity, ob-orderflow]
sources: [raw/ict-smc/ict-smc-summary.md]
confidence: high
---

# ICT 盤中微結構（當日沖銷）

> 本頁整理台股當日沖銷視角下，ICT 對「盤中如何建立、讀取、利用價格微結構」的語義與資料能力邊界。核心立場：**時間容器與資料能力先行，名稱／事後故事不足以為可交易資格**。相關：[[smc-market-structure]]、[[ict-daytrading-modules]]。

## 1. 試撮／集合競價與時間容器（Auction & Segment）
- 集合競價（試撮）／連續交易／收盤撮合／零股是**不同狀態容器**，不得混為同一 session；「所有 09:00 後資料視為同一 session」是反例（DOC-05 CH-12）。
- 台灣 profile 分離集合競價、連續交易與零股資料能力；若資料供應商無 auction prints，opening feature 降級但其他 segment 可繼續（CH-12、CH-22 Taiwan-first）。
- 開盤價（`DAILY_OPEN`／`WEEKLY_OPEN`／`MIDNIGHT_OPEN`）必須引用 `price_source`＋`confirmed_at`；**不准用視覺上第一根 K 補開盤價**（CH-12）。
- 交易日由交易所規則編譯為 `TradingDaySpec`，由 TWSE／TPEx 官方 effective-date snapshot 注入，不硬寫會漂移的鐘點（CH-22）。

## 2. 大單／主力：只能是 proxy，不是因果
- 本冊核心防線：**OHLC price action 是 proxy，不是 L2 或機構意圖證明**（DOC-00 DDD-04、CH-23）。
- 「大單」在盤中只能經由可觀測代理來間接讀取：高低點外流動性池（BSL／SSL）、Draw-on-Liquidity、displacement 與價格交付路徑（CH-06/07）。
- Volume Imbalance 在 OHLC 層只是「相鄰 close／open 或 body non-overlap」的價格 proxy；真實成交量分配或 aggressor 需 L2／raw trades，否則 OFFSET（CH-23 Data Capability Ladder、CH-09）。

## 3. 分K／多週期 Top-Down（Minute bars & HTF/LTF）
- OHLC／Bar／Candle 以 **confirmed state** 為準：只有已收盤 bar 才可作 swing、pivot、FVG 幾何的 anchor（DOC-01 CH-02、CH-08）。
- 多週期 Top-Down：HTF（日／週）定義決策區與 bias，LTF（分K 級）只做觸發與執行端（CH-03、CH-13）。LTF MSS 不得用來改寫 HTF range（frame leakage 反例）。
- 分K 需與 session／segment 對齊：一根 bar 跨越 segment 邊界會污染 opening range 與 session statistics（CH-12）。

## 4. PO3／AMD（Power of Three ／ Accumulation-Manipulation-Distribution）
- PO3／AMD 是「**序列／profile 候選**」，只有在 authoritative range、phase order、時間 eligibility 與可觀測事件俱備時才 QUALIFIED；「名稱、三段波動或事後故事」均不足（CH-13-H2-07）。
- AMD 三階段：**Accumulation（累積）→ Manipulation（操縱/洗盤）→ Distribution（分配）**，三階段需時間單調且每階段有獨立可觀測證據（CH-13-H2-08）。
- PO3／AMD 是模型 component（供 DOC-06 參考），不是獨立 setup 名稱（CH-13、DOC-06）。

## 5. Market Profile／Volume Profile：auxiliary context
- Market Profile 在本冊被 `ROUTE_OUT_WITH_OWNER` 標為 AUXILIARY：僅作 session／profile 上下文輔助，**不得取代 ContextPacket**（DOC-05）。
- Volume Profile 為 OPTIONAL：提供成交量分布 context，不能替代 ICT canonical sequence；體積來源不可靠即 OFFSET（DOC-08 CH-23）。
- POC／Value Area 這類概念屬二創／輔助詞彙，需按 DOC-00 CH-01 治理後才能作為 alias 使用。

## 6. 與當日沖銷的接口
- 上述微結構全部餵給模型資格判定（[[ict-daytrading-modules]]）與結構事件（[[smc-market-structure]]）；品質不滿足某項即降級或 NO_TRADE（fail-closed）。

## 來源
^[raw/ict-smc/ict-smc-summary.md] ｜ DOC-01 CH-02、DOC-02 CH-03、DOC-03 CH-06/07、DOC-04 CH-09/11、DOC-05 CH-12/13、DOC-08 CH-22/23。
