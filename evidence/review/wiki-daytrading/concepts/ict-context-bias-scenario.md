---
title: ICT 模組、MTF 情境與 Bias/Scenario (CH-12/CH-15)
created: 2026-08-21
updated: 2026-08-21
type: concept
tags: [ict-module, smc, market-structure, bias, scenario, liquidity, regime, method]
sources:
  - raw/tw-ict-v3/TW-ICT_專業技術文檔_v3.0_DOC-05_2026-07-29_r2.md
  - raw/tw-ict-v3/TW-ICT_專業技術文檔_v3.0_DOC-06_2026-07-29_r2.md
confidence: high
---

# ICT 模組、MTF 情境編譯與 Bias/Scenario

> 主軸：台股當日沖銷。ICT/SMC 的模組與圖形只作 **context／hypothesis**，不得直接變成 SetupDecision、RiskAuthorization 或 OrderIntent。本頁對應 DOC-05 CH-12（多週期 Context Stack、Bias、Scenario）與 DOC-06 CH-15（named models、Taiwan adapter、setup qualification）。

## MTF（多週期）責任圖，不是投票

`ContextPacket` 是 frozen PIT bundle，先凍結 `future_information_cutoff`，所有 data `available_at <= cutoff`。`MTFResponsibilityMap` 指派高／中／低週期**責任**而非投票；`LTF cannot override HTF without explicit transition guard`；多週期多數決會混淆 horizon。`ContextStack` 保存 regime、range、session、event、conflicts；`unresolved_conflicts` 不可隱藏（拒絕 `D05-CONTEXT-CONFLICT-HIDDEN`）。

## Dealing Range / Session Profile / PO3 / AMD

- **DealingRangeContext：** 明示 range owner、premium/discount/equilibrium、DOL（Draw on Liquidity）、session、expiry 與 invalidation。拒絕固定模板與跨市場／跨 session 無轉譯。
- **Session Profile：** `TimeGateSpec` 不是固定鐘點清單，而是有效日期、target market、calendar、session、opening behavior、event window、global handoff、expiry 與 evidence tier 的契約。Opening Object 由官方日曆與 SessionMap 建立。
- **PO3（Power of 3）：** accumulation → manipulation → distribution 三階段；**必須有可觀察 phase rules**，不能事後把任意「震盪—假突破—趨勢」貼上三階段。
- **AMD：** 同 PO3 之 accumulation/manipulation/distribution 三階段判讀，屬 TIME 與 price action 的階段模型。
- **OTE：** dealing-range retracement component，須綁 current range owner、direction、PD location、trigger 與 no-chase；來源未支持的固定百分比不得作全市場規範。

## Bias（假說而非方向預言）

`BiasHypothesis`（owner R79/R13，producer WF-D05-10）是**可反駁、有 counter-evidence、invalidation、expiry 與 checker** 的假說。只有在 `BiasSupport + CounterEvidenceSet + BiasInvalidation + expiry + checker` 全部存在時才可 `SUPPORTED`。狀態：`BIAS_DRAFT → SUPPORTED / CONTESTED / INVALIDATED / EXPIRED`。缺 counter-evidence 拒絕 `D05-BIAS-NO-COUNTER`。SMT（Synchronous Market Technique）需 `PairRegistry + 同步 clock + CorrelationRegime`；**相關性不等於因果、事後挑 pair 是 hindsight**。

## ScenarioTree：恆五分支

`ScenarioTree`（owner R79/R69）必須**精確五分支**：Base / Bull / Bear / Unknown / Tail。每分支有 guards、invalidation、expiry 與 legal action。新 evidence 只能建立 `BranchSwitch`／new tree version，**不得回寫 T0**。狀態：`SCENARIO_DRAFT → ACTIVE_BASE/BULL/BEAR/UNKNOWN/TAIL → HANDOFF_READY / WAIT / NO_TRADE / ROUTE_BACK`。只寫 bullish path 等於把 scenario 變預言。

## ICT 模組體系（Component Registry, CH-15.7 & MOD cards）

模組拆成 `context, bias/scenario, time, structure, liquidity, DOL, delivery, PD Array, trigger, invalidation, target, expiry, counter-evidence`；缺任一必要 component 只能 `DRAFT/RESEARCH_ONLY/WAIT/REJECTED`。DOC-06 有 28 個 Named Module Cards（如 `MOD-D06-001 OHLCVNormalizer`, `002 BarConfirmationEngine`, `003 SwingDetector`, `005 KeyLevelRegistry`, `006 RangeOwnershipResolver`）；DOC-09 承載歷史 ICT 模組鏈 #1~107 的 failure oracle 檢定。關鍵取用：

| 模組 | 要點 |
| --- | --- |
| MMXM / MMBM / MMSM | 需 context、range、liquidity path、delivery shift、PD Array、trigger、invalidation、expiry；「market maker」只作 lineage，不證明真實機構行為 |
| AMD / PO3 | 三階段須可觀察 phase rules |
| Silver Bullet / Killzone | 海外時間窗須經 Taiwan adapter 重新映射校準，未認證前為 research hypothesis |
| Judas Swing | 需要 opening/session reference、誘導路徑、reclaim/delivery shift、expiry |
| Turtle Soup / OTE / Unicorn | 各綁 old high/low、range owner、PD collision resolver，只穿價／視覺重疊不足 |
| BOS/MSS/CHoCH/FVG/OB/DOL/premium-discount | 是 **components**，不是單獨 named model，不能 bypass component completeness |

## Taiwan Adapter（台股化）

海外 session/killzone、外匯跨日、DOM/footprint、無漲跌幅 gap 與 shorting 假設，一律先經 RuleSnapshot、SessionMap、CapabilityProfile、成本、流動性、標的類型與 effective-date 檢查。AdapterCertification：`CERTIFIED_RESEARCH / CERTIFIED_PAPER / CONDITIONAL / RESEARCH_ONLY / REJECTED / STALE/EXPIRED/UNKNOWN`。缺有效台股 mapping 時 R83 輸出 `RESEARCH_ONLY/NO_TRADE`。

## 相關頁
- [[tw-ict-mainline-method]]
- [[tw-ict-risk-gates]]
