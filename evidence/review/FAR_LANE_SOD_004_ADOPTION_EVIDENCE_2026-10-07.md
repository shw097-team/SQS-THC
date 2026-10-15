# FAR-LANE-SOD-004 — adoption of the enforcement plan (single evidence file)

> Round `FAR-LANE-SOD-004` · generated 2026-10-07T11:31:13.083261+00:00 · **claim ceiling = CANDIDATE_ONLY**
> Predecessors: `ROUTE-LANE-001`, `FAR-LANE-VERIFY-002`, `FAR-LANE-SOD-003` (kit + adoption guide).
> Instruction: execute the FAR research conclusions and recommendations in full, under the same
> mandated model SoD — `PLAN gpt-6.1-sol/openai-codex → EXECUTE Codex CLI + deepseek-v4.1-flash/opencode-go →
> VERIFY-SECURITY glm-5.3-flash/opencode-go`.

## 1. Governance lineage

| Surface | Receipt |
|---|---|
| HGK admission | `REQ-FAR-LANE-SOD-004` FROZEN; `TS/WO-FAR-LANE-SOD-004-{PLAN,EXECUTE,VERIFY}` (writers plan-lane / codex / hermes-verify-lane); base HEAD `623fd3f5`; `canonical_events` 934 → 935 (`receipts/admission_receipt.json`) |
| KANBAN | board `far-lane-sod-004`, 9 cards, every card carrying an explicit per-card model/provider override (`gpt-6.1-sol/openai-codex` on the PLAN card, `glm-5.3-flash/opencode-go` on the VERIFY card, `deepseek-v4.1-flash/opencode-go` elsewhere) — the durable per-task route, not the global pin |
| SWARM (PLAN) | `deleg_b78efec7`, `gpt-6.1-sol`, 507 s — preimage-backed adoption design |
| CODEX CLI (EXECUTE) | `proc_a8b1ea21e710`, sealed launcher, `opencode-go/deepseek-v4.1-flash`, exit 0, `write_model_used` = the single sanctioned model, chain not exhausted |
| SWARM (VERIFY) | `deleg_8ee7fa5c`, `glm-5.3-flash/opencode-go` |
| Relayed RUN | sealed relay restored this round: supervisor `Verify` reported DEGRADED, then `Run` brought `healthz` to ok (opencodex 2.11.0) |
| OPENSPEC / GSTACK | `openspec/changes/lane-sod-enforcement` still `validate --strict` valid (27 tasks); gstack route disposition in the predecessor round's evidence |

## 2. What was APPLIED (and how it was proven)

| Step | Effect | Independent proof run by the orchestrator |
|---|---|---|
| S1 binding repoint | `config/hermes.json` `/install_root` and `/canonical_hermes_home` now name the MSIX install; `/provider_route/model` = `deepseek-v4.1-flash` | `hgk-lane-policy.py validate` → **findings 0, rc 0**; `diff-live` → `changes: []` — defect **D19 closed** |
| S2 documentation | guide copy carries the six-line troubleshooting pointer at the existing `Step 9-0a`; **both** guardrail runtime-note copies byte-identical (`138e4f05…`, 7,805 B) with the corrected mint truth | byte-equality and content checks re-run by hand |
| S3 duplicate sync | the stale packaged mint copy was synced to the repaired bytes | both mint copies now `211dace8…`, 4,710 B — **equal** |
| S4 supervisor task | `HGK-OpenCodex-Sealed-10101` registered, `State=Ready`, pwsh + `supervise-hgk-opencodex.ps1 -Action Run`, working dir HG-KSEOS, triggers enabled | `Get-ScheduledTask` readback + relay `healthz` ok |

Every step was executed under preimage discipline: the pre-change bytes are kept under
`var/far-lane-sod-004/backup/` with a recorded sha256, and each receipt names its rollback.

## 3. What was NOT applied, and why

The design deliberately did **not** fabricate productive diffs for five of the eight integration points.
They are recorded in `receipts/not_applied.json` as `applied: false`:

| Point | Target | Reason |
|---|---|---|
| 1 dispatcher guard call | `hermes_cli/kanban_db_dispatch.py` | `BLOCKER-BINDING` |
| 2 sealed launcher refusal | `scripts/start-hgk-hermes.ps1` | `BLOCKER-BINDING` |
| 3 fallback lane gate | `agent/auxiliary_client.py` | `BLOCKER-BINDING` |
| 4 delegation-role enforcement | `tools/delegate_tool.py` | `BLOCKER-BINDING` |
| 8 admission-token mechanism | `scripts/hgk-lane-guard.py` | `BLOCKER-PROBE` |

