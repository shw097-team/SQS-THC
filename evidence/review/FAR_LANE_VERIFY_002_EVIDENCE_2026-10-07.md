# FAR round FAR-LANE-VERIFY-002 - single evidence file

- Requirement: `REQ-FAR-LANE-VERIFY-002` (FROZEN in the Shared Spine)
- Board: `far-lane-verify-002` (13 cards) | Admission: `TS-...-EXECUTE`/`TS-...-VERIFY` ADMITTED, `WO-...-EXECUTE` (writer=codex) and `WO-...-VERIFY` (writer=hermes-verify-lane) CREATED
- Generated: 2026-10-07T13:56:58+08:00 | Artifacts bound: 83 files / 6094524 bytes
- Evidence manifest: `evidence/EVIDENCE_MANIFEST.json` sha256 `b3be94d5c40207650c34b5f9b8078d5a0235c4a7c2c989158bcfbcbee4918b1f`
- Policy file as frozen: `config/model-lane-assignment.json` revision 8 sha256 `e9480d1eb8cc10bfdd7187dd15e856eceaad47a6218ff041266d509c25317755`
- `canonical_events` at freeze: **932**

> This file was generated LAST, after every artifact it binds, and then mirrored byte-identically to three further roots. Nothing in it is an acceptance: the round's ceiling is NO_SUBJECT_STORE_MUTATION plus the enumerated write ledger below.

## 1. What the round settled

**Root cause of the maker/checker collapse.** The prior governed round's alleged independent verification was executed inside the orchestrator's own main loop: runtime log lines for session `20261007_004622_88f655` report `model=deepseek-v4.1-flash provider=opencode-go` on every call, and the executor receipt seals the same model. Configured delegation and lane-policy models do not reroute a terminal call executed by the main loop, so maker and checker ran on one model. Independently confirmed by the verifier (K1).

**A probe that reports an arm live is not evidence the arm can serve as a lane.** The NVIDIA arm of the mandated model `z-ai/glm-5.3-flash` answers a direct completion (HTTP 200 in 5.27 s) yet two subagent turns on that arm never completed a model call: `deleg_2a2f7429` reached 9 api calls and stalled 599.3 s waiting for a response, `deleg_7bd21075` stalled on its FIRST call and was stopped at 1,800.99 s with 3 api calls. The same task on the other provider completed in 158.9 s.

**The plain non-Flash sibling.** A raw short probe returns `finish_reason=length` with empty visible content because reasoning consumes the budget; with thinking disabled all four arms answered 200/OK in 2-3 s, including the plain sibling on NVIDIA. The earlier 'the model is unreachable' framing is therefore too strong and is restated as an open contradiction between a transport timeout and a thinking-mode/budget interaction. (Verifier finding, carried in `ledger/ContradictionLedger.tsv`.)

**A routing fact encoded at four sites.** The verify supply is written in `sod`, `assignment[]`, `lane_chains` and historical keys. An edit to `sod` alone leaves the file self-contradicting, which is what the verifier caught (verdict PARTIAL) and what most likely produced the earlier flash/non-flash drift in the same file.

## 2. The operator-directed supply change

`config/model-lane-assignment.json` revision 7 -> 8: `sod.verify_security_lane` moved from `nvidia / z-ai/glm-5.3` to `opencode-go / glm-5.3-flash`; the NVIDIA arm is retained only as a declared secondary and is recorded as `ANSWERS_A_DIRECT_COMPLETION_ONLY`. After the verifier's PARTIAL verdict, `assignment[].VERIFY_SECURITY` and `lane_chains.VERIFY_SECURITY` were swept as well (old text preserved under `VERIFY_SECURITY_previous_revision_8`). Before `0b158cf5...`, final `e9480d1eb8cc10bfdd7187dd15e856eceaad47a6218ff041266d509c25317755`. Backup and rollback: `backup/model-lane-assignment.rev7.json` (byte-for-byte restore). Receipts: `evidence/PROVIDER_SUPPLY_CHANGE_RECEIPT.json`, `evidence/PROVIDER_SUPPLY_CHANGE_SWEEP.diff`, `evidence/VERIFIER_FINDING_DISPOSITION.json`.

The lane's remaining obligation then ran ON the new supply: `deleg_9966296a`, session `20261007_133742_33767d`, `model=glm-5.3-flash provider=opencode-go`, completed in 158.9 s with verdict PARTIAL (K1 confirmed, K2 PARTIAL with a verified counterexample, K3 confirmed) alongside a second artifact from the same lane carrying the lenient reading (PASS with caveats). Both artifacts are preserved verbatim and neither was rewritten; the stricter verdict is the operative one.

## 3. The three landable remediations

(a) Admit the candidate repair set (`var/staging/hgk-r13r14/_exec/r13r14.patch`, 52,632 B, 19 files) as a TaskSpec plus WorkOrder, apply it inside an admitted isolated worktree, run the suite, then take an independent check from a different model. (b) Route the verify lane by pointing the delegation route at the mandated model for the duration of the dispatch and restoring it afterwards — now with the supply set to OPENCODE GO as its standing primary — and, where a board drives the dispatch, use the per-task override (`kanban create --model/--provider`, mapped at `kanban_db_dispatch.py:2694`). (c) Re-verify D15/D16 on the canonical store only after the hermeticity repair lands, otherwise run against an override store and say so. Full text: `lanes/lane_c_solution.*`, `openspec/changes/lane-verify-routing-remediation/`.

