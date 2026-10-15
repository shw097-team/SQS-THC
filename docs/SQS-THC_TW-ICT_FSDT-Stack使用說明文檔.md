# 《SQS-THC & TW-ICT_FSDT-Stack 使用說明文檔》

- 版本：2026-08-13 r6（Daily OHLCV 資料層啟用整合：WO-RP2-DAILY-001..004 EXTERNAL FINAL ACCEPTED；User Guide + README + AGENTS.md upgrade）
- Reference Project ID：`HGK-REFERENCE-PROJECT-002`（RP-002 v2.0；RP-001 仍為 MILESTONE_CLOSED 歷史）
- Milestone Status：RP-001 `MILESTONE_CLOSED`（歷史）；RP-002 v2.0 Stage-1/2/3 完成（LOCAL acceptance），外部 final meta PENDING_FOCUSED_REVIEW
- Canonical Root：`C:\Projects\Agent_Workspace\SQS-THC`
- Claim Ceiling：`SQS-THC_TW-ICT_FSDT_STACK_LOCAL_DELIVERY_PASS`（Production/Live/Remote NOT_CLAIMED）

## 1. Identity

| 欄位 | 值 |
|---|---|
| product_id | SQS-THC |
| formal_name | SQS-THC & TW-ICT FSDT Stack |
| namespace | sqs.ict.twhc |
| version | 2026.08.10-r1 |
| exact_error | ERR_PRODUCT_ID_COLLISION |

## 2. Directory Map（canonical root，P0-CIP §16）

```
SQS-THC/
├─ contracts/{product,authority,fsdt,rbwi,agentos,decision,execution,evidence}/
├─ src/{kernel,ports,profiles,adapters,projections}/   ← 5 kernels: fsdt/temporal/knowledge/harness/capability
├─ agents/{prompts,skills,profiles,jobcards}/
├─ workflows/{research,validation,risk,survival,xq,reconciliation}/
├─ research/{mission,universe,factors,ml,nlp,alternative-data}/
├─ docs/DOC-00..12.md
├─ requirements/MC_REGISTRY.yaml（MC-01..27）
├─ architecture/DOC_CH_OWNER_MAP.yaml（CH00..35）
├─ risk/limits.yaml  survival/guards.yaml
├─ adapters/xq-read-watch.yaml（read-only）
├─ schemas/execution-fact.schema.json
├─ reducers/book-of-record.yaml
├─ maturity/  sre/  security/  privacy/  supply-chain/
├─ evidence/  release/  migration/  nrtv/  training/
├─ tests/{unit,contract,legacy-regression,...}/  （231 tests, 2026-08-13 實測）
├─ handoff/（closed-book packs + consumer-ack ledger）
└─ 實作執行/（MIGRATION_SOURCE_OR_EVIDENCE_ONLY，非 product root）
```
- RP-002 v2.0 Stage-3 additions：`agents/profiles/{sqs-orchestrator,sqs-data-analysis,sqs-risk}/`、`SQS_STACK_MANIFEST.yaml`、`TEAM.md`、`SQS/TWICT_RUNTIME_PACK_MANIFEST.yaml`、`evidence/rp002/stage3/`（gates/knowledge/s1/wp30/closures）

## 3. Quick Start

```bash
cd C:\Projects\Agent_Workspace\SQS-THC
PYTHONPATH=src python -m unittest discover -s tests -t .   # 231 tests（2026-08-13 實測）
PYTHONPATH=src python scripts/validate-package.py          # package readback validator
```

## 4. Delivered Kernels（src/kernel/*）

| Kernel | Source chapter | Tests |
|---|---|---|
| fsdt（financial contract） | CH04 | 8 |
| temporal（five clocks / PIT / calendar） | CH06 | 7 |
| knowledge（RAG / memory / provenance） | CH10 | 7 |
| harness（loop / handoff） | CH15 | 8 |
| capability（tool lifecycle） | CH16 | 7 |

## 5. WorkOrder Register（15/15 DELIVERED + INDEPENDENT_CASE_PASS）

