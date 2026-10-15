# SQS-THC Publication Round Evidence (SQS-THC-PUBLICATION-20261015)

## What this round did

1. **Target repo created**: `shw097-team/SQS-THC` (public, fresh; owner-directed with fine-grained PAT).
2. **Curated snapshot branch `published-20261015`** pushed: 884 tracked files, omitting `wiki/` (66MB downstream
   derived knowledge markdown), `data_plane/data/` (283MB generated data, re-derivable from TWSE via
   `data_plane/src/backfill_daily.py`), `.venv-data/`, `var/`, `實作執行/Shioaji API/` (broker credential dir,
   .gitignore line 23), `實作執行/SQS-THC_SOURCE_INVENTORY.json` (40MB digest list, .gitignore line 10),
   `shioaji.log`, `__pycache__/`, `worktrees/`.  Exclusions match the product's own `.gitignore` intent.
3. **Manifest**: `evidence/publication-20261015/manifest.json` records all 884 published paths with raw byte
   sha256 + size; each exclusion carries a written reason (no silently-dropped evidence).
4. **Secret scan PASS (0 hits)** across every staged byte before push (patterns github_pat_, ghp/usr_,
   sk-, AKIA, PRIVATE KEY block, xox, AIza, JWT eyJ, and the two locally-known shipped-API key strings).
5. **Pushed with token never in argv/URL/config**: `-c credential.helper=` inline helper form reading the PAT
   file at runtime; GCM contoainment (GCM_INTERACTIVE=never), `GIT_TERMINAL_PROMPT=0`.
6. **Product untouched at round end**: SQS-THC local HEAD stays `9a70501a…`; the working tree carries the same
   incidental file-restorations (`git checkout -- "實作執行/"` restoring 14 files under implementation-archive/) +
   the two files that were already modified by a prior round.
7. **Suite re-run at round time**: 244 tests OK, `PACKAGE_READBACK_OK`.

## Claim ceiling

- `PUBLICATION_APPROVED`: **NOT CLAIMED** — visibility ≠ approval; this is a candidate publication snapshot,
  NOT a release, NOT production. `prod_status NOT_CLAIMED`, `sqs_live_trading NOT_AUTHORIZED`.
- External engineers: please see `README.md` §1-§8 (landing) + `docs/SQS-THC_TW-ICT_FSDT-Stack使用說明文檔.md`
  (full User Guide) + `evidence/rp002/stage3/RP002_R1_EVIDENCE_FOR_EXTERNAL_REVIEW.md` (external review MD).
- No LICENSE file has been added. The owner retains all rights; the round did NOT pick a licence
  (licence/publication gate stays with the owner).
- SOD: PLAN/ORCHESTRATION in this Hermes chat is served by `opencode-go/glm-5.3-flash` (chain fallback1);
  EXECUTE is `opencode-go/deepseek-v4.1-flash`; VERIFY/checker is `opencode-go/glm-5.3-flash` (independent Codex
  CLI subprocess; separate process/context; no shared conclusions). Model-family overlap between PLAN serving arm
  and CHECKER arm is a *recorded* owner-order deviation (SoD residual disclosed in lane_mandate.json).

## Independent checker verdict

Pending — dispatched next (WO-SQSPUB-20261015-VERIFY).
