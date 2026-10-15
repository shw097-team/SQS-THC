# DOC-10 - Decision/XQ/Reconciliation

> Work order: `WO-TS-REF-10` (`TS-010` Decision/XQ/reconciliation)
> Source authority: `SSOT/SQS-THC_P0-CIP-PACK_v2026.08.06-r2.md` §17 `TS-010`,
> `MC-24` (decision compiler / XQ/XS read-watch adapter / HITL), `MC-25`
> (execution truth / book of record / pure reducer / reconciliation),
> `CH27` / `CH28` / `CH29`
> Owner: `F25-01` · Receiver: Operations Adapter Lead · Deliverable: `ART-10`
> Claim ceiling: `LOCAL_DELIVERY` (see §5)

## 1. Decision compiler (`CH27` / `MC-24`)

- The decision compiler turns an admitted candidate into replayable,
  human-gated decision artifacts. It is not a strategy performance report and
  it grants no automatic order submission.
- Truth separation is strict: `DecisionArtifact != HumanApproval !=
  ManualHandoff`; `OrderIntent != SubmitAttemptReceipt != BrokerAck !=
  ExecutionEvent != Fill`; `External Fact != Derived Projection !=
  ReconciliationDecision`.
- `CandidateEligibility` requires the conjunction of a `ValidationDecision`,
  a `RiskAuthorization` and a `SurvivalDecision`; `UNKNOWN`, `VETO` or
  `STALE` resolves to `NO_TRADE` (fail-closed).
- Selection is deterministic with an explicit tie-break; every translation
  carries a `TranslationLossReport` - semantics that cannot be expressed
  exactly in the target surface must be listed with materiality, never hidden
  by a successful compile or UI render.
- Any order action requires a `HumanGateRequest` -> `HumanApproval` ->
  `ManualHandoff` chain. Orders are `HITL_ONLY`: there is no autonomous order
  path in this work order. An approval binds an exact digest, scope, expiry
  and revocation; `ManualHandoff` never creates a broker fact.

## 2. XQ read-watch adapter (`adapters/xq-read-watch.yaml`, `CH28` / `MC-24`)

- `adapters/xq-read-watch.yaml` declares the XQ/XS/XScript surface as a
  READ-ONLY watch adapter: `watch_only: true`, `write: false`,
  `broker_write: false`, `autonomous_order_submission: false`,
  `order_path: HITL_ONLY`, `mode: RADAR_ONLY`.
- Allowed operations are `watch`, `read`, `compile` and `radar`. Forbidden
  operations are `submit`, `cancel`, `modify` and `replace`.
- `compile != activation != parity != fill`: a compile receipt, an
  activation decision or a Radar visual match is never a fill, a position, a
  cash balance, PnL or live readiness. The current mode is `RADAR_ONLY`.
- Any autonomous order write path - an adapter with `write: true`, a
  `submit`/`cancel`/`modify`/`replace` operation, or any `order_path` other
  than `HITL_ONLY` - is NACK'd with exact error `ERR_AUTONOMOUS_ORDER_PATH`
  and performs no mutation (fail-closed, no broker write).

## 3. Execution facts (`schemas/execution-fact.schema.json`, `CH29` / `MC-25`)

- `schemas/execution-fact.schema.json` is the execution fact schema. Every
  fact carries exactly the required fields `fact_id`, `ts`, `side`, `qty`,
  `price` and `status`; `side` is `BUY`/`SELL`, `qty`/`price` are strictly
  positive numbers, `status` is `FILLED`/`PARTIAL`/`REJECTED`/`CANCELLED`/
  `UNKNOWN`.
- Execution truth comes only from external broker/clearing facts. UI state,
  compile logs, hashes, CI or package PASS are never promoted to facts.
- Timeout stays `UNKNOWN` and never auto-promotes; a duplicate `fact_id` is
  idempotent; a sequence gap is never guessed - it is surfaced for
  reconciliation.

## 4. Book of record reducer (`reducers/book-of-record.yaml`, `CH29` / `MC-25`)

- `reducers/book-of-record.yaml` declares the book of record: a single truth,
  append-only ledger reduced by a pure, deterministic fold over facts ordered
  by `(ts, fact_id)`.
- Projections (position, cash, PnL) are recomputable from the fact log and
  are never hand-edited; a correction is a NEW event, never an
  UPDATE/DELETE of an existing fact.
- A direct order mutation - an order object fed to the reducer, or an
  update/delete of an existing fact - is NACK'd with exact error
  `ERR_AUTONOMOUS_ORDER_PATH` and performs no mutation (fail-closed).
- Reconciliation compares external facts with derived projections under an
  explicit source precedence and tolerance policy; a critical mismatch
  resolves to `STOP_THE_LINE` / incident handoff rather than a silent
  rewrite.

## 5. Governance, claim ceiling and exact error

- Decision/XQ/reconciliation follows `MC-24` / `MC-25` and the illegal
  transition rule: no HumanGate may override a blocking
  risk/survival/security/rights veto, and no code path may submit, cancel,
  modify or replace an order without human approval. Any autonomous order
  write path raises exact error `ERR_AUTONOMOUS_ORDER_PATH`.
- Claim ceiling is `LOCAL_DELIVERY`: this work order materializes the
  decision/XQ/reconciliation document, the read-only XQ watch adapter, the
  execution fact schema, the book-of-record reducer and their acceptance
  tests. It does **not** claim `G08` / `G09` / `G10` passed, runtime
  executed, broker connectivity, or production readiness.
- Fail-closed semantics: every rejection (`ERR_AUTONOMOUS_ORDER_PATH` or a
  field-naming error) is a no-op - no mutation, no partial write, no broker
  interaction, no network.

## 6. Non-goals

- No autonomous order submission.
- No broker write.
- No production approval authority.
- No unscoped network or secret access.
- No runtime/tool activation without authorization.
- No unsolicited external write.

## 7. References

- `MC-24` (decision compiler / XQ/XS read-watch adapter / HITL) -> `TS-010` /
  `T-028` / `T-029` / `ART-10` / `G08` / `G09`
- `MC-25` (execution truth / book of record / pure reducer / reconciliation)
  -> `TS-010` / `T-030` / `ART-10` / `G10`
- `CH27` / `CH28` / `CH29` (DOC-10 owned chapters), `SPEC-08`, `SPEC-29`,
  `SPEC-16`, `SPEC-18`, `LGR-12`, `ERR_AUTONOMOUS_ORDER_PATH`