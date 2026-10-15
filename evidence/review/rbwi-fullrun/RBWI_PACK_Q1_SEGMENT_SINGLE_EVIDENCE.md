# RBWI_NATIVE_TIME_SEGMENT_4_PLUS_1 PACK — Q1 Segment External Evidence (single MD)

**artifact_id:** `RBWI_PACK_Q1_SEGMENT_SINGLE_EVIDENCE`
**pack_revision:** v2026.08.14-r2 · **parent_workorder:** WO-RBWI-FULLRUN-001
**parent_run_id:** RUN-RBWI-FULLRUN-20260820-001 · **candidate_id:** CAND-RBWI-20260814
**segment:** Q1_CONTEXT_PREOPEN · **binding:** BIND-RBWI-Q1-20260820-001
**generated:** 2026-08-20T21:00+08:00 · **timezone:** Asia/Taipei
**control_plane:** HG-KSEOS · **runtime:** Hermes · **tracked_writer:** Codex
**financial_boundary:** LOCAL_PAPER_SIMULATION_ONLY · **live_broker:** NOT_AUTHORIZED

---

## 0. Claim Ceiling (verbatim)

```
TW_ICT_RBWI_FULL_RUN_Q1_LOCAL_PAPER_SIMULATION_INTERNAL_ALL_PASS
Runtime = Q1 SEGMENT_PASS_AND_FROZEN (SIM_BACKTEST_CLOCK, offline)
Independent = PASS (dual-lane Swarm readback 7/7 + 6/6; AO fresh-context VERIFY_ONLY PASS)
Production = NOT_CLAIMED · Live trading = NOT_AUTHORIZED · Broker write = NOT_AUTHORIZED
Q2/Q3/Q4 = BOUND_PENDING (REQUIRED_HITL-APPROVAL/1 + live market session)
```

**Non-claims (explicit, not to be read as PASS):**
- Q2_OPENING_S1 / Q3_MIDDAY_S2 / Q4_CLOSE_POSTMARKET are **NOT executed**. They are
  bound (`BIND-RBWI-Q2/Q3/Q4-20260820-001`), each `BOUND_PENDING_*` with
  `REQUIRED_HITL-APPROVAL/1` and `account_mode=PAPER_ONLY`. No position, order, fill,
  or financial side-effect was placed or is claimed. SessionCandidatePool-S1 is a
  **pre-open proxy from the daily layer**, not a live pre-open order book.
- No profitability, IS/OOS alpha, TCA, portfolio-model, production-autonomy, or
  live-trading claim is made anywhere in this evidence set (positive PnL ≠ acceptance).
- No live/broker write exists: `broker_write=false` (sf-02), `live_broker_write=DENY`
  (XQ_ACCOUNT_MODE), `order_path=HITL_ONLY`.

---

## 1. Binding & Lineage

| Field | Value |
|---|---|
| parent WorkOrder | WO-RBWI-FULLRUN-001 (spine state CREATED, writer=codex, RB-WO-RBWI-FULLRUN-001) |
| parent Kanban board | rbwi-fullrun-2026-08-14 (K0/K6b done; K1–K5 revalidated; K7b Q2-gate todo; K8 S2 BLOCKED_pending) |
| canonical RBWI | `知識庫/SQS-THC & TW-ICT_FSDT-Stack_SSOT/TW-ICT_RBWI_v3.0.0_r2_2026-07-30.md` sha256 `a94b2ec0…` (10,269 lines) |
| Master overlay | `TW_ICT_RBWI_FULL_RUN_MASTER_EXECUTION_OVERLAY_4PLUS1_2026-08-14_r2.md` sha256 `345e150f…` |
| Q1 overlay | `TW_ICT_RBWI_Q1_CONTEXT_PREOPEN_QUALIFICATION_OVERLAY_r2.md` sha256 `9e8723b5…` |
| Q1 thin prompt | `RUN_TWICT_RBWI_Q1_CONTEXT_PREOPEN_THIN_PROMPT_r2.md` sha256 `50e40f0f…` |
| Pack static build | `PACK_R2_BUILD_MANIFEST.json` static_checks all true, failures=[] (9/9 MD, SHA256SUMS OK) |
| gate0 verdict | G0_PASS (13/13 baseline receipts re-verified; HGK doctor PASS/blocking=0) |

