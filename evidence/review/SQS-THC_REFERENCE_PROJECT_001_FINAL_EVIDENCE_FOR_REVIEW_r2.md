# SQS-THC & TW-ICT_FSDT-Stack — Final Evidence for Review r2 (WAVE3 closure)

> Generated: 2026-08-11T03:05:00+08:00
> Changeset: `RP001-WAVE3-SHIOAJI-DATA-BACKTEST-FINAL-CLOSURE-001` (CONTINUATION)
> Prior frozen evidence (read-only lineage, DO NOT rewrite):
> `evidence/review/SQS-THC_REFERENCE_PROJECT_001_FINAL_EVIDENCE_FOR_REVIEW.md`
> (sha256 `b774cc2540ab9b6a…`, sections A–S)
> This r2 supersedes it as the current single handoff MD.

## A. Machine Header

```yaml
reference_project_id: HGK-REFERENCE-PROJECT-001
changeset_id: RP001-WAVE3-SHIOAJI-DATA-BACKTEST-FINAL-CLOSURE-001
changeset_class: CONTINUATION
execution_mode: HIGH_AUTONOMY_RESUMABLE_FAIL_CLOSED
hgk_root: C:\Projects\Agent_Workspace\HG-KSEOS
sqs_root: C:\Projects\Agent_Workspace\SQS-THC (CANONICAL_PRODUCT_ROOT)
shioaji_workspace: C:\Projects\Agent_Workspace\SQS-THC\實作執行\Shioaji API (PROVIDER_RUNTIME_SOURCE_AND_PILOT)
orchestrator: HERMES
coding_executor: CODEX
topology_policy: HG_KSEOS_DETERMINISTIC_ADMISSION
highest_allowed_claim: SQS-THC_TW-ICT_FSDT_STACK_LOCAL_DELIVERY_PASS
production: NOT_CLAIMED
live_trading: NOT_AUTHORIZED
remote_deployment: NOT_CLAIMED
```

## B. Status / Verdict

```text
STATUS: PARTIAL / RESUMABLE
RBWI_REQUIRED_COMPOSITE: TEMP_CLOSED (external market-time lane only;
       everything required for LOCAL_DELIVERY is terminal)
OPEN_EDGE: RBWI_EXTERNAL_MARKET_TEMPORAL (live market-hour lane)
CLASS: TEMP_EXTERNAL
SOURCE_LOCATOR: TW-ICT_RBWI_v3.0.0_r2 (market-time operator lane) — genuinely
       time-bound; not required for local-delivery claim per G0 D4 adjudication
RESUME_CONDITION: market-hour window + operator session (auto-resumable via
       authorized continuation mechanism, no new user prompt required)
NEXT_WORKORDER: none AUTO_LOCAL remains; sweep = 0
HUMAN_ACTION_IF_ANY: none now
```

## C. HGK Baseline (G0 thin controls)

| Item | Value |
|---|---|
| HEAD | 60820e5 (G0: admit_requirement / completion_sweep / rbwi_composite / denominator guard predicates) |
| Suite | 245/245 OK |
| Acceptance | 161/161 `HG-KSEOS_LOCAL_DELIVERY_PASS - EXTERNAL FINAL ACCEPTED` |
| Coverage reducer | PASS (reasons=[]) |
| G0 defects closed | D1 AUTO_CONTINUATION (completion_sweep + auto-local self-continuation) · D2 DYNAMIC_DENOMINATOR (admit_requirement → Requirement→TaskSpec→WorkOrder) · D3 COMPLETION_SWEEP (classification auto_local/blocked_hitl/temp_external/non_blocking_debt) · D4 RBWI_COMPOSITE (cannot PASS above required child; TEMP_CLOSED semantics) |
| Isolated repair | worktree `codex/rp001-wave3-g0-repair` → cherry-picked to main (single writer) |

## D. Shioaji Provider (G1)

- Workspace inventory: 3 assets (consent PDF 217,792B / key txt 119B / pfx 2,752B) — sha256 recorded, contents never exposed
- SDK: shioaji 1.7.2 (official-probed current), polars 1.43.2, duckdb 1.5.5 in `.venv-data`
- **SJ_DATA_READ_QUALIFIED (exit 0)**: real login (simulation=True data lane), contracts resolvable, read-only kbars probe 797 rows
- Credential boundary: API key+secret loaded at runtime from local key file; pfx (trading cert) NEVER loaded; key file + workspace gitignored; no credential in code/log/evidence
- Permissions: Market/Data allowed; Account/Trading/Production denied (provider-side SJ_DATA_READ profile)

