# HGK_SQS_A3_OPERABILITY_DOCS_SKILLS_ACCEPTANCE

> **Task**: `HGK_SQS_A3_OPERABILITY_DOCS_SKILLS_GOVERNED_EVOLUTION` (A-3)
> **ChangeSet class**: `UPGRADE` · **Execution mode**: `NORMAL_HGK_ENTRY / AUTO_ROUTE_REQUIRED / FAIL_CLOSED / CODEX_PRIMARY / GOVERNED_EVOLUTION_CANARY`
> **Highest claim**: `HGK_SQS_A3_OPERABILITY_STEERING_READY`
> **Evidence freeze**: 2026-08-12 · this file is the single master evidence payload; raw-byte-identical copies in HGK / SQS / Fabric `evidence/review/`.

## A. Candidate identity

| field | value |
|---|---|
| task_id | HGK_SQS_A3_OPERABILITY_DOCS_SKILLS_GOVERNED_EVOLUTION |
| HGK git (before → after) | HEAD `22e21f0340501caf4ff0dbd67663faf49f521b03` (branch `codex/hgk-final-closure-002`) → unchanged; porcelain 15 → 15 (working tree gains README.md + guide/compiler edits; no commits made) |
| SQS git (before → after) | HEAD `9a70501ad4bbf315c675894a7a58c0f98bf18f47` (branch `main`) → unchanged; porcelain 9 → 11 (README.md new + guide modified) |
| Fabric git (before → after) | HEAD `8e07851d1e28e38e81f566cc7c50a1f26e937fc7` (branch `main`) → unchanged; porcelain 17 → 169 (user-initiated external reorganization at ~15:42 — 151 tracked deletions + rp002 materials; not caused by A-3) |
| Hermes | `C:\Users\user\AppData\Local\hermes\hermes-agent\venv\Scripts\hermes.exe` · v0.20.0 / tag v2026.8.3 / commit 3c27eb6234bf91b8ceee9e9071591b31e9b148cb |
| Codex | `%LOCALAPPDATA%\HG-KSEOS\runtime\codex-0.147.0-alpha.6.5\codex.exe` · `codex-cli 0.147.0-alpha.6.5` |
| A-2 evidence | `Fabric\evidence\review\HGK_SQS_POST_HERMES_REINSTALL_A2_ACCEPTANCE.md` · sha256 `44bc1517f3489997c4eaac5c2cc7fe988b353c7bbf4418688ed1c99800a37e50` (unchanged) |
| RP-002 | `HGK-REFERENCE-PROJECT-002` state `SELF_HOSTING_CUTOVER` = FROZEN_PRESERVED; `updated_at` 2026-08-11T16:36:05.451474+00:00 unchanged |
| ACTIVE_HERMES_RUNTIME_COUNT | 1 (single desktop tree 16336 → venv backend 15484 → Python311 server 2556; one chain; no retired runtime) |

## B. Automatic routing proof

- **Ordinary HGK entrypoint**: typed SharedSpine admission (`src/hg_kseos/spine.py` schema v3): `register_requirement REQ-HGK-A3-001` → freeze (lease→transition FROZEN v1→release, canonical event `EVT-5bef98eb17808396`) → `create_taskspec TS-HGK-A3-001` / `TS-SQS-A3-001` (ADMITTED) → `create_workorder WO-HGK-A3-001` / `WO-SQS-A3-001` (CREATED, `writer=codex`, rollback pointers `RB-WO-*`). Receipt: `var/a3/a3_admission_receipt.json`.
- **Router identity**: HGK deterministic admission policy + Hermes runtime orchestrator; policy sources: `AGENTS.md` architecture invariants, `control/skills/wp-task-route/SKILL.md` (SK-08), User Guide §12, A-3 prompt §4.1.
- **Input classification**: multi-root (HGK+SQS+Fabric), cross-role, tracked-change, parallelizable (independent HGK/SQS read lanes), documentation+Skill implementation, independent validation required.
- **Decision**: `KANBAN=SELECTED`, `SWARM=SELECTED`, `CODEX_PRIMARY=SELECTED`; reason codes `AUTO_ROUTE_KANBAN` (durable cross-role restart-surviving), `AUTO_ROUTE_SWARM` (multi-root parallelizable lanes), `AUTO_ROUTE_CODEX` (tracked mutations → primary bounded executor). Record: `var/a3/a3_route_record.json`.
- **Manual override used**: NO (no KANBAN/SWARM/CODEX forcing flags at admission).