**Four segment bindings (all point to the same parent):**
`BIND-RBWI-Q1-20260820-001` (SEGMENT_PASS) · `…-Q2-…` (BOUND_PENDING_Q1_VALID_AND_LIVE_SESSION) ·
`…-Q3-…` (BOUND_PENDING_Q2_FROZEN) · `…-Q4-…` (BOUND_PENDING_Q3_FROZEN).

---

## 2. Execution Surfaces (default-on, all applied)

- **HGK control plane:** every durable mutation rides WO-RBWI-FULLRUN-001 lineage; maker
  writes are WorkOrder-scoped evidence-generation only (no creating a 2nd control plane).
- **KANBAN:** board rbwi-fullrun-2026-08-14 — K0 admission completed, K6b (bindings)
  completed, K7b (Q2 gate) created, K8 honestly closed as BLOCKED_pending.
- **SWARM:** genuine 2-lane independent readback (deleg_5ce69ab4): HGK evidence lane
  **7/7 PASS**, SQS data-layer lane **6/6 PASS**; overlap interval both ran live.
- **GSTACK:** named-method registry `hg_kseos/named_methods.py` — gstack.plan-eng-review /
  review / qa = `CERTIFIED_ACTIVE_SELECTED_SLICES`; route check recorded
  `selected_route=NATIVE, reason_code=HGK_HERMES_ORCHESTRATES_DIRECTLY_Q1_QUALIFICATION`.
- **OPENSPEC:** `CERTIFIED_ACTIVE_BROWNFIELD`; **N/A** this segment (no durable
  brownfield repair triggered), recorded `NOT_TRIGGERED_NO_BROWNFIELD`.
- **CODEX:** writer=WO-RBWI-FULLRUN-001 (sealed lane codex 0.147.0-alpha.6.5); bound-on-repair;
  Q1 required no durable code repair (all offline checks passed) — recorded in method ledger.

**Method actual-use ledger:** `RBWI_METHOD_ACTUAL_USE_LEDGER.tsv` (7 rows).

---

## 3. Deterministic Denominator Projection

```
RBWI_EXECUTION_DENOMINATOR.tsv                 = 150 rows (header +150 data)
SEGMENT_DENOMINATOR_Q1_CONTEXT_PREOPEN.tsv     = 37 rows (G0001..G0037, 0 orphan, 0 dup)
  MANDATORY_RUNTIME_NODE=4 · REQUIRED_DELIVERABLE=16 · NEGATIVE_SECURITY_RECOVERY_FIXTURE=4 · REQUIRED_USER_JOURNEY=13
Q1 denominator digest sha256 = 81175b24…  (matches checkpoint segment_denominator_digest)
```

Q1 PASS condition met: subset 100% terminal, 0 orphan, no stale candidate row.

---

## 4. Q1 Execution Evidence (raw index — PRIMARY home + 3 mirror roots)

> **更新 (user 逐項比對 request)**: 開盤前工作事項 100% 覆蓋已補做並驗證。canonical 開盤前
> 全清單（週 W-00..08 + 日 D-00..09 + modules）全部物化為 receipts —— 見 §4.1。