## E. Historical Acquisition (G2)

| Metric | Value |
|---|---|
| Universe | 50 symbols (TWSE large-caps + TPEx exemplars), 49 with data |
| Window | 2025-08-11 .. 2026-08-10 (12 months) |
| Bars | **2,793,223** 1-minute rows |
| Raw artifacts | 637 window parquet (29-day chunks, idempotent, sha256 receipts) |
| Failures | 1: `2311:NO_CONTRACT` (honest, no silent drop) |
| Pacing | 0.30s request gap + 3-attempt bounded retry; quota evidence in receipts journal |

## F. Backtest Database (G2/G3)

- Raw (immutable provider parquet) → Core minute parquet (49 files, zstd) → DuckDB `backtest.duckdb` (2,793,223 rows) → SQLite `catalog.sqlite`
- **DatasetVersion `DSV-2026-08-11-r1`**: manifest sha256 `15454c670182a4f6f6147af0b3a7d11df2d4a917baf73cdf2c5cf128a33289c7`, lineage parent = acquisition receipts journal, PIT fields asof/known_at/event_time
- **G3 qualification ALL PASS (10/10)**: pit_no_lookahead=0 · monotonic_clock=0 · ohlc_invariants=0 · deterministic_replay=1dbbfd80 · is_oos=1,418,364/1,374,859 · gap_report (min 235 days/symbol) · no_duplicates=0 · dataset_version_bound · leakage_guard_fails_closed=0
- Independent re-run: **G3_BACKTEST_DB_QUALIFIED (exit 0)**

## G. Data Quality (G4, Codex bounded read-heavy)

- Report: `data_plane/reports/data_quality_report.md` (21,185B, commit 08bcf94)
- 47/49 symbols cover all 242 trading days; gaps: 1101 (−1d), 2327 (−7d corporate-action suspension)
- Session reality: max 266 bars/session (09:01–13:25+13:30), not 300 — TWSE auction structure
- OHLC: 0 violations; implied price Amount/(Volume×1000) ≈ Close (3.56% max) → **Volume in board lots (張)**
- 0 duplicates raw=core=duckdb=manifest; PIT clean
- 2 corporate-action discontinuities (2327 −74.0% 2025-08-25, 2105 −13.0% ex-div) — consumer must handle unadjusted prices
- Safe-use conditions documented (no-trade minutes, auction prints, ×1000 scaling)

## H. Multi-Agent Runtime (G4, deterministic admission)

- Topology: KANBAN_SINGLE + CODEX_BOUNDED (atomic DB work = DIRECT per policy; no forced swarm)
- Kanban: WAVE3 card `t_c48d3de0` (board sqs-thc-ref-001) with G1→G2→G3→G5 dependency chain
- Codex bounded worker: G4 data-quality analysis (read-heavy subagent-style card), commit 08bcf94
- Negative invariants: double_writer=0 · second_orchestrator=0 · unauthorized_effect=0 · duplicate_effect=0 · lost_handoff=0 · secret_cross_profile=0 · release_authority_escape=0 · unbounded_recursion=0

## I. RBWI Composite (G5)

- Coverage matrix (7 rows): `evidence/review/SQS_CSB_RBWI_COMPOSITE_MATRIX.json` — RBWI step → SQS subsystem → capability/tool → permission → runtime evidence → negative/fallback → result
- Composite via HGK G0 `rbwi_composite`: local_paper=PASS · external_market=**TEMP_CLOSED** · tool_coverage=PASS · user_journey=PASS · negative_degraded=PASS · replay=PASS
- **RBWI_REQUIRED_COMPOSITE = TEMP_CLOSED** (external market-time lane only; cannot PASS above required child — G0 D4 semantics)
- Runs on the NEW final candidate (canonical root + data_plane), not the stale pre-Shioaji candidate

## J. Spartoi / Provider / Tool / Integration Edges

- Spartoi crosswalk: `實作執行/SQS_SPARTOI_INTEGRATION_CROSSWALK.json` (1,798 files / 13 authority docs / 10 capabilities REUSE/ADAPTER-first)
- Spartoi remaining required integration: **0** (V1 local-delivery scope; extraction edges admitted only when required — completion sweep = 0 AUTO_LOCAL)
- Provider admission: Shioaji QUALIFIED (G1), FinMind CONDITIONAL_NOT_REQUIRED, XQ SOURCE_VALID_NOT_APPLICABLE
- Required-active capabilities: 8/8 bound (named-method ACTIVE scope)

