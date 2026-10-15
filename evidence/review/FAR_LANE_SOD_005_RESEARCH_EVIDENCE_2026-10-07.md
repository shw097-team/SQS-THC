# FAR-LANE-SOD-005 - FAR research: post-freeze amendment necessity and the VERIFY-lane post-mortem

> Round `FAR-LANE-SOD-005` · generated 2026-10-07T12:50:36.780907+00:00 · **claim ceiling = CANDIDATE_ONLY**
> Mandated SoD: PLAN `gpt-6.1-sol/openai-codex` -> EXECUTE sealed Codex CLI + `deepseek-v4.1-flash/opencode-go`
> -> VERIFY `glm-5.3-flash/opencode-go`.

## 1. Governance lineage

| Surface | Receipt |
|---|---|
| HGK admission | `REQ-FAR-LANE-SOD-005` FROZEN; `TS/WO-FAR-LANE-SOD-005-{PLAN-A,PLAN-B,EXECUTE,VERIFY}`; base HEAD `623fd3f5`; `canonical_events` 935 -> 936 |
| KANBAN | board `far-lane-sod-005`, six cards with explicit per-card model/provider overrides (PLAN cards `gpt-6.1-sol`, VERIFY card `glm-5.3-flash`, others `deepseek-v4.1-flash`) |
| SWARM | `deleg_2fc4b980` ran PLAN-A and PLAN-B in parallel on the mandated PLAN model; `deleg_e0d8c2e7` ran the VERIFY lane |
| CODEX CLI | `proc_6193ca544357`, sealed launcher, `opencode-go/deepseek-v4.1-flash`, exit 0, single sanctioned model, chain not exhausted |
| OPENSPEC / GSTACK | unchanged this round; the enforcement change set remains `openspec/changes/lane-sod-enforcement` (valid, 27 tasks) |

## 2. Q1 - is a post-freeze amendment warranted for the cosmetic prose defect?

**Necessity LOW. Recommendation: do not amend the FAR-LANE-SOD-004 freeze; record the erratum here.**

- Materiality: {'classification': 'COSMETIC documentation inconsistency; acknowledged scope residual, not failed adoption.', 'routing': 'No demonstrated routing harm. Structured provider_route.model correctly pins deepseek-v4.1-flash; prior independent verifier explicitly found text-only/no routing impact. No operational codex_route reader found in inspected repository source types. This is bounded evidence, not proof about every external reader. [C1,C6,C14]', 'operator_confusion': 'Real but low-consequence ambiguity: an operator reading or copying the narrative may believe deepseek-v4-flash was/currently is
- Deciding criterion: Does leaving this exact prose unchanged cause demonstrated execution/policy/checker error or materially invalidate the independently verified frozen acceptance record? No on inspected evidence: model pin correct, no source consumer found, drift invariant under prose substitution, original design/verdict explicitly disclose the residual. Operator confusion alone warrants a visible erratum, not reop
- Recommendation as delivered: Choose option (a): preserve FAR-LANE-SOD-004 and all four frozen mirrors unchanged; add the explicit codex_route erratum to FAR-LANE-SOD-005 evidence, with no post-freeze amendment now.
- The amendment's full cost chain was enumerated in ten steps (authorization, preimage, field-level diff,
  a delta verdict, re-enumeration, a new manifest, a regenerated evidence file, four mirror re-copies, governance
  reconciliation, and an explicit supersession declaration). Its blast radius is that every frozen digest becomes
  a superseded identity - which is precisely why LOW-level cosmetic drift is better carried as an erratum.
- Counter-argument (stated fairly by the report and endorsed here): a configuration file whose prose names the
  wrong model can mislead an operator, and "zero findings" partly reflects checker coverage rather than perfect
  documentation. The residual is therefore disclosed, not dismissed.
- Independent check: the VERIFY lane re-walked the repository and found **zero readers** of the
  `provider_route.codex_route` prose across 88 textual hits (all hits are the prose itself, mirrors, or historical
  acceptance check identifiers).

## 3. Q2 - why are VERIFY lanes long-running and stall-prone?

**Necessity HIGH - repair the VERIFY lane contract and orchestration. No evidence supports replacing the model,
weakening verification, bypassing guards, or rebuilding the platform.**

