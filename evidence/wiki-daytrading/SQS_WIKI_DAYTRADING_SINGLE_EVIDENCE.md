# SQS-WIKI 台股當日沖銷知識庫 — 建置完成（單一 Evidence MD）

**artifact_id:** `SQS_WIKI_DAYTRADING_SINGLE_EVIDENCE`
**建置:** 2026-08-21 · **主軸:** 台股當日沖銷 T+0（非隔夜）· **治理:** HGK / Fabric
**工具:** KANBAN + SWARM(多子代理) + GSTACK/OPENSPEC + Codex CLI

## 0. Claim Ceiling
```
SQS_WIKI_DAYTRADING_KB_BUILT
主軸 = 台股當日沖銷 (T+0); ICT/SMC = context/hypothesis 非直接決策
四套權威文檔大量導入完成
WIKI lint 全通過 (Codex PASS, local 0 broken/0 orphan)
方法為"知識載體", 不含 live 交易; Paper/live NOT_AUTHORIZED
```

## 1. 主軸確立（回應"當日沖銷非隔夜"）
- WIKI 13 概念頁全聚焦當日沖銷 T+0；**無任何頁宣稱隔夜留倉**。
- **Overnight Gate**（tw-ict-risk-gates, 源 TW-ICT v3.0 DOC-07）：日終無 fresh OvernightDecision 之 intraday 部位 **FORCED_FLATTEN，禁止自然留倉改隔日沖** —— 文檔規定把隔夜當禁止項，WIKI 正確呈現。
- 主軸方法鏈 `Universe→CandidatePool→MTF Bias→Scenario→TradeHypothesis`（TW-ICT v3.0 DOC-05）。

## 2. 四套權威文檔大量導入
| 位階 | 文檔 | raw DOC 數 | 承載概念頁 |
|---|---|---|---|
| 上位 | TW-ICT_v3.0_專業技術文檔 | 12 | tw-ict-mainline-method / tw-ict-risk-gates / ict-context-bias-scenario |
| 支援 | ICT&SMC_專業技術文檔 | 12 | ict-daytrading-modules / ict-intraday-microstructure / smc-market-structure |
| 支援 | 台股當沖_專業技術文檔_v3.0 | 14 | daytrading-t0-flow / stock-selection / open-auction / intraday-exits |
| 支援 | 市場資訊&台股趨勢_專業技術文檔_v2.0 | 16 | tw-market-index-structure / tw-funds-and-news-flow / tw-scenario-daytrading-suitability |

WIKI 結構：SCHEMA.md + index.md(13 concepts 登錄) + log.md + raw(48 來源) + concepts(13 頁)，Obsidian 相容。

## 3. 方法 inventory（lane1 抽取，19 項代表）
- 非補償式 gate 還原鏈 Rule→Data→Eligibility→Capability→Liquidity→Evidence→Score
- SetupQualificationRouter → QUALIFIED/OBSERVE/RESEARCH_ONLY
- ICT 模組五分類（時間容器/流動性掠取/動能延續/反轉/序列）
- 候選池 G1→G4 漏斗；試撮=觀測非成交；進場 precond→trigger→invalidation→expiry
- effective_R/approved_qty 風控；日損 Kill Switch 階梯；StopPlan 七類停損
- Overnight Gate：無 fresh decision 之部位 FORCED_FLATTEN

## 4. 驗收與自迭代修補
- **Codex lint**: 初 CONCERNS(3 HIGH: raw wikilink/源DOC缺失/指向錯) → **修補後 PASS**
  (修: market-trend 3頁 raw wikilink→plain, 補複製 16+14 源DOC, index raw段 backtick-only)
- **本地 lint**: 13 pages, 13 distinct wikilinks, **0 broken, 0 orphan** (inbound 2~12)
- **SWARM lane0**: PASS (10 PASS/1 PARTIAL/0 blocking) 主軸確認+四套導入確認
- **SWARM lane1**: PASS 方法 inventory 19 項 + 7 方法頁來源權威全解析無斷鏈

## 5. Nonclaims
- LOCAL/RESEARCH 知識庫; 方法為知識載體
- Paper/live/production NOT_AUTHORIZED
- ICT/SMC 定位為 context/hypothesis, 不直接變成 SetupOrder/Risk/OrderIntent

## 6. Stop
STOP_FOR_NEXT: WIKI 已建置驗收通過; 若要"用於當沖方法制定"下一步是: 依主軸方法鏈把 1 個當沖候選
(如 Open Auction Breakout / PO3) 接入 SQS method finalization(WF-09→10→11→08), 需 live/盤中資料
或先以盤中可離線資料做當沖回測(非隔夜)。未自我主張 production/live。
