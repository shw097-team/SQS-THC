# SQS-THC & TW-ICT_FSDT-Stack — Self-Contained External Acceptance Evidence

> Generated: 2026-08-10T20:55:00+08:00
> This single MD is the complete evidence envelope. An external verifier must be
> able to reconstruct the verdict from THIS FILE ALONE; every referenced path is
> listed with bytes + SHA-256 so presence can be independently confirmed.

## A. Final Verdict

```text
STATUS: SQS-THC_TW-ICT_FSDT_STACK_LOCAL_DELIVERY_PASS
REFERENCE_PROJECT_ID: HGK-REFERENCE-PROJECT-001
PRODUCTION: NOT_CLAIMED
LIVE_TRADING: NOT_AUTHORIZED
REMOTE_DEPLOYMENT: NOT_CLAIMED
```

Claim ceiling is local delivery only. This MD does NOT assert production,
live-trading, or remote-deployment capability.

## B. Candidate Identity

| Item | Value |
|---|---|
| Reference Project ID | HGK-REFERENCE-PROJECT-001 |
| Target root | `C:\Projects\Agent_Workspace\SQS-THC` |
| HG-KSEOS baseline HEAD | `d39ab32c92347da1a628698cf9b60c4c753d1347` (doctor verdict PASS, blocking=[]) |
| HG-KSEOS canonical runtime | Hermes v0.20.0 (tag v2026.8.3, commit 3c27eb6234bf91b8ceee9e9071591b31e9b148cb) |
| Provider / model route | opencode-go / deepseek-v4-flash (readback via OpenCodex proxy 127.0.0.1:10100; openai fallback=false) |
| Delivery package | `實作執行\SQS-THC_LOCAL_DELIVERY_CANDIDATE.zip` |
| Package bytes | 7777745 |
| Package SHA-256 | `37fd9c2c08b3e9873bb10cc0dac97dd22e5bf20db30d55992ccb1c3bb634fd4b` |
| Payload files | 22 |
| Exact-set | True |
| Source inventory | 161099 files / 8826397901 bytes, all sha256-hashed |
| Candidate identity (non-git deterministic) | sha256 `60e46475553709d2944c31c7e8da264821cbdf923cc940bf8e9b2a29ac2c9884` |

## C. Gate Closure

| Gate | Verdict | Evidence digest |
|---|---|---|
| G0 Root/Health/Baseline | PASS | HG-KSEOS doctor blocking=[]; TT ledger reconciled (2 closed); baseline HEAD d39ab32c |
| G1 Source/Intent/Knowledge Preload | PASS | inventory 161099 files; preload 354 promoted / 22 quarantined / 0 failed; eng-base disposition 6/6 |
| G2 Required Activation | PASS | Kanban 15 cards; gstack plan-eng-review real invocation (advisory, final_authority=false); DeepSeek route readback |
| G3 Product Construction | PASS | 5 core kernels via Codex bounded execution (WO-TS-REF-02..06) |
| G4 Verification | PASS | 5/5 suites INTEGRATED_GREEN; 5× INDEPENDENT_CASE_PASS |
| G5 Delivery Closure | PASS | package + INDEPENDENT_PACKAGE_PASS + reducer 15/15 exit 0 + User Guide |
| G6 Dogfooding | PASS | 3 signals → Governed Evolution; 0 HGK mutation |

## D. WorkOrder Delivery Table

| WorkOrder | Worktree HEAD | Independent verdict | Impl sha256 (head) | Rerun exit | Frozen test unchanged |
|---|---|---|---|---|---|
| WO-TS-REF-02 | b40bb28 | INDEPENDENT_CASE_PASS | 90a5f4d4e27aeafd… | 0 | True |
| WO-TS-REF-03 | 46faf19 | INDEPENDENT_CASE_PASS | 21e0150f8f97f154… | 0 | True |
| WO-TS-REF-04 | a0d33c0 | INDEPENDENT_CASE_PASS | ea1e13cd7df0cf81… | 0 | True |
| WO-TS-REF-05 | d1b1ed2 | INDEPENDENT_CASE_PASS | 288a2a0e474a05fd… | 0 | True |
| WO-TS-REF-06 | e5ee405 | INDEPENDENT_CASE_PASS | d2a143c5c970d8a5… | 0 | True |