Measured anchors (independent parsers, agreeing exactly where they overlap):

| Lane | Wall | API calls | Guard refusals | Tool max | Tool sum | Input growth | Output tokens |
|---|---:|---:|---:|---:|---:|---|---:|
| `deleg_02fea2fc` VERIFY (interrupted) | 2764 s | 170 | **33** | 104.2 s | 527.0 s | 14,001 -> 207,566 | 101,964 |
| `deleg_68413d1a` VERIFY | 1036 s | 83 | - | **180.7 s** | 305.2 s | - | - |
| `deleg_8ee7fa5c` VERIFY | 768 s | 46 | - | 108.4 s | 218.7 s | - | - |
| `deleg_ab3cf194` PLAN | 195.6 s | 12 | - | 1.0 s | 12.9 s | - | - |
| `deleg_b78efec7` PLAN | 507 s | 24 | - | 3.7 s | 43.6 s | - | - |

Findings that decide the question:

- Per-call latency tracks **output** size (r = **0.804** over 170 calls) and not input size (r = **-0.038**):
  the lane is slow because of what it generates and the tool work it drives, not because it re-reads context.
- Single-call maxima cluster at **80-180 s on VERIFY** versus **1-4 s on PLAN**: the cost is in broad filesystem
  discovery (two measured scans timed out at 180.7 s and 196.8 s), not in model latency - hence
  "intrinsic model slowness" is **not** established.
- Flagged results cluster on VERIFY (12-39 per anchor versus 3-9 on PLAN): refusal-and-retry loops are real and
  were badly under-counted in the orchestrator's own earlier note (33, not 9).
- A live demonstration in this same round: the first VERIFY attempt was killed at 17 s by an **external stop**
  (`user_stop`, "parent delegation ended") - **not** a lane defect - and the retry respected the new discipline
  (verdict skeleton written FIRST at 20:25:52 and present throughout its long generation phase). That single
  change removed the round's worst failure mode (a verdict lost because it was only written at the end).

Proposed changes delivered, with the highest-value items named:

| id | change | cost |
|---|---|---|
| P1 | MINIMUM VIABLE: durable target-path verdict skeleton before discovery | Near-zero implementation risk; briefing edit plus on |
| P2 | BIGGEST STRUCTURAL WIN: bounded acceptance matrix + read-only evidence runner | Medium engineering effort; estimate 1-3 engineer-day |
| P3 | Bound and index filesystem discovery | Low; estimate half a day to add authoritative roots  |
| P4 | Serialize-validate before safe verdict replacement; checkpoint per item | Low; estimate half a day plus failure-injection test |
| P5 | Typed refusal handling: stop retries and emit BLOCKED/HITL | Low for lane-contract rule; medium for guard/tool re |
| P6 | Receipt summarization once, compact output and context caps | Low; estimate half a day for per-family parsers and  |
| P7 | Enforced per-item budgets and no-progress watchdog | Low/medium; estimate one day to implement observable |
| P8 | Controlled telemetry/A-B qualification before model replacement | Medium; estimate one engineer-day setup plus approve |

- **P1 (minimum viable, near-zero risk):** write a durable target-path verdict skeleton **before** discovery, then
  refine it in place. Adopt immediately.
- **P2 (biggest structural win):** a frozen, numbered acceptance matrix plus a deterministic read-only evidence
  runner, retaining bounded adversarial checks - so a verifier checks a list and runs a runner instead of
  rediscovering the scope by scanning.

## 4. Independent verification

- **Independent verdict, research round**: verdict **PARTIAL** · `lanes/laneV_research_verdict.json` (5,050 B, sha256 `3382eb32975f2d47...`)

- Q2 verdict: **SOUND** - every headline number for `deleg_02fea2fc` was reproduced a third way
  (2763.02 s, 170 API calls, 33 refusals, tokens 14,001 -> 207,566 in / 101,964 out, r_in = -0.038, r_out = 0.804),
  and the fault attribution with P1/P2 was judged proportional with no overselling.
- Q1 verdict: **SOUND_WITH_CAVEAT** - the LOW rating and the erratum recommendation are defensible; the report's
  claim that the frozen digests still match was already stale at verify time for one artifact (see section 5).
