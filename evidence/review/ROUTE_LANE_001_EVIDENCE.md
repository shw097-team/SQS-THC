# ROUTE-LANE-001 — single evidence MD

**Subject:** wiring the operator-mandated model SoD routing (PLAN / EXECUTE / VERIFY-SECURITY) onto the
canonical Hermes runtime and the sealed HGK Codex CLI lane, and what that wiring can and cannot be shown
to enforce.

**Control plane:** HG-KSEOS (Shared Spine typed API). **Orchestration plane:** canonical Hermes
(`20261007_010043_d76343`). **Execution worker:** Codex CLI, sealed HGK lane.
**Requirement:** `REQ-LANE-ROUTE-001` (FROZEN). **WorkOrders:** `WO-LANE-ROUTE-001-EXECUTE` (writer=codex),
`WO-LANE-ROUTE-001-VERIFY` (writer=hermes-verify-lane). **Board:** `lane-route-001`.

## 0. Claim ceiling

Routing is **declared and partially wired**; revision 5 adds measured per-lane fallback chains. The EXECUTE hand-off to the Codex CLI sealed lane is
**operational and provider-receipted**, and the lane model set is pinned **at the config surface**. It is
**NOT** an enforced invariant that Codex CLI children can only use one model — an independent lane
falsified that by invoking a de-listed model successfully (F7). No acceptance is claimed for any work
produced under this routing. Production / live / remote: **NOT_CLAIMED**.

## 1. What the operator asked for (frozen wording)

1. SoD scheme — revision 1: PLAN = GPT 6.1 SOL (OpenAI OAuth) → EXECUTE = DeepSeek V4.1 Flash
   (OPENCODE GO) → VERIFY/SECURITY = GPT 6.1 SOL. **Superseded.**
2. SoD scheme — **revision 2 (in force):** PLAN = GPT 6.1 SOL (**OpenAI OAuth**) → EXECUTE = DeepSeek
   V4.1 Flash (OPENCODE GO) → **VERIFY/SECURITY = GLM-5.3 (NVIDIA NIM primary, OPENCODE GO fallback)**.
3. Hermes' default EXECUTE route must hand execution to **Codex CLI**, with Codex CLI and its
   children/sub-agents pinned to **DeepSeek V4.1 Flash (OPENCODE GO)**.
4. A third clause asking that PLAN **and** VERIFY/SECURITY both run on DeepSeek V4.1 Flash was
   **withdrawn by the operator** (it collapses maker and checker onto one model, violating the AGENTS.md
   maker ≠ checker invariant). It is recorded as superseded, not executed.

## 2. Surfaces exercised (each with raw evidence)

| Surface | Status | Raw evidence |
|---|---|---|
| HGK control plane | DONE — spine lineage + lease-gated transitions, fail-closed | `var/lane-route-001/admission_report.json` |
| KANBAN | DONE — board + 10-card gate DAG, assign/claim/heartbeat/comment/complete | `receipts/kanban_cycle.json`, board DB |
| SWARM | DONE — 2 independent delegation lanes (fresh context, VERIFY_ONLY/read-only) | `deleg_dc8bcd60` (task-0, task-1) |
| SWARM (verify-model lanes) | PARTIAL — V2 (opencode-go/glm-5.3) ran and called tools but exceeded its budget before emitting JSON; V1 (nvidia/glm-5.3) produced **no response at all** | `receipts/step6_swarm_verify_lanes.json`; V2's transcript = read_file, read_file, terminal (read-only listing) |
| GSTACK / OPENSPEC | DONE — registry `ACTIVE_SELECTED` = 8/9; `route(flow)` = NATIVE | §5 |
| CODEX | DONE — real spawns on the sealed lane, provider receipt, singleton chain | `receipts/codex_lane_probe_2.json`, `receipts/codex_chain_pin.json` |

### 2.1 Containment false alarm on the verify-model lanes (F13)

