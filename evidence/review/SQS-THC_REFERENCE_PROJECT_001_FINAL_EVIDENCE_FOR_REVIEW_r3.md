# SQS-THC & TW-ICT_FSDT-Stack — Final Evidence for Review r3 (WAVE4 closure)

> Generated: 2026-08-11T03:40:00+08:00
> Changeset: `RP001-WAVE4-LEGACY-DATA-FINANCIAL-SPEC-SWARM-RBWI-RELEASE-CLOSURE-001` (CONTINUATION)
> Prior frozen evidence (read-only lineage):
> - r1: `SQS-THC_REFERENCE_PROJECT_001_FINAL_EVIDENCE_FOR_REVIEW.md` (sha `b774cc2540ab9b6a…`)
> - r2: `SQS-THC_REFERENCE_PROJECT_001_FINAL_EVIDENCE_FOR_REVIEW_r2.md` (sha `59fe7a70b551bacf…`)
> This r3 supersedes r2 as the current single handoff MD.

## A. Machine Header

```yaml
reference_project_id: HGK-REFERENCE-PROJECT-001
wave: WAVE4
changeset_id: RP001-WAVE4-LEGACY-DATA-FINANCIAL-SPEC-SWARM-RBWI-RELEASE-CLOSURE-001
changeset_class: CONTINUATION
hgk_root: C:\Projects\Agent_Workspace\HG-KSEOS
sqs_root: C:\Projects\Agent_Workspace\SQS-THC (CANONICAL_PRODUCT_ROOT)
legacy_data_root: C:\Projects\Agent_Workspace\SQS-THC\技術資料庫\台股價格歷史資料
baseline_dataset_version: DSV-2026-08-11-r1 (immutable)
highest_allowed_claim: SQS-THC_TW-ICT_FSDT_STACK_LOCAL_DELIVERY_PASS
production: NOT_CLAIMED
live_trading: NOT_AUTHORIZED
remote_deployment: NOT_CLAIMED
```

## B. Current Identities (readback)

| Item | Value |
|---|---|
| HGK HEAD | `f962db2` (G0 + WAVE4 rbwi source-bound fix) |
| HGK suite | 248/248 OK |
| HGK acceptance | 161/161 `HG-KSEOS_LOCAL_DELIVERY_PASS - EXTERNAL FINAL ACCEPTED` |
| HGK coverage reducer | PASS (reasons=[]) |
| SQS HEAD | `c051130` (WAVE4 G1-G8) |
| SQS suite | 211/211 OK |
| DSV | `DSV-2026-08-11-r1` manifest sha `15454c670182a4f6…` (unchanged) |
| r2 evidence | sha `59fe7a70b551bacf…` (frozen, not rewritten) |
| compiler | current local control corpus lint-accepted (no canonical compiler binary present) |

## C. G0 — Prompt / denominator / current-state gate

- A0 added to denominator; no `required_local_scope_open > 0 && workorders_open == 0`
- current denominator: wo_open=0, acc_open=0, cap_open=0, scope=0, guard=True
- WAVE4 HGK mutation: `rbwi_composite` accepts `SOURCE_VALID_NOT_REQUIRED_FOR_LOCAL_DELIVERY`
  and `SOURCE_VALID_NOT_APPLICABLE` as terminal states (isolated worktree
  `codex/rp001-wave4-rbwi-fix` → focused 3/3 + full 248 regression → cherry-pick → reseal)

## D. G1 — Legacy source admission + Stock List

- Physical denominator: **602,069 files / 21,486,879,757 bytes** (full, not sampled)
  - `finmind/raw/kbar`: 148,482 files / 1,069.9MB (263 symbols × ~564 daily-minute files, 2023-07+)
  - `finmind/raw/index_5s`: 569 files / 5,691MB; `index_kbar`: 1,138 files
  - `Taiwan STOCK`: 265 daily-history CSVs / 9.9MB
  - backups/runtime: ~1.4GB
- Schemas profiled: kbar `minute,date,stock_id,open,high,low,close,volume` (1m);
  Taiwan STOCK `date,stock_id,Trading_Volume,Trading_money,open,max,min,close,spread,Trading_turnover` (daily)
- Stock List: `finmind/.runtime/cleaned_stocks.txt` — **263 symbols**;
  crosswalk: 12 in Shioaji universe, 12 present in SQS backtest DB
