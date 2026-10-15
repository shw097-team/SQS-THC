---
title: ICT/SMC 當沖模組類別
created: 2026-08-21
updated: 2026-08-21
type: concept
tags: [daytrading, ict-module, method, scenario, ob-orderflow]
sources: [raw/ict-smc/ict-smc-summary.md]
confidence: high
---

# ICT/SMC 當沖模組類別（當日沖銷）

> 本頁以 DOC-06（CH-15/16/17）為主軸，把台股當日沖銷常用的 ICT/SMC 模型整理為**模組類別**，並掛上 fail-closed 治理：名稱不具資格權、事件資格 binary 判定、veto 優先。相關：[[ict-intraday-microstructure]]、[[smc-market-structure]]。

## 0. 治理：模型身份先於命名
- CH-15 管模型身份與生命週期（MMXM／ICT 13 Models；`DRAFT→RESEARCH_ACTIVE→PAPER_ACTIVE→DEMOTED/RETIRED`）。二創命名（MMXM derivative、Unicorn 等）不能取得 canonical 身份。
- 防 **model shopping**：同一段 movement 事後分別稱 Silver Bullet／Turtle Soup 屬反例，輸出 REJECTED／QUARANTINED。
- 唯一施工鏈：`有效上游物件 → 凍結 Model Portfolio → 綁定模型專屬 execution contract → 觀察專屬 sequence → SetupCandidate → binary qualification → qualified-only ranking → veto reducer`（CH-15/17）。

## 1. 依觸發本質的分類
| 類別 | 代表模型／component | 觸發語義 |
|---|---|---|
| 時間容器型 | Killzone、Silver Bullet（M03）、Opening Range、Session Model | 依 TimeGate／session 開啟的 temporal component；時間到 **不是** setup（DOC-05 CH-12、DOC-06 CH-16） |
| 流動性掠取型 | Turtle Soup／Failure Swing（M04）、Draw-on-Liquidity、Butterfly/Reversal | 對明確 prior liquidity 的 raid→reclaim→反轉確認（CH-06、CH-16） |
| 動能／延續型 | BOS continuation、Displacement/FVG momentum（M01）、Impulse | 已確認 displacement＋qualified array 的延續（CH-04/09/11、CH-06 M01） |
| 反轉型 | CHoCH／MSS reversal、Breaker/Rejection Block、OTE | 保護 swing 被破／供給需求區的反轉確認（CH-04/10、CH-16 OTE） |
| 序列型 | PO3／AMD、Range Model | 累積→操縱→分配序列，作 component 而非獨立 setup（CH-13-H2-07/08） |

## 2. 模型與 component 的分界（CH-16）
- 四個模型（Silver Bullet、Turtle Soup、OTE、Opening／Range／Session Models）各有**不可互換的專屬 sequence** 與必要條件；component（FVG、OTE、SMT、block）與 model 嚴格分離，否則任何 pattern 都可被包成策略（CH-15 防線）。
- Silver Bullet 在本冊是 M03 的 temporal component contract，非獨立方向／下單參數；window open 但 setup 失敗 → NO_TRADE（DOC-05 CH-12-H2-06、DOC-06）。

## 3. Setup 資格與 No-Trade（CH-17）
- `SetupCandidate` 走 **binary qualification**：模型專屬 sequence 必備條件未全部成立 → 保持 CANDIDATE／REJECTED，不以 optional 條件補足。
- hard **veto reducer** 優先於 ranking：bias 未定、risk gate 不滿、Freshness 過期、displacement／PD object 缺 → 一律 NO_TRADE。
- No-trade 是 headline：模型敘事成立 ≠ entry candidate 成立，錯過後不得追價補造 setup（CH-15/16）。

## 4. 接「當日沖銷」主軸
- 模組產出 SetupCandidate → 風控（risk budget、stop distance、position sizing）在 DOC-07 CH-20；執行與持倉在 CH-18/19；回測／驗證在 DOC-10 CH-25。
- 完整當沖流程對應決策權威鏈 `Universe→CandidatePool→MTF Bias→Scenario→TradeHypothesis`（參 [[ict-intraday-microstructure]] 的 HTF bias 輸入與 [[smc-market-structure]] 的結構元件）。

## 來源
^[raw/ict-smc/ict-smc-summary.md] ｜ DOC-03 CH-06、DOC-04 CH-09/10/11、DOC-05 CH-12/13、DOC-06 CH-15/16/17、DOC-07 CH-18/19/20、DOC-10 CH-25。