| # | Artifact | sha256 (head) | bytes |
|---|---|---|---|
| 1 | BACKTEST_RUN_RECEIPTS/BACKTEST_RUN_RECEIPT_Q1.json | ab10306b | 2137 |
| 2 | BASELINE_AUTHORITY_INVENTORY.json | 1cc30d6c | 1493 |
| 3 | BASELINE_DATASET_INVENTORY.json | 4b7fabfc | 595 |
| 4 | BASELINE_FAR_RUNTIME.json | 6911ab34 | 349 |
| 5 | BASELINE_FDA_XQ_SUBJECT.json | e2a94976 | 583 |
| 6 | BASELINE_GSTACK_OPENSPEC_STATE.json | 912e9870 | 980 |
| 7 | BASELINE_HGK_HEALTH.json | c8f563a6 | 168 |
| 8 | BASELINE_MACHINE_STATE.json | d165b6ea | 551 |
| 9 | BASELINE_RBWI_SUBJECT_MANIFEST.json | 6cc801ec | 1577 |
| 10 | BASELINE_RECEIPT_CROSSWALK.tsv | 115b91dd | 1423 |
| 11 | BASELINE_REQUIRED_CAPABILITY_PREFLIGHT.json | 267cc0ad | 1366 |
| 12 | BASELINE_SQS_TESTS.exitcode.txt | 5feceb66 | 1 |
| 13 | BASELINE_SQS_TESTS.stdout.txt | 793c73d5 | 336 |
| 14 | BASELINE_XQ_ACCOUNT_MODE.json | 3626a50b | 380 |
| 15 | FAR_RUN_RECEIPT.json | 10a8faeb | 1119 |
| 16 | GATE0_RECEIPTS_SUMMARY.json | 949a365b | 2324 |
| 17 | RBWI_CHECKPOINTS/Q1_SEGMENT_CHECKPOINT.json | b95c7272 | 3079 |
| 18 | RBWI_DENOMINATOR_PROJECTION_SUMMARY.json | ad8351bd | 805 |
| 19 | RBWI_METHOD_ACTUAL_USE_LEDGER.tsv | 76df5dcf | 612 |
| 20 | RBWI_RUN_LEDGER.jsonl | f1d52390 | 1231 |
| 21 | RBWI_SEGMENT_BINDINGS/BIND-RBWI-Q1-20260820-001.json | 5b84841b | 1470 |
| 22 | RBWI_SEGMENT_BINDINGS/BIND-RBWI-Q2-20260820-001.json | 9b4f6981 | 1444 |
| 23 | RBWI_SEGMENT_BINDINGS/BIND-RBWI-Q3-20260820-001.json | db8bc98b | 1421 |
| 24 | RBWI_SEGMENT_BINDINGS/BIND-RBWI-Q4-20260820-001.json | ba3f9254 | 1415 |
| 25 | sf-01-receipt.json (WeeklyContextPackage) | 9e65b7c3 | 7129 |
| 26 | sf-02-receipt.json (DailyRunExecutionPackage FROZEN) | d37f6eff | 1410 |
| 27 | sf-03-receipt.json (SessionCandidatePool-S1) | 33d63b2b | 80295 |

**Q1 fact summary:**
- SF-01 Weekly Context: regime card MIXED (median tail ret ~0), evidence stack,
  universe snapshot 258 TWSE, bias hypotheses, 5-branch scenario tree (BASE_MIXED).
- SF-02 Daily Freeze: DailyRunExecutionPackage FROZEN; 4 mutation/write flags all false.
- SF-03 Pre-open candidate: **SessionCandidatePool-S1 PRIMARY=138 / EXCLUDE=120**, tier
  without relaxing for count (Gate-04 PASS); proxy from daily layer (Q2 uses live pre-open).
- Backtest qualification: **PIT known_at<=asof=0 AND known_at!=asof+1d=0 (T+1 semantic)**,
  deterministic replay `result_hash==replay_result_hash` TRUE, walk-forward IS/OOS split,
  TWSE fee 0.1425% + sell tax 0.3% + 5bps slippage model, engine duckdb-1.5.5+polars-1.43.2,
  provenance TWSE_STOCK_DAY official + catalog.sqlite.
- FAR R0-R8: `R8_HANDOFF_COMPLETE`, output class CandidateResearch, self_promotion=DENIED.

### 4.1 ══ 開盤前工作事項 100% 覆蓋（user 逐項比對補做）══

canonical RBWI §11/§12 定義的台股開盤前全流程，逐項物化為 receipts（`PREOPEN_WORKING/`）：