- Overall **PARTIAL** (6 of 9 checks hold): the two failures are boundary checks, not content checks.

## 5. Finding N1 - a concurrent governed round superseded the shared SSOT mid-round

This is the round's most consequential discovery and it resolves the only failed boundary check.

- While this round ran, **another governed round, `FAR-LANE-SOD-006`**, was admitted into the same control plane:
  `var/far-lane-sod-006/` was created at 20:31:12 local, `REQ-FAR-LANE-SOD-006` landed in the spine at 20:19:34 local,
  `canonical_events` advanced 936 -> **937**, and `WO-FAR-LANE-SOD-006-{PLAN-A,PLAN-B,EXECUTE,VERIFY-A,VERIFY-B}`
  now exist. It runs in a separate Hermes session (`20261007_200605_743d2a`).
- Consequence: the lane policy advanced from revision 9 (`969af3036aeca8e7...`, the digest this round pinned at
  admission) to revision 11 (`6d1f047a5cdfc147...` at freeze), and `config/lane-routing-registry.yaml`
  advanced from `5d50ca9f...` (the digest frozen into FAR-LANE-SOD-004) to `09d6964648e660e2...`
  with epoch 10 and `source_of_routes.revision: 11`.
- The VERIFY lane correctly flagged the registry change as an unattributed mid-round drift, and it was right to fail
  the boundary check: at verify time nothing in the evidence explained it. The attribution is now known - a later
  governed round, not a rogue write and not this round's lanes.
- **No restore was performed.** Rolling the registry back to `5d50ca9f...` would have clobbered the
  legitimate work of round 006. The superseded identity is recorded, not reverted - the same principle this round's
  Q1 answer applies to the cosmetic prose.
- Recommendation (new): the SSOT files (`config/model-lane-assignment.json`, `config/lane-routing-registry.yaml`)
  must be written through HGK admission **under a lock**, and every round must record the round that supersedes its
  pinned digests, so a boundary check can distinguish "superseded by round N" from "unattributed drift".

## 6. Claim ceiling and write ledger

`NO_SUBJECT_STORE_MUTATION`. Enumeration of everything this round touched:
(1) the admission audit rows for `REQ-FAR-LANE-SOD-005` (`canonical_events` 935 -> 936);
(2) the `far-lane-sod-005` board store and its six cards;
(3) the whole of `var/far-lane-sod-005/` (admission script, lane deliverables, instrument, dataset, receipts, codex outputs, this freeze);
(4) the Hermes runtime state: deliberate `delegation.provider/model` writes to route the PLAN and VERIFY lanes,
   restored to `openai-codex/gpt-6.1-sol`, plus agent.log;
(5) this evidence file's three mirrors under `HG-KSEOS/evidence/review`, `Fabric/evidence/review`,
   `SQS-THC/evidence/review` (four byte-identical copies).
**Everything else that changed under this repository during the round window belongs to round 006, not to this round** -
including the policy revision 9 -> 11 and the registry epoch change recorded in section 5.

**Not claimed**: external acceptance, promotion, production, that the VERIFY lane's deficiencies are repaired
(they are diagnosed and specified, not implemented), that the cosmetic prose has been cleared, and the correctness
of anything not re-executed here.

## 7. Residual gaps carried forward

- The Q2 plan is a plan: P1 is demonstrated (used in this round's own retry) but P2-P8 are specified, not built.
- C8 (instrument re-run) was deliberately marked optional by the orchestrator and was not performed; the instrument
  and dataset digests are recorded instead.
- The Shared Spine write check was not completed inside the verify budget; the spine's event count is recorded here
  from a direct read-only query.
- Concurrent rounds share one repository with no lock on the SSOT files (finding N1).
- The guide's prose erratum is recorded here; the guide file itself was deliberately not amended (Q1 answer).

## 8. Artifact digest

18 artifacts, 324,601 bytes. Manifest `evidence/EVIDENCE_MANIFEST.json` sha256 `fea406f8573f228c6df24062d4c6ffe2350390d20692c9f64ecb84d671dcc31c`.
Per-artifact digests are authoritative in the manifest, never in this file.

## 9. Mirror verification

This file is written last and mirrored to three additional roots; all four copies are asserted byte-identical
at generation time and re-checked by hand.
