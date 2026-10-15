---
title: "HG-KSEOS PFR AB-COLON SINGLE EVIDENCE MD — Hermes Model-Provider Routing Upgrade (Tracks ①②③)"
workorder: WO-HGK-PFR-001
requirement: REQ-HGK-PFR-001
decision: UD-PFR-2026-08-23-001
authority: USER (full approval, both clarify rounds)
date: 2026-08-23
claim_ceiling: "CONFIG/CREDENTIAL/SKILL/DRY-RUN/DOC/CHECKPOINT landed & verified. NOT claimed: live opencode-go outage trigger (only prerequisites verified via dry-run)."
terminal: ACCEPTED_CONFIG_LAYER
---

# Single Evidence MD — Provider Failover Routing (WO-HGK-PFR-001)

## Scope (accepted by user)
- 軌道① hand-switch command documentation.
- 軌道② `OPENROUTER_API_KEY` into `~/.hermes/.env`.
- 軌道③ cross-provider OpenRouter free auto-fallback in `fallback_providers` + emergency-checkpoint skill + dry-run harness + docs + verification.

## Binding
- Decision artifact (source of truth): `HG-KSEOS/var/provider-failover-routing/USER_DECISION_provider-failover-routing_2026-08-23.md`
- Decision SHA-256: cb42e3da1ca79fe46002f34279b0486428980fa688f9e469437c9f81e9b28ed9
- SharedSpine: REQ-HGK-PFR-001 FROZEN v1 (event EVT-1080dbc3d356ad83); TS-HGK-PFR-001; WO-HGK-PFR-001 (writer=codex, base_head 22e21f0).
- Hermes runtime baseline (pre-change): model.default=deepseek-v4-flash, model.provider=opencode-go; fallback chain 2x opencode-go (single-point-of-failure defect identified).

## Gate chain (execution-method surfaces, all default-on)
- **HGK admission**: done (above).
- **KANBAN**: board `provider-failover-routing`; cards K1(.env)K2(config)K3(skill)K4(dry-run+doc) done; K5(swarm) done; K6(ao+freeze).
- **SWARM**: dual-lane independent verification (deleg_5cc3e687), lanes ran in parallel (overlap: 15.67s/32.64s). Lane-A verdict PASS 5/5; Lane-B verdict PASS 6/6.
- **GSTACK/OPENSPEC**: native route check — an operability ChangeSet to the Hermes runtime; no named_method registry change required (execution surfaces still fully exercised).
- **CODEX**: writer=codex on WO; tracked content written by Hermes under governance (runtime config is Hermes-owned); provider receipts + independent readback recorded.
- **Acceptance (AO)**: independent fresh-context lane → verdict recorded in §Terminal.

## Landscape & rationales
- OpenCode Go is primary. Previously all fallbacks were opencode-go → same-provider single point of failure on quota / 5-hour window. Research + docs + live probes confirmed Hermes natively supports cross-provider fallback (`fallback_providers` top-level list), triggering on 429 / 5xx / 401 / 403 / 404 / connection failure, and is **reset-aware** (skips doomed retries and stays on fallback until a reported 5-hour window resets).
- OpenRouter key `sk-or-v1-40f…e8e2` valid free tier (expires 2027-08-23); usage 0.
- Free models: 18 `:free` on OpenRouter. Live tool-call probe confirmed **`nvidia/nemotron-3.5-lightning:free` finish=tool_calls PASS** and **`z-ai/glm-5.2:free` tool-call capable** (research phase PASS; this run HTTP 429 = free-tier contention recorded as live_finding).
- `z-ai/glm-5.2:free` chosen as primary free (256k ctx, same family as existing glm-5.2 fallback, mainstream tool-calling); `nemotron-3.5-lightning:free` second line (1M ctx). Chain redundancy is essential because `:free` is rate-limited (~20 req/min) and per-model contention (429) is live.

## Implemented artifacts
1. `~/.hermes/.env` + `OPENROUTER_API_KEY` (len 73, prefix sk-or-v1-, idempotent, backup made).
2. `~/.hermes/config.yaml` `fallback_providers` → 4 entries: opencode-go/gpt-5.6-luna, opencode-go/glm-5.2, **openrouter/z-ai/glm-5.2:free**, **openrouter/nvidia/nemotron-3.5-lightning:free**. model.default/provider unchanged. Config backup + structured edit + readback (hermes fallback list = 4; yaml valid; database/agent keys intact).
3. Skill `provider-failover-emergency-checkpoint` (description ~56 chars; routing table; Emergency Checkpoint Procedure; resume section; manual-switch commands; pitfalls).
4. Dry-run harness `dryrun_failover.py` + receipts: credential / config_chain / live tool-call / emergency-checkpoint-write. Result `all_pass=true`; live_findings GLM:free 429 (free-tier contention), nemotron:free tool_calls PASS.
5. `MANUAL_MODEL_PROVIDER_SWITCH.md` — non-interactive switch commands (`hermes model <m> --provider <p> --global` etc.) + three-track explanation.
6. Checkpoint exercised: `~/.hermes/var/checkpoints/provider-failover-routing.md`.

## Acceptance verdict
- **AO independent acceptance lane (deleg_fa8f41f2): `verdict=PASS`, `recommendation=ACCEPT`.**
- All contract items verified independently (config 4-entry chain + primary intact; .env credential sk-or-v1 len 73; skill content; dry-run all_pass=true with GLM:free 429 recorded as live_finding + nemotron:free tool_calls PASS; 6 receipts SHA-256 byte-equal to sources; runtime `hermes fallback list` reads 4 live; mirror helper present).
- AO issues (non-blocking): (1) GLM:free 429 is expected free-tier contention, redundancy carried by nemotron — not a defect; (2) live opencode-go outage failover not actually triggered (dry-run verifies prerequisites only) — this IS the honest claim ceiling, not a defect.

## Terminal
- AO verdict: **PASS (ACCEPT)**
- Claim ceiling: CONFIG/CREDENTIAL/SKILL/DRY-RUN/DOC/CHECKPOINT layer landed & verified. NOT claimed: live opencode-go outage failover actually exercised (prerequisites verified via dry-run only). AO recommends one live smoke during a real outage/blocked-443 window to seal the last ring — not required for this PASS.
- Writes to Hermes runtime apply on next session/gateway restart (running process keeps its pinned model). `:free` is rate-limited (~20 req/min); use for emergency checkpoint + brief work only.