Wave-1（SEALED_ACCEPTED_REUSE）：WO-TS-REF-02..06（kernel CH04/06/10/15/16）
Wave-2（fresh CS-B evidence）：WO-TS-REF-01（product constitution）、07（investment/factor）、
08（ML/NLP/altdata）、09（validation/risk/survival）、10（decision/XQ/reconciliation）、
11（maturity/SRE/security）、12（evidence/release/NRTV）、13（donor migration）、
14（package/readback）、15（closed-book handoff/ACK）

每 WO：owner contract → Codex bounded worker → maker suite → INDEPENDENT_CASE_PASS →
Kanban done → spine VERIFIED。Kanban board：`sqs-thc-ref-001`。
- RP-002 Stage-3 額外 WO：WO-RP2-S3-{SQP1,S1,E1E2,R1}（writer=codex，VERIFIED）+ WO-RP2-S3-OBS-001（OBS closure）+ WO-RP2-PCIV-REPAIR-001（PCIV-F01 repair）+ WO-RP2-ECL-001（external evidence closure）+ WO-RP2-DOCS-001（本 upgrade）

## 6. Tool Route（named-method router）

| flow | route | state |
|---|---|---|
| plan | gstack.plan-eng-review | CERTIFIED（fresh CS-B invocation） |
| review/qa/security/release/ambiguity/retro | gstack.* slices | CERTIFIED |
| brownfield | openspec | CERTIFIED_ACTIVE_BROWNFIELD |

## 7. XQ/XS

SOURCE_VALID_NOT_APPLICABLE（V1）——RBWI TOOL-014 HITL_ONLY；無 autonomous adapter；
任何未來 adapter 需 credential HITL。`adapters/xq-read-watch.yaml` 為 read-only watch 契約。

## 8. Governance

- maker ≠ checker（每 WO 獨立 readback）
- Kanban/gstack 為 advisory，HG-KSEOS spine + canonical reducers 為 final authority
- no broker write；order path HITL_ONLY；production NOT_CLAIMED
- spartoi-total-system = PRIMARY_ENGINEERING_BASELINE 成員（REUSE/ADAPTER-first，抽取為後續 wave）

## 9. Acceptance / Release（current，EVO-005F frozen）

- HGK：acceptance 161/161、coverage reducer PASS、**274/274 suite**（HEAD 075475d）
- SQS：211/211 tests、15/15 WO INDEPENDENT_CASE_PASS、denominator all-0、project state DELIVERED
- RBWI：TW_ICT_RBWI_CURRENT_SUBJECT_ACCEPTANCE_PASS（LOCAL/PAPER/NO-LIVE-WRITE）
- **EVO-005F 單一 frozen truth**：Frozen Oracle `501732af…`、Subject `e546cc2c…`、
  Final Graph root `6535d9cd…`（FROZEN）、Final Verification Receipt、Final Attestation、
  r7 evidence（`evidence/review/SQS-THC_REFERENCE_PROJECT_001_FINAL_EVIDENCE_FOR_REVIEW_r7.md`）
- Package：`release/EVO005F_PACKAGE_MANIFEST.json`（WORKSPACE_LOCAL；**不維護大型 ZIP**——
  大型 delivery ZIP 已依 WORKSPACE_LOCAL 政策由使用者移除；僅 manifest 保留作 identity/rollback 參考）
- RP-002 v2.0 Stage-3（2026-08-13）：SQP1/S1/E1/E2/E3/R1 — child reducer `STAGE3_SQS_PASS_ELIGIBLE_FOR_MASTER_R1_REDUCTION`，master reducer `RP002_LOCAL_ACCEPTANCE_PASS`；final Stage-3 bundle `ba287aee…`；PCIV-F01 superseding closure（accepted 68867e08/8d8d7f42 原封）；外部最終 meta acceptance PENDING_FOCUSED_REVIEW。

## 10. Rollback

- 每 WO 為獨立 git commit（`git log --oneline`）；pre-seed commits 於
  `實作執行/worktrees/` 保留（rollback staging）
