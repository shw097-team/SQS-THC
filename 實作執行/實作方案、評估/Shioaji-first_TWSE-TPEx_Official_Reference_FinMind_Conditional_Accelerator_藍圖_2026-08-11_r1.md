# Shioaji-first + TWSE/TPEx Official Reference + FinMind Conditional Accelerator 藍圖

> **System Integration / Evidence Contract / Fail-Closed Blueprint**  
> 專案：SQS-THC × TW-ICT FSDT Stack  
> 日期：2026-08-11（Asia/Taipei）  
> 版本：`2026-08-11_r1`  
> 任務型態：`DESIGN` with `EVAL / SEARCH_ONLY / DRIFT_PROBE` children  
> **最終裁決：FAIL-CLOSED（Runtime / Provider / Release）**  
> **Author-side Design 狀態：CONSTRUCTION_READY_WITH_CR_OPEN**  
> Claim Ceiling：`SESSION_CONTEXT_BOOTSTRAPPED / AUTHOR_SIDE_DESIGN_ONLY`  
> Runtime / Provider Admission / XQ Parity / Independent NRTV / Paper / Shadow：`NOT_RUN`  
> Live：`BLOCKED`；Production：`NOT_CLAIMED`

**一句話核心結論：** 不重做既有 `DatasetVersion / PIT / Parquet / DuckDB / SQLite / Provider Admission / XQ-HITL` 架構；以 **Shioaji 作「MVP 台股 intraday historical + realtime + simulation 的 primary candidate」**、以 **TWSE/TPEx 作 official rule/universe/reference authority**、以 **FinMind 作 empirical-triggered conditional research/backfill accelerator**，並把所有 provider 維持 `ADMISSION_PENDING`，直到 rights、account entitlement、throughput、timestamp/parity、security、fallback、simulation、XQ parity 的可重播 evidence 全部閉合。

---

## 0. Evidence Contract / 使用契約

本藍圖嚴格區分：

- **NORMATIVE**：本次指令、P0-CIP、SQS/TW-ICT 主藍圖與工程 DOC、實作前包、Final PACK/控制工件、目前兩份使用者提供的決策/缺口附件，以及 GRP 控制規則。
- **SUPPORT**：2026-08-11 前可驗證的 Shioaji、TWSE、TPEx、FinMind、DuckDB、uv、GitHub/OpenSSF、Microsoft 與研究資料。SUPPORT 只能回答「現行能力/限制/技術選型」，不得反向改寫 Financial/Risk/Execution truth。
- **UNVERIFIED**：沒有 exact source/anchor、沒有 current provider entitlement、沒有 empirical run、沒有 rights/price receipt、沒有 RepoContext 的任何主張。
- **FAIL-CLOSED**：若 critical prerequisite 缺 evidence，對應 capability 必須 `DENY / HOLD / TEMP_CLOSED / ADMISSION_PENDING`；不得以「看起來可用」補成 PASS。

### 0.1 本輪 physical coverage readback

本輪對 `/mnt/data` 直接枚舉並掃描全部 Markdown 實體檔（不是抽樣），得到：

- Markdown files：**138**
- Bytes：**83,767,017**
- Logical lines：**816,833**
- Aggregate content-digest（per-file SHA digest concat 再 SHA-256）：`4174b4558f1cfcb432b74d13a5ce5c810be282fc6d4c712798933fadfa3abedb`
- 本題關鍵詞命中文件：**129 / 138**
- `FinMind`：204 occurrences / 15 files；`Shioaji`：339 / 9；`TT-DATA-PROVIDER-PARITY`：93 / 7；`TT-BROKER-PROVIDER-ADMISSION`：60 / 6。

**證據邊界：**上述是本輪 direct physical denominator / keyword full-scan，不等於宣稱本輪逐字重新語義精讀 138 檔。語義裁決依 exact source locators、既有 Target100 full-read audit、相關全文檢索與本輪兩份附件 full-read 組合完成。

---
## 1. Inputs Manifest 與定位證明

### 1.1 Authority / Source Family Manifest

| 來源 / 檔案族 | Role | 定位證明 | 狀態 | 本藍圖採用 |
|---|---|---|---|---|
| 本次任務指令 | NORMATIVE A0 | 本頁最新 user instruction | FOUND | 交付格式、Fail-Closed、100% denominator、Web SUPPORT、單一 MD |
| `PORTABLE_MOUNT_PROFILE.md` | CONTROL | GRP00_PORTABLE_MOUNT_PROFILE v2026.08.07-final-r2 | FOUND | task-kind/router/security/claim ceiling |
| `DEPLOYMENT_PROMPT.md` | CONTROL | portable mount bootstrap/degrade/readback | FOUND | session mount、no install claim |
| `GRP-00~09` + `AGENTS.md` | CONTROL | Primary/Secondary GRP router；RepoContext/TaskSpec/evidence/release | FOUND | Files-first、provider lifecycle、security、NRTV、handoff、release |
| `SQS-THC_P0-CIP-PACK_v2026.08.06-r2` + vol01~10 | NORMATIVE | physical mount + source locators | FOUND | 台股當沖 first、data granularity、FinMind/TWSE/TPEx/Shioaji/XQ 原始角色 |
| `SQS-THC_藍圖_2026-08-01_r2` | NORMATIVE via P0 lineage | SQS P0 source fence / source register | FOUND_IN_P0 | Product/owner/tool replaceability |
| `Hermes_AGENT_SPEC...收斂藍圖_2026-08-02_r2` | NORMATIVE via P0 lineage | SQS P0 source fence | FOUND_IN_P0 | Hermes manager / bounded worker / no direct authority |
| `Spartoi_to_SQS-THC_整合收斂藍圖_2026-08-02_r2` | NORMATIVE via P0 lineage | SQS P0 source fence | FOUND_IN_P0 | Taiwan day-trading vertical kernel / tool adapter tier |
| `SQS-THC_最終整合收斂藍圖_2026-08-02_r2` | NORMATIVE via P0 lineage | SQS P0 source fence | FOUND_IN_P0 | final convergence / fail-closed |
| `SQS-THC_工程開發文檔_DOC-00~12` | NORMATIVE | 13 physical files | FOUND | typed objects、daily run、permissions、evidence |
| `TW-ICT_FSDT-Stack_P0-CIP-PACK...rFINAL-r2` + vol01~10 | NORMATIVE | 11 physical files | FOUND | Financial Contract Kernel、PIT/backtest/legacy RBWI migration |
| `TW-ICT_FSDT-Stack_藍圖_r2` | NORMATIVE via TW P0 lineage | embedded/source register | FOUND_IN_P0 | Financial truth / execution separation |
| `TW-ICT_RBWI_v3.0.0_r2` | NORMATIVE via TW P0 / engineering locators | source locators in SQS Engineering/TW P0 | FOUND_IN_LINEAGE | Fast loop、T0/T1、HITL、one-year local minute-K legacy baseline |
| `TW-ICT_FSDT-Stack_專業技術文檔_DOC-00~29` | NORMATIVE | 30 physical files | FOUND | PIT/Five Clocks、backtest/model risk、tools、execution/reconciliation |
| `TW-ICT 專業技術文檔 v3 DOC-00~11` | DONOR/NORMATIVE by route | 12 physical files | FOUND | detailed workflow/tool donor；不得覆蓋 owner truth |
| `XQ&XS DOC-00~13` | DONOR/SUPPORT | 14 physical files | FOUND | XQ/XScript/Radar/visual/microstructure parity；不作 broker truth |
| `Spartoi SP-TS-00~10` | DONOR | 11 physical files | FOUND | AgentOS/harness/security/handoff donor |
| `HG-KSEOS...r2` | DONOR | physical package | FOUND | Windows/Hermes/Codex substrate；runtime 不推定 |
| `實作前開發文檔包 G01/G02/G03 r2` | NORMATIVE A2 projection | 3 physical files | FOUND | Product/Financial + engineering/tool + trace/acceptance |
| `RBWI_WP_CONTROL_PACK 總藍圖/全冊藍圖/規格/方案` | NORMATIVE current projection | physical files | FOUND | current L1/DOC/WP/CTL/provider-neutral construction contract |
| `G01~G07 FULL GROUP r2` | NORMATIVE read-only delivery projection | 7 physical files | FOUND | current Final DOC bodies；runtime gates remain NOT_RUN |
| `TOOL_REGISTRY.md` | NORMATIVE sidecar | G02/G07 reader contract points to `../registries/TOOL_REGISTRY.md` | **MISSING_DIRECT_CONTENT** | CR_OPEN：不可宣稱完整 physical pack 已/未有 Shioaji/FinMind named row |
| `WINDOWS_EXECUTABLE_RECIPES.md` | NORMATIVE sidecar | G02/G07 reader contract points to `../install/WINDOWS_EXECUTABLE_RECIPES.md` | **MISSING_DIRECT_CONTENT** | CR_OPEN：實際 repo command/runtime recipe 不可宣稱已 materialized |
| `SQS-THC × TW-ICT...台股歷史資料...成本鑑定.md` | NORMATIVE current decision memo | full-read + SHA in current mount | FOUND | Shioaji-first、data tiers、cost uncertainty、FinMind conditional |
| `修補為具名 preferred candidate admission pending.md` | NORMATIVE current gap memo | full-read + SHA in current mount | FOUND | named-provider materialization gap / no silent supersession |
| 2026 Web/official/GitHub/research | SUPPORT only | §4 Web Source Register | FOUND | capability/drift/limit/tool selection；不得覆寫 NORMATIVE |

### 1.2 Key Normative Locator Register

| ID | File | Locator | What it proves |
|---|---|---|---|
| `N-P0-DATA-ROLE` | `SQS-THC_P0-CIP資料_vol-03.md` | `L10067` | L2 Data：FinMindAdapter/TWSEAdapter/TPExAdapter/ShioajiMarketDataAdapter；日線、分鐘、tick、五檔、5秒委託成交。 |
| `N-P0-GRANULARITY` | `SQS-THC_P0-CIP資料_vol-03.md` | `L10085-L10090` | 日線→30/15m→5/3m→1m→Tick/5秒→Order book；Tick/Order book 僅 confirmation/execution-risk，不能單獨入場。 |
| `N-P0-PHASE` | `SQS-THC_P0-CIP資料_vol-03.md` | `L10224, L10240` | P2 Data+Universe = FinMind/TWSE/TPEx；Shioaji/XQ 分別承擔 broker/API 與 paper/UI 等不同角色。 |
| `N-P0-MIN-LOOP` | `SQS-THC_P0-CIP資料_vol-03.md` | `L7977-L7978` | daytrade universe → minute/tick data quality；先做最小台股當沖研究閉環。 |
| `N-TW-1Y-BT` | `TW-ICT_FSDT-Stack_P0-CIP資料_vol-09.md` | `L140, L162-L163, L605` | 一年分K回測／本地分K一年盲審；為 legacy/upstream operational baseline，非永久 retention law。 |
| `N-FINAL-DATA-TT` | `SQS-THC_TW-ICT_FSDT-Stack_實作RBWI_WP_控制工件_PACK_全冊藍圖_2026-08-09_r2.md` | `L2434-L2986 multiple anchors` | 外部 feed timestamp/parity、storage/rights、流動性/成本需 TT-DATA-PROVIDER-PARITY。 |
| `N-FINAL-BROKER-TT` | `G03_RBWI_Execution_Agent_Harness(3).md` | `L472-L544` | TT-BROKER-PROVIDER-ADMISSION；external writes OFF；provider admission 未執行。 |
| `N-FINAL-PROVIDER-LC` | `G07_Tool_Provider_PRW_Windows(3).md` | `PKG-L1-17.1~17.5` | CapabilitySlot→RuntimeAdmissionState→ToolDecision/PinLock/License/Security/Pilot/Parity→Fallback/Uninstall/Exit。 |
| `N-FINAL-EXEC` | `G03_RBWI_Execution_Agent_Harness(3).md` | `PKG-L1-30/31` | External write fence、idempotency、UNKNOWN→HOLD+QUERY-before-retry、BoR/reconciliation；Live BLOCKED。 |
| `N-CURRENT-COST` | `SQS-THC × TW-ICT FSDT Stack｜台股歷史資料實際需求、最佳取得管道與成本鑑定.md` | `§2-22` | 本輪既有決策 memo：Shioaji-first；1m 12~24m；Tick bounded；FinMind conditional；費用未證實者保留 TT。 |
| `N-CURRENT-GAP` | `修補為具名 preferred candidate  admission pending.md` | `named-provider materialization gap` | 上游具名 provider 在 Final G01~G07 body 不可見；缺口是 named binding，不是 data architecture 缺失。 |


### 1.3 Current two attachments detached readback

| File | Bytes | Lines | SHA-256 | Status |
|---|---:|---:|---|---|
| `修補為具名 preferred candidate  admission pending.md` | 9,781 | 380 | `243ae8e1c19b2c41016375cba94bb1f1ccbc8f1d66b76ca3041af0fa3328ce5c` | FULL_READ |
| `SQS-THC × TW-ICT FSDT Stack｜台股歷史資料實際需求、最佳取得管道與成本鑑定.md` | 23,662 | 859 | `2d82378f000c296eedf85aa9b823b67f41bff6ef6aa538d08e2aec9dd51044a5` | FULL_READ |

---
## 2. Authority Stack & RCA

### 2.1 Adjudication Priority

```text
A0  本次任務 / current user decision memos
 ↓
A1  SQS-THC + TW-ICT P0-CIP / original product-financial intent
 ↓
A2  實作前開發文檔 G01/G02/G03 + SQS/TW engineering DOC
 ↓
A3  Current RBWI/WP/CONTROL PACK / Final G01~G07 + current control artifacts
 ↓
A4  GRP process/control contract (routing, provider lifecycle, evidence, release)
 ↓
A5  Donor technical docs (TW-v3 / XQ&XS / Spartoi / HG-KSEOS)
 ↓
SUPPORT 2026 official web / GitHub / OpenSSF / research
```

衝突規則：低位來源不得反向覆寫 Product/Financial truth；但 **current A0 patch 可以在保留 owner/claim boundary 下改變 provider preference**。因此本藍圖把 P0 的「FinMind data + Shioaji broker」保留為 lineage，但依 current requirement 與 2026 capability drift 把 runtime candidate 收斂成 `Shioaji-first`；這不是宣告 FinMind 被淘汰，而是 `conditional accelerator`。

### 2.2 RCA Root-Cause Tree

#### RCA-01｜症狀：先前曾回答「沒有歷史資料 provider 規劃」
- **根因 A：** 把 `provider_admission=NOT_RUN` 誤讀成 `provider_plan=MISSING`。
- **根因 B：** Final G01~G07 body 將 provider identity 抽象成 CapabilitySlot/ProviderIdentity，但 P0 具名 FinMind/Shioaji 未在 group body literal materialize。
- **證據：** `N-P0-DATA-ROLE`、`N-FINAL-PROVIDER-LC`、current gap memo。
- **修正：** `plan existence`、`named binding`、`runtime admission` 三軸分開；absence from group body 不等於 superseded。

#### RCA-02｜症狀：FinMind 一度被當成 historical default
- **根因：** 把「資料種類廣 / research warehouse 便利」錯當成「day-trading MVP 必需」。
- **證據：** P0 的核心顆粒度是 intraday price/microstructure；Tick/OrderBook 只作確認/執行風險；one-year minute-K 曾是 RBWI baseline。
- **修正：** 需求驅動 provider：MVP 先 1m + recent tick/bidask + official rules；FinMind 只在 trigger 成立時 admission。