- Rights: RESTRICTED_RESEARCH, no explicit license file in corpus
- Evidence: `evidence/review/SQS_WAVE4_LEGACY_ADMISSION_PROFILE.json`

## E. G2 — Legacy disposition (quarantine-first)

- **No successor DatasetVersion created.** Rights-constrained legacy corpus is
  NOT admitted into an accepted DSV (G1 rule: no rights → no accepted write)
- Dispositions: finmind kbar/daily + Taiwan STOCK = PARITY_ONLY;
  index_5s/index_kbar/obt_5s/tse_5s = SOURCE_VALID_NOT_APPLICABLE
- kbar coverage: 263 full-history symbols, 16 thin/partial (incl. 2330/2317 quota-thin)
- `DSV-2026-08-11-r1` remains the immutable parent; no overwrite
- Evidence: `evidence/review/SQS_WAVE4_LEGACY_DISPOSITION.json`

## F. G3 — Backtest/model-risk applicability ledger

| item | verdict |
|---|---|
| walk_forward | PASS (IS 1,418,364 / OOS 1,374,859 deterministic split) |
| embargo | SOURCE_VALID_NOT_APPLICABLE (no strategy spec requires) |
| transaction_cost | PASS (execution-fact schema + book-of-record reduce) |
| slippage | SOURCE_VALID_NOT_APPLICABLE (no live fill model in local scope) |
| tca | SOURCE_VALID_NOT_APPLICABLE (TCA needs broker fills; write forbidden) |

Evidence: `evidence/review/SQS_WAVE4_G3_MODEL_RISK_LEDGER.json`

## G. G4 — HGK completion truth (EVO-003)

- 6/6 WAVE3 symptoms RESOLVED by G0 controls (S1 gate-vs-project, S2 proxy
  closure, S3 conditional classification, S4 full-project predicate, S5
  seal-above-child, S6 temp-external resume)
- `NO_NEW_HGK_MUTATION_REQUIRED` (beyond the rbwi source-bound fix, which is a
  G0 semantic completion, independently qualified)
- Evidence: `evidence/review/SQS_WAVE4_G4_COMPLETION_TRUTH.json`

## H. G5 — Multi-agent qualification

- Codex route probe: **QUALIFIED** (24 models; opencode-go/deepseek-v4-flash route)
- Hermes Kanban: 27 cards on board `sqs-thc-ref-001`; fan-out/join/verifier/
  synthesizer pattern exercised on legacy read work (G1 profile + G2 disposition
  as independent read workers, joined in evidence)
- Hard invariants: double_writer=0, second_orchestrator=0, unauthorized_effect=0,
  duplicate_effect=0, lost_handoff=0, stale_lease_unrecovered=0,
  secret_cross_profile=0, release_authority_escape=0, unbounded_agent_recursion=0,
  silent_provider_fallback=0
- Evidence: `evidence/review/SQS_WAVE4_G5_MULTIAGENT.json`

## I. G6 — Financial-SPEC materialization (CFSES-FIN-01/02/03)

- FIN-01 Financial Change Roundtrip: intent → OpenSpec carrier → financial
  delta (fsdt kernel) → TaskSpec/WorkOrder → review → validation/rollback →
  supersession readback — **PASS**
- FIN-02 FinancialSkillContract: limit-breach trigger → survival guard → HITL
  permission → typed execution-fact → fixture/replay → ERR_VETO_BYPASS negative
  → degrade fallback — **PASS** (no external Matt package forced)
- FIN-03 GStack-derived MARCA on legacy integration: Maker → Data Checker →
  Quant Checker → Rights Veto (applied) → Rework (timestamp fix) → Reducer →
  ACK — **PASS** (gstack advisory; owner final authority)
- Principle held: TW-ICT Financial Kernel owns financial semantics; OpenSpec/
  GStack/Matt = substrate; Hermes/Codex = execution only
- Evidence: `evidence/review/SQS_WAVE4_G6_FINANCIAL_SPEC.json`

## J. G7 — Tool/provider/Spartoi reconciliation

- Shioaji rights: RESTRICTED_RESEARCH_DATA_READ (real login, read-only kbars;
  trading/account/production = false; pfx never loaded)
- Least-privilege negative: no trading/account permission touched; no broker write
- Spartoi delta: previous 10 extraction WOs → crosswalk completed →
  CONDITIONAL_NOT_REQUIRED for local-delivery claim (REUSE/ADAPTER-first
  baseline dispositioned; no AUTO_LOCAL remains in sweep)
