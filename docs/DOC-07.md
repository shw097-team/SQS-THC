# DOC-07 — Investment Mission & Factor Research

> Work order: `WO-TS-REF-07` (`TS-007` Investment mission and factor research)
> Source authority: `SSOT/SQS-THC_P0-CIP-PACK_v2026.08.06-r2.md` §17 `TS-007`,
> `CH18` (investment mission / universe / research governance / committee /
> capacity budget), `CH19` / `CH20` (technical and factor research)
> Owner: `F18-01` · Receiver: Quant Research Lead · Deliverable: `ART-07`
> Claim ceiling: `LOCAL_DELIVERY` (see §4)

## 1. Investment mission

- `research/mission.yaml` — the canonical investment mission (`MC-18` / `CH18`).
- The mission fixes the research **denominator** before any factor work starts:
  a research candidate is admissible only when it belongs to the mission
  `universe_version`, satisfies `mandate_constraints`, stays within a
  nonnegative `capacity_budget`, and is only promoted while the
  `committee_decision` is active.
- Acceptance predicate (CH18): `candidate belongs to universe_version AND
  mandate_constraints satisfied AND capacity_budget nonnegative AND
  committee_decision active`.
- The mandate is a **research** mandate: it scopes what may be researched and
  delivered, not what may be traded or executed.

## 2. Tradable universe

- `research/universe.yaml` — the tradable universe (`MC-18` / `CH18`).
- Every universe entry carries `id`, `symbol`, `tradable: true` and a
  `data_source`. An entry without the `tradable` flag is a mandate violation:
  it claims universe membership without satisfying the tradability gate.
- Entries are point-in-time candidates of the current `universe_version`;
  universe constituents may not silently change during an experiment
  (CH18 edge: `ABSTAIN_OR_DEGRADED_WITH_TT`).

## 3. Factor research

- `research/factors/` — typed factor definitions (`MC-19` / `CH20`), each with
  `id`, `source`, `definition` and `guard`:
  - `factor-momentum` — cross-sectional trailing 12-month total return rank;
    lookback window frozen at `signal_time`; PIT-aligned prices; restatement
    lookahead prohibited.
  - `factor-reversal` — cross-sectional 5-day return reversal rank; liquid,
    tradable constituents only; bid-ask / cost-adjusted returns.
  - `factor-liquidity` — cross-sectional average daily turnover rank; frozen
    volume/spread lookback; tradability gate checked before ranking.
- A factor definition **must** carry a source reference. A factor without a
  source cannot be adopted into the research mandate.
- Factor research is grounded in `CH20`: `fundamental_asof <= decision_time`,
  holdings PIT-valid, neutralization residual within tolerance, turnover within
  budget — no lookahead, no restatement leakage into historical ranks.

## 4. Governance, claim ceiling and exact error

- Research governance follows `CH18`: mission → universe → budget → committee
  review; any illegal transition is NACK'd and any blocking
  risk/survival/security/rights veto is never overridden by a HumanGate.
- Claim ceiling is `LOCAL_DELIVERY`: this work order materializes the mission,
  universe and factor definitions plus their validation tests. It does **not**
  claim `G05` passed, runtime executed, or production readiness.
- Fail-closed semantics: any artifact that violates the mandate (factor without
  `source`, universe entry without `tradable`, claim ceiling overreach) raises
  `ERR_MANDATE_VIOLATION` and performs no mutation. Missing required fields are
  rejected with a field-naming error (fail-closed, distinct from a mandate
  violation).

## 5. Non-goals

- No autonomous order submission.
- No broker write.
- No production approval authority.
- No unscoped network or secret access.
- No runtime/tool activation without authorization.
- No unsolicited external write.

## 6. References

- `MC-18` (investment mission / universe / research governance / committee /
  capacity budget) → `TS-007` / `T-019` / `ART-07` / `G05`
- `MC-19` (ICT / technical analysis / patterns / fundamentals / breadth /
  factors / stock selection) → `TS-007` / `T-020` / `T-021` / `ART-07` / `G05`
- `SPEC-10`, `LGR-05`, `G05` (TS-007 dependencies)