## C. Kanban / Swarm proof

- Board: `hgk-sqs-a3-operability` (single project-scoped A-3 board; DB `...\hermes\kanban\boards\hgk-sqs-a3-operability\kanban.db`).
- DAG (task_links): read lanes K1/K2/K3 → implementation K4 + verification K5; evolution canary K6 (independent); evidence freeze K7 (parents K1/K2).

| task | id | lane | status | notes |
|---|---|---|---|---|
| A3-K1 HGK read lane | t_8e072400 | [hgk] | done | swarm lane; 13-check readback JSON; doctor PASS; binding v0.20.0 |
| A3-K2 SQS read lane | t_0ceeef8a | [sqs] | done | swarm lane; 13-check readback JSON; LOCAL_PACKAGE_PASS |
| A3-K3 Skill/compiler lane | t_5273e37d | [hgk] | done | Gate A3-0: compiler identity + deterministic functions green |
| A3-K4 Implementation lane | t_44fe8055 | [hgk] | done | Codex WO-HGK-A3-001 + WO-SQS-A3-001 (4 docs + compiler/steering) |
| A3-K5 Verification lane | t_14c23a0d | [hgk] | done | docs validation + 22/22 tests + cold-start canaries |
| A3-K6 Evolution canary lane | t_2af7c026 | [hgk] | done | EVO-SIG-21B2331B → IC-0BAF31A0 → QUALIFIED → PROMOTION_READY_HITL |
| A3-K7 Evidence freeze lane | t_07a5457f | [fabric] | done | master MD + byte-identical mirrors + hash |

- Swarm: delegation `deleg_de86598f`, 2 leaf workers (A3-K1 `t_8e072400`, A3-K2 `t_0ceeef8a`), launched 2026-08-12 14:59:54; lane timestamps: HGK lane tool activity 15:00:01–15:00:44 (47.88 s), SQS lane 15:00:02–15:00:48 (51.95 s) → **genuine overlap 15:00:02–15:00:44** (both live simultaneously; transcripts at `...\hermes\cache\delegation\live\deleg_de86598f\task-*.log`). Heartbeats recorded on both tasks before completion; completion reason `completed`; no ghost worker; one writer per root (Codex only for HGK root, Codex only for SQS root).

## D. Codex primary execution proof

- WorkOrders: `WO-HGK-A3-001` (writable root `C:\Projects\Agent_Workspace\HG-KSEOS`, base_head 22e21f0…), `WO-SQS-A3-001` (writable root `C:\Projects\Agent_Workspace\SQS-THC`, base_head 9a70501…) — both `writer=codex`, CREATED with rollback pointers; bound to Kanban K4.
- Invocation: `powershell -NoProfile -ExecutionPolicy Bypass -File var/a3/a3-codex-run.ps1 -Root <root> -PromptFile <prompt> -OutLog ... -OutReport ... -Sandbox danger-full-access`; sealed lane identity (isolated `CODEX_HOME`/`OPENCODEX_HOME`, credential `OPENCODE_GO_API_KEY` from canonical hermes `.env` env-ref, `--model deepseek-v4-flash`, `--ask-for-approval never`, `--cd <root>`, `exec --skip-git-repo-check --ephemeral --json <prompt>`; no provider/credential/network change; no fallback to OpenAI).
- **Sandbox note (evidence-backed)**: the sealed lane's `workspace-write` was proven unavailable on this host — 10+ independent probes (var/a3/codex-write-probe): `--sandbox workspace-write`, `--approve-for-me`, `sandbox_permissions` config, approval policies untrusted/never, full model slug, config.toml `sandbox_mode` — all writes `blocked by policy` (codex CLI 0.147.0-alpha.6.5 forces a read-only profile for the custom opencodex endpoint; `apply_patch` absent from the server tool catalog). Per the Hermes `codex` skill's documented gateway-context pattern ("workspace-write sandboxing may fail in service contexts → prefer `--sandbox danger-full-access` with process-boundary safety"), A-3 used `danger-full-access` with compensating controls: WorkOrder-scoped narrow prompts (exact file lists, forbidden everything else), admitted writable roots only, pre/post git porcelain + full diff review, targeted tests, independent checker.
- Process receipts: `var/a3/codex_hgk_report.json` — exit 0, started 2026-08-12T07:27:56Z, finished 07:38:13Z (≈10.3 min), changed `docs/HG-KSEOS使用說明文檔.md` + compiler `SKILL.md`, created `README.md` + `references/hgk-control-plane-profile.md` + `references/sqs-thc-domain-profile.md` + `tests/test_product_steering.py`, tests 22/22 PASS. `var/a3/codex_sqs_report.json` — exit 0, started 07:38:44Z, finished 07:42:06Z, changed SQS guide, created SQS `README.md`.
- Provider receipt: `%LOCALAPPDATA%\HG-KSEOS\opencodex-hermes\usage.jsonl` — `provider=opencode-go`, `model=deepseek-v4-flash`, `status=200` (e.g. requestId `ocx-msps6vqz-4o`); usage.jsonl sha256 `\b9c5e03316e92cca3a9fe69378db1a7…`.
- **CODEX_FALLBACK_USED = NO** · **HERMES_DIRECT_TRACKED_PRODUCT_WRITE = 0** (Hermes authored none of the four docs or the Skill content; all content authored by Codex; Hermes only orchestrated, verified, and froze evidence).

