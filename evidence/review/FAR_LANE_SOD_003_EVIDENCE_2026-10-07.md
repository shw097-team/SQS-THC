# FAR-LANE-SOD-003 — single evidence file

> Round `FAR-LANE-SOD-003` · generated 2026-10-07T10:39:51.446224+00:00 · **claim ceiling = CANDIDATE_ONLY**
> Predecessors: `ROUTE-LANE-001`, `FAR-LANE-VERIFY-002`.
> Deliverable: a complete, landable plan that makes the mandated model SoD routing enforced and
> durable — `PLAN gpt-6.1-sol/openai-codex → EXECUTE Codex CLI + deepseek-v4.1-flash/opencode-go →
> VERIFY-SECURITY glm-5.3-flash/opencode-go` — plus the machinery that keeps later routing on it.

## 1. Governance lineage

| Surface | Receipt |
|---|---|
| HGK admission | `REQ-FAR-LANE-SOD-003` FROZEN; `TS/WO-FAR-LANE-SOD-003-EXECUTE` (writer=codex), `TS/WO-FAR-LANE-SOD-003-VERIFY` (writer=hermes-verify-lane); base HEAD `623fd3f5`; `canonical_events` 932 → 933 (`receipts/admission_receipt.json`) |
| KANBAN | board `far-lane-sod-003`, 13 cards with DAG; VERIFY card pinned `model_override=glm-5.3-flash`, `provider_override=opencode-go` (`receipts/kanban_cards.json`) |
| SWARM (PLAN) | 3 design lanes `deleg_ee0ad625` (gpt-6.1-sol, 621 s); 1 FAR research lane `deleg_ab3cf194` (gpt-6.1-sol, 196 s) |
| SWARM (VERIFY) | `deleg_02fea2fc` interrupted at 2,763 s with no verdict → superseded by `deleg_68413d1a` (glm-5.3-flash/opencode-go, 1,036 s, PARTIAL) → after the repair pass, `deleg_4ab77238` (iteration 2) |
| CODEX CLI | EXECUTE `proc_d892125676bb`, `opencode-go/deepseek-v4.1-flash`, exit 0, 174 commands, 2 benign policy-blocked directory listings |
| OPENSPEC | change `lane-sod-enforcement`, `validate --strict` → valid (27 tasks) |
| GSTACK | named-method route disposition, `evidence/GSTACK_SOD_RECEIPT.json` |
| Dispatch routing | `receipts/dispatch_receipt_r2.json`: the pin at spawn matched the mandate for every lane; `method_router.py`/`spec_adapter.py` verified ABSENT upstream |

## 2. The mandated SoD, as actually observed (runtime log is authoritative)

```
2026-10-07 14:32:27 agent.turn_context session=20261007_143226_7610ff model=gpt-6.1-sol provider=openai-codex platform=subagent
2026-10-07 14:32:27 agent.turn_context session=20261007_143227_8a5632 model=gpt-6.1-sol provider=openai-codex platform=subagent
2026-10-07 14:32:27 agent.turn_context session=20261007_143227_b2ef8b model=gpt-6.1-sol provider=openai-codex platform=subagent
2026-10-07 15:20:37 agent.turn_context session=20261007_152037_a6f089 model=glm-5.3-flash provider=opencode-go platform=subagent
```

Maker = `deepseek-v4.1-flash/opencode-go` (main loop). PLAN, EXECUTE and VERIFY therefore ran on
three **distinct** mandated models — the maker/checker collapse that failed FAR-Q3 in the
predecessor round does **not** reproduce on the round's own dispatch lanes. The same log shows the
pin binds at spawn and is not retroactive: session `a6f089` kept `glm-5.3-flash` across API calls
#96…#170 after the pin had already been restored to the PLAN model.

## 3. Problem set (lane A): 25 falsifiable defects