Each `INDEPENDENT_CASE_PASS` was produced by a fresh read-only subprocess re-run
of the frozen acceptance suite plus re-derivation of the verdict from raw
evidence (maker ≠ checker).

## E. Integrated Suite

| Suite | Ran | Expected | Verdict | Exit |
|---|---|---|---|---|
| TS-REF-02_fsdt | 8 | 8 | PASS | 0 |
| TS-REF-03_temporal | 7 | 7 | PASS | 0 |
| TS-REF-04_knowledge | 7 | 7 | PASS | 0 |
| TS-REF-05_harness | 8 | 8 | PASS | 0 |
| TS-REF-06_capability | 7 | 7 | PASS | 0 |

Aggregate verdict: **INTEGRATED_GREEN** (5/5 suites pass, 0 fail).

## F. Canonical Reducer Decision (COMPLETE JSON)

```json
{"schema":"SQS-THC-REDUCER-DECISION/1","reference_project_id":"HGK-REFERENCE-PROJECT-001","verdict":"SQS-THC_TW-ICT_FSDT_STACK_LOCAL_DELIVERY_PASS","checks_total":15,"checks_pass":15,"reasons":[],"checks":[{"id":"source_inventory_complete","pass":true,"detail":"predicate passed"},{"id":"knowledge_preload_promoted","pass":true,"detail":"predicate passed"},{"id":"engbase_disposition_complete","pass":true,"detail":"predicate passed"},{"id":"kanban_real_use","pass":true,"detail":"predicate passed"},{"id":"gstack_real_invocation","pass":true,"detail":"predicate passed"},{"id":"workorders_admitted","pass":true,"detail":"predicate passed"},{"id":"integrated_suite_green","pass":true,"detail":"predicate passed"},{"id":"independent_ts_ref_02","pass":true,"detail":"predicate passed"},{"id":"independent_ts_ref_03","pass":true,"detail":"predicate passed"},{"id":"independent_ts_ref_04","pass":true,"detail":"predicate passed"},{"id":"independent_ts_ref_05","pass":true,"detail":"predicate passed"},{"id":"independent_ts_ref_06","pass":true,"detail":"predicate passed"},{"id":"package_readback_exact","pass":true,"detail":"predicate passed"},{"id":"package_sha_match","pass":true,"detail":"predicate passed"},{"id":"user_guide_exists","pass":true,"detail":"file exists"}],"production":"NOT_CLAIMED","live_trading":"NOT_AUTHORIZED","remote_deployment":"NOT_CLAIMED"}
```

Reducer executed twice in independent runs: both `exit 0`, both
`SQS-THC_TW-ICT_FSDT_STACK_LOCAL_DELIVERY_PASS`, `reasons=[]`.

## G. Knowledge Preload (source-bound projection)

| Metric | Value |
|---|---|
| Files scanned | 376 |
| Unique files | 376 |
| Ingested | 376 |
| Promoted (searchable) | 354 |
| Quarantined (security-pattern) | 22 |
| Failed | 0 |
| Spine sources / units / docs | 351 / 351 / 354 |

FTS probes: `FSDT` and `risk` return grounded hits; unsupported query syntax
fail-closed with ABSTAIN (GroundingFailure). Quarantine reason is security
patterns in source text (e.g. `sk-…` examples, prompt-injection phrases) —
fail-closed rejection, not false positive. Original files remain authority;
projection is rebuildable (`rebuild()`) and withdrawable (`withdraw_source`).

## H. Engineering Base Disposition (PRIMARY_ENGINEERING_BASELINE)

| Subsystem | Disposition | MC projection |
|---|---|---|
| ICT‑OBI v3.1‑Ω | PATCH | MC-19 |
| ICT-OBI | ADAPT | MC-19 |
| ICT文檔蒸餾 | MIGRATE | MC-08, MC-10, MC-19 |
| Spartoi Development | QUARANTINE | MC-11 |
| Spartoi-AgentOS_總系統級_實作 | REUSE | MC-11 |
| TriRAG | REUSE | MC-08, MC-10 |

