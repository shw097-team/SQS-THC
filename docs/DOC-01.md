# DOC-01 — Intent / Requirement / Financial Change

> Work order: `WO-TS-REF-01` (`TS-001`) · Owner: `F01-01` · Receiver: GPT B Product/Docs Lead
> Source authority: `SSOT/SQS-THC_P0-CIP-PACK_v2026.08.06-r2.md` §17 `TS-001` (gitignored, read-only)

## 1. Intent

- `product_id`: `SQS-THC`; `formal_name`: `SQS-THC & TW-ICT FSDT Stack`;
  `namespace`: `sqs.ict.twhc`; version `2026.08.10-r1` (see `DOC-00.md`).
- Upper product family: `SQS`; distribution type: `REFERENCE_DISTRIBUTION`
  (`CH01` acceptance predicate: `product_id='SQS-THC' AND upper_product_family='SQS'
  AND distribution_type='REFERENCE_DISTRIBUTION'`).
- Pain: fragmented identity/authority/requirement sources with no single
  canonical constitution; the P0-CIP pack defines design contracts but the
  repo-side artifacts were `PROPOSED_NOT_MATERIALIZED`.
- Outcome: one canonical product constitution plus a DOC skeleton
  (identity, MC registry, chapter/owner map, intent/requirement/financial
  change) materialized as the `ART-01` Product & Authority Constitution Pack.

## 2. Requirement

- `requirements/MC_REGISTRY.yaml` — canonical MC registry, unique IDs
  `MC-01..MC-27` (domain semantics per SSOT §3.2, not ID-order pairing).
- `architecture/DOC_CH_OWNER_MAP.yaml` — chapter -> owner map covering
  `CH00..CH35` (36 protected H1 chapters; DOC-00 owns `CH00`, DOC-01 owns
  `CH01..CH03`).
- `contracts/product/PRODUCT_CONSTITUTION.yaml` — `SPEC-01` ProductIdentitySpec
  contract fields (`product_id`, `formal_name`, `internal_name`, `namespace`,
  `version`, `supersedes`, `aliases`, `non_goals`), identity-unique invariant,
  exact error `ERR_PRODUCT_ID_COLLISION` and state model
  `PROPOSED->IDENTITY_UNIQUE->HUMAN_RATIFIED->ACTIVE->SUPERSEDED`.
- Requirement graph binding: `MC-01` -> `SPEC-01`/`SPEC-34`; `LGR-04`/`LGR-18`/
  `LGR-19`; `TS-001`; `T-001`/`T-037`; `G00`/`G17`; `ART-01`/`ART-14`.

## 3. Financial change

- Change class: `DOCUMENTATION_AND_CONTRACT` — no live financial execution,
  no broker write, no autonomous order submission, no production approval.
- Financial scope: TW-ICT FSDT financial contract kernel (`SPEC-05..SPEC-08`)
  remains design-contract only in this change; paper/shadow per PD-30 maturity.
- Financial impact: none in this phase; release/rollback rehearsed before any
  promotion, consumer ACK required (`G00` Authority and Identity Lock,
  `G01` Source and FSDT Landing Completeness).

