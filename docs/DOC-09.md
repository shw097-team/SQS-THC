# DOC-09 - Validation/Risk/Survival Veto

> Work order: `WO-TS-REF-09` (`TS-009` Validation/risk/survival veto)
> Source authority: `SSOT/SQS-THC_P0-CIP-PACK_v2026.08.06-r2.md` §17 `TS-009`,
> `MC-21` / `MC-22` / `MC-23`, `CH24` / `CH25` / `CH26`
> Owner: `F22-01/F23-03/F24-01` · Receiver: Independent Validation and Risk Team
> Deliverable: `ART-09`
> Claim ceiling: `LOCAL_DELIVERY` (see §5)

## 1. Validation runs (`validation/`)

- `validation/` holds validation runs, each with `id`, `spec_ref` and
  `result` (`PASS`/`FAIL`/`ABSTAIN`/`BLOCKED`):
  - `validation/run-ch24-backtest-oos.yaml` - CH24 independent validation
    run (frozen dataset, OOS reproduction, counter-evidence).
  - `validation/run-ch25-limits-stress.yaml` - CH25 portfolio risk limits
    and stress validation run.
  - `validation/run-ch26-survival-guards.yaml` - CH26 Talebian survival
    guard validation run.
- Every run's `spec_ref` anchors to `TS-009` (e.g. `TS-009/CH24`) so the
  run traces to the source authority without leaving the repo.
- A validation run is a *record*: it materializes the outcome of a
  deterministic, fail-closed validation. It performs no broker write and no
  network access.

## 2. Hard risk limits (`risk/limits.yaml`)

- `risk/limits.yaml` holds hard risk limits, each with `id`, `metric`,
  `max` and `hard: true` (CH25 / `MC-22` domain: all exposures within
  limits AND stress_loss <= approved threshold AND kill_state permits
  allocation).
- A hard limit is never overridable: any attempt to bypass it - for
  example a `bypass`/`bypass_enabled` flag on a hard limit, or `hard`
  demoted from `true` - is NACK'd with exact error `ERR_VETO_BYPASS` and
  performs no mutation (fail-closed).
- An empty limit list is a valid state (no hard limits yet ratified is
  admissible), but a limit missing a required field (`id`, `metric`,
  `max`, `hard`) is rejected with a field-naming error, distinct from
  `ERR_VETO_BYPASS`.

## 3. Survival guards (`survival/guards.yaml`)

- `survival/guards.yaml` holds survival guards, each with `id`,
  `condition` and `action` (CH26 / `MC-23` domain: ruin barrier, unknown
  exposure, fragility mandate, blast radius, optionality / via negativa).
- Allowed actions are `VETO`, `BLOCK`, `STOP_LINE` and `ABSTAIN`. An action
  of `SKIP` (or any action outside the allowlist) is a guard bypass and is
  NACK'd with exact error `ERR_VETO_BYPASS`; the guard chain performs no
  mutation (fail-closed).
- A guard missing a required field (`id`, `condition`, `action`) is
  rejected with a field-naming error, distinct from `ERR_VETO_BYPASS`.

## 4. Stress fixtures (`fixtures/stress/`)

- `fixtures/stress/` holds deterministic stress fixtures used by the
  validation/risk/survival acceptance tests:
  - `stress_valid.yaml` - a scenario that must survive (all exposures
    within limits).
  - `limits_empty.yaml` - empty hard-limit list (valid state).
  - `limit_bypass.yaml` - hard limit carrying a forbidden `bypass` flag ->
    `ERR_VETO_BYPASS`.
  - `guard_skip.yaml` - survival guard with action `SKIP` ->
    `ERR_VETO_BYPASS`.
  - `limit_missing_field.yaml` - hard limit missing a required field
    (rejected with a field-naming error).
- The stress runner is deterministic, in-repo, stdlib-only: exposures are
  compared against scenario limits and the outcome must equal the
  fixture's `expected` result. There is no broker write and no network.

## 5. Governance, claim ceiling and exact error

- Validation/risk/survival follows `MC-21` / `MC-22` / `MC-23` and the
  illegal transition rule: any HumanGate must never override a blocking
  risk/survival/security/rights veto; a veto bypass attempt raises exact
  error `ERR_VETO_BYPASS`.
- Claim ceiling is `LOCAL_DELIVERY`: this work order materializes the
  validation runs, hard risk limits, survival guards, stress fixtures and
  their acceptance tests. It does **not** claim `G05` / `G06` / `G07`
  passed, runtime executed, or production readiness.
- Fail-closed semantics: every rejection (`ERR_VETO_BYPASS` or field error)
  is a no-op - no mutation, no partial write, no broker interaction.

## 6. Non-goals

- No autonomous order submission.
- No broker write.
- No production approval authority.
- No unscoped network or secret access.
- No runtime/tool activation without authorization.
- No unsolicited external write.

## 7. References

- `MC-21` (independent validation / method-model risk / backtest /
  capacity / counter-evidence) -> `TS-009` / `T-025` / `T-049` / `ART-09` /
  `G05`
- `MC-22` (portfolio, risk budget, limits, kill, recovery, independent risk
  veto) -> `TS-009` / `T-026` / `ART-09` / `G06`
- `MC-23` (Talebian survival guards) -> `TS-009` / `T-027` / `ART-09` /
  `G07`
- `CH24` / `CH25` / `CH26` (DOC-09 owned chapters), `SPEC-13`, `SPEC-17`,
  `SPEC-18`, `LGR-11`, `LGR-12`, `ERR_VETO_BYPASS`