#### RCA-03｜症狀：歷史長度容易被「資料越多越好」支配
- **根因：** 沒把 trading horizon、independent validation 與 storage cost 分離。
- **證據：** `TW-ICT_FSDT-Stack_P0-CIP資料_vol-09.md:L162-L163/L605` 的一年分K；Final PKG-L1-25 要 PIT/IS-OOS/walk-forward/cost/independent validation。
- **修正：** 1m retention 為 **policy parameter**，不是 truth；初始 patch = 18~24m；必須用 OOS/walk-forward 判定是否延長。

#### RCA-04｜症狀：同一 provider 同時被期待當 source-of-record、transport、broker truth
- **根因：** authority/transport/operational surface 未拆開。
- **修正：** `TWSE/TPEx = official reference authority`；`Shioaji = bounded data/broker runtime candidate`；`FinMind = conditional acquisition accelerator`；`XQ = parity/HITL surface`；local `DatasetVersion` = reproducible research object，不是 exchange/broker truth。

#### RCA-05｜症狀：可設計但不能證明可跑
- **根因：** 缺 account entitlement、Shioaji bandwidth tier、actual bytes/symbol、rights receipt、provider parity、XQ runtime、RepoContext。
- **證據：** `TT-DATA-PROVIDER-PARITY`、`TT-BROKER-PROVIDER-ADMISSION`、`TT-EXECUTION-PROVIDER`、`TT-XQ-RUNTIME` 全仍 open。
- **修正：** 本藍圖以 pilot gates 把 unknown 變成可關閉 TT；在 gate 前 `FAIL-CLOSED`。

#### RCA-06｜症狀：可能引入 Airflow/Kafka/ClickHouse 等過重系統
- **根因：** 把 future scale 當 current requirement。
- **證據：** P0 已將 ClickHouse/QuestDB 等 heavy data layer 延後，DuckDB/Parquet 為 local research baseline。
- **修正：** Windows Task Scheduler + deterministic Python worker + Parquet/DuckDB/SQLite；只有 measured bottleneck 才開 CR 升級。

---
## 3. 2026 Web Research Summary（SUPPORT ONLY）

> Research cutoff：2026-08-11。8/9~8/11 未發現足以推翻架構的新官方重大公告；本輪重點是驗證 live docs/current capability/limits/rights。每一個重大選型至少以「project normative + 一到多個 official/support source」交叉；外部來源不取得 norm authority。

### 3.1 Shioaji：為何升為 MVP primary candidate

1. **Historical 能力**：官方 Historical Market Data 支援 stock Ticks 與 minute Kbars；stock history 自 2020-03-02；Kbars 單次 date range ≤30 天；官方明示這些接口供 after-market analysis/backtest，盤中不可 polling，應用 subscription。`[WEB-SJ-01] + [WEB-SJ-02]`
2. **Realtime continuity**：官方 Quick Start/stream docs 支援 `tick / bid_ask / quote`，Python/CLI/HTTP，HTTP server 可透過 SSE 收流。`[WEB-SJ-03] + [WEB-SJ-07]`
3. **Simulation / future execution**：Simulation mode 可 market data + place/update/cancel order + positions/P&L；正式 order/action 仍需 signing/test/permission/CA。`[WEB-SJ-05] + [WEB-SJ-06]`
4. **Least privilege 可落地**：API key 可選 Market/Data、Account、Trading、Production、account、expiry、allowed IP；因此能把 data worker 與 simulation/live execution key 真正分權。`[WEB-SJ-04] + [WEB-SJ-05]`
5. **限制是可工程化的**：daily bandwidth / request-rate / subscription count 有明示限制；因此不能假定「2年×全市場×tick」可一次抓完，必須用 bounded universe + quota-aware pilot。`[WEB-SJ-01] + [WEB-SJ-02]`

**Adjudication：** Shioaji 的現行 capability 已超過早期 P0 只把它視為 broker/simulation candidate 的狹義角色；把它升為 `primary_intraday_provider_candidate` 與 current A0 需求一致，但**runtime state 仍是 ADMISSION_PENDING**。

### 3.2 TWSE / TPEx：官方 reference authority

- TWSE OpenAPI 提供 daily、當沖 eligible/suspension、5秒統計、除權息、margin、交易日等官方資料入口；TPEx OpenAPI 提供 OTC 對應的 daily/eligible/suspension/margin/disposition/除權息等。`[WEB-TWSE-01] + [WEB-TPEX-01]`
- 若某 dataset 採政府資料開放授權條款，才可依其授權使用；不能把「政府平台一般 ODL」擴張成所有交易所資料均同授權。`[WEB-ODL-01] + dataset-specific rights receipt required`
- 高粒度歷史委託/成交/揭示檔為 Data E-Shop paid/licensed lane，MVP 不能因為「更官方」就直接採購。`[WEB-TWSE-ESHOP-01] + N-P0-MIN-LOOP`

### 3.3 FinMind：為何保留但降成 Conditional Accelerator

- FinMind 仍提供廣泛台灣金融 dataset 與 historical tick/Kbar；部分能力受 Backer/Sponsor/SponsorPro entitlement。`[WEB-FM-01] + [WEB-FM-05]`
- 2026-06 的 full-day storage_objects 是 SponsorPro 且只從功能上線後累積，不是 2 年 historical backfill shortcut。`[WEB-FM-02] + [WEB-FM-01]`
- 資料使用權依來源與方案；不得把 GitHub Apache-2.0 軟體 license 當 raw data redistribution rights。`[WEB-FM-03] + [WEB-FM-04]`
- current exact Sponsor/SponsorPro checkout price 在本輪可驗證的公開官方文件中未取得，因此 **不得硬填舊價**；維持 `CR-FINMIND-PRICE`。

### 3.4 OSS / platform：不造輪子但不過度工程化

- **DuckDB + Parquet**：官方支援 Parquet 原生讀寫、pushdown、Hive partitioning，符合 existing local-first architecture；不引入 lakehouse。`[WEB-DUCK-01] + [WEB-DUCK-02]`
- **uv**：用 `uv.lock` / locked sync 管 Python dependency；避免自寫 environment manager。`[WEB-UV-01] + existing P0 reproducibility requirement`
- **Windows Task Scheduler**：MVP 用 `schtasks` 排 deterministic local workers，不先引入 Airflow/Dagster。`[WEB-MS-01] + existing Windows-first architecture`
- **GitHub/OpenSSF**：Actions 第三方 action pin full SHA、最小 token permissions；OpenSSF Scorecard 只作 SUPPORT/security signal，不能替代 semantic/runtime/provider admission。`[WEB-GH-01] + [WEB-OSSF-01]`

### 3.5 2026 research cross-check

近期研究再次說明：聚合式金融資料若沒有 announcement/available-at/revision chronology，會出現 PIT leakage；Taiwan-equity research 也把 PIT chronology/temporal causality 當必要 precondition。這只用來支持既有 FSDT `PIT/Five Clocks/DatasetVersion`，**不增加新 Product truth**。`[WEB-RES-01] + [WEB-RES-02] + [WEB-RES-03]`

---
## 4. Integrated Solution — 最小磨合架構

### 4.1 Target Architecture

```text
                     ┌────────────────────────────┐
                     │  TWSE / TPEx Official Ref  │
                     │ rules / universe / calendar│
                     └──────────────┬─────────────┘
                                    │ official-reference snapshots
                                    ▼
┌────────────────────────────────────────────────────────────────────┐
│                  Taiwan Data Acquisition Boundary                  │
│                                                                    │
│  Shioaji DATA key (Market/Data only)     FinMind conditional slot  │
│  ├─ Historical Kbars/Ticks                ├─ bulk/backfill trigger  │
│  ├─ Realtime Tick/BidAsk                  ├─ broad research trigger │
│  └─ usage/quota telemetry                 └─ parity trigger         │
└──────────────────┬───────────────────────────┬──────────────────────┘
                   │                           │ only when admitted
                   ▼                           ▼
            immutable raw zone          immutable raw zone
                   └──────────────┬────────────┘
                                  ▼
                       Data Contract / PIT Gate
                       schema / clocks / rights
                       gaps / duplicate / parity
                                  ▼
                         DatasetVersion + Lineage
                                  ▼
                ┌─────────────────┴──────────────────┐
                ▼                                    ▼
          Parquet canonical                     SQLite metadata
      raw/core/derived partitions          catalog/rights/receipts
                │
                ▼
              DuckDB
                │
      ┌─────────┼───────────┐
      ▼         ▼           ▼
   Backtest    Replay     RBWI candidate query
 PIT/OOS/WF  Cost/TCA      (read-only)
      │
      ▼
 Independent Validation
      │
      ├──────────────► XQ/XS backtest/visual parity (support surface)
      │
      └──────────────► Shioaji SIM (separate key/profile; no live)
```

### 4.2 Role / Authority Matrix

| Component | Architecture role | Writes canonical product/financial truth? | MVP state |
|---|---|---:|---|
| TWSE / TPEx | official rules/universe/reference authority | only source facts in own domain | REQUIRED_REFERENCE |
| Shioaji Historical | intraday historical carrier candidate | NO | ADMISSION_PENDING |
| Shioaji Realtime | current market-data runtime candidate | NO | ADMISSION_PENDING |
| Shioaji Simulation | broker simulation candidate | NO; only broker/sim facts | ADMISSION_PENDING / external action fenced |
| Shioaji Live | future execution adapter | broker facts only after receipt | **BLOCKED** |
| FinMind | research/backfill/parity accelerator | NO | CONDITIONAL_NOT_REQUIRED |
| XQ/XS | XScript/Radar/visual/backtest/HITL parity surface | NO | runtime/parity NOT_RUN |
| Parquet/DuckDB | local reproducible research store | NO | DESIGN_DEFAULT |
| DatasetVersion/PIT gate | versioned research data contract | owns research dataset identity only | DESIGN_DEFAULT |
| Independent Validation | backtest/model-risk verdict | ValidationReceipt only | NOT_RUN |

### 4.3 Data Granularity / Retention Policy

> 以下「Recommended initial target」是 **A0 design patch candidate**，不是偷偷把 retention 變成 Financial truth；只有上游 one-year minute-K baseline 與 granularity 是 source-grounded。任何延長/縮短要由 empirical OOS/regime/throughput evidence 開 CR。

| Data | NORMATIVE basis | Recommended initial target | Universe | Why / fail rule |
|---|---|---|---|---|
| Daily OHLCV | 日線 = Bias/DOL/context | 2–5 years | all eligible TWSE/TPEx | 儲存成本低；只做 context，不代表 intraday sample sufficiency |
| **1-minute K** | 1m = entry refinement；legacy RBWI = one-year local minute-K | **18–24 months** | research/tradable universe | primary backtest carrier；可切 IS/OOS/WF；不足則 CR extend |
| 3m/5m/15m/30m | P0 explicit timeframes | **do not separately download** | derived | deterministic resample from canonical 1m；避免 vendor aggregation drift |
| Tick trade | execution confirmation/TCA | 3–12 months initially + forward capture | liquid/microstructure subset | 不做全市場2年；若 Cost/TCA oracle證明不足再擴大 |
| BidAsk top-5 | microstructure confirmation | forward + case windows | active candidate subset | Shioaji BidAsk 是 top-5，不宣稱 full order-event book |
| Full order/trade event book | not MVP requirement | DEFER | case-specific | 只有 institutional microstructure requirement 成立才評估 Data E-Shop |
| Fundamental/chip | context/slow-loop/T1 | selected features only | as required | PIT/known-at/revision 不完整即拒絕進 backtest |

### 4.4 Universe policy

- **Full market**：只需要 official daily universe/rule snapshot 與低成本 daily context。
- **Research universe**：用 historical liquidity/eligibility 建立，初期可由 bounded list 啟動；不得因 provider quota 暗中改變 strategy eligibility。
- **Intraday subscribed universe**：必須受 Shioaji current subscription cap/quotas 控制；超出能力時先縮小/分層 candidate pool，不能 silent drop 無 evidence。
- **Microstructure subset**：只有需要 Tick/BidAsk/TCA 的高流動候選；不等同全市場。

### 4.5 Provider Capability Slots（修補 named-provider materialization gap）

```yaml
capability_slots:
  CAP_TW_OFFICIAL_RULE_REFERENCE:
    owner: Taiwan_Rule_Rights_Privacy_Owner
    providers: [TWSE, TPEx]
    state: REQUIRED_REFERENCE
    writes: [MarketRuleProfile, InstrumentEligibility, CalendarReference]

  CAP_TW_INTRADAY_MARKET_DATA:
    owner: Tool_OSS_Provider_Qualification_Owner
    preferred_candidate: Shioaji
    state: ADMISSION_PENDING
    scope:
      - historical_1m_kbars
      - historical_ticks_bounded
      - realtime_tick
      - realtime_bidask
    prohibited:
      - canonical_financial_truth
      - autonomous_order_submit
    fallback:
      historical: last_accepted_DatasetVersion_for_research_only
      realtime: HOLD_NO_NEW_INTRADAY_DECISION

  CAP_TW_BROKER_SIMULATION:
    preferred_candidate: Shioaji
    state: ADMISSION_PENDING
    mode: SIMULATION_ONLY
    live: BLOCKED

  CAP_TW_RESEARCH_ACCELERATOR:
    candidate: FinMind
    state: CONDITIONAL_NOT_REQUIRED
    activate_if_any:
      - SHIOAJI_BACKFILL_SLO_FAILS
      - FULL_MARKET_INTRADAY_BULK_REQUIRED
      - BROAD_CHIP_OR_FUNDAMENTAL_DATA_REQUIRED
      - SECOND_PROVIDER_PARITY_REQUIRED
    admission_requires:
      - current_price_receipt
      - plan_entitlement_receipt
      - dataset_rights_receipt
      - provenance_and_PIT_audit
      - parity_fixture
```

### 4.6 Event Matrix

| Event / Clock | Producer | Mandatory inputs | Action | Output / evidence | Fail-closed |
|---|---|---|---|---|---|
| D-1 / pre-open | Official rule worker | TWSE/TPEx source profile | fetch rule/universe/calendar diffs | `OfficialRuleSnapshot` + hash | stale/rights/error → affected instrument `INELIGIBLE_OR_UNKNOWN` |
| Pre-open candidate | RBWI candidate worker | last accepted DatasetVersion + today rule snapshot | liquidity/eligibility screening | `SessionCandidatePool` | missing rules/data → HOLD/NO_TRADE; no quota-driven silent eligibility change |
| 08:5x | stream supervisor | Shioaji DATA key + candidate pool | validate quota/connection, subscribe | `StreamStartReceipt` | login/permission/sub cap fail → HOLD realtime lane |
| 09:00–13:30 | Shioaji stream | tick/BidAsk | append raw events; no order action | raw JSONL/Parquet spool + heartbeat | data gap → DEGRADED; no fake fill/order |
| intraday minute boundary | local reducer | raw ticks or provider minute feed | deterministic 1m aggregate | `MinuteBarCandidate` | non-monotonic/gap/OHLC invariant fail → QUARANTINE bar |
| market close + buffer | historical worker | Shioaji historical permission | query Kbars/ticks gap fill | `AcquisitionReceipt` | quota/network fail → retry bounded; remain PENDING |
| close reconciliation | data checker | stream raw + historical query + official ref | compare coverage/price/volume clocks | `ProviderParityReceipt` | unexplained diff → TEMP_CLOSED dataset |
| dataset close | Dataset owner | all required receipts | hash/manifest/lineage/publish | `DatasetVersion N+1` | missing rights/schema/parity → no publish |
| after-close research | backtest worker | closed DatasetVersion only | PIT/OOS/WF/cost backtest | BacktestReceipt candidate | never promotes live/financial truth |
| independent eval | independent checker | candidate receipts | counter-evidence/model risk | ValidationReceipt | self-checker/insufficient evidence → REJECT/TEMP_CLOSED |
| XQ parity window | XQ adapter | fixed DatasetVersion/case | XScript/backtest/visual parity | XQParityReceipt | NOT_RUN or discrepancy → no parity claim |
| Shioaji SIM | broker adapter | valid RiskAuthorization + H2 scope | simulation only | broker/sim receipt | unknown side effect → HOLD+QUERY-before-retry |
| provider outage | SRE | telemetry | stop fresh lane, preserve evidence | IncidentRecord | **never fail-open to stale live input** |

