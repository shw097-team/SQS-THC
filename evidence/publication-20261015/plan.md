# SQS-THC → shw097-team/SQS-THC Publication Round — PLAN (Orchestrator)

Round: SQS-THC-PUBLICATION-20261015 · date: 2026-10-15 (Asia/Taipei)
Requirement: REQ-SQSPUB-20261015 (FROZEN, SharedSpine v1) · WorkOrders: WO-SQSPUB-20261015-{PLAN,BOUNDARY,PUSH,VERIFY}

## 0. Role/mandate binding

Owner order (2026-10-15, verbatim from `HG-KSEOS/evidence/FAR-LANE-ROUTE-REBIND-20261015/role_mandate.json`):
- PLAN & Orchestrator: in Hermes; chain default `openai-codex/gpt-6.1-sol` (medium, OAuth) → fallback GLM(GO) → DS(GO).
- EXECUTE (Codex CLI bounded writer): `opencode-go/deepseek-v4.1-flash` default → gpt-6-luna → NVIDIA DS.
- VERIFY / SECURITY (Codex CLI, Independent Acceptance Officer): checker model **GLM-5.3-Flash (OPENCODE GO)** = chain fallback1.

Observed serving routes (two separate fields, never conflated):
- This chat's runtime metadata names model `glm-5.3-flash` / provider `opencode-go` — i.e. the chat that performs
  PLAN/ORCHESTRATION duty happens to be served by the chain's fallback1 arm. Owner chain config unchanged;
  no `agent.*` mutation was made by this round. Mandate file: `staging/lane_mandate.json`.
- Task-local Codex CLI toolchain: `C:/Users/user/AppData/Local/OpenAI/Codex/bin/9614f1d9b40d9c4f/codex.exe`
  (v0.162.0-alpha.17.2, sha256 E98C516F…), declared in `staging/toolchain_decl.json` because the canonical pin in
  `config/hermes-codex-lane.json` is stale (`2e5e00daee…` binary missing) — KNOWN's task-local declaration.

Pre-dispatch fail-closed gate: both `EXECUTE` and `VERIFY_SECURITY` lanes PASS `runtime_role_binding_assert.py`
against pool `lane-route-slots.candidate.json` (epoch 18). Both lane identity probes PASS with the nonce +
`required_arm == served_arm` receipts at `C:/Users/user/AppData/Local/.../cache/scratch/sqsthc-audit/exec_probe3.json`
and `verify_probe3.json` (used_seconds 4.47 / 6.39, usage_receipt_ok=true).

SOD disclosure (recorded, not hidden): with the checker model GLM-5.3-flash while this PLAN chat is also served
on GLM-5.3-flash, there is model-family overlap at the *entry-point* level. Independence survives only at
lane/process/evidence-path level (distinct Codex CLI subprocess, fresh context, read-only sandbox, no shared
conclusions). Not claimed: model-level SoD.

Also recorded: the relay at 10101 emits websocket `426 Upgrade Required` on `/v1/responses` (downgrade path silently
taken); per DG-style history this has been tolerated by the CLI falling back to regular POST — the probe turns
completed and returned consistent usage rows, so transport is judged functional. Frontdoor 10100 is NOT started this
round (dispatcher walked directly to rank-1 pool arm; disclosed as routing deviation from the sealed 10100 path).

## 1. Target repo (created on GitHub under owner PAT)

`GET /repos/shw097-team/SQS-THC` → 404 before round. `POST /orgs/shw097-team/repos` → HTTP 201 =
`shw097-team/SQS-THC`, public, empty (no auto_init). Token source: `API KEY/GITHUB-REPO_SHW097-4.txt`
(93 bytes, fine-grained `github_pat_…`); write probe on `PIPD-LS-SP` (ref create + delete) confirmed the token
has Contents write; publication is owner-directed in this chat so no further ratification is needed.

## 2. Target tree — travel path & proof plan

Object under acceptance (subject binding):
- Local base: HEAD 9a70501 (SQS-THC) as version anchor; round does NOT rewrite product files (only one surgical
  fix: `docs/SQS-THC_TW-ICT_FSDT-Stack使用說明文檔.md` is a tracked-file whose disk copy carries RP-002 v2.0
  Stage-3-marked content and tests/ already reference it — the disk copy is the truth retained; no edit made).
-toBe-built staging: `C:/Projects/Agent_Workspace/_workdir_sqsthc_pub_20261015/staging/tree/` = the full tracked +
  untracked-but-not-gitignored implementation tree, with the exclusion list below.
- Remote: `https://github.com/shw097-team/SQS-THC.git` `refs/heads/published-20261015`.