## 4. Governance surfaces and receipts

| Surface | Receipt |
|---|---|
| HGK admission | `admit.py`, spine readback (REQ FROZEN, 2 TS, 2 WO) |
| Kanban | board `far-lane-verify-002`, 13 cards, receipts in the round |
| Swarm | PLAN lanes `deleg_914b6fc6`; verify attempts `deleg_2a2f7429`, `deleg_7bd21075`, `deleg_f81c3971`, `deleg_9966296a` |
| Codex CLI | `codex/spawn_receipt.txt` (74 cmd, 0 blocked), `spawn2_receipt.txt` (136 cmd), `spawn3_receipt.txt`; `attempt1_relay_down/` preserves the relay-failure attempt |
| GSTACK | `evidence/GSTACK_ROUTE_RECEIPT.json` (per-role dispositions; named absence of `method_router.py`) |
| OpenSpec | change `lane-verify-routing-remediation`, `openspec validate --strict` -> valid; named absence of `spec_adapter.py` |

## 5. Claim ceiling and write ledger

Ceiling: **NO_SUBJECT_STORE_MUTATION** — the spine's research and forensic stores were not written — PLUS the following enumerated writes:

1. Control-plane audit rows appended by admission (`canonical_events` 931 -> 932).
2. The kanban board store and its cards/events (13 cards, 51+ task events).
3. This run directory (`var/far-lane-verify-002`, incl. backups, attempts and receipts).
4. The sealed Codex lane home, refreshed by launcher starts (`opencodex-catalog.json`, `config.toml`).
5. Runtime session/tool/delegation persistence under the Hermes home, plus agent.log.
6. **ONE tracked canonical configuration file edited on operator instruction**: `config/model-lane-assignment.json` rev7 -> rev8 (+ four-site sweep). Backed up, diffed, reversible.

Not claimed: historical write-trace completeness; whole live-runtime byte immutability; any acceptance, promotion, production or live-service effect; any Stage-3 activity.

## 6. Defects and errata carried by this round

| # | Item | Status |
|---|---|---|
| E1 | Verifier wrote two artifacts with different verdict words for one job | Disclosed, both preserved, stricter one operative |
| E2 | Two verify attempts never completed a model call on the NVIDIA arm | Recorded with transcripts; cause = lane request shape, not raw reachability |
| E3 | The relay process was killed mid-round, so an EXECUTE packet failed loudly (os error 10061) | Attempt preserved; relay restarted and verified |
| E4 | The gate checker scans its own previous output, producing self-referential violations | Named; historical record in `EXECUTE_REPORT.md` left unlaundered |
| E5 | A maker citation used a bare filename and a run-dir-relative receipt path | Repaired to absolute paths; pre-repair record kept |
| E6 | Orchestrator path errata (staging clone path, two citation slips in its own receipt) | Corrected and disclosed |
| E7 | Policy file encoded the routing fact at four sites | Root cause recorded; all active sites swept |
| E8 | Codex packet 2 artifacts predated the supply change | Detected by timestamp/content check; refreshed in packet 3 with pre-refresh copies preserved |

## 7. Artifact digests

Full list: `evidence/EVIDENCE_MANIFEST.json` (
`b3be94d5c40207650c34b5f9b8078d5a0235c4a7c2c989158bcfbcbee4918b1f`). Largest / most load-bearing:

| Artifact | Bytes | sha256 |
|---|---|---|
| `codex/codex2_events.jsonl` | 3020668 | `e93bc5d6bbafc547afcdc9aa...` |
| `lanes/lane_b_claim_ceiling.json` | 714619 | `8306a504e09ede95afded1b2...` |
| `retrieval/SpineFtsHits.tsv` | 468278 | `a284399c412d4b6dac5cd6e2...` |
| `evidence/gate_check.json` | 453640 | `25287f4345d81473ad4a146d...` |
| `retrieval/SourceSnapshotLedger.tsv` | 275523 | `2ab6d00567cfa3cb360b222a...` |
| `codex/codex3_events.jsonl` | 260794 | `a167e38be28ba7dc82069428...` |
| `codex/codex_events.jsonl` | 236441 | `d68e6e1860b9ab0bb24ee3f6...` |
| `lanes/lane_b_claim_ceiling.md` | 135298 | `d40b40317a59ad0847dcb4cc...` |
| `lanes/lane_c_solution.json` | 52553 | `0e59e98a8826065be00e9a47...` |
| `lanes/lane_c_solution.md` | 44850 | `12aed571f582eae722c807d5...` |
| `lanes/attempts/lane_v1_transcript_INTERRUPTED.log` | 26353 | `e06ee2b842febc51a9c01f00...` |
| `retrieval/far_retrieval_lv002.py` | 24122 | `afeaab69d86fa92ae1747367...` |
| `lanes/lane_a_routing_facts.json` | 22419 | `0839cc8d726fe4efac33f502...` |
| `product/ResearchRunReceipt.json` | 18161 | `07530d2a48ec6db168dae41a...` |

## 8. Mirror verification

This file is byte-identical at: the round directory, `HG-KSEOS/evidence/review`, `Fabric/evidence/review`, `SQS-THC/evidence/review`.

```
STOP - FAR round FAR-LANE-VERIFY-002: research complete, remediation designed and received as a
candidate; the supply change is applied and reversed-able; independent verification was obtained
from the mandated model on the new supply. Nothing here is accepted.
```