### 4.7 Degrade Matrix

| Condition | State | Allowed | Forbidden | Recovery evidence |
|---|---|---|---|---|
| Shioaji historical unavailable | `DEGRADED_HIST` | research on prior accepted DatasetVersion | publish new DatasetVersion | successful gap-fill + quality receipt |
| Shioaji realtime unavailable | `HOLD_REALTIME` | offline research / official rule refresh | new intraday decisions requiring fresh ticks | reconnect + coverage/heartbeat receipt |
| Shioaji quota near cap | `THROTTLED` | slow after-market backfill, resume cursor | bypass rate limit / mass retry | usage receipt + next window |
| Official rule source stale | `RULE_UNKNOWN` | research-only | trade eligibility assertion | fresh official snapshot |
| FinMind unavailable/not subscribed | `NO_ACCELERATOR` | Shioaji-first lane | assume FinMind data exists | none; FinMind not MVP dependency |
| provider parity mismatch | `QUARANTINE_DATASET` | inspect raw and receipts | backtest promotion | explained-difference decision or repaired dataset |
| rights/license unknown | `RIGHTS_BLOCKED` | metadata inspection only | retain/use restricted payload beyond allowed scope | RightsReceipt |
| XQ parity NOT_RUN | `XQ_UNVERIFIED` | internal backtest | XQ equivalence claim | deterministic XQ parity receipt |
| broker side effect UNKNOWN | `HOLD_QUERY` | query broker state | blind retry | correlated BrokerAck/OrderState reconciliation |
| RepoContext missing | `BLOCKED_EXTERNAL` | local blueprint/code templates | repo patch/merge/deploy | RepoContext + TaskSpec |

---
## 5. Directly Implementable Reference Layout（PLANNED / UNBOUND UNTIL RepoContext）

> 以下路徑是 **reference construction landing**；因本輪沒有 real RepoContext，不宣稱這些檔案已存在或已套用。真正 repo write 前依 `AGENTS.md/GRP-04` 建 TaskSpec、allowed_paths、commands、oracles。

```text
data_plane/
├─ config/
│  ├─ provider_profile.yaml
│  ├─ data_policy.yaml
│  ├─ source_matrix.yaml
│  └─ universe_profile.yaml
├─ src/twdata/
│  ├─ shioaji_client.py
│  ├─ backfill_kbars.py
│  ├─ stream_quotes.py
│  ├─ official_reference.py
│  ├─ normalize.py
│  ├─ quality.py
│  ├─ reconcile.py
│  └─ dataset_publish.py
├─ schemas/
│  ├─ minute_bar.schema.json
│  ├─ acquisition_receipt.schema.json
│  ├─ dataset_manifest.schema.json
│  └─ provider_parity.schema.json
├─ tests/
│  ├─ test_kbar_chunk_30d.py
│  ├─ test_no_live_permission.py
│  ├─ test_minute_invariants.py
│  ├─ test_gap_detection.py
│  ├─ test_dataset_immutable.py
│  ├─ test_provider_parity.py
│  └─ test_pit_no_lookahead.py
└─ data/
   ├─ raw/{provider}/{trade_date}/
   ├─ core/minute/venue=.../symbol=.../year=.../month=.../
   ├─ core/daily/
   ├─ derived/
   └─ metadata/catalog.sqlite
```

### 5.1 `provider_profile.yaml`

```yaml
version: 1
mode: fail_closed

shioaji:
  historical:
    state: ADMISSION_PENDING
    auth_profile: SJ_DATA_READ
    permissions_required: [Market_Data]
    production_environment: false
    trading_permission: false
    account_permission: false
    allowed_ip_required: true
    max_kbar_window_days: 30
    realtime_polling: forbidden
  realtime:
    state: ADMISSION_PENDING
    auth_profile: SJ_DATA_READ
    quote_types: [tick, bid_ask]
  simulation:
    state: ADMISSION_PENDING
    auth_profile: SJ_SIM_EXEC
    production_environment: false
    trading_permission: true
  live:
    state: BLOCKED
    auth_profile: null

finmind:
  state: CONDITIONAL_NOT_REQUIRED
  activation_gate: FINMIND_ACTIVATION_DECISION
  exact_plan_price: UNVERIFIED
  dataset_rights: UNVERIFIED

official_reference:
  TWSE: {state: REQUIRED_REFERENCE}
  TPEx: {state: REQUIRED_REFERENCE}

xq:
  role: PARITY_AND_HITL_SURFACE
  runtime_parity: NOT_RUN
```

### 5.2 `data_policy.yaml`

```yaml
version: 1
retention:
  daily:
    initial_years: 5
    authority: PATCH_DEFAULT
  minute_1m:
    upstream_baseline_months: 12
    initial_target_months: 24
    authority: PATCH_CANDIDATE
  tick:
    initial_months: 6
    max_without_CR_months: 12
    universe: MICROSTRUCTURE_SUBSET
  bidask:
    mode: FORWARD_CAPTURE_PLUS_CASES
  full_order_event_book:
    mode: DEFER

timeframes:
  canonical_download: [1m]
  derived_resample: [3m, 5m, 15m, 30m]

publish_requirements:
  - source_identity
  - rights_receipt
  - schema_pass
  - monotonic_clock_pass
  - gap_report
  - duplicate_report
  - checksum
  - lineage
  - parity_disposition
```

### 5.3 Python environment — use existing tools, not a custom package manager

```bash
# PLANNED: run only inside a real RepoContext
uv init
uv add shioaji==1.5.1 polars pyarrow duckdb pydantic pyyaml httpx
uv lock
uv sync --locked
```

- `shioaji==1.5.1` 是本輪 web probe 所見 current stable candidate；**implementation day 必須重新 official-probe + pin + lock**，不能把這行當永久 pin。
- `uv.lock` 必須 commit；CI 用 locked sync；dependency update 走 CR/PR + regression。

### 5.4 `backfill_kbars.py` — quota-aware 30-day-chunk reference

```python
from __future__ import annotations

import hashlib
import json
import os
import time
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import polars as pl
import shioaji as sj

RAW = Path(os.environ.get("TW_DATA_ROOT", "data")) / "raw" / "shioaji_kbars"
RAW.mkdir(parents=True, exist_ok=True)


def windows(start: date, end: date):
    """Shioaji Kbars range must be <= 30 days. Use 29-day span defensively."""
    cur = start
    while cur <= end:
        stop = min(cur + timedelta(days=29), end)
        yield cur, stop
        cur = stop + timedelta(days=1)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def login_data_only() -> sj.Shioaji:
    key = os.environ["SJ_API_KEY"]
    secret = os.environ["SJ_SEC_KEY"]
    api = sj.Shioaji(simulation=True)
    api.login(api_key=key, secret_key=secret)
    # SECURITY CONTRACT: this key must be created with Market/Data only;
    # Trading/Account/Production must be OFF at the provider side.
    return api


def fetch_symbol(api: sj.Shioaji, code: str, start: date, end: date) -> list[dict]:
    receipts = []
    contract = api.Contracts.Stocks[code]
    for a, b in windows(start, end):
        target = RAW / f"symbol={code}" / f"start={a.isoformat()}_end={b.isoformat()}.parquet"
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists():
            receipts.append({"status": "SKIP_EXISTS", "path": str(target), "sha256": sha256_file(target)})
            continue

        # Read-only request: bounded retry is allowed; never blind-retry broker writes.
        last_error = None
        for attempt in range(3):
            try:
                kb = api.kbars(contract=contract, start=a.isoformat(), end=b.isoformat())
                df = (
                    pl.DataFrame(kb.dict())
                    .with_columns(
                        pl.col("ts").cast(pl.Datetime("ns")).alias("event_time"),
                        pl.lit(code).alias("symbol"),
                        pl.lit("SHIOAJI").alias("provider"),
                        pl.lit(datetime.now(timezone.utc).isoformat()).alias("retrieved_at"),
                    )
                    .select([
                        "symbol", "event_time", "Open", "High", "Low", "Close",
                        "Volume", "Amount", "provider", "retrieved_at"
                    ])
                )
                if df.is_empty():
                    raise RuntimeError("EMPTY_KBAR_RESULT")
                tmp = target.with_suffix(".tmp.parquet")
                df.write_parquet(tmp, compression="zstd")
                tmp.replace(target)
                receipts.append({
                    "status": "FETCHED", "symbol": code,
                    "start": a.isoformat(), "end": b.isoformat(),
                    "rows": df.height, "path": str(target), "sha256": sha256_file(target),
                })
                break
            except Exception as exc:
                last_error = repr(exc)
                if attempt == 2:
                    raise
                time.sleep(2 ** attempt)
        time.sleep(0.30)  # conservative request pacing; actual rate telemetry still governs
    return receipts


if __name__ == "__main__":
    # Universe is a bounded, already-approved research list; never auto-expand to bypass quota.
    symbols = [s for s in os.environ.get("TW_SYMBOLS", "2330,2317").split(",") if s]
    start = date.fromisoformat(os.environ["TW_START"])
    end = date.fromisoformat(os.environ["TW_END"])
    api = login_data_only()
    all_receipts = []
    try:
        for symbol in symbols:
            all_receipts.extend(fetch_symbol(api, symbol, start, end))
        Path("data/metadata").mkdir(parents=True, exist_ok=True)
        Path("data/metadata/backfill_receipt.json").write_text(
            json.dumps(all_receipts, ensure_ascii=False, indent=2), encoding="utf-8"
        )
    finally:
        api.logout()
```

**Acceptance boundary：** 這段是 reference implementation；沒有 account entitlement / current SDK run receipt 前不得標 `WORKS_IN_TARGET_ENV`。

### 5.5 `stream_quotes.py` — data-only realtime capture

```python
import json
import os
from datetime import datetime, timezone
from pathlib import Path

import shioaji as sj

OUT = Path(os.environ.get("TW_DATA_ROOT", "data")) / "raw" / "shioaji_stream"
OUT.mkdir(parents=True, exist_ok=True)

api = sj.Shioaji(simulation=True)
api.login(api_key=os.environ["SJ_API_KEY"], secret_key=os.environ["SJ_SEC_KEY"])

@api.quote.on_quote
def on_quote(topic: str, quote: dict):
    # append-only raw evidence; normalization happens downstream
    day = datetime.now(timezone.utc).date().isoformat()
    path = OUT / f"date={day}.jsonl"
    record = {
        "observed_at": datetime.now(timezone.utc).isoformat(),
        "topic": topic,
        "payload": quote,
        "provider": "SHIOAJI",
    }
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, ensure_ascii=False, default=str) + "\n")

symbols = [s for s in os.environ.get("TW_SYMBOLS", "2330,2317").split(",") if s]
for code in symbols:
    contract = api.Contracts.Stocks[code]
    api.quote.subscribe(contract, quote_type=sj.constant.QuoteType.Tick)
    api.quote.subscribe(contract, quote_type=sj.constant.QuoteType.BidAsk)

# Production service should replace input() with a supervised process/service lifecycle.
input("streaming; press Enter to stop\n")
api.logout()
```

**Security invariant：** `SJ_DATA_READ` key 只能 Market/Data，Trading/Account/Production 全關；即使程式碼被 prompt/tool injection 影響，也不能靠同一 credential 下單。

### 5.6 Official reference config（endpoint identity only; schema must be probed）

```yaml
sources:
  TWSE:
    base: https://openapi.twse.com.tw/v1
    required_domains:
      - stock_daily_reference
      - day_trade_eligibility
      - day_trade_suspension
      - trading_halt
      - price_limit_or_market_rule
      - calendar
  TPEX:
    base: https://www.tpex.org.tw/openapi/v1
    required_domains:
      - otc_daily_reference
      - day_trade_eligibility
      - day_trade_suspension
      - disposition_attention
      - calendar_or_market_rule
```

**Fail-closed：** 不在 blueprint 裡硬猜 endpoint path/schema；installation/pilot 時從 OpenAPI spec 解析 exact operation + response schema，將 operation-id/hash 寫入 `SourceProfile`。

### 5.7 Dataset publish contract

```json
{
  "dataset_id": "TW_INTRADAY_1M",
  "dataset_version": "YYYYMMDDTHHMMSSZ+sha256",
  "status": "PENDING|ACCEPTED|QUARANTINED",
  "source_profiles": [],
  "raw_hashes": [],
  "schema_hash": "",
  "event_time_min": "",
  "event_time_max": "",
  "known_at_policy": "",
  "rights_receipts": [],
  "gap_report": "",
  "duplicate_report": "",
  "provider_parity_receipt": "",
  "parent_version": "",
  "created_at": "",
  "claim_ceiling": "RESEARCH_DATASET_ONLY"
}
```

### 5.8 Windows scheduling — no orchestration platform for MVP

```powershell
# PLANNED only. Resolve actual repo path/account before execution.
$python = "C:\path\to\repo\.venv\Scripts\python.exe"
$repo   = "C:\path\to\repo"

schtasks /Create /TN "SQS-TW-Official-PreOpen" /SC DAILY /ST 08:20 `
  /TR "cmd /c cd /d $repo && $python -m twdata.official_reference" /F

schtasks /Create /TN "SQS-TW-PostClose-Reconcile" /SC DAILY /ST 15:45 `
  /TR "cmd /c cd /d $repo && $python -m twdata.reconcile" /F
```

**Calendar gate：** worker 啟動後必須先讀 official trading calendar；週末/休市日直接 `SKIP_WITH_RECEIPT`。Task Scheduler 只給「時間觸發」，不擁有交易日 truth。

---
## 6. Permission / Secret / Side-effect Design

### 6.1 Three Shioaji profiles — mandatory separation

| Profile | Provider permissions | Local secret scope | Allowed | Forbidden |
|---|---|---|---|---|
| `SJ_DATA_READ` | Market/Data=ON; Account=OFF; Trading=OFF; Production=OFF; account/IP/expiry scoped | data worker only | historical + realtime quotes | account, order, production |
| `SJ_SIM_EXEC` | Market/Data=ON; Trading=ON; Production=OFF; simulation test signed | simulation adapter only | simulation place/update/cancel + receipts | live production |
| `SJ_LIVE_EXEC` | **NOT ISSUED / BLOCKED** | none | none | all live orders |

這個分割同時由 project `LeastPrivilege / ExternalWriteFence / H2 token` 與 Shioaji current API-key capability支持。即使 Shioaji 技術上可用一把 production key做更多事，本藍圖禁止以便利性合併 privilege。

### 6.2 Secret handling

- `.env` 只作 provider-documented local loading interface；**不得 commit**。
- repo 只保存 `.env.example`，不放 real key/secret/CA password。
- data worker 不持有 CA；simulation/live adapter 與 data worker 分 process / identity。
- log/evidence 永遠 redact credential、person id、account id；provider raw payload 若含敏感欄位先分類再寫。
- production CA/key 要等 `TT-BROKER-PROVIDER-ADMISSION + Human approval + H2 action token + Paper/Shadow` 全閉合。

### 6.3 Side-effect fencing

```text
DATA_READ       → read-only, bounded retry allowed
SIMULATION      → side-effect-like; idempotency + receipt + query-before-retry
LIVE_EXTERNAL   → DENY/BLOCKED
UNKNOWN_RESULT  → HOLD + QUERY, never blind retry
```

---
## 7. Implementation Plan & Change List

### 7.1 Minimal-change principle

