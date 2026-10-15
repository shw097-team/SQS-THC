# DOC-08 - ML/NLP/Alternative Data Research

> Work order: `WO-TS-REF-08` (`TS-008` ML/NLP/alternative data research)
> Source authority: `SSOT/SQS-THC_P0-CIP-PACK_v2026.08.06-r2.md` §17 `TS-008`,
> `MC-20` (statistical time series / ML/DL/RL / foundation models / financial
> LLM-NLP / alternative data / CV), `CH21` / `CH22` / `CH23`
> Owner: `F20-01` · Receiver: Quant ML Lead · Deliverable: `ART-08`
> Claim ceiling: `LOCAL_DELIVERY` (see §5)

## 1. Research scope

- `research/ml/` - typed model cards (`MC-20` / `CH21` / `CH22`), each with
  `id`, `leakage_guard`, `metrics` and `status`:
  - `model-ml-rf-overnight` - ML random-forest overnight gap classifier;
    tabular features, PIT-aligned, research-only.
  - `model-dl-lstm-volume` - DL LSTM next-bar volume forecast for
    liquidity-aware execution sizing; research-only.
  - `model-rl-trade-sizing` - RL sizing policy; paper/shadow only, never
    autonomous submission; research-only.
- `research/nlp/` - NLP assets (`MC-20` / `CH23`), each with `id`, `source`
  and `purpose`: `nlp-tone-lexicon`, `nlp-llm-news-summary`,
  `nlp-embedding-reports`.
- `research/alternative-data/` - alternative data sources (`MC-20` / `CH22`),
  each with `id`, `license` and `source`:
  `alt-satellite-plant-activity`, `alt-web-pricing-feed`,
  `alt-news-sentiment-feed`.
- `fixtures/models/` - model/NLP/alt-data validation fixtures, including the
  empty model-directory fixture `fixtures/models/models_empty/`.

## 2. Model cards and the leakage guard

- A model card MUST carry `id`, `leakage_guard`, `metrics` and `status`
  (`MC-20` research denominator; no card without a guard is admissible).
- `leakage_guard` fixes the temporal split:
  `train_start <= train_end <= test_start <= test_end` (ISO dates). A card
  whose training window leaks into the test window (`train_end > test_start`)
  is a leakage violation and is NACK'd with exact error `ERR_MODEL_LEAKAGE`;
  the validation performs no mutation (fail-closed).
- `metrics` are reported on the out-of-sample / test window only; metrics
  computed on training data are not admissible evidence. `status` is
  `RESEARCH_ONLY` for every materialized card (no production claim).
- Research is grounded in `SPEC-03` / `SPEC-04` (data quality, PIT,
  provenance) and `SPEC-10` / `SPEC-24`: `fundamental_asof <= decision_time`,
  features frozen at `signal_time`, no restatement or lookahead leakage into
  the historical window.

## 3. NLP assets

- `research/nlp/` holds NLP assets with `id`, `source` and `purpose`; every
  `source` is a resolvable anchored locator into the read-only SSOT corpus.
- NLP-derived signals inherit the same temporal discipline: a text snapshot is
  valid only as of its capture time; retro-edited or post-hoc text may not be
  used to backfill a historical signal window.

## 4. Alternative data licensing

- `research/alternative-data/` holds alternative data sources with `id`,
  `license` and `source`. An alternative data source WITHOUT a `license`
  cannot be proven leakage/PIT/rights-safe and is rejected fail-closed with
  exact error `ERR_MODEL_LEAKAGE`.
- All materialized sources carry a restrictive, non-redistributable license
  (`COMMERCIAL_AGREEMENT_NON_REDISTRIBUTABLE`,
  `WEBSITE_TERMS_OF_USE_RESTRICTED`, `VENDOR_AGREEMENT_NON_REDISTRIBUTABLE`).

## 5. Governance, claim ceiling and exact error

- Research governance follows `MC-20`: model card -> leakage guard -> OOS
  metrics -> status; any illegal transition is NACK'd. Blocking
  risk/survival/security/rights vetoes are never overridden.
- Claim ceiling is `LOCAL_DELIVERY`: this work order materializes model cards,
  NLP assets, alternative data sources and their validation tests. It does
  **not** claim `G05` passed, runtime executed, or production readiness.
- Fail-closed semantics: training window leaking into the test window
  (`train_end > test_start`), or alternative data without a license, raises
  `ERR_MODEL_LEAKAGE` and performs no mutation. Missing required fields are
  rejected with a field-naming error (fail-closed, distinct from
  `ERR_MODEL_LEAKAGE`). An empty model list is allowed (no models yet
  researched is a valid state).

## 6. Non-goals

- No autonomous order submission.
- No broker write.
- No production approval authority.
- No unscoped network or secret access.
- No runtime/tool activation without authorization.
- No unsolicited external write.

## 7. References

- `MC-20` (statistical time series / ML/DL/RL / foundation models / financial
  LLM-NLP / alternative data / CV) -> `TS-008` / `T-022` / `T-023` / `T-024` /
  `ART-08` / `G05`
- `SPEC-03`, `SPEC-04`, `SPEC-10`, `SPEC-24`, `LGR-15`, `G05` (TS-008
  dependencies)
