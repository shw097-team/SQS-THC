---
title: "PFR LIVE-SMOKE SINGLE EVIDENCE MD — Minimal Simulated Live-Run Acceptance (scenarios A 401 + B 429/5h-reset)"
workorder: WO-HGK-PFR-SMOKE-001
supersedes: WO-HGK-PFR-001 (base scheme, VERIFIED 2026-08-23)
decision: UD-PFR-2026-08-23-001
authority: USER (option "情境A＋情境B" confirmed)
date: 2026-08-23
claim_ceiling: "REAL live failover now empirically PROVEN for two paths in an isolated simulated environment (auth-401 cross-provider switch + 429/5h-reset reset-aware skip). NOT claimed: a naturally-occurring production 5h-window event was observed (mechanism simulated via isolated stub/poisoned credential, not a natural outage)."
terminal: LIVE_SMOKE_ACCEPTED
---

# Single Evidence MD — Live-Smoke acceptance (minimal simulated live-run)

## Purpose
Prove the provider-failover scheme truly works live (not just prerequisite dry-run):
Hermes, under a failing primary, actually switches cross-provider and completes a real
minimal agent task on the OpenRouter free backend. Seals the honest ceiling noted in
the base PFR round.

## Method (low-risk, isolated, non-destructive)
`tests/live_smoke.py`: for each scenario, builds an ephemeral isolated HERMES_HOME
(minimal config.yaml + .env, primary rendered failing), runs `hermes chat -q -Q` with a
minimal task (write marker file + report provider/model), then asserts exit 0, marker
content `FAILOVER_OK`, and the isolated session's `state.db` records
billing_provider=openrouter + a `:free` model.
- Production `config.yaml` / `.env` / live session: untouched (verified: harness only
  reads the real OpenRouter key from the key file for the isolated .env; writes go to
  disposable homes; never reaches the production gateway).
- Harness contains exactly one `sk-or-v1-` literal == the log-redaction regex (no real key).

## Scenario results (harness run 2026-08-23, live outbound calls to OpenRouter free)
- **Scenario A (primary credential poisoned -> HTTP 401):** exit 0; marker=FAILOVER_OK;
  state.db billing_provider=openrouter, base_url=https://openrouter.ai/api/v1/,
  model=nvidia/nemotron-3.5-lightning:free. (34.8s)
- **Scenario B (local stub primary returns 429 + 5-hour reset):** exit 0;
  marker=FAILOVER_OK; billing_provider=openrouter, model=nvidia/nemotron-3.5-lightning:free;
  **stub_request_count=4 (bounded)** → Hermes skipped doomed retries (reset-aware) and
  stayed on the free fallback instead of retry-looping on the 5h-reset primary. (14.4s)
- `all_pass=true`, harness exit 0. Both scenarios completed on nemotron free (GLM free was
  429-contended → Hermes skipped to the next free line, live evidence of the redundancy).

## Honest claim evolution
- Previously NOT claimed (PFR-001): "live failover not actually exercised." → **Now
  empirically proven** for both the auth-failure cross-provider switch (A) and the
  rate-limit/5h-reset reset-aware path (B), in an isolated simulated environment.
- Still NOT claimed: observation of a naturally-occurring production opencode-go 5h-window
  outage (the mechanism is proven via simulated/poisoned primaries, not a natural event).

## Acceptance verdict
- **AO independent acceptance lane (deleg_e0525057): `verdict=PASS`, `recommendation=PASS`.**
- AO independently re-read both isolated `state.db` sessions (billing_provider=openrouter,
  base_url=https://openrouter.ai/api/v1/, model `:free`), both marker files = FAILOVER_OK,
  result.json both PASS + all_pass=true + stub_requests=4(bounded). errors.log confirmed the
  real failover chain (A: opencode-go 401×3→openrouter glm:free 429→nemotron completes;
  B: primary stub 429+5h-reset attempt-1 reset-aware skip, stub hit 4×). Harness writes only
  to isolated homes; production config/.env untouched; no plaintext key in receipts/logs/
  state.db (only redaction regex literal in live_smoke.py line 85).
- Non-blocking suggestion (not required for PASS): set auxiliary free-only so Hermes internal
  auxiliary tasks (vision/compression/web) also use the `:free` queue (no cost incurred this run).

## Terminal
- AO verdict: **PASS**
- Claim ceiling: REAL live failover EMPIRICALLY PROVEN for both the auth-401 cross-provider
  path and the 429/5h-reset reset-aware path, in an isolated simulated environment. NOT
  claimed: observation of a naturally-occurring production opencode-go 5h-window event
  (mechanism simulated via poisoned/stub primary; natural-outage observation remains a future
  optional confirmation).
- Harness reusable: `HG-KSEOS/var/provider-failover-routing/tests/live_smoke.py`.