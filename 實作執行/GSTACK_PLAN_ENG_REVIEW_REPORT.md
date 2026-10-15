# GSTACK REVIEW REPORT — HGK-REFERENCE-PROJECT-001 (advisory)

- Skill: gstack plan-eng-review (selected slice via named-method router `route("plan")` → `gstack.plan-eng-review` CERTIFIED)
- Mode: headless advisory (GSTACK_HEADLESS=1); final_authority=false; release authority stays with HG-KSEOS
- Review target: SQS-THC & TW-ICT_FSDT-Stack construction plan (15 P0-CIP TaskSpec WorkOrders, admission evidence SQS-THC_WORKORDER_ADMISSION.json)

## Step 0 — Scope Challenge

1. **Existing code reuse**: PRIMARY_ENGINEERING_BASELINE disposition complete (6 subsystems: REUSE×2 / ADAPT / PATCH / MIGRATE / QUARANTINE). ICT-OBI runners/scripts + TriRAG store + Spartoi-AgentOS RBWI are captured rather than rebuilt — no parallel implementation base.
2. **Minimum change set**: 15 TaskSpec families derive directly from P0-CIP MC registry (TS-001..TS-015); no invented scope.
3. **Complexity check**: 15 WorkOrders > 8-file smell threshold. Mitigation: each WorkOrder is a family-scoped contract with writer=codex + raw/independent evidence; execution is wave-sequenced by dependency (kernel → data → knowledge → harness → release). **Finding G1: recommend sequencing gates rather than parallel fan-out — the Kanban board has no dependency edges yet (P2).**
4. **Search check**: no new frameworks introduced; reuse-first disposition; built-in Shared Spine / Hermes Kanban / Codex CLI used. WebSearch unavailable (network-off policy) — proceeding in-distribution.
5. **Completeness check**: P0-CIP requires 50 tests / 19 gates / 15 TaskSpecs — plan admits all 15; acceptance closure must not shortcut T-001..T-050 coverage to existence checks (P1: ensure acceptance executors are depth-calibrated, not symbol-presence).
6. **Distribution check**: deliverable is LOCAL_DELIVERY package (zip + manifest + readback), production NOT_CLAIMED. Distribution pipeline = package_local + TST-092 readback — in scope.

## Section 1 — Architecture review

- A1 (conf 8): Reuse-first baseline is sound; ICT-OBI ADAPT must keep contract kernel (MC-04) separate from legacy runners to avoid leaking 1.2GB duckdb into delivery package. Recommend explicit package include/exclude list.
- A2 (conf 6): Knowledge preload used Shared Spine KnowledgeFactory (354 docs promoted, FTS searchable, withdrawable) — no second SSOT. Good.
- A3 (conf 5): Non-git target (SQS-THC) — candidate identity must use deterministic file-set hash manifest, not git HEAD.

## Section 2 — Code quality review

- Q1 (conf 7): WorkOrder writers are `codex` with `--sandbox workspace-write`; Windows sandbox cannot CREATE new files — pre-seed skeleton files in the worktree base commit before Codex fills them (known OpenCodex route constraint).
- Q2 (conf 6): Evidence contract per WorkOrder must record raw + independent receipts with sha256; summary-only closure is forbidden.

## Section 3 — Tests review

- T1 (conf 8): Acceptance must cover positive/negative/boundary per TaskSpec family with deterministic executors; 50 baseline tests from P0-CIP T-001..T-050 are the denominator source, computed from corpus, never hardcoded.
- T2 (conf 6): Financial/data/model-risk domains need real runtime probes (fixtures + oracles), not file-existence checks.

## Section 4 — Performance review

- P1 (conf 7): Full-corpus inventory (161,099 files / 8.8GB hashed) is one-time; keep it out of the delivery package and out of the hot test path.
- P2 (conf 5): Kanban dependency graph should link kernel → downstream families to prevent parallel writes to the same target tree.

## Verdict

NOT_READY (advisory) — 2 P2 findings actionable before first execution wave: (1) Kanban dependency edges, (2) package include/exclude list. Neither is release-blocking; HGK canonical acceptance remains the final authority.
