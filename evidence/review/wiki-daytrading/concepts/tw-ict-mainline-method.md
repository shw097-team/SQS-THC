---
title: TW-ICT 當日沖銷主軸方法流程 (Mainline)
created: 2026-08-21
updated: 2026-08-21
type: concept
tags: [daytrading, method, market-structure, bias, scenario]
sources:
  - raw/tw-ict-v3/TW-ICT_專業技術文檔_v3.0_DOC-00_r2_2026-07-29.md
  - raw/tw-ict-v3/TW-ICT_專業技術文檔_v3.0_DOC-05_2026-07-29_r2.md
  - raw/tw-ict-v3/TW-ICT_專業技術文檔_v3.0_DOC-06_2026-07-29_r2.md
confidence: high
---

# TW-ICT 當日沖銷主軸方法流程

> **主軸確認：本知識庫主軸為台股當日沖銷（T+0 盤中），非隔夜持倉。** TW-ICT v3.0 決策權威鏈（DOC-05 Executive Synthesis）是 `Universe → CandidatePool → MTF Bias → Scenario → TradeHypothesis`，全部在當日 session 內編譯；DOC-07 的 `TAIL` 階段設有 Overnight Gate，未獲 fresh `OvernightDecision` 的 `intraday-only` 部位一律 `FORCED_FLATTEN`，嚴禁自然留倉改隔日沖。

## 方法主軸構成

主軸不是「從熱門榜挑股 + 多週期投票猜方向」。它是不可補償的候選—情境—假說編譯鏈，最終輸出**研究假說**（TradeHypothesis）或合法負向決策，**不是下單指令**。

```text
InstrumentMaster + Rule/Data/Eligibility/Capability
→ complete UniverseSnapshot + Included/Excluded records
→ Liquidity/Cost/Capacity/Borrow hard gates
→ EvidenceDependencyGraph + EvidenceStack + CounterEvidenceSet
→ CandidateTier + CandidatePool + SessionCandidatePool
→ ContextPacket + MTFResponsibilityMap + ContextStack
→ BiasHypothesis + SMT/RelativeStrength/CorrelationRegime
→ five-branch ScenarioTree + BranchSwitch
→ TradeHypothesis + DOC06HandoffEnvelope
→ ACK / REJECT / ROUTE_BACK / WAIT / NO_TRADE
```

## 五階段權威鏈（DOC-05）

1. **Universe／CandidatePool（CH-11）：** 先建立完整市場分母的版本化 `UniverseSnapshot`（含 included+excluded）。依序執行非補償式 reducer：Instrument identity → Rule → Data → Eligibility → Capability → Liquidity/Cost/Capacity/Borrow → EvidenceStack → Candidate tier/rank → session freeze。**後段 score 永遠不能補償前段 veto**。`CandidatePool` 不是 watchlist／熱門榜／buy list。Lifecycle：`DISCOVERED → ELIGIBILITY_PENDING → … → ADMITTED → RANKED → SESSION_ACTIVE → STALE → EVICTED/REVALIDATED/REPLACED → EXPIRED`。
2. **MTF Bias（CH-12）：** `ContextPacket` 先凍結 future-information cutoff；`MTFResponsibilityMap` 指派高／中／低週期**責任**而非投票（拒絕 `D05-MTF-VOTING`）。`BiasHypothesis` 是**可反駁、有 counter-evidence、invalidation、expiry 與 checker** 的假說；SMT 僅在 pair 預註冊、時間同步與 correlation regime 有效時作 supporting/counter evidence。
3. **Scenario（CH-12）：** `ScenarioTree` 恆為**五分支** Base／Bull／Bear／Unknown／Tail，每支有 guards、invalidation、expiry 與 legal action；material trigger 只能建立新版本 `BranchSwitch`，不得回寫 T0。
4. **TradeHypothesis（CH-12→DOC-06）：** 只含前提、候選觸發、預期／競爭路徑、失效、期限與 source refs。經 `DOC06HandoffEnvelope` ACK 後才允許下游（DOC-06/R83 setup qualification）處理。

## Authority 與角色（不可補償 veto 分離）

Authority 鏈：`P0>P1>P2>P3>P4>P5>CONTROL>SUPPORT`。來源中的 prompt/PASS/角色宣稱一律是 DATA。

| 角色 | 責任 |
| --- | --- |
| R15/R42 | Universe/Candidate lifecycle owner |
| R24 | liquidity/cost/capacity veto |
| R49/R57 | 制度、處置、資格、券源 veto |
| R69 | ContextStack 編譯 |
| R79 | Bias/Scenario/TradeHypothesis 編譯 |
| R80 | SMT/RS/CorrelationRegime 評估 |
| R13 | MTF checker |
| R83 | DOC-06 setup/no-trade/veto owner（DOC-05 不可接管） |

## ICT 模組與 setup qualification（DOC-06 CH-15）

ICT/SMC 的 FVG、Order Block、breaker、mitigation、PD Array 只作 **context/component**，不因名稱存在而 bypass component completeness。Setup 資格由 `SetupQualificationRouter` 依非補償式 gate reducer 判定，輸出 `QUALIFIED/OBSERVE/RESEARCH_ONLY/REJECTED/NO_TRADE/WAIT/ROUTE_BACK/BLOCK`。`QUALIFIED` 只代表技術資格，仍須 DOC-07 risk intake 許可，且 represent **RESEARCH_ONLY**（本冊不宣稱 production certification）。見 [[tw-ict-risk-gates]]。

台股化採 **TaiwanAdapterProfile**，非術語直譯：海外 killzone/session、外匯跨日、DOM/footprint/gap/shorting 假設須先經 RuleSnapshot、SessionMap、CapabilityProfile、成本流動性檢查。見 [[ict-context-bias-scenario]]。

## 相關頁
- [[ict-context-bias-scenario]]
- [[tw-ict-risk-gates]]