**保留不改：**
- `PKG-L1-07/08/09` PIT/Data/Five Clocks/Research Store。
- `PKG-L1-17` provider admission lifecycle。
- `PKG-L1-25` backtest/PIT/OOS/WF/cost/model-risk。
- `PKG-L1-29` XQ/XS parity/HITL surface。
- `PKG-L1-30/31` OMS/EMS/external-write/BoR/reconciliation。
- `DuckDB / Parquet / SQLite` local-first data architecture。

**只補：** named provider binding、runtime data profile、retention policy、quota-aware acquisition、rights/parity receipts、Windows worker recipes。

### 7.2 Proposed change plan

| Proposed path | Change | Purpose | Risk | State |
|---|---|---|---|---|
| `registries/TOOL_REGISTRY.md` | PATCH named slots | Shioaji primary candidate / FinMind conditional / TWSE-TPEx official ref | actual sidecar content not mounted | PLANNED / CR_OPEN |
| `install/WINDOWS_EXECUTABLE_RECIPES.md` | PATCH | uv/Shioaji worker + Task Scheduler recipes | RepoContext missing | PLANNED / CR_OPEN |
| `docs/PKG-DOC-04...` or corresponding data sidecar | PATCH | data retention/acquisition profiles | no duplicate owner | PLANNED |
| `docs/PKG-DOC-09...` or broker sidecar | PATCH | `SJ_DATA_READ` vs `SJ_SIM_EXEC` vs live blocked | privilege mixing | PLANNED |
| `registries/CONTROL_REGISTRY_INDEX.md` | LINK ONLY | register new profile/receipt paths | avoid second registry | PLANNED |
| `data_plane/config/*` | ADD | runtime config, no normative truth takeover | drift | PLANNED |
| `data_plane/src/twdata/*` | ADD | deterministic acquisition/reconcile/publish | API drift/quota | PLANNED |
| `data_plane/tests/*` | ADD | first-fail evidence | false PASS if fixtures weak | PLANNED |

### 7.3 Implementation waves

#### Wave 0 — Design/identity closure
1. Resolve real RepoContext.
2. Read actual `TOOL_REGISTRY.md` and `WINDOWS_EXECUTABLE_RECIPES.md`; diff against this patch.
3. Create TaskSpec with allowed paths, commands, tests, oracles, rollback.
4. Official-probe Shioaji version/docs and pin immutable package version in `uv.lock`.
5. Create `SJ_DATA_READ` key with Market/Data only + allowed IP + expiry; **no Trading/Production**.

**Gate W0 PASS:** exact provider identity/pin, permission screenshot/readback or provider API management receipt, source/rights profile, no live key.  
**FAIL:** missing account/permission/rights => `TT-BROKER-PROVIDER-ADMISSION` remains open.

#### Wave 1 — 20–50 symbol empirical backfill pilot
- 30-day chunks; 12 months first, then 24 only after data SLO/space/throughput evidence.
- Capture `api.usage()`/quota telemetry where available.
- Measure bytes/symbol/day, rows/symbol/day, request failure, gaps, wall-clock, storage after ZSTD.

**Gate W1 PASS:** ≥99.9% expected minute coverage on selected trading sessions **or** every gap is explicitly classified; zero duplicate key violations; reproducible hashes; no quota policy violation. Threshold is initial engineering target and must be owner-configurable.

#### Wave 2 — Daily realtime capture
- Subscribe only approved candidate universe.
- Append raw; no model/order side effect.
- After close, query historical gap-fill and reconcile.

**Gate W2 PASS:** stream heartbeat, clock monotonicity, no unexplained gap beyond configured tolerance, close reconciliation produces `DatasetVersion`.

#### Wave 3 — Official rule/universe reference
- TWSE/TPEx operation IDs, schema hashes, rights profile.
- Daily diff and stale-source gate.

**Gate W3 PASS:** effective date + source hash + eligibility state readback.

#### Wave 4 — Backtest/replay
- 1m canonical dataset; derive 3/5/15/30m.
- PIT, IS/OOS, walk-forward, cost/slippage/TCA, negative cases.
- XQ parity on fixed deterministic cases.

**Gate W4 PASS:** internal backtest reproducible; XQ discrepancies are `MATCH` or `EXPLAINED_DIFFERENCE`; no promotion from XQ alone.

#### Wave 5 — Shioaji simulation
- Separate `SJ_SIM_EXEC` key/profile.
- Simulation signing/test prerequisites complete.
- Order idempotency + UNKNOWN query-before-retry + BoR/reconcile fixtures.

**Gate W5 PASS:** simulation receipts and reconciliation only. **Live remains BLOCKED.**

#### Wave 6 — Conditional FinMind decision
Only if trigger metrics prove need. Before purchase: current price, plan entitlement, raw/local retention rights, PIT provenance, source parity, exit plan.

### 7.4 Minimal Regression / Test Tracking List

| Test ID | Fixture / mutation | Expected first failure / PASS oracle |
|---|---|---|
| T-DATA-001 | valid Shioaji 30-day kbar chunk | schema + monotonic time + nonempty + checksum PASS |
| T-DATA-002 | 31+ day requested chunk | local splitter prevents request; no provider call |
| T-DATA-003 | duplicate `(symbol,event_time)` | `DUPLICATE_BAR` before publish |
| T-DATA-004 | High < max(Open,Close) | `OHLC_INVARIANT_FAIL` |
| T-DATA-005 | Low > min(Open,Close) | `OHLC_INVARIANT_FAIL` |
| T-DATA-006 | non-monotonic event_time | `CLOCK_MONOTONICITY_FAIL` |
| T-DATA-007 | missing expected minute | gap report; dataset PENDING/QUARANTINED by policy |
| T-DATA-008 | stale official eligibility | `RULE_UNKNOWN` / no trade eligibility assertion |
| T-DATA-009 | rights receipt missing | `RIGHTS_BLOCKED` |
| T-DATA-010 | provider parity unexplained | `PROVIDER_PARITY_FAIL` |
| T-DATA-011 | same raw input twice | same normalized output hash |
| T-DATA-012 | rerun existing immutable partition | skip/idempotent; no overwrite without supersession |
| T-PIT-001 | future published fundamental | `LOOKAHEAD_FAIL` |
| T-PIT-002 | revised value without revision lineage | `REVISION_LINEAGE_FAIL` |
| T-BT-001 | fixed strategy + fixed DatasetVersion | deterministic result hash |
| T-BT-002 | OOS period leaks training | `OOS_CONTAMINATION_FAIL` |
| T-BT-003 | cost/slippage omitted | `COST_MODEL_REQUIRED` |
| T-BT-004 | XQ PASS but internal PIT FAIL | overall FAIL; no cross-surface inheritance |
| T-SJ-001 | data key has Trading permission | `LEAST_PRIVILEGE_FAIL` |
| T-SJ-002 | data key has Production enabled | `PRODUCTION_PERMISSION_FAIL` |
| T-SJ-003 | realtime code calls historical polling loop | static/runtime policy FAIL |
| T-SJ-004 | quota near cap | controlled throttle + cursor; no blind retry |
| T-SJ-005 | >subscription capability | explicit NACK / reduce candidate scope with owner decision |
| T-SIM-001 | simulation order duplicate request | idempotency prevents duplicate side effect |
| T-SIM-002 | order response unknown | HOLD+QUERY, no retry until state known |
| T-SIM-003 | live production flag true | FAIL before login/start in MVP profile |
| T-SEC-001 | secret appears in git diff/log | FAIL + revoke/rotate |
| T-SEC-002 | dependency action unpinned | CI FAIL |
| T-REC-001 | publish without parent/source hashes | FAIL |
| T-REC-002 | archived checksum self-includes manifest | FAIL / regenerate |
| T-DEG-001 | Shioaji outage | research-only fallback; realtime HOLD |
| T-DEG-002 | FinMind unavailable | no impact to MVP primary lane |

### 7.5 Required Gates

```text
G0_SOURCE_BINDING
 → G1_PROVIDER_IDENTITY_PIN_LICENSE
 → G2_PERMISSION_LEAST_PRIVILEGE
 → G3_HISTORICAL_PILOT
 → G4_DATA_QUALITY_PIT
 → G5_OFFICIAL_RULE_REFERENCE
 → G6_PROVIDER_PARITY
 → G7_BACKTEST_OOS_COST
 → G8_XQ_PARITY
 → G9_SHIOAJI_SIMULATION
 → [STOP: LIVE BLOCKED]
```

No gate may inherit PASS from another surface.

---
## 8. Risk Register & CR_OPEN

| ID | Risk / Missing evidence | Severity | Current state | Blocked claim/action | Closure condition | Degrade |
|---|---|---:|---|---|---|---|
| CR-001 | actual `TOOL_REGISTRY.md` body not mounted | HIGH | MISSING | final named-provider pack patch claim | direct full read + diff | keep this blueprint as proposed patch only |
| CR-002 | actual `WINDOWS_EXECUTABLE_RECIPES.md` body not mounted | HIGH | MISSING | executable repo recipe claim | direct read + TaskSpec | reference commands only |
| CR-003 | RepoContext absent | HIGH | MISSING | repo mutation / CI / deploy | RepoContext + AGENTS + TaskSpec | BLOCKED_EXTERNAL |
| CR-004 | Shioaji account/API entitlement not inspected | CRITICAL | UNVERIFIED | provider admission | account + API key scope receipt | ADMISSION_PENDING |
| CR-005 | Shioaji data retention/use rights for intended local cache not fully adjudicated | CRITICAL | UNVERIFIED | long-term local retention | official terms/account agreement + RightsReceipt | pilot only within verified scope |
| CR-006 | Shioaji actual bandwidth tier unknown | HIGH | UNVERIFIED | 24m backfill schedule | `api.usage`/account tier + pilot telemetry | bounded backfill |
| CR-007 | actual bytes/symbol/day & storage not measured | MEDIUM | NOT_RUN | capacity forecast | 20–50 symbol pilot | 12m first, expand only if pass |
| CR-008 | current exact Shioaji recurring API/data price not independently published in docs reviewed | MEDIUM | UNVERIFIED | `NT$0` budget promise | official/account fee receipt | budget as TT, do not assert zero |
| CR-009 | FinMind exact 2026 Sponsor/SponsorPro price | MEDIUM | UNVERIFIED | purchase forecast | current checkout/official price receipt | not required for MVP |
| CR-010 | FinMind exact dataset entitlement/local retention rights | HIGH | UNVERIFIED | accelerator admission | plan+dataset rights receipt | NOT_REQUIRED |
| CR-011 | TWSE/TPEx per-dataset rights/attribution | HIGH | PARTIAL | local official snapshot publication | dataset-specific license record | reference-only until bound |
| CR-012 | `TT-DATA-PROVIDER-PARITY` | CRITICAL | OPEN | canonical provider parity | deterministic fixtures + discrepancy dispositions | QUARANTINE affected dataset |
| CR-013 | `TT-BROKER-PROVIDER-ADMISSION` | CRITICAL | OPEN | broker/sim provider claim | identity/pin/license/security/sim/pilot | external writes OFF |
| CR-014 | `TT-EXECUTION-PROVIDER / TT-RECONCILIATION-RUNTIME` | CRITICAL | OPEN | broker facts/BoR runtime | simulation and independent reconcile evidence | NO LIVE |
| CR-015 | `TT-XQ-PARITY / TT-XQ-RUNTIME` | HIGH | OPEN | XQ equivalence | fixed cases + compile/backtest/visual receipts | internal only |
| CR-016 | Independent NRTV / Paper / Shadow | CRITICAL | NOT_RUN | release/live | separate independent receipts | Live BLOCKED |
| CR-017 | 24-month minute target is patch default, not immutable upstream rule | MEDIUM | DESIGN_DECISION | hard normative retention claim | empirical OOS/regime/cost decision | allow 12m baseline if sufficient |
| CR-018 | top-5 BidAsk ≠ full historical order-event book | HIGH | KNOWN_BOUNDARY | order-book replay claim | licensed full order-event source | classify replay tier honestly |
| CR-019 | FinMind current price/plan may drift | MEDIUM | DRIFT | cost forecast | activation-time web/checkout probe | no subscription dependency |
| CR-020 | Shioaji SDK/API may drift | HIGH | DRIFT | code compatibility | implementation-day official probe + locked env + fixtures | pin last admitted version |

### 8.1 Cost Adjudication

| Lane | Current cost evidence | Blueprint budget treatment |
|---|---|---|
| TWSE/TPEx OpenAPI/reference | public official interfaces; per-dataset rights still bind | `LOW/OPEN_DATA` but no universal zero-cost/rights claim |
| Shioaji | account required; docs reviewed do not provide a separate current historical-data subscription price table | `CR-008`; **do not promise NT$0** |
| FinMind | entitlements confirmed, exact current checkout price not verified | `CR-009`; no MVP budget until activation trigger |
| TWSE Data E-Shop | current listed historical product prices exist | defer; only future microstructure CR |
| Local storage | depends on pilot bytes | `CR-007`; no guessed TB forecast |

**Correction to earlier discussion:**「Shioaji data subscription ≈ NT$0」只能視為未證實的 planning assumption，不能成為本藍圖的 NORMATIVE cost claim；現版改為 `PRICE_UNVERIFIED`。

---
## 9. Machine-Readable Blocks

### 9.1 `machine_summary.json`

```json
{
  "blueprint_id": "TW_DATA_SHIOAJI_FIRST_2026_08_11_R1",
  "date": "2026-08-11",
  "task_kind": ["DESIGN", "EVAL", "SEARCH_ONLY", "DRIFT_PROBE"],
  "final_verdict": "FAIL_CLOSED_RUNTIME_PROVIDER_RELEASE",
  "design_status": "CONSTRUCTION_READY_WITH_CR_OPEN",
  "claim_ceiling": "AUTHOR_SIDE_DESIGN_ONLY",
  "architecture": {
    "official_reference": ["TWSE", "TPEx"],
    "primary_intraday_provider_candidate": "Shioaji",
    "research_accelerator_candidate": "FinMind",
    "accelerator_state": "CONDITIONAL_NOT_REQUIRED",
    "xq_role": "PARITY_HITL_SURFACE",
    "storage": ["Parquet", "DuckDB", "SQLite"]
  },
  "data_policy": {
    "daily": {"initial_years": "2-5", "authority": "PATCH_DEFAULT"},
    "minute_1m": {"upstream_baseline_months": 12, "initial_target_months": "18-24", "authority": "PATCH_CANDIDATE"},
    "derived_timeframes": ["3m", "5m", "15m", "30m"],
    "tick": {"initial_months": "3-12", "universe": "BOUNDED_MICROSTRUCTURE_SUBSET"},
    "bidask": "FORWARD_PLUS_CASE_WINDOWS",
    "full_order_event_book": "DEFER"
  },
  "permissions": {
    "SJ_DATA_READ": {"market_data": true, "account": false, "trading": false, "production": false},
    "SJ_SIM_EXEC": {"market_data": true, "trading": true, "production": false},
    "SJ_LIVE_EXEC": "BLOCKED_NOT_ISSUED"
  },
  "required_gates": [
    "G0_SOURCE_BINDING",
    "G1_PROVIDER_IDENTITY_PIN_LICENSE",
    "G2_PERMISSION_LEAST_PRIVILEGE",
    "G3_HISTORICAL_PILOT",
    "G4_DATA_QUALITY_PIT",
    "G5_OFFICIAL_RULE_REFERENCE",
    "G6_PROVIDER_PARITY",
    "G7_BACKTEST_OOS_COST",
    "G8_XQ_PARITY",
    "G9_SHIOAJI_SIMULATION"
  ],
  "hard_blocks": [
    "REPOCONTEXT_MISSING",
    "SHIOAJI_ENTITLEMENT_UNVERIFIED",
    "DATA_RIGHTS_UNVERIFIED",
    "PROVIDER_PARITY_NOT_RUN",
    "BROKER_PROVIDER_ADMISSION_NOT_RUN",
    "XQ_PARITY_NOT_RUN",
    "INDEPENDENT_NRTV_NOT_RUN",
    "PAPER_SHADOW_NOT_RUN",
    "LIVE_BLOCKED"
  ],
  "finmind_activation_triggers": [
    "SHIOAJI_BACKFILL_SLO_FAILS",
    "FULL_MARKET_INTRADAY_BULK_REQUIRED",
    "BROAD_RESEARCH_DATASET_REQUIRED",
    "SECOND_PROVIDER_PARITY_REQUIRED"
  ]
}
```