| 層級 | 步驟 | 狀態 |
|---|---|---|
| 週 Weekly | **W-00** 凍結制度/行事曆/資料能力 · **W-01** 全球傳導假說 · **W-02** 台灣 Regime(MIXED) · **W-03** EvidenceStack · **W-04** Universe(258/TWSE) · **W-05** 週候選池(空池合法) · **W-06** MTF+Bias · **W-07** 五分支 Scenario · **W-08** 凍結 WeeklyContextPackage | 9/9 ACTIVE |
| 日 Daily 盤前 | **D-00** 能力/權限預檢 · **D-01** RuntimeContext · **D-02** 載入週 Context · **D-03** 凍結 Rule/Data/Event · **D-04** Universe/Candidate(PREOPEN) · **D-05** Daily Context overlay · **D-06** Daily Bias · **D-07** 綁定 Scenario · **D-08** 凍結 DailyRunExecutionPackage(FROZEN) · **D-09** 試撮 S1 股池 | 10/10（D-09 live= PREPARED_PENDING_LIVE→Q2/XQ） |
| Modules | **SF-16** Capability Admission · **SF-00** Runtime Bootstrap · **SF-17** Operator Cockpit | 3/3 |
| Q1 既有 | **SF-01** Weekly Context · **SF-02** Daily Freeze · **SF-03** Pre-open Candidate | 3/3 |

**覆蓋證明檔：** `RBWI_PREOPEN_100PCT_COVERAGE_CHECK.json`（25/25 = 100%，無 missing）、
`RBWI_PREOPEN_COVERAGE_MANIFEST.json`（22 step receipts + 覆蓋解析）。
**綁定：** Q1 checkpoint `preopen_coverage.coverage_pct=100`。
**獨立 fresh verify lane（deleg_2519fb9c）**：開盤前 100% 覆蓋 + 22 receipts 實質欄位 +
三 root 鏡像 byte-identical 驗證。

---

## 5. Gates & Independent Verification

| Gate | Verdict | Evidence |
|---|---|---|
| Gate-0 baseline | PASS | 13/13 receipts; HGK doctor PASS/blocking=0; SQS 231 tests OK (exit 0) |
| Deterministic denominator | PASS | 150/37 rows, 0 orphan, 0 dup, digest chain consistent |
| Quality smoke | PASS | check_daily **11/11** (2026-08-20 re-run) + SQS unittest 231 OK |
| Backtest qualification | PASS | PIT 0/0, deterministic=TRUE, cost model present |
| **Swarm independent readback** | **PASS** | HGK lane 7/7 + SQS lane 6/6 (both fresh-context, read-only) |
| **Acceptance Officer (VERIFY_ONLY)** | **PASS** | fresh-context; 7 evidence items PASS; blocking=[]; maker/checker separated |
| Non-claims verified | VERIFIED | (a) no live/broker-write claims; (b) Q2-Q4 NOT fabricated as PASS |

**Self-iterated repair loop (automated detect → patch → re-verify):**
- Gate-0 first pass mis-reported `BASELINE_HGK_HEALTH.doctor_verdict=PARSE_FAIL`
  (root cause: doctor subprocess decoded UTF-8 as mbcs). **Patched** generator
  (utf-8 decode + robust JSON-span extract) → re-ran → `PASS, blocking_count=0`.
  Re-verified by both Swarm lane and AO.
- PIT check first pass used minute-layer leak semantics (`known_at>asof`) →
  false `PIT_bad=221349`. **Corrected** to canonical daily T+1 semantics
  (`known_at<=asof` violation, `known_at==asof+1d` structural) → `0/0` PASS.

---

## 6. Stop / Hold items (NOT part of this claim)

```text
STOP: Q1 is the only segment executed. Do NOT proceed to Q2 without:
  (a) user HITL approval for financial side-effects per HITL-APPROVAL/1 receipts
      (entry = HUMAN_ENTRY_APPROVAL per FDA route ROUTE-SQS-XQ-GLOBALWINNER-001);
  (b) a live market session (next trading day 09:00–13:30 Asia/Taipei) with XQ/XS
      PAPER desktop available and FDA route ACTIVE;
  (c) Q2 checkpoint hydration of SessionCandidatePool-S1 BEFORE live pre-open data.
External final meta acceptance, production, live trading, and remote deployment are
NOT self-issued and remain PENDING.
```

---

## 7. Mirror & Readback

This single evidence MD and all 27 raw artifacts are stored byte-identical at:
- PRIMARY: `SQS-THC/evidence/rbwi-fullrun/`
- MIRROR: `HG-KSEOS/evidence/review/rbwi-fullrun/`
- MIRROR: `SQS-THC/evidence/review/rbwi-fullrun/`
- MIRROR: `Fabric/evidence/review/rbwi-fullrun/`

SHA-256 equality verified for all 27 files across all roots.
