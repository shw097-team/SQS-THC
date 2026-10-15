---
title: 當沖選股：候選池漏斗與股性
created: 2026-08-21
updated: 2026-08-21
type: concept
tags: [daytrading, liquidity, market-structure, method]
sources:
  - raw/daytrading-v3/daytrading-v3-summary.md
  - raw/daytrading-v3/daytrading-v3-sources.md
confidence: high
---

# 當沖選股：候選池漏斗與股性

> 主軸 = 台股當日沖銷（T+0）。選股不是「熱門榜挑股」；它是 `Universe → CandidatePool` 的非補償式漏斗，輸出的 CandidateCard **只表示可研究標的，不授權 OrderIntent**（DOC-04）。盤前/試撮/開盤候選池的時點與重驗見 [[daytrading-open-auction]]。

## 法定資格與方向（DOC-01，前置 G1）

- **當沖標的適格**：可現股當沖標的由制度/規則檔決定；**先賣後買**額外依賴券源（借券可用量、費用、回補限制），券源與借券成本是**時點化資料**，昨日餘額或口頭承諾不得沿用（CLM-DOC01-016）。
- 未沖銷/券差觸發**強制回補/交割 T+2 incident**；注意/處置/分盤/漲跌停會 override eligibility（CH-01-H2-05/08）。

## 候選池漏斗（G1~G4，DOC-04 CH-05）

```text
市場全集+主清單 → G1 制度/交易資格/處置/券源 → G2 資料時間/權利/freshness
→ G3 流動性/spread/depth/成交連續度/借券 → G4 成本/滑價/容量/可執行經濟性
→ CandidateTier/CandidateCard（研究用，非下單）
```
- 所有轉換 `validate → transform → state transition → reason code → versioned output`；輸入或規則未知輸出 `UNKNOWN/ROUTE_OUT`，**不補洞、不靠排序分數補償**。
- Pool 依 session 走 PREOPEN → AUCTION → OPEN → INTRADAY → TAIL_RESEARCH；新版本以 `supersedes` 使舊版 `EXPIRED`，**不得並存互相矛盾的自選清單**（`NO_CANDIDATE` 可輸出空池）。
- TAIL_RESEARCH pool 只交付 `RESEARCH_ONLY` 隔日研究候選，`NOT_HOLD_AUTHORIZATION`、`DOC09_APPROVAL_REQUIRED`——**與隔夜主軸切割**（見 [[daytrading-intraday-exits]]）。

## 股性：可驗證的 feature（DOC04-14）

「股性」拆成**分布與穩定度**的 `StockCharacterProfile`：波動、振幅、gap、spread stability、depth recovery、momentum persistence、mean reversion、event sensitivity。所有特徵需 `window + as_of + drift flag`；以主觀形容詞或單日表現永久定義股性 → 反例，樣本不足輸出 `UNKNOWN`。

## 排序：策略別、禁止萬用總分（DOC04-16）

排序是「**策略—時段—特徵**」三者的契約，各 RankingProfile 有 required/forbidden evidence，**無 universal score**；權重/閾值未校準時標 `CALIBRATION_REQUIRED`，不假造固定數字：

| Profile | Session | 關鍵 required evidence |
| --- | --- | --- |
| BREAKOUT-OPEN | OPEN | 開盤成交連續度、spread stability、相對強弱 |
| PULLBACK-INTRADAY | INTRADAY | 趨勢持續、回撤結構、流動性恢復 |
| REVERSAL-INTRADAY | INTRADAY | 極端偏離、成交反轉、counter-evidence |
| EVENT | PREOPEN/INTRADAY | Catalyst available_at、曝險、流動性 |
| RELATIVE-STRENGTH | OPEN/INTRADAY | 產業/市場基準後的相對表現 |

## 產業/Catalyst/籌碼為 conditional context

- 產業與 Catalyst 只能**在 QUALIFIED set 內調整 profile/confidence**，不改 gate state；題材熱度 ≠ 深度、受惠敘事 ≠ 公司曝險、市場廣度惡化時應成 counter-evidence（DOC04-15）。
- 籌碼/法人（三大法人、分點、融資融券、借券、集保）與供給風險作 supporting evidence，見 [[ict-context-bias-scenario]] 與相關策略；供給風險/隔日賣壓接口由 DOC-09 承接。

## 相關頁

- [[daytrading-open-auction]]
- [[daytrading-t0-flow]]
- [[smc-market-structure]]
- [[ict-context-bias-scenario]]