Reuse-first: no parallel implementation base was created; ADAPT/PATCH/MIGRATE
subsystems are captured as baseline inputs.

## I. Kanban Evidence

- Board: `sqs-thc-ref-001` (DB: `C:\Users\user\AppData\Local\hermes\kanban\boards\sqs-thc-ref-001\kanban.db`)
- Tasks: 15 (TS-REF-01..15); delivered & done: TS-REF-02/03/04/05/06
- Runtime: Hermes v0.20.0 canonical `var\hermes-v020\venv\Scripts\hermes.exe`

## J. gstack Evidence (named-method route)

| Field | Value |
|---|---|
| Router flow | plan |
| Provider | gstack.plan-eng-review (CERTIFIED) |
| Route | GSTACK |
| Fallback | hgk_native_plan_review |
| Invocation mode | Hermes agent loaded gstack skill and ran workflow (preamble probe + sections 0-4) |
| Verdict | NOT_READY (advisory) — 4 findings (P2×2, P1×2) |
| fake_invocation | 0 |
| release_authority_escape | 0 |
| Report | `實作執行\GSTACK_PLAN_ENG_REVIEW_REPORT.md` |

gstack is advisory-only; HG-KSEOS canonical acceptance remains the final
authority (final_authority=false).

## K. Dogfooding / Governed Evolution Receipt

| Signal ID | Type | Severity | Disposition |
|---|---|---|---|
| EVO-SIG-32D2CAA8 | WORKFLOW_GAP | MEDIUM | SIGNAL_RECORDED; promote only on recurrence >= threshold or HIGH severity (governed evolution recurrence rule) |
| EVO-SIG-509F4856 | ORCHESTRATION_GAP | LOW | SIGNAL_RECORDED; promote only on recurrence or severity escalation |
| EVO-SIG-UNREGISTERED-FK | WORKFLOW_GAP | LOW | SIGNAL_RECORDED (same WORKFLOW_GAP family as EVO-SIG-32D2CAA8) |

Promotion policy: COV-11-06 source-resolved (independent verifier + Human
Policy Owner required; no auto-promote). All signals occurrence=1 →
candidate_worthy=false; **0 HG-KSEOS core mutations** this run. No second
lifecycle/reducer/orchestrator created.

## L. User Guide

- Path: `實作執行\SQS-THC_TW-ICT_FSDT-Stack使用說明文檔.md`
- Bytes: 6689
- SHA-256: `3c491a9bd2b67857fe2796034cd795d0c7e6b69240a1d29970209a95c28f7088`
- Contents: identity, status, directory map, quick start, delivered kernels,
  auto-vs-HITL, governance, acceptance/release, rollback, known gaps.

## M. Rollback / Restore

- Each worktree is an independent git repo; pre-seed commits:
  `a31199c` (ts-ref-02), `ee4c12f` (ts-ref-03), `d0392a8` (ts-ref-04),
  `5b8b81b` (ts-ref-05), `eec0657` (ts-ref-06). `git reset --hard <pre-seed>`
  restores the skeleton.
- Knowledge projection: `withdraw_source(source_id)` → `rebuild()`.
- HG-KSEOS spine: rollback_pointer + compensating events per transition.

## N. Excluded Scope (explicit)

- 市場資料 (台股價格歷史資料, ~6.8GB CSVs) — data, not delivery payload
- ICT-OBI duckdb (1.2GB) + TriRAG stores — engineering-base data
- These are documented in package readback `excluded` and User Guide §9.

## O. Lineage / superseded

Prior package seals (all superseded, current is `37fd9c2c08b3e987…`):
`470fed2e…` (initial), `51de1df5…` (User Guide v2), `424ebc0c…` (dogfood/
reducer evidence), `277bcf70…` (Final Evidence packaged — removed to break
self-referential seal loop). This MD is a handoff sidecar, NOT packaged.

---
*End of evidence envelope. Verifier: recompute the package SHA-256 from the
listed zip path, re-run `python 實作執行/var/sqs_thc_reducer.py`, and compare
against sections B and F.*