The Step-6 receipt records `containment.no_writes_by_lanes = false`: the digest of the watched tree changed
during the lane run. That is **not** a lane violation. V2's own session transcript holds exactly three tool
calls — `read_file`, `read_file`, and a `terminal` call that only listed a directory — with no write tool,
and V1 never produced a response, so it executed nothing. The receipt's own
`out_of_band_violation.config_written_during_run` is `false`. The digest moved because the maker was writing
remediation artifacts into the same watched tree at the same time. The lanes are cleared; the check design
is at fault for watching a tree the maker was still writing.

## 3. Lane assignment as wired

| Lane | Model / provider | How it is enforced |
|---|---|---|
| PLAN | gpt-6.1-sol / openai-codex | `delegation.provider|model`; subagents + auxiliary decomposer/triage |
| EXECUTE | deepseek-v4.1-flash / opencode-go | dispatched to the sealed Codex CLI lane (`default_execute_route=CODEX_CLI_SEALED_LANE`), chain pinned per invocation |
| VERIFY / SECURITY | z-ai/glm-5.3-**flash** / nvidia, fallback **glm-5.3-flash** / opencode-go | declared lane + per-card override; **both arms measured LIVE** |

`model.codex_bin` is set in the canonical Hermes config to the pinned, hash-verified lane binary.
`model.openai_runtime` is **deliberately not set** (F8).

## 3.1 Amended per-lane fallback chains (revision 5)

The operator amended the scheme so every lane carries an ordered fallback chain. **Every arm was measured
before it was declared** — `receipts/fallback_arm_probes.json` plus two Hermes one-shots:

| Lane | Arm | Model / provider | Engine | Measured | Status |
|---|---|---|---|---|---|
| PLAN | primary | gpt-6.1-sol / openai-codex | Hermes | delegation lanes ran on it | LIVE |
| PLAN | fallback_1 | z-ai/glm-5.3 / nvidia | Hermes | `NO_RESPONSE / 75.12s` | **DEAD** |
| PLAN | fallback_2 | glm-5.3 / opencode-go | Hermes | `GLM_FB_OK` / 7 s | LIVE |
| EXECUTE | primary | deepseek-v4.1-flash / opencode-go | sealed Codex CLI lane | provider receipt 200 | LIVE |
| EXECUTE | fallback_1 | deepseek-ai/deepseek-v4.1-flash / nvidia | Hermes provider client | `200 / 32.61s` | LIVE |
| EXECUTE | fallback_2 | gpt-6-luna / openai-codex | Hermes provider client | `LUNA_FB2_OK` / 5 s | LIVE |
| VERIFY | primary | z-ai/glm-5.3-**flash** / nvidia | Hermes | `HTTP 200 / 1.7s` | **LIVE** |
| VERIFY | fallback_1 | glm-5.3-**flash** / opencode-go | Hermes | `FLASH_FB_OK` / 5 s | LIVE |

Control probe: the same NVIDIA endpoint rejected a deliberately invalid credential with
`403 / 0.17s`, so auth *is* checked there and the real credential is fine — the
fault is model-specific (F1, refined below), not a NIM-wide outage.

**Platform limit that shapes this wiring.** Hermes exposes exactly **one global `fallback_providers`
chain** (`agent/auxiliary_client.py`); there is no per-lane fallback surface. The global chain was set to
the ordered union of the mandated arms and read back (7 entries). Per-lane *ordering* is therefore
authoritative in `config/model-lane-assignment.json` revision 5 and only approximated in the global chain.

**The sealed lane keeps one model.** The relay exposes a single provider namespace (`opencode-go`), so the
two EXECUTE fallback arms cannot be Codex lane models; they are Hermes-side arms, declared under
`execute_fallbacks_out_of_lane` in the lane binding. The Codex lane itself stays pinned to its single
sanctioned model (`model_fallbacks` reduced from the stale two-model list to `["deepseek-v4.1-flash"]`),
which is what keeps requirement 2 intact and closes the F4 escape hatch in the binding.

