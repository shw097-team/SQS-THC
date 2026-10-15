# DOC-11 - Maturity/SRE/Security

> Work order: `WO-TS-REF-11` (`TS-011` Maturity/SRE/security)
> Source authority: `SSOT/SQS-THC_P0-CIP-PACK_v2026.08.06-r2.md` section 17
> `TS-011`, `MC-26` (maturity / paper-shadow / operator operations / SRE /
> security/privacy/identity/rights/supply chain), `CH30` / `CH31` / `CH32`
> Owner: `F28-01/F31-01` - Receiver: SRE and Security Team
> Deliverable: `ART-11`
> Claim ceiling: `LOCAL_DELIVERY` (see section 7)

## 1. Maturity model (`maturity/maturity-model.yaml`, `CH30` / `MC-26`)

- `maturity/maturity-model.yaml` holds the maturity model: ordered levels,
  each with `id`, `name` and `evidence_required`.
- Maturity is a side-effect budget, not a feature checklist. A level is only
  reached when every evidence item required by that level AND every previous
  level is present (each maturity plane has independent evidence AND previous
  plane passed AND rollback rehearsal complete).
- Any promotion to a maturity level without its evidence - for example a
  paper or CI success promoted directly to Live - is NACK'd with exact error
  `ERR_PROMOTION_WITHOUT_EVIDENCE` and performs no mutation (fail-closed).

## 2. SLOs (`sre/slos.yaml`, `CH31` / `MC-26`)

- `sre/slos.yaml` holds service level objectives, each with `id`,
  `slo_target` (a number strictly between 0 and 1) and a `runbook_ref` that
  resolves to a runbook id in `sre/runbooks.yaml`.
- A dangling `runbook_ref`, a non-numeric target, or a runbook whose
  `slo_target` does not equal the referencing SLO is rejected (fail-closed).

## 3. Runbooks (`sre/runbooks.yaml`, `CH31` / `MC-26`)

- `sre/runbooks.yaml` holds runbooks, each with `id`, `slo_target` and
  `runbook_ref` (the procedure anchor: Observe -> Bound -> Contain -> Restore
  -> Reconcile).
- Every runbook defends at least one SLO; a runbook with no defending SLO is
  rejected (fail-closed). An incident is never closed without root
  cause / rollback / readback.

## 4. Security policies (`security/policies.yaml`, `CH32` / `MC-26`)

- `security/policies.yaml` holds security policies, each with `id` and
  `policy` (CH32 / `MC-26` domain: least privilege satisfied AND rights_basis
  approved AND high-risk action has scoped approval_token AND supply chain
  ref verified).
- The security veto is fail-closed: prompt injection, tool poisoning, secret
  exposure or confused deputy input is denied and quarantined, never passed
  to a tool boundary.
- An empty policy list is a valid state (no policy ratified yet is
  admissible), but a policy missing `id` or `policy` is rejected with a
  field-naming error, distinct from `ERR_PROMOTION_WITHOUT_EVIDENCE`.

## 5. Privacy register (`privacy/register.yaml`, `CH32` / `MC-26`)

- `privacy/register.yaml` holds privacy entries, each with `id` and `scope`.
- The register records the bounded privacy scope of every data surface;
  anything outside a registered scope is not collected, retained or linked.
- An entry missing `id` or `scope` is rejected (field-naming error).

## 6. Supply chain pins (`supply-chain/pins.yaml`, `CH32` / TOOL registry)

- `supply-chain/pins.yaml` holds supply chain pins, each with `id`, `tool`,
  `pin` and `status`, in TOOL card format.
- An ADOPT tool carries `pin: UNRESOLVED::TOOL-xx::PIN` and
  `status: BLOCKED_PENDING_QUALIFICATION` until the exact pin is resolved
  with reliable local/dual-source evidence. ADOPT/ADAPT is a design
  selection, not an installation or admission.
- No tool or dependency is executed on an unresolved pin; a pin that claims a
  resolved value while still `BLOCKED_PENDING_QUALIFICATION` is rejected
  (fail-closed).

## 7. Governance, claim ceiling and exact error

- Maturity/SRE/security follows `MC-26` and the illegal transition rule: no
  HumanGate may override a blocking risk/survival/security/rights veto.
  Promotion to a maturity level without the required evidence raises exact
  error `ERR_PROMOTION_WITHOUT_EVIDENCE`; the promotion performs no mutation.
- Claim ceiling is `LOCAL_DELIVERY`: this work order materializes the
  maturity/SRE/security document, the maturity model, SLOs and runbooks,
  security policies, privacy register, supply chain pins and their acceptance
  tests. It does **not** claim `G11` / `G12` / `G13` / `G14` / `G15` passed,
  runtime executed, tool qualification completed, or production readiness.
- Fail-closed semantics: every rejection (`ERR_PROMOTION_WITHOUT_EVIDENCE` or
  a field-naming error) is a no-op - no mutation, no partial write, no broker
  interaction, no network.

## 8. Non-goals

- No autonomous order submission.
- No broker write.
- No production approval authority.
- No unscoped network or secret access.
- No runtime/tool activation without authorization.
- No unsolicited external write.

## 9. References

- `MC-26` (maturity / paper-shadow / operator operations / SRE /
  security/privacy/identity/rights/supply chain) -> `TS-011` / `T-031` /
  `T-032` / `T-033` / `ART-11` / `G11` / `G12` / `G13`
- `CH30` / `CH31` / `CH32` (DOC-11 owned chapters), `SPEC-12`, `SPEC-17`,
  `SPEC-19`, `SPEC-20`, `SPEC-34`, `LGR-18`, `G14`, `G15`,
  `ERR_PROMOTION_WITHOUT_EVIDENCE`