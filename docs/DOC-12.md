# DOC-12 - Evidence/Release/Controlled Learning/NRTV

> Work order: `WO-TS-REF-12` (`TS-012` Evidence/release/learning/NRTV)
> Source authority: `SSOT/SQS-THC_P0-CIP-PACK_v2026.08.06-r2.md` section 17
> `TS-012`, `MC-27` (Observability, Evidence, Audit, Provenance, Release
> Integrity, Controlled Learning, Migration/Exit, AIKD and NRTV), `CH33` /
> `CH34` / `CH35`
> Owner: `F34-01/F35-01` - Receiver: Independent Release Team
> Deliverable: `ART-12`
> Claim ceiling: `LOCAL_DELIVERY` (see section 7)

## 1. Evidence ledger (`evidence/ledger.yaml`, `CH33` / `SPEC-16`)

- `evidence/ledger.yaml` holds the evidence ledger: append-only, hash-linked
  entries, each with `id`, `sha256` and `ref`.
- The ledger is the single evidence truth for this work order. Each `sha256`
  must equal the actual SHA-256 digest of the artifact at `ref`; a drift
  raises exact error `ERR_CHECKSUM_MISMATCH` (fail-closed).
- Existing entries are never edited or deleted in place; a correction is a
  new appended entry. File existence/hash/LLM self-review never becomes a
  production PASS (`ERR_EVIDENCE_FORGED`).
- CH33 typed objects `EvidenceReceipt` / `ProvenanceAttestation` enforce
  `artifact_hash verifies AND producer_id != checker_id AND freshness_at
  current AND status_vector preserves plane separation`.

## 2. Release gates (`release/gates.yaml`, `CH33` / `SPEC-17` / `SPEC-34`)

- `release/gates.yaml` holds release gates, each with `id`, `gate` and
  `required` (the exact evidence ids the gate needs from the ledger).
- `G17` (Release/Rollback/Readback) and `G18` (NRTV/Replacement) are the
  release plane; both stay `NOT_RUN` until their required evidence is
  present. Release admission is gate-checked, never self-declared.
- Claiming `PRODUCTION` without the required release AND NRTV evidence - for
  example a release gate claiming `PRODUCTION` without required evidence -
  is NACK'd with exact error `ERR_PRODUCTION_CLAIM_INFLATION` and performs
  no mutation (fail-closed). Local delivery can never imply runtime, NRTV or
  production.

## 3. Migration plans (`migration/plans.yaml`, `CH34` / `SPEC-31`)

- `migration/plans.yaml` holds migration plans, each with `id`, `from`, `to`
  and `status`.
- Migration follows `PROPOSED -> COMPATIBILITY_ANALYZED -> DUAL_RUN ->
  CUTOVER -> SUNSET/ROLLBACK`; a plan without an explicit rollback path is
  rejected with `ERR_MIGRATION_NO_ROLLBACK` (fail-closed). No migration
  activates without consumer ACK and a rehearsed previous-active rollback.

## 4. NRTV config (`nrtv/config.yaml`, `CH35` / `SPEC-35`)

- `nrtv/config.yaml` holds NRTV configuration, each with `id`,
  `runtime_window` and `condition`.
- NRTV is target-only and independent: frozen question set, blind run,
  no-return-to-source proof, retrieval locator accuracy, semantic parity and
  an independent evaluator identity. A self-judged NRTV pass is rejected
  (`ERR_NRTV_SELF_JUDGE` / `ERR_SELF_NRTV`, fail-closed).

## 5. Training runs (`training/runs.yaml`, `CH35`)

- `training/runs.yaml` holds training runs, each with `id`, `model_ref` and
  `status`.
- A training packet (`TrainingPacket`) is only built after an independent
  NRTV run of the source packet; `NOT_RUN` / `DESIGN_CLOSED_NOT_RUN` are the
  honest ceilings until an external receipt exists. No self-declared PASS.

## 6. Controlled learning / AIKD (`CH34` / `CH35`)

- `DriftSignal` / `LearningCandidate` require change evidence AND CR approval
  AND migration/rollback defined AND consumer ACK before deprecation; silent
  self-modification is rejected with `ERR_SELF_MODIFICATION` /
  `ERR_DRIFT_UNCALIBRATED` (fail-closed).
- `SourceToAnchorRow` / `ChapterClosureCard` / `ProbeCase` / `NRTVRun` /
  `TrainingPacket` require a resolving source anchor, a substantive excerpt,
  an existing target rule and a probe whose expected anchor answers without
  raw source comeback (`ERR_RAW_STUFFING` / `ERR_SOURCE_COMEBACK`).

## 7. Governance, claim ceiling and exact error

- Evidence/release/learning/NRTV follows `MC-27` and the illegal transition
  rule: no HumanGate may override a blocking risk/survival/security/rights
  veto. Claiming `PRODUCTION` without the required NRTV and evidence raises
  exact error `ERR_PRODUCTION_CLAIM_INFLATION`; the claim performs no
  mutation.
- Claim ceiling is `LOCAL_DELIVERY`: this work order materializes the
  evidence ledger, release gates, migration plans, NRTV config, training
  runs, `docs/DOC-12.md` and their acceptance tests. It does **not** claim
  `G16` / `G17` / `G18` passed, runtime executed, independent NRTV run,
  release admission or production readiness.
- Fail-closed semantics: every rejection (`ERR_PRODUCTION_CLAIM_INFLATION`,
  `ERR_CHECKSUM_MISMATCH` or a field-naming error) is a no-op - no mutation,
  no partial write, no broker interaction, no network.

## 8. Non-goals

- No autonomous order submission.
- No broker write.
- No production approval authority.
- No unscoped network or secret access.
- No runtime/tool activation without authorization.
- No self-judged NRTV, release admission or production PASS.

## 9. References

- `MC-27` (observability / evidence / audit / provenance / release
  integrity / controlled learning / migration-exit / AIKD / NRTV) ->
  `TS-012` / `T-034` / `T-035` / `T-036` / `T-048` / `T-049` / `T-050` /
  `ART-12` / `G16` / `G17` / `G18`
- `CH33` / `CH34` / `CH35` (DOC-12 owned chapters), `SPEC-16`, `SPEC-17`,
  `SPEC-31`, `SPEC-34`, `SPEC-35`, `LGR-19`, `LGR-20`,
  `ERR_PRODUCTION_CLAIM_INFLATION`
