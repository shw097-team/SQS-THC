---
name: provider-failover-emergency-checkpoint
description: "On opencode-go failover, save task to resumable breakpoint."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [provider, failover, openrouter, fallback, checkpoint, resume, emergency]
    related_skills: [hermes-agent]
---

# Provider Failover Emergency Checkpoint

Hermes has a cross-provider fallback chain so service keeps running when the
primary model provider (opencode-go) is unavailable. When that happens the
agent must FIRST emergency-save the in-flight task to a resumable breakpoint,
then continue only lightweight emergency work on the fallback (OpenRouter free).

## When to use (trigger)

- The active **runtime metadata** (Model / Provider shown in the session) is **not**
  `deepseek-v4-flash` / `opencode-go` (primary), i.e. the fallback chain engaged.
- You see provider failures: quota / **5-hour usage-window** exhausted, HTTP 429,
  5xx, auth (401/403), 404, or connection failures from opencode-go.
- The user reports the primary provider is down and asks to keep the task alive.

## Established routing (set 2026-08-23, WO-HGK-PFR-001)

| Priority | Provider | Model | Purpose |
|---|---|---|---|
| Primary | opencode-go | deepseek-v4-flash | default |
| F1 | opencode-go | gpt-5.6-luna | same-provider (fails together on quota) |
| F2 | opencode-go | glm-5.2 | same-provider |
| F3 | **openrouter** | **z-ai/glm-5.2:free** | **best free, tool-calling verified** |
| F4 | **openrouter** | **nvidia/nemotron-3.5-lightning:free** | second free, 1M ctx |

Hermes fallback is reset-aware: when opencode-go reports a 5-hour-window reset
not yet elapsed, it skips doomed retries and stays on the fallback until the
window passes. So the switch to OpenRouter free is automatic and persistent for
the remaining window. Config lives in `~/.hermes/config.yaml` -> `fallback_providers`;
credential `OPENROUTER_API_KEY` -> `~/.hermes/.env`.

## Emergency Checkpoint Procedure (ECP) — run on failover

1. **Confirm active provider/model**: `hermes model` or check runtime metadata.
2. **Write a checkpoint** to `~/.hermes/var/checkpoints/<task-slug>.md` with YAML
   front-matter + body:
   - `task_goal`, `current_step`, `step_index`, `partial_outputs`/`artifact_paths`,
     `next_actions`, `resume_token`, `detected_at`, `active_provider`, `active_model`.
   - Path `<slug>` = short name for the in-flight task (e.g. the task/board slug).
3. **Flush durable memory**: `hermes memory set` for any preference/decision learned
   so far (do not dump raw transcripts into permanent memory).
4. **Persist the session** (Hermes auto-saves state.db + sessions/*.jsonl — no
   manual step needed; just don't wipe it).
5. **Notify the user** with: provider-change notice, checkpoint absolute path,
   `@session:<profile>/<id>` link, and the exact resume instruction below.
6. **Continue only bounded lightweight emergency work** on the free model. Do NOT
   start new heavy / long tasks on `:free`.

## Resume (next session)

- User (or new session) reads `~/.hermes/var/checkpoints/<task-slug>.md`, or uses
  the `@session` link / `/resume <session>` to reopen the interrupted session.
- Continue from `current_step` using `next_actions`; do NOT restart from scratch.

## Manual provider switch (redundant with the auto fallback)

```bash
hermes model <model> --provider <provider> --global   # persist as default (next session)
hermes model <model> --provider <provider>            # this session only
# examples
hermes model z-ai/glm-5.2:free --provider openrouter --global
hermes config set model.provider openrouter            # + model.default = <model>
# current default / readback
hermes model ; hermes fallback list
```
> A provider change affects the NEXT session (the running session keeps its
> pinned model); in-session use `/model <alias> --provider <p>`.

## Pitfalls

- **`:free` is rate-limited** (roughly 20 req/min, generous enough for emergency
  save + a few follow-up calls). Never run a long agentic job on OpenRouter free.
- **New `.env`/config vars need a gateway/session restart** to be live in a
  running process; the config is picked up on provider-failure resolution.
- **Never write the raw API key** into checkpoints, logs, or messages (redactor is
  on, but do not print it intentionally).
- If the primary comes back before the window passes, `hermes model` returns to
  opencode-go/deepseek-v4-flash on the next default resolution; the checkpoint is
  still valid for resuming the task.