Classes: ENFORCEMENT 9, TOOLING 8, DECLARATION 5, AVAILABILITY 3. Highlights:
`D1` maker/checker collapse unenforced; `D2` ordinary delegation pinned to PLAN not VERIFY;
`D3` global fallbacks list executor models before checker arms; `D4` per-lane fallbacks are not a
runtime surface; `D5` global delegation swaps race; `D6` per-card overrides affect the next
dispatch only; `D11` NVIDIA Flash secondary has no lane-shaped proof; `D19` the binding points to a
legacy home and an old model slug; `D23` the gate checker scans its own previous output;
`D25` named GSTACK/OpenSpec adapters absent. Full text and evidence quotations:
`lanes/laneA_defect_register.json`.

## 4. The delivered plan (candidate kit)

| scope | path | bytes | sha256 |
|---|---:|---:|---|
| deliverable | `config/lane-routing-registry.yaml` | 11,192 | `5d50ca9fdf3ab690…` |
| deliverable | `src/hg_kseos/lane_policy.py` | 14,751 | `498ab9435a7d5f88…` |
| deliverable | `src/hg_kseos/lane_admission.py` | 9,489 | `235b4bfbb5e98eb8…` |
| deliverable | `scripts/hgk-lane-policy.py` | 4,758 | `91014a30358a8de7…` |
| deliverable | `scripts/hgk-lane-guard.py` | 10,218 | `93079679890bdb31…` |
| deliverable | `scripts/probe-hgk-lane.py` | 7,892 | `88f2a809dff66de8…` |
| deliverable | `scripts/hgk-artifact-gate.py` | 9,224 | `f2ae2f1828069ae9…` |
| deliverable | `scripts/supervise-hgk-opencodex.ps1` | 6,965 | `2e77b3cdd387cf2d…` |
| deliverable | `tests/test_lane_policy.py` | 13,812 | `dad474c66c9ad44a…` |
| deliverable | `tests/test_lane_guard.py` | 5,279 | `270b9515d51c1849…` |
| deliverable | `HGI_LANE_ENFORCEMENT_KIT.md` | 11,664 | `28af765401e179d0…` |

- **RB-1** single-source routing registry + whole-policy projection + exhaustive drift check
  (`config/lane-routing-registry.yaml`, `src/hg_kseos/lane_policy.py`, `scripts/hgk-lane-policy.py`).
- **RB-2** mandatory pre-dispatch conformance gate + durable first-class verify-dispatch that does
  **not** depend on flipping a global delegation pin (`scripts/hgk-lane-guard.py`,
  `src/hg_kseos/lane_admission.py`).
- **RB-3** lane-shaped admission probe (never ADMITTED from a direct completion), repaired gate
  checker, stale-packet gate, supervised relay (`scripts/probe-hgk-lane.py`,
  `scripts/hgk-artifact-gate.py`, `scripts/supervise-hgk-opencodex.ps1`).
- **RB-4** durable wiring (+14 surfaces) and executable drift regression
  (`tests/test_lane_policy.py`: 3 tests, 42 drift-injection subcases, no skip;
  `tests/test_lane_guard.py`: 8 regression tests locking the repaired guard behaviour).
- Adoption guide: `HGI_LANE_ENFORCEMENT_KIT.md`. OpenSpec change: `openspec/changes/lane-sod-enforcement/`.

## 5. Enforcement evidence

### 5.1 Before the independent verdict (as originally recorded)

| Case | Intent | Exit | Decision | Error |
|---|---|---:|---|---|
| A2 | verify target model == maker model, ADMITTED | 2 | REFUSE | `ERR_LANE_SOD_VIOLATION` |
| B2 | verify on `glm-5.3-flash/opencode-go`, ADMITTED | 0 | ADMIT | — |
| C2 | separated model but `UNPROVEN` admission | 3 | REFUSE | `ERR_LANE_NOT_ADMITTED` |
| D2 | EXECUTE lane misusing the PLAN model | 2 | REFUSE | `ERR_LANE_SOD_VIOLATION` |
| E2 | PLAN lane on `gpt-6.1-sol/openai-codex` | 0 | ADMIT | — |
| X | unknown lane name | 3 | REFUSE | `ERR_LANE_UNKNOWN_LANE` |

### 5.2 After the repair pass (maker re-run, `receipts/REPAIR_RECEIPT_R1.json`)