### 9.2 `change_plan.tsv`

```tsv
path\tchange_type\treason\tauthority\tstate\trisk
registries/TOOL_REGISTRY.md\tPATCH\tMaterialize Shioaji primary candidate + FinMind conditional accelerator + TWSE/TPEx official reference\tPKG-L1-17\tPLANNED_CR_OPEN\tCurrent sidecar body not mounted
install/WINDOWS_EXECUTABLE_RECIPES.md\tPATCH\tAdd uv/Shioaji/Task Scheduler bounded recipes\tPKG-L1-18\tPLANNED_CR_OPEN\tRepoContext missing
docs/PKG-DOC-04_or_bound_data_sidecar\tPATCH\tBind retention/acquisition/PIT profile without changing Data owner\tPKG-L1-07/08/09\tPLANNED\tOwner flattening if duplicated
docs/PKG-DOC-09_or_bound_execution_sidecar\tPATCH\tSeparate SJ_DATA_READ/SJ_SIM_EXEC/live blocked\tPKG-L1-30/31\tPLANNED\tPrivilege escalation
data_plane/config/provider_profile.yaml\tADD\tProvider states/permissions/triggers\tTaskSpec\tPLANNED\tDrift
data_plane/config/data_policy.yaml\tADD\tRetention/timeframe policy\tTaskSpec\tPLANNED\tHard-coded policy misuse
data_plane/src/twdata/backfill_kbars.py\tADD\t30-day-chunk historical acquisition\tTaskSpec\tPLANNED\tQuota/API drift
data_plane/src/twdata/stream_quotes.py\tADD\tRealtime read-only tick/BidAsk capture\tTaskSpec\tPLANNED\tSecret/network
data_plane/src/twdata/official_reference.py\tADD\tTWSE/TPEx source snapshots\tTaskSpec\tPLANNED\tSchema/rule drift
data_plane/src/twdata/reconcile.py\tADD\tStream-vs-history/provider parity\tTaskSpec\tPLANNED\tFalse reconciliation
data_plane/src/twdata/dataset_publish.py\tADD\tDatasetVersion immutable publish\tTaskSpec\tPLANNED\tPartial publish
data_plane/tests/*\tADD\tFirst-fail regression fixtures\tGRP-06\tPLANNED\tWeak oracle
```

### 9.3 `checkrun_contract.tsv`

```tsv
required_check\towner\tinput\toracle\tevidence\ton_fail\tdegrade
SOURCE_BINDING\tSourceAuthorityOwner\tsubject/version/hash/source_locator\texact anchor resolves\tSourceAuthorityRecord\tTEMP_CLOSED\tNo normative use
PROVIDER_IDENTITY_PIN\tToolProviderQualificationOwner\tprovider identity/version\timmutable identity + pin\tPinLock\tADMISSION_DENIED\tUse no-provider fallback
DATA_RIGHTS\tRightsPrivacyOwner\tdataset/source/use\tlicense scope permits intended use\tRightsReceipt\tRIGHTS_BLOCKED\tMetadata only
SJ_LEAST_PRIVILEGE\tSecurityOwner\tAPI key profile\tData key has no Trading/Account/Production\tPermissionReceipt\tDENY\tNo Shioaji runtime
HISTORICAL_PILOT\tDataOwner\t20-50 symbols/12m\tcoverage/hash/quota SLO\tPilotReceipt\tTEMP_CLOSED\tReduce/pace scope, never bypass
DATA_QUALITY_PIT\tDataOwner+IndependentChecker\traw+calendar+clocks\tno gap/dup/lookahead invariant violation\tDataQualityReceipt\tQUARANTINE_DATASET\tPrior accepted dataset research-only
OFFICIAL_RULE_REFERENCE\tTaiwanRuleOwner\tTWSE/TPEx snapshot\teffective-date/source hash valid\tRuleReceipt\tRULE_UNKNOWN\tNO_TRADE affected scope
PROVIDER_PARITY\tIndependentChecker\tShioaji/offical/optional FinMind case\tMATCH or EXPLAINED_DIFFERENCE\tParityReceipt\tTEMP_CLOSED\tNo provider equivalence claim
BACKTEST_OOS_COST\tIndependentQuantValidator\tDatasetVersion+strategy\tPIT/OOS/WF/cost/capacity pass\tValidationReceipt\tREJECT\tNo paper promotion
XQ_PARITY\tXQAdapter+IndependentChecker\tfixed case\tcompile/backtest/visual discrepancy explained\tXQParityReceipt\tXQ_UNVERIFIED\tInternal only
SHIOAJI_SIMULATION\tExecutionAdapterOwner\tRiskAuthorization+sim profile\tidempotency/ACK/UNKNOWN/reconcile pass\tSimulationReceipt\tHOLD\tNo live
RELEASE_CLAIM\tReleaseAuthority\tall required receipts\tno missing/expired/invalidated gate\tReleaseClaimReceipt\tFAIL_CLOSED\tLive BLOCKED
```

---
## 10. Web Source Register（SUPPORT）

| ID | Source | URL | Used for |
|---|---|---|---|
| `WEB-SJ-01` | Shioaji Historical Market Data | https://sinotrade.github.io/tutor/market_data/historical/ | Ticks/Kbars；股票歷史自 2020-03-02；Kbars 單次 start/end 不超過 30 天；歷史 query 用於盤後/回測，不作即時 polling。 |
| `WEB-SJ-02` | Shioaji Use Restrictions | https://sinotrade.github.io/tutor/limit/ | 歷史查詢頻率與每日 bandwidth；即時行情應 subscription；需 cache；違規可能停權。 |
| `WEB-SJ-03` | Shioaji Quick Start | https://sinotrade.github.io/quickstart/ | Python/CLI/HTTP；tick/bid_ask/quote；SSE/HTTP；下單接口與 CA boundary。 |
| `WEB-SJ-04` | Shioaji Token & Certificate | https://sinotrade.github.io/tutor/prepare/token/ | API key 可限制到期、Market/Data、Account、Trading、Production、帳號與 allowed IP；production 下單需 CA。 |
| `WEB-SJ-05` | Shioaji API Signing and Test | https://sinotrade.github.io/tutor/prepare/terms/ | 正式環境前需簽署文件並完成 simulation login/place_order 測試；Trading permission 需顯式開啟。 |
| `WEB-SJ-06` | Shioaji Simulation Mode | https://sinotrade.github.io/tutor/simulation/ | Simulation 支援 market data、orders、positions/P&L；simulation 不等於 production admission。 |
| `WEB-SJ-07` | Shioaji GitHub | https://github.com/Sinotrade/Shioaji | 2026 provider implementation family；Python/HTTP-capable integration、CLI/server/AI coding support，以 official docs 為 capability truth。 |
| `WEB-FM-01` | FinMind Technical Data Docs | https://finmind.github.io/tutor/TaiwanMarket/Technical/ | TaiwanStockPriceTick / TaiwanStockKBar entitlement、歷史範圍與 async 使用；需依當期方案驗證。 |
| `WEB-FM-02` | FinMind WhatIsNew | https://finmind.github.io/WhatIsNew/ | 2026-06 storage_objects 為 SponsorPro 且只自功能上線後累積，不提供更早 historical backfill。 |
| `WEB-FM-03` | FinMind Disclaimer & Data Licensing | https://finmind.github.io/Disclaimer/ | 2026-07-12 資料來源/授權說明；使用權依來源與方案；不可把軟體 Apache-2.0 誤當成資料再散布權。 |
| `WEB-FM-04` | FinMind Terms of Use | https://finmind.github.io/en/PrivacyPolicy/ | 方案資料授權依 sponsor/Disclaimer；禁止 public realtime raw redistribution/mirror service 等。 |
| `WEB-FM-05` | FinMind GitHub Releases | https://github.com/FinMind/FinMind/releases | 2026 release/drift 支援；版本需在 admission 時重新 pin。 |
| `WEB-TWSE-01` | TWSE OpenAPI | https://openapi.twse.com.tw/ | 上市官方 reference；daily、當沖資格、暫停、5秒統計、除權息、margin、交易日等資料入口。 |
| `WEB-TPEX-01` | TPEx OpenAPI | https://www.tpex.org.tw/openapi/ | 上櫃官方 reference；daily、當沖資格/暫停、margin、除權息、處置等資料入口。 |
| `WEB-ODL-01` | Taiwan Open Government Data License 1.0 | https://data.gov.tw/license | 若特定 dataset 採 ODL 1.0，可在授權條件與 attribution 下使用；仍需逐 dataset 綁 rights。 |
| `WEB-TWSE-ESHOP-01` | TWSE Data E-Shop Historical Products | https://eshop.twse.com.tw/zh/category/main/7 | 高粒度歷史檔屬付費/授權產品；MVP 不預設採購。 |
| `WEB-DUCK-01` | DuckDB Parquet | https://duckdb.org/docs/stable/data/parquet/overview | Parquet 原生讀寫、projection/filter pushdown；適合 local analytical store。 |
| `WEB-DUCK-02` | DuckDB Hive Partitioning | https://duckdb.org/docs/stable/data/partitioning/hive_partitioning | Hive-style partition 讀取與 partition pruning；避免自造 metadata query engine。 |
| `WEB-UV-01` | uv Project / Locking Docs | https://docs.astral.sh/uv/concepts/projects/sync/ | uv.lock + sync/locked；用現成 lock/sync 取代自製 dependency manager。 |
| `WEB-GH-01` | GitHub Actions Secure Use | https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions | 第三方 actions 應 pin full-length commit SHA、最小權限。 |
| `WEB-OSSF-01` | OpenSSF Scorecard Checks | https://github.com/ossf/scorecard/blob/main/docs/checks.md | Dangerous-Workflow、Pinned-Dependencies、Token-Permissions 等 SUPPORT checks；不等於產品 semantic/runtime PASS。 |
| `WEB-MS-01` | Microsoft schtasks /create | https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/schtasks-create | Windows 本機排程可用 schtasks 建立 deterministic worker schedule；MVP 不需 Airflow/Dagster。 |
| `WEB-RES-01` | 2026 Open-source financial data PIT leakage audit | https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7041280 | SUPPORT：聚合資料若未保留 point-in-time chronology 可能產生 forward-information leakage。 |
| `WEB-RES-02` | 2026 Taiwan-equity PIT engine research | https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7016199 | SUPPORT：Taiwan equity PIT/announcement-time chronology、可驗證 temporal causality。 |
| `WEB-RES-03` | 2026 walk-forward/embargo leakage diagnostic | https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7029819 | SUPPORT：walk-forward、embargo、decision-time leakage 控制；不作策略獲利規範。 |


### 10.1 Source-quality rule

- Shioaji capability/limits/security：以 Sinotrade official docs + official GitHub 交叉。
- FinMind capability/entitlement/rights：以 FinMind docs + WhatIsNew + Disclaimer/Terms + GitHub release 交叉。
- Market rules/reference：以 TWSE/TPEx official source為主；第三方文章不作規範。
- Software supply-chain：GitHub/OpenSSF 僅 SUPPORT；Final Pack 本身已把 OpenSSF/SLSA/SBOM 放在 support/provenance lane，不得以 Scorecard PASS 取代 domain/provider/evidence PASS。
- Research papers 只用來 challenge PIT/leakage/validation，不用來設定交易績效 threshold。

---

## 11. Final Adjudication

### 11.1 What is closed at design level

- 台股歷史資料的 **actual MVP need** 已可收斂：daily context + 1m primary historical + bounded recent Tick/BidAsk + official rules/universe；full warehouse/full order-event history 不是 MVP prerequisite。
- 上游 FinMind/Shioaji plan **存在**；Final current architecture 的缺口是 **named-provider materialization**，不是缺 Data/Provider architecture。
- Provider choice 已有 minimal-change patch：`Shioaji-first + TWSE/TPEx Official Reference + FinMind Conditional Accelerator`。
- Existing `PIT / DatasetVersion / Parquet / DuckDB / SQLite / Backtest / XQ / ProviderAdmission` 保留，不另造 data platform。
- 直接可施工的 reference config/scripts/tests/gates 已給出；但因 RepoContext/provider account 未綁，狀態仍是 `PLANNED`。

### 11.2 Why final status remains FAIL-CLOSED

Critical empirical/evidence gaps 未閉合：

1. Actual `TOOL_REGISTRY.md` / Windows recipe sidecars 尚未 direct-read。
2. Shioaji account entitlement、data rights、bandwidth tier、target-host execution 尚未驗證。
3. 20–50-symbol historical pilot / daily realtime capture / close reconciliation 未執行。
4. `TT-DATA-PROVIDER-PARITY`、`TT-BROKER-PROVIDER-ADMISSION`、`TT-XQ-RUNTIME`、`TT-EXECUTION-PROVIDER` 未關閉。
5. Independent NRTV / Paper / Shadow 未執行；Live 仍 BLOCKED。

因此本藍圖**可以作為下一個施工 TaskSpec 的上位設計**，但不得被標為 `INSTALLED / ADMITTED / RUNTIME_PASS / RELEASE_CANDIDATE / PRODUCTION_PASS`。

### 11.3 Fixed-point recommendation

```text
Read real TOOL_REGISTRY / Windows recipes
→ TaskSpec + allowed paths
→ Create SJ_DATA_READ least-privilege profile
→ 20–50 symbols × 12m Kbar pilot
→ extend to 18–24m only if throughput/OOS needs justify
→ realtime Tick/BidAsk forward capture
→ official TWSE/TPEx daily rule snapshot
→ close DatasetVersion + PIT + quality/parity
→ internal backtest/OOS/cost
→ XQ parity
→ Shioaji simulation
→ STOP (Live remains blocked)
→ FinMind activation only if empirical trigger fires
```

**Final one-line verdict：** `Shioaji-first` 是 current MVP 的合理 **preferred candidate**，不是已驗證 provider；`FinMind` 應保留 capability slot 但不成為付費前置依賴；`TWSE/TPEx` 持續作 official reference authority；所有 runtime/live claim 在 evidence 未閉合前一律 FAIL-CLOSED。

---
## Appendix A — Physical Markdown Inventory (138 files)

> 這是本輪 `/mnt/data/*.md` 的 direct physical denominator。Role 是本藍圖的讀取分類，不改寫各文件內部 authority。