**SoD across all arms.** Executor arms = {deepseek-v4.1-flash (opencode-go), deepseek-v4.1-flash (nvidia),
gpt-6-luna (openai-codex)}; verifier arms = {glm-5.3 (nvidia), glm-5.3 (opencode-go)}. No executor arm
shares a model with any verifier arm, so **maker ≠ checker holds on all 3 × 2 = 6 combinations**. Provider
separation is weaker: it collapses where EXECUTE fallback_1 (nvidia) or PLAN fallback_1 (nvidia) meets the
VERIFY primary (nvidia), and EXECUTE fallback_2 places the executor on the PLAN provider. Those are
recorded as weakenings, not violations — adding fallbacks can only weaken separation, never strengthen it.

### 3.2 VERIFY moved to GLM-5.3-Flash (revision 6)

VERIFY / SECURITY is now **GLM-5.3-Flash**, NVIDIA NIM primary and OPENCODE GO fallback, both measured LIVE
(**HTTP 200 / 1.7 s** and **`FLASH_FB_OK` / 5 s**). The NVIDIA arm is the interesting one: the plain
`z-ai/glm-5.3` route hangs past 75 s while the Flash variant of the same family answers in 1.7 s on the same
endpoint and credential, which is what confines F1 to the non-Flash route. The verifier keeps its model
across a failover (flash on both arms), so the maker != checker separation is unaffected by the change.

## 4. Verification of the EXECUTE lane (live, not from config)

* Sealed-lane probe: `provider_route_confirmed: true`, `provider_status: 200`,
  `provider_request_id: ocx-muwy3otj-1`, `codex_home` = isolated lane home, `process_scoped: true`.
* Singleton-chain write: `write_chain == ["opencode-go/deepseek-v4.1-flash"]`, one attempt (index 0),
  `write_model_used = opencode-go/deepseek-v4.1-flash`, nonce `CODEX_CHAIN_PIN_OK` returned.
* Isolated Hermes smoke for `openai_runtime=codex_app_server`: exit 0 and the marker was produced, but the
  sealed lane recorded **0 new usage rows** → the key did not route the turn (F8).

## 5. GSTACK / OPENSPEC route evidence

```json
{"flow": "lane-route-001-sod-model-routing", "provider": null, "state": null,
 "fallback": null, "final_authority": true, "route": "NATIVE"}
```

`named_methods.ACTIVE_SELECTED` = `gstack.cso, gstack.office-hours, gstack.plan-eng-review, gstack.qa,
gstack.retro, gstack.review, gstack.ship, openspec` (8 of 9 named methods). This version of `route()` returns
no `reason_code` field; nothing was invented to fill the gap. `NATIVE` is a router-lane disposition and
never a licence to skip the execution surfaces.

## 6. Independent verification (segregation that was actually exercised)

Both lanes ran on **gpt-6.1-sol / openai-codex**, i.e. a different model *and* provider from the Codex
executor (deepseek-v4.1-flash / opencode-go). They were told the maker's receipts are CLAIMS, not evidence,
and were forbidden to modify anything. Both returned verdicts **against** the maker's claims.

* `deleg_dc8bcd60` task-0 — **ACCEPTANCE OFFICER: FAIL** (13 API calls).
  Re-derived every artifact; recomputed 9 declared hashes (7 MATCH, 2 MISMATCH); read the live board
  (Status: 10/10 `done`, 0 mismatches) while noting that 2 done cards explicitly say NOT COMPLETE;
  found the revision-3 `effective_wiring` overstated the wiring, the `provider_separation` PASS false on
  the fallback arm, and the acceptance card seeded on the PLAN model. 0 files mutated by the checker.
* `deleg_dc8bcd60` task-1 — **ADVERSARIAL CHALLENGER: UNSUPPORTED** (4 API calls).
  Probed the relay live: `opencode-go/deepseek-v4.1-flash` → 200 (1.14 s);
  **`opencode-go/glm-5.2` (removed from all three model lists) → 200 with usable content**;
  `opencode-go/gpt-5.6-luna` → 400 (ModelProtocolUnsupported, i.e. not an allowlist rejection).
  Conclusion: the lane's model lists are **not** an admission gate.