| Case | Intent | Exit | Required |
|---|---|---:|---|
| g1 | verify target model == maker model | 2 | SoD violation refused |
| g2 | verify arm with an ADMITTED receipt fixture | 0 | legitimate ADMIT still admitted |
| g3 | same arm, bare string `ADMITTED` | 3 | unevidenced admission refused (V3) |
| g4 | receipt provider ≠ `--target-provider` | 3 | provider mismatch refused (V4) |
| g5 | receipt present, `--target-provider` omitted | 3 | omission is not a wildcard (V4) |
| g6 | registry copy with a wrong source pin | 4 | staleness still detected (V1 path) |
| g7b | PLAN arm with an ADMITTED plan fixture | 0 | positive control for the PLAN lane |
| g8 | PLAN fixture + `--expected-epoch 8` vs live 9 | 4 | epoch assertion cannot be forced (V6) |

Unit tests after the repair: `tests.test_lane_policy` 3/3 OK; `tests.test_lane_guard` 8/8 OK.
Drift check (`scripts/hgk-lane-policy.py validate`): exactly **3** findings, all
`PROJECTION_DEBT` against `config/hermes.json` (legacy home, legacy home key, old slug) =
defect `D19`, `fatal: false`, and **zero** `DRIFT_VALUE` — including zero for the four new
`reasoning_effort` bindings.

## 6. Adoption status — what holds *today* versus what is staged

- **Holds today**: the declared policy names the mandated routes at **revision 9**
  (sha `969af3036aeca8e7…`); `sod.plan_lane` / `execute_lane` / `verify_security_lane` match the
  mandate, and the VERIFY/SECURITY lane now carries an explicit `reasoning_effort: medium` at four
  sites that the drift check actually inspects.
- **Demonstrated candidate**: the gate refuses violations fail-closed (8-case matrix above), the
  drift check catches real positives (`D19`), and both regression suites run green.
- **Staged, not adopted**: nothing in the live dispatch path consults the guard or the registry yet.
  The minimal-diff wiring into the live dispatcher/launcher is documented, not applied. The
  mechanism this round actually used to route its own VERIFY lane is still the global delegation
  pin — the very fragility RB-2 exists to remove.
- **Therefore**: "later routing follows the scheme" is **guaranteed by design and by a
  failing-loud regression test**, *not* by live enforcement. Any statement that the live stack is
  already enforced would be an overclaim.

## 7. Claim ceiling and write ledger