| # | File | Role | Bytes | Lines | SHA-256 | Relevant-keyword flags |
|---:|---|---|---:|---:|---|---|
| 1 | `AGENTS.md` | CONTROL_NORMATIVE | 12,880 | 219 | `2ea19f21e0f590b016ded6ea392ea2fa314a0fe6e0aa372b81f7ac1b72253a66` | - |
| 2 | `AUDIT_SQS-THC_TW-ICT_FSDT-Stack_實作RBWI_WP_控制工件_PACK_草案_v2026.08.09-draft-r1_實質草案級骨架全量審查報告_2026-08-09_r1.md` | AUDIT_SUPPORT | 74,445 | 970 | `d604af8d336e8ce45e6ddda0b2c71cdad5ac7ef08aa60efdb92db157513f311f` | 回測,tick,DatasetVersion,PIT,DuckDB,Parquet,XQ |
| 3 | `DEPLOYMENT_PROMPT(1).md` | CONTROL_NORMATIVE | 8,188 | 138 | `cee60cdf51f5c25b952a879a6e429b6fc0a087d652e8b6778bf75146b57770c5` | - |
| 4 | `DEPLOYMENT_PROMPT.md` | CONTROL_NORMATIVE | 8,188 | 138 | `cee60cdf51f5c25b952a879a6e429b6fc0a087d652e8b6778bf75146b57770c5` | - |
| 5 | `G01_Authority_Product_Financial_Core(3).md` | SUPPORT_OR_CONTEXT | 323,307 | 1,225 | `a4dfee34bdae2c533b0e053dc1be061ea05793455d797585855a848f1bea350a` | tick,PIT,XQ |
| 6 | `G02_Taiwan_Data_Research_ICT_Risk(3).md` | SUPPORT_OR_CONTEXT | 472,916 | 1,872 | `db948e7c69f10bb7ff9335ed5ef8dd1a148f684f6a851482e71c872ae1499d65` | 回測,tick,DatasetVersion,PIT,DuckDB,Parquet,XQ |
| 7 | `G03_RBWI_Execution_Agent_Harness(3).md` | SUPPORT_OR_CONTEXT | 336,699 | 1,253 | `7b9efaf9207cbfcdee8d5d09db77e20ba52bdb50db34989d4c22c86d059b2a82` | tick,PIT,XQ |
| 8 | `G04_Quant_Validation_Model_Risk(3).md` | SUPPORT_OR_CONTEXT | 88,455 | 441 | `1d9d256451e64f3471e96f3a7b661bdbf6075f15670eef97acd60a88b90587e7` | PIT,XQ |
| 9 | `G05_Assurance_Knowledge_Recovery(3).md` | SUPPORT_OR_CONTEXT | 85,029 | 436 | `a1e01f19ccb6de9a971ad6aced4cf9351623f08e6cd6e449493de54eac536f6c` | PIT,XQ |
| 10 | `G06_Learning_Evidence_Release(3).md` | SUPPORT_OR_CONTEXT | 105,014 | 465 | `46172deee832b42a109f2e83c0aee92897166d3e86536dce92ecf4f6cfce63a1` | PIT,XQ |
| 11 | `G07_Tool_Provider_PRW_Windows(3).md` | SUPPORT_OR_CONTEXT | 103,866 | 403 | `111a5a03ea9dc89f1d51cc600f1444557d047e7c804dba9409f864d8336eff01` | XQ |
| 12 | `GRP-00.md` | CONTROL_NORMATIVE | 8,033 | 176 | `efa948788b0946a7ca3fac141203ca406010f646b308f99b34932af96b60ec07` | - |
| 13 | `GRP-01_CONTROL_PRODUCT.md` | CONTROL_NORMATIVE | 649,280 | 3,506 | `1ba585ea8ee6b63d9a515fd9cd764ed2b7c76c29f86a872575cd05b48124697d` | PIT |
| 14 | `GRP-02_ARCHITECTURE_AGENT.md` | CONTROL_NORMATIVE | 207,556 | 2,523 | `a6e840cc9dc9d5969b8438217d981d56efe517cf74322aed6869d4759d9f41c5` | PIT |
| 15 | `GRP-03_SKILLS_SHARED.md` | CONTROL_NORMATIVE | 215,910 | 3,396 | `4c73f66b5e9cd9aa5f127786b03c88ce52dc564a92605128f9d9aeb78b7b15db` | - |
| 16 | `GRP-04_PRW_FACTORY.md` | CONTROL_NORMATIVE | 2,212,567 | 5,975 | `b6fa9e23179631739b7976d8c711ce66f1dabe4dd38deae5c9f43d68d3465ba3` | 回測,tick,PIT,XQ |
| 17 | `GRP-05_TOOLCHAIN_PROVIDER.md` | CONTROL_NORMATIVE | 355,749 | 3,695 | `517e5160d403ee5435104eb45b888042670fb640dac42319b4dd25db9937dddd` | - |
| 18 | `GRP-06_ASSURANCE_SECURITY.md` | CONTROL_NORMATIVE | 146,162 | 658 | `d4290ef7978864a877beb86a38bd9f019718f7011e50310496d020944ffccca0` | - |
| 19 | `GRP-07_BUILDER_KNOWLEDGE.md` | CONTROL_NORMATIVE | 202,156 | 3,950 | `97ee2eabefe21d7ecfdd4c1ef39ac89d297783694a2423cf7a1e44b99b41d964` | PIT |
| 20 | `GRP-08_RUNBOOK_HANDOFF.md` | CONTROL_NORMATIVE | 26,018 | 495 | `7c4653d8bdf726a550ba4e6469cdcdfa78c3251a4252b4a44c98c0f554ab60ff` | - |
| 21 | `GRP-09_RELEASE.md` | CONTROL_NORMATIVE | 516,225 | 1,123 | `02985d76b99f4922c2a50456b4ae5b35a46d2987be5e3fd9a646350370937767` | 回測,PIT |
| 22 | `HG-KSEOS_實作前開發文檔包_v2026.08.06-r2(1).md` | DONOR_SUPPORT | 2,311,551 | 10,396 | `7e287444c99112978ec1740adaaa848511dbc49737bb3419790f3efd4241e76f` | PIT,DuckDB |
| 23 | `PORTABLE_MOUNT_PROFILE.md` | CONTROL_NORMATIVE | 140,736 | 814 | `64f6998aafd4072cc6cbbe8f8d573339ac095920ee8716e3a7200226fc8822ec` | - |
| 24 | `SQS-THC × TW-ICT FSDT Stack｜台股歷史資料實際需求、最佳取得管道與成本鑑定.md` | PROJECT_NORMATIVE | 23,662 | 859 | `2d82378f000c296eedf85aa9b823b67f41bff6ef6aa538d08e2aec9dd51044a5` | FinMind,Shioaji,TWSE,TPEx,回測,分K,tick,DatasetVersion,PIT,DuckDB,Parquet,XQ |
| 25 | `SQS-THC_P0-CIP-PACK_v2026.08.06-r2.md` | PROJECT_NORMATIVE | 1,417,610 | 15,780 | `0d7c38267632a23f02e4256ab20cd16fdc5a8a5251393201c4178dc671c92f1b` | 回測,tick,DatasetVersion,PIT,DuckDB,Parquet,XQ |
| 26 | `SQS-THC_P0-CIP資料_vol-01.md` | PROJECT_NORMATIVE | 660,478 | 9,797 | `8d1e6babfc03ff2e05b745f5ae0436e31c0fcb6a6874a42e66a72d5b89728448` | Shioaji,回測,tick,PIT,DuckDB,Parquet,XQ |
| 27 | `SQS-THC_P0-CIP資料_vol-02.md` | PROJECT_NORMATIVE | 680,622 | 8,954 | `906bdac51bc210385c84983be5a7bd65a58be8b1659a3aa860e65ba74b6fae18` | Shioaji,TWSE,TPEx,回測,tick,DatasetVersion,PIT,DuckDB,Parquet,XQ |
| 28 | `SQS-THC_P0-CIP資料_vol-03.md` | PROJECT_NORMATIVE | 576,325 | 11,788 | `64a30f39e4dad07110efd9307d342ec7ac990a881f65a2dd7259726349fc962e` | FinMind,Shioaji,TWSE,TPEx,回測,tick,PIT,DuckDB,Parquet,XQ |
| 29 | `SQS-THC_P0-CIP資料_vol-04.md` | PROJECT_NORMATIVE | 644,189 | 13,497 | `0059067455b10f641a7a774ea981ef86e70bc591068dbb3c89cc097d2e17604b` | FinMind,Shioaji,TWSE,TPEx,回測,tick,PIT,DuckDB,Parquet,XQ |
| 30 | `SQS-THC_P0-CIP資料_vol-05.md` | PROJECT_NORMATIVE | 672,754 | 13,495 | `fe71ceb36f4abd57ebcbab44fc734de5b2025868bb6061d9e8f310fd8377943c` | PIT |
| 31 | `SQS-THC_P0-CIP資料_vol-06.md` | PROJECT_NORMATIVE | 694,824 | 18,857 | `6506b463a12525ea1beb52324c94af589c40c993303aa80822ce3837d8c2759b` | - |
| 32 | `SQS-THC_P0-CIP資料_vol-07.md` | PROJECT_NORMATIVE | 684,753 | 10,390 | `c0113d39914b47cbaa325134030ce9bcb5e1c09cd323e6ab23543af0c4c1c059` | PIT |
| 33 | `SQS-THC_P0-CIP資料_vol-08.md` | PROJECT_NORMATIVE | 654,417 | 12,689 | `ef48d3f90b114af3a13c5c8360ad1e7b6d2e0069790e2ea00e2d3c96e39f065b` | - |
| 34 | `SQS-THC_P0-CIP資料_vol-09.md` | PROJECT_NORMATIVE | 679,605 | 10,731 | `18f0fc31cb09243746a49f0399208049d82416407543658005f8abf6bb134cef` | PIT |
| 35 | `SQS-THC_P0-CIP資料_vol-10.md` | PROJECT_NORMATIVE | 681,971 | 12,906 | `30fd1be0ba83bd750cc6dcbe3b60ffca811b8e60e2c5bbb63369647edf1cb0c4` | PIT |
| 36 | `SQS-THC_TW-ICT_FSDT-Stack_實作RBWI_WP_控制工件_PACK_全冊藍圖_2026-08-09_r2.md` | PROJECT_NORMATIVE | 3,963,795 | 13,584 | `cac03502a57678e4b34baaf5dbf4f3d238cdcdbe028cf696c1766a9792364cea` | FinMind,TWSE,TPEx,回測,tick,DatasetVersion,PIT,DuckDB,Parquet,XQ |
| 37 | `SQS-THC_TW-ICT_FSDT-Stack_實作RBWI_WP_控制工件_PACK_實作RBWI_WP_控制工件_方案_2026-08-09_r1.md` | PROJECT_NORMATIVE | 71,473 | 1,155 | `ef719b20756ac6bb6492fd294f3c37d7c0ad7c28e77703d2c82c41d3a59370f9` | PIT,DuckDB,Parquet,XQ |
| 38 | `SQS-THC_TW-ICT_FSDT-Stack_實作RBWI_WP_控制工件_PACK_專家角色職位與專精領域總表_2026-08-09_r2.md` | PROJECT_NORMATIVE | 93,000 | 533 | `4fafe16dfdc5a906a4a7887877bf3eb6862227a0a309b6cab057aded1c12fd67` | TWSE,TPEx,tick,DatasetVersion,PIT,DuckDB,Parquet,XQ |
| 39 | `SQS-THC_TW-ICT_FSDT-Stack_實作RBWI_WP_控制工件_PACK_必須實作驗收交付總規格_2026-08-09_r2.md` | PROJECT_NORMATIVE | 305,186 | 1,422 | `9a43790eb5138fa255e6ffe98354e26c49caff96fddb6057700e558eb0f9b085` | FinMind,TWSE,TPEx,回測,tick,DatasetVersion,PIT,DuckDB,Parquet,XQ |
| 40 | `SQS-THC_TW-ICT_FSDT-Stack_實作RBWI_WP_控制工件_PACK_目標功能_SPEC_開源工具SKILLS安裝測試_驗收檢測交付_2026-08-09_r3.md` | PROJECT_NORMATIVE | 347,028 | 1,931 | `d16b5f32a1715c690ce08a1320cb7ac10e014f706b2d208361210473ed8e0e11` | FinMind,TWSE,TPEx,回測,tick,DatasetVersion,PIT,DuckDB,Parquet,XQ |
| 41 | `SQS-THC_TW-ICT_FSDT-Stack_實作RBWI_WP_控制工件_PACK_總藍圖_2026-08-09_r2.md` | PROJECT_NORMATIVE | 3,595,937 | 13,502 | `487a183c653f467e42dedbad0182c22ae1c52d5cbab348726f6adff3b65904eb` | FinMind,TWSE,TPEx,回測,tick,DatasetVersion,PIT,DuckDB,Parquet,XQ |
| 42 | `SQS-THC_TW-ICT_FSDT-Stack_實作RBWI_WP_控制工件_PACK_草案_v2026.08.09-draft-r2.md` | PROJECT_NORMATIVE | 4,622,434 | 14,642 | `9346bd015713304c1c527152d6e249104cd7efd5c0065961bcbf8b880f6db9e7` | FinMind,TWSE,TPEx,回測,tick,DatasetVersion,PIT,DuckDB,Parquet,XQ |
| 43 | `SQS-THC_TW-ICT_FSDT-Stack_實作前開發文檔包_v2026.08.09-r2_G01_產品金融核心與執行正文.md` | PROJECT_NORMATIVE | 1,126,406 | 5,031 | `322161904817f21e1521b3f833b101e6ab3e6080b4bc6190e5ad32258afc4af4` | 回測,tick,DatasetVersion,PIT,DuckDB,Parquet,XQ |
| 44 | `SQS-THC_TW-ICT_FSDT-Stack_實作前開發文檔包_v2026.08.09-r2_G02_工程契約工具技術供體與施工登錄.md` | PROJECT_NORMATIVE | 2,231,142 | 7,061 | `67acf69a05830b00abaf3ce12dba5c87192222c61092a8f736b2dd3172fe05c8` | FinMind,TWSE,TPEx,回測,tick,DatasetVersion,PIT,DuckDB,Parquet,XQ |
| 45 | `SQS-THC_TW-ICT_FSDT-Stack_實作前開發文檔包_v2026.08.09-r2_G03_追溯驗收移交與Readback.md` | PROJECT_NORMATIVE | 112,525 | 375 | `3f1d00cf5f1507285119932f926c6c5e0b184ae9121bbba0e9992d3813822bcf` | 回測,tick,DatasetVersion,PIT,XQ |
| 46 | `SQS-THC_工程開發文檔_DOC-00_2026-08-04_r2.md` | PROJECT_NORMATIVE | 235,308 | 3,845 | `db2d911f1cad03a4347711fbc8bc2b660e9eba79a447d4ea9295b6f3b0980060` | TWSE,TPEx,回測,PIT,DuckDB,Parquet,XQ |
| 47 | `SQS-THC_工程開發文檔_DOC-01_2026-08-04_r2.md` | PROJECT_NORMATIVE | 175,256 | 2,129 | `cd29f9afe23ff04566ba52d9deddd9535858895ae5e7c338a2aebd6635928093` | 回測,tick,DatasetVersion,PIT,DuckDB,Parquet,XQ |
| 48 | `SQS-THC_工程開發文檔_DOC-02_2026-08-04_r2(1).md` | PROJECT_NORMATIVE | 522,926 | 5,541 | `2df0c1af385a048a4d3177292454128d0e968772142038f701ac3172b824caaf` | TWSE,TPEx,回測,tick,DatasetVersion,PIT,DuckDB,Parquet,XQ |
| 49 | `SQS-THC_工程開發文檔_DOC-03_2026-08-04_r2.md` | PROJECT_NORMATIVE | 385,383 | 8,098 | `244853748769d3c9a5d0ff52e62aebf7907280b7aaa373fbf198f745f03a89e4` | TWSE,TPEx,回測,tick,DatasetVersion,PIT,DuckDB,Parquet,XQ |
| 50 | `SQS-THC_工程開發文檔_DOC-04_2026-08-04_r2.md` | PROJECT_NORMATIVE | 320,628 | 3,706 | `a4f736f084118f36d6a492e63139369834c2d629afecbb57e09f08f04ddc8620` | TWSE,TPEx,PIT,DuckDB,Parquet,XQ |
| 51 | `SQS-THC_工程開發文檔_DOC-05_2026-08-04_r2.md` | PROJECT_NORMATIVE | 2,390,346 | 6,863 | `3834a10efbe26def560b15260cb0620a7564c2216502932f9585e20f6ef249fd` | Shioaji,TWSE,TPEx,回測,tick,DatasetVersion,PIT,DuckDB,Parquet,XQ |
| 52 | `SQS-THC_工程開發文檔_DOC-06_2026-08-04_r2.md` | PROJECT_NORMATIVE | 257,663 | 4,190 | `d18930b18aecabb2a8ef0224049e02a16d84d441674c0938af7b633fd5870b4e` | PIT,DuckDB,Parquet,XQ |
| 53 | `SQS-THC_工程開發文檔_DOC-07_2026-08-04_r2.md` | PROJECT_NORMATIVE | 410,261 | 6,649 | `a01f83c4cbbce1ddb0126e801b936efb8bba0714423f4555f268ba95e6a57d71` | 回測,tick,DatasetVersion,PIT,DuckDB,Parquet,XQ |
| 54 | `SQS-THC_工程開發文檔_DOC-08_2026-08-04_r2.md` | PROJECT_NORMATIVE | 548,799 | 8,122 | `5200271c7af1c9fed5d7ec54fdf13b430d8ad5dbec24daad1f5052ad0a84863a` | 回測,tick,PIT,DuckDB,Parquet,XQ |
| 55 | `SQS-THC_工程開發文檔_DOC-09_2026-08-04_r2.md` | PROJECT_NORMATIVE | 724,552 | 23,578 | `09494ac68030174b03d4702f6f63b2ba7ab2747195422af9c416a4cfdcd33143` | TWSE,TPEx,回測,tick,PIT,DuckDB,Parquet,XQ |
| 56 | `SQS-THC_工程開發文檔_DOC-10_2026-08-04_r2.md` | PROJECT_NORMATIVE | 440,166 | 4,812 | `4d9eba36c4ef90e6111cb9b58c6f090cb6a2cdd678dffcf0edbf736dbff85f38` | TWSE,DatasetVersion,PIT,DuckDB,Parquet,XQ |
| 57 | `SQS-THC_工程開發文檔_DOC-11_2026-08-04_r2.md` | PROJECT_NORMATIVE | 814,522 | 16,960 | `cdeb06eefc2dacac6d3966bdf04d924da8bb518add740dafd5adeb2698e7c3d2` | 回測,PIT,DuckDB,Parquet,XQ |
| 58 | `SQS-THC_工程開發文檔_DOC-12_2026-08-04_r2(1).md` | PROJECT_NORMATIVE | 484,541 | 11,463 | `628042692d83a2b728fdecd92b9920760d497704cb1b99ba31c63f085fed80bc` | PIT,DuckDB,Parquet,XQ |
| 59 | `Spartoi_總系統級_SP-TS-00.md` | DONOR_SUPPORT | 218,591 | 1,760 | `cf7c393ea9fb739dfc8140252063d2f427ad30f16a1f7485a7d377c4656113d3` | TWSE,PIT,XQ |
| 60 | `Spartoi_總系統級_SP-TS-01.md` | DONOR_SUPPORT | 436,046 | 3,088 | `f9c1620afea5dcb8e939c99226f663a27aef4a8376263e7c29463be4c9b10c72` | PIT,DuckDB,Parquet,XQ |
| 61 | `Spartoi_總系統級_SP-TS-02.md` | DONOR_SUPPORT | 174,393 | 1,484 | `ff15257269c9fffa0a6d4c978a24225cfae4d2185bfad32d2aec9ac38584a62c` | XQ |
| 62 | `Spartoi_總系統級_SP-TS-03.md` | DONOR_SUPPORT | 148,587 | 1,463 | `3b93e448a2a6f62cb400eeae9425021084cc64a99e176e71729f02d32b8676c6` | 回測,PIT |
| 63 | `Spartoi_總系統級_SP-TS-04.md` | DONOR_SUPPORT | 390,240 | 1,422 | `fd9d9874abbd637b5664b5fba8a571da4dbef34388a1fefbee3fbd3f13ab47af` | tick,PIT,XQ |
| 64 | `Spartoi_總系統級_SP-TS-05.md` | DONOR_SUPPORT | 196,924 | 1,471 | `b095b64b49b8217694d583535746f86db715f8f4f48b7c788ef857d3fd1561cc` | PIT |
| 65 | `Spartoi_總系統級_SP-TS-06.md` | DONOR_SUPPORT | 227,516 | 1,224 | `84d44b7ac2e9cbd2101cee66c164723eced00509ab9876072ee3e29988369e62` | 回測,tick,PIT,XQ |
| 66 | `Spartoi_總系統級_SP-TS-07.md` | DONOR_SUPPORT | 160,369 | 1,203 | `87592cae2e78909b40cb23fdcb7dbfff8061550c85926fee1ddea5532cf9f9fd` | PIT |
| 67 | `Spartoi_總系統級_SP-TS-08.md` | DONOR_SUPPORT | 312,616 | 1,428 | `48683ba8332d9e2fcad04b24b4179db631bc40c4dd3cf1a18d00b7514be425bb` | PIT |
| 68 | `Spartoi_總系統級_SP-TS-09.md` | DONOR_SUPPORT | 95,785 | 1,249 | `47c532dca41862333ac6a154b5fd0087958a44e12388ebabfe06e387e41363b5` | PIT |
| 69 | `Spartoi_總系統級_SP-TS-10.md` | DONOR_SUPPORT | 381,741 | 1,206 | `0ad7ea12816abbb59e21b5c305572dd323c0e4af6de81e955c1f30f4e789e5fb` | TWSE,TPEx,回測,PIT |
| 70 | `TW-ICT FSDT Stack：OpenSpec／GStack／Matt Pocock Skills「Coding SPEC → Financial SPEC」承接完整性鑑定報告.md` | PROJECT_NORMATIVE | 33,495 | 1,239 | `cdd76bdea42c5b32d79d0aaf8820311479d29cc01eb8e012639970ecf7c98a95` | PIT,DuckDB,Parquet,XQ |
| 71 | `TW-ICT_FSDT-Stack_P0-CIP-PACK_v2026.08.06-rFINAL-r2.md` | PROJECT_NORMATIVE | 1,115,929 | 12,988 | `cd1b90d70fc2a161fff1840af4ffe2a46c4a092b5bfa4872bbdd67dddbeb87ed` | TWSE,TPEx,回測,tick,PIT,DuckDB,Parquet,XQ |
| 72 | `TW-ICT_FSDT-Stack_P0-CIP資料_vol-01.md` | PROJECT_NORMATIVE | 425,749 | 10,536 | `47a6bfb2963147274cdf3db439f6eb1d58bc61cd222700a22ce66d822545d0b6` | TWSE,TPEx,回測,tick,PIT,DuckDB,Parquet,XQ |
| 73 | `TW-ICT_FSDT-Stack_P0-CIP資料_vol-02.md` | PROJECT_NORMATIVE | 444,962 | 3,374 | `c9f2b67b904ffac3a0d25d49d4f3e37eeae2aa1b7143d5e2955972f3d67623e8` | PIT,DuckDB,Parquet,XQ |
| 74 | `TW-ICT_FSDT-Stack_P0-CIP資料_vol-03.md` | PROJECT_NORMATIVE | 430,750 | 6,239 | `0ab9903a1d2de1a4623ce04b540a0a671dda0566d3ebd2d922f7785704fe148f` | TWSE,TPEx,tick,PIT,DuckDB,Parquet,XQ |
| 75 | `TW-ICT_FSDT-Stack_P0-CIP資料_vol-04.md` | PROJECT_NORMATIVE | 409,041 | 6,888 | `1389ae13b4a0e2130f6d0fec31dc2c189211783a1f43c8af4286e3bd8217c35b` | Shioaji,TWSE,TPEx,回測,分K,tick,PIT,DuckDB,Parquet,XQ |
| 76 | `TW-ICT_FSDT-Stack_P0-CIP資料_vol-05.md` | PROJECT_NORMATIVE | 409,142 | 9,559 | `e8d2d2f730b4293ca2bc0d22ba83bdca1fa03d0d654b5927c49aec3242dd55e6` | TWSE,TPEx,回測,分K,PIT,DuckDB,Parquet,XQ |
| 77 | `TW-ICT_FSDT-Stack_P0-CIP資料_vol-06.md` | PROJECT_NORMATIVE | 446,306 | 3,374 | `8da673dda6c28fd8bcfe6c60517da1834b19d0b655bf8fa000d4a041e4bb6d45` | PIT,DuckDB,Parquet,XQ |
| 78 | `TW-ICT_FSDT-Stack_P0-CIP資料_vol-07.md` | PROJECT_NORMATIVE | 432,094 | 6,239 | `f9ad1ba33485f7c67834b92e30de1289b480573617df82780dd53273835dd652` | TWSE,TPEx,tick,PIT,DuckDB,Parquet,XQ |
| 79 | `TW-ICT_FSDT-Stack_P0-CIP資料_vol-08.md` | PROJECT_NORMATIVE | 422,381 | 3,917 | `35727568e54bb5f02b7c7a7a15950f87025d0b0de33051bd96df593774dce240` | TWSE,TPEx,回測,分K,PIT,DuckDB,Parquet,XQ |
| 80 | `TW-ICT_FSDT-Stack_P0-CIP資料_vol-09.md` | PROJECT_NORMATIVE | 420,717 | 9,877 | `cb17ba0c1034cd7c15b2ea90a88ad13961b04ecabe6fb4d846147a9c653c39f1` | FinMind,TWSE,TPEx,回測,分K,tick,PIT,DuckDB,Parquet,XQ |
| 81 | `TW-ICT_FSDT-Stack_P0-CIP資料_vol-10.md` | PROJECT_NORMATIVE | 427,475 | 7,899 | `6ef9c707ac08e5240908bcfdb4ca29d84798aa08c2c192811dc473e5ebe2f36b` | FinMind,TWSE,TPEx,回測,tick,PIT,DuckDB,Parquet,XQ |
| 82 | `TW-ICT_FSDT-Stack_專業技術文檔_DOC-00_2026-07-31_r2(1).md` | PROJECT_NORMATIVE | 373,457 | 6,717 | `04e0e3071127ef0bc8d3789dea7c97b47eb3ed3d352ecb8d87753cfbf56d0f73` | FinMind,TWSE,TPEx,回測,PIT,DuckDB,Parquet,XQ |
| 83 | `TW-ICT_FSDT-Stack_專業技術文檔_DOC-01_2026-07-31_r3.md` | PROJECT_NORMATIVE | 1,110,401 | 10,315 | `410dab9ad0c18720d4aae372f338100859a632af6e744bddabcac9975dd3daf9` | 回測,tick,PIT,DuckDB,Parquet,XQ |
| 84 | `TW-ICT_FSDT-Stack_專業技術文檔_DOC-02_2026-07-31_r3.md` | PROJECT_NORMATIVE | 417,544 | 6,528 | `0ccaad683490348dd31a61744a1d2a17620bdc197911b97f93c51f9f1ae912ba` | TWSE,TPEx,回測,PIT |
| 85 | `TW-ICT_FSDT-Stack_專業技術文檔_DOC-03_2026-07-31_r2.md` | PROJECT_NORMATIVE | 935,926 | 13,666 | `fa7cb4385785df19285cc5338dcd8953b24f4a15da7487942dfb10c2d575e104` | TWSE,TPEx,回測,tick,PIT,DuckDB,Parquet |
| 86 | `TW-ICT_FSDT-Stack_專業技術文檔_DOC-04_2026-07-31_r3.md` | PROJECT_NORMATIVE | 505,175 | 6,662 | `9cb79be47f648bca6fbcd924dcd141c3ef087d8ec6eca52638ee8b0ccfcde35d` | 回測,PIT |
| 87 | `TW-ICT_FSDT-Stack_專業技術文檔_DOC-05_2026-07-31_r2.md` | PROJECT_NORMATIVE | 1,147,080 | 4,313 | `ae68fa557dd5591f91392bb055e6ac19ae976bfc941d97355c8090c788e48631` | FinMind,TWSE,回測,tick,PIT,DuckDB,Parquet,XQ |
| 88 | `TW-ICT_FSDT-Stack_專業技術文檔_DOC-06_2026-07-31_r2.md` | PROJECT_NORMATIVE | 340,131 | 4,173 | `3cd6e70cef7047d89963067888d3187f13cdbf52aa71f725eb8bf2aee891db5c` | TWSE,TPEx,回測,tick,PIT,DuckDB,Parquet,XQ |
| 89 | `TW-ICT_FSDT-Stack_專業技術文檔_DOC-07_2026-07-31_r2.md` | PROJECT_NORMATIVE | 641,558 | 8,466 | `b36f9d2615d30e0b1df91ae72efa8ac8a460fa20bdfe9ce9a9077b897c05cc6f` | TWSE,TPEx,回測,tick,DatasetVersion,PIT,DuckDB,Parquet,XQ |
| 90 | `TW-ICT_FSDT-Stack_專業技術文檔_DOC-08_2026-07-31_r2.md` | PROJECT_NORMATIVE | 273,034 | 4,428 | `daa1dfaa0f3565929fb55c19981fc417a326267cca1d6f8552eb8e1922e89ff3` | TWSE,TPEx,tick,PIT,DuckDB,Parquet,XQ |
| 91 | `TW-ICT_FSDT-Stack_專業技術文檔_DOC-09_2026-07-31_r2.md` | PROJECT_NORMATIVE | 965,499 | 8,461 | `f4c7340f8eaf812d2313aef11d62a0d6099303fda5b8fdfab6951868a67ec3bf` | TWSE,TPEx,PIT,DuckDB,Parquet |
| 92 | `TW-ICT_FSDT-Stack_專業技術文檔_DOC-10_2026-07-31_r2.md` | PROJECT_NORMATIVE | 426,071 | 5,217 | `bcee23ab941d74a7befcaf77dc03948f39643b7ee3511cef07da27f30e4f2c3e` | TWSE,TPEx,tick,PIT,DuckDB,Parquet,XQ |
| 93 | `TW-ICT_FSDT-Stack_專業技術文檔_DOC-11_2026-07-31_r2.md` | PROJECT_NORMATIVE | 376,936 | 11,464 | `2172b47fbde22310bacccbb630c447706bb5b7418cc14a9ecc04efd464c13d40` | TWSE,TPEx,回測,tick,PIT,DuckDB,Parquet,XQ |
| 94 | `TW-ICT_FSDT-Stack_專業技術文檔_DOC-12_2026-07-31_r3.md` | PROJECT_NORMATIVE | 1,319,393 | 13,170 | `e763ca0a79271fcaaff93b043afbba78a9031804582611feb78c476733442236` | TWSE,TPEx,回測,tick,PIT,DuckDB,Parquet,XQ |
| 95 | `TW-ICT_FSDT-Stack_專業技術文檔_DOC-13_2026-07-31_r3(1).md` | PROJECT_NORMATIVE | 387,581 | 4,495 | `b2b7dd12fc18d5f8b0027bbbad72682b4307a7c20cf40c573a2d6331b38eb786` | TWSE,回測,tick,PIT,DuckDB,Parquet,XQ |
| 96 | `TW-ICT_FSDT-Stack_專業技術文檔_DOC-14_2026-07-31_r3.md` | PROJECT_NORMATIVE | 683,315 | 9,319 | `09b7fcd6c03ad32f14717be3bced112c206205765ffa20845a3a30c18d39bb4d` | 回測,tick,PIT,DuckDB,Parquet,XQ |
| 97 | `TW-ICT_FSDT-Stack_專業技術文檔_DOC-15_2026-07-31_r2.md` | PROJECT_NORMATIVE | 244,196 | 3,765 | `adb18bfc49d6e57b34cead03de8d0c4a798c0f280b9a110ec4aa0c2b51103211` | TWSE,tick,PIT,XQ |
| 98 | `TW-ICT_FSDT-Stack_專業技術文檔_DOC-16_2026-07-31_r2.md` | PROJECT_NORMATIVE | 202,100 | 3,272 | `2f6876f3fc5068637e4dd09bc4a020b547d610460f017e3437659d872ef5b14d` | PIT,DuckDB,Parquet,XQ |
| 99 | `TW-ICT_FSDT-Stack_專業技術文檔_DOC-17_2026-07-31_r2.md` | PROJECT_NORMATIVE | 865,622 | 5,058 | `a484543434bea3216f5a23b14d9fdfd5dfe4c1fe66861559a1124a32bc5dc071` | DuckDB,Parquet,XQ |
| 100 | `TW-ICT_FSDT-Stack_專業技術文檔_DOC-18_2026-07-31_r2.md` | PROJECT_NORMATIVE | 581,060 | 12,798 | `d502d0fa3e626c12e1d02d8168f7cc15ef777801abd4f700537cc65688d07e6f` | 回測,PIT,DuckDB,Parquet,XQ |
| 101 | `TW-ICT_FSDT-Stack_專業技術文檔_DOC-19_2026-07-31_r2(1).md` | PROJECT_NORMATIVE | 718,037 | 8,903 | `2ceb70d7cc15f1d14d95621d8aecf453bfec796428353536354ea4169d19ce46` | PIT,Parquet |
| 102 | `TW-ICT_FSDT-Stack_專業技術文檔_DOC-20_2026-07-31_r2(2).md` | PROJECT_NORMATIVE | 1,333,275 | 18,061 | `7d96f4862353bb37adfa4ae28b45b46a88118061d85924ec0d8f823098feba86` | 回測,DatasetVersion,PIT,DuckDB,Parquet |
| 103 | `TW-ICT_FSDT-Stack_專業技術文檔_DOC-21_2026-07-31_r2.md` | PROJECT_NORMATIVE | 1,314,674 | 10,131 | `b5108601cc83077623bdb33eb809305e139fb16e35a576794dc2967546384489` | 回測,tick,PIT,DuckDB,Parquet,XQ |
| 104 | `TW-ICT_FSDT-Stack_專業技術文檔_DOC-22_2026-07-31_r2(1).md` | PROJECT_NORMATIVE | 705,715 | 10,328 | `fab83ab0bff3b464e33b74a656523dbd0feed035adb2564ba7e11fccaf9b3645` | PIT |
| 105 | `TW-ICT_FSDT-Stack_專業技術文檔_DOC-23_2026-07-31_r2.md` | PROJECT_NORMATIVE | 471,228 | 6,173 | `0cb380c69987acfc1fad5a670ddefea5226d18faa000d77b1fb3c9e6e498cf18` | TWSE,回測,tick,PIT,DuckDB,Parquet,XQ |
| 106 | `TW-ICT_FSDT-Stack_專業技術文檔_DOC-24_2026-07-31_r2.md` | PROJECT_NORMATIVE | 611,323 | 9,426 | `3ded710847a00220778524476520118010620b99013a7e7df3174ef354f563db` | PIT,DuckDB,Parquet |
| 107 | `TW-ICT_FSDT-Stack_專業技術文檔_DOC-25_2026-07-31_r2(1).md` | PROJECT_NORMATIVE | 1,151,452 | 11,929 | `366a9d57c36cb3cdcd0169d34eb928162cbe4ed7844750124f53ab211526423f` | 回測,PIT,DuckDB,Parquet |
| 108 | `TW-ICT_FSDT-Stack_專業技術文檔_DOC-26_2026-07-31_r2.md` | PROJECT_NORMATIVE | 840,878 | 7,972 | `3a98629b3f5984c0590b00a0522a7dec098886ae90144a677dc56b2063810b74` | TPEx,回測,PIT,DuckDB |
| 109 | `TW-ICT_FSDT-Stack_專業技術文檔_DOC-27_2026-07-31_r2.md` | PROJECT_NORMATIVE | 1,073,437 | 17,588 | `6d95955e1100ab8417a848eb471118bdbdbdb30bc08ce562c43126f07ca682c4` | 回測,PIT,XQ |
| 110 | `TW-ICT_FSDT-Stack_專業技術文檔_DOC-28_2026-07-31_r2.md` | PROJECT_NORMATIVE | 259,043 | 4,361 | `1f8737ef5ad1a75eaa3410395ff8185d98067bf2f18854b8352edffa9a3d71d9` | 回測,tick,PIT,DuckDB,Parquet |
| 111 | `TW-ICT_FSDT-Stack_專業技術文檔_DOC-29_2026-07-31_r2.md` | PROJECT_NORMATIVE | 1,346,543 | 14,814 | `5ce3b383308b718e2a038e8077ba83cbc2e6d1f37ae1dfc2b2833f2eaa979588` | FinMind,Shioaji,TWSE,TPEx,回測,tick,PIT,DuckDB,Parquet,XQ |
| 112 | `TW-ICT_專業技術文檔_v3.0_DOC-00_r2_2026-07-29.md` | DONOR_SUPPORT | 1,439,671 | 8,657 | `47ba4ff4c4aacb1efdf25518a12da7448812c33fc2a7836b11b46dd07bc46815` | TWSE,回測,tick,PIT |
| 113 | `TW-ICT_專業技術文檔_v3.0_DOC-01_r2.md` | DONOR_SUPPORT | 167,318 | 2,131 | `082816dcab0a70db711f3d687c8df4fc7ef7a4f15931da2e5f62da89901ffe57` | TWSE,TPEx,回測,tick,PIT,DuckDB,Parquet,XQ |
| 114 | `TW-ICT_專業技術文檔_v3.0_DOC-02_2026-07-29_r2(2).md` | DONOR_SUPPORT | 447,907 | 6,530 | `c57fb7de0cc204e36ff2942276588fc25a0931e323fe37828b3e46b507416a92` | TWSE,TPEx,回測,tick,PIT,DuckDB,Parquet |
| 115 | `TW-ICT_專業技術文檔_v3.0_DOC-03_2026-07-29_r2(2).md` | DONOR_SUPPORT | 320,954 | 6,642 | `c8734c66a6ac9e514bd3411a836c9c50f05dd5b2d095281705e2f3ceac22cc3b` | TWSE,TPEx,回測,tick,PIT,DuckDB,Parquet |
| 116 | `TW-ICT_專業技術文檔_v3.0_DOC-04_2026-07-29_r2(2).md` | DONOR_SUPPORT | 306,997 | 4,102 | `75936e46be1300acac0478a0cbe190d0219cd68ca7c16b259712dc2b2ab55f33` | TWSE,TPEx,回測,PIT,DuckDB,Parquet |
| 117 | `TW-ICT_專業技術文檔_v3.0_DOC-05_2026-07-29_r2(2).md` | DONOR_SUPPORT | 469,932 | 8,041 | `605bb30eefbff6d828da2e61424db749ef15124e9f5e5170034eca67b9eaaa8b` | TWSE,TPEx,回測,tick,PIT,DuckDB,Parquet,XQ |
| 118 | `TW-ICT_專業技術文檔_v3.0_DOC-06_2026-07-29_r2.md` | DONOR_SUPPORT | 351,576 | 3,371 | `baf882b7eec67eb8c740340c6dea0358a7f3f3a8f28541c8da03d047917f56de` | TWSE,TPEx,回測,tick,PIT,DuckDB,Parquet,XQ |
| 119 | `TW-ICT_專業技術文檔_v3.0_DOC-07_2026-07-29_r2.md` | DONOR_SUPPORT | 182,485 | 3,401 | `47f4255a32fcd5acc681ccb1535f3bf676af913e2e5c19e6931f9860e0fcaaa8` | 回測,tick,PIT,DuckDB,Parquet,XQ |
| 120 | `TW-ICT_專業技術文檔_v3.0_DOC-08_2026-07-29_r2(2).md` | DONOR_SUPPORT | 229,624 | 3,613 | `9eeee54b9e0cce20a92d49e69d67b0d1272338894d20b4e5594b2550ffd177b4` | TPEx,回測,tick,DatasetVersion,PIT,DuckDB,Parquet |
| 121 | `TW-ICT_專業技術文檔_v3.0_DOC-09_r2_2026-07-29(2).md` | DONOR_SUPPORT | 866,271 | 7,142 | `a17f676958619ef3787ce37266c6e21984a3b9ce857a2103ae9112988e74e55c` | TWSE,TPEx,回測,tick,DatasetVersion,PIT,DuckDB,Parquet,XQ |
| 122 | `TW-ICT_專業技術文檔_v3.0_DOC-10_2026-07-29_r2(2).md` | DONOR_SUPPORT | 177,946 | 2,101 | `117d97254d8f4af3ffb21973c2a9c792b27714cbbaeaea89575b9b03145e6574` | TWSE,TPEx,回測,tick,PIT,DuckDB,Parquet,XQ |
| 123 | `TW-ICT_專業技術文檔_v3.0_DOC-11_r2_2026-07-29.md` | DONOR_SUPPORT | 300,340 | 5,565 | `b50bc1b331c1630270cb12499d33bb977cba78c97e499ae37b584abaf935f987` | 回測,tick,PIT |
| 124 | `XQ&XS_專業技術文檔_DOC-00_2026-07-27_r1(2).md` | DONOR_SUPPORT | 358,916 | 3,842 | `375e261b44ef8593268fc32a7f5594b17c970bbc7642aa9883d08bfe6d7a5a6e` | 回測,分K,tick,PIT,XQ |
| 125 | `XQ&XS_專業技術文檔_DOC-01_2026-07-27_r1.md` | DONOR_SUPPORT | 298,846 | 2,986 | `ab8b3682db8d53cc982a28ac252dab4bebb165d1c10f546e4a091889e2a0e942` | 回測,分K,tick,XQ |
| 126 | `XQ&XS_專業技術文檔_DOC-02_2026-07-27_r1(1).md` | DONOR_SUPPORT | 385,806 | 1,773 | `2f3a41dd4f71724402ab5965bd8c9db26d8a0a2c8732ee1cc99b80edfc30c973` | 回測,分K,tick,PIT,XQ |
| 127 | `XQ&XS_專業技術文檔_DOC-03_2026-07-27_r1.md` | DONOR_SUPPORT | 159,725 | 1,446 | `68ea2b124bc51e9629d2574c7ec505a2a764d8ef698cb0cd14a860dfc54d817f` | 回測,分K,tick,XQ |
| 128 | `XQ&XS_專業技術文檔_DOC-04_2026-07-27_r1(1).md` | DONOR_SUPPORT | 1,459,697 | 5,254 | `5a0d8a9f90746ca539ec5c808155ae233e9c84ed79ca55b43862b536b0245abb` | 回測,分K,tick,PIT,XQ |
| 129 | `XQ&XS_專業技術文檔_DOC-05_2026-07-27_r1(1).md` | DONOR_SUPPORT | 1,198,892 | 3,325 | `29f3e60a18aa9b69019cd1590f29f91c8c5ad6eb17d1e739e947ec0a0000e8d1` | TWSE,回測,分K,tick,PIT,XQ |
| 130 | `XQ&XS_專業技術文檔_DOC-06_2026-07-27_r1(1).md` | DONOR_SUPPORT | 580,340 | 5,102 | `4d0b664aa9b1960ea95d93dd8cac800a15c69222c859dbaa1bf969d88b631967` | 回測,分K,tick,PIT,XQ |
| 131 | `XQ&XS_專業技術文檔_DOC-07_2026-07-27_r1(1).md` | DONOR_SUPPORT | 369,290 | 2,736 | `fc8848a21b97eeb2f74f2b904e879b58cbe3c8e387aca62c3383d02fbcd0abb7` | 回測,分K,tick,XQ |
| 132 | `XQ&XS_專業技術文檔_DOC-08_2026-07-27_r1(1).md` | DONOR_SUPPORT | 413,704 | 3,290 | `14a6cd973c08770dc9102047c1b2c38953317dd60fefb98dc0bb82fb948e43b4` | 回測,分K,tick,PIT,XQ |
| 133 | `XQ&XS_專業技術文檔_DOC-09_2026-07-27_r1(1).md` | DONOR_SUPPORT | 207,579 | 2,273 | `50aac0d1337e21e90d8e5cade15f966b8f68b0d9b2f2c6cfc126364bceffb175` | 回測,分K,tick,PIT,XQ |
| 134 | `XQ&XS_專業技術文檔_DOC-10_2026-07-27_r1(1).md` | DONOR_SUPPORT | 212,951 | 2,464 | `8cb16399c91fed58727ef070370ede071a8897b048ff0e1a9aa446e114baf1fb` | 回測,分K,tick,XQ |
| 135 | `XQ&XS_專業技術文檔_DOC-11_2026-07-27_r1(1).md` | DONOR_SUPPORT | 250,973 | 1,922 | `e3e05bd1edb311b6885e0c3c439c74e936ad2035294df19b8f0f2b1f4a9026e3` | 回測,分K,tick,PIT,XQ |
| 136 | `XQ&XS_專業技術文檔_DOC-12_2026-07-27_r2(1).md` | DONOR_SUPPORT | 382,795 | 2,227 | `94d7dfeee0caa46478032833642cfdc3ec727910fe427a8ba89b1d3ea566c9a0` | 回測,分K,tick,PIT,XQ |
| 137 | `XQ&XS_專業技術文檔_DOC-13_2026-07-27_r1.md` | DONOR_SUPPORT | 1,572,751 | 6,215 | `c31009dd362b266847c3a4c1cdca7ac141bd788db00ef472b27288ca5ee9f530` | 回測,分K,tick,Parquet,XQ |
| 138 | `修補為具名 preferred candidate  admission pending.md` | PROJECT_NORMATIVE | 9,781 | 380 | `243ae8e1c19b2c41016375cba94bb1f1ccbc8f1d66b76ca3041af0fa3328ce5c` | FinMind,Shioaji,TWSE,TPEx,DatasetVersion,PIT,XQ |


