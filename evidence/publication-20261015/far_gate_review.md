# FAR — SQS-THC Public Publication Round (SQS-THC-PUBLICATION-20261015)

FAR = Find-and-Adapt-Research: find the reusable precedent inside this stack, adapt it to this task with a
low-friction route, record the residual/gap honestly. This document binds what "reuse" means here.

## Gate-1: search + reuse (what already exists, and is being reused)

| # | reusable precedent (probe path) | what it gives this round | reuse decision |
|---|---|---|---|
| R1 | `scripts/hgk-lane-dispatch.py` + `scripts/runtime_role_binding_assert.py` + `config/lane-route-slots.candidate.json` (epoch 18) + past round `evidence/FAR-LANE-ROUTE-REBIND-20261015/` | the ENTIRE lane/mandate/toolchain binding machinery used to serve EXECUTE (DeepSeek) and VERIFY (GLM) turns under the owner chain with receipts and `require_arm==served_arm` | REUSED AS-IS |
| R2 | `scripts/remote_write_precheck` + `REMOTE_WRITE_MARKERS` inside the dispatcher (Phase C4 + D6) | refuses publishing-brief lanes without an attached publication WorkOrder — this round explicitly passes `--publication-workorder WO-SQSPUB-20261015-PUSH` for any lane whose brief mentions push/publish/refs/heads (pre-spawn refuse is typable, disclosed; it cannot, and is not claimed to, stop an already-spawned lane from calling git) | REUSED |
| R3 | `scripts/validate-package.py` + `PYTHONPATH=src python -m unittest discover -s tests -t .` (244 tests OK 2026-10-15 local) | product self-test as a PRE-push subject-boundary proof: today's tree runs the same suite with zero product edits — the staged bytes are the tested bytes | REUSED |
| R4 | `STATUS_VECTOR.json` gates + `evidence/rp002/stage3/RP002_R1_EVIDENCE_FOR_EXTERNAL_REVIEW.md` (hash-bound, external-review shaped) | acts as the tree's own external-review-facing artifact — the new public doc points at it so external engineers see the intended claim ceiling immediately, not an advertisement | REUSED |
| R5 | `staging/plan.md` §3 exclusion doctrine + the `.gitignore` producer's own exclusion lines (the broker-API credential dir, `SQS-THC_SOURCE_INVENTORY.json`, `data_plane/data/`, `var/`, `shioaji.log`) | makes the staged-tree boundary identical to the product's own ignore intent, not a hand-invented boundary — the reason `.gitignore` itself is committed and cited | REUSED |
| R6 | Single-evidence-MD convention of past SQS rounds (e.g. `evidence/review/FAR_FINAL_ACCEPTANCE_EVIDENCE.md`, `.../RP002_R1_EVIDENCE_FOR_EXTERNAL_REVIEW.md`) | formatting constraint for the new round-evidence MD: one pointer-rich public MD, hash-bound to the tree it ships with, claim ceiling at the top | REUSED |
| R7 | `hgk-verify-evidence-runner.py` (read-only, deterministic probes, forbid-list + allowed probe IDs, D01 output-collision boundary) | venv-local deterministic verifier pattern if the checker lane needs to re-derive byte equality between staging manifest and remote readback — pushed to the checker as an *allowed probe style*, never as arbitrary argv | REUSED (style) |
| R8 | `release-evidence-and-publication.md` skill reference (branch-first push, anonymous readback, token handling, `credential.helper` inline form for git ≥2.53-on-Windows askpass fix) | the branch push mechanics: PAT never in argv; `-c credential.helper=` clears the system GCM that otherwise blocks an unattended lane; redacted logs; token-free remote URL before push | REUSED AS-IS |

## Gate-2: adapted, not verbatim

- The `PIPD-LS-SP` release-evidence tag flow does NOT apply as-is: this target is a NEW repo on an empty tree
  (no release history, no owner grant file — only the owner PAT), so instead of tag+release the round pushes a
  branch `published-20261015`, and the branch tip becomes the tree-under-review.
- `wiki/` handling is an ADAPTATION of the product's own `.gitignore` intent to remote-not-local publication
  (the remote is a code-reference snapshot; wiki is downstream derived knowledge-authoring, 66 MB — its receipts
  ARE published so a reviewer can still see how the wiki was built/verified).
- `adapters/fda-xq-globalwinner-route.yaml` IS published (sha256 8f65c29f…, 3402 B): part of the implementation
  surface demonstrating a governed, fail-closed automation boundary (binding WO-SQS-FDA-XQ-ROUTE-001; watch-only
  / no-live-write semantics; expires 2026-12-31). Publishing the binding FILE does not authorize any desktop
  automation and contains no credentials. Any real use of the bound XQ desktop route remains under its own HITL
  gate — this round only publishes the contract text.
- The Hermes pre-tool guard blocked round-internal file writes on this topic (multiple refusal events of the
  same class, during this file's composition); resolved after the owner's explicit in-chat authorization by
  binding the short-TTL session token to the live session id. Disclosed as a side effect.

## Gate-3: residual / gap disclosure

- `wiki/` EXCLUDED (with size and reason recorded in manifest's `excluded_on_purpose`).
- `data_plane/data/*.parquet` + `backtest.duckdb` (283 MB) EXCLUDED: re-derivable from TWSE source via the
  shipped `data_plane/src/backfill_daily.py` (User Guide §16); the external engineer's design premise does not
  need the exact parquet bytes.
- `.venv-data/` (1 GB site-packages) / `var/` / `.git` / broker-credential path / `SQS-THC_SOURCE_INVENTORY.json`
  (40 MB digest list) / `shioaji.log` / `worktrees/` / cache dirs — never published; the `.gitignore` producer's
  own rules are the boundary.
- Relay 10101 emits HTTP 426 on websocket but the CLI tolerates it via JSON fallback; frontdoor 10100 was not
  started this round — disclosed as a routing deviation from the sealed-lane path; not a SOD violation.
- The suite at round time emits 244 OK; `README.md` still says "231 tests (2026-08-13 measured)" — a factual
  state, not edited by this round; the checker note records the actual at-publication measurement (244 OK).
- No LICENSE file exists in SQS-THC. Publishing under the owner's PAT makes visibility public; the round does
  NOT add an SPDX identifier, does NOT pick an OSS licence on the owner's behalf, does NOT describe the repo as
  licensed. Licence/publication gate stays with the owner (`PUBLICATION_APPROVED` stays NOT CLAIMED — visibility
  is not approval); a one-action ratification record accompanies the round.

## Target artifact enumeration

Published (branch `published-20261015` of `shw097-team/SQS-THC`):

- src/ (5 kernels fsdt/temporal/knowledge/harness/capability + method; 14 py, 2173 LOC)
- tests/ (28 py across contract/adversarial/edge/legacy/method/negative; 7782 LOC)
- data_plane/src (34 py, 4950 LOC), data_plane/config (policy + provider_profile + STATUS_VECTOR_DAILY +
  daily universe), data_plane/reports
- docs/ (DOC-00..12, User Guide, TS workorder contracts)
- evidence/ (review 3.6 MB incl. HERMES_INCIDENT RCA 918 KB, rp002/stage3 449 KB, daily-ohlcv 292 KB,
  rbwi-fullrun 414 KB, wiki-daytrading, wiki-kb-rebuild, far-method-research, far-negative-pnl,
  far-nextweek-method, far-review-session, daytrading-t0, method-finalization, spartoi-preopen,
  taskspecs, readback, release, gates, tools, ledger.yaml)
- SQS_* top-level manifests (8 files), STATUS_VECTOR.json, TEAM.md, SQS/TWICT_RUNTIME_PACK_MANIFEST.yaml,
  AGENTS.md, README.md, adapters/*.yaml, agents/profiles/sqs-* (3 profiles)
- contracts/ (incl PRODUCT_CONSTITUTION.yaml + rbwi/CANONICAL_OBJECTS.yaml), schemas/, scripts/, tools/,
  strategies/, research/, risk/, survival/, maturity/, sre/, security/, privacy/, supply-chain/, workflows/,
  training/, migration/, release/, reducers/, nrtv/, requirements/, fixtures/, handoff/, validation/,
  deprecation/, architecture/, plus 實作執行/ production-line plans (EXCLUDING the broker-API credential dir
  and the 40 MB source-inventory file)

## Claim ceiling

Every row above is backed by a probe/receipt recorded in the round receipts. NOT claimed: release, production
readiness, externally signed acceptance, or any XQ desktop-automation authority. The publication is candidate
publication under owner direction; visibility ≠ approval.