Every finding the checkers returned was **accepted and acted on**; the maker's artifacts were corrected
to match, rather than the findings being argued down (§7, §8).

## 7. Findings register

12 entries in `var/lane-route-001/FINDINGS_REGISTER.json`. The material ones:

* **F7 (HIGH, OPEN)** — the lane's model lists do not gate the relay's direct completion path; the
  "Codex children may only use deepseek-v4.1-flash" clause is **UNSUPPORTED as an enforced invariant**.
  Independently reproduced by the challenger lane.
* **F8 (HIGH, recorded decision)** — `model.openai_runtime=codex_app_server` is a no-op for
  provider=opencode-go (gated to openai / openai-codex / named custom providers); setting it would also
  remove `delegate_task`, which the SWARM and VERIFY lanes need. Deliberately not set.
* **F4 (HIGH, compensated not fixed)** — the launcher's Write chain still defaults to three models and
  advances on any non-zero exit; compensated at the call site by pinning `-ModelChain`, not repaired in
  `scripts/` (outside the admitted write set).
* **F1 (HIGH, OPEN, provider-side, REFINED in revision 5)** — NVIDIA NIM's `z-ai/glm-5.3` completion path is unreachable (no response after 75 s) while the **same endpoint** serves `deepseek-ai/deepseek-v4.1-flash` with HTTP 200 in 32.6 s on the same credential, and a garbage key is rejected in 0.17 s. The fault is **model-specific**, not a NIM-wide outage. Confirmed three further times by the independent lanes.
  (garbage key → 401 in 0.19 s; real key → hang on the target, its sibling, and the streaming path).
  Confirmed twice more by the independent lanes.
* **F2 (HIGH, REPAIRED)** — the relay was held by the npm-global ocx without the credential in its process
  env; restarted from the pinned runtime through the sanctioned launcher.
* **F9 (MEDIUM, OPEN, tooling)** — the delegation banner reported the subagent model as rejected and "every
  task failed before doing any work" while both children completed (13 and 4 API calls) and `agent.log`
  shows their turns on `model=gpt-6.1-sol provider=openai-codex`. The banner contradicts the log.
* **F3, F6, F10, F11, F12** — stale lane regression test; no `codex_home` config key; the Kanban CLI refuses
  mutation from a delegated child; the acceptance card seeded on the PLAN model; a declared stderr log the
  launcher never creates.

## 8. Corrective actions taken after the independent lanes reported

* `config/model-lane-assignment.json` → **revision 4**: the false `codex_app_server` wiring claims removed,
  `provider_separation` corrected from `PASS` to `PARTIAL` with the fallback-arm collapse stated, the
  acceptance-card deviation recorded, the independent verdicts attached.
* `receipts/codex_write_receipt.json` → the stale declaration labelled **SUPERSEDED** with both hashes; the
  two 0-byte receipts marked **VOID**; the missing declared stderr log explained as a harness defect.
* `receipts/codex_lane_probe_2.json`'s usage digest → labelled as **append-growth** (the declared digest
  matches the historical 2408-line prefix the probe actually read), so the probe evidence stands while the
  whole-file digest is marked stale.

## 9. Artifact index (SHA-256)