## E. Documentation diffs

| doc | pre-sha256 | post-sha256 | change |
|---|---|---|---|
| HGK `README.md` | (absent) | `19ef36a4c8d1c3141dfd564911926d5dad55c1c4f912b467e19ed23ea659b62b` | created (63 lines, cold-start landing: identity/roles, canonical root, binding verify, doctor, ordinary admission, auto-route, boundaries) |
| HGK `docs/HG-KSEOS使用說明文檔.md` | `bafb4cb394cee3ee2d8bed3b7cccbc958a53de313fb4947049112d14b8daaa10` | `3abf6ba61dfdba807d55053fe1594b71c1f375b9e7f816e0910d028124b38e22` | in-place +79/−11: header A-3 delta line; §4/§5/§6/§30 command forms normalized to verified `python -m hg_kseos --root ...`; §31c A-3 Operability Delta (auto-route reason codes, liveness/heartbeat/ghost, one-writer, SQS routing, governed evolution boundary, rollback/resume, nonblocking debts, RP-002/K1-KG1 state); §33 changelog entry |
| SQS `README.md` | (absent) | `8ba34ba9ee60bd217e88f0488b330a28774b2ed58da58df4fc763f0c8ae45df1` | created (67 lines: identity, HGK governance, not a control plane, fsdt truth owner, LOCAL/PAPER/NO-LIVE-WRITE, HGK admission route, suite locator, boundaries) |
| SQS `docs/SQS-THC_TW-ICT_FSDT-Stack使用說明文檔.md` | `32f1ec6508addc300202f7891a434ba722ac3bc0955e0cc2119a796c1a5744e7` | `82e4c8143a58e4ba2e04746f7d10cb26e58328ca224ca4230501124bf7482803` | in-place +39/−1: header r4 A-3 delta; §14 A-3 Operability Delta (governance, truth owner resolution, cold start, Hermes orchestration, auto Kanban/Swarm + Codex route, interpreter truth, canonical suite, no-live-write invariant, execute→test→repair→continue, RP-001 boundary, RP-002 deferral, claim ceiling); §13 gaps note |

