---
title: SMC 市場結構 — 供給需求／BOS／CHoCH／imbalance
created: 2026-08-21
updated: 2026-08-21
type: concept
tags: [smc, market-structure, liquidity, daytrading]
sources: [raw/ict-smc/ict-smc-summary.md]
confidence: high
---

# SMC 市場結構（當日沖銷）

> 本頁以 **受控 auxiliary 視角**整理 SMC（Smart Money Concepts）四大塊：供給需求、BOS、CHoCH／MSS、imbalance。權威規則（DOC-00 CH-01）：**ICT 為 canonical，SMC／二創為受控 auxiliary**；熱門術語不得覆寫 ICT canonical 條件。相關：[[ict-intraday-microstructure]]、[[ict-daytrading-modules]]。

## 0. 治理前提
- SMC 詞彙（供需區、BOS／CHoCH 標籤、POI、指標框線）在 DOC-00 CH-01 本體治理中為 alias／auxiliary，可補案例與可讀性，**不可取代** canonical 條件。
- 一切結構事件先降為 `BreakObservation`；只有 confirmed swing、immutable BreakPolicy、位移 gate 通過後才發布 `StructureEvent`（DOC-02 CH-04）。

## 1. BOS（Break of Structure）
- BOS 在本冊指符合 policy 的 **continuation event**（同向狀態延續）——破高破低經 `BreakPolicy` 驗證，不是每個越界都自動成立（CH-04）。
- candidate、event、state、entry signal 嚴格分離：`CANDIDATE_BREAK → CONFIRMED_CONTINUATION`。
- 反例：把所有破高破低都標 BOS → 結構隨 pivot 演算法或結果改寫（因 `OVERSEGMENTED_SWING` 失敗）。

## 2. CHoCH／MSS（結構轉換）
- MSS（Market Structure Shift）＝**保護 swing 被突破**的 shift 事件；CHoCH 僅為 **conditional alias**，不得按詞面與 MSS 等價（CH-04 taxonomy map）。
- Shift 需 protected swing 被破＋context／displacement 支持；wick 越界但無 close／displacement 只能記 BreakObservation，不能發布 shift（CH-04）。
- 「MSS／CHoCH 靜默合併」與「LTF MSS 改寫 HTF range」都是反例，分別判 `TAXONOMY_COLLISION`／`HORIZON_OVERRIDE`。

## 3. 供給需求（Supply / Demand → Order Block）
- Order Block 是**具事件血緣的 zone object**，不是「最後一根反向 candle」，也不是「供需區」或 institutional candle（CH-10）。
- 最低資格鏈：可定位 origin candle／cluster → 可重建 pre-origin liquidity interaction → CH-11 confirmed displacement → CH-04 或 delivery-state 支持（CH-10）。
- 七家族：Mitigation、Breaker、Rejection、Suspension、Propulsion、Reclaimed 等各帶 owner；最後一根反向 K 直接標 OB 是反例（CH-10、DOC-03 CH-08 family taxonomy）。
- 依 CH-05，供需落在 **Premium／Discount（溢價／折價）與 Equilibrium** 語境：Dealing Range 內定義均衡，折價區為多方偏好、溢價區為空方偏好。

## 4. Imbalance（失衡家族）
- `Imbalance` 是上位家族「方向性不對稱交付」，不是單一 detector（CH-09）。
- **FVG**：三根封閉 K 線的方向性幾何區間——bullish `low(b3)>high(b1)`，bounds 凍結於第三根收盤；bearish 反之（CH-09）。
- Volume Imbalance 在 OHLC 層只是相鄰 close/open 或 body non-overlap 的價格 proxy（CH-09、CH-23）。
- 同家族：Liquidity Void（多 bar 低重疊快速交付）、BPR（兩獨立反向已確認區間之交）、IFVG（inversion）。CH-09 拒絕「所有失衡相同」「缺口必然回補」等升格。

## 5. 當日沖銷應用
- SMC 結構事件（BOS／CHoCH／imbalance／OB）是建立 Direction＋Entry 的元件，供 [[ict-daytrading-modules]] 做模型資格判定；fail-closed 時一律 NO_TRADE。

## 來源
^[raw/ict-smc/ict-smc-summary.md] ｜ DOC-00 CH-01、DOC-02 CH-04/05、DOC-03 CH-08、DOC-04 CH-09/10/11、DOC-08 CH-23。