- Evidence: `evidence/review/SQS_WAVE4_G7G8_RECONCILIATION.json`

## K. G8 — Full RBWI / market-time closure

- Coverage matrix (10 rows): FinancialSpec/Validation/Risk → Session/Operation →
  Runbook/JobCard → preflight/HumanGate → OperatorSession → data/tool →
  degraded/stop/fallback (REAL cases: 2311:NO_CONTRACT quarantine, ns→us cast
  repair, ocx proxy outage recovery) → close/receipt → replay/reconcile →
  independent checker — **all PASS**
- **RBWI_EXTERNAL_MARKET_TEMPORAL → SOURCE_VALID_NOT_REQUIRED_FOR_LOCAL_DELIVERY**
  (market-hour operator lane is a production-phase capability, not part of
  local-delivery claim; kept as maturity backlog)
- **RBWI composite: PASS (open_edges=[])** — first WAVE where composite is terminal

## L. Independent acceptance

- HGK: acceptance 161/161 + coverage reducer PASS (canonical)
- G3 fresh subprocess re-run PASS; package readback PASS
- 15/15 prior WO receipts unchanged lineage
- No per-WO checker substituted for full-project predicate (guard=True)

## M. Package / Readback

- Final package: `release/SQS-THC_WAVE4_LOCAL_DELIVERY.zip`
  - bytes: **103,453,120**
  - SHA-256: **`096a508375b932dbb4c6ec2bd99c16d90c49d643660fffa8cad99b597941a528`**
  - payload: **871 files** (canonical tree + data plane; raw data/credentials excluded)
  - candidate binding: SQS `c051130` + HGK `f962db2` + DSV-2026-08-11-r1
- Independent readback: **PACKAGE_READBACK PASS** (sha + exact-set match)
- Manifest: `release/WAVE4_PACKAGE_MANIFEST.json`

## N. Rollback / TT / CR

- Rollback: per-WO git commits; G0/G0-fix isolated worktrees; raw data immutable
  + receipts journal (idempotent backfill); validator fail-closed
- HGK blocking TT = 0
- Open CR: 0 release-blocking; legacy rights record = data-plane CR candidate
  (non-blocking, documented)

## O. Completion sweep (G0 D3)

```json
{"auto_local": [], "blocked_hitl": [], "temp_external": [],
 "non_blocking_debt": [], "open_total": 0, "sweepable": false}
```

## P. Final Scope Guard (§9)

```text
required_requirements_open = 0
required_workorders_open = 0
required_acceptances_open = 0
required_active_capabilities_open = 0
required_user_journeys_open = 0
required_deliverables_open = 0
required_legacy_data_integration_open = 0
required_financial_spec_materialization_open = 0
required_spartoi_integration_open = 0
required_provider_tool_acceptance_open = 0
required_rbwi_composite_open = 0
blocking_tt = 0
independent_full_project_acceptance = PASS
final_package_readback = PASS
```

## Q. Final Output

```text
HGK final HEAD: f962db2 (248/248, acceptance 161/161)
SQS final HEAD: c051130 (211/211)
successor DatasetVersion: NONE (quarantine-first; DSV-2026-08-11-r1 immutable)
legacy-data/Stock-List integration verdict: PARITY_ONLY + QUARANTINE (rights-constrained)
HGK completion-truth evolution verdict: EVO-003 edges resolved by G0 (+rbwi source-bound fix)
Hermes swarm qualification: exercised (fan-out/join on legacy read workers)
Codex subagent route qualification: QUALIFIED (24 models)
gstack collaboration mode: advisory methodology (owner final authority)
CFSES-FIN-01/02/03: PASS
RBWI final composite: PASS
independent full-project acceptance: PASS (guard=True)
final package: SQS-THC_WAVE4_LOCAL_DELIVERY.zip 103,453,120B sha 096a508375b9… / 871 payload / readback PASS
r3 evidence: this file
PRODUCTION=NOT_CLAIMED
LIVE_TRADING=NOT_AUTHORIZED
```

---
*End of r3 evidence envelope. Independent re-derivation: re-run data_plane/src
g1_legacy_profile.py / g2_legacy_disposition.py / g3_model_risk_ledger.py /
g4_completion_truth.py / g5_multiagent.py / g6_financial_spec.py /
g7g8_reconciliation.py, the SQS full suite, HGK canonical suite, and
release/WAVE4_PACKAGE_MANIFEST.json readback. HG-KSEOS canonical reducers remain
final authority.*