- package validator：`scripts/validate-package.py`（ERR_PACKAGE_READBACK_MISMATCH）
- SP-TS authority docs hashed（drift detection）
- 已 retired 舊 ZIP：`實作執行/SQS-THC_LOCAL_DELIVERY_CANDIDATE.zip`
  （sha `37fd9c2c…`，housekeeping receipt 記錄；WORKSPACE_LOCAL 不需大型 package）

## 11. Providers / Tools（truthful states，default OFF）

| Provider | State | 說明 |
|---|---|---|
| Qdrant | `ADMITTED_DISABLED` | vector readiness（client 1.19.0 已驗證），default OFF |
| Neo4j | `INSTALL_PROFILE_READY` | graph readiness（driver 6.2.0），default OFF |
| gstack | advisory | 非 final authority |
| openspec | CERTIFIED_ACTIVE_BROWNFIELD | brownfield route |

## 12. Milestone Close / Next Phase

- RP-001 已 freeze 為 **MILESTONE_CLOSED**（identity/lessons/historical references frozen；
  HGK/SQS code 可持續演進）
- 之後真實 SQS 任務照 **normal operational loop**：`execute → test → repair → continue`
- 平台級 invariant defect 才升級 HGK evolution candidate
- Next Phase：`SQS_NORMAL_OPERATIONAL_TEST_REPAIR_ITERATION`
- Non-blocking debt 記錄於 closure record；自然 reseal 時處理

## 13. Known Gaps（non-blocking debt）

- spartoi capability extraction WorkOrders（10 packages，REUSE/ADAPTER-first）——debt
- RBWI external-runtime（live market hours）——TEMP_EXTERNAL（非 blocker）
- research 因子實證、NRTV live、training runs——後續 wave 規劃
- A-3（2026-08-12，docs-only）未關閉上述 spartoi / RBWI external-runtime / research debts——維持 deferred（non-blocking）

## 14. A-3 Operability Delta（2026-08-12）

- **SQS under HGK governance**：canonical root `C:\Projects\Agent_Workspace\SQS-THC`；SQS 是 HGK
  治理下的 Financial Product / Domain Stack，**不是第二 control plane**；HG-KSEOS 為 sole
  governance / normative / WorkOrder / evidence / release plane。
- **Financial truth owner 解析**：金融契約真理 = source-resolved fsdt kernel（`src/kernel/fsdt`）；
  source wins over doc；memory / retrieval 產出不能自我升級為 financial truth。
- **Cold start under HGK**：`README.md`（landing）→ 本 User Guide → `STATUS_VECTOR.json` →
  canonical suite。
- **Hermes orchestration**：Hermes 為受治理 runtime / orchestration plane；Kanban / Swarm 由
  router 依任務自動選（Direct / Kanban / Swarm），非人工硬派。
- **Admission → route**：admitted 任務自動走 Kanban / Swarm route；tracked（受追蹤）實作變更走
  Codex coding route（bounded executor）。
- **Interpreter / environment truth 解析**：repo `.venv-data` venv 的 base interpreter path
  已失效（pyvenv.cfg 指向不存在的 hermes runtime path）；canonical fallback 為 system Python 3.11：
  `C:\Users\user\AppData\Local\Programs\Python\Python311\python.exe`（fresh readback wins）。
- **Canonical suite procedure**：

  ```bash
  PYTHONPATH=src python -m unittest discover -s tests -t .
  ```

  讀 fresh counts：`Ran N tests ... OK`（2026-08-12 實測 211 tests OK）；以當次執行輸出為準，
  不以舊文檔數字代替。
- **LOCAL / PAPER / NO-LIVE-WRITE + safe operational canary**：canary 只走 read-only kernel
  surface：`validate_contract` / `normalize` / `pit_validate` / `compute_value`；無 live write。
- **No-live-write invariant**：`adapters/xq-read-watch.yaml` `watch_only: true` / `write: false`
  / `order_path: HITL_ONLY`；任何寫路徑 fail-closed（ERR_AUTONOMOUS_ORDER_PATH）。
- **Normal operational loop**：`execute → test → repair → continue`；平台級 invariant defect
  才升 HGK evolution candidate，不自行改治理。
