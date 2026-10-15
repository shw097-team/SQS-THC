# DOC-00 — SQS-THC Product Constitution

> Work order: `WO-TS-REF-01` (`TS-001` Product constitution & DOC skeleton)
> Source authority: `SSOT/SQS-THC_P0-CIP-PACK_v2026.08.06-r2.md` §17 `TS-001`, §11 `SPEC-01`, §15 `ART-01` (gitignored, read-only corpus)
> Owner: `F01-01` · Receiver: GPT B Product/Docs Lead · Deliverable: `ART-01`

## 1. Product identity (SPEC-01)

| Field | Value |
|---|---|
| product_id | `SQS-THC` |
| formal_name | `SQS-THC & TW-ICT FSDT Stack` |
| internal_name | `sqs_thc` |
| namespace | `sqs.ict.twhc` |
| version | `2026.08.10-r1` |
| supersedes | none (initial constitution) |
| aliases | none |
| non_goals | see §3 |

## 2. Identity-unique invariant and exact error

- Namespace is the identity key: a product namespace MUST be unique inside the
  product registry (`SPEC-01` domain invariant; duplicate namespace fails `G00`).
- Registering a second product with an already-registered namespace is a
  duplicate-namespace mutation. Exact error on duplicate namespace:
  `ERR_PRODUCT_ID_COLLISION` (fail-closed; no mutation, no partial write).
- A deprecated alias MUST NOT be promoted as a new product_id; only one active
  product root exists for namespace `sqs.ict.twhc`.
- Owner/version/source/evidence hash required; secrets prohibited
  (`SPEC-01` security/permission clause).

## 3. Non-goals

- No autonomous order submission.
- No broker write.
- No production approval authority.
- No unscoped network or secret access.
- No runtime/tool activation without authorization.
- No unsolicited external write.

## 4. SPEC-01 state model

```text
PROPOSED->IDENTITY_UNIQUE->HUMAN_RATIFIED->ACTIVE->SUPERSEDED
```

Constitution version `2026.08.10-r1` is materialized at `PROPOSED`
(design contract materialized; human ratification pending).

## 5. Materialized contracts (TS-001 target set)

- `contracts/product/PRODUCT_CONSTITUTION.yaml` — SPEC-01 fields + state model
- `requirements/MC_REGISTRY.yaml` — MC registry, unique IDs `MC-01..MC-27`
- `architecture/DOC_CH_OWNER_MAP.yaml` — chapter -> owner map (`CH00..CH35`)
- `docs/DOC-01.md` — intent / requirement / financial change document