`NO_SUBJECT_STORE_MUTATION` (the spine's research and forensic stores were not written) plus an
enumerated ledger:
(1) control-plane admission audit rows, `canonical_events` 932 → 933 (admission) → 934 (the
authorization work order);
(2) the `far-lane-sod-003` board store and its 13 cards;
(3) this round directory, including `receipts/`, `evidence/`, `lanes/`, `codex/`, `backup/`;
(4) new candidate artifacts inside `HG-KSEOS/` — `config/lane-routing-registry.yaml`,
`src/hg_kseos/lane_policy.py`, `src/hg_kseos/lane_admission.py`, `scripts/hgk-lane-policy.py`,
`scripts/hgk-lane-guard.py`, `scripts/probe-hgk-lane.py`, `scripts/hgk-artifact-gate.py`,
`scripts/supervise-hgk-opencodex.ps1`, `tests/test_lane_policy.py`, `tests/test_lane_guard.py`,
`HGI_LANE_ENFORCEMENT_KIT.md`, `openspec/changes/lane-sod-enforcement/`;
(5) **the canonical policy file itself**: `config/model-lane-assignment.json` revision 8 → 9 on the
operator's explicit instruction, byte-preimage preserved at
`backup/model-lane-assignment.rev8.json`;
(6) Hermes runtime state: deliberate `delegation.provider/model` writes, restored to
`openai-codex/gpt-6.1-sol`, plus agent.log;
(7) the guarded pre-call authorization store (a session token) and one ACTIVE route registered in
the pre-call route registry for this round;
(8) **this evidence file's three mirrors** under `HG-KSEOS/evidence/review`,
`Fabric/evidence/review`, `SQS-THC/evidence/review` (four byte-identical copies).
**Not claimed**: external acceptance, promotion, production, live enforcement, Stage-3/SQP1
activity, and the correctness of anything not re-executed here.

## 8. Verdicts, defects, errata and nonclaims

- **Independent verdict, iteration 1**: verdict **PARTIAL** · `lanes/laneV_sod_enforcement_verdict.json` (11,066 B, sha256 `690a184f2c19c84a…`)
- **Independent verdict, iteration 2 (repair set)**: verdict **PASS**; repair defects closed 6, still open 0 · `lanes/laneV2_repair_verdict.json` (10,787 B, sha256 `bbbfaf61913f22d2…`)
- The independent iteration-1 verdict returned **PARTIAL** with six defects and graded the round's
  own disclosure as **ACCURATE**. Two were major (V1 stale source pin — which had been introduced by
  this round's own revision-9 change; V2 post-window registry mutation), two minor (V3 bare-string
  admission, V4 skipped provider reconciliation), two informational (V5 `reasoning_effort` stripped
  by compaction and unchecked, V6 argv-forced epoch). The maker pass repaired V1, V3, V4, V5, V6 and
  added a fail-closed branch for an unreadable pinned source; V2 was an attribution question, now
  answered.
- **Correction to an earlier draft of this file**: an earlier revision of this evidence text stated
  that the canonical policy file was not modified. That is no longer true and was superseded by the
  declared revision-8 → 9 change recorded in §7(5). The earlier statement is preserved here as an
  erratum rather than silently overwritten.
- **V2 attribution**: the registry mutation the verifier could not attribute was this round's own
  declared `reasoning_effort` append (16:23 local, post-window). It is recorded in
  `evidence/ARTIFACT_ACCOUNT.json`; the EXECUTE receipt was deliberately **not** rewritten, so its
  recorded hashes remain the historical record.
- **Artifact account** (`evidence/ARTIFACT_ACCOUNT.json`): all 25 entries of the EXECUTE receipt's
  artifact table recomputed from disk → 22 match, 3 mismatch, 0 missing. One mismatch is the
  declared revision-9 change; two (`evidence/lane-admission/*/receipt.json`) are flagged as open
  findings and were handed to the independent verifier rather than hidden.
- **Engine deviation**: the repair pass ran in the orchestrator/maker loop, not through Codex CLI as
  the round's preferred EXECUTE engine, because the sealed relay `127.0.0.1:10101` refused
  connections at repair time. Disclosed as a deviation.
- The pre-call authorization mechanism had a real defect that this round found and repaired: its
  token-refresh guard compared turn identifiers as strings and therefore could never refresh an
  expired token, so a later explicit authorization had no effect. The fix is in place and was proved
  by refreshing an expired token; the round's blocks and the diagnosis are recorded in
  `receipts/AUTHORIZATION_RECEIPT.json`.
- Documentation decision (FAR research lane): the operator-facing manual gains a six-line
  troubleshooting pointer at most, not a guard chapter; two candidate patches are staged and
  deliberately **not applied** (`candidate_patch_fda_guide.md`,
  `candidate_patch_guardrail_runtime_notes.md`).
- No pre-existing repository file was modified by the EXECUTE lane: every `git status` modified
  entry carries an mtime outside the lane's 14:46:48–15:09:17 window.
- Two commands were blocked by the sandbox policy during EXECUTE — both malformed PowerShell
  directory listings; no artifact was affected.
- Errata of the orchestrator's own: an early claim that the pre-call classifier was "broader than
  its source" was wrong — the guard behaves exactly as coded, and the blocked calls were blocked for
  the documented markers that the orchestrator's own text contained.
- Open findings carried, not closed: `D19` (binding staleness — found, not fixed), the NVIDIA
  secondary arm's lack of lane-shaped proof, and the promotion-envelope gap (former BL2).

## 9. Artifact digest

97 artifacts, 1,354,277 bytes. Manifest `evidence/EVIDENCE_MANIFEST.json`
sha256 `49b35200a959caa1d7a8ddadbc2ce60973b3c1f7142799a5bcc53ca817efe1a9`. Per-artifact digests are authoritative in the manifest, not here.

## 10. Mirror verification

This file is mirrored to three additional roots and all four copies are asserted byte-identical at
generation time; the assertion result is printed by the freeze step and re-checked by hand.