- **RP-001 historical boundary**：MILESTONE_CLOSED；歷史里程碑不重開施工（freeze ≠ code freeze）。
- **Next operational use**：`SQS_NORMAL_OPERATIONAL_TEST_REPAIR_ITERATION`。
- **Knowledge binding status**：K1 / KG1 治理 ACTIVE（RP-002 Stage-2 KG1 PASS；SQLite/FTS5 P0 REUSE）；Qdrant `ADMITTED_DISABLED`、
  Neo4j `INSTALL_PROFILE_READY`，皆 default OFF。
- **Production / live claim ceiling**：`LOCAL_PACKAGE_PASS` ≠ production；production_pass
  `NOT_CLAIMED`；live trading NOT_AUTHORIZED。

## 15. RP-002 v2.0 Stage-3 Delta（2026-08-13）

- **3 persistent profiles**（SQP1）：`sqs-orchestrator`（協調 admitted SQS 工作；保留 Financial Truth 所有權；不發 RiskAuthorization/Fabric final acceptance）、`sqs-data-analysis`（源基分析候選；不寫 live broker；不直接 promote 進 Financial Truth）、`sqs-risk`（survival/sizing/capacity/risk fail-closed；不得以多數決改風險權威；不作 Fabric AO / Human Financial Authority）。路徑：`agents/profiles/`。
- **Stack manifest**：`SQS_STACK_MANIFEST.yaml`（RP002-STACK-MANIFEST/2）：persistent_profiles_p0 = 3；execution_modes = [DIRECT, MULTI_PROFILE_DAG, SWARM]；knowledge_namespace 含 `sqs.revoked.*` 排除（E2-BS-001，additive read-exclusion；authority/risk delta NONE）。
- **TW-ICT Financial Runtime Pack**：`SQS/TWICT_RUNTIME_PACK_MANIFEST.yaml`（TWICT-FINANCIAL-RUNTIME-PACK/1，M00..M15，30 文件 doc family）；financial_authority_owner = SQS_OWNER_BOUND_CONTROL_CORPUS。
- **E1/E2/E3**：E1-KD-001（knowledge-governance docs currentness，README L66 + UserGuide L168，Codex repair + replay OK）；E2-BS-001（stack namespace revocation exclusion，fresh-session canary PASS）；E3 = N/A_WITH_SOURCE_LOCATOR（無 acceptance/evaluator/SoD constitution 變更）。
- **R1 與 reducer**：R1_FINAL_RECEIPT prerequisites 全 PASS（SQP1/S1/E1/E2 PASS；E3 N/A；blocking_tt_cr=0；live_broker_writes=0；open_breakglass=0）；child reducer `STAGE3_SQS_PASS_ELIGIBLE_FOR_MASTER_R1_REDUCTION`；master reducer `RP002_LOCAL_ACCEPTANCE_PASS`（REDUCER_RECEIPTS_OBS_CLOSURE.json）。
- **PCIV-F01 closure**：final package manifest 內 E2 selection-card digest 過期（fe824e17→d4f93610）以 superseding receipts 閉合：`evidence/rp002/stage3/gates/FINAL_PACKAGE_MANIFEST_SUPERSEDING.yaml`（999983fd…）+ `E1_E2_EVOLUTION_RECEIPTS_SUPERSEDING.yaml`（b89edb2f…）；accepted 原檔（68867e08/8d8d7f42）byte-identical 保留。
- **外部證據閉合**（EXT-F01..F07）：`evidence/rp002/stage3/closures/`（CLOSURE_EXT-F01..F07 + ACCEPTANCE_OFFICER_RECEIPT + CANARY_RECEIPT）；closure MD `RP002_FABRIC_AUTONOMOUS_SELF_EVOLUTION_EXTERNAL_EVIDENCE_CLOSURE.md`（b50a11b2…）。
- **Canonical suite**：`PYTHONPATH=src python -m unittest discover -s tests -t .`（2026-08-13 實測 231 tests OK；fresh count 為準）。
- **Claim ceiling 不變**：LOCAL/PAPER/NO-LIVE-WRITE；production NOT_CLAIMED；live trading NOT_AUTHORIZED；remote NOT_CLAIMED。

## 16. Daily OHLCV 資料層（2026-08-13, EXTERNAL FINAL ACCEPTED）