| artifact | sha256 | bytes | lines | role |
|---|---|---|---|---|
| `config/model-lane-assignment.json` | `1ae1899562941eaa195af57166c9ddbcda70b516e351f486f4a79c03df298d28` | 7712 | 131 | revision 4 assignment |
| `config/hermes-codex-lane.json` | `60b9c9c5701ab0d7c307a1d8d2b9df56c29e675d4c09780a0199e98ad0f7b931` | 5319 | 70 | sealed Codex lane binding |
| `var/lane-route-001/admission_report.json` | `ac7daeeba0a465eb3da7435d4cb031debde87122219187d68f02f5f5513d398c` | 555 | 16 | HGK admission / spine lineage |
| `var/lane-route-001/FINDINGS_REGISTER.json` | `af2c3bc9121521200456dfdc60676f108b6a61e28fe3a78593239fc8c45cadb1` | 5120 | 104 | 12 findings |
| `var/lane-route-001/receipts/codex_lane_probe_2.json` | `15ac4d92a701ff81a903e8902624c8bb917c59a8c948b83234c3e25041226c2e` | 2447 | 34 | sealed lane provider receipt |
| `var/lane-route-001/receipts/codex_chain_pin.json` | `9bb64336a22b621252550089a5508c11ed69bdd24df4f3a3b23839886b310a61` | 2198 | 39 | singleton chain pin |
| `var/lane-route-001/receipts/codex_write_receipt.json` | `de213cadbf6d8663cf7778d4e325ba0cab3a8e17ecf9ea475bc34d58fb163c8b` | 5080 | 99 | tracked writer receipt (relabelled) |
| `var/lane-route-001/receipts/step5_ocx_child_model_pin.json` | `055857353ca91b5c4febe8043c11bd0beb88635949b838024b1ebbdc511dc682` | 4823 | 85 | child-model pin (config surface) |
| `var/lane-route-001/receipts/step5b_isolated_codex_runtime_smoke.json` | `4ecb3154af2d5b6be72c50f6492475fbd97490eeceda6bc6e01e70416fa03e15` | 2820 | 39 | isolated smoke — F8 evidence |
| `var/lane-route-001/receipts/step6_swarm_verify_lanes.json` | `677e68d00dadc96dfdf676baac7985b236733b69ceb6c7b39d0a1181d986356c` | 1891 | 57 | verify-model lanes (V1 silent, V2 budget-exceeded) |
| `var/lane-route-001/receipts/kanban_cycle.json` | `de5f11dc5383b7942cb0e3aaaa9ee61861e807f9581d7c962114462f748bf1bb` | 7264 | 275 | kanban cycle receipt |
| `hermes/config.yaml` | `c76c2e122bf9869409d533bca0878b7fc050c11ff07399e08f9231839af9a273` | 6417 | 256 | canonical Hermes config |
| `lane/opencodex-hermes/config.json` | `d947a0ce5a98cb218e75d17226bd306ac16ca7cd3997e1a4369a236bc0698c53` | 922 | 35 | isolated relay config (models pinned) |
| `lane/opencodex-hermes/usage.jsonl` | `f423d3b63d6fd054da9741d0a5e162c04d5a64bdf51ad3c597f64a1d2d8316db` | 3085556 | 2453 | relay usage log (append-only; digest truncated to line count at read time) |

Subject artifacts hashed: **14** (14 declared, 0 missing).

Note: `usage.jsonl` is an append-only log; the digest above is bound to the byte length and line count recorded in the same row, which is what makes an append-growth mismatch distinguishable from a fabrication.

## 9.1 Operator decisions recorded after the audits

**OPD-002 — PLAN fallback_1 retained though dead.** Asked whether to swap, drop or keep the dead
`z-ai/glm-5.3` / NVIDIA arm on the PLAN lane, the operator chose to **keep it, declared DEAD**, with PLAN
fallback_2 (`opencode-go/glm-5.3`, measured LIVE at 7 s) carrying the lane in practice. Recorded as accepted
risk `RISK-PLAN-FB1-DEAD` with the mitigation and the review trigger, rather than silently deleted, so the
next reader is told the arm is dead instead of discovering it mid-incident. Consequence stated plainly: a
PLAN-lane failover spends time on a dead arm before succeeding on fallback_2.

## 10. Nonclaims

* No production, release, deployment, live-trading or remote claim.
* No acceptance of any work produced under this routing; no self-issued external verdict.
* No claim that the VERIFY primary (NVIDIA NIM) works — it does not, and the lane ran on its fallback.
* No claim that the EXECUTE lane is forced onto one model for callers that omit `-ModelChain`.
* No claim about Codex **grandchild** behaviour beyond the relay enforcement gap recorded in F7.
* The Step 6 verify-model lanes are reported as they happened (one budget-exceeded but demonstrably
  running, one silent); their partial results are **not** presented as verification.

STOP — maker lane closed. An independent acceptance verdict for this round is NOT issued by the maker.