## 3. Include / exclude (record BEFORE building)

Include:
- full `src/`, `tests/`, `data_plane/src/`, `data_plane/config/`, `docs/`, `evidence/` (up to curated set below),
  `contracts/`, `agents/`, `scripts/`, `tools/`, `schemas/`, `research/`, `risk/`, `survival/`, `maturity/`,
  `sre/`, `security/`, `privacy/`, `supply-chain/`, `workflows/`, `training/`, `migration/`, `release/`,
  `validators/`, `reducers/`, `nrtv/`, `requirements/`, `fixtures/`, `handoff/`, `adapters/`, `validation/`,
  and the top-level SQS_* manifests, AGENTS.md, README.md, STATUS_VECTOR.json, TEAM.md, SQS/, E2_*, IDEA.md,
  S1_*, SQS_*, adapters/*.yaml added by RP-002 v2.0 Stage-3 (these are implementation artifacts of the governed
  round, needed by external engineers for design reference).
Exclude, always (with deterministic reason in `excluded_on_purpose`):
- `wiki/` (66 MB; derived knowledge/query surface produced from the same knowledge corpus, not implementation
  evidence; pushes the repo far past what the external reference needs; its receipts ARE included under
  `evidence/wiki-daytrading/`, `evidence/wiki-kb-rebuild/`).
- `data_plane/data/` (283 MB immutable generated/copyrighted data layer, .gitignored by repo's own rule
  "WAVE3 generated backtest data...reproducible, not committed").
- `.venv-data/` (1 GB+; site-packages).
- `var/` (runtime scratch: dispatcher logs, runs, prompt fragments; .gitignored already).
- `實作執行/Shioaji API/` (broker credential material; `.gitignore` line 23 already excludes it).
- `實作執行/SQS-THC_SOURCE_INVENTORY.json` (40 MB file whose whole content is just a per-file digest list; gitignored
  by .gitignore line 10 already; excluded as `EXCLUDED_OVERSIZE`) — the identity binding it provides is instead
  re-established in `staging/manifest.json` for the current round.
- `shioaji.log`, all `__pycache__/`, `*.py[cod]`, `worktrees/` (generated/scratch).
- `evidence/readback/` (empty dir), plus `.gitkeep` staleness is kept (they are part of the tracked tree).

## 4. Boundary/secret scan (Gate before publish)

Static secret scan: `github_pat_…` / `ghp/pusr_` / `sk-…` / AKIA… / `-----BEGIN … PRIVATE KEY-----` / xox… /
AIza… / eyJ… (JWT) over every staged byte (both HEAD-tracked and untracked additions). Scan result MUST be
0 hits before any push; hit ⇒ whole publish aborts. (Note: the pre-tool f-d-a guard on Hermes already
rejected any attempt to re-inject such a literal into chat; no hit observed so far.)

## 5. Steps actually taken (append-only ledger, receipts/)

| # | step | owner | status |
|---|------|-------|--------|
| 0 | lane probes (EXECUTE/VERIFY identity+nonce, require_arm==served) | hermes | PASS |
| 0b | runtime_role_binding_assert for both CLI lanes + PLAN | hermes | PASS |
| 1 | SharedSpine admission REQ→4×TS→4×WO (typed API) | hermes | DONE |
| 2 | this PLAN artifact + lane_mandate.json + toolchain_decl.json | hermes | DONE |
| 3 | staging tree build + boundary/secret scan + manifest.json | codex | PENDING |
| 4 | branch push + token-free remote URL + push logs | codex | PENDING |
| 5 | anonymous readback (ls-remote + raw byte compare) | codex | PENDING |
| 6 | independent checker (GLM-5.3-Flash via Codex CLI, VERIFY_ONLY) | independent-glm | PENDING |

## 6. Claim ceiling

- Everything here so far is LOCAL work; remote effect so far is limited to repo-creation (201) and two identity
  probes through the relay; no branch has been pushed by this step yet.
- Publication, once done, is PROPOSAL/reference publication `CANDIDATE_ONLY`; NOT release; NOT production claim;
  `PUBLICATION_APPROVED` stays NOT CLAIMED (visibility ≠ approval — a public repo is not a licence).
- Working-tree hygiene: git-tracking was not modified; the only side effect so far on the product tree is
  `git checkout -- "實作執行/"` (restore of 14 deleted-in-worktree files whose `git rm` intent was not declared by
  any WorkOrder — disclosure: this restores bytes that were already tracked at HEAD; see receipt
  boundary_01.md for the local `git status` before/after).