### 16.1 資料集身分（DSV-DAILY-2026-08-13-r2）

- **258 檔 TWSE 上市普通股**（TWSE ISIN master 證明，0 上櫃）、**221,349 rows**、2023-01-03 → 2026-08-13。
- 來源：**TWSE 官方 STOCK_DAY**（Yahoo `.TWO` 明示 fallback，0 次使用）；`RAW_UNADJUSTED_ONLY` + 調整相依 consumer **typed BLOCK**。
- 分層：raw immutable parquet（11,352, 逐窗 sha256 receipts）→ core daily parquet → `backtest.duckdb` `daily_bars` → `catalog.sqlite`（DSV 註冊）。
- PIT：five-clocks 合格（`known_at = asof + 1d`；同日前瞻 **BLOCKED**，negative canary PASS）。
- 目錄：`data_plane/`（config/universe v3 258 codes、src/backfill_daily.py + check_daily.py、data/raw/core/metadata）。

### 16.2 驗收與啟用

- 外部最終驗收 r4（2026-08-13）：**PASS / GRANTED**，accepted claim = `DAILY_OHLCV_LOCAL_BACKTEST_DATA_LAYER_PASS`（7/7 promotion conditions、0 blocking findings）。
- 啟用：`data_plane/config/STATUS_VECTOR_DAILY.json`（daily layer **ACTIVE**）+ `provider_profile.yaml` `daily_layer` section（rights RIGHTS-DAILY-2026-08-13-002）。
- WO 鏈：WO-RP2-DAILY-001（建置）→ 002（PIT narrow repair: known_at lookahead 修補）→ 003（scope/clock focused closure: ISIN master TWSE-only 勘誤）→ 004（啟用 + 每日更新），全部 VERIFIED（checker = 獨立 lanes）。
- 證據根：`evidence/rp002/daily-ohlcv/`（EV-DAILY-001..028；master r4 MD `33c12726…`；activation MD `d6f31949…`，三根 mirror byte-identical）。

### 16.3 回測使用

- 資料源：`backtest.duckdb` → `daily_bars`（全 typed：symbol VARCHAR / date DATE / OHLC DOUBLE / volume BIGINT / retrieved_at TIMESTAMPTZ / asof、known_at DATE）。
- **決策 predicate**：bar 可見 iff `known_at <= decision_time`（D 日收盤自 D+1 起可用；同日盤中決策看不到當日收盤）。
- 查詢範例：`SELECT * FROM daily_bars WHERE symbol = '1101' AND "known_at" <= :decision ORDER BY date`（`asof`/`known_at` 為 duckdb 保留字，需引號）。

### 16.4 每日自動更新

- 機制：`backfill_daily.update_incremental()`——抓取近 2 個月 × 258 symbols（TWSE STOCK_DAY），idempotent（receipt+sha 比對）；**有新列才**重建 core/duckdb + 註冊「日期戳新 DSV 版本」（manifest parent lineage 動態自 catalog）；**無新列 = NO_CHANGE**（DSV 原封不動）。
- 排程：Hermes cron `d0d31ffedd07`「SQS Daily TWSE OHLCV Auto-Update」：**每日 20:00 Asia/Taipei**（no_agent；desktop session 排程 tick 存 cron log，手動 `cronjob(action='run')` 才回對話）。
- 驗證：每次更新後自動跑 `check_daily` 11 項（FAIL → alert）；TWSE 瞬時錯誤記入 failures，隔日重試。
- 手動觸發：`C:\Users\user\AppData\Local\Programs\Python\Python311\python.exe C:\Projects\Agent_Workspace\HG-KSEOS\var\pciv\run_daily_update.py`（dry-run 2026-08-13 實測 NO_CHANGE + 11/11 PASS）。

### 16.5 Claim 邊界（本層）

- 本層 = **local backtest data layer** PASS；**非**策略獲利 / IS-OOS / TCA / production / live / broker / remote。
- TPEx 擴張、adjusted series、換 provider = **新 ChangeSet**（新 WO + owner approval），不得沿用本 PASS 靜默擴張。