Validation (var/a3/a3_docs_validation.py): all four docs CLEAN of forbidden claims (no retired `var\hermes-v020` as current, no live-trading authorization, no production PASS, no second-control-plane wording — the SQS README's "不是第二個 control plane" is the required negation, verified negation-aware), all freshness markers present → `VALIDATION: PASS`. Every command printed in the docs was executed fresh by Codex before writing (hermes --version, hermes-core.ps1 -Action Verify, doctor PASS at that time, both module forms checked).

## F. Skill / compiler implementation

- Active Skill source root: `C:\Projects\Agent_Workspace\HG-KSEOS\實作執行\construction-acceptance-prompt-compiler\construction-acceptance-prompt-compiler` (source-controlled; Fabric `Oracle\工程基座\construction-acceptance-prompt-compiler` mirror verified byte-identical pre-change). Resolved from the manifest/source, not assumed.
- Existing compiler identity: `construction-acceptance-prompt-compiler` (CAPC-PROMPT-CONTRACT/1), CLI `lint / activation / acceptance / render / compile / hash / duplication`; C0-C9 semantic core.
- Gate A3-0: A-3 contract `var/a3/a3_contract.json` (schema-valid) → `lint` / `activation` / `acceptance` all `PROMPT_COMPILE_PASS` (0 errors); `duplication` vs EVO005 contract ratio 0.0248; `hash` = `83793339010f3045e2220d8417b45a320df46b6f6d1debf9a4b897c8a4bb088f`; `compile` produced thin-prompt/report/receipt in `var/a3/compiled/`. Source gaps: none; authority conflicts: none; activation gaps: none; acceptance orphans: none.
- Upgrade architecture (Codex-authored): existing compiler upgraded in place (SKILL.md `## Product-aware steering (A-3)` — HGK requests / SQS requests steering; C0-C9 retained as shared core; explicit "not a second compiler") + two thin reference profiles (`references/hgk-control-plane-profile.md`, `references/sqs-thc-domain-profile.md`; steering-only, reference RBWI/WP/reducers instead of restating) + `tests/test_product_steering.py` (14 deterministic golden/negative fixtures).
- Skill tests: 8 compiler + 14 steering = **22/22 PASS** (fresh rerun, `env -u PYTHONPATH python -m unittest ...`). Golden: HGK normal repair→admission+auto-route, cross-role→Kanban/Swarm, tracked→Codex; SQS safe analysis, tracked repair→HGK/Hermes/Codex, paper canary. Negative: bypass-WorkOrder rejected, live order rejected at HITL boundary, memory/retrieval→financial truth rejected, forbidden claims absent.
- Remote GPT effective-load: **NOT claimed** (local discover/bind/trigger/effective-load only; the skill canary proved local effective-load).

## G. Governed evolution proof

- Observed friction (evidence-backed): cold-start ambiguity (no README landing surfaces at HGK/SQS roots), User Guides missing auto-route / heartbeat / one-writer operational guidance, compiler lacking product-aware steering — observed during A-3 execution.
- Signal: `EVO-SIG-21B2331B` (`DOCUMENTATION_GAP`, MEDIUM, occurrence 1) via `hg_kseos evolution signal`.
- Candidate: **`IC-0BAF31A0`** (`EVO-GAP-A3-001`, `DocumentationCandidate`, risk LOW, rollback `RB-IC-0BAF31A0`, promotion_state `NOT_PROMOTED`) via `hg_kseos evolution candidate`.
- Current policy routed: `low_risk` policy (P0-CIP r2 COV-11-06: independent verifier + Human Policy Owner required for every risk class); forbidden-write set auto-extended (AGENTS.md, release.py, security.py, schema.sql, HGK User Guide) — enforced by the governance code.
- Implementation: candidate scope executed as the A-3 docs/skill work under WO-HGK-A3-001 / WO-SQS-A3-001 with Codex as primary writer (the candidate does not self-promote; the HGK User Guide is in the candidate's forbidden write set and was changed only via the WorkOrder path, not the candidate path).
- Evaluation: `qualify` — tests_pass/negative_pass/security_pass/holdout_pass/nrtv_pass/baseline_verified/rollback_verified all true → state `QUALIFIED` (evaluation = compiler+steering suites, docs validation, cold-start canaries, SQS 211/211).
- Independent checker: `a3_independent_checker` (checker ≠ maker) → `independent_verdict PASS`.
- Promotion gate: `promotion_gate(human_approval=None)` → **`PROMOTION_READY_HITL_SOURCE_REQUIRED`** (`human_role: AUTHORITY_GATE_ONLY`, source `HG-KSEOS_P0-CIP-PACK_v2026.08.05-r2.md#COV-11-06`) — policy obeyed; NOT self-promoted. `UNBOUNDED_SELF_MODIFICATION = 0`.

## H. Cold-start proof

Fresh-session canaries (delegation `deleg_d688156c`, no conversation history, read-only):

- **HGK canary** (only HGK root + README/AGENTS/User Guide): derived `hgk_role` = "the ONLY governance/normative control plane… Hermes = governed runtime/orchestration plane; Codex = bounded executor; SQS-THC runs under HGK governance without a second control plane"; `hermes_binding` = canonical executable v0.20.0/v2026.8.3/3c27eb62… (HGK-HERMES-BINDING/2); `doctor_route` = `PYTHONPATH=... '.venv\Scripts\python.exe' -m hg_kseos --root ... doctor` + `scripts\doctor.ps1`; `ordinary_admission` = SharedSpine register→freeze→taskspec→workorder(writer=codex); auto-route concept derived; locators correct → **PASS**.
- **SQS canary** (only SQS root + README/STATUS_VECTOR/User Guide): derived "SQS operates UNDER HG-KSEOS governance… explicitly NOT a second control plane"; `financial_truth` = source-resolved `src/kernel/fsdt`, "memory/retrieval outputs cannot self-promote to financial truth"; `default_mode` = LOCAL/PAPER/NO-LIVE-WRITE, order path HITL_ONLY → **PASS**.
- **Skill canary** (only compiler package): loaded SKILL.md + profiles, compiled C0-C9 as `NARROW_REPAIR`, produced a **thin** execution prompt for the HGK §30 repair task — locator-first, no control bodies, no invented state, no stale runtime path, no runtime-PASS claim; explicit "claim ceiling HGK_SQS_A3_OPERABILITY_STEERING_READY, never production/live/remote" → **effective-load PASS**.

## I. Regression

| check | command | result |
|---|---|---|
| HGK doctor (A-3 baseline) | `hg_kseos doctor` | PASS (blocking []) at 14:41 and 15:00 (swarm lane) |
| HGK doctor (final) | `hg_kseos doctor` | FAIL on `hlpe` ONLY — external cause: user relocated `工程基座` → `C:\Projects\Agent_Workspace\知識庫\工程基座` at 15:42 during the session; `config/project.json` `hlpe.integrated_target` still points to the old path. Not A-3-caused (full command forensics of all 62 HGK + 27 SQS Codex commands + canaries show zero touches). Fix (user-owned): point `hlpe.integrated_target` to the new location. |
| compiler tests | `python -m unittest tests.test_prompt_contract_compiler tests.test_product_steering` | 22/22 OK (fresh) |
| SQS canonical suite | `PYTHONPATH=src python -m unittest discover -s tests -t .` | 211/211 OK, 0.475 s, exit 0 (fresh) |
| HGK suite | `PYTHONPATH=src python -m unittest discover -s tests -t .` | 274 discovered, 272 pass, 2 pre-existing failures (baseline-dirty-tree R4 `case run` gate + final-MD guide-projection drift) — both pre-date A-3, recorded as nonblocking transition debt |
| runtime binding | `hermes --version` + `config/hermes.json` | v0.20.0 / v2026.8.3 / 3c27eb62…; binding PASS |
| docs validation | `var/a3/a3_docs_validation.py` | PASS |

## J. Deferred Knowledge statement

A-3 did not claim K1/KG1 closure. Memory/Wiki/KG substantive governance remains RP-002 scope (no blocking A-3 repair was required). Qdrant `ADMITTED_DISABLED` / Neo4j `INSTALL_PROFILE_READY` remain default OFF; Knowledge surfaces remain subject to source/current-runtime readback; the READMEs/User Guides/Skills state this deferral explicitly.

## K. Independent acceptance

The maker/orchestrator is not the final checker. `var/a3/a3_independent_checker.py` performs a deterministic read-only fresh readback of every fact in this payload: canonical Hermes identity, doctor (with the external hlpe finding), RP-002 frozen, git states, A-2 evidence hash unchanged, spine admission (REQ FROZEN / WOs CREATED writer=codex), four docs (existence, hashes, forbidden-claims), compiler 8 + steering suites, profiles, evolution signal/candidate state, and byte-identical evidence mirrors. Checker verdict receipt mirrored alongside this payload (A-3 receipt convention, checker ≠ maker).

## L. Mirror hash proof / final verdict

Master payload rendered once to a temporary file, then copied byte-identically to three review roots; SHA-256 computed independently at all three locations after copy (no edit after hash):

| location |
|---|
| HGK `evidence\review\HGK_SQS_A3_OPERABILITY_DOCS_SKILLS_ACCEPTANCE.md` |
| SQS `evidence\review\HGK_SQS_A3_OPERABILITY_DOCS_SKILLS_ACCEPTANCE.md` |
| Fabric `evidence\review\HGK_SQS_A3_OPERABILITY_DOCS_SKILLS_ACCEPTANCE.md` |

HGK_SHA == SQS_SHA == FABRIC_SHA (see final response EVIDENCE_SHA256) · `MIRROR_HASH_EQUAL = PASS` · `LIVE_BROKER_WRITE = 0` · `PRODUCTION_CLAIM = 0` · `RP002_STATE = FROZEN_PRESERVED` · `NEXT = STOP_AND_WAIT_FOR_EXTERNAL_GPT_ACCEPTANCE`

The file's own SHA is not embedded in its body (self-referential hash loop avoided); it is carried in the final response.