`BLOCKER-BINDING`: no trusted HGK execution-binding/resolver accessor was found in the inspected source,
so a task's lane role cannot be resolved from authority — deriving it from a prompt, card body or caller
metadata would **forge** authority rather than enforce it.
`BLOCKER-PROBE`: `scripts/probe-hgk-lane.py`'s live branch explicitly states that genuine dispatch is not
implemented and returns `ERR_LANE_LIVE_EXERCISE_NOT_IMPLEMENTED`, so a lane-shaped admission cannot be
liveness-proven yet.
Containment-only alternatives exist for these points; applying them would pause unrelated non-governed
work while not achieving enforcement. They were deliberately not applied.

## 4. The corrected mint truth (recorded because an earlier draft got it wrong)

An earlier staged documentation draft implied the mint hook's refresh defect was "already fixed" everywhere.
Byte-diff settles it: the **loaded** mint script is the legacy path named in the live `config.yaml`
`pre_llm_call` registration, and it **already carries the repair** (the unconditional early `return` became
"return only while the stored token is still live"). The **packaged duplicate** was stale and byte-identical
to the pre-repair backup; this round synced it (S3), so the two copies are now equal. Both statements are
asserted by the independent verdict.

## 5. Verdicts

- **Independent verdict, adoption round**: verdict **PASS** · `lanes/laneV_adoption_verdict.json` (10,803 B, sha256 `8d517407479d166c…`)
- **Predecessor verdict, iteration 1**: verdict **PARTIAL** · `var/far-lane-sod-003/lanes/laneV_sod_enforcement_verdict.json` (11,066 B, sha256 `690a184f2c19c84a…`)
- **Predecessor verdict, iteration 2**: verdict **PASS** · `var/far-lane-sod-003/lanes/laneV2_repair_verdict.json` (10,787 B, sha256 `bbbfaf61913f22d2…`)

## 6. Claim ceiling and write ledger

`NO_SUBJECT_STORE_MUTATION` (the spine's research and forensic stores were not written) plus an enumerated
ledger:
(1) control-plane admission audit rows, `canonical_events` 934 → 935;
(2) the `far-lane-sod-004` board store and its 9 cards;
(3) the round directory `var/far-lane-sod-004/` (design, preimages, receipts, codex outputs, lanes);
(4) **live files written by this round**: `config/hermes.json` (repoint), `HG-KSEOS/evidence/review/FDA_USER_GUIDE.md`
(correction), both copies of `fda-guardrail-runtime-notes.md`, and the packaged `fda_guard_mint.py`
(duplicate sync) — each with a preimage under `backup/`;
(5) a Windows scheduled task `HGK-OpenCodex-Sealed-10101` (previously absent);
(6) Hermes runtime state: deliberate `delegation.provider/model` writes for the VERIFY dispatches, restored to
`openai-codex/gpt-6.1-sol`, plus agent.log;
(7) **this evidence file's three mirrors** under `HG-KSEOS/evidence/review`, `Fabric/evidence/review`,
`SQS-THC/evidence/review` (four byte-identical copies).

**Not claimed**: external acceptance, promotion, production, that the live dispatch chain enforces the SoD
(it does not — see §3), that D2–D8 or lane admission are closed, and the correctness of anything not
re-executed here.

## 7. Residual gaps carried forward

- Productive enforcement still requires a trusted binding accessor and a working live lane probe; until then
  the gate remains a demonstrated, fail-closed *candidate* that a dispatcher must be told to call.
- The guide edited is the repo's review copy; the operator-facing attachment under the Hermes attachments
  directory was not modified by this round.
- The scheduled supervisor task is a scheduled task, not a service: a logoff stops an interactive run, and a
  `healthz` 200 does not attest provider weights or listener ownership.
- `config/hermes.json` retains other legacy-named fields (executable, python path, kanban db path, route
  narrative) that were deliberately left alone; only the three pointers the registry projects were repointed.

## 8. Artifact digest

36 artifacts, 950,779 bytes. Manifest `evidence/EVIDENCE_MANIFEST.json` sha256 `7db0835c752a2ecd10750b4e3f4e6c64650d64206001b8410a8b66e4a7269809`.
Per-artifact digests are authoritative in the manifest, not here.

## 9. Mirror verification

This file is mirrored to three additional roots and all four copies are asserted byte-identical at generation
time; the assertion result is printed by the freeze step and re-checked by hand.
