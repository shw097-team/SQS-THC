# MVLT A/B Experiment Evidence — Bounded-Repair Closure (v2, FINAL)

- **Generated (freeze order LAST)**: 2026-08-24T02:28:45.143461+00:00
- **Project**: MVLT-AB-20260824 (HGK Shared Spine; state EXECUTING at 2026-08-24T02:10:50Z)
- **WorkOrders**: WO-TS-20260824-01 / WO-TS-20260824-02 (admitted pre-execution)
- **Input**: var/mvlt/input.json SHA-256 `d1139e357adc060eaa4c6027ce361e665add0d5097f2311981aa11e190955551`
- **Model/Provider**: deepseek-v4-flash via opencode-go (both modes)
- **Plan**: .hermes/plans/2026-08-23_governed-vs-bare-mvlt.md v2 hardened (challenge FINDINGS M1–M6 folded)

## 1. Execution surfaces closed (bounded repair, user-approved Option A)

| Surface | Evidence | Status |
|---|---|---|
| HGK admission | Spine project REQ→TS→WO lineage; state WORKORDERS_ADMITTED→EXECUTING | CLOSED |
| Kanban board+DAG | board `mvlt-ab`, 10 tasks, 19 task_links edges | CLOSED |
| Kanban claim/complete loop | kanban_closure_receipt.json — 8 run/swarm tasks assign/claim/heartbeat/complete all rc=0 | CLOSED |
| Swarm ≥2 genuine lanes | deleg_2ed200be (Lane A) + deleg_ef2634b6 (Lane B), live logs, parallel overlap ~10:12–10:16 | CLOSED |
| AO fresh-context lane | deleg_4820f355 → **ACCEPTANCE_OFFICER_VERDICT=PASS** (345.58s, incl. spine readback + phrase-scan of claims) | CLOSED |
| Single MD freeze + mirrors | this file, written LAST, byte-identical ×3 roots | CLOSED |

## 2. Measurements (N=3 per mode, median)

| Metric | Mode A (pure Hermes, ephemeral home) | Mode B (canonical Hermes governed round) |
|---|---|---|
| wall_clock runs (s) | 67.44 / 25.35 / 15.43 | 16.69 / 23.52 / 16.51 |
| median wall_clock (s) | **25.35** | **16.69** |
| schema_ok | 3/3 true | 3/3 true |
| digest_match (computed==input SHA) | 3/3 true | 3/3 true |
| model recorded | deepseek-v4-flash ×3 | deepseek-v4-flash ×3 |

- **Median ratio B/A = 0.658**, exact-resample bootstrap **90% CI [0.245, 1.524]** (729 resample combinations; CI contains 1.0).
- Independent rederivation: Swarm Lane B recomputed medians/ratio/CI/mirror hashes from raw files without trusting embedded values → matched.

## 3. Governance cost quantification (this round, measured)

- **Kanban full-DAG claim/complete overhead (t0 fixed cost): 26.99 s for 8 tasks** (~3.37 s/task, subprocess CLI path).
- Admission (Spine REQ→TS→WO + lifecycle transitions): performed pre-measurement; not included in the 26.99 s figure.
- Swarm dual-lane verification: Lane A 223.95 s, Lane B 205.62 s wall each (parallel; not additive to critical path beyond max ≈ 224 s).
- AO verdict round: 345.58 s.

## 4. Findings on the ORIGINAL research question ("性能和表現是否有實際差異?")

1. **Core artifact performance/quality: NO attributable difference.** Both modes produced byte-correct artifacts at the same correctness rate (6/6). Ratio point estimate favors B but CI includes 1.0 and the fresh-vs-warm-home confound (declared in plan §9-M1) forbids causal attribution.
2. **Governance does NOT slow model inference**: artifact generation speed is provider-bound, identical route both modes. Governance adds *orchestration* costs around the model (quantified §3), not inside it.
3. **Process integrity IS structurally different** — and this experiment itself demonstrated it live: an earlier execution round claimed governance but silently skipped Kanban/Swarm/evidence surfaces; the governed pipeline's independent AO lane DETECTED that drift (deleg_f6df44d5 FINDINGS). Bare Hermes has no mechanism that can catch such drift. This is the actual, evidenced behavioral difference between the two modes.
4. **Traceability**: Mode A leaves zero auditable lineage by design; Mode B leaves REQ→TS→WO→Kanban events→Swarm logs→AO verdict→this frozen MD (verifiable chain, all receipts on disk).

## 5. Claim ceiling (honest, per plan §9-M5/M6)

- CLAIMED: under this confound structure, with N=3 observational samples, no substantive difference in artifact correctness or core-task speed was found; governance overhead is measurable and itemized above; traceability lineage is complete for Mode B only.
- NOT CLAIMED: "governance causes speed/difference"; "no significant difference" (absence-of-evidence phrasing prohibited); statistical significance (no formal test at N=3); production/FDA/trading/live-broker readiness; external meta acceptance.
- Decision rule outcome (§9-M6): ratio CI [0.245, 1.524] crosses both the equivalence band upper bound region and 1.0 → **INCONCLUSIVE on performance difference** (correctness baseline PASS both modes).

## 6. Raw receipt index

- var/mvlt/input.json (`d1139e357adc060eaa4c6027ce361e665add0d5097f2311981aa11e190955551`)
- var/mvlt/mode_a/metrics_mode_a.json · mode_b/metrics_mode_b.json (+ 6 artifacts)
- var/mvlt/kanban_closure_receipt.json
- var/mvlt/swarm_receipt.json + cache/delegation/live/deleg_2ed200be/task-0.log + deleg_ef2634b6/task-0.log
- AO: cache/delegation/live/deleg_4820f355/task-0.log (final JSON: ACCEPTANCE_OFFICER_VERDICT=PASS)
- Prior-round drift finding: deleg_f6df44d5 (FINDINGS — execution-method gap, repaired this round)

## 7. Nonclaims

No strategy, trading, FDA, production, or live-broker outcomes are claimed or implied. This is a governance-stack micro-benchmark only.