## Appendix B — Direct Full-Scan Denominator

```json
{
  "file_count": 138,
  "bytes": 83767017,
  "lines": 816833,
  "aggregate_digest": "4174b4558f1cfcb432b74d13a5ce5c810be282fc6d4c712798933fadfa3abedb",
  "hit_files": 129
}
```

Keyword occurrence denominator (case-insensitive physical scan):

```text
FinMind                     204 occurrences / 15 files
Shioaji                     339 occurrences / 9 files
TWSE                        736 occurrences / 55 files
TPEx                        430 occurrences / 49 files
歷史                         1580 occurrences / 91 files
回測                         1753 occurrences / 84 files
分鐘                          874 occurrences / 35 files
分K                           152 occurrences / 19 files
Tick                         1911 occurrences / 77 files
OrderBook                    186 occurrences / 19 files
DatasetVersion               575 occurrences / 25 files
PIT                         8029 occurrences / 119 files
DuckDB                      1174 occurrences / 78 files
Parquet                     1289 occurrences / 78 files
XQ                         27407 occurrences / 95 files
XScript                    18649 occurrences / 54 files
TT-DATA-PROVIDER-PARITY       93 occurrences / 7 files
TT-BROKER-PROVIDER-ADMISSION  60 occurrences / 6 files
```

## Appendix C — Readback Contract

- UTF-8 decode: REQUIRED
- File non-empty: REQUIRED
- Required sections 0–11 + Appendices A–C: REQUIRED
- `machine_summary.json`, `change_plan.tsv`, `checkrun_contract.tsv`: REQUIRED
- No `INSTALLED / ADMITTED / PRODUCTION_PASS` claim: REQUIRED
- Final detached SHA-256: reported outside body below after write

<!-- FINAL_END_SENTINEL: TW_DATA_SHIOAJI_FIRST_BLUEPRINT_20260811_R1 -->