## K. Regression / Security / Negative

- SQS: **211/211 OK** (kernel + 15 TaskSpec WO tests, all positive/negative/edge fail-closed)
- HGK: **245/245 OK**
- G3 negative fixtures: leakage guard fail-closed (0 cross-bar leaks), no-duplicate, no-lookahead
- G4 negative: corporate-action discontinuities identified (not hidden), missing-minute no-trade semantics documented
- Credential hygiene: no secret in code/log/evidence; Shioaji workspace gitignored

## L. Independent Acceptance

- G1: SJ_DATA_READ_QUALIFIED (real provider, not mock)
- G3: independent fresh subprocess re-run PASS (G3_INDEPENDENT_RERUN)
- HGK: acceptance 161/161 + coverage reducer PASS (canonical)
- Wave-1/2: 15 WO INDEPENDENT_CASE_PASS receipts (unchanged lineage)

## M. Package / Readback

- HGK reseal: package `69162fcb…` / 420 payload / exact_set PASS (baseline unchanged by G0 — source-only thin patch, no package content change)
- SQS TS-014 artifacts: `release/manifest/MANIFEST.json`, `release/checksums/CHECKSUMS.sha256`, `scripts/validate-package.py` (PACKAGE_READBACK_OK)
- Data plane: DatasetVersion manifest sha256 `15454c6701…` + catalog-bound

## N. Rollback

- Per-WO git commits; G0 isolated worktree (`codex/rp001-wave3-g0-repair`) for HGK patch rollback
- Data plane: raw parquet immutable + receipts journal → rebuildable from provider (idempotent backfill)
- validator fail-closed (ERR_PACKAGE_READBACK_MISMATCH)

## O. Blocking TT / CR

- HGK blocking TT = 0
- Open CR: 0 release-blocking; corporate-action handling documented as consumer obligation (data-plane CR candidate, non-blocking)

## P. Completion Sweep (G0 D3, terminal)

```json
{"auto_local": [], "blocked_hitl": [], "temp_external": ["RBWI_EXTERNAL_MARKET_TEMPORAL"],
 "non_blocking_debt": [], "open_total": 1, "sweepable": false}
```

## Q. Scope Guard (§9)

```text
required_requirements_open = 0
required_workorders_open = 0
required_acceptances_open = 0
required_active_capabilities_open = 0
required_user_journeys_open = 0
required_deliverables_open = 0
required_spartoi_integration_open = 0
required_shioaji_historical_data_open = 0
required_backtest_database_open = 0
required_provider_data_acceptance_open = 0
required_rbwi_composite_open = 1 (TEMP_CLOSED: external market-time lane)
blocking_tt = 0
independent_full_project_acceptance = per-WO + G1/G3 PASS; composite = TEMP_CLOSED
final_package_readback = PASS
```

## R. Final Output

```text
STATUS: PARTIAL / RESUMABLE
PROJECT_LEVEL_LOCAL_DELIVERY_PASS: FORBIDDEN (RBWI_EXTERNAL_MARKET_TEMPORAL open)
OPEN_EDGE: RBWI_EXTERNAL_MARKET_TEMPORAL
CLASS: TEMP_EXTERNAL (market-hour lane; NOT required for local-delivery)
SOURCE_LOCATOR: TW-ICT_RBWI_v3.0.0_r2 §6.6 market-time operator lane
CURRENT_EVIDENCE: evidence/review/SQS_CSB_RBWI_COMPOSITE_MATRIX.json
CHECKPOINT: SQS-THC_CHECKPOINT_WAVE3.json
RESUME_CONDITION: market-hour window + operator session; auto-resume via
       authorized continuation (no new user prompt — G0 D1 AUTO_CONTINUATION)
NEXT_WORKORDER: none AUTO_LOCAL
HUMAN_ACTION_IF_ANY: none now
PRODUCTION: NOT_CLAIMED
LIVE_TRADING: NOT_AUTHORIZED
```

---
*End of r2 evidence envelope. Re-run: `.venv-data/Scripts/python.exe data_plane/src/g1_shioaji_qualify.py`,
`data_plane/src/backfill_kbars.py`, `data_plane/src/build_backtest_db.py`,
`data_plane/src/qualify_backtest_db.py`, `data_plane/src/g3_g5_rbwi_composite.py`,
and SQS full suite (PYTHONPATH=src python -m unittest discover -s tests -t .)
to independently re-derive. HG-KSEOS canonical reducers remain final authority.*
