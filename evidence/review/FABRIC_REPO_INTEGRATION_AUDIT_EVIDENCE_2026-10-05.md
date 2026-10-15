# FABRIC REPO 整合稽核 — 外部驗收可用性（單一證據 MD，全量 raw 內嵌）

```yaml
schema: HGK-FABRIC-REPO-INTEGRATION-AUDIT/1
artifact: FABRIC_REPO_INTEGRATION_EXTERNAL_VERIFIABILITY_AUDIT
mode: READ_ONLY (no mutation of the mirror, no publication, no external acceptance issued)
control_plane: HG-KSEOS (admission / WorkOrder / evidence / release)
runtime_plane: Hermes Agent (KANBAN + SWARM lanes + CODEX CLI independent lane)
generated_at_local: 2026-10-05 17:51:32 
claim_ceiling: READ_ONLY_VERIFIABILITY_AUDIT | NO_EXTERNAL_ACCEPTANCE | NO_MIRROR_MUTATION | NO_PUBLICATION
non_claims: [NOT_EXTERNALLY_ACCEPTED, NOT_MERGED, NOT_RELEASED, NOT_PRODUCTION, NO_LIVE_WORLD_EFFECT]
```

## 0. 稽核問題（受稽核的原始提問）

1. `github.com/shw097-team/Fabric` 是否已整合上傳 **`fabric-desktop-automation`（FDA，《FDA_USER_GUIDE》）** 的相關資料夾檔案，供外部驗收官驗收？
2. `github.com/shw097-team/Fabric` 是否已整合上傳 **`fabric-autonomous-research`（FAR，《fabric-autonomous-research_使用說明手冊_v2026.08.13-r1》）** 的相關資料夾檔案，供外部驗收官驗收？

## 1. 結論（兩題直接作答）

| 題 | 結論 | 資料夾是否上傳 | 外部驗收官可否完成驗收 |
|---|---|---|---|
| 1 FDA | **已整合上傳（結構面 FULL）** | 是：`FABRIC/fabric-desktop-automation/` 25 檔 + `DESKTOP/`（藍圖/11 份外部複驗報告/538 檔執行面）+ `FABRIC/Independent Acceptance Officer/` | **僅部分**：設計/契約/程式/治理檔與外部複驗報告可讀，但**全部 raw 收據、EvidenceManifest、單一證據 MD 與其打包腳本未上傳** → 無法複算任何 PASS 斷言 |
| 2 FAR | **已整合上傳（結構面 FULL）** | 是：`FABRIC/fabric-autonomous-research/` 905 檔（canary/governance 50 收據/evidence-bundle/research-product 契約+22 模板/methods）+ `FAR/far-swof-kseos-rca-001/` 25 檔 | **僅部分**：契約面、gate 收據、canonical 單一驗收 MD（hash 自洽）可驗；但**外部 r7 驗收報告、`FAR_EXTERNAL_REVIEW_PACKAGE_v3.zip`、各 `FAR_*_EVIDENCE.md` master 未上傳** → 無法獨立複核 FAR-R1 PASS |

**共同根因**：`INTEGRATION/MANIFEST.json` 與根 `README.md` §2 明示 `"excluded": ["var/", "worktrees/", "evidence/ raw stores", ".venv/", "API KEY/"]`。整個 repo **沒有任何名為 `evidence/` 或 `review/` 的目錄**（含子目錄全樹檢查 = 0 命中），而兩份主體的 §12/§5 交付清單與 README 的「verified action-class receipts」都以該目錄為載體。

## 2. 稽核方法（可複製）

- 遠端唯讀：GitHub REST（repo meta → default branch → `git/trees?recursive=1`）+ `git clone --depth 1`。
- 本地權威：`C:/Projects/Agent_Workspace/Fabric`（HEAD 243bf8fa…）。
- 身分證明：**git blob 層**（`git ls-tree -r HEAD`）+ **工作樹 sha256（原始與 CRLF 正規化兩式）**，避免 line-ending 偽差異。
- 並行獨立通道：2 條 sub-agent 稽核 lane（FDA / FAR，各自輸出 JSON）+ 1 條 **Codex CLI** 唯讀獨立裁決 lane。
- 全程未修改 mirror、未上傳任何內容、未發出任何外部驗收。

## 3. 受稽核遠端主體（raw）

```json
{
 "full_name": "shw097-team/Fabric",
 "id": 1404471533,
 "private": false,
 "visibility": "public",
 "default_branch": "main",
 "fork": false,
 "size": 31690,
 "pushed_at": "2026-10-04T16:17:43Z",
 "updated_at": "2026-10-04T16:17:47Z",
 "has_issues": true
}
```
- HEAD = `60ed68a68bc7d39385e65d1aa96dcf30b47acd30`（`git rev-parse HEAD`，clone 實測）
- tree recursive：`truncated=false`，blob 1988、tree 391
- 根目錄檔案數：`DESKTOP/`=561, `FABRIC/`=1166, `FAR/`=25, `HG-KSEOS/`=234, `INTEGRATION/`=1, `README.md/`=1
- 歷史僅 6 筆（全新 mirror repo，非本地 `Fabric` repo 的續傳；GitHub `compare/243bf8fa...60ed68a6` → **HTTP 404**，即本地 HEAD 不存在於此 repo）：
  - `5059d4d944 chore(mirror): integrate Fabric + FAR + HG-KSEOS for external acceptance`
  - `ede6d3923b feat(mirror): add the Fabric governance subject (1166 files)`
  - `ddddd0d887 feat(mirror): add the desktop-effect plane slice (590 files)`
  - `23d995d09f fix(mirror): flatten an embedded git repo inside the desktop-effect slice`
  - `4a1a4f2912 chore: drop an API-response scratch file inadvertently captured`
  - `60ed68a68b docs(hgk): sync the upgraded README / AGENTS / User Guide`

**`INTEGRATION/MANIFEST.json`（全文）**

```json
{
 "schema": "FABRIC-INTEGRATION-MIRROR/1",
 "subjects": ["Fabric", "FAR", "Desktop-effect plane", "HG-KSEOS"],
 "binding": "Under the current Fabric governance contract, HG-KSEOS is the sole control plane; current canonical Hermes is bound as its governed Runtime/Orchestration Plane.",
 "purpose": "single-surface external acceptance of all subjects at once",
 "claim_ceiling": "MIRROR_OF_GOVERNED_ARTIFACTS_FOR_EXTERNAL_ACCEPTANCE_ONLY",
 "excluded": ["var/", "worktrees/", "evidence/ raw stores", ".venv/", "API KEY/"],
 "included_subject_state": {
   "hgk_commits": ["c0cb5cb canonical acceptance resolver", "c12412e ordering oracle"],
   "far_gate1": "CONFIRMS_USEFUL",
   "far_gate2": "authorized",
   "controls_implemented": ["C1","C2","C3","C4","C5","C6","C7","C8"],
   "independent_checker": "PASS"
 },
 "pending": ["desktop-effect plane slice: authorization-token refresh required; gate not bypassed"],
 "non_claims": ["NOT_EXTERNALLY_ACCEPTED","NOT_MERGED","NOT_RELEASED","NOT_PRODUCTION","NO_LIVE_WORLD_EFFECT"]
}
```

## 4. 身分證明（mirror ≡ 本地權威）

| 主體 | mirror 檔數 | 本地檔數 | 共同 | blob 相同 | blob 不同 | 工作樹 raw 差 | 其中 CRLF-only | **真實內容差** |
|---|---|---|---|---|---|---|---|---|
| FDA | 25 | 78 | 25 | 2 | 23 | 23 | 23 | **0** |
| FAR | 905 | 918 | 905 | 841 | 64 | 64 | 64 | **0** |

> `core.autocrlf=true`（兩側皆是）造就 raw sha 差；`\r\n→\n` 正規化後 **0 差異**。結論：**mirror 內容 = 本地權威內容，逐檔位元等價（模除換行）**。

### 4.1 FDA 共同檔逐檔登記（sha256 / bytes / 判定）

| # | path | local sha256 | mirror sha256 | verdict |
|---|---|---|---|---|
| 1 | `AGENTS.md` | `b5257a3e5d06c5781911c4ffbed19bdccc82c763158053842ddc89dcbe6f9e1a` | `d1af3cc1e32fe44a5ea2f5c81da8b95e4691f88e56ce43d46bfa3e0115f6cf7d` | CRLF_ONLY |
| 2 | `FDA_ASSET_REGISTRY.json` | `960c31939f094d6b23e441728bc55d784b3899bbfbb81a9b76038031b7d96dde` | `9fe43e0e260abba479ffbfafee9c89ef030f8f36c1d25fe331f8a951d923888f` | CRLF_ONLY |
| 3 | `FDA_DESKTOP_CAPABILITY_MATRIX.yaml` | `9406456db853e9e6597c30ed400240808c7b0c777dd49c34eb611bf4c863d6c4` | `83a2719c550fa9e02ee9d2874abfb6163eca69b5d5daf47603e660e2f158e190` | CRLF_ONLY |
| 4 | `FDA_DIRECTORY_TREE.txt` | `57ceaf69fb27c21da59fff188e3c1cf90575da7e7861a19d7387b191e5767c98` | `57ceaf69fb27c21da59fff188e3c1cf90575da7e7861a19d7387b191e5767c98` | IDENTICAL |
| 5 | `FDA_EXECUTION_BINDING.json` | `6a3269202d0dba0ba6c8bb0d6656e592dcda4042a0dc88e63fba732e3335b095` | `42a38166175ef1d48315c755ad4f7ad8543943cbb6ce9e5cba4b7e3749fad484` | CRLF_ONLY |
| 6 | `FDA_FOLDER_REORGANIZATION_RECEIPT.json` | `00d690f94a05aabc644e9c9cafc4664fc98602eeaa5e28f54d17ae6ee7e58cbe` | `00d690f94a05aabc644e9c9cafc4664fc98602eeaa5e28f54d17ae6ee7e58cbe` | IDENTICAL |
| 7 | `README.md` | `aa3084bac9c01af17868582b04c3405b673a7e16947f9c0cbf3f972eef2a20a9` | `7be43f9322a588a7e5f16f9df11ace90b4fbb9f0d3575c5d42b651155f79fb77` | CRLF_ONLY |
| 8 | `TEAM.md` | `1936a4651ef549cce50f5ecec9a45a712c7bf92adab0ffd12afa12ff3d43a311` | `1c18a127c61d6e27c702dd5be260a17f1b51861cd2f9849ff1e420b396a8b8a1` | CRLF_ONLY |
| 9 | `WO_FDA_XQ_002.yaml` | `6c80ff03511753175a627b501ae5a72fa9e5195bc3830d438e88a6bf979b3c87` | `7d6808854172e1369f7d4c8cc6d04967dc9104dcaa3f4c593f050b35035544b6` | CRLF_ONLY |
| 10 | `docs/FDA_USER_GUIDE.md` | `21a3d22b26e499b1bad10dc7fb0235402b460c3138e0fd719e7791d120815ee5` | `87d4f9cb532e3f9561dbc1e1fb2aee6e1ce29d36a47bbae53a153386674b8780` | CRLF_ONLY |
| 11 | `fda_lease.py` | `856580b533b547a82772de8624c78792d669cb11bb9cb99551c7141a06594db2` | `a38301c869254c1e1abe4fea081b5285264f5dda890749a6128035d174c511e5` | CRLF_ONLY |
| 12 | `fda_router.py` | `c3d64650a6e0c6fd3d99b5236c30c4cb03b7621be9763299e335ac1c6ed95e6c` | `757943c3cf48f667f1f6918660fdd1298321705ddd2178f54137fff3715b07e5` | CRLF_ONLY |
| 13 | `governance/FDA_DEFERRED_SEMIAUTO_CONTRACT.yaml` | `6e1c808e278592f2b4d75c6296b4b81d9e227a2f21e188c9594b18085bbf0f8f` | `d231f2db43bd61b9b30db6cca55baf2787e25509de775e34decfb1305a82421f` | CRLF_ONLY |
| 14 | `governance/FDA_INTEROP_DISPOSITION.yaml` | `9fac4d255030443f8031a5bfe62d8e204698cf664ada2b06a65986f347c7ee5e` | `918104da5a550c92747a92961ac2a38c2e25c0ecea66c64113b52b5a45dfde4a` | CRLF_ONLY |
| 15 | `governance/FDA_ROUTE_CHECK.yaml` | `05256d982f8634fe25a5cf6d6e85685ca8fdcd54163c913a4cb689f6d922a909` | `4ed3ee8038c66e21d6be90a8f6c8dcb38575d75877e63e6965db09669e9d2228` | CRLF_ONLY |
| 16 | `governance/FDA_XQ_PAPER_FIXTURE_MANIFEST.yaml` | `6a108d3a8c25221541c1eb9ac72d192412a9f0690d219f8dab0acf0694a4a2cf` | `b08ea5401e3e7ba4d12e125ff16a9281aa8cd239c47f5366d8e7347c6a5bb88f` | CRLF_ONLY |
| 17 | `independent_checker.py` | `9009713fd70392d64b84dcf0c1319adb5cfef51d260cd196c831c960f1bbe22e` | `02fafed44595d4a2fae1aa7b5101613d66747036c18f771fa77eccfc4bd6a2b9` | CRLF_ONLY |
| 18 | `test_xq_action_router.py` | `e8778f2d73349905455e7254a9f2e0f5f3a7195cd6503093aa6c54504d615c2c` | `8336f7a2eb1049be2e13117d0484f2c36dd254c0a61c4f9f7857f15c02f5db22` | CRLF_ONLY |
| 19 | `test_xq_build_drift.py` | `cf234c66e389900b517d437a6d2ec4d69977104876fc4ab898a6f4df1aaf8eb9` | `f8c6c618871d1288d9ca0e85e05c52e23252b9d75f08d31638615bf9487bfeb0` | CRLF_ONLY |
| 20 | `test_xq_native_adapter.py` | `89566c1a2c5070d524c74fd34a5e164cce5f2a888ee4abcaac6df1af4ac9f060` | `c184fe04ddf285ac2bbbf440b551814ca32af62d1fba387761e9e2b09ea8aa11` | CRLF_ONLY |
| 21 | `tests/test_fda_lease.py` | `8caeb1dba6715af44f038e095eccc2287eebc817dac6782a0eb29bd742383ee6` | `39177f1970748e82293a3e262d9eb9051dd33edc19578d552833456f1151bb24` | CRLF_ONLY |
| 22 | `tests/test_fda_router.py` | `64a52a017d0ef757fbc725afb6fdfb71bf2b41829723743345e123643b45ba13` | `e396f2e7b870097ace901453901ac53d0792fd10307d0ff50bbd755db53a50de` | CRLF_ONLY |
| 23 | `tests/test_fda_router_integration.py` | `654df5de873b6e71ec1b73bbfb3ca9a92ff4b4758ab558b3784a2f68452d6b97` | `c4306a0a0fcb4e9f901d39e103ab4247ddf3bbf7ecb2d0b15f2b0563c8140ebc` | CRLF_ONLY |
| 24 | `tests/test_fda_security.py` | `6b0e2f19268db5fb0507fd6b39034db36e46922a42a93dfa3e5eff6004c359b3` | `bba80a4d00efcd99278d20a2db5e890b72c0ba1949cfa95cede875914a4c1557` | CRLF_ONLY |
| 25 | `xq_native_adapter.py` | `7655c411b5dfebd2da01364f665d82a5c31db7ad66ba2ce0521214401915ddc4` | `92bc33bb2449c52bc6a62af0ff2eee26501948c3e6ecd585650183e986cd3820` | CRLF_ONLY |

### 4.2 FAR 共同檔全量登記（905 檔）

| # | path | local sha256 | mirror sha256 | verdict |
|---|---|---|---|---|
| 1 | `AGENTS.md` | `a4d4d6fcb7e56f4293e2fdbcd168427d3253df2ba033c2ecc524a4965b8cba9e` | `a4d4d6fcb7e56f4293e2fdbcd168427d3253df2ba033c2ecc524a4965b8cba9e` | IDENTICAL |
| 2 | `FAR_DIRECTORY_TREE.txt` | `13d40a11dd27bde20df7be346bc022a754c63c75ba390de4e19b6b6d73c74eb0` | `e583656e98d6f20c790f45894f7fc1a678f778a2ade305bc1b0143b9149264c0` | CRLF_ONLY |
| 3 | `FAR_FINAL_ACCEPTANCE_EVIDENCE.md` | `b0b21ced799face772327199e5b29ca1bf016b5177a06ffe9ee1832efa653d40` | `b0b21ced799face772327199e5b29ca1bf016b5177a06ffe9ee1832efa653d40` | IDENTICAL |
| 4 | `FAR_FINAL_HARDENING_ACCEPTANCE_EVIDENCE.md` | `1e74bbca65638866133ebb7a57b11b302444e3173400d2e14b7a9de2a7623cc0` | `1e74bbca65638866133ebb7a57b11b302444e3173400d2e14b7a9de2a7623cc0` | IDENTICAL |
| 5 | `FAR_HARDENING_FINAL_EVIDENCE_MANIFEST.json` | `b1c7733a07f810aba41f8e79edd4c9330324e6b037d7d677e45e4bcde90fe99c` | `b1c7733a07f810aba41f8e79edd4c9330324e6b037d7d677e45e4bcde90fe99c` | IDENTICAL |
| 6 | `FAR_HARDENING_FINAL_INTAKE.json` | `e6e7eabab1d3e1dc04027f8b88509e2d82b593fbe5742145b655d31e98e787ab` | `e6e7eabab1d3e1dc04027f8b88509e2d82b593fbe5742145b655d31e98e787ab` | IDENTICAL |
| 7 | `FAR_HARDENING_FINAL_SUBJECT_MANIFEST.json` | `70e05d6491067cfa2c2d33e6431bfd08108f85628cf5d03540ef4b1ac082566c` | `70e05d6491067cfa2c2d33e6431bfd08108f85628cf5d03540ef4b1ac082566c` | IDENTICAL |
| 8 | `FAR_LONG_HORIZON_CONTRACT.yaml` | `5b000850417005f64865c38bb9784f4734dbb4ec600ec3a34e218893178113eb` | `245a33a0118e727e4772741986a789c8d5943c67547588c8e58ba51a9e881368` | CRLF_ONLY |
| 9 | `FAR_ROUTE_CHECK.yaml` | `b8556fbfc3b1cbf26b83df572051f867400d65b325c3b4d4de78dd7a062f1efc` | `cf7c1d4dbeb31f51e61a73696e751bb5bd2122367f2ea067b1839c0a3aa6f168` | CRLF_ONLY |
| 10 | `README.md` | `09a8183e98b7b547bd472e0f3f441141ff6a872508f01148d5131521e291ec48` | `09a8183e98b7b547bd472e0f3f441141ff6a872508f01148d5131521e291ec48` | IDENTICAL |
| 11 | `TEAM.md` | `479235fedb658d25a3d237388a47fb86e46b2e00c49193423a6e939941b88b00` | `479235fedb658d25a3d237388a47fb86e46b2e00c49193423a6e939941b88b00` | IDENTICAL |
| 12 | `canary/FAR-20260813-001/CandidateKnowledge.yaml` | `27971be093e7cb834b51b64b06c180600a2763eccbcca00c62e2f25bf17d0229` | `27971be093e7cb834b51b64b06c180600a2763eccbcca00c62e2f25bf17d0229` | IDENTICAL |
| 13 | `canary/FAR-20260813-001/CandidateResearch.yaml` | `64ab598926bfe21aca97f253ac588d28240530469e0bea80aa3a2b1c41d57923` | `64ab598926bfe21aca97f253ac588d28240530469e0bea80aa3a2b1c41d57923` | IDENTICAL |
| 14 | `canary/FAR-20260813-001/ClaimLedger.tsv` | `c996162edf57053bc0748aa4b831c6751089718fe9d844ea34768842e32fc8ed` | `c996162edf57053bc0748aa4b831c6751089718fe9d844ea34768842e32fc8ed` | IDENTICAL |
| 15 | `canary/FAR-20260813-001/ContradictionLedger.tsv` | `7d7685a51f69a67f561fe6f28659413dfa7ef3631a00e52ffc3dc4a5b2a07ef3` | `7d7685a51f69a67f561fe6f28659413dfa7ef3631a00e52ffc3dc4a5b2a07ef3` | IDENTICAL |
| 16 | `canary/FAR-20260813-001/ExtractionLedger.jsonl` | `ee5aaaa2338a3df10945cbb75abfcb0bfd12802655334a2945ad27f644dd78bc` | `ee5aaaa2338a3df10945cbb75abfcb0bfd12802655334a2945ad27f644dd78bc` | IDENTICAL |
| 17 | `canary/FAR-20260813-001/FitGapLedger.tsv` | `6fc7d47783e3524c784d4489c8d60f5699b59ee20dc8c88a466b969138207df7` | `6fc7d47783e3524c784d4489c8d60f5699b59ee20dc8c88a466b969138207df7` | IDENTICAL |
| 18 | `canary/FAR-20260813-001/HypothesisLedger.tsv` | `256c38c1db32541d978fb4dd6841e2afcd5b4c0f210ff35a0d11acc6c1d442a1` | `256c38c1db32541d978fb4dd6841e2afcd5b4c0f210ff35a0d11acc6c1d442a1` | IDENTICAL |
| 19 | `canary/FAR-20260813-001/OpenQuestionLedger.tsv` | `b8e0594638a40ef24435132df80711accf6ed3cb2b74f60a0d3538760f3afaf2` | `b8e0594638a40ef24435132df80711accf6ed3cb2b74f60a0d3538760f3afaf2` | IDENTICAL |
| 20 | `canary/FAR-20260813-001/ProposedEvolution.yaml` | `448349620e8a3eb7137419c46aec685290d4a509165b967e2d1ad99e10fe08e8` | `448349620e8a3eb7137419c46aec685290d4a509165b967e2d1ad99e10fe08e8` | IDENTICAL |
| 21 | `canary/FAR-20260813-001/QueryLedger.tsv` | `12d33cf11bce77095fe0634f4581e0bc7d677ab2c1f6a43e2423fbe1552c1ab2` | `12d33cf11bce77095fe0634f4581e0bc7d677ab2c1f6a43e2423fbe1552c1ab2` | IDENTICAL |
| 22 | `canary/FAR-20260813-001/RejectedAlternativeLedger.tsv` | `748cf327d109ca352f31ce82a432ca5e0b88b0c476319e3809d81fcdf24d3bf9` | `748cf327d109ca352f31ce82a432ca5e0b88b0c476319e3809d81fcdf24d3bf9` | IDENTICAL |
| 23 | `canary/FAR-20260813-001/ResearchHandoff.yaml` | `bc6600174519a6ae31e592a07bed0862aa148af23cb5603210f172c5d8a66425` | `bc6600174519a6ae31e592a07bed0862aa148af23cb5603210f172c5d8a66425` | IDENTICAL |
| 24 | `canary/FAR-20260813-001/ResearchPlan.yaml` | `a9b8c7a6daf923abcc0a5206195ab01d0f82b9e79ddd2c94db209cd943fcbf32` | `a9b8c7a6daf923abcc0a5206195ab01d0f82b9e79ddd2c94db209cd943fcbf32` | IDENTICAL |
| 25 | `canary/FAR-20260813-001/ResearchRequest.yaml` | `29e178aa074c98164af205b91974a8324be397bba8ffe5ca7abc6f6abd095302` | `29e178aa074c98164af205b91974a8324be397bba8ffe5ca7abc6f6abd095302` | IDENTICAL |
| 26 | `canary/FAR-20260813-001/ResearchRunReceipt.json` | `28f4751b04c0f120f4f0311b5cbdbc066be1214b85e6ae00670d0bdc55a74264` | `28f4751b04c0f120f4f0311b5cbdbc066be1214b85e6ae00670d0bdc55a74264` | IDENTICAL |
| 27 | `canary/FAR-20260813-001/ResearchSourceDenominator.tsv` | `27351e5bddf1c403c54eb4a2e28c11d72582df761ae0eb3b949094d89d9a0bda` | `27351e5bddf1c403c54eb4a2e28c11d72582df761ae0eb3b949094d89d9a0bda` | IDENTICAL |
| 28 | `canary/FAR-20260813-001/ResearchSynthesis.md` | `88ef08fc014012322ff103c9bd0b40387af26a2cd7fdde31c237096ee82f420a` | `88ef08fc014012322ff103c9bd0b40387af26a2cd7fdde31c237096ee82f420a` | IDENTICAL |
| 29 | `canary/FAR-20260813-001/SourceDispositionLedger.tsv` | `bc73245f416aad89c8151ee8b3d85be89a05ed7510a984981300ef9dee7d3296` | `bc73245f416aad89c8151ee8b3d85be89a05ed7510a984981300ef9dee7d3296` | IDENTICAL |
| 30 | `canary/FAR-20260813-001/SourceSnapshotLedger.tsv` | `078ed79fb3cf82afe71c326d3b4c95cb4355adc6ead876f12a374738108681c1` | `078ed79fb3cf82afe71c326d3b4c95cb4355adc6ead876f12a374738108681c1` | IDENTICAL |
| 31 | `canary/FAR-20260813-002/CandidateKnowledge.yaml` | `9ced4398c8005e34c2f843a6bb1bc2e5f10d800cf298952ff3d441db1921a2e3` | `9ced4398c8005e34c2f843a6bb1bc2e5f10d800cf298952ff3d441db1921a2e3` | IDENTICAL |
| 32 | `canary/FAR-20260813-002/CandidateResearch.yaml` | `04508e833ae29cadcc6a5b0b5b1b8a8f58a7bd0424f26497d3c2b3c5a5f91538` | `04508e833ae29cadcc6a5b0b5b1b8a8f58a7bd0424f26497d3c2b3c5a5f91538` | IDENTICAL |
| 33 | `canary/FAR-20260813-002/ClaimLedger.tsv` | `0676060ee33035984e9b9dc8dce1a193aceb90973d500432fbc149b3626650aa` | `0676060ee33035984e9b9dc8dce1a193aceb90973d500432fbc149b3626650aa` | IDENTICAL |
| 34 | `canary/FAR-20260813-002/ContradictionLedger.tsv` | `446bbff21bef34f88c2588f6421ac00c4752d2424f75d15708c3f0d39eb394e3` | `446bbff21bef34f88c2588f6421ac00c4752d2424f75d15708c3f0d39eb394e3` | IDENTICAL |
| 35 | `canary/FAR-20260813-002/DisagreementLedger.tsv` | `d4b66dde431de39bced6f41b859914d41dd9734b4bd4254c078d66f3fba38001` | `d4b66dde431de39bced6f41b859914d41dd9734b4bd4254c078d66f3fba38001` | IDENTICAL |
| 36 | `canary/FAR-20260813-002/ExtractionLedger.jsonl` | `9b96f9b01466dab9fa4bc696c4a27d82452d8372ac17c606f0649914c2fb42b3` | `9b96f9b01466dab9fa4bc696c4a27d82452d8372ac17c606f0649914c2fb42b3` | IDENTICAL |
| 37 | `canary/FAR-20260813-002/FitGapLedger.tsv` | `af22b59dc2ba62d04c803f922561587331500eea9dd926d2eeade5baff95fff5` | `af22b59dc2ba62d04c803f922561587331500eea9dd926d2eeade5baff95fff5` | IDENTICAL |
| 38 | `canary/FAR-20260813-002/HypothesisLedger.tsv` | `ae048f0ecc635cc923b17ebd6eafba8916dd66f541c7c3a4da29a37a141c16c2` | `ae048f0ecc635cc923b17ebd6eafba8916dd66f541c7c3a4da29a37a141c16c2` | IDENTICAL |
| 39 | `canary/FAR-20260813-002/OpenQuestionLedger.tsv` | `0d1d5ee227822f8d2b312a5b1f5df1e201274552715ca6b16c790255e556a5fc` | `0d1d5ee227822f8d2b312a5b1f5df1e201274552715ca6b16c790255e556a5fc` | IDENTICAL |
| 40 | `canary/FAR-20260813-002/ProposedEvolution.yaml` | `4bae9eaba4eea7f74f6082b9cad2236ca3928f8020c00c86a3f8f7efb79e1dc7` | `4bae9eaba4eea7f74f6082b9cad2236ca3928f8020c00c86a3f8f7efb79e1dc7` | IDENTICAL |
| 41 | `canary/FAR-20260813-002/QueryLedger.tsv` | `68e6bccf27ab2796d89aafe5f84a66b2d7725cf0207b0eb72b9895bddc9db9a5` | `68e6bccf27ab2796d89aafe5f84a66b2d7725cf0207b0eb72b9895bddc9db9a5` | IDENTICAL |
| 42 | `canary/FAR-20260813-002/RejectedAlternativeLedger.tsv` | `ab2052582c45d66e8eceeaab35699d8519f9275114d1f61c12b41c9ea12f15ae` | `ab2052582c45d66e8eceeaab35699d8519f9275114d1f61c12b41c9ea12f15ae` | IDENTICAL |
| 43 | `canary/FAR-20260813-002/ResearchHandoff.yaml` | `2eabe56113a20320967ab729dbc67c9d75c3cfecbe9d0fb405d3c07e3ea431d5` | `2eabe56113a20320967ab729dbc67c9d75c3cfecbe9d0fb405d3c07e3ea431d5` | IDENTICAL |
| 44 | `canary/FAR-20260813-002/ResearchPlan.yaml` | `0e7f8c18058834a3c8a4fe6352562ddb1ed4884b878f77d7e2151dac8b0aac4c` | `0e7f8c18058834a3c8a4fe6352562ddb1ed4884b878f77d7e2151dac8b0aac4c` | IDENTICAL |
| 45 | `canary/FAR-20260813-002/ResearchRequest.yaml` | `19fab4830c1e73c205e113841f84f7461d590fe3cbcf494b5a149a290b610b5e` | `19fab4830c1e73c205e113841f84f7461d590fe3cbcf494b5a149a290b610b5e` | IDENTICAL |
| 46 | `canary/FAR-20260813-002/ResearchRunReceipt.json` | `16ab001000f4b346cebbec43b1541f9b0f00ebd96371ea2479e66044becab9f3` | `16ab001000f4b346cebbec43b1541f9b0f00ebd96371ea2479e66044becab9f3` | IDENTICAL |
| 47 | `canary/FAR-20260813-002/ResearchSourceDenominator.tsv` | `f3c3def5ec2294a655a1aec3e79ef2d54ce7fd2f42ce1d6f1543089d4221282d` | `f3c3def5ec2294a655a1aec3e79ef2d54ce7fd2f42ce1d6f1543089d4221282d` | IDENTICAL |
| 48 | `canary/FAR-20260813-002/ResearchSynthesis.md` | `165e28381f78e5d009e23527175b4b52db9d4ff1fb40dbf5b8c85b0841f193c2` | `165e28381f78e5d009e23527175b4b52db9d4ff1fb40dbf5b8c85b0841f193c2` | IDENTICAL |
| 49 | `canary/FAR-20260813-002/SourceDispositionLedger.tsv` | `6386672932a166c1f70576ff7c2016fe1ef5923fb9d7f46cea442650bc0c6c3e` | `6386672932a166c1f70576ff7c2016fe1ef5923fb9d7f46cea442650bc0c6c3e` | IDENTICAL |
| 50 | `canary/FAR-20260813-002/SourceSnapshotLedger.tsv` | `73365237310dfef9c5294b62ab09c9461fb2d6f8353029c7411b288276bca660` | `73365237310dfef9c5294b62ab09c9461fb2d6f8353029c7411b288276bca660` | IDENTICAL |
| 51 | `canary/FAR-20260813-003/CrossReferenceLedger.tsv` | `9bbc1ff7c49ffa9fae015b0d4892cab64d398c038b8fb171ea5679ff8a084380` | `6022b4a1b0f0e6b2fe8a6ac2e6999367a5b76f299a8b535002863f549782c7e7` | CRLF_ONLY |
| 52 | `canary/FAR-20260813-003/RetrievalLedger.json` | `1b7c898d699e6ea7ab2d41514d665065229e65a226ccd2ec326cf31c32ebe935` | `1b7c898d699e6ea7ab2d41514d665065229e65a226ccd2ec326cf31c32ebe935` | IDENTICAL |
| 53 | `canary/FAR-20260813-003/RetrievalSynthesis.json` | `ff9e35e5c67e50ee8f583feb86a63b997508efb7856fd43d080548059bdbfd6c` | `ff9e35e5c67e50ee8f583feb86a63b997508efb7856fd43d080548059bdbfd6c` | IDENTICAL |
| 54 | `canary/FAR-20260813-004-tri-source-design/CrossReferenceLedger.tsv` | `8eb32e81b5b8a030551cacff2a0bbfe415e9fc7340cfdd99f608370fd1a30566` | `b19b65b273d4385540d926e564cb15d6b3c4a9d787d5d865fa6523191aa906c8` | CRLF_ONLY |
| 55 | `canary/FAR-20260813-004-tri-source-design/RetrievalLedger.json` | `8f4bc2e4edca435a96555555a9d460729df3e27a061edbecd6c9bbcf60f28e06` | `8f4bc2e4edca435a96555555a9d460729df3e27a061edbecd6c9bbcf60f28e06` | IDENTICAL |
| 56 | `canary/FAR-20260813-005-trisource-canaries/CANARY-4_stale_memory.json` | `98b19b996dfec647ac3d505d94c1e9714bc415ca613a89cdad921abd68e50b00` | `98b19b996dfec647ac3d505d94c1e9714bc415ca613a89cdad921abd68e50b00` | IDENTICAL |
| 57 | `canary/FAR-20260813-005-trisource-canaries/CANARY-5_web_outage.json` | `5d471e35a4ddef010e38e85077f97e50e66a1e3adfa53d6f630235e0b49e17ea` | `5d471e35a4ddef010e38e85077f97e50e66a1e3adfa53d6f630235e0b49e17ea` | IDENTICAL |
| 58 | `canary/FAR-20260813-006-trisource-real/AdjudicatedClaims.json` | `2b4d6056b7924135835c44581099cca795d0b12573f0928b6fe1a019c895304d` | `2b4d6056b7924135835c44581099cca795d0b12573f0928b6fe1a019c895304d` | IDENTICAL |
| 59 | `canary/FAR-20260813-006-trisource-real/RetrievalLedger.json` | `940dec8a0c3cb7ebc321f031fdc7c30374a190994f2648205920202e6c71953f` | `940dec8a0c3cb7ebc321f031fdc7c30374a190994f2648205920202e6c71953f` | IDENTICAL |
| 60 | `canary/FAR-20260813-006-trisource-real/TriSourceCoverageReceipt.json` | `f131b53361a23a8678e877dbc44036a8c849b6814dad290b481a54241a9ce184` | `f131b53361a23a8678e877dbc44036a8c849b6814dad290b481a54241a9ce184` | IDENTICAL |
| 61 | `canary/FAR-20260814-007-hardening/CANARY-7_swarm.json` | `324730842cc620fb9e592c6ad090571045243b5878c83460a38edb2910ce1054` | `324730842cc620fb9e592c6ad090571045243b5878c83460a38edb2910ce1054` | IDENTICAL |
| 62 | `canary/FAR-20260814-007-hardening/CANARY-H1_H5.json` | `60984082e84ca599c630585eba136ad00d22d94c2dc74d58b2a6dfa55f3961b3` | `60984082e84ca599c630585eba136ad00d22d94c2dc74d58b2a6dfa55f3961b3` | IDENTICAL |
| 63 | `canary/FAR-20260814-007-hardening/TEST_DENOMINATOR.json` | `4cc8c6938ea366262bb88248a9898ba34a544dd8f201b82f5691b02736d83cca` | `4cc8c6938ea366262bb88248a9898ba34a544dd8f201b82f5691b02736d83cca` | IDENTICAL |
| 64 | `canary/LH-CANARY-001/ResearchCompletionContract.marker` | `037b5c83d622267483aaeb9a264f1870e2a69dfe891622a2ababb7f978518836` | `037b5c83d622267483aaeb9a264f1870e2a69dfe891622a2ababb7f978518836` | IDENTICAL |
| 65 | `canary/LH-CANARY-001/checkpoint.json` | `350d0706f12cad94b6dcf4b2106d90eb76c9cf66c3626812b009f33564d2e7bf` | `350d0706f12cad94b6dcf4b2106d90eb76c9cf66c3626812b009f33564d2e7bf` | IDENTICAL |
| 66 | `canary/LH-CANARY-001/worker.log` | `60b75e387a6e1f013eb21244e762208e8ca0a72bb4a75ccc890ec32039742320` | `60b75e387a6e1f013eb21244e762208e8ca0a72bb4a75ccc890ec32039742320` | IDENTICAL |
| 67 | `canary/LH-CANARY-001/worker.pid` | `94838f458b4bc3aa9d7ba23bf1ac8941b619512f677c153978ad4e22afd1fd3f` | `94838f458b4bc3aa9d7ba23bf1ac8941b619512f677c153978ad4e22afd1fd3f` | IDENTICAL |
| 68 | `docs/fabric-autonomous-research_使用說明手冊_v2026.08.13-r1.md` | `326ae50937770a41c7b26ad008bb6876572bd2e9e166f64c2226e222d0dd38b6` | `bbb256411dd8fcd75db3fcd866975053252bc784843e30f3709318fece14c356` | CRLF_ONLY |
| 69 | `evidence-bundle/raw-canary/FAR-20260813-001/CandidateKnowledge.yaml` | `27971be093e7cb834b51b64b06c180600a2763eccbcca00c62e2f25bf17d0229` | `27971be093e7cb834b51b64b06c180600a2763eccbcca00c62e2f25bf17d0229` | IDENTICAL |
| 70 | `evidence-bundle/raw-canary/FAR-20260813-001/CandidateResearch.yaml` | `64ab598926bfe21aca97f253ac588d28240530469e0bea80aa3a2b1c41d57923` | `64ab598926bfe21aca97f253ac588d28240530469e0bea80aa3a2b1c41d57923` | IDENTICAL |
| 71 | `evidence-bundle/raw-canary/FAR-20260813-001/ClaimLedger.tsv` | `c996162edf57053bc0748aa4b831c6751089718fe9d844ea34768842e32fc8ed` | `c996162edf57053bc0748aa4b831c6751089718fe9d844ea34768842e32fc8ed` | IDENTICAL |
| 72 | `evidence-bundle/raw-canary/FAR-20260813-001/ContradictionLedger.tsv` | `7d7685a51f69a67f561fe6f28659413dfa7ef3631a00e52ffc3dc4a5b2a07ef3` | `7d7685a51f69a67f561fe6f28659413dfa7ef3631a00e52ffc3dc4a5b2a07ef3` | IDENTICAL |
| 73 | `evidence-bundle/raw-canary/FAR-20260813-001/ExtractionLedger.jsonl` | `ee5aaaa2338a3df10945cbb75abfcb0bfd12802655334a2945ad27f644dd78bc` | `ee5aaaa2338a3df10945cbb75abfcb0bfd12802655334a2945ad27f644dd78bc` | IDENTICAL |
| 74 | `evidence-bundle/raw-canary/FAR-20260813-001/FitGapLedger.tsv` | `6fc7d47783e3524c784d4489c8d60f5699b59ee20dc8c88a466b969138207df7` | `6fc7d47783e3524c784d4489c8d60f5699b59ee20dc8c88a466b969138207df7` | IDENTICAL |
| 75 | `evidence-bundle/raw-canary/FAR-20260813-001/HypothesisLedger.tsv` | `256c38c1db32541d978fb4dd6841e2afcd5b4c0f210ff35a0d11acc6c1d442a1` | `256c38c1db32541d978fb4dd6841e2afcd5b4c0f210ff35a0d11acc6c1d442a1` | IDENTICAL |
| 76 | `evidence-bundle/raw-canary/FAR-20260813-001/OpenQuestionLedger.tsv` | `b8e0594638a40ef24435132df80711accf6ed3cb2b74f60a0d3538760f3afaf2` | `b8e0594638a40ef24435132df80711accf6ed3cb2b74f60a0d3538760f3afaf2` | IDENTICAL |
| 77 | `evidence-bundle/raw-canary/FAR-20260813-001/ProposedEvolution.yaml` | `448349620e8a3eb7137419c46aec685290d4a509165b967e2d1ad99e10fe08e8` | `448349620e8a3eb7137419c46aec685290d4a509165b967e2d1ad99e10fe08e8` | IDENTICAL |
| 78 | `evidence-bundle/raw-canary/FAR-20260813-001/QueryLedger.tsv` | `12d33cf11bce77095fe0634f4581e0bc7d677ab2c1f6a43e2423fbe1552c1ab2` | `12d33cf11bce77095fe0634f4581e0bc7d677ab2c1f6a43e2423fbe1552c1ab2` | IDENTICAL |
| 79 | `evidence-bundle/raw-canary/FAR-20260813-001/RejectedAlternativeLedger.tsv` | `748cf327d109ca352f31ce82a432ca5e0b88b0c476319e3809d81fcdf24d3bf9` | `748cf327d109ca352f31ce82a432ca5e0b88b0c476319e3809d81fcdf24d3bf9` | IDENTICAL |
| 80 | `evidence-bundle/raw-canary/FAR-20260813-001/ResearchHandoff.yaml` | `bc6600174519a6ae31e592a07bed0862aa148af23cb5603210f172c5d8a66425` | `bc6600174519a6ae31e592a07bed0862aa148af23cb5603210f172c5d8a66425` | IDENTICAL |
| 81 | `evidence-bundle/raw-canary/FAR-20260813-001/ResearchPlan.yaml` | `a9b8c7a6daf923abcc0a5206195ab01d0f82b9e79ddd2c94db209cd943fcbf32` | `a9b8c7a6daf923abcc0a5206195ab01d0f82b9e79ddd2c94db209cd943fcbf32` | IDENTICAL |
| 82 | `evidence-bundle/raw-canary/FAR-20260813-001/ResearchRequest.yaml` | `29e178aa074c98164af205b91974a8324be397bba8ffe5ca7abc6f6abd095302` | `29e178aa074c98164af205b91974a8324be397bba8ffe5ca7abc6f6abd095302` | IDENTICAL |
| 83 | `evidence-bundle/raw-canary/FAR-20260813-001/ResearchRunReceipt.json` | `28f4751b04c0f120f4f0311b5cbdbc066be1214b85e6ae00670d0bdc55a74264` | `28f4751b04c0f120f4f0311b5cbdbc066be1214b85e6ae00670d0bdc55a74264` | IDENTICAL |
| 84 | `evidence-bundle/raw-canary/FAR-20260813-001/ResearchSourceDenominator.tsv` | `27351e5bddf1c403c54eb4a2e28c11d72582df761ae0eb3b949094d89d9a0bda` | `27351e5bddf1c403c54eb4a2e28c11d72582df761ae0eb3b949094d89d9a0bda` | IDENTICAL |
| 85 | `evidence-bundle/raw-canary/FAR-20260813-001/ResearchSynthesis.md` | `88ef08fc014012322ff103c9bd0b40387af26a2cd7fdde31c237096ee82f420a` | `88ef08fc014012322ff103c9bd0b40387af26a2cd7fdde31c237096ee82f420a` | IDENTICAL |
| 86 | `evidence-bundle/raw-canary/FAR-20260813-001/SourceDispositionLedger.tsv` | `bc73245f416aad89c8151ee8b3d85be89a05ed7510a984981300ef9dee7d3296` | `bc73245f416aad89c8151ee8b3d85be89a05ed7510a984981300ef9dee7d3296` | IDENTICAL |
| 87 | `evidence-bundle/raw-canary/FAR-20260813-001/SourceSnapshotLedger.tsv` | `078ed79fb3cf82afe71c326d3b4c95cb4355adc6ead876f12a374738108681c1` | `078ed79fb3cf82afe71c326d3b4c95cb4355adc6ead876f12a374738108681c1` | IDENTICAL |
| 88 | `evidence-bundle/raw-canary/FAR-20260813-006-trisource-real/AdjudicatedClaims.json` | `6ee541940314db7e8edf289977529cf401ef10575b0536468291c8f0182d90b9` | `6ee541940314db7e8edf289977529cf401ef10575b0536468291c8f0182d90b9` | IDENTICAL |
| 89 | `evidence-bundle/raw-canary/FAR-20260813-006-trisource-real/RetrievalLedger.json` | `c67e2a3d337b2ebfa52e49bc619c236d644c17dd86418dcd46827e5e92d82969` | `c67e2a3d337b2ebfa52e49bc619c236d644c17dd86418dcd46827e5e92d82969` | IDENTICAL |
| 90 | `evidence-bundle/raw-canary/FAR-20260813-006-trisource-real/TriSourceCoverageReceipt.json` | `5cface880d80c10c6e5c4c1e74697dfcf16461f3138f5dcbfea0b5f3ae7fd7e3` | `5cface880d80c10c6e5c4c1e74697dfcf16461f3138f5dcbfea0b5f3ae7fd7e3` | IDENTICAL |
| 91 | `evidence-bundle/raw-github/github_d_research.json` | `e0d1a4028e1562ad4b4a2e2ee0833a533c67ba6bd731b130b1752ef28640153a` | `e0d1a4028e1562ad4b4a2e2ee0833a533c67ba6bd731b130b1752ef28640153a` | IDENTICAL |
| 92 | `evidence-bundle/raw-github/github_d_research_r2.json` | `a8cb0ff8195e6ef8ecfb4cc2d2fbcb5a0425feba609afabb2f404eb3374adf97` | `a8cb0ff8195e6ef8ecfb4cc2d2fbcb5a0425feba609afabb2f404eb3374adf97` | IDENTICAL |
| 93 | `evidence-bundle/raw-kanban/far-external-closure_snapshot_final.txt` | `6e2101892fd4bd5711fdc78ad3e0f2b22e7c3df7184906690fca1346dcdf8bef` | `6e2101892fd4bd5711fdc78ad3e0f2b22e7c3df7184906690fca1346dcdf8bef` | IDENTICAL |
| 94 | `evidence-bundle/raw-kanban/far-first-use_snapshot.txt` | `c6779507a4365c9dad1f78644390021fd857161792082c2d5a5cc6ddbe620a1e` | `c6779507a4365c9dad1f78644390021fd857161792082c2d5a5cc6ddbe620a1e` | IDENTICAL |
| 95 | `evidence-bundle/raw-kanban/far-first-use_snapshot_final.txt` | `2abdec76a31c2057220b18ddcda6927a75e1927249a436c0c15890e984ec4756` | `2abdec76a31c2057220b18ddcda6927a75e1927249a436c0c15890e984ec4756` | IDENTICAL |
| 96 | `evidence-bundle/raw-kanban/far-implementation_snapshot.txt` | `cc7ffa99fc8f321a295af6b51cdba346f4dd2ee2a46d2bcc8354e118ae5e9994` | `cc7ffa99fc8f321a295af6b51cdba346f4dd2ee2a46d2bcc8354e118ae5e9994` | IDENTICAL |
| 97 | `evidence-bundle/raw-kanban/far-implementation_snapshot_final.txt` | `8d09bc2fc896d9678cb33bb3eadaf9f6ad6d902f135dd77ec5636bd02bb67813` | `8d09bc2fc896d9678cb33bb3eadaf9f6ad6d902f135dd77ec5636bd02bb67813` | IDENTICAL |
| 98 | `evidence-bundle/raw-receipts/FAR_AO_LANE_RECEIPT.json` | `af0d6c07ce64f1bd20fcd0f40811aeedaa543e6b8f56e1c46b77945dce8323ca` | `a225e3d87b544be9369d89fdc88bdba72e439fdbb5b0d417c62d2805be339489` | CRLF_ONLY |
| 99 | `evidence-bundle/raw-receipts/FAR_ARIS_EFFECTIVE_LOAD_RECEIPT.json` | `a8b3456e8f91bf222961de74d40e77b9f69635807d58481b45e390003de53283` | `a8b3456e8f91bf222961de74d40e77b9f69635807d58481b45e390003de53283` | IDENTICAL |
| 100 | `evidence-bundle/raw-receipts/FAR_ARIS_METHOD_DISPOSITION.yaml` | `d54db220bce5406c596e6a00e8d2e356daf1fb5541e8d562d716c061f8f3bfd4` | `f4e32479e3fc9d457f9e4bd3c8146b7df8439eef0b318c32d74b60210afa7c0a` | CRLF_ONLY |
| 101 | `evidence-bundle/raw-receipts/FAR_ARTIFACT_INDEX.json` | `83ab2f4aabded1c91d7ba788cb409cf32055a465a723a9b5f6e115321533e53a` | `83ab2f4aabded1c91d7ba788cb409cf32055a465a723a9b5f6e115321533e53a` | IDENTICAL |
| 102 | `evidence-bundle/raw-receipts/FAR_C0_CAPC_RECEIPT.json` | `d659d9f0656f7e57518a1df9d1c0f4f96d10a3fe2d826b1f675ae194d2c8e0a8` | `d5866b822cb26baceb677fdbfad2bbe4c562197f3b550f71e49191c75fded23c` | CRLF_ONLY |
| 103 | `evidence-bundle/raw-receipts/FAR_CAPABILITY_MATRIX.yaml` | `2469d85bf94f16886eb71b169b799fb243c8b5c6bdf3f627178140e9e1f6df6f` | `ecd20d1cb8d8a07b4cb6c3a5c3486bb91ae1e16478bc3837c1dc9f8ada20d081` | CRLF_ONLY |
| 104 | `evidence-bundle/raw-receipts/FAR_CHALLENGE_CLOSURE.json` | `66a373ab524d4cbbac9728f41eb4fe15c65c3cb51105e9b0dc379b0be09faf97` | `bdc158df8078cee895e4945e3d6696cf220546096615e66dc5e856106459ba17` | CRLF_ONLY |
| 105 | `evidence-bundle/raw-receipts/FAR_EVOLUTION_CANARY_RECEIPT.json` | `ea3b22e3dff092e38879ab9f3127b213419b41c3a358f7cd479d3a7219169f8d` | `ea3b22e3dff092e38879ab9f3127b213419b41c3a358f7cd479d3a7219169f8d` | IDENTICAL |
| 106 | `evidence-bundle/raw-receipts/FAR_EXECUTION_BINDING.json` | `87ae3bd2a7f07b875e7247bb3d34f3b843e90054d83aa802b24dcfc5985cd218` | `30de9e926afad8752682dcfaaee23dbb25f421ce0ff9043b42dfa43ce02f8977` | CRLF_ONLY |
| 107 | `evidence-bundle/raw-receipts/FAR_FIRST_USE_EVIDENCE.md` | `5d210253ebcdaee45566c58626dfdacf50a8a600bc66759273895ca867270fc1` | `5d210253ebcdaee45566c58626dfdacf50a8a600bc66759273895ca867270fc1` | IDENTICAL |
| 108 | `evidence-bundle/raw-receipts/FAR_FIRST_USE_INDEX.json` | `a1da01b3f089c8fa509117464107fbc7178ef777f18366520e218f03f00224c5` | `a1da01b3f089c8fa509117464107fbc7178ef777f18366520e218f03f00224c5` | IDENTICAL |
| 109 | `evidence-bundle/raw-receipts/FAR_GATES_RECEIPT.json` | `bc55f4bc0e0a75ca3484df80421da383e7ccad83c0e0973fccecd182a91c9662` | `bc55f4bc0e0a75ca3484df80421da383e7ccad83c0e0973fccecd182a91c9662` | IDENTICAL |
| 110 | `evidence-bundle/raw-receipts/FAR_IMPLEMENTATION_EVIDENCE.md` | `8c708e5cffd41516f4dd1f5735c9d374e8fca8dd95ff69be0af1e381f43687f8` | `8c708e5cffd41516f4dd1f5735c9d374e8fca8dd95ff69be0af1e381f43687f8` | IDENTICAL |
| 111 | `evidence-bundle/raw-receipts/FAR_INTEROP_DISPOSITION.yaml` | `bf6a9b00e548de21dc6b897c460eb057c3c96b0105cf131e9c639504b15d948f` | `bb7699118a60f777a7a2a049bb88f6c450fb28be57c62074e3c265382eb54301` | CRLF_ONLY |
| 112 | `evidence-bundle/raw-receipts/FAR_LONG_HORIZON_CONTRACT.yaml` | `0dccec95cfaa2d46a93c4e18ad0f18b9639c45e89ac00fe494e01eb6712b16a6` | `0fdf0ed4152f1bf93f2c66627991fbf57fd5782f9c7000203a70368e161b867e` | CRLF_ONLY |
| 113 | `evidence-bundle/raw-receipts/FAR_PRIME_QUALIFICATION_RECORD.yaml` | `d2a9c67c147caf459b9ede9c4f64afd854c0c232f7f0c7567455c3017136663d` | `4ec7fb4e65f6f362ba064e7450cb825351b5431b52b5b71d1e53e330d754a818` | CRLF_ONLY |
| 114 | `evidence-bundle/raw-receipts/FAR_Q0_CROSSWALK.md` | `f73e276cf1264708a1e0ef1b73d07192b03948fc3c2ce8b22453448c41e8d088` | `59fb27047558733f695d8e2c0e3fa99d0a93666851e8913fb5ff8924f6d5d1b5` | CRLF_ONLY |
| 115 | `evidence-bundle/raw-receipts/FAR_ROUTE_CHECK.yaml` | `bd6f5c113410065131e73f4a406d2e18f28ff82de50dc446a85314ba11b9de93` | `4e1c692768beec8f5c504544fea12af49f03752ec19f1eacff994472c5c5b92b` | CRLF_ONLY |
| 116 | `evidence-bundle/raw-receipts/FAR_SOURCE_SECURITY.yaml` | `c7afbff30c6caa3c7ff7c40d7915f271bfef8dca6314aabf1ba82ce5f3a2aba0` | `ddacd339695d68ea9b2e58ae537ed0fb88bd6cf353eb6efd05ed93884c79e192` | CRLF_ONLY |
| 117 | `evidence-bundle/raw-receipts/FAR_SWARM_Q10_RECEIPT.json` | `764b4f2945acc381d8576e329b4eef00433f39eed1d11401281e2029e560f2c8` | `8c311a8d139ba3b675c487278af57560f25b22d518754a670493b911240818e0` | CRLF_ONLY |
| 118 | `evidence-bundle/raw-receipts/TEAM.md` | `ae67143a2928b27ef4916a78b9e8f2bb46759cd9edb031c60c688c83926e8ae5` | `0247356a8578fe75c8cf4095592eea3978b32836824857579cfd84dbdecbda4e` | CRLF_ONLY |
| 119 | `evidence-bundle/raw-receipts/far_router.py` | `ade07192ae8d04776b67046ad90ffbf4cbcbe1d2fa0b3494a9d6a80057f23a3a` | `8644f623bc8c0f34b84f3c820423dd148456908e17dfbb15f3d2a78bcb59cccd` | CRLF_ONLY |
| 120 | `evidence-bundle/raw-receipts/far_source_security.py` | `5227edde39a04edc848df42d1faf089fcbd71f4a65d5da1a5a2b00390f375331` | `654536767159c215492272436a54e441a714c5f4f9a4561caae441a03f43fab3` | CRLF_ONLY |
| 121 | `evidence-bundle/raw-receipts/far_watchdog.py` | `852eb358303c95ab145eebb873e4740c6179710e11fce1c52e5c90a39599c346` | `2df969541fb88472d704493a62a019ca06334a4df1e760f346187a61aee62c79` | CRLF_ONLY |
| 122 | `evidence-bundle/raw-spine/far_spine_readback.json` | `7847dab4702990410aeda359ef790ffae1cf14b0d7e590a8bbfd35800ca1c350` | `7847dab4702990410aeda359ef790ffae1cf14b0d7e590a8bbfd35800ca1c350` | IDENTICAL |
| 123 | `evidence-bundle/raw-spine/far_spine_readback_final.json` | `46826ae9721a5c902a006b591bd8ba4f4ec1ccb8b09da69c105c669a9ea07e01` | `46826ae9721a5c902a006b591bd8ba4f4ec1ccb8b09da69c105c669a9ea07e01` | IDENTICAL |
| 124 | `evidence-bundle/raw-spine/far_spine_readback_final_r2.json` | `d24e8b80b8db38150395d582a1de59210a2f9644cb6e64d5f73344dac6632017` | `d24e8b80b8db38150395d582a1de59210a2f9644cb6e64d5f73344dac6632017` | IDENTICAL |
| 125 | `evidence-bundle/raw-tests/far_tests_suite.exitcode.txt` | `5feceb66ffc86f38d952786c6d696c79c2dbc239dd4e91b46729d73a27fb57e9` | `5feceb66ffc86f38d952786c6d696c79c2dbc239dd4e91b46729d73a27fb57e9` | IDENTICAL |
| 126 | `evidence-bundle/raw-tests/far_tests_suite.stderr.txt` | `a435a2adbec429eef6d00bffd724ab93ae3d2a6279b425f07b0b1335843affee` | `a435a2adbec429eef6d00bffd724ab93ae3d2a6279b425f07b0b1335843affee` | IDENTICAL |
| 127 | `evidence-bundle/raw-tests/far_tests_suite.stdout.txt` | `4aa600009eabd4ae334d7557e5094ab5d5f583208734d0e6c194339bc52453c5` | `3bfefd08551f876b75af1b83b1796f24ab70351fddd61d9453c48bef93a4d33a` | CRLF_ONLY |
| 128 | `far_retrieval.py` | `76db4f30001a2b7d74ed8fbd3c5adbfa618226ed82db78cdf23a186675f2b4c8` | `3165732037bf46497c7ce0b30dacc6c0c5132f7dbffdafe5cd1678b3b18f730a` | CRLF_ONLY |
| 129 | `far_router.py` | `ade07192ae8d04776b67046ad90ffbf4cbcbe1d2fa0b3494a9d6a80057f23a3a` | `8644f623bc8c0f34b84f3c820423dd148456908e17dfbb15f3d2a78bcb59cccd` | CRLF_ONLY |
| 130 | `far_source_security.py` | `5227edde39a04edc848df42d1faf089fcbd71f4a65d5da1a5a2b00390f375331` | `654536767159c215492272436a54e441a714c5f4f9a4561caae441a03f43fab3` | CRLF_ONLY |
| 131 | `far_trisource.py` | `9d18a78ca90c3eb75ae2ee1cf530412ffc20c001144482d805f55d802d3ecaaf` | `673823179734650045841e078a9cc24776a19330b2d15235b7cffa5b25428219` | CRLF_ONLY |
| 132 | `far_watchdog.py` | `852eb358303c95ab145eebb873e4740c6179710e11fce1c52e5c90a39599c346` | `2df969541fb88472d704493a62a019ca06334a4df1e760f346187a61aee62c79` | CRLF_ONLY |
| 133 | `governance/AO_FINDING_FAR_002.json` | `f72540ce6771d7e04366b3ee44607b828c8142690d87fd6b03a5f925aec3a30b` | `3366c7ed5a58364582c77d1233145ab1082742e5395bf6c02fa04087f7333462` | CRLF_ONLY |
| 134 | `governance/CLOSURE-EXT-FAR-001.json` | `63410756b5ae5a7d59ecc0258ef61b1fd069e2d5bb5b783742e6c62008d0ece9` | `63410756b5ae5a7d59ecc0258ef61b1fd069e2d5bb5b783742e6c62008d0ece9` | IDENTICAL |
| 135 | `governance/CLOSURE-EXT-FAR-002.json` | `bffdde4657649c732306ef2437c1f874fefc2c2daa35209f23ba64af42480d1a` | `bffdde4657649c732306ef2437c1f874fefc2c2daa35209f23ba64af42480d1a` | IDENTICAL |
| 136 | `governance/CLOSURE-EXT-FAR-003.json` | `d225b7f196c4992a27b23fdc3d64c813fb5b6edb0c956db9dfc00ff6054559a8` | `d225b7f196c4992a27b23fdc3d64c813fb5b6edb0c956db9dfc00ff6054559a8` | IDENTICAL |
| 137 | `governance/CLOSURE-EXT-FAR-004.json` | `bd724c24e126536fea10cbfe3b07417ad9bd5d8750dd3c9e640aa2711076f88a` | `bd724c24e126536fea10cbfe3b07417ad9bd5d8750dd3c9e640aa2711076f88a` | IDENTICAL |
| 138 | `governance/CLOSURE-EXT-FAR-005.json` | `a5a8e71d4039afec26a6d273d4244b21043708457349e36ff7ce185cb1cab3c4` | `a5a8e71d4039afec26a6d273d4244b21043708457349e36ff7ce185cb1cab3c4` | IDENTICAL |
| 139 | `governance/CLOSURE-EXT-FAR-006.json` | `c560c9c1aec42a7b2180c009fc2d58e358e3129ec4a74a9621d3d68416cf54d0` | `c560c9c1aec42a7b2180c009fc2d58e358e3129ec4a74a9621d3d68416cf54d0` | IDENTICAL |
| 140 | `governance/CLOSURE-EXT-FAR-007.json` | `21aa62e8f8708db4eeacaa965bad20615b2e9c1e0621a54665831f398d6a238a` | `21aa62e8f8708db4eeacaa965bad20615b2e9c1e0621a54665831f398d6a238a` | IDENTICAL |
| 141 | `governance/CLOSURE-EXT-FAR-008.json` | `daf8a07ab67ce62d9b2d6301aef22dc18c6a21b0e143e21c73e7a6af595f57a8` | `daf8a07ab67ce62d9b2d6301aef22dc18c6a21b0e143e21c73e7a6af595f57a8` | IDENTICAL |
| 142 | `governance/CLOSURE-EXT-FAR-009.json` | `3d7ce328a2987638db94ab21b0e516223f11971713434550993fb2ec90a843ee` | `3d7ce328a2987638db94ab21b0e516223f11971713434550993fb2ec90a843ee` | IDENTICAL |
| 143 | `governance/CLOSURE-EXT-FAR-010.json` | `a2dc08b9b18d933c6f5172898a8d9883c71a17b09f1e2508b5a073f4faf85295` | `a2dc08b9b18d933c6f5172898a8d9883c71a17b09f1e2508b5a073f4faf85295` | IDENTICAL |
| 144 | `governance/FAR_ACTIVATION_RECEIPT.json` | `f8f0e9aec6406c4f241e6dc7417ec24e8bda5aab7f82fdd3f8bcb47dbc3ca27a` | `0e4ea57ec4a84287f7c1f5745ff2c52b845a16827613e224b8e551896f051130` | CRLF_ONLY |
| 145 | `governance/FAR_ACTIVATION_RECEIPT_v3.json` | `639f90e7fcc0eaff71e3f557e1a9040096c5e6b4ffd117669a672c73efb2fcfa` | `dcb857cbacc98000cec86f54709920b2329d7a3dc4215dbd89ba00ea40b49bb0` | CRLF_ONLY |
| 146 | `governance/FAR_AO_LANE_RECEIPT.json` | `af0d6c07ce64f1bd20fcd0f40811aeedaa543e6b8f56e1c46b77945dce8323ca` | `a225e3d87b544be9369d89fdc88bdba72e439fdbb5b0d417c62d2805be339489` | CRLF_ONLY |
| 147 | `governance/FAR_ARIS_EFFECTIVE_LOAD_RECEIPT.json` | `a8b3456e8f91bf222961de74d40e77b9f69635807d58481b45e390003de53283` | `a8b3456e8f91bf222961de74d40e77b9f69635807d58481b45e390003de53283` | IDENTICAL |
| 148 | `governance/FAR_ARIS_METHOD_DISPOSITION.yaml` | `d54db220bce5406c596e6a00e8d2e356daf1fb5541e8d562d716c061f8f3bfd4` | `f4e32479e3fc9d457f9e4bd3c8146b7df8439eef0b318c32d74b60210afa7c0a` | CRLF_ONLY |
| 149 | `governance/FAR_C0_CAPC_RECEIPT.json` | `d659d9f0656f7e57518a1df9d1c0f4f96d10a3fe2d826b1f675ae194d2c8e0a8` | `d5866b822cb26baceb677fdbfad2bbe4c562197f3b550f71e49191c75fded23c` | CRLF_ONLY |
| 150 | `governance/FAR_CAPABILITY_MATRIX.yaml` | `d5868f098a09685d7e33fa650f1b8419d045a873e5ca37792b37a8fe582fd390` | `81e5dff31e93f26e8ad51212d9ce42e1cd4dc073aea77a18a73591689f63b1f6` | CRLF_ONLY |
| 151 | `governance/FAR_CHALLENGE_CLOSURE.json` | `66a373ab524d4cbbac9728f41eb4fe15c65c3cb51105e9b0dc379b0be09faf97` | `bdc158df8078cee895e4945e3d6696cf220546096615e66dc5e856106459ba17` | CRLF_ONLY |
| 152 | `governance/FAR_CODEX_RETRIEVAL_DEFECT_001.json` | `ef1a240e2d525b9630bc6a6c0b86b7a0f03fa96588652e9f94edda1516b3829f` | `e7618cac7ea9a87eec019bc492f1b3d0c80f20f61d181158143cd269fa48eb43` | CRLF_ONLY |
| 153 | `governance/FAR_EVOLUTION_CANARY_RECEIPT.json` | `ea3b22e3dff092e38879ab9f3127b213419b41c3a358f7cd479d3a7219169f8d` | `ea3b22e3dff092e38879ab9f3127b213419b41c3a358f7cd479d3a7219169f8d` | IDENTICAL |
| 154 | `governance/FAR_EXECUTION_BINDING.json` | `87ae3bd2a7f07b875e7247bb3d34f3b843e90054d83aa802b24dcfc5985cd218` | `30de9e926afad8752682dcfaaee23dbb25f421ce0ff9043b42dfa43ce02f8977` | CRLF_ONLY |
| 155 | `governance/FAR_EXTC_CAPC_RECEIPT.json` | `71cb1ad46f893d6ee142d67ce36c44f893e69f17a97b49b106768f78b5b0a0e7` | `71cb1ad46f893d6ee142d67ce36c44f893e69f17a97b49b106768f78b5b0a0e7` | IDENTICAL |
| 156 | `governance/FAR_EXTERNAL_REVIEW_PACKAGE_RECEIPT.json` | `52f0d02941384623e55a5ee503940867d2209962a1b751ba727cf6522554fd2f` | `52f0d02941384623e55a5ee503940867d2209962a1b751ba727cf6522554fd2f` | IDENTICAL |
| 157 | `governance/FAR_FOLDER_REORGANIZATION_RECEIPT.json` | `e4032d17dc70b5211dd23cb7019f6d6c87e914b7fe9c2f04cf756df8452cae1a` | `e4032d17dc70b5211dd23cb7019f6d6c87e914b7fe9c2f04cf756df8452cae1a` | IDENTICAL |
| 158 | `governance/FAR_GATES_RECEIPT.json` | `bc55f4bc0e0a75ca3484df80421da383e7ccad83c0e0973fccecd182a91c9662` | `bc55f4bc0e0a75ca3484df80421da383e7ccad83c0e0973fccecd182a91c9662` | IDENTICAL |
| 159 | `governance/FAR_HARDENING_AO_RECEIPT.json` | `fe7196e4566675312192585ef41a4f75e9bc31723b54811ab17d4b6dbcb62009` | `b888db0144d30ba744ae7b5cde62ae34de50a8e3b8c44c9062020b557185474f` | CRLF_ONLY |
| 160 | `governance/FAR_HARDENING_COMPILE_RECEIPT.json` | `511868d87228ea8641816f48bb4e1f54ba762ce1c309ffd665e6ab1be90d0587` | `f41c79aa7aa11ea03262ec9a2a2b3160c11d4a8d2bfba0d0a4d031ec08ce4349` | CRLF_ONLY |
| 161 | `governance/FAR_HARDENING_FITGAP_RECEIPT.json` | `ff6c80408464d7d11d03afc82f284bafdc5bf1d9506c2537d0829c160da7bedf` | `ff6c80408464d7d11d03afc82f284bafdc5bf1d9506c2537d0829c160da7bedf` | IDENTICAL |
| 162 | `governance/FAR_HARDENING_ROLLBACK_RECEIPT.json` | `28a4ae6c63b1ad4ed35f051e1f982d112b3f9a50f97f81923bcffaad1ffc655a` | `4e994c15dcffaba1ba19c4d5090e301213131e96ebae3bdf881b477579dd217e` | CRLF_ONLY |
| 163 | `governance/FAR_HARDENING_SECURITY_CLOSURE.json` | `67fed6184efbf92a934b1cbb78a418cf7d1194fa8b8940d21e13cdb9a6d19870` | `67fed6184efbf92a934b1cbb78a418cf7d1194fa8b8940d21e13cdb9a6d19870` | IDENTICAL |
| 164 | `governance/FAR_HARDENING_SUBJECT_MANIFEST.json` | `aee7b7efd2a1b65a31a4af7792c593873364265168b1a973fb5e47b4a21cd05b` | `aee7b7efd2a1b65a31a4af7792c593873364265168b1a973fb5e47b4a21cd05b` | IDENTICAL |
| 165 | `governance/FAR_INTERNAL_ALLPASS_GATE.json` | `83c0a39daffd8a47cf79e849f9c38a586b880f3235ff1d96a83d6b3b8e3fb387` | `83c0a39daffd8a47cf79e849f9c38a586b880f3235ff1d96a83d6b3b8e3fb387` | IDENTICAL |
| 166 | `governance/FAR_INTERNAL_ALLPASS_GATE_V3.json` | `efe35c8d8c4e6d08d4df49175638ba07c463229a936c08f9c7359540dc8ea4a7` | `efe35c8d8c4e6d08d4df49175638ba07c463229a936c08f9c7359540dc8ea4a7` | IDENTICAL |
| 167 | `governance/FAR_INTEROP_DISPOSITION.yaml` | `bf6a9b00e548de21dc6b897c460eb057c3c96b0105cf131e9c639504b15d948f` | `bb7699118a60f777a7a2a049bb88f6c450fb28be57c62074e3c265382eb54301` | CRLF_ONLY |
| 168 | `governance/FAR_MIRROR_READBACK_RECEIPT.json` | `1d564301ac122109d057fb6ef5d431a2dda6eb88fa43e6ca0c77a98beaa7ff87` | `1d564301ac122109d057fb6ef5d431a2dda6eb88fa43e6ca0c77a98beaa7ff87` | IDENTICAL |
| 169 | `governance/FAR_NEGATIVE_SIDE_EFFECT_RECEIPT.json` | `52fb07f3f6adc89e78caaf716622d21dceab5587fedeb8befef83272e8fdeb96` | `52fb07f3f6adc89e78caaf716622d21dceab5587fedeb8befef83272e8fdeb96` | IDENTICAL |
| 170 | `governance/FAR_PRIME_QUALIFICATION_RECORD.yaml` | `d2a9c67c147caf459b9ede9c4f64afd854c0c232f7f0c7567455c3017136663d` | `4ec7fb4e65f6f362ba064e7450cb825351b5431b52b5b71d1e53e330d754a818` | CRLF_ONLY |
| 171 | `governance/FAR_Q0_CROSSWALK.md` | `f73e276cf1264708a1e0ef1b73d07192b03948fc3c2ce8b22453448c41e8d088` | `59fb27047558733f695d8e2c0e3fa99d0a93666851e8913fb5ff8924f6d5d1b5` | CRLF_ONLY |
| 172 | `governance/FAR_Q10_AO_RECEIPT.json` | `da3174916358fdc20c8072e1adfb3062af72d44e0a4d65093b0fda4708e496eb` | `05f6deb44d72dd7cd3b89d77bacb6f054c426df9255f7ff2b16a2990b61621eb` | CRLF_ONLY |
| 173 | `governance/FAR_Q4_REAL_INVOCATION_RECEIPT.json` | `143887c82803373a67f362390920f3d6e462d5340c162898baf9ab67aaa99b00` | `143887c82803373a67f362390920f3d6e462d5340c162898baf9ab67aaa99b00` | IDENTICAL |
| 174 | `governance/FAR_R8_HISTORICAL_BASELINE.md` | `5ae16928efda36823e29a40c2fc75ca047e75918e52a033c9d8cfd4e58eb54fc` | `c754ab2179cb712df9ed07b3c70dc6d93f1ba48efc49f78b4dc36afb7ed9bdc4` | CRLF_ONLY |
| 175 | `governance/FAR_REGRESSION_CROSSWALK.json` | `46a74fd56bc551a391a661177897b84a2013e682a645435c60290dcd3fab99e7` | `46a74fd56bc551a391a661177897b84a2013e682a645435c60290dcd3fab99e7` | IDENTICAL |
| 176 | `governance/FAR_RETRIEVAL_CHALLENGE_CLOSURE.json` | `9f0f6525097b3abc00d7717aabfcd0728e842982dd09ed4afedc405703cd2681` | `cf3b42c78b2c173faaaff9fdf9e6fb08e86fdd8a869842681bd198d77040cb39` | CRLF_ONLY |
| 177 | `governance/FAR_SOURCE_SECURITY.yaml` | `c7afbff30c6caa3c7ff7c40d7915f271bfef8dca6314aabf1ba82ce5f3a2aba0` | `ddacd339695d68ea9b2e58ae537ed0fb88bd6cf353eb6efd05ed93884c79e192` | CRLF_ONLY |
| 178 | `governance/FAR_SUBJECT_ROOT_MANIFEST.json` | `00806ea1c932f498ae7b4f2f067fb93d2f67f93a170d5872cde210c30916a558` | `00806ea1c932f498ae7b4f2f067fb93d2f67f93a170d5872cde210c30916a558` | IDENTICAL |
| 179 | `governance/FAR_SWARM_Q10_RECEIPT.json` | `764b4f2945acc381d8576e329b4eef00433f39eed1d11401281e2029e560f2c8` | `8c311a8d139ba3b675c487278af57560f25b22d518754a670493b911240818e0` | CRLF_ONLY |
| 180 | `governance/FAR_TRI_SOURCE_CHALLENGE_CLOSURE.json` | `1e325082cb7726066b4055fa3933d5ce49d8b6583832ff7725885aaa53039a34` | `c98eb15ce03165581bc0ff566d04b85579ecc6af9a9d1d01314c36fadb47a742` | CRLF_ONLY |
| 181 | `governance/FAR_TRI_SOURCE_D_DECISIONS.json` | `f341e46bc24573090125809ec52a34451f453deeb2c039a06a3e0373d5f78f9c` | `f341e46bc24573090125809ec52a34451f453deeb2c039a06a3e0373d5f78f9c` | IDENTICAL |
| 182 | `governance/FAR_TRI_SOURCE_FITGAP_RECEIPT.json` | `bf25fde57ae4102ec5c724624a3fb1bc432f0e33ffd7c2174404e0f0fc25df3d` | `8a5ecf76b198f4abd45fb70c00689a73095d762cbbacf273a33b2c7079c1c567` | CRLF_ONLY |
| 183 | `methods/aris-vendor/.env.example` | `0026f405d7e8e0b855b7a17a2e6d7fef79068976b075744347a4787f474ae638` | `0026f405d7e8e0b855b7a17a2e6d7fef79068976b075744347a4787f474ae638` | IDENTICAL |
| 184 | `methods/aris-vendor/.gitattributes` | `e0670a4436402d4fefe33d13b7786d49a9e54f7e2f9703b4b30b24897b1f3b85` | `e0670a4436402d4fefe33d13b7786d49a9e54f7e2f9703b4b30b24897b1f3b85` | IDENTICAL |
| 185 | `methods/aris-vendor/.github/agents/aris-reviewer-claude.agent.md` | `cb78b6b1570d3ed3bf9e0b78a12d0b45cd201c7ca0ed0b61a22186c0d44dccc2` | `cb78b6b1570d3ed3bf9e0b78a12d0b45cd201c7ca0ed0b61a22186c0d44dccc2` | IDENTICAL |
| 186 | `methods/aris-vendor/.github/agents/aris-reviewer-openai.agent.md` | `c6d983e1e2df98e498cde979211169ac7a3640261bc61d0c64d64403df23e09c` | `c6d983e1e2df98e498cde979211169ac7a3640261bc61d0c64d64403df23e09c` | IDENTICAL |
| 187 | `methods/aris-vendor/.github/workflows/check-skills-inventory.yml` | `fba872e4a0c0c90b9ec2121d88316f156cf831d581d6fe920c2ae4d614d06026` | `fba872e4a0c0c90b9ec2121d88316f156cf831d581d6fe920c2ae4d614d06026` | IDENTICAL |
| 188 | `methods/aris-vendor/.github/workflows/lint-skills-helpers.yml` | `18bff0d74d787c3238c243ffb9893723d3cba53a4f0848f03864221e45cdbddc` | `18bff0d74d787c3238c243ffb9893723d3cba53a4f0848f03864221e45cdbddc` | IDENTICAL |
| 189 | `methods/aris-vendor/.github/workflows/test-install-aris-ps1.yml` | `3a238488d4d51a7e76a06900509c52beb18b021df526e4623e588ee16ef12b57` | `3a238488d4d51a7e76a06900509c52beb18b021df526e4623e588ee16ef12b57` | IDENTICAL |
| 190 | `methods/aris-vendor/.github/workflows/test-suite.yml` | `fea869f4525f0b5dc81fedbe11de8de0ca08d6d38fc1dd77aab65a2aa26ee175` | `fea869f4525f0b5dc81fedbe11de8de0ca08d6d38fc1dd77aab65a2aa26ee175` | IDENTICAL |
| 191 | `methods/aris-vendor/.gitignore` | `ab5043f7d74b6c09b068f16eb0e4bd028773881d7fc26a1374b7915e39efb2e0` | `ab5043f7d74b6c09b068f16eb0e4bd028773881d7fc26a1374b7915e39efb2e0` | IDENTICAL |
| 192 | `methods/aris-vendor/AGENT_GUIDE.md` | `7d585cabf4c23ccaa5214762bc95129a332ceba98a94309b51b012472b1b9add` | `7d585cabf4c23ccaa5214762bc95129a332ceba98a94309b51b012472b1b9add` | IDENTICAL |
| 193 | `methods/aris-vendor/CONTRIBUTING.md` | `f8a464d769308fed89acf11ba6e2b20552a6e9008c5669ec8522acb0fe296363` | `f8a464d769308fed89acf11ba6e2b20552a6e9008c5669ec8522acb0fe296363` | IDENTICAL |
| 194 | `methods/aris-vendor/CONTRIBUTING_CN.md` | `46f12ab3121765765167bc66fbea239fbcd30d3b31cbe884290fe6ea17871e47` | `46f12ab3121765765167bc66fbea239fbcd30d3b31cbe884290fe6ea17871e47` | IDENTICAL |
| 195 | `methods/aris-vendor/LICENSE` | `e30cf5dd5f49b4f9b656590e23d782b4756c924a9f0ff0162b3e7b5d87006bf5` | `e30cf5dd5f49b4f9b656590e23d782b4756c924a9f0ff0162b3e7b5d87006bf5` | IDENTICAL |
| 196 | `methods/aris-vendor/README.md` | `a761815e91c6971f01b392b609053944d68cf7d0f713c8c734246ed2678d1d72` | `a761815e91c6971f01b392b609053944d68cf7d0f713c8c734246ed2678d1d72` | IDENTICAL |
| 197 | `methods/aris-vendor/README_CN.md` | `71fe3206185c47ef1e618ab007329fea150908cc9d5644820565078e8b867853` | `71fe3206185c47ef1e618ab007329fea150908cc9d5644820565078e8b867853` | IDENTICAL |
| 198 | `methods/aris-vendor/SETUP_GUIDE.md` | `496581556d5fed7a9efb83bf04ecaba99e39229efafde7aee7d5f2df931e2a01` | `496581556d5fed7a9efb83bf04ecaba99e39229efafde7aee7d5f2df931e2a01` | IDENTICAL |
| 199 | `methods/aris-vendor/SETUP_GUIDE_CN.md` | `12599e2d08b48df57dd120afe92ea9d9875964ff8ec142dfd0c829c64250ea7e` | `12599e2d08b48df57dd120afe92ea9d9875964ff8ec142dfd0c829c64250ea7e` | IDENTICAL |
| 200 | `methods/aris-vendor/aris-monitor/README.md` | `1a5b4749943beefee52ec7b0b2efd43b3312ad22963925a2f31290799b78fb8a` | `1a5b4749943beefee52ec7b0b2efd43b3312ad22963925a2f31290799b78fb8a` | IDENTICAL |
| 201 | `methods/aris-vendor/aris-monitor/assets/screenshot.png` | `45f9dae192eeb42236959de084f4576ff1beb034dd48cf9d9e1206828abe12a6` | `45f9dae192eeb42236959de084f4576ff1beb034dd48cf9d9e1206828abe12a6` | IDENTICAL |
| 202 | `methods/aris-vendor/aris-monitor/focus-tty.sh` | `20b7c520744ebf9a666eb6d44f7620496f1679229492e9ac451cf2201fc9bb3b` | `20b7c520744ebf9a666eb6d44f7620496f1679229492e9ac451cf2201fc9bb3b` | IDENTICAL |
| 203 | `methods/aris-vendor/aris-monitor/focus.py` | `1c97005ed5cb8f2a83c37a13d8e282bd385d12a87bd713ea6db2f2ec25940ddb` | `1c97005ed5cb8f2a83c37a13d8e282bd385d12a87bd713ea6db2f2ec25940ddb` | IDENTICAL |
| 204 | `methods/aris-vendor/aris-monitor/run.sh` | `9d3c8646e311b1989e90142d9b7060f67b7446a9e74365ddf3674be343acd401` | `9d3c8646e311b1989e90142d9b7060f67b7446a9e74365ddf3674be343acd401` | IDENTICAL |
| 205 | `methods/aris-vendor/aris-monitor/scanner.py` | `9020cf529449a535db5f317a2ec45be4e8b5cc636a593c0f6bb61a88d317a94e` | `9020cf529449a535db5f317a2ec45be4e8b5cc636a593c0f6bb61a88d317a94e` | IDENTICAL |
| 206 | `methods/aris-vendor/aris-monitor/ticker.py` | `5128f37cb2612985694f44329091b74c885272f9cf5f4fd78ca9443c80c8bf90` | `5128f37cb2612985694f44329091b74c885272f9cf5f4fd78ca9443c80c8bf90` | IDENTICAL |
| 207 | `methods/aris-vendor/aris-monitor/widget.py` | `7badae1229c21fd93eada5a7830a0f673aeda441f953784cddfd076894fc8c8b` | `7badae1229c21fd93eada5a7830a0f673aeda441f953784cddfd076894fc8c8b` | IDENTICAL |
| 208 | `methods/aris-vendor/assets/claude-fleet-preview.png` | `fee49a687aa43a0f6eae45f7410d786e5768c0be73d54f3c770ce3f7a446550a` | `fee49a687aa43a0f6eae45f7410d786e5768c0be73d54f3c770ce3f7a446550a` | IDENTICAL |
| 209 | `methods/aris-vendor/assets/community_showcase_7_10_codex.png` | `5e03da05aee68902c088d9a1df54c618b7e6205068de85488e19011f239a4933` | `5e03da05aee68902c088d9a1df54c618b7e6205068de85488e19011f239a4933` | IDENTICAL |
| 210 | `methods/aris-vendor/assets/community_showcase_8_10.png` | `a7ede3c1de5c1799690014227ad09f91b0be4786f1ca99ecb9754925bfb68e8c` | `a7ede3c1de5c1799690014227ad09f91b0be4786f1ca99ecb9754925bfb68e8c` | IDENTICAL |
| 211 | `methods/aris-vendor/assets/feishu_interactive.jpg` | `c64b44f7135ed1914634ba5b2101dbca5ef20ace86d07f49c79852895ce48eeb` | `c64b44f7135ed1914634ba5b2101dbca5ef20ace86d07f49c79852895ce48eeb` | IDENTICAL |
| 212 | `methods/aris-vendor/assets/feishu_push.png` | `63909a8a80965186aba745522beccb0c7a11b949da34645ec3386cc664819313` | `63909a8a80965186aba745522beccb0c7a11b949da34645ec3386cc664819313` | IDENTICAL |
| 213 | `methods/aris-vendor/assets/paper_illustration_demo.png` | `8170e42e34789269dad533d6e916f218d3a7efe7a07a008ce8fe022763420747` | `8170e42e34789269dad533d6e916f218d3a7efe7a07a008ce8fe022763420747` | IDENTICAL |
| 214 | `methods/aris-vendor/community_papers/UAV-CC.pdf` | `027b384acbd7c96fd3f2eaa7d82ca918a55e29b3d2a1e0be69b4b0f38ea86a61` | `027b384acbd7c96fd3f2eaa7d82ca918a55e29b3d2a1e0be69b4b0f38ea86a61` | IDENTICAL |
| 215 | `methods/aris-vendor/docs/ALI_CODING_PLAN_GUIDE.md` | `5e7596bd16f236b962d3e774e980bb5981779dcaa398aec1a7137797014d85cb` | `5e7596bd16f236b962d3e774e980bb5981779dcaa398aec1a7137797014d85cb` | IDENTICAL |
| 216 | `methods/aris-vendor/docs/ANTIGRAVITY_ADAPTATION.md` | `1c77fd2d5715010c2bfd63fd04edd57c4c15a109b1583c203d19ff2a8a96c7f5` | `1c77fd2d5715010c2bfd63fd04edd57c4c15a109b1583c203d19ff2a8a96c7f5` | IDENTICAL |
| 217 | `methods/aris-vendor/docs/ANTIGRAVITY_ADAPTATION_CN.md` | `28363c22dab7635e494c0dd9ac1000b9f7531f1112732f5fb0be6f9414cf880c` | `28363c22dab7635e494c0dd9ac1000b9f7531f1112732f5fb0be6f9414cf880c` | IDENTICAL |
| 218 | `methods/aris-vendor/docs/ARIS-Code-README_CN.md` | `2bce9d278bf19a6bd641b72eb488674836b3580843d1a99b5a2fc62b43cea676` | `2bce9d278bf19a6bd641b72eb488674836b3580843d1a99b5a2fc62b43cea676` | IDENTICAL |
| 219 | `methods/aris-vendor/docs/ARIS-Code-README_EN.md` | `00cf684cc3f002c01e0629c930af4b9332fd4833763753d11b4bc4da999f7cd9` | `00cf684cc3f002c01e0629c930af4b9332fd4833763753d11b4bc4da999f7cd9` | IDENTICAL |
| 220 | `methods/aris-vendor/docs/ARIS_INTRO.html` | `6bc54d695e1ad2534ed232bc317533d0f7f3a547a2da529ac0779316a3830544` | `6bc54d695e1ad2534ed232bc317533d0f7f3a547a2da529ac0779316a3830544` | IDENTICAL |
| 221 | `methods/aris-vendor/docs/ARIS_INTRO.md` | `baeecff46486ac2a304f5b6996268d37ab9cff717b18fa1be9eb0088fb2d1259` | `baeecff46486ac2a304f5b6996268d37ab9cff717b18fa1be9eb0088fb2d1259` | IDENTICAL |
| 222 | `methods/aris-vendor/docs/ARIS_INTRO.review.json` | `938d79b1f68285935121fe3ea300d27ebae0840e624baab39e07ee34bf320c04` | `938d79b1f68285935121fe3ea300d27ebae0840e624baab39e07ee34bf320c04` | IDENTICAL |
| 223 | `methods/aris-vendor/docs/CODEX_CLAUDE_REVIEW_GUIDE.md` | `6982a71fecbb7e033b815875ff498be6ac1b7cb5fec847e170d63c675c5d4a5b` | `6982a71fecbb7e033b815875ff498be6ac1b7cb5fec847e170d63c675c5d4a5b` | IDENTICAL |
| 224 | `methods/aris-vendor/docs/CODEX_CLAUDE_REVIEW_GUIDE_CN.md` | `35fd8ec2e35735a210efb4fdd67ba398b094a81a7a8772265363ba256384f425` | `35fd8ec2e35735a210efb4fdd67ba398b094a81a7a8772265363ba256384f425` | IDENTICAL |
| 225 | `methods/aris-vendor/docs/CODEX_GEMINI_REVIEW_GUIDE.md` | `6cfefcb33a0ba9fff8890890ff9b3ea420f433adc781e1fc9661d97f8e1e570a` | `6cfefcb33a0ba9fff8890890ff9b3ea420f433adc781e1fc9661d97f8e1e570a` | IDENTICAL |
| 226 | `methods/aris-vendor/docs/CODEX_GEMINI_REVIEW_GUIDE_CN.md` | `2e124bc4fdc8282dabcaef0aa72d81f8413f1bffbc68dbef0165fdb46a688f17` | `2e124bc4fdc8282dabcaef0aa72d81f8413f1bffbc68dbef0165fdb46a688f17` | IDENTICAL |
| 227 | `methods/aris-vendor/docs/COPILOT_CLI_ADAPTATION.md` | `d741022d4fa920513310a41e67645832a90356514277136cb35bafb241f1ffe4` | `d741022d4fa920513310a41e67645832a90356514277136cb35bafb241f1ffe4` | IDENTICAL |
| 228 | `methods/aris-vendor/docs/CURSOR_ADAPTATION.md` | `da8bf07f7763a92889dcafe937d66736112ea0f7198da00de453816a997aa683` | `da8bf07f7763a92889dcafe937d66736112ea0f7198da00de453816a997aa683` | IDENTICAL |
| 229 | `methods/aris-vendor/docs/CUSTOMIZATION.md` | `a34f03bf226c5979beace81363542e1f9af3266f6065d9c5190eb1ba258395d6` | `a34f03bf226c5979beace81363542e1f9af3266f6065d9c5190eb1ba258395d6` | IDENTICAL |
| 230 | `methods/aris-vendor/docs/CUSTOMIZATION_CN.md` | `a526b2e5999e3e8a3dd41b0e8da0696369a9ca5edcbbe62d95ac594c2b44601c` | `a526b2e5999e3e8a3dd41b0e8da0696369a9ca5edcbbe62d95ac594c2b44601c` | IDENTICAL |
| 231 | `methods/aris-vendor/docs/GPU_SETUP.md` | `1e1bb54ca21361a71d8d6089f5968a4c84ebe142da47c8aea2746b86d0ac54f5` | `1e1bb54ca21361a71d8d6089f5968a4c84ebe142da47c8aea2746b86d0ac54f5` | IDENTICAL |
| 232 | `methods/aris-vendor/docs/GPU_SETUP_CN.md` | `89b75f7d073716e3141940a5ccea927d01f1e70e035a68560109225ad4e8364c` | `89b75f7d073716e3141940a5ccea927d01f1e70e035a68560109225ad4e8364c` | IDENTICAL |
| 233 | `methods/aris-vendor/docs/LLM_API_MIX_MATCH_GUIDE.md` | `476d849c55c7339a5fd686a1a4817727ab183e9c10d88c1f62519fd508dc2802` | `476d849c55c7339a5fd686a1a4817727ab183e9c10d88c1f62519fd508dc2802` | IDENTICAL |
| 234 | `methods/aris-vendor/docs/MANUAL_REVIEW_GUIDE.md` | `7e90194aa1383ec2600765da51cec5e302c778f76a42e0d1c0aaccd0c9749c92` | `7e90194aa1383ec2600765da51cec5e302c778f76a42e0d1c0aaccd0c9749c92` | IDENTICAL |
| 235 | `methods/aris-vendor/docs/MANUAL_REVIEW_GUIDE_CN.md` | `898d31552cea281e38e8a4d45683b42a00aeb39794588e2dd90ba49a9a1992d8` | `898d31552cea281e38e8a4d45683b42a00aeb39794588e2dd90ba49a9a1992d8` | IDENTICAL |
| 236 | `methods/aris-vendor/docs/MINIMAX_MCP_GUIDE.md` | `02496ac78351d0d43a5cd95d198e35299479b38caeee2c7a1d47ddf0cc2ed9fb` | `02496ac78351d0d43a5cd95d198e35299479b38caeee2c7a1d47ddf0cc2ed9fb` | IDENTICAL |
| 237 | `methods/aris-vendor/docs/MODELSCOPE_GUIDE.md` | `d2a76f5b392acd207b3c4545bb5995186fa8e0b1c198d57dbb9ff6cd795ea818` | `d2a76f5b392acd207b3c4545bb5995186fa8e0b1c198d57dbb9ff6cd795ea818` | IDENTICAL |
| 238 | `methods/aris-vendor/docs/MODEL_COMBINATIONS.md` | `ecfe6c888f4ef2a5819202810b252b5fe21125d367e8d2180445b36c87d73925` | `ecfe6c888f4ef2a5819202810b252b5fe21125d367e8d2180445b36c87d73925` | IDENTICAL |
| 239 | `methods/aris-vendor/docs/MODEL_COMBINATIONS_CN.md` | `6d0831b76d11b7a3cbf40b0968e6d0140c5cdc5e7cfedfad612f73df51edb5f0` | `6d0831b76d11b7a3cbf40b0968e6d0140c5cdc5e7cfedfad612f73df51edb5f0` | IDENTICAL |
| 240 | `methods/aris-vendor/docs/MiniMax-GLM-Configuration.md` | `8548e15d73b07815d6d4881dc2b0a25263f02fd3b711a617d0e82d8b7a9693bb` | `8548e15d73b07815d6d4881dc2b0a25263f02fd3b711a617d0e82d8b7a9693bb` | IDENTICAL |
| 241 | `methods/aris-vendor/docs/NARRATIVE_REPORT_EXAMPLE.md` | `e3cdd66c75d6c037eef9631da6a8f72c82089176f4fd6e03f63efb24b6e54bc1` | `e3cdd66c75d6c037eef9631da6a8f72c82089176f4fd6e03f63efb24b6e54bc1` | IDENTICAL |
| 242 | `methods/aris-vendor/docs/OPENCLAW_ADAPTATION.md` | `a9c60c6a60aabf205753b453fdbd166c5cb2e322cc5b17798373c90d3f656b8d` | `a9c60c6a60aabf205753b453fdbd166c5cb2e322cc5b17798373c90d3f656b8d` | IDENTICAL |
| 243 | `methods/aris-vendor/docs/OPENROUTER_GUIDE.md` | `d84965b9a009fb2c1ed139f9434acd7ef9118307f9dfed91e4705dcfbd100a8d` | `d84965b9a009fb2c1ed139f9434acd7ef9118307f9dfed91e4705dcfbd100a8d` | IDENTICAL |
| 244 | `methods/aris-vendor/docs/OPENROUTER_GUIDE_CN.md` | `83a43c4f4fea596313711ae678f847a836f028b19714c0cfda4ffbc81c6cbe45` | `83a43c4f4fea596313711ae678f847a836f028b19714c0cfda4ffbc81c6cbe45` | IDENTICAL |
| 245 | `methods/aris-vendor/docs/PROJECT_FILES_GUIDE.md` | `1029bc47aeca117ffd76dca93b5a082b0db4285115b633cc370c1ef1ed24c607` | `1029bc47aeca117ffd76dca93b5a082b0db4285115b633cc370c1ef1ed24c607` | IDENTICAL |
| 246 | `methods/aris-vendor/docs/PROJECT_FILES_GUIDE_CN.md` | `95350f17c1bf535f8546ac99d07757881f8fe912e20586663bd1476dabf7eec3` | `95350f17c1bf535f8546ac99d07757881f8fe912e20586663bd1476dabf7eec3` | IDENTICAL |
| 247 | `methods/aris-vendor/docs/RESUBMIT_AND_TALK.md` | `c2329e069ad52b8a3c3f19be5751dd09013673b5cedf18da6e7841de9898ad58` | `c2329e069ad52b8a3c3f19be5751dd09013673b5cedf18da6e7841de9898ad58` | IDENTICAL |
| 248 | `methods/aris-vendor/docs/RESUBMIT_AND_TALK_CN.md` | `363db52038d379de427c7d7afa6cb5ed42d17932aa7d625f480987aac3632eba` | `363db52038d379de427c7d7afa6cb5ed42d17932aa7d625f480987aac3632eba` | IDENTICAL |
| 249 | `methods/aris-vendor/docs/SESSION_RECOVERY_GUIDE.md` | `22d9346aee6c066297127b17f7c903138160c517baea48e43c37e6caa6c41d86` | `22d9346aee6c066297127b17f7c903138160c517baea48e43c37e6caa6c41d86` | IDENTICAL |
| 250 | `methods/aris-vendor/docs/SESSION_RECOVERY_GUIDE_CN.md` | `5f203ea61dab12fa4aff36ce4f97022b2c89f0cfb191113e20600192f01660f2` | `5f203ea61dab12fa4aff36ce4f97022b2c89f0cfb191113e20600192f01660f2` | IDENTICAL |
| 251 | `methods/aris-vendor/docs/SKILLS_CATALOG.md` | `77dcf928a85e033c51a22b56fe1e50196bc2d2a39f481c9176031073de1f0c40` | `77dcf928a85e033c51a22b56fe1e50196bc2d2a39f481c9176031073de1f0c40` | IDENTICAL |
| 252 | `methods/aris-vendor/docs/TRAE_ARIS_RUNBOOK_CN.md` | `dd93ab44200824027d8a165897ee97e5bfa456e9dde46581ff9304a43599403e` | `dd93ab44200824027d8a165897ee97e5bfa456e9dde46581ff9304a43599403e` | IDENTICAL |
| 253 | `methods/aris-vendor/docs/TRAE_ARIS_RUNBOOK_EN.md` | `218b505167b8a47d9ecfc3df3278eade19b20c0de4b501bf095bea092f58bbd6` | `218b505167b8a47d9ecfc3df3278eade19b20c0de4b501bf095bea092f58bbd6` | IDENTICAL |
| 254 | `methods/aris-vendor/docs/WATCHDOG_GUIDE.md` | `a374dbc93bea75f42e63d2169fe11307369a8e3527e3ed6764409044bad70b16` | `a374dbc93bea75f42e63d2169fe11307369a8e3527e3ed6764409044bad70b16` | IDENTICAL |
| 255 | `methods/aris-vendor/docs/WATCHDOG_GUIDE_CN.md` | `fe3baf6865af19c5d7d8034542b88047954424f6398fe34e0e078e0c5790030c` | `fe3baf6865af19c5d7d8034542b88047954424f6398fe34e0e078e0c5790030c` | IDENTICAL |
| 256 | `methods/aris-vendor/docs/aris-code-banner.png` | `d8b37b1f6e0413a931fc532945aa8f0deb3a560df6f60f4a399ae1ba69176e1b` | `d8b37b1f6e0413a931fc532945aa8f0deb3a560df6f60f4a399ae1ba69176e1b` | IDENTICAL |
| 257 | `methods/aris-vendor/docs/aris-code-screenshot.png` | `7d7a25cbf4337856905cad804364d7f8be206318593809f363d897b219b381be` | `7d7a25cbf4337856905cad804364d7f8be206318593809f363d897b219b381be` | IDENTICAL |
| 258 | `methods/aris-vendor/docs/aris-movie-director-method.png` | `ca1aedeeb70c1ab619c89c5dca30815c386dd08032ae91544ea9d80cf5e17487` | `ca1aedeeb70c1ab619c89c5dca30815c386dd08032ae91544ea9d80cf5e17487` | IDENTICAL |
| 259 | `methods/aris-vendor/docs/aris_intro_slides.pdf` | `37c4f73de95ed3c6a504c95c1372bff247078bb10b7eeb68b899eb71c4836148` | `37c4f73de95ed3c6a504c95c1372bff247078bb10b7eeb68b899eb71c4836148` | IDENTICAL |
| 260 | `methods/aris-vendor/docs/aris_logo.svg` | `0d0bbce1971fac0f1e0f51fefe295ece9b6034690a8e5ceb6f54adb6cf2c74e5` | `0d0bbce1971fac0f1e0f51fefe295ece9b6034690a8e5ceb6f54adb6cf2c74e5` | IDENTICAL |
| 261 | `methods/aris-vendor/docs/auto_review_score_curve.png` | `74be1f0cdb177bfd5c84d072607ee577d9d65aa73837ea5a71a2bb2ee2a649b1` | `74be1f0cdb177bfd5c84d072607ee577d9d65aa73837ea5a71a2bb2ee2a649b1` | IDENTICAL |
| 262 | `methods/aris-vendor/docs/blogs/continuous_dlm_2026h1_survey.html` | `71089a7a22d3bd1b6d73928971a240b731edd3c015c58c1f1cd278cf1487fa03` | `71089a7a22d3bd1b6d73928971a240b731edd3c015c58c1f1cd278cf1487fa03` | IDENTICAL |
| 263 | `methods/aris-vendor/docs/hero_combined.svg` | `ba8ba7dcaa551d6db2ed777b7e219d11ac508a7efb606a624aa96539de3a64c3` | `ba8ba7dcaa551d6db2ed777b7e219d11ac508a7efb606a624aa96539de3a64c3` | IDENTICAL |
| 264 | `methods/aris-vendor/docs/hero_idea.svg` | `aa7ab53cec8f7f78dd44390cc31a49ccb24ab71a5f7c95c7d7fa3eadf2948d8d` | `aa7ab53cec8f7f78dd44390cc31a49ccb24ab71a5f7c95c7d7fa3eadf2948d8d` | IDENTICAL |
| 265 | `methods/aris-vendor/docs/hero_implement.svg` | `149a7ffefe7c5a239daefc011ada0fd645c65b8a894e267dace5c8b6a0cb1381` | `149a7ffefe7c5a239daefc011ada0fd645c65b8a894e267dace5c8b6a0cb1381` | IDENTICAL |
| 266 | `methods/aris-vendor/docs/hero_interaction.svg` | `a6c4d3563a46f7302bf92a41667be64b2bb9d6d19a7525895aae50017ae437fa` | `a6c4d3563a46f7302bf92a41667be64b2bb9d6d19a7525895aae50017ae437fa` | IDENTICAL |
| 267 | `methods/aris-vendor/docs/hf_daily_paper_1.svg` | `ebc41e2d6efe59dd33d0dcbf5863dfd16c82dcc9bf4927e502a61d77aada3d01` | `ebc41e2d6efe59dd33d0dcbf5863dfd16c82dcc9bf4927e502a61d77aada3d01` | IDENTICAL |
| 268 | `methods/aris-vendor/docs/integrations/FEISHU.md` | `bfc6fc8998bdc553fb2d760ea90a03028ffa4215537fb7e0fe4e52cfc0ea669a` | `bfc6fc8998bdc553fb2d760ea90a03028ffa4215537fb7e0fe4e52cfc0ea669a` | IDENTICAL |
| 269 | `methods/aris-vendor/docs/integrations/FEISHU_CN.md` | `0c583c289879730977b89f2b42d59fb075a94b9de20463f5576b4e46c7a06aff` | `0c583c289879730977b89f2b42d59fb075a94b9de20463f5576b4e46c7a06aff` | IDENTICAL |
| 270 | `methods/aris-vendor/docs/integrations/OBSIDIAN.md` | `f2603b51b2d1a76cc372df998ba7565ec6afc55b80f50a8ad667f7df3c1edab6` | `f2603b51b2d1a76cc372df998ba7565ec6afc55b80f50a8ad667f7df3c1edab6` | IDENTICAL |
| 271 | `methods/aris-vendor/docs/integrations/OBSIDIAN_CN.md` | `4c9d776e0352108e84078db928ee78ac7fddfd78c55f8f1713ff1fa20c112bc1` | `4c9d776e0352108e84078db928ee78ac7fddfd78c55f8f1713ff1fa20c112bc1` | IDENTICAL |
| 272 | `methods/aris-vendor/docs/integrations/VAST_GPU_GUIDE.md` | `3d30582549a72cf2c5ff85a6dcac48177013c5a44dfd47194a0e4a6523625500` | `3d30582549a72cf2c5ff85a6dcac48177013c5a44dfd47194a0e4a6523625500` | IDENTICAL |
| 273 | `methods/aris-vendor/docs/integrations/VAST_GPU_GUIDE_CN.md` | `b75a35ca889caa7bc67f225bb6ef7f2ee469565c6e23af6740192124c2d20fb2` | `b75a35ca889caa7bc67f225bb6ef7f2ee469565c6e23af6740192124c2d20fb2` | IDENTICAL |
| 274 | `methods/aris-vendor/docs/integrations/ZOTERO.md` | `e9014dc6cb15e008eb2d720ac917287c07bdf695ec105c50f76a0c8203666a2d` | `e9014dc6cb15e008eb2d720ac917287c07bdf695ec105c50f76a0c8203666a2d` | IDENTICAL |
| 275 | `methods/aris-vendor/docs/integrations/ZOTERO_CN.md` | `e9e5f0df5d1dac1e7cd8e484a77b9e613603fa5cea7e757a12478b2d244837b8` | `e9e5f0df5d1dac1e7cd8e484a77b9e613603fa5cea7e757a12478b2d244837b8` | IDENTICAL |
| 276 | `methods/aris-vendor/docs/tutorials/3d_generation_tutorial.html` | `f9ab9923fec8fc06fea8e6b023545d7b5d1ad861a9a12caf34e3c4d50f5e3d2a` | `f9ab9923fec8fc06fea8e6b023545d7b5d1ad861a9a12caf34e3c4d50f5e3d2a` | IDENTICAL |
| 277 | `methods/aris-vendor/docs/tutorials/3d_generation_tutorial.md` | `beab28036da8f28744b8d64815a669d0fce44c978bd869145e41b15860659ccc` | `beab28036da8f28744b8d64815a669d0fce44c978bd869145e41b15860659ccc` | IDENTICAL |
| 278 | `methods/aris-vendor/docs/tutorials/3d_generation_tutorial.review.json` | `c79cb0fa5764e9b4257a162002d0e5941e3452d2198f63a8b510c17a6fe81959` | `c79cb0fa5764e9b4257a162002d0e5941e3452d2198f63a8b510c17a6fe81959` | IDENTICAL |
| 279 | `methods/aris-vendor/docs/tutorials/3d_generation_tutorial_en.html` | `5b4b0634c1c8f2a6ff2eb1d8b06ea05fdc1da94f8d38322099238adf207010c5` | `5b4b0634c1c8f2a6ff2eb1d8b06ea05fdc1da94f8d38322099238adf207010c5` | IDENTICAL |
| 280 | `methods/aris-vendor/docs/tutorials/3d_generation_tutorial_en.md` | `9caec9665d59cc27afa1d1593863904b12b36b74df9446dff5440621e7923272` | `9caec9665d59cc27afa1d1593863904b12b36b74df9446dff5440621e7923272` | IDENTICAL |
| 281 | `methods/aris-vendor/docs/tutorials/README.md` | `94148c359e49f505f5b061c0a684848a310f328a8cb72c948d6b0925417a616f` | `94148c359e49f505f5b061c0a684848a310f328a8cb72c948d6b0925417a616f` | IDENTICAL |
| 282 | `methods/aris-vendor/docs/tutorials/agent_foundations_tutorial.html` | `3b5dd4781a93ab6c4615c6bf3b50f191655cbc75b60532daea34f7ae925ec170` | `3b5dd4781a93ab6c4615c6bf3b50f191655cbc75b60532daea34f7ae925ec170` | IDENTICAL |
| 283 | `methods/aris-vendor/docs/tutorials/agent_foundations_tutorial.md` | `a329ddea9be664b99a53f2b46fbe530838614228ddebbe7b43450f15eb8b12ad` | `a329ddea9be664b99a53f2b46fbe530838614228ddebbe7b43450f15eb8b12ad` | IDENTICAL |
| 284 | `methods/aris-vendor/docs/tutorials/agent_foundations_tutorial.review.json` | `0b688cdfc83f18825d194bf0f3ba07e507591ef2fd81223642ede072a84600d1` | `0b688cdfc83f18825d194bf0f3ba07e507591ef2fd81223642ede072a84600d1` | IDENTICAL |
| 285 | `methods/aris-vendor/docs/tutorials/agent_foundations_tutorial_en.html` | `9e30682a7020e1ef52b2507b310fd3a7fe69b003033a885599b7b19d388608cd` | `9e30682a7020e1ef52b2507b310fd3a7fe69b003033a885599b7b19d388608cd` | IDENTICAL |
| 286 | `methods/aris-vendor/docs/tutorials/agent_foundations_tutorial_en.md` | `1b1053abea299e0de1f646724a1d612f24612034b2b2b9a32a988d1cf8da8728` | `1b1053abea299e0de1f646724a1d612f24612034b2b2b9a32a988d1cf8da8728` | IDENTICAL |
| 287 | `methods/aris-vendor/docs/tutorials/agentic_rl_tutorial.html` | `003e176e5cf6894f19cf2dac8367579fc926569512a6da5b146b00aefba0a458` | `003e176e5cf6894f19cf2dac8367579fc926569512a6da5b146b00aefba0a458` | IDENTICAL |
| 288 | `methods/aris-vendor/docs/tutorials/agentic_rl_tutorial.md` | `d3d476658bea0760566d2cc9d6eaf72ceaab67d8c81d3eeaa4442473092e8e6e` | `d3d476658bea0760566d2cc9d6eaf72ceaab67d8c81d3eeaa4442473092e8e6e` | IDENTICAL |
| 289 | `methods/aris-vendor/docs/tutorials/agentic_rl_tutorial.review.json` | `b2422f2a80514928a046c12cc40d37b314f6386741d4529bc1cb534abccf9f66` | `b2422f2a80514928a046c12cc40d37b314f6386741d4529bc1cb534abccf9f66` | IDENTICAL |
| 290 | `methods/aris-vendor/docs/tutorials/agentic_rl_tutorial_en.html` | `460aadaa11f0ab2bb995b2a964e600578524d51e04832d772f127bde07182871` | `460aadaa11f0ab2bb995b2a964e600578524d51e04832d772f127bde07182871` | IDENTICAL |
| 291 | `methods/aris-vendor/docs/tutorials/agentic_rl_tutorial_en.md` | `9dd920e9292be2a57353c0f123d48af9f77fab2a9e3c60a7606b1cfd297d6f9c` | `9dd920e9292be2a57353c0f123d48af9f77fab2a9e3c60a7606b1cfd297d6f9c` | IDENTICAL |
| 292 | `methods/aris-vendor/docs/tutorials/attention_tutorial.html` | `882db6004af7754648603c68ce9716d55f5ff95dc77536aafda30a7be47a1502` | `882db6004af7754648603c68ce9716d55f5ff95dc77536aafda30a7be47a1502` | IDENTICAL |
| 293 | `methods/aris-vendor/docs/tutorials/attention_tutorial.md` | `8d8d5146c1a9a924cd5e29973b7419d9fe14f5009c392db4b4ad6ff3a12ab1e0` | `8d8d5146c1a9a924cd5e29973b7419d9fe14f5009c392db4b4ad6ff3a12ab1e0` | IDENTICAL |
| 294 | `methods/aris-vendor/docs/tutorials/attention_tutorial.review.json` | `15e1d9ff9ce2e27688191b2991877799842f317b0e4605586ff19c40a679f728` | `15e1d9ff9ce2e27688191b2991877799842f317b0e4605586ff19c40a679f728` | IDENTICAL |
| 295 | `methods/aris-vendor/docs/tutorials/attention_tutorial_en.html` | `0f3d4f9022cf66528b853a0727cf8e3f2c4d9f1a149d829198a0273bffab5b83` | `0f3d4f9022cf66528b853a0727cf8e3f2c4d9f1a149d829198a0273bffab5b83` | IDENTICAL |
| 296 | `methods/aris-vendor/docs/tutorials/attention_tutorial_en.md` | `ecb6fe924cee8db5b2dd0daa4fb81c3866ec6b47ceadaa73ba0011378eb07e67` | `ecb6fe924cee8db5b2dd0daa4fb81c3866ec6b47ceadaa73ba0011378eb07e67` | IDENTICAL |
| 297 | `methods/aris-vendor/docs/tutorials/diffusion_distillation_tutorial.html` | `03dbb13b83f3e6dd33576f45a34eebac96b56c6cbce6702835bd20de3e68e923` | `03dbb13b83f3e6dd33576f45a34eebac96b56c6cbce6702835bd20de3e68e923` | IDENTICAL |
| 298 | `methods/aris-vendor/docs/tutorials/diffusion_distillation_tutorial.md` | `cdf8cbf0098fd69e5a36cbd5b787d6415815106fdc3159de14661b50323e5b7c` | `cdf8cbf0098fd69e5a36cbd5b787d6415815106fdc3159de14661b50323e5b7c` | IDENTICAL |
| 299 | `methods/aris-vendor/docs/tutorials/diffusion_distillation_tutorial.review.json` | `2d8365327bb9130c2e08bbf0d77409b99083340e3ff959646e322e20738d92aa` | `2d8365327bb9130c2e08bbf0d77409b99083340e3ff959646e322e20738d92aa` | IDENTICAL |
| 300 | `methods/aris-vendor/docs/tutorials/diffusion_distillation_tutorial_en.html` | `23633fc40a715486404687cddb8c80cbdddfd97724164ad1d9a72c7b14f30c23` | `23633fc40a715486404687cddb8c80cbdddfd97724164ad1d9a72c7b14f30c23` | IDENTICAL |
| 301 | `methods/aris-vendor/docs/tutorials/diffusion_distillation_tutorial_en.md` | `cceb6c61f1f5be01eacd4f25cf2ef79067c1093da76e75e4a92df0a3e3c84877` | `cceb6c61f1f5be01eacd4f25cf2ef79067c1093da76e75e4a92df0a3e3c84877` | IDENTICAL |
| 302 | `methods/aris-vendor/docs/tutorials/diffusion_foundations_tutorial.html` | `dbbe1ea3c3689c18be5f79920785d5098f3cef3b9d13448fdd709ba1683df207` | `dbbe1ea3c3689c18be5f79920785d5098f3cef3b9d13448fdd709ba1683df207` | IDENTICAL |
| 303 | `methods/aris-vendor/docs/tutorials/diffusion_foundations_tutorial.md` | `95c1efc6f929678361bb3b54ef684da7def546002107412458fd14673ebbef67` | `95c1efc6f929678361bb3b54ef684da7def546002107412458fd14673ebbef67` | IDENTICAL |
| 304 | `methods/aris-vendor/docs/tutorials/diffusion_foundations_tutorial.review.json` | `3c70f0c7bc7e4d78a48e281e09f46476a57a21ae742cdf35789b3def55ed01b1` | `3c70f0c7bc7e4d78a48e281e09f46476a57a21ae742cdf35789b3def55ed01b1` | IDENTICAL |
| 305 | `methods/aris-vendor/docs/tutorials/diffusion_foundations_tutorial_en.html` | `d5d164255ad9015250529fb4f229c14497ac6ecd867fbf3a2fe251543b2c8925` | `d5d164255ad9015250529fb4f229c14497ac6ecd867fbf3a2fe251543b2c8925` | IDENTICAL |
| 306 | `methods/aris-vendor/docs/tutorials/diffusion_foundations_tutorial_en.md` | `5f3b3e8403e8abdc6cbd6ec2c8d893bc9c2919733358f4837062708d53549727` | `5f3b3e8403e8abdc6cbd6ec2c8d893bc9c2919733358f4837062708d53549727` | IDENTICAL |
| 307 | `methods/aris-vendor/docs/tutorials/diffusion_post_training_tutorial.html` | `5ec14ee6cb6c77d58a76bdf5ec1796fff21aa64ab106483eb176f422c5ba68f9` | `5ec14ee6cb6c77d58a76bdf5ec1796fff21aa64ab106483eb176f422c5ba68f9` | IDENTICAL |
| 308 | `methods/aris-vendor/docs/tutorials/diffusion_post_training_tutorial.md` | `95b47c84420904cb38b68b156d25372d305084281e28fec71d19c405801efef8` | `95b47c84420904cb38b68b156d25372d305084281e28fec71d19c405801efef8` | IDENTICAL |
| 309 | `methods/aris-vendor/docs/tutorials/diffusion_post_training_tutorial.review.json` | `5af1efdc5779f814e5aab5a87d2ec61b1886aaa032aa4759d0762ef3847a5d86` | `5af1efdc5779f814e5aab5a87d2ec61b1886aaa032aa4759d0762ef3847a5d86` | IDENTICAL |
| 310 | `methods/aris-vendor/docs/tutorials/diffusion_post_training_tutorial_en.html` | `9d81a5dc3ac7ec3b2b44a28e963e635ae4c7cdd91f4c54c053709b190cdd864f` | `9d81a5dc3ac7ec3b2b44a28e963e635ae4c7cdd91f4c54c053709b190cdd864f` | IDENTICAL |
| 311 | `methods/aris-vendor/docs/tutorials/diffusion_post_training_tutorial_en.md` | `6143ed98abc28b9f37f4b33126bbd73399f59e75b12a5c4dcc82769593d96ceb` | `6143ed98abc28b9f37f4b33126bbd73399f59e75b12a5c4dcc82769593d96ceb` | IDENTICAL |
| 312 | `methods/aris-vendor/docs/tutorials/distributed_training_tutorial.html` | `31b169b223aab131b16a7460cf1573890a2a5796d4907f76308b69f605900b35` | `31b169b223aab131b16a7460cf1573890a2a5796d4907f76308b69f605900b35` | IDENTICAL |
| 313 | `methods/aris-vendor/docs/tutorials/distributed_training_tutorial.md` | `86087779b70e3bcaf4b22536bdf96eae5fd0d9e07675f4b9c61122ce67ee0af7` | `86087779b70e3bcaf4b22536bdf96eae5fd0d9e07675f4b9c61122ce67ee0af7` | IDENTICAL |
| 314 | `methods/aris-vendor/docs/tutorials/distributed_training_tutorial.review.json` | `1487e32d3e07b7a219268479a2a1538415882c21e29e96f328fbe0232c5c5bd9` | `1487e32d3e07b7a219268479a2a1538415882c21e29e96f328fbe0232c5c5bd9` | IDENTICAL |
| 315 | `methods/aris-vendor/docs/tutorials/distributed_training_tutorial_en.html` | `0e838f855b9ecc4a91b9afc7cd5d1b08861364bd1fbf8cf2aa5ed53a20af79fd` | `0e838f855b9ecc4a91b9afc7cd5d1b08861364bd1fbf8cf2aa5ed53a20af79fd` | IDENTICAL |
| 316 | `methods/aris-vendor/docs/tutorials/distributed_training_tutorial_en.md` | `9ee6b9a3603bcd089bca124fa44f3bdb41d7b5604595f3a506cb9ff601bcd999` | `9ee6b9a3603bcd089bca124fa44f3bdb41d7b5604595f3a506cb9ff601bcd999` | IDENTICAL |
| 317 | `methods/aris-vendor/docs/tutorials/flow_matching_tutorial.html` | `ce6c167a4c2293ab4494b8be9ee6b72c8538b28e6aafe8574f548a6c59b57b12` | `ce6c167a4c2293ab4494b8be9ee6b72c8538b28e6aafe8574f548a6c59b57b12` | IDENTICAL |
| 318 | `methods/aris-vendor/docs/tutorials/flow_matching_tutorial.md` | `ab4358901d204fec676df6ce3b8559be4e69fec3833f764bcfc937b113eea281` | `ab4358901d204fec676df6ce3b8559be4e69fec3833f764bcfc937b113eea281` | IDENTICAL |
| 319 | `methods/aris-vendor/docs/tutorials/flow_matching_tutorial.review.json` | `8416b67538df085890ca96bc10dc763b275cd1002cbe7e7d26051f3d718da6f6` | `8416b67538df085890ca96bc10dc763b275cd1002cbe7e7d26051f3d718da6f6` | IDENTICAL |
| 320 | `methods/aris-vendor/docs/tutorials/flow_matching_tutorial_en.html` | `8571bd00292e41f87b5a1575b218faabb344f46278e142553222a84fc5e2685f` | `8571bd00292e41f87b5a1575b218faabb344f46278e142553222a84fc5e2685f` | IDENTICAL |
| 321 | `methods/aris-vendor/docs/tutorials/flow_matching_tutorial_en.md` | `90243d531e3f172dc24c2345e6ada197471f80f92dd45892bc0d002afa86c3f0` | `90243d531e3f172dc24c2345e6ada197471f80f92dd45892bc0d002afa86c3f0` | IDENTICAL |
| 322 | `methods/aris-vendor/docs/tutorials/image_generation_systems_tutorial.html` | `70fd8b1b37ee3ff18cb1b3ffcf83a30a966ac6aa728b848cb79ec2c582c1f90f` | `70fd8b1b37ee3ff18cb1b3ffcf83a30a966ac6aa728b848cb79ec2c582c1f90f` | IDENTICAL |
| 323 | `methods/aris-vendor/docs/tutorials/image_generation_systems_tutorial.md` | `76785ba96660960ae6f5caf7e252e7da39ef38867ad61c2750d98f248e53d625` | `76785ba96660960ae6f5caf7e252e7da39ef38867ad61c2750d98f248e53d625` | IDENTICAL |
| 324 | `methods/aris-vendor/docs/tutorials/image_generation_systems_tutorial.review.json` | `8eb2e92e4926fe9afeaa1b7d31b1841868facf3305f4b2c49ed3354a7330d4a1` | `8eb2e92e4926fe9afeaa1b7d31b1841868facf3305f4b2c49ed3354a7330d4a1` | IDENTICAL |
| 325 | `methods/aris-vendor/docs/tutorials/image_generation_systems_tutorial_en.html` | `42a4f8d8a84f8b2c50a4ef6f2adc91d030c0951b1556bfac6066b44a19aefb2b` | `42a4f8d8a84f8b2c50a4ef6f2adc91d030c0951b1556bfac6066b44a19aefb2b` | IDENTICAL |
| 326 | `methods/aris-vendor/docs/tutorials/image_generation_systems_tutorial_en.md` | `ef1c753cbe28e852ebfe465a39ec257bc3cadab4915b843627143ce1a7056b13` | `ef1c753cbe28e852ebfe465a39ec257bc3cadab4915b843627143ce1a7056b13` | IDENTICAL |
| 327 | `methods/aris-vendor/docs/tutorials/kl_divergence_rlhf_tutorial.html` | `52eccb3009fd814191190ecb8a58a76de0f4cfde6fd901565d34173c8ed62b12` | `52eccb3009fd814191190ecb8a58a76de0f4cfde6fd901565d34173c8ed62b12` | IDENTICAL |
| 328 | `methods/aris-vendor/docs/tutorials/kl_divergence_rlhf_tutorial.md` | `f0b8b5e62023c40790eecc3c8e2e1afdf9fceea26ffa5b9859d0d4382cb7ea4a` | `f0b8b5e62023c40790eecc3c8e2e1afdf9fceea26ffa5b9859d0d4382cb7ea4a` | IDENTICAL |
| 329 | `methods/aris-vendor/docs/tutorials/kl_divergence_rlhf_tutorial.review.json` | `d51af08a161ab37394510ff45aa27f213639afd158320780db8da3fecaa27b9e` | `d51af08a161ab37394510ff45aa27f213639afd158320780db8da3fecaa27b9e` | IDENTICAL |
| 330 | `methods/aris-vendor/docs/tutorials/kl_divergence_rlhf_tutorial_en.html` | `af3b4dc44f4e276defc9bca03183ed0b7cf39d956346ec638ee7a214e8d1783c` | `af3b4dc44f4e276defc9bca03183ed0b7cf39d956346ec638ee7a214e8d1783c` | IDENTICAL |
| 331 | `methods/aris-vendor/docs/tutorials/kl_divergence_rlhf_tutorial_en.md` | `4477782e0f503450db748cc46a12ddd9361df1fbcdcf2f996d8fee58f4761b73` | `4477782e0f503450db748cc46a12ddd9361df1fbcdcf2f996d8fee58f4761b73` | IDENTICAL |
| 332 | `methods/aris-vendor/docs/tutorials/kv_cache_speculative_decoding_tutorial.html` | `aba97c1687f65b3c1e566163fe762ba9df9050027622e6219fed646bc2599b59` | `aba97c1687f65b3c1e566163fe762ba9df9050027622e6219fed646bc2599b59` | IDENTICAL |
| 333 | `methods/aris-vendor/docs/tutorials/kv_cache_speculative_decoding_tutorial.md` | `688b47c5bdc93b69a749ced6c2c6139c00a0f1b08b091aea38463c16e5ab94db` | `688b47c5bdc93b69a749ced6c2c6139c00a0f1b08b091aea38463c16e5ab94db` | IDENTICAL |
| 334 | `methods/aris-vendor/docs/tutorials/kv_cache_speculative_decoding_tutorial.review.json` | `5ab2db5412c0012803dcfa274e51e42347dcd405805f7ad447d48b8b7cc7091a` | `5ab2db5412c0012803dcfa274e51e42347dcd405805f7ad447d48b8b7cc7091a` | IDENTICAL |
| 335 | `methods/aris-vendor/docs/tutorials/kv_cache_speculative_decoding_tutorial_en.html` | `e79ce3565ffc954d88e70efa0167ef2356cb615cbb53edc0f1cd09fe1876b2c9` | `e79ce3565ffc954d88e70efa0167ef2356cb615cbb53edc0f1cd09fe1876b2c9` | IDENTICAL |
| 336 | `methods/aris-vendor/docs/tutorials/kv_cache_speculative_decoding_tutorial_en.md` | `3357e2dd8dc0b865cf18f49e60842241679e7af6c296d7d80820b6f6c1ebc292` | `3357e2dd8dc0b865cf18f49e60842241679e7af6c296d7d80820b6f6c1ebc292` | IDENTICAL |
| 337 | `methods/aris-vendor/docs/tutorials/llm_opd_tutorial.html` | `b0cb0c23cc11d6f18bde1d01ef80a28bdcd5c2172db229533b2c3fc1a5cb8c4d` | `b0cb0c23cc11d6f18bde1d01ef80a28bdcd5c2172db229533b2c3fc1a5cb8c4d` | IDENTICAL |
| 338 | `methods/aris-vendor/docs/tutorials/llm_opd_tutorial.md` | `621b0792bede0b06654b0341b652bb5055eeac2b24c258e58c2f63ace770bed7` | `621b0792bede0b06654b0341b652bb5055eeac2b24c258e58c2f63ace770bed7` | IDENTICAL |
| 339 | `methods/aris-vendor/docs/tutorials/llm_opd_tutorial.review.json` | `5b293c23c7498bb736eb5b16f518c5b5f51f86b0bf6a96fde9387d9d32f56c10` | `5b293c23c7498bb736eb5b16f518c5b5f51f86b0bf6a96fde9387d9d32f56c10` | IDENTICAL |
| 340 | `methods/aris-vendor/docs/tutorials/llm_opd_tutorial_en.html` | `102565ab7d857c4fcf0fdf5916f023b205becc0f579485582d898925a357a546` | `102565ab7d857c4fcf0fdf5916f023b205becc0f579485582d898925a357a546` | IDENTICAL |
| 341 | `methods/aris-vendor/docs/tutorials/llm_opd_tutorial_en.md` | `70c85782439f0b5a5c6c9b6dff2637a7911ad95b525b9969d90ba883502953d8` | `70c85782439f0b5a5c6c9b6dff2637a7911ad95b525b9969d90ba883502953d8` | IDENTICAL |
| 342 | `methods/aris-vendor/docs/tutorials/long_context_rope_yarn_mla_tutorial.html` | `75dd3ea273ea091bfc5cbd96f6566f27388e89cdc51e74973dff60fcf7cae32c` | `75dd3ea273ea091bfc5cbd96f6566f27388e89cdc51e74973dff60fcf7cae32c` | IDENTICAL |
| 343 | `methods/aris-vendor/docs/tutorials/long_context_rope_yarn_mla_tutorial.md` | `cf9958df2aff90f900727a9cd8fa0b82b5b5cb28354087aa59f52b9b62e6c24d` | `cf9958df2aff90f900727a9cd8fa0b82b5b5cb28354087aa59f52b9b62e6c24d` | IDENTICAL |
| 344 | `methods/aris-vendor/docs/tutorials/long_context_rope_yarn_mla_tutorial.review.json` | `3bfa2d82494168a73aea55ae964d127c617bc205d96e3a28d4fe9e68716f576e` | `3bfa2d82494168a73aea55ae964d127c617bc205d96e3a28d4fe9e68716f576e` | IDENTICAL |
| 345 | `methods/aris-vendor/docs/tutorials/long_context_rope_yarn_mla_tutorial_en.html` | `3ab2b4541f9654376cf00250aec10971b1f2fd461f35e02df1e149cf12d18d69` | `3ab2b4541f9654376cf00250aec10971b1f2fd461f35e02df1e149cf12d18d69` | IDENTICAL |
| 346 | `methods/aris-vendor/docs/tutorials/long_context_rope_yarn_mla_tutorial_en.md` | `d8ebcc89a3ac6a7b354d7603a4d0f5f495fe5b539c64ca49e48ae38c72c84075` | `d8ebcc89a3ac6a7b354d7603a4d0f5f495fe5b539c64ca49e48ae38c72c84075` | IDENTICAL |
| 347 | `methods/aris-vendor/docs/tutorials/moe_tutorial.html` | `213309f37d002e0310f6010bf34aa5d1f02e68a8f315799f7d843e35c72df931` | `213309f37d002e0310f6010bf34aa5d1f02e68a8f315799f7d843e35c72df931` | IDENTICAL |
| 348 | `methods/aris-vendor/docs/tutorials/moe_tutorial.md` | `e860589270ed447981c868a7e0f0ba51ac8917a8908580825403af8205baf3b1` | `e860589270ed447981c868a7e0f0ba51ac8917a8908580825403af8205baf3b1` | IDENTICAL |
| 349 | `methods/aris-vendor/docs/tutorials/moe_tutorial.review.json` | `86023d282e4b7f53ec9d963ca02f2b4bc60187b41e5d58de168c0f7d1251462d` | `86023d282e4b7f53ec9d963ca02f2b4bc60187b41e5d58de168c0f7d1251462d` | IDENTICAL |
| 350 | `methods/aris-vendor/docs/tutorials/moe_tutorial_en.html` | `68d1fd68aa924affc77821fe148ce6621510e62f6e4f116d5ad6b3fc7b0b4017` | `68d1fd68aa924affc77821fe148ce6621510e62f6e4f116d5ad6b3fc7b0b4017` | IDENTICAL |
| 351 | `methods/aris-vendor/docs/tutorials/moe_tutorial_en.md` | `c0214eed718070285a8feb2b8e346bced55b9baf4f51f408da869d5ef6b9a65f` | `c0214eed718070285a8feb2b8e346bced55b9baf4f51f408da869d5ef6b9a65f` | IDENTICAL |
| 352 | `methods/aris-vendor/docs/tutorials/multi_agent_long_horizon_tutorial.html` | `a97adbc354b67249320a839e66e74888ad97aa404073dd846003989d6d151078` | `a97adbc354b67249320a839e66e74888ad97aa404073dd846003989d6d151078` | IDENTICAL |
| 353 | `methods/aris-vendor/docs/tutorials/multi_agent_long_horizon_tutorial.md` | `b0be93d29409b81e5bf5e3e896e8ee3b9ae84d0c1a17e72e5ca46476f1d5c065` | `b0be93d29409b81e5bf5e3e896e8ee3b9ae84d0c1a17e72e5ca46476f1d5c065` | IDENTICAL |
| 354 | `methods/aris-vendor/docs/tutorials/multi_agent_long_horizon_tutorial.review.json` | `0e21e83ed00dc683641f651c309abf2d0d20bda296bacb115fb733a5bf1bcf6f` | `0e21e83ed00dc683641f651c309abf2d0d20bda296bacb115fb733a5bf1bcf6f` | IDENTICAL |
| 355 | `methods/aris-vendor/docs/tutorials/multi_agent_long_horizon_tutorial_en.html` | `8ea49f009ca3bcb243f8f34bc5ddafa03f7db938136c343c4e4e65b3e72b41f0` | `8ea49f009ca3bcb243f8f34bc5ddafa03f7db938136c343c4e4e65b3e72b41f0` | IDENTICAL |
| 356 | `methods/aris-vendor/docs/tutorials/multi_agent_long_horizon_tutorial_en.md` | `8ac31a10efb058f7fd711607186b1277254cb908ceb627bd733c50e049d9b289` | `8ac31a10efb058f7fd711607186b1277254cb908ceb627bd733c50e049d9b289` | IDENTICAL |
| 357 | `methods/aris-vendor/docs/tutorials/quantization_tutorial.html` | `909c88556910b8b424fea43ee36472b91bf4574b5e31082432e8476b1aedf80a` | `909c88556910b8b424fea43ee36472b91bf4574b5e31082432e8476b1aedf80a` | IDENTICAL |
| 358 | `methods/aris-vendor/docs/tutorials/quantization_tutorial.md` | `f04948e0f203c2972cb16b925ae326b7e46f34e691c037df51dbabe54f88a301` | `f04948e0f203c2972cb16b925ae326b7e46f34e691c037df51dbabe54f88a301` | IDENTICAL |
| 359 | `methods/aris-vendor/docs/tutorials/quantization_tutorial.review.json` | `c88b0cfbdb752f44568812675bd150e2b832ee19fb7dcc10e34f1ba346bf6380` | `c88b0cfbdb752f44568812675bd150e2b832ee19fb7dcc10e34f1ba346bf6380` | IDENTICAL |
| 360 | `methods/aris-vendor/docs/tutorials/quantization_tutorial_en.html` | `3f3f30b79d31889fbf824687629a266bd59da179aa497d2fdf447d7333141d8c` | `3f3f30b79d31889fbf824687629a266bd59da179aa497d2fdf447d7333141d8c` | IDENTICAL |
| 361 | `methods/aris-vendor/docs/tutorials/quantization_tutorial_en.md` | `a4b453729283fdc4cc0fdb167b8620e68d87510a092dd1861915ed5965818231` | `a4b453729283fdc4cc0fdb167b8620e68d87510a092dd1861915ed5965818231` | IDENTICAL |
| 362 | `methods/aris-vendor/docs/tutorials/reasoning_models_tutorial.html` | `a3e87d170eb8f7a0ce173e03209f5178c2d38a06d2ff8f0812cf8e7eeda93316` | `a3e87d170eb8f7a0ce173e03209f5178c2d38a06d2ff8f0812cf8e7eeda93316` | IDENTICAL |
| 363 | `methods/aris-vendor/docs/tutorials/reasoning_models_tutorial.md` | `549e2f7e241c94ec0b8f2203727ae759afe568daa1c62d507051768725890e63` | `549e2f7e241c94ec0b8f2203727ae759afe568daa1c62d507051768725890e63` | IDENTICAL |
| 364 | `methods/aris-vendor/docs/tutorials/reasoning_models_tutorial.review.json` | `ec7638c9b5696c19d2a97d6bfae0d6e7c0cacfbb50112b53b528dc7b050e08c1` | `ec7638c9b5696c19d2a97d6bfae0d6e7c0cacfbb50112b53b528dc7b050e08c1` | IDENTICAL |
| 365 | `methods/aris-vendor/docs/tutorials/reasoning_models_tutorial_en.html` | `23da1baecd2e11808dba41a70160fdc8f9e092fb1236cb7a04cbfee90032ee01` | `23da1baecd2e11808dba41a70160fdc8f9e092fb1236cb7a04cbfee90032ee01` | IDENTICAL |
| 366 | `methods/aris-vendor/docs/tutorials/reasoning_models_tutorial_en.md` | `0aefca37b314b59a1cc8e7548f79d120508f4fc5d1fc5b34f33210f9f9e6213e` | `0aefca37b314b59a1cc8e7548f79d120508f4fc5d1fc5b34f33210f9f9e6213e` | IDENTICAL |
| 367 | `methods/aris-vendor/docs/tutorials/rlhf_dpo_grpo_ppo_tutorial.html` | `ea7c8e251c3fa93a9d45cf32b33c14055f5941930908913fda65009ffa65500c` | `ea7c8e251c3fa93a9d45cf32b33c14055f5941930908913fda65009ffa65500c` | IDENTICAL |
| 368 | `methods/aris-vendor/docs/tutorials/rlhf_dpo_grpo_ppo_tutorial.md` | `67ea410d68e2504164d7d17556f41bf5c4535ebf520c2790b433851a034a78ad` | `67ea410d68e2504164d7d17556f41bf5c4535ebf520c2790b433851a034a78ad` | IDENTICAL |
| 369 | `methods/aris-vendor/docs/tutorials/rlhf_dpo_grpo_ppo_tutorial.review.json` | `66f9961a456933b27732d1465577bb829723f549b97dca08a3aa8848dd110a8b` | `66f9961a456933b27732d1465577bb829723f549b97dca08a3aa8848dd110a8b` | IDENTICAL |
| 370 | `methods/aris-vendor/docs/tutorials/rlhf_dpo_grpo_ppo_tutorial_en.html` | `52b4256e3f56286111bf6ef6d0d1627770f1f7345a4047e24368139f81af20b9` | `52b4256e3f56286111bf6ef6d0d1627770f1f7345a4047e24368139f81af20b9` | IDENTICAL |
| 371 | `methods/aris-vendor/docs/tutorials/rlhf_dpo_grpo_ppo_tutorial_en.md` | `0740c1296ea5c2902e4cab332899d30786c1f175d2420b5a53c4587fb7ec65c0` | `0740c1296ea5c2902e4cab332899d30786c1f175d2420b5a53c4587fb7ec65c0` | IDENTICAL |
| 372 | `methods/aris-vendor/docs/tutorials/self_evolving_agents_tutorial.html` | `4b182c44ea33759e51c01ab4413ff056b1275622122924e8f37767511fec3ce1` | `4b182c44ea33759e51c01ab4413ff056b1275622122924e8f37767511fec3ce1` | IDENTICAL |
| 373 | `methods/aris-vendor/docs/tutorials/self_evolving_agents_tutorial.md` | `b863a1d3abfdb3512a3e5907947e3bb9281a00ddf4546199218fb469c965296e` | `b863a1d3abfdb3512a3e5907947e3bb9281a00ddf4546199218fb469c965296e` | IDENTICAL |
| 374 | `methods/aris-vendor/docs/tutorials/self_evolving_agents_tutorial.review.json` | `9b59e3c131882f60bb39b71006a8455d38810b48071869e38da89709f4d2eb1c` | `9b59e3c131882f60bb39b71006a8455d38810b48071869e38da89709f4d2eb1c` | IDENTICAL |
| 375 | `methods/aris-vendor/docs/tutorials/self_evolving_agents_tutorial_en.html` | `6666dfef7c92461ef597d813a4401e4b62456681363323c34825d4b73e9801b7` | `6666dfef7c92461ef597d813a4401e4b62456681363323c34825d4b73e9801b7` | IDENTICAL |
| 376 | `methods/aris-vendor/docs/tutorials/self_evolving_agents_tutorial_en.md` | `65f5baf62206b2506086becf7b79fc11d4a8dc9ff113bb5f2ae933595131abb5` | `65f5baf62206b2506086becf7b79fc11d4a8dc9ff113bb5f2ae933595131abb5` | IDENTICAL |
| 377 | `methods/aris-vendor/docs/tutorials/vae_vqvae_vqgan_tutorial.html` | `06bed704a1f29f85adb63a50ba2170041d0b1d64716592cd6b3d26627bfb5bd7` | `06bed704a1f29f85adb63a50ba2170041d0b1d64716592cd6b3d26627bfb5bd7` | IDENTICAL |
| 378 | `methods/aris-vendor/docs/tutorials/vae_vqvae_vqgan_tutorial.md` | `826ba28b7bb7ff38ca137ceebd48b0f4395a58dfb4081bb9f874234f2a61899c` | `826ba28b7bb7ff38ca137ceebd48b0f4395a58dfb4081bb9f874234f2a61899c` | IDENTICAL |
| 379 | `methods/aris-vendor/docs/tutorials/vae_vqvae_vqgan_tutorial.review.json` | `a36433c93f166b138e3b3619cfa61282b7b17b08e5711e87a648903c0b38db0d` | `a36433c93f166b138e3b3619cfa61282b7b17b08e5711e87a648903c0b38db0d` | IDENTICAL |
| 380 | `methods/aris-vendor/docs/tutorials/vae_vqvae_vqgan_tutorial_en.html` | `7b5ccedb07c97913356dcb1123ba4468768a9a86b95b2767042c2c6c3895e716` | `7b5ccedb07c97913356dcb1123ba4468768a9a86b95b2767042c2c6c3895e716` | IDENTICAL |
| 381 | `methods/aris-vendor/docs/tutorials/vae_vqvae_vqgan_tutorial_en.md` | `e6f6353f05d0ca8087a60c811e411690589bfc2fb7bb61ab2388feaa93fb835b` | `e6f6353f05d0ca8087a60c811e411690589bfc2fb7bb61ab2388feaa93fb835b` | IDENTICAL |
| 382 | `methods/aris-vendor/docs/tutorials/video_generation_tutorial.html` | `0ed3813a15698129fc10855efce85e05b9f4e47a3d9c8a4c8c17332b1d2c60c7` | `0ed3813a15698129fc10855efce85e05b9f4e47a3d9c8a4c8c17332b1d2c60c7` | IDENTICAL |
| 383 | `methods/aris-vendor/docs/tutorials/video_generation_tutorial.md` | `4aaa64ff3f54473df8980186427f4215f75c5d6dbe3e8196316ef72b9a7c4643` | `4aaa64ff3f54473df8980186427f4215f75c5d6dbe3e8196316ef72b9a7c4643` | IDENTICAL |
| 384 | `methods/aris-vendor/docs/tutorials/video_generation_tutorial.review.json` | `de25510899b68b448e80921c5751d96ba47a6e4ebc8c2303fdba1d819e003a93` | `de25510899b68b448e80921c5751d96ba47a6e4ebc8c2303fdba1d819e003a93` | IDENTICAL |
| 385 | `methods/aris-vendor/docs/tutorials/video_generation_tutorial_en.html` | `2041f976b9a4809621ff005a959bda08d45fa71e4628190ecc0c3ce003710a7b` | `2041f976b9a4809621ff005a959bda08d45fa71e4628190ecc0c3ce003710a7b` | IDENTICAL |
| 386 | `methods/aris-vendor/docs/tutorials/video_generation_tutorial_en.md` | `4fa0ce035daf77d9b135b7c0d4e328c1f5977598cc414e89c98dcf067ed9f3a0` | `4fa0ce035daf77d9b135b7c0d4e328c1f5977598cc414e89c98dcf067ed9f3a0` | IDENTICAL |
| 387 | `methods/aris-vendor/docs/tutorials/vlm_multimodal_tutorial.html` | `e0b4ef0203bbb15351cd59007ebc9af69949a3082be46420614bb713fa413da5` | `e0b4ef0203bbb15351cd59007ebc9af69949a3082be46420614bb713fa413da5` | IDENTICAL |
| 388 | `methods/aris-vendor/docs/tutorials/vlm_multimodal_tutorial.md` | `f9cc9510bdd535499bcf756290f8ccf31a6785c97df3fa1dabb9e9c1bf74541f` | `f9cc9510bdd535499bcf756290f8ccf31a6785c97df3fa1dabb9e9c1bf74541f` | IDENTICAL |
| 389 | `methods/aris-vendor/docs/tutorials/vlm_multimodal_tutorial.review.json` | `0ff93eeed034c9fb235b32af203b1d3c332f5960028f13723df91270b80588da` | `0ff93eeed034c9fb235b32af203b1d3c332f5960028f13723df91270b80588da` | IDENTICAL |
| 390 | `methods/aris-vendor/docs/tutorials/vlm_multimodal_tutorial_en.html` | `de94a06112489d4183306239dd56dcaf396f9254cd4f05ac6be09d479d395ac8` | `de94a06112489d4183306239dd56dcaf396f9254cd4f05ac6be09d479d395ac8` | IDENTICAL |
| 391 | `methods/aris-vendor/docs/tutorials/vlm_multimodal_tutorial_en.md` | `de321e4d3dec5699eff7277bb4b2558d3a0c6dd7c5bc5186a9f166ef71be609a` | `de321e4d3dec5699eff7277bb4b2558d3a0c6dd7c5bc5186a9f166ef71be609a` | IDENTICAL |
| 392 | `methods/aris-vendor/docs/wechat_group.jpg` | `52a82193cb1b6c813bece997f8112e7ccb6f3f06dd03be92e9e2156e7f704694` | `52a82193cb1b6c813bece997f8112e7ccb6f3f06dd03be92e9e2156e7f704694` | IDENTICAL |
| 393 | `methods/aris-vendor/mcp-servers/claude-review/README.md` | `bdb31fdc13d75dc78a3f4e7e85b93d3551afebbf0f8dee0db048a0d58ea8c31c` | `bdb31fdc13d75dc78a3f4e7e85b93d3551afebbf0f8dee0db048a0d58ea8c31c` | IDENTICAL |
| 394 | `methods/aris-vendor/mcp-servers/claude-review/run_with_claude_aws.sh` | `cbf321427afdcfa29f8d864b576494858ff3cdcfd444dd1a9a17d4ed83ab6ddc` | `cbf321427afdcfa29f8d864b576494858ff3cdcfd444dd1a9a17d4ed83ab6ddc` | IDENTICAL |
| 395 | `methods/aris-vendor/mcp-servers/claude-review/server.py` | `f5e13a5f13e360381108549a10a56b72a4f9732f0cfe5c1a09f089b5a800e76a` | `f5e13a5f13e360381108549a10a56b72a4f9732f0cfe5c1a09f089b5a800e76a` | IDENTICAL |
| 396 | `methods/aris-vendor/mcp-servers/codex-image2/README.md` | `b86a3ae4e1a12fc1fa02669b35142edfaf952d1016457087aa3c2ea7e7759fea` | `b86a3ae4e1a12fc1fa02669b35142edfaf952d1016457087aa3c2ea7e7759fea` | IDENTICAL |
| 397 | `methods/aris-vendor/mcp-servers/codex-image2/server.py` | `c697f730950cfb50d48dbc523f0109f0f941a57a2e2106dc6641a4a58364867b` | `c697f730950cfb50d48dbc523f0109f0f941a57a2e2106dc6641a4a58364867b` | IDENTICAL |
| 398 | `methods/aris-vendor/mcp-servers/feishu-bridge/requirements.txt` | `2a2c17c400824a8bad12b99d25b382aa33e7f0b330c5c6a5161b88f59dbf36e4` | `2a2c17c400824a8bad12b99d25b382aa33e7f0b330c5c6a5161b88f59dbf36e4` | IDENTICAL |
| 399 | `methods/aris-vendor/mcp-servers/feishu-bridge/server.py` | `74b25c27efc6c5b8c418e8768e6e846ae92ad477541185e4741d86b7e94fd10b` | `74b25c27efc6c5b8c418e8768e6e846ae92ad477541185e4741d86b7e94fd10b` | IDENTICAL |
| 400 | `methods/aris-vendor/mcp-servers/gemini-review/README.md` | `7b3f0e7b8e60177b8aecb463b36fbbf593a810ba2c5c8b264a14e2bb1f4e9466` | `7b3f0e7b8e60177b8aecb463b36fbbf593a810ba2c5c8b264a14e2bb1f4e9466` | IDENTICAL |
| 401 | `methods/aris-vendor/mcp-servers/gemini-review/server.py` | `9666c7b28971c85f88a35169a67e6c727d61e2a0a52871ce801695a1af12dda2` | `9666c7b28971c85f88a35169a67e6c727d61e2a0a52871ce801695a1af12dda2` | IDENTICAL |
| 402 | `methods/aris-vendor/mcp-servers/llm-chat/requirements.txt` | `1c9327746b9637a24f178ee83c5825c5a1ff49aec60d30aec5c75fd71592af3a` | `1c9327746b9637a24f178ee83c5825c5a1ff49aec60d30aec5c75fd71592af3a` | IDENTICAL |
| 403 | `methods/aris-vendor/mcp-servers/llm-chat/server.py` | `a01c75d774089fbe2a889979c7210e633c787c4e9e40a30ce2d7552eb9be7180` | `a01c75d774089fbe2a889979c7210e633c787c4e9e40a30ce2d7552eb9be7180` | IDENTICAL |
| 404 | `methods/aris-vendor/mcp-servers/manual-review/README.md` | `1bbfae96e20ec13b1594e1a17c934c197241978069cbac84c1bfdfc0d7d3aa80` | `1bbfae96e20ec13b1594e1a17c934c197241978069cbac84c1bfdfc0d7d3aa80` | IDENTICAL |
| 405 | `methods/aris-vendor/mcp-servers/manual-review/server.py` | `51072ee853dc73748895dabf9ad77a7b5de29a79758fae502b819720cbe8cbf1` | `51072ee853dc73748895dabf9ad77a7b5de29a79758fae502b819720cbe8cbf1` | IDENTICAL |
| 406 | `methods/aris-vendor/mcp-servers/manual-review/ui.html` | `4c1c0dd2052cd29c1e972a541fcef20b3e1fa9b5c941c007bca17698ef14dd52` | `4c1c0dd2052cd29c1e972a541fcef20b3e1fa9b5c941c007bca17698ef14dd52` | IDENTICAL |
| 407 | `methods/aris-vendor/mcp-servers/minimax-chat/requirements.txt` | `1c9327746b9637a24f178ee83c5825c5a1ff49aec60d30aec5c75fd71592af3a` | `1c9327746b9637a24f178ee83c5825c5a1ff49aec60d30aec5c75fd71592af3a` | IDENTICAL |
| 408 | `methods/aris-vendor/mcp-servers/minimax-chat/server.py` | `506aa8a6f0bae7d07e6fec015952ea65232388e4b9e745f7d46885e9726d1c3f` | `506aa8a6f0bae7d07e6fec015952ea65232388e4b9e745f7d46885e9726d1c3f` | IDENTICAL |
| 409 | `methods/aris-vendor/skills/ablation-planner/SKILL.md` | `d1bd7d4ac61efac5a82273e8d8d1cdfab119760c3534bc18ad14e70852f51baa` | `d1bd7d4ac61efac5a82273e8d8d1cdfab119760c3534bc18ad14e70852f51baa` | IDENTICAL |
| 410 | `methods/aris-vendor/skills/alphaxiv/SKILL.md` | `2123b9fa5b70e5ed479389a50f6ab8acb0c956495d82dc03a89899b7b730b8f3` | `2123b9fa5b70e5ed479389a50f6ab8acb0c956495d82dc03a89899b7b730b8f3` | IDENTICAL |
| 411 | `methods/aris-vendor/skills/analyze-results/SKILL.md` | `2b97b8ae1a279ac8a7db14e7d7bea67934c88352d55c95e20fcfb681a8640930` | `2b97b8ae1a279ac8a7db14e7d7bea67934c88352d55c95e20fcfb681a8640930` | IDENTICAL |
| 412 | `methods/aris-vendor/skills/arxiv/SKILL.md` | `474be36fb19d0dd99ddc8c6fa2d684836a45dca9d02051d98b5c79ac979307ed` | `474be36fb19d0dd99ddc8c6fa2d684836a45dca9d02051d98b5c79ac979307ed` | IDENTICAL |
| 413 | `methods/aris-vendor/skills/auto-paper-improvement-loop/SKILL.md` | `2aba928102f0bc0b8cb2ec02e4837f726e08d8590df0b1341de137646740849a` | `2aba928102f0bc0b8cb2ec02e4837f726e08d8590df0b1341de137646740849a` | IDENTICAL |
| 414 | `methods/aris-vendor/skills/auto-review-loop-llm/SKILL.md` | `f46c40b1a3edcc63b07cf263253fc01e706d2335bd851d672d66099b29774cf8` | `f46c40b1a3edcc63b07cf263253fc01e706d2335bd851d672d66099b29774cf8` | IDENTICAL |
| 415 | `methods/aris-vendor/skills/auto-review-loop-minimax/SKILL.md` | `70f4952522747030f4ee8011c0e29c7670a289bd0bff73fffbcb9bac232a4102` | `70f4952522747030f4ee8011c0e29c7670a289bd0bff73fffbcb9bac232a4102` | IDENTICAL |
| 416 | `methods/aris-vendor/skills/auto-review-loop/SKILL.md` | `782803dab87f636db235133a2fb1513400ca9bdce012305ec033a633a371538b` | `782803dab87f636db235133a2fb1513400ca9bdce012305ec033a633a371538b` | IDENTICAL |
| 417 | `methods/aris-vendor/skills/citation-audit/SKILL.md` | `c3e131c5747dc9c95eeceea3e7746c7fbb3eb5a312d02de61bb2e9cd61197395` | `c3e131c5747dc9c95eeceea3e7746c7fbb3eb5a312d02de61bb2e9cd61197395` | IDENTICAL |
| 418 | `methods/aris-vendor/skills/claims-drafting/SKILL.md` | `701d3111d87619c7ea1d5b88335d0d71a2cdb40b20944a5abc28d9ca50212b55` | `701d3111d87619c7ea1d5b88335d0d71a2cdb40b20944a5abc28d9ca50212b55` | IDENTICAL |
| 419 | `methods/aris-vendor/skills/comm-lit-review/SKILL.md` | `9fefbc15dae68a19176f6d7e78c348979a23b2a2363291b7ef81081c6dfb770d` | `9fefbc15dae68a19176f6d7e78c348979a23b2a2363291b7ef81081c6dfb770d` | IDENTICAL |
| 420 | `methods/aris-vendor/skills/deepxiv/SKILL.md` | `cbf5e46d7140d78a4e28191cf773e3d645b1c75a4926e414906d2dfa03ee22bc` | `cbf5e46d7140d78a4e28191cf773e3d645b1c75a4926e414906d2dfa03ee22bc` | IDENTICAL |
| 421 | `methods/aris-vendor/skills/dse-loop/SKILL.md` | `ae8e147011f7c1a6add208b6cecb218d03a83949fba0ef9b0b1936e4b0ee18bf` | `ae8e147011f7c1a6add208b6cecb218d03a83949fba0ef9b0b1936e4b0ee18bf` | IDENTICAL |
| 422 | `methods/aris-vendor/skills/embodiment-description/SKILL.md` | `8833b4569435077554d51ac59f79c8b4ceca64b777f129b1e8eaa328be9bb9a2` | `8833b4569435077554d51ac59f79c8b4ceca64b777f129b1e8eaa328be9bb9a2` | IDENTICAL |
| 423 | `methods/aris-vendor/skills/exa-search/SKILL.md` | `c9ffd1e95004f591d6bc17e1a5bf16864f0c0230f446d60c6fc2b3890afb71de` | `c9ffd1e95004f591d6bc17e1a5bf16864f0c0230f446d60c6fc2b3890afb71de` | IDENTICAL |
| 424 | `methods/aris-vendor/skills/experiment-audit/SKILL.md` | `476bde891323ebf9496ac2a52f8dbbf67fae13cfc6f7c69d4d3213794f3f1af2` | `476bde891323ebf9496ac2a52f8dbbf67fae13cfc6f7c69d4d3213794f3f1af2` | IDENTICAL |
| 425 | `methods/aris-vendor/skills/experiment-bridge/SKILL.md` | `1045988eabda1dcf19ed02a6832cec596f6667eaecb70ca50a0cf2a721d9759f` | `1045988eabda1dcf19ed02a6832cec596f6667eaecb70ca50a0cf2a721d9759f` | IDENTICAL |
| 426 | `methods/aris-vendor/skills/experiment-plan/SKILL.md` | `c5b53692ff95b0b55e80702e33afc79d9fe8d4f55a69e2a39714013f97ac595e` | `c5b53692ff95b0b55e80702e33afc79d9fe8d4f55a69e2a39714013f97ac595e` | IDENTICAL |
| 427 | `methods/aris-vendor/skills/experiment-queue/SKILL.md` | `6da32285f905d77664334bba7f7bbc2c069814ff5c3bc266ecc00f6c77d77208` | `6da32285f905d77664334bba7f7bbc2c069814ff5c3bc266ecc00f6c77d77208` | IDENTICAL |
| 428 | `methods/aris-vendor/skills/experiment-queue/scripts/build_manifest.py` | `2fe0d13d2bba863e9bbde65f8a746f1c0f46b7e2c08e16107786fad6980a5820` | `2fe0d13d2bba863e9bbde65f8a746f1c0f46b7e2c08e16107786fad6980a5820` | IDENTICAL |
| 429 | `methods/aris-vendor/skills/experiment-queue/scripts/queue_manager.py` | `9b53e554bda3fec88d9d293e323e26f531d8c074b7544a8ca7b4c3b529ab0129` | `9b53e554bda3fec88d9d293e323e26f531d8c074b7544a8ca7b4c3b529ab0129` | IDENTICAL |
| 430 | `methods/aris-vendor/skills/feishu-notify/SKILL.md` | `1a6c2e7a92b4f10c25cb7a9c647919a9dcc9b1fc9a6c99a86e73d757c8a6edbf` | `1a6c2e7a92b4f10c25cb7a9c647919a9dcc9b1fc9a6c99a86e73d757c8a6edbf` | IDENTICAL |
| 431 | `methods/aris-vendor/skills/figure-description/SKILL.md` | `4c69bc650a67d1688f44c909c49be98ffe74ea427b3859edb3c3357ec5730136` | `4c69bc650a67d1688f44c909c49be98ffe74ea427b3859edb3c3357ec5730136` | IDENTICAL |
| 432 | `methods/aris-vendor/skills/figure-spec/SKILL.md` | `93c1018de5e744354809807ff9f4b29693dcd7272f4cf5aec6e55f3e802708f5` | `93c1018de5e744354809807ff9f4b29693dcd7272f4cf5aec6e55f3e802708f5` | IDENTICAL |
| 433 | `methods/aris-vendor/skills/figure-spec/scripts/figure_renderer.py` | `02b4e01e46b51aeca12722ddd7b21bb7da3c3b175bba5d129c45d671fb07a0bc` | `02b4e01e46b51aeca12722ddd7b21bb7da3c3b175bba5d129c45d671fb07a0bc` | IDENTICAL |
| 434 | `methods/aris-vendor/skills/formula-derivation/SKILL.md` | `2e5f5ce665023cdc460126c9c8403503c17961145a2b052d25200f9bbd9a9b4d` | `2e5f5ce665023cdc460126c9c8403503c17961145a2b052d25200f9bbd9a9b4d` | IDENTICAL |
| 435 | `methods/aris-vendor/skills/gemini-search/SKILL.md` | `a8778e4e1dacae68691d13342a9a33200ade427beb777a4defbbb91dfcb030e3` | `a8778e4e1dacae68691d13342a9a33200ade427beb777a4defbbb91dfcb030e3` | IDENTICAL |
| 436 | `methods/aris-vendor/skills/grant-proposal/SKILL.md` | `c0859beb700f4f805752ab352738f740034154dc548cd060cc0e3f85b698a35e` | `c0859beb700f4f805752ab352738f740034154dc548cd060cc0e3f85b698a35e` | IDENTICAL |
| 437 | `methods/aris-vendor/skills/idea-creator/SKILL.md` | `980e2fb9214b092213e44993ace9ea8940f7eb0694b5032e7fbb9aeeadb5b5b1` | `980e2fb9214b092213e44993ace9ea8940f7eb0694b5032e7fbb9aeeadb5b5b1` | IDENTICAL |
| 438 | `methods/aris-vendor/skills/idea-discovery-robot/SKILL.md` | `4533db8a0aa8b262eb2b5ee5b55a1d94ee6e1927eb37aea43f65ef2d6a6c2f94` | `4533db8a0aa8b262eb2b5ee5b55a1d94ee6e1927eb37aea43f65ef2d6a6c2f94` | IDENTICAL |
| 439 | `methods/aris-vendor/skills/idea-discovery/SKILL.md` | `c265e307f1fb8b7f30eff7ea258218fc49aa52d785ebfdcee015736f1620807e` | `c265e307f1fb8b7f30eff7ea258218fc49aa52d785ebfdcee015736f1620807e` | IDENTICAL |
| 440 | `methods/aris-vendor/skills/integrity-forensics/SKILL.md` | `01e3d60412fecef6c9c512b2119e3ae8fe175ad74a818991acc988465d438677` | `01e3d60412fecef6c9c512b2119e3ae8fe175ad74a818991acc988465d438677` | IDENTICAL |
| 441 | `methods/aris-vendor/skills/interview-cheatsheet/SKILL.md` | `0524612213093cbd9196164b635d66843c472086e6d190c4207f2a8b2ee7d4ab` | `0524612213093cbd9196164b635d66843c472086e6d190c4207f2a8b2ee7d4ab` | IDENTICAL |
| 442 | `methods/aris-vendor/skills/invention-structuring/SKILL.md` | `bc0ac16349e9f607575b26bac8f6183563e8c19aa3ab5665b61c72b91ebde3e1` | `bc0ac16349e9f607575b26bac8f6183563e8c19aa3ab5665b61c72b91ebde3e1` | IDENTICAL |
| 443 | `methods/aris-vendor/skills/jurisdiction-format/SKILL.md` | `7683f58c4ad6465b4c4dd4f360876b12b0132777ca4ba40c1e48b777f4b40bb9` | `7683f58c4ad6465b4c4dd4f360876b12b0132777ca4ba40c1e48b777f4b40bb9` | IDENTICAL |
| 444 | `methods/aris-vendor/skills/kill-argument/SKILL.md` | `074e7cb2baa97e63232107940634581520d2c61dcfb62fdd3668d25bb48e9306` | `074e7cb2baa97e63232107940634581520d2c61dcfb62fdd3668d25bb48e9306` | IDENTICAL |
| 445 | `methods/aris-vendor/skills/mermaid-diagram/SKILL.md` | `b7cb4fb550b43be0c49224b608ff2a3a4a208997b8c8ce1d6a6310d165915f50` | `b7cb4fb550b43be0c49224b608ff2a3a4a208997b8c8ce1d6a6310d165915f50` | IDENTICAL |
| 446 | `methods/aris-vendor/skills/meta-apply/SKILL.md` | `5122453add96f0bd13933a1d9416ff61afbfce4f6892dc656f2495c0dcadbfa6` | `5122453add96f0bd13933a1d9416ff61afbfce4f6892dc656f2495c0dcadbfa6` | IDENTICAL |
| 447 | `methods/aris-vendor/skills/meta-optimize/SKILL.md` | `07c8c71e3f9937036c762f444d8c04d7f18ed56ed80840b8a0d0e2df67f8458c` | `07c8c71e3f9937036c762f444d8c04d7f18ed56ed80840b8a0d0e2df67f8458c` | IDENTICAL |
| 448 | `methods/aris-vendor/skills/monitor-experiment/SKILL.md` | `0527977308bb7b26139ffb56cd2d45ecc72a9dd2961073ad51fac4aac106961d` | `0527977308bb7b26139ffb56cd2d45ecc72a9dd2961073ad51fac4aac106961d` | IDENTICAL |
| 449 | `methods/aris-vendor/skills/novelty-check/SKILL.md` | `c512579faa065c7e886935d64c2d7d7c810cef8e8f5f6ff5cd902d6ab90e68af` | `c512579faa065c7e886935d64c2d7d7c810cef8e8f5f6ff5cd902d6ab90e68af` | IDENTICAL |
| 450 | `methods/aris-vendor/skills/openalex/SKILL.md` | `4c853b646987c4472a8360e044ad232aa9731dcfb60c7183073e8e5f3e6ac9c1` | `4c853b646987c4472a8360e044ad232aa9731dcfb60c7183073e8e5f3e6ac9c1` | IDENTICAL |
| 451 | `methods/aris-vendor/skills/overleaf-sync/SKILL.md` | `15644b418d9d043ac1f66e03242a9f8ecebc63569fc0a43f913252f3bfb2abe7` | `15644b418d9d043ac1f66e03242a9f8ecebc63569fc0a43f913252f3bfb2abe7` | IDENTICAL |
| 452 | `methods/aris-vendor/skills/paper-claim-audit/SKILL.md` | `7cf2a3659a0de183925969039a026a585d111d324f564bb3d2a6ff5cc4457f68` | `7cf2a3659a0de183925969039a026a585d111d324f564bb3d2a6ff5cc4457f68` | IDENTICAL |
| 453 | `methods/aris-vendor/skills/paper-compile/SKILL.md` | `ca064e9b7dffe80d9c3bcabb060f81c651e4926eb1c069a04c6416a8e58fed93` | `ca064e9b7dffe80d9c3bcabb060f81c651e4926eb1c069a04c6416a8e58fed93` | IDENTICAL |
| 454 | `methods/aris-vendor/skills/paper-figure/SKILL.md` | `4bb31eab22c73150c2160e45e17e76c2afb308cff7233de517bab3f3d3c63800` | `4bb31eab22c73150c2160e45e17e76c2afb308cff7233de517bab3f3d3c63800` | IDENTICAL |
| 455 | `methods/aris-vendor/skills/paper-illustration-image2/SKILL.md` | `178b200cd549e53dd1b02450a8bf086cfde7dbf4042613d8d87fe555b9411842` | `178b200cd549e53dd1b02450a8bf086cfde7dbf4042613d8d87fe555b9411842` | IDENTICAL |
| 456 | `methods/aris-vendor/skills/paper-illustration-image2/scripts/paper_illustration_image2.py` | `bc97f5b1ae14ffaff10c24240b6e93f3c1282ffd340d4756ea80477649f32890` | `bc97f5b1ae14ffaff10c24240b6e93f3c1282ffd340d4756ea80477649f32890` | IDENTICAL |
| 457 | `methods/aris-vendor/skills/paper-illustration/SKILL.md` | `af9307d178b8242c9a8d2e94c1264add91d5aa2bbc6444556b51b501c1918e65` | `af9307d178b8242c9a8d2e94c1264add91d5aa2bbc6444556b51b501c1918e65` | IDENTICAL |
| 458 | `methods/aris-vendor/skills/paper-plan/SKILL.md` | `32316a6e8009da226e75c5bb26a1417b934a6519ca34e80747e32397074eadd3` | `32316a6e8009da226e75c5bb26a1417b934a6519ca34e80747e32397074eadd3` | IDENTICAL |
| 459 | `methods/aris-vendor/skills/paper-poster-html/DESIGN_FINAL.md` | `1e1931569efe301a05ce815c238f48b05b7f27a92a7d179f84ebe1d5e22fdf25` | `1e1931569efe301a05ce815c238f48b05b7f27a92a7d179f84ebe1d5e22fdf25` | IDENTICAL |
| 460 | `methods/aris-vendor/skills/paper-poster-html/IMPLEMENTATION_CONVENTIONS.md` | `59cdf8fafb92a22efa93971b647e05386f46c473909c752674d65990b8886483` | `59cdf8fafb92a22efa93971b647e05386f46c473909c752674d65990b8886483` | IDENTICAL |
| 461 | `methods/aris-vendor/skills/paper-poster-html/LICENSES/posterly-MIT.txt` | `0f097b552f2be95d202723d681c73a1dec10d64d0afea3ee0a0eaf63def9a5be` | `0f097b552f2be95d202723d681c73a1dec10d64d0afea3ee0a0eaf63def9a5be` | IDENTICAL |
| 462 | `methods/aris-vendor/skills/paper-poster-html/NOTICE.md` | `058090d55f2c7d143f70b4e3020cb7bcb8349480edd9dbf46921e05067862ab1` | `058090d55f2c7d143f70b4e3020cb7bcb8349480edd9dbf46921e05067862ab1` | IDENTICAL |
| 463 | `methods/aris-vendor/skills/paper-poster-html/SKILL.md` | `6c44eabe999a90f733a722af99c2a920446900864f99342a2aa1bd9281de4e98` | `6c44eabe999a90f733a722af99c2a920446900864f99342a2aa1bd9281de4e98` | IDENTICAL |
| 464 | `methods/aris-vendor/skills/paper-poster-html/scripts/_posterly/__init__.py` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | IDENTICAL |
| 465 | `methods/aris-vendor/skills/paper-poster-html/scripts/_posterly/canvas.py` | `11503d98ebc2b817c34d3d05e85c169c8b9ccee55cc0d19ff4c6d488f39c36ec` | `11503d98ebc2b817c34d3d05e85c169c8b9ccee55cc0d19ff4c6d488f39c36ec` | IDENTICAL |
| 466 | `methods/aris-vendor/skills/paper-poster-html/scripts/_posterly/measure.py` | `ffaab446329621f5621fa29fd7e0cabb38a5be1a31e92be6acd36b818de416e3` | `ffaab446329621f5621fa29fd7e0cabb38a5be1a31e92be6acd36b818de416e3` | IDENTICAL |
| 467 | `methods/aris-vendor/skills/paper-poster-html/scripts/_posterly/polish.py` | `d401dbf27ee198a35b4d4a83aaf1df2c23e148f353557b66599f88155f9df96b` | `d401dbf27ee198a35b4d4a83aaf1df2c23e148f353557b66599f88155f9df96b` | IDENTICAL |
| 468 | `methods/aris-vendor/skills/paper-poster-html/scripts/_posterly/preflight.py` | `ca81022db3d92b9b3f3414128378df55bc2aba6560681d4d930e1e3426e31d32` | `ca81022db3d92b9b3f3414128378df55bc2aba6560681d4d930e1e3426e31d32` | IDENTICAL |
| 469 | `methods/aris-vendor/skills/paper-poster-html/scripts/_posterly/render.py` | `0ba4bcb874e0648b9058a1ae0b0168dc16f4c8ee382f005f69326d45acf9034b` | `0ba4bcb874e0648b9058a1ae0b0168dc16f4c8ee382f005f69326d45acf9034b` | IDENTICAL |
| 470 | `methods/aris-vendor/skills/paper-poster-html/scripts/_posterly/textutil.py` | `a2b32524cf004810d46bb442b6f418ff7445b3aff4d7995a8bf6b7784de36c3e` | `a2b32524cf004810d46bb442b6f418ff7445b3aff4d7995a8bf6b7784de36c3e` | IDENTICAL |
| 471 | `methods/aris-vendor/skills/paper-poster-html/scripts/_posterly/verify_final.py` | `bb2c737496d49d5028e7c8798f2aa39837c0f72677fa6b444c5710dac6e3d283` | `bb2c737496d49d5028e7c8798f2aa39837c0f72677fa6b444c5710dac6e3d283` | IDENTICAL |
| 472 | `methods/aris-vendor/skills/paper-poster-html/scripts/asset_check.py` | `84f6b34560c903ddf8d6748ad70858ec00734f03a590d5705914c6ce53c6e37c` | `84f6b34560c903ddf8d6748ad70858ec00734f03a590d5705914c6ce53c6e37c` | IDENTICAL |
| 473 | `methods/aris-vendor/skills/paper-poster-html/scripts/extract_pdf_figures.py` | `5f2f48392c69a50d7e894ad5ac2462e4e6971e266a8ab9f760f786e00c222910` | `5f2f48392c69a50d7e894ad5ac2462e4e6971e266a8ab9f760f786e00c222910` | IDENTICAL |
| 474 | `methods/aris-vendor/skills/paper-poster-html/scripts/poster_check.py` | `a048eeba87444be279b8b0fb3796079419546315ed10b460778bc82c752e4db6` | `a048eeba87444be279b8b0fb3796079419546315ed10b460778bc82c752e4db6` | IDENTICAL |
| 475 | `methods/aris-vendor/skills/paper-poster-html/scripts/preprocess_figures.py` | `74d18140aab1ba5e10d0f26fb21c99cc2b7293fb4f2ab6a9d891d91d4328ad47` | `74d18140aab1ba5e10d0f26fb21c99cc2b7293fb4f2ab6a9d891d91d4328ad47` | IDENTICAL |
| 476 | `methods/aris-vendor/skills/paper-poster-html/scripts/render_preview.py` | `5114c27fb2fc0703c2a3c749f2b84cfd6d6cc29051b44572e99db87b7ca8ea52` | `5114c27fb2fc0703c2a3c749f2b84cfd6d6cc29051b44572e99db87b7ca8ea52` | IDENTICAL |
| 477 | `methods/aris-vendor/skills/paper-poster-html/scripts/run_gates.py` | `807d59964259e1eff1a6bd13af2f34b3c1d1404316d1a3a32558b420308fb7e3` | `807d59964259e1eff1a6bd13af2f34b3c1d1404316d1a3a32558b420308fb7e3` | IDENTICAL |
| 478 | `methods/aris-vendor/skills/paper-poster-html/scripts/style_check.py` | `029eff049907ea1a8ca4ee65ca8d10fe26d09591d6d96684fc6cb14e90879530` | `029eff049907ea1a8ca4ee65ca8d10fe26d09591d6d96684fc6cb14e90879530` | IDENTICAL |
| 479 | `methods/aris-vendor/skills/paper-poster-html/templates/COMPONENTS.md` | `382e60604f4bbe9a8aa96272348f34314089de847760c1897a6f701b5984f8b8` | `382e60604f4bbe9a8aa96272348f34314089de847760c1897a6f701b5984f8b8` | IDENTICAL |
| 480 | `methods/aris-vendor/skills/paper-poster-html/templates/README.md` | `366923d0de663296a2e3aca8479775423ac280b126d9d9272aa0041413dca309` | `366923d0de663296a2e3aca8479775423ac280b126d9d9272aa0041413dca309` | IDENTICAL |
| 481 | `methods/aris-vendor/skills/paper-poster-html/templates/landscape_4col.html` | `1e72098d28541968bcd7b3960be70d545b86680998c6976f545615d5b7b735d8` | `1e72098d28541968bcd7b3960be70d545b86680998c6976f545615d5b7b735d8` | IDENTICAL |
| 482 | `methods/aris-vendor/skills/paper-poster-html/templates/landscape_hero.html` | `fd82519f94a25397fbb799af6b5ec887140763980f39b42598a6ad27a470ed93` | `fd82519f94a25397fbb799af6b5ec887140763980f39b42598a6ad27a470ed93` | IDENTICAL |
| 483 | `methods/aris-vendor/skills/paper-poster-html/templates/portrait_2col.html` | `c6031ab64807f04d5db19ef5aa2d57bc49db0853e1a98c18de38f81b804e1779` | `c6031ab64807f04d5db19ef5aa2d57bc49db0853e1a98c18de38f81b804e1779` | IDENTICAL |
| 484 | `methods/aris-vendor/skills/paper-poster-html/templates/tokens/acl.json` | `e9c2bcef6c7433f9ca79437bae729b513f59ff61b8b843c575a205be52f2e4e8` | `e9c2bcef6c7433f9ca79437bae729b513f59ff61b8b843c575a205be52f2e4e8` | IDENTICAL |
| 485 | `methods/aris-vendor/skills/paper-poster-html/templates/tokens/cvpr.json` | `921e1c08dabf2f10531c87a4a10bd9228642afc2e089ed3d3a9fcef3ea24288c` | `921e1c08dabf2f10531c87a4a10bd9228642afc2e089ed3d3a9fcef3ea24288c` | IDENTICAL |
| 486 | `methods/aris-vendor/skills/paper-poster-html/templates/tokens/generic.json` | `229084d6c166d589b3c3ec2cf024c4e6341c91eea45b07fb84bd7be8c1e6bf82` | `229084d6c166d589b3c3ec2cf024c4e6341c91eea45b07fb84bd7be8c1e6bf82` | IDENTICAL |
| 487 | `methods/aris-vendor/skills/paper-poster-html/templates/tokens/iclr.json` | `b176829c14d8fbaa7b0eb49873ce7b9cb3150aad13990b4eecaa2c825582a65b` | `b176829c14d8fbaa7b0eb49873ce7b9cb3150aad13990b4eecaa2c825582a65b` | IDENTICAL |
| 488 | `methods/aris-vendor/skills/paper-poster-html/templates/tokens/icml.json` | `078dbb6101e8579559ba24a41582af0b3b8dbc3f487a8fb9676ca5ba41b5e345` | `078dbb6101e8579559ba24a41582af0b3b8dbc3f487a8fb9676ca5ba41b5e345` | IDENTICAL |
| 489 | `methods/aris-vendor/skills/paper-poster-html/templates/tokens/neurips.json` | `f59567e68fa011eae86ec58d85abe564d6acce5174896a755e7588e3da33954c` | `f59567e68fa011eae86ec58d85abe564d6acce5174896a755e7588e3da33954c` | IDENTICAL |
| 490 | `methods/aris-vendor/skills/paper-poster/SKILL.md` | `7dec9b7f9bc2d12df23148cd38f51ea344b0b23370051ef6e03779ed41e97260` | `7dec9b7f9bc2d12df23148cd38f51ea344b0b23370051ef6e03779ed41e97260` | IDENTICAL |
| 491 | `methods/aris-vendor/skills/paper-slides/SKILL.md` | `b80122f34562924ea2823dbc522c6ae6e2915941aa86a721952900ee04dc6c9e` | `b80122f34562924ea2823dbc522c6ae6e2915941aa86a721952900ee04dc6c9e` | IDENTICAL |
| 492 | `methods/aris-vendor/skills/paper-talk/SKILL.md` | `0bd7722963e9dc721cff4d66fda72e5e4242a116370dfae2fc9669b408d2f199` | `0bd7722963e9dc721cff4d66fda72e5e4242a116370dfae2fc9669b408d2f199` | IDENTICAL |
| 493 | `methods/aris-vendor/skills/paper-write/SKILL.md` | `502ac7f0fcf806bdb67f1681b0178133a38323dff82804244e422a74fe4d88b2` | `502ac7f0fcf806bdb67f1681b0178133a38323dff82804244e422a74fe4d88b2` | IDENTICAL |
| 494 | `methods/aris-vendor/skills/paper-write/templates/IEEEtran.bst` | `314f0ece704568faf827011bac498650691b2b5ee06320720830e782416d5a5f` | `314f0ece704568faf827011bac498650691b2b5ee06320720830e782416d5a5f` | IDENTICAL |
| 495 | `methods/aris-vendor/skills/paper-write/templates/IEEEtran.cls` | `da751920a317ed318b7b5cd7fa585a6cc7d28502d457856382e9be24b10a3bd7` | `da751920a317ed318b7b5cd7fa585a6cc7d28502d457856382e9be24b10a3bd7` | IDENTICAL |
| 496 | `methods/aris-vendor/skills/paper-write/templates/iclr2026.tex` | `1e4c20b3c5b7445966194151d33c3e2023e828e621be8baf7ffb234b987cfc23` | `1e4c20b3c5b7445966194151d33c3e2023e828e621be8baf7ffb234b987cfc23` | IDENTICAL |
| 497 | `methods/aris-vendor/skills/paper-write/templates/icml2025.tex` | `d346d4b5b96276a4e04ccd7590ad158cce4aabcc090281dca7c4b0900d11530b` | `d346d4b5b96276a4e04ccd7590ad158cce4aabcc090281dca7c4b0900d11530b` | IDENTICAL |
| 498 | `methods/aris-vendor/skills/paper-write/templates/ieee_conference.tex` | `a3dc3a175a7dd1512f4a2fdb844a0a482a9e919162e37dc27373d501fbafafbc` | `a3dc3a175a7dd1512f4a2fdb844a0a482a9e919162e37dc27373d501fbafafbc` | IDENTICAL |
| 499 | `methods/aris-vendor/skills/paper-write/templates/ieee_journal.tex` | `bdff7ff0aa376d8a46675bdb6e96c4dd715463360735706aa5fbaa5f834b7604` | `bdff7ff0aa376d8a46675bdb6e96c4dd715463360735706aa5fbaa5f834b7604` | IDENTICAL |
| 500 | `methods/aris-vendor/skills/paper-write/templates/math_commands.tex` | `3efe4556b2c33b4a93c1b6e86b99b9a3ecbd9c9565ccc06bf8a1f51293470dc6` | `3efe4556b2c33b4a93c1b6e86b99b9a3ecbd9c9565ccc06bf8a1f51293470dc6` | IDENTICAL |
| 501 | `methods/aris-vendor/skills/paper-write/templates/neurips2025.tex` | `fef6448048e58b748d67f438dce6fcfedcc49467542a951d1986dc5b81ca256c` | `fef6448048e58b748d67f438dce6fcfedcc49467542a951d1986dc5b81ca256c` | IDENTICAL |
| 502 | `methods/aris-vendor/skills/paper-writing/SKILL.md` | `b8c3678e294e6d5a366739a646ff655f932be5299692e4b14c3f5dbee44e0d8b` | `b8c3678e294e6d5a366739a646ff655f932be5299692e4b14c3f5dbee44e0d8b` | IDENTICAL |
| 503 | `methods/aris-vendor/skills/patent-novelty-check/SKILL.md` | `374eae99fb0d0e603d6e881de00daea799dc96eb833446e7db08c87304abf274` | `374eae99fb0d0e603d6e881de00daea799dc96eb833446e7db08c87304abf274` | IDENTICAL |
| 504 | `methods/aris-vendor/skills/patent-pipeline/SKILL.md` | `48834310bc0b728544047dc20909996f65647e1ef80b1e1c4666cbf60403faa9` | `48834310bc0b728544047dc20909996f65647e1ef80b1e1c4666cbf60403faa9` | IDENTICAL |
| 505 | `methods/aris-vendor/skills/patent-review/SKILL.md` | `dceadf86a54b816b0a59be5cc2e52a9ff9fe4ff03613fafd9972046b4eeb5510` | `dceadf86a54b816b0a59be5cc2e52a9ff9fe4ff03613fafd9972046b4eeb5510` | IDENTICAL |
| 506 | `methods/aris-vendor/skills/pixel-art/SKILL.md` | `e65d74863168eeefb0405c6da9db1858bd7940d4bda40af9d3e85acffba5dc8c` | `e65d74863168eeefb0405c6da9db1858bd7940d4bda40af9d3e85acffba5dc8c` | IDENTICAL |
| 507 | `methods/aris-vendor/skills/prior-art-search/SKILL.md` | `8793fb26c522de4c44a64b68df81e5d12718a99866c639658261cea680bd58b2` | `8793fb26c522de4c44a64b68df81e5d12718a99866c639658261cea680bd58b2` | IDENTICAL |
| 508 | `methods/aris-vendor/skills/proof-checker/SKILL.md` | `533b0eed57171381cd5aabeb1c5cee7bbf23f46c36ad3483ddcc710c4cf5a8e1` | `533b0eed57171381cd5aabeb1c5cee7bbf23f46c36ad3483ddcc710c4cf5a8e1` | IDENTICAL |
| 509 | `methods/aris-vendor/skills/proof-orchestrator/NOTICE.md` | `a496eb4ac401ae1fcfcd0958f47e585c1949e4cf43553517468fcdf73fc17124` | `a496eb4ac401ae1fcfcd0958f47e585c1949e4cf43553517468fcdf73fc17124` | IDENTICAL |
| 510 | `methods/aris-vendor/skills/proof-orchestrator/SKILL.md` | `bde239fa93e051281a529fb436c9dc277b82221cffe0941e1aab54c203fbc9f5` | `bde239fa93e051281a529fb436c9dc277b82221cffe0941e1aab54c203fbc9f5` | IDENTICAL |
| 511 | `methods/aris-vendor/skills/proof-orchestrator/references/audit-output-contract.md` | `cff8da1ef42794c64aba244decb19895b97ae912651e023c5c0b54a110e3eb7e` | `cff8da1ef42794c64aba244decb19895b97ae912651e023c5c0b54a110e3eb7e` | IDENTICAL |
| 512 | `methods/aris-vendor/skills/proof-orchestrator/references/deepseek-routing.md` | `1a3072362c8831b602b4adc4d69fba743a27584fac1c1413ca79a5831e9715eb` | `1a3072362c8831b602b4adc4d69fba743a27584fac1c1413ca79a5831e9715eb` | IDENTICAL |
| 513 | `methods/aris-vendor/skills/proof-orchestrator/references/dispatch-prompts.md` | `a32693defd4ec03fe7c23a813d3e7a6b5b868ce34ac3ffe34b798ad624f469b7` | `a32693defd4ec03fe7c23a813d3e7a6b5b868ce34ac3ffe34b798ad624f469b7` | IDENTICAL |
| 514 | `methods/aris-vendor/skills/proof-orchestrator/references/notation-audit.md` | `8db3079a9209d9c71b977d448cff1abe33c5cf6414b1923735c813c9fc56e757` | `8db3079a9209d9c71b977d448cff1abe33c5cf6414b1923735c813c9fc56e757` | IDENTICAL |
| 515 | `methods/aris-vendor/skills/proof-orchestrator/references/proof-audit-rubric.md` | `fb962314da5291f5376da55f502f94a9337f380b481cf12208d6b586341b86bf` | `fb962314da5291f5376da55f502f94a9337f380b481cf12208d6b586341b86bf` | IDENTICAL |
| 516 | `methods/aris-vendor/skills/proof-orchestrator/references/stress-tests.md` | `5d865f4bc1df6d872103b6da7cfb2a24c6b8d40432c6228e94285e136fe48614` | `5d865f4bc1df6d872103b6da7cfb2a24c6b8d40432c6228e94285e136fe48614` | IDENTICAL |
| 517 | `methods/aris-vendor/skills/proof-writer/SKILL.md` | `d59b1865ba06f060b40920ace4ff8f61dc729615387bb91b1eb22a5d5442f2fe` | `d59b1865ba06f060b40920ace4ff8f61dc729615387bb91b1eb22a5d5442f2fe` | IDENTICAL |
| 518 | `methods/aris-vendor/skills/qzcli/SKILL.md` | `328953e6e4a21f8a38e979f9729818721af387724b799cb7cc96e072d0012d2f` | `328953e6e4a21f8a38e979f9729818721af387724b799cb7cc96e072d0012d2f` | IDENTICAL |
| 519 | `methods/aris-vendor/skills/rebuttal/SKILL.md` | `e8d30a41aa6682f57a0068d72ecca4c9993fcb1188e8e8b834b3b0f4ea18b9f7` | `e8d30a41aa6682f57a0068d72ecca4c9993fcb1188e8e8b834b3b0f4ea18b9f7` | IDENTICAL |
| 520 | `methods/aris-vendor/skills/render-html/SKILL.md` | `0f9e5b4572242685fe7a4bd6f10c6832727d060a58942d7c61adca7b7fc02773` | `0f9e5b4572242685fe7a4bd6f10c6832727d060a58942d7c61adca7b7fc02773` | IDENTICAL |
| 521 | `methods/aris-vendor/skills/render-html/scripts/render_html.py` | `f563872737d1fafbc38ea6a6de85451063daa196b219e163dcb32c3abeb6d58f` | `f563872737d1fafbc38ea6a6de85451063daa196b219e163dcb32c3abeb6d58f` | IDENTICAL |
| 522 | `methods/aris-vendor/skills/render-html/scripts/templates/academic.html` | `af3a2f998091edd2804b9e64eab21bf77b6caa57349fcfbbe767b1a8d16380cc` | `af3a2f998091edd2804b9e64eab21bf77b6caa57349fcfbbe767b1a8d16380cc` | IDENTICAL |
| 523 | `methods/aris-vendor/skills/render-html/scripts/templates/dashboard.html` | `156e0825a131279debe55d1b91d7aa7c5f85e755458414932110687c9c3b3779` | `156e0825a131279debe55d1b91d7aa7c5f85e755458414932110687c9c3b3779` | IDENTICAL |
| 524 | `methods/aris-vendor/skills/research-lit/SKILL.md` | `00d9f549e4db72f3b02d55b9f6dcd61b20403f5a7e25cf3396160423140b9183` | `00d9f549e4db72f3b02d55b9f6dcd61b20403f5a7e25cf3396160423140b9183` | IDENTICAL |
| 525 | `methods/aris-vendor/skills/research-pipeline/SKILL.md` | `e1f97fdcc1e8a28af0a425d3bac344d9c675ef7397d3b3ad8f27cb97dbf20510` | `e1f97fdcc1e8a28af0a425d3bac344d9c675ef7397d3b3ad8f27cb97dbf20510` | IDENTICAL |
| 526 | `methods/aris-vendor/skills/research-refine-pipeline/SKILL.md` | `d5091663645dae48b84ce273d0f774090aeb2c553ed064d2d4cfc17fad9c52e9` | `d5091663645dae48b84ce273d0f774090aeb2c553ed064d2d4cfc17fad9c52e9` | IDENTICAL |
| 527 | `methods/aris-vendor/skills/research-refine/SKILL.md` | `2cbda50557603d608990eff7f7a9890b2f75978a5219a8bc8b6e49cebe7e1884` | `2cbda50557603d608990eff7f7a9890b2f75978a5219a8bc8b6e49cebe7e1884` | IDENTICAL |
| 528 | `methods/aris-vendor/skills/research-review/SKILL.md` | `2d2c27ccedeb9d053b16ff9e64e61e2653c42841618d382531a3191cc37b72db` | `2d2c27ccedeb9d053b16ff9e64e61e2653c42841618d382531a3191cc37b72db` | IDENTICAL |
| 529 | `methods/aris-vendor/skills/research-wiki/SKILL.md` | `3bd314f83f2db97fcfafb74495f1ca23bebad37a69d355bc61aaea8cbb519552` | `3bd314f83f2db97fcfafb74495f1ca23bebad37a69d355bc61aaea8cbb519552` | IDENTICAL |
| 530 | `methods/aris-vendor/skills/resubmit-pipeline/SKILL.md` | `c919caf4c1dfe39ef34cce802e15f38d0c71076ce2fae074a7e3b509dac7d53a` | `c919caf4c1dfe39ef34cce802e15f38d0c71076ce2fae074a7e3b509dac7d53a` | IDENTICAL |
| 531 | `methods/aris-vendor/skills/result-to-claim/SKILL.md` | `251940dc0a443b27e9b24ef7d65c05c6e3ed09b67b66de85d627fafee7506a5b` | `251940dc0a443b27e9b24ef7d65c05c6e3ed09b67b66de85d627fafee7506a5b` | IDENTICAL |
| 532 | `methods/aris-vendor/skills/run-experiment/SKILL.md` | `4d481ce95d8bcadb93b095c3dd9bda51d68b6edea6b710316d6c0c74bb5bcfa8` | `4d481ce95d8bcadb93b095c3dd9bda51d68b6edea6b710316d6c0c74bb5bcfa8` | IDENTICAL |
| 533 | `methods/aris-vendor/skills/semantic-scholar/SKILL.md` | `41be9cd7d08d2d795d4fe0c87d23288712febd2807b8d4d38a2ea9c54ebb31e8` | `41be9cd7d08d2d795d4fe0c87d23288712febd2807b8d4d38a2ea9c54ebb31e8` | IDENTICAL |
| 534 | `methods/aris-vendor/skills/serverless-modal/SKILL.md` | `e8444d7c5e4cb53f400602a96bf9fbb8c682b85ffda8c24bcceb19cc3337e31f` | `e8444d7c5e4cb53f400602a96bf9fbb8c682b85ffda8c24bcceb19cc3337e31f` | IDENTICAL |
| 535 | `methods/aris-vendor/skills/shared-references/acceptance-gate.md` | `acfe2e790d97445396ff4eb605b91e4de756082d617b89cf9278bff76dc25623` | `acfe2e790d97445396ff4eb605b91e4de756082d617b89cf9278bff76dc25623` | IDENTICAL |
| 536 | `methods/aris-vendor/skills/shared-references/assurance-contract.md` | `6bc8c73d6773fb1e564faefeca2876395db9f69f6c521cbb51425d32ad71f593` | `6bc8c73d6773fb1e564faefeca2876395db9f69f6c521cbb51425d32ad71f593` | IDENTICAL |
| 537 | `methods/aris-vendor/skills/shared-references/capture-antipatterns.md` | `419b914ade074842b815bff5133c18993a31305ca36e40b08918856777857378` | `419b914ade074842b815bff5133c18993a31305ca36e40b08918856777857378` | IDENTICAL |
| 538 | `methods/aris-vendor/skills/shared-references/citation-discipline.md` | `01fc1cf751d7e0e6bef04897df6ef1bcf1e1b20e5b56d9f208e020cc48ba6725` | `01fc1cf751d7e0e6bef04897df6ef1bcf1e1b20e5b56d9f208e020cc48ba6725` | IDENTICAL |
| 539 | `methods/aris-vendor/skills/shared-references/compute-env-contract.md` | `293606bcf6281712e0f5e1a05be9b67e001f2e5b567e2a956e2099de9c648974` | `293606bcf6281712e0f5e1a05be9b67e001f2e5b567e2a956e2099de9c648974` | IDENTICAL |
| 540 | `methods/aris-vendor/skills/shared-references/effort-contract.md` | `c1cb84a099d7d465ce71e0fc6c8fe7449c8273072b4cb977e0e58744d767f482` | `c1cb84a099d7d465ce71e0fc6c8fe7449c8273072b4cb977e0e58744d767f482` | IDENTICAL |
| 541 | `methods/aris-vendor/skills/shared-references/evidence-precheck.md` | `919a437a2e4a618ff6bcac6c03b7ec12bde3fef33d1a2aea25c9d98fcbd5e2d2` | `919a437a2e4a618ff6bcac6c03b7ec12bde3fef33d1a2aea25c9d98fcbd5e2d2` | IDENTICAL |
| 542 | `methods/aris-vendor/skills/shared-references/experiment-integrity.md` | `22150fbdc5867e7790c88f968bccb367079c2db4c190ddce980709aea7e76f60` | `22150fbdc5867e7790c88f968bccb367079c2db4c190ddce980709aea7e76f60` | IDENTICAL |
| 543 | `methods/aris-vendor/skills/shared-references/external-cadence.md` | `d0d8e92c9c8f5e60555c8ddf32cf15c78d0bdc61a367ef35d8b0fef8dab906f3` | `d0d8e92c9c8f5e60555c8ddf32cf15c78d0bdc61a367ef35d8b0fef8dab906f3` | IDENTICAL |
| 544 | `methods/aris-vendor/skills/shared-references/fan-out-pattern.md` | `c592ab391aad5e4573d6041c2a396a6daaf34e830aa384a9a17f0b9ede8d5fa1` | `c592ab391aad5e4573d6041c2a396a6daaf34e830aa384a9a17f0b9ede8d5fa1` | IDENTICAL |
| 545 | `methods/aris-vendor/skills/shared-references/injection-hygiene.md` | `c7abafc35dfa243b86f4990cfe41f7ee982716a463bfdb57750035e6cb7175c9` | `c7abafc35dfa243b86f4990cfe41f7ee982716a463bfdb57750035e6cb7175c9` | IDENTICAL |
| 546 | `methods/aris-vendor/skills/shared-references/integration-contract.md` | `891b4254337b6da02b25bef55cbe750e90f36fd7c8b537218e49febf6d69ddc0` | `891b4254337b6da02b25bef55cbe750e90f36fd7c8b537218e49febf6d69ddc0` | IDENTICAL |
| 547 | `methods/aris-vendor/skills/shared-references/output-composition.md` | `8de81708431091a21a641be5f91db7958bb9f9a4b85d4fe03f52c5b496948651` | `8de81708431091a21a641be5f91db7958bb9f9a4b85d4fe03f52c5b496948651` | IDENTICAL |
| 548 | `methods/aris-vendor/skills/shared-references/output-language.md` | `7b326400dca5130ce4beedf72fc2010680afe96eb56a6ab21210d323adc9a52e` | `7b326400dca5130ce4beedf72fc2010680afe96eb56a6ab21210d323adc9a52e` | IDENTICAL |
| 549 | `methods/aris-vendor/skills/shared-references/output-manifest.md` | `28e29bc8e53c52afe4eeeb590df8893282a3bbced08e105e154ad228b6cd1922` | `28e29bc8e53c52afe4eeeb590df8893282a3bbced08e105e154ad228b6cd1922` | IDENTICAL |
| 550 | `methods/aris-vendor/skills/shared-references/output-versioning.md` | `73a4269b537be728b0ecc35789f11fa6d1fafa6d0430d07ad2738f064b1e4da3` | `73a4269b537be728b0ecc35789f11fa6d1fafa6d0430d07ad2738f064b1e4da3` | IDENTICAL |
| 551 | `methods/aris-vendor/skills/shared-references/patent-format-cn.md` | `e5be6c2c6fab3c84c795b53ca419198192b95f2c1ccd63833b5d0510a8f93c1f` | `e5be6c2c6fab3c84c795b53ca419198192b95f2c1ccd63833b5d0510a8f93c1f` | IDENTICAL |
| 552 | `methods/aris-vendor/skills/shared-references/patent-format-ep.md` | `8cf58ac775fe524c230cd7f371abd0ce25eb774029129bc336f884026c58ba23` | `8cf58ac775fe524c230cd7f371abd0ce25eb774029129bc336f884026c58ba23` | IDENTICAL |
| 553 | `methods/aris-vendor/skills/shared-references/patent-format-us.md` | `13f179cc70fc8664f356d5258bdaa52a4cc577496e385e5ac5cdd421a12f4f65` | `13f179cc70fc8664f356d5258bdaa52a4cc577496e385e5ac5cdd421a12f4f65` | IDENTICAL |
| 554 | `methods/aris-vendor/skills/shared-references/patent-writing-principles.md` | `8c8dc8250948bd0741b792d350e3afdc686ed194a1bf02359fb0e55b81468d1d` | `8c8dc8250948bd0741b792d350e3afdc686ed194a1bf02359fb0e55b81468d1d` | IDENTICAL |
| 555 | `methods/aris-vendor/skills/shared-references/prior-art-databases.md` | `8225843987fbabb5f11788c19ed8a739f10691319865485d5cb876e7bc2a3cb7` | `8225843987fbabb5f11788c19ed8a739f10691319865485d5cb876e7bc2a3cb7` | IDENTICAL |
| 556 | `methods/aris-vendor/skills/shared-references/resumable-runs.md` | `08e776c6365aec0c5bd9b97dde9722550b202ac00053208964d655e38d21a011` | `08e776c6365aec0c5bd9b97dde9722550b202ac00053208964d655e38d21a011` | IDENTICAL |
| 557 | `methods/aris-vendor/skills/shared-references/review-scope-limits.md` | `1636b6bb96a18683698faad7bc103122ad0da9dcf3218b899f8413533f366e2a` | `1636b6bb96a18683698faad7bc103122ad0da9dcf3218b899f8413533f366e2a` | IDENTICAL |
| 558 | `methods/aris-vendor/skills/shared-references/review-tracing.md` | `4ac32ec75c8ed8e77a418c121b68b19e018992330ac0d626e43de3ed14937f38` | `4ac32ec75c8ed8e77a418c121b68b19e018992330ac0d626e43de3ed14937f38` | IDENTICAL |
| 559 | `methods/aris-vendor/skills/shared-references/reviewer-independence.md` | `fbbfcb6e7ff53010b596e8e01ce456d1906734f5bd198745f76ccd62787af3e3` | `fbbfcb6e7ff53010b596e8e01ce456d1906734f5bd198745f76ccd62787af3e3` | IDENTICAL |
| 560 | `methods/aris-vendor/skills/shared-references/reviewer-routing.md` | `47ed236c6d30b96c9e4d3c6dccffa3a744db938d2592a6c7dd3070b3c0ca78e0` | `47ed236c6d30b96c9e4d3c6dccffa3a744db938d2592a6c7dd3070b3c0ca78e0` | IDENTICAL |
| 561 | `methods/aris-vendor/skills/shared-references/skill-governance.md` | `270b4043772cda171a55f0cc36dfbd4d160ff2b309f6f882bb50a377764c369d` | `270b4043772cda171a55f0cc36dfbd4d160ff2b309f6f882bb50a377764c369d` | IDENTICAL |
| 562 | `methods/aris-vendor/skills/shared-references/taste-calibration.md` | `245e12a52b6c013022ddbcd8c682e4e5290bda6e38ecc6f14d7b2eaeb2988af8` | `245e12a52b6c013022ddbcd8c682e4e5290bda6e38ecc6f14d7b2eaeb2988af8` | IDENTICAL |
| 563 | `methods/aris-vendor/skills/shared-references/venue-checklists.md` | `712396be66d4db85f0038c5ff5479a5fc66db03bc7175c8ed931f7284802f4e2` | `712396be66d4db85f0038c5ff5479a5fc66db03bc7175c8ed931f7284802f4e2` | IDENTICAL |
| 564 | `methods/aris-vendor/skills/shared-references/wiki-helper-resolution.md` | `ef6af207034a2eea17d437ac2f4c620962f72960ae7a5bf0d00818e1bafc71c2` | `ef6af207034a2eea17d437ac2f4c620962f72960ae7a5bf0d00818e1bafc71c2` | IDENTICAL |
| 565 | `methods/aris-vendor/skills/shared-references/writing-principles.md` | `25c71f6b76fad1a198b47b4eae9b1d101561578cc0a8767e91706957829f0abe` | `25c71f6b76fad1a198b47b4eae9b1d101561578cc0a8767e91706957829f0abe` | IDENTICAL |
| 566 | `methods/aris-vendor/skills/skills-codex-claude-review/README.md` | `3b3583babc0dee5389a03bc7e38223870c6352d3dd328ba12f1aeb9c641f3531` | `3b3583babc0dee5389a03bc7e38223870c6352d3dd328ba12f1aeb9c641f3531` | IDENTICAL |
| 567 | `methods/aris-vendor/skills/skills-codex-claude-review/README_CN.md` | `53e3da0faac1d75f8df21a6e9ac133c60e11f880f8fee78b837fc21842d27b34` | `53e3da0faac1d75f8df21a6e9ac133c60e11f880f8fee78b837fc21842d27b34` | IDENTICAL |
| 568 | `methods/aris-vendor/skills/skills-codex-claude-review/auto-paper-improvement-loop/SKILL.md` | `9076a3d9ec35359e5f841e82c9d051aac020711c64f20ca5ff8bbebab1db6808` | `9076a3d9ec35359e5f841e82c9d051aac020711c64f20ca5ff8bbebab1db6808` | IDENTICAL |
| 569 | `methods/aris-vendor/skills/skills-codex-claude-review/auto-review-loop/SKILL.md` | `aa6705662d530916ff7d24de257a934a70bdfd50e5c73798ba569bb5d214d163` | `aa6705662d530916ff7d24de257a934a70bdfd50e5c73798ba569bb5d214d163` | IDENTICAL |
| 570 | `methods/aris-vendor/skills/skills-codex-claude-review/novelty-check/SKILL.md` | `3da0bfec9cd1e4967f9413f6bbca3713d39477a327e3411f56dbc88f6396d452` | `3da0bfec9cd1e4967f9413f6bbca3713d39477a327e3411f56dbc88f6396d452` | IDENTICAL |
| 571 | `methods/aris-vendor/skills/skills-codex-claude-review/paper-figure/SKILL.md` | `35ef68458ac9318b6e02e7f513a0a5bcd5c64d39aa3a9ece25c3256e047e0d9e` | `35ef68458ac9318b6e02e7f513a0a5bcd5c64d39aa3a9ece25c3256e047e0d9e` | IDENTICAL |
| 572 | `methods/aris-vendor/skills/skills-codex-claude-review/paper-plan/SKILL.md` | `c5b32253458230ecaaf6e34c7a2544af7c45e6a0e35ee9de96cbf9fe9e8b2fa9` | `c5b32253458230ecaaf6e34c7a2544af7c45e6a0e35ee9de96cbf9fe9e8b2fa9` | IDENTICAL |
| 573 | `methods/aris-vendor/skills/skills-codex-claude-review/paper-write/SKILL.md` | `a27b1fb60bce90904e22de2146626746db22f307a844a466a9d25e0ad6eb65a4` | `a27b1fb60bce90904e22de2146626746db22f307a844a466a9d25e0ad6eb65a4` | IDENTICAL |
| 574 | `methods/aris-vendor/skills/skills-codex-claude-review/research-refine/SKILL.md` | `9cb8f40b527028e4dd71321f70f4a76e5e432dd140d4c7be582cc480ae8f2579` | `9cb8f40b527028e4dd71321f70f4a76e5e432dd140d4c7be582cc480ae8f2579` | IDENTICAL |
| 575 | `methods/aris-vendor/skills/skills-codex-claude-review/research-review/SKILL.md` | `5f9089d21dda71208cf6538aa9bd3680b162857f5c70d180afb88a75a972407f` | `5f9089d21dda71208cf6538aa9bd3680b162857f5c70d180afb88a75a972407f` | IDENTICAL |
| 576 | `methods/aris-vendor/skills/skills-codex-gemini-review/README.md` | `07bf82c23dbd2613db49d39935a6f62449768cb9846b7786cb3a359c04f7844c` | `07bf82c23dbd2613db49d39935a6f62449768cb9846b7786cb3a359c04f7844c` | IDENTICAL |
| 577 | `methods/aris-vendor/skills/skills-codex-gemini-review/README_CN.md` | `6916272c6ffd02a0d191124e19baf7e4d798af6eb67e4cb01a78271bdd134a77` | `6916272c6ffd02a0d191124e19baf7e4d798af6eb67e4cb01a78271bdd134a77` | IDENTICAL |
| 578 | `methods/aris-vendor/skills/skills-codex-gemini-review/auto-paper-improvement-loop/SKILL.md` | `6f2afe3f6c2ed9f0fde09ee2039bc54644706f8eaf6761a6cee4d1df6164a845` | `6f2afe3f6c2ed9f0fde09ee2039bc54644706f8eaf6761a6cee4d1df6164a845` | IDENTICAL |
| 579 | `methods/aris-vendor/skills/skills-codex-gemini-review/auto-review-loop/SKILL.md` | `ec08e64e9ee22538204e164627583d0b3738335c47d660c5ddd7c71d4e410417` | `ec08e64e9ee22538204e164627583d0b3738335c47d660c5ddd7c71d4e410417` | IDENTICAL |
| 580 | `methods/aris-vendor/skills/skills-codex-gemini-review/grant-proposal/SKILL.md` | `8e834ea2ce5fc82591140bf57d7a723a5e74b6232039fb793fe3d9f8a025a72c` | `8e834ea2ce5fc82591140bf57d7a723a5e74b6232039fb793fe3d9f8a025a72c` | IDENTICAL |
| 581 | `methods/aris-vendor/skills/skills-codex-gemini-review/idea-creator/SKILL.md` | `80174ad9cff8e92b0f6c2d11f9ba14fd8b986f55c54807ad1e61bd61eb80d50c` | `80174ad9cff8e92b0f6c2d11f9ba14fd8b986f55c54807ad1e61bd61eb80d50c` | IDENTICAL |
| 582 | `methods/aris-vendor/skills/skills-codex-gemini-review/idea-discovery-robot/SKILL.md` | `dd0e7f33bff7b7a16fd4fca3bca1b475e3acd7ce24de68af6fdd20ad778c7e29` | `dd0e7f33bff7b7a16fd4fca3bca1b475e3acd7ce24de68af6fdd20ad778c7e29` | IDENTICAL |
| 583 | `methods/aris-vendor/skills/skills-codex-gemini-review/idea-discovery/SKILL.md` | `1250df2ee2521c0a28960ec28c6a05714dc775a2e415cc4910b7529c47323d84` | `1250df2ee2521c0a28960ec28c6a05714dc775a2e415cc4910b7529c47323d84` | IDENTICAL |
| 584 | `methods/aris-vendor/skills/skills-codex-gemini-review/novelty-check/SKILL.md` | `60ac7cc93f9e94082038f54375295b213483ee80cc16b26fd35f78426776468f` | `60ac7cc93f9e94082038f54375295b213483ee80cc16b26fd35f78426776468f` | IDENTICAL |
| 585 | `methods/aris-vendor/skills/skills-codex-gemini-review/paper-figure/SKILL.md` | `5dc702aa809cf4a53f906167f292643fb76748ee66998aa4da3e1e945ee134d2` | `5dc702aa809cf4a53f906167f292643fb76748ee66998aa4da3e1e945ee134d2` | IDENTICAL |
| 586 | `methods/aris-vendor/skills/skills-codex-gemini-review/paper-plan/SKILL.md` | `74cb50a2ca3f09611eb557af7d10b4511ecb6762535366178d8f925599e44a38` | `74cb50a2ca3f09611eb557af7d10b4511ecb6762535366178d8f925599e44a38` | IDENTICAL |
| 587 | `methods/aris-vendor/skills/skills-codex-gemini-review/paper-poster-html/SKILL.md` | `618fa29802098c59bcb3ad449b2db00b50f7f72bf09343b443809664e527bac3` | `618fa29802098c59bcb3ad449b2db00b50f7f72bf09343b443809664e527bac3` | IDENTICAL |
| 588 | `methods/aris-vendor/skills/skills-codex-gemini-review/paper-slides/SKILL.md` | `3cca23fa611bacd9c0838de2eed702a320163a429e90079227f6387bc5c8fdd4` | `3cca23fa611bacd9c0838de2eed702a320163a429e90079227f6387bc5c8fdd4` | IDENTICAL |
| 589 | `methods/aris-vendor/skills/skills-codex-gemini-review/paper-write/SKILL.md` | `7db054a1708b1b9c014968953954771a8cc817439543238ac439414acd101f38` | `7db054a1708b1b9c014968953954771a8cc817439543238ac439414acd101f38` | IDENTICAL |
| 590 | `methods/aris-vendor/skills/skills-codex-gemini-review/paper-writing/SKILL.md` | `9d6a394798ee3fa513b9a89a9eba14cf87d030dc3284d63a149f22998ed6c256` | `9d6a394798ee3fa513b9a89a9eba14cf87d030dc3284d63a149f22998ed6c256` | IDENTICAL |
| 591 | `methods/aris-vendor/skills/skills-codex-gemini-review/research-refine/SKILL.md` | `e70c912082ebe40709b3684e254e823e61536a992d50694ae1a7c7a6e8982772` | `e70c912082ebe40709b3684e254e823e61536a992d50694ae1a7c7a6e8982772` | IDENTICAL |
| 592 | `methods/aris-vendor/skills/skills-codex-gemini-review/research-review/SKILL.md` | `4164b014f49264e7bed6943f959f249b154dca647e02a63cf8a918d664434273` | `4164b014f49264e7bed6943f959f249b154dca647e02a63cf8a918d664434273` | IDENTICAL |
| 593 | `methods/aris-vendor/skills/skills-codex/README.md` | `dc01a42bca415c2e3d3b25f14625a50d80bff804a485633b86ba1b63e59b16e6` | `dc01a42bca415c2e3d3b25f14625a50d80bff804a485633b86ba1b63e59b16e6` | IDENTICAL |
| 594 | `methods/aris-vendor/skills/skills-codex/README_CN.md` | `b474f5198d5149c33a9294b4a3b24196d0b43062cdff18664d586cc1e050ee90` | `b474f5198d5149c33a9294b4a3b24196d0b43062cdff18664d586cc1e050ee90` | IDENTICAL |
| 595 | `methods/aris-vendor/skills/skills-codex/ablation-planner/SKILL.md` | `be8086de1e8f902f1bca51c57288872672c0295608314578667f652a74435110` | `be8086de1e8f902f1bca51c57288872672c0295608314578667f652a74435110` | IDENTICAL |
| 596 | `methods/aris-vendor/skills/skills-codex/alphaxiv/SKILL.md` | `f0e6a3994f683209835f8ff5e30f1a6ae1298d14113050406673d0a48a795784` | `f0e6a3994f683209835f8ff5e30f1a6ae1298d14113050406673d0a48a795784` | IDENTICAL |
| 597 | `methods/aris-vendor/skills/skills-codex/analyze-results/SKILL.md` | `1a5f798558018fe6c8faa8b9997ac4cd1076aceb73cfb5bdc261e5de5727f7e2` | `1a5f798558018fe6c8faa8b9997ac4cd1076aceb73cfb5bdc261e5de5727f7e2` | IDENTICAL |
| 598 | `methods/aris-vendor/skills/skills-codex/arxiv/SKILL.md` | `f984dc04545e7cab0781fc518e9bc7ed5121175cac15a53707e8fc5bbd97c95f` | `f984dc04545e7cab0781fc518e9bc7ed5121175cac15a53707e8fc5bbd97c95f` | IDENTICAL |
| 599 | `methods/aris-vendor/skills/skills-codex/auto-paper-improvement-loop/SKILL.md` | `ccb8f4c615165e9810b3755d0a7f7ef61ff54a24002f0a3312c10366aa63d16f` | `ccb8f4c615165e9810b3755d0a7f7ef61ff54a24002f0a3312c10366aa63d16f` | IDENTICAL |
| 600 | `methods/aris-vendor/skills/skills-codex/auto-review-loop-llm/SKILL.md` | `6ba0c18e04f8171803ddbd7748873e135234db27175639fbad31b0f9ed0f6440` | `6ba0c18e04f8171803ddbd7748873e135234db27175639fbad31b0f9ed0f6440` | IDENTICAL |
| 601 | `methods/aris-vendor/skills/skills-codex/auto-review-loop-minimax/SKILL.md` | `a6f768b079f1ef3f9531167c4557a09cef64aae69518ee557317263fd2c8bc33` | `a6f768b079f1ef3f9531167c4557a09cef64aae69518ee557317263fd2c8bc33` | IDENTICAL |
| 602 | `methods/aris-vendor/skills/skills-codex/auto-review-loop/SKILL.md` | `a469fa702650eb103ecd2b2d3197e26c9c9f351e6a5031e75e0b50ec5d125797` | `a469fa702650eb103ecd2b2d3197e26c9c9f351e6a5031e75e0b50ec5d125797` | IDENTICAL |
| 603 | `methods/aris-vendor/skills/skills-codex/citation-audit/SKILL.md` | `e8727396043b28151ce57555cee8d6760214006b5004cca7d17ebbac0ae77d55` | `e8727396043b28151ce57555cee8d6760214006b5004cca7d17ebbac0ae77d55` | IDENTICAL |
| 604 | `methods/aris-vendor/skills/skills-codex/claims-drafting/SKILL.md` | `f950328646695ccc066c87d4eb176ee7f505d0c4d008220457e80a3362c34f02` | `f950328646695ccc066c87d4eb176ee7f505d0c4d008220457e80a3362c34f02` | IDENTICAL |
| 605 | `methods/aris-vendor/skills/skills-codex/comm-lit-review/SKILL.md` | `f8f46536c2e0b3e34fa633b617cb407ded580dcc3ee29f8f14daef21e92f1909` | `f8f46536c2e0b3e34fa633b617cb407ded580dcc3ee29f8f14daef21e92f1909` | IDENTICAL |
| 606 | `methods/aris-vendor/skills/skills-codex/comm-lit-review/references/domain-taxonomy.md` | `fe60f6da0a53df9cfe24a9490967c0fe501852601c41db1e44ac3b5170a2cbc8` | `fe60f6da0a53df9cfe24a9490967c0fe501852601c41db1e44ac3b5170a2cbc8` | IDENTICAL |
| 607 | `methods/aris-vendor/skills/skills-codex/comm-lit-review/references/output-template.md` | `a189d60a9c5f439d995a7a6ee9a2ea9989096e98fe6cac61fc49bedcb560c864` | `a189d60a9c5f439d995a7a6ee9a2ea9989096e98fe6cac61fc49bedcb560c864` | IDENTICAL |
| 608 | `methods/aris-vendor/skills/skills-codex/comm-lit-review/references/source-policy.md` | `36db0b748275c7a1e1502a1de7f1ad6f4d08889891467811f63684bc92026f20` | `36db0b748275c7a1e1502a1de7f1ad6f4d08889891467811f63684bc92026f20` | IDENTICAL |
| 609 | `methods/aris-vendor/skills/skills-codex/comm-lit-review/references/venue-tiering.md` | `44568b391ceb668f5eb425f6f9ee631ac6f6b99ea27c2d59e2a84a76a98e608a` | `44568b391ceb668f5eb425f6f9ee631ac6f6b99ea27c2d59e2a84a76a98e608a` | IDENTICAL |
| 610 | `methods/aris-vendor/skills/skills-codex/deepxiv/SKILL.md` | `30f94ac2fff16a839c2bda505980b59a26bf0069d426f319f695459a636298f1` | `30f94ac2fff16a839c2bda505980b59a26bf0069d426f319f695459a636298f1` | IDENTICAL |
| 611 | `methods/aris-vendor/skills/skills-codex/dse-loop/SKILL.md` | `daf99d22d3fd955ca197cfc79bc3dc999e6283018f84be8887fe2f3465f74f68` | `daf99d22d3fd955ca197cfc79bc3dc999e6283018f84be8887fe2f3465f74f68` | IDENTICAL |
| 612 | `methods/aris-vendor/skills/skills-codex/embodiment-description/SKILL.md` | `8833b4569435077554d51ac59f79c8b4ceca64b777f129b1e8eaa328be9bb9a2` | `8833b4569435077554d51ac59f79c8b4ceca64b777f129b1e8eaa328be9bb9a2` | IDENTICAL |
| 613 | `methods/aris-vendor/skills/skills-codex/exa-search/SKILL.md` | `bb3ec11445ad13e897f891bf0873fa634ced9532de01e4542c342dc2c4ba4edb` | `bb3ec11445ad13e897f891bf0873fa634ced9532de01e4542c342dc2c4ba4edb` | IDENTICAL |
| 614 | `methods/aris-vendor/skills/skills-codex/experiment-audit/SKILL.md` | `ea9c8e6e5b497dbb9611d209ea6e6a714b5ac023f94cba39d6a301963462d1c5` | `ea9c8e6e5b497dbb9611d209ea6e6a714b5ac023f94cba39d6a301963462d1c5` | IDENTICAL |
| 615 | `methods/aris-vendor/skills/skills-codex/experiment-bridge/SKILL.md` | `596b342d256af1596e6b8b09d6225bd09956f2cd1cd9fc5931b790bae4e59c0a` | `596b342d256af1596e6b8b09d6225bd09956f2cd1cd9fc5931b790bae4e59c0a` | IDENTICAL |
| 616 | `methods/aris-vendor/skills/skills-codex/experiment-plan/SKILL.md` | `61812df053fd8717cccb248fcabec3863f930eaedba03463bc059294dcc3863a` | `61812df053fd8717cccb248fcabec3863f930eaedba03463bc059294dcc3863a` | IDENTICAL |
| 617 | `methods/aris-vendor/skills/skills-codex/experiment-queue/SKILL.md` | `3a66fbd5f7684d3279bb91eb5d4ec64245f86da3ba507a7b60e357c7d8dfd00f` | `3a66fbd5f7684d3279bb91eb5d4ec64245f86da3ba507a7b60e357c7d8dfd00f` | IDENTICAL |
| 618 | `methods/aris-vendor/skills/skills-codex/feishu-notify/SKILL.md` | `12ba4c282e594a269c4cb28e89a6202a128370ca7bb016a396f3feb118492e4d` | `12ba4c282e594a269c4cb28e89a6202a128370ca7bb016a396f3feb118492e4d` | IDENTICAL |
| 619 | `methods/aris-vendor/skills/skills-codex/figure-description/SKILL.md` | `4c69bc650a67d1688f44c909c49be98ffe74ea427b3859edb3c3357ec5730136` | `4c69bc650a67d1688f44c909c49be98ffe74ea427b3859edb3c3357ec5730136` | IDENTICAL |
| 620 | `methods/aris-vendor/skills/skills-codex/figure-spec/SKILL.md` | `f7f69413608eeeb7670800579e119b1b0f1e63881300d4977fc3a0e9b148c76d` | `f7f69413608eeeb7670800579e119b1b0f1e63881300d4977fc3a0e9b148c76d` | IDENTICAL |
| 621 | `methods/aris-vendor/skills/skills-codex/formula-derivation/SKILL.md` | `2e5f5ce665023cdc460126c9c8403503c17961145a2b052d25200f9bbd9a9b4d` | `2e5f5ce665023cdc460126c9c8403503c17961145a2b052d25200f9bbd9a9b4d` | IDENTICAL |
| 622 | `methods/aris-vendor/skills/skills-codex/gemini-search/SKILL.md` | `7672efc2601561fb0c08410bb1d82a2e27461e070aaa93c3cde9eb57be95f4d7` | `7672efc2601561fb0c08410bb1d82a2e27461e070aaa93c3cde9eb57be95f4d7` | IDENTICAL |
| 623 | `methods/aris-vendor/skills/skills-codex/grant-proposal/SKILL.md` | `81971ba7e6f49bbbc6d8930dd2acec9bbb258fce29740077763e9079bb5fac35` | `81971ba7e6f49bbbc6d8930dd2acec9bbb258fce29740077763e9079bb5fac35` | IDENTICAL |
| 624 | `methods/aris-vendor/skills/skills-codex/idea-creator/SKILL.md` | `66e9444411ae6baa79f7511133e8997b00238624eb59683fb58a25783f0443d4` | `66e9444411ae6baa79f7511133e8997b00238624eb59683fb58a25783f0443d4` | IDENTICAL |
| 625 | `methods/aris-vendor/skills/skills-codex/idea-discovery-robot/SKILL.md` | `227069a6b137fbc886c76ea9191cbbae9ad7c4210bf392c566f5fd8d038a746e` | `227069a6b137fbc886c76ea9191cbbae9ad7c4210bf392c566f5fd8d038a746e` | IDENTICAL |
| 626 | `methods/aris-vendor/skills/skills-codex/idea-discovery/SKILL.md` | `d7b67f75a0499cc15e2e618faf944785c6a21ae40b204072b1e6d5a09be4f296` | `d7b67f75a0499cc15e2e618faf944785c6a21ae40b204072b1e6d5a09be4f296` | IDENTICAL |
| 627 | `methods/aris-vendor/skills/skills-codex/integrity-forensics/SKILL.md` | `00a1e7e2d187791213d4190b8c88a91e7607654a51bc3855357038b212ebcad6` | `00a1e7e2d187791213d4190b8c88a91e7607654a51bc3855357038b212ebcad6` | IDENTICAL |
| 628 | `methods/aris-vendor/skills/skills-codex/interview-cheatsheet/SKILL.md` | `87c32abd9043412d48de5cbada26a6584771a414515855b45de34fd21b9d4fab` | `87c32abd9043412d48de5cbada26a6584771a414515855b45de34fd21b9d4fab` | IDENTICAL |
| 629 | `methods/aris-vendor/skills/skills-codex/invention-structuring/SKILL.md` | `f8a259d92bba82f5a47f196543fcc25c567d9ec9b94782c1fe9ee57141f9cad8` | `f8a259d92bba82f5a47f196543fcc25c567d9ec9b94782c1fe9ee57141f9cad8` | IDENTICAL |
| 630 | `methods/aris-vendor/skills/skills-codex/jurisdiction-format/SKILL.md` | `7683f58c4ad6465b4c4dd4f360876b12b0132777ca4ba40c1e48b777f4b40bb9` | `7683f58c4ad6465b4c4dd4f360876b12b0132777ca4ba40c1e48b777f4b40bb9` | IDENTICAL |
| 631 | `methods/aris-vendor/skills/skills-codex/kill-argument/SKILL.md` | `20f88e07ee5d674c4484f1287ba4285bce85723dd45493fbb294a9bbc393b55a` | `20f88e07ee5d674c4484f1287ba4285bce85723dd45493fbb294a9bbc393b55a` | IDENTICAL |
| 632 | `methods/aris-vendor/skills/skills-codex/mermaid-diagram/SKILL.md` | `2d9eab0a8b1cc94e43799171287ed85455d8cfa2b75d4f19269bad168d8bb1dd` | `2d9eab0a8b1cc94e43799171287ed85455d8cfa2b75d4f19269bad168d8bb1dd` | IDENTICAL |
| 633 | `methods/aris-vendor/skills/skills-codex/meta-apply/SKILL.md` | `8231da1aae4bc3297477c167044eeb9bfc7bc0e17ac03f6225508fc588e80ff7` | `8231da1aae4bc3297477c167044eeb9bfc7bc0e17ac03f6225508fc588e80ff7` | IDENTICAL |
| 634 | `methods/aris-vendor/skills/skills-codex/meta-optimize/SKILL.md` | `bf57bb6dac5baaaeac823e8130bb53653145531eb0ad67ac8ee9220b29feb515` | `bf57bb6dac5baaaeac823e8130bb53653145531eb0ad67ac8ee9220b29feb515` | IDENTICAL |
| 635 | `methods/aris-vendor/skills/skills-codex/monitor-experiment/SKILL.md` | `66a42b21a7ec5a9c4ee2d4da6babfd533764d6c4188dcc178d5bcbd1d8a31072` | `66a42b21a7ec5a9c4ee2d4da6babfd533764d6c4188dcc178d5bcbd1d8a31072` | IDENTICAL |
| 636 | `methods/aris-vendor/skills/skills-codex/novelty-check/SKILL.md` | `998e801ab4d5dedabf643364680befe05023f4b819f44734db6ad67c2128b801` | `998e801ab4d5dedabf643364680befe05023f4b819f44734db6ad67c2128b801` | IDENTICAL |
| 637 | `methods/aris-vendor/skills/skills-codex/openalex/SKILL.md` | `6af90a676a2e3a27b896258f2855931c2bf31ca259d135d45dc61ab1cea05dd6` | `6af90a676a2e3a27b896258f2855931c2bf31ca259d135d45dc61ab1cea05dd6` | IDENTICAL |
| 638 | `methods/aris-vendor/skills/skills-codex/overleaf-sync/SKILL.md` | `15644b418d9d043ac1f66e03242a9f8ecebc63569fc0a43f913252f3bfb2abe7` | `15644b418d9d043ac1f66e03242a9f8ecebc63569fc0a43f913252f3bfb2abe7` | IDENTICAL |
| 639 | `methods/aris-vendor/skills/skills-codex/paper-claim-audit/SKILL.md` | `8860aa3f50e72f6549ab6f0b5464242d76eaed719361f7e2e5aa9730895a8533` | `8860aa3f50e72f6549ab6f0b5464242d76eaed719361f7e2e5aa9730895a8533` | IDENTICAL |
| 640 | `methods/aris-vendor/skills/skills-codex/paper-compile/SKILL.md` | `c2467ad7b4c915d6e3d51b975d60d2626cc1da58f3b202fc03b753907f737b0c` | `c2467ad7b4c915d6e3d51b975d60d2626cc1da58f3b202fc03b753907f737b0c` | IDENTICAL |
| 641 | `methods/aris-vendor/skills/skills-codex/paper-figure/SKILL.md` | `f010f03366a89bce3fba6c07c6c9d1c831f16fb1ce946d1eb678eb3518c94c07` | `f010f03366a89bce3fba6c07c6c9d1c831f16fb1ce946d1eb678eb3518c94c07` | IDENTICAL |
| 642 | `methods/aris-vendor/skills/skills-codex/paper-illustration-image2/SKILL.md` | `ed99bfb0e1a98b3acf17d00178bb03e4e5d8775ab737141a6b59a0549765a726` | `ed99bfb0e1a98b3acf17d00178bb03e4e5d8775ab737141a6b59a0549765a726` | IDENTICAL |
| 643 | `methods/aris-vendor/skills/skills-codex/paper-illustration-image2/scripts/paper_illustration_image2.py` | `bc97f5b1ae14ffaff10c24240b6e93f3c1282ffd340d4756ea80477649f32890` | `bc97f5b1ae14ffaff10c24240b6e93f3c1282ffd340d4756ea80477649f32890` | IDENTICAL |
| 644 | `methods/aris-vendor/skills/skills-codex/paper-illustration/SKILL.md` | `1c876e39d880781bc5d6f51c616e02f4e5858750867f027968d5b91564179643` | `1c876e39d880781bc5d6f51c616e02f4e5858750867f027968d5b91564179643` | IDENTICAL |
| 645 | `methods/aris-vendor/skills/skills-codex/paper-plan/SKILL.md` | `2a7fdeb649357a423dfa3b0e87a4356639c247c7075babb59e30664c4dde6a6b` | `2a7fdeb649357a423dfa3b0e87a4356639c247c7075babb59e30664c4dde6a6b` | IDENTICAL |
| 646 | `methods/aris-vendor/skills/skills-codex/paper-poster-html/SKILL.md` | `7d9e3dfce9f84e037718c48909a438916adfa178043eea546e5caea213111cfe` | `7d9e3dfce9f84e037718c48909a438916adfa178043eea546e5caea213111cfe` | IDENTICAL |
| 647 | `methods/aris-vendor/skills/skills-codex/paper-poster/SKILL.md` | `fea8d7e3f4a07d0be9b43d4e7964b989074a26e858d11027e8ed34f8c3be70cb` | `fea8d7e3f4a07d0be9b43d4e7964b989074a26e858d11027e8ed34f8c3be70cb` | IDENTICAL |
| 648 | `methods/aris-vendor/skills/skills-codex/paper-slides/SKILL.md` | `19f19bcec2a015c48fd725e2fc8ee224e1c589bdf0350af288cb2df7df13c90b` | `19f19bcec2a015c48fd725e2fc8ee224e1c589bdf0350af288cb2df7df13c90b` | IDENTICAL |
| 649 | `methods/aris-vendor/skills/skills-codex/paper-talk/SKILL.md` | `5d55889df72fef0f1f9c11057d82e1200a33ea7ba8d54163fef413b0f5e08c4a` | `5d55889df72fef0f1f9c11057d82e1200a33ea7ba8d54163fef413b0f5e08c4a` | IDENTICAL |
| 650 | `methods/aris-vendor/skills/skills-codex/paper-write/SKILL.md` | `55d17812945859c74b4f077833d8ecbf426fc987f715e6354bf5d0effc23fec0` | `55d17812945859c74b4f077833d8ecbf426fc987f715e6354bf5d0effc23fec0` | IDENTICAL |
| 651 | `methods/aris-vendor/skills/skills-codex/paper-write/templates/IEEEtran.bst` | `314f0ece704568faf827011bac498650691b2b5ee06320720830e782416d5a5f` | `314f0ece704568faf827011bac498650691b2b5ee06320720830e782416d5a5f` | IDENTICAL |
| 652 | `methods/aris-vendor/skills/skills-codex/paper-write/templates/IEEEtran.cls` | `da751920a317ed318b7b5cd7fa585a6cc7d28502d457856382e9be24b10a3bd7` | `da751920a317ed318b7b5cd7fa585a6cc7d28502d457856382e9be24b10a3bd7` | IDENTICAL |
| 653 | `methods/aris-vendor/skills/skills-codex/paper-write/templates/aaai2026.bst` | `ac26e2c66047435c0ed25f21ae36ad42d731cf3d794c4a8b5f05a62141a27294` | `ac26e2c66047435c0ed25f21ae36ad42d731cf3d794c4a8b5f05a62141a27294` | IDENTICAL |
| 654 | `methods/aris-vendor/skills/skills-codex/paper-write/templates/aaai2026.sty` | `a39f1866a04dd1e2603613c876fa446aaea2c2f3e34d02be868fd21520bfade5` | `a39f1866a04dd1e2603613c876fa446aaea2c2f3e34d02be868fd21520bfade5` | IDENTICAL |
| 655 | `methods/aris-vendor/skills/skills-codex/paper-write/templates/aaai2026.tex` | `bed12c50b5e027fd88097d238ec4e7ebf1ae7b450cb06d6df7c8ae126a620aea` | `bed12c50b5e027fd88097d238ec4e7ebf1ae7b450cb06d6df7c8ae126a620aea` | IDENTICAL |
| 656 | `methods/aris-vendor/skills/skills-codex/paper-write/templates/acl.sty` | `19dfeddc2c0e448f3926a0bef048a9db3f3611b46265b760caabd7ada4f361de` | `19dfeddc2c0e448f3926a0bef048a9db3f3611b46265b760caabd7ada4f361de` | IDENTICAL |
| 657 | `methods/aris-vendor/skills/skills-codex/paper-write/templates/acl2026.tex` | `339c9ee9705c1767d44ef24b85365c0bb8619ecc3fcf66172bf1356292389614` | `339c9ee9705c1767d44ef24b85365c0bb8619ecc3fcf66172bf1356292389614` | IDENTICAL |
| 658 | `methods/aris-vendor/skills/skills-codex/paper-write/templates/acl_natbib.bst` | `e332fd51dcea48e2a8a89754892c3cb99674a1cd70b527b661e9aaffc235e83c` | `e332fd51dcea48e2a8a89754892c3cb99674a1cd70b527b661e9aaffc235e83c` | IDENTICAL |
| 659 | `methods/aris-vendor/skills/skills-codex/paper-write/templates/acm.bst` | `ecbc9bfbf595d820dcc271d1bada20448c6eb5a6cf4d57de8dc4ed2608d5f23f` | `ecbc9bfbf595d820dcc271d1bada20448c6eb5a6cf4d57de8dc4ed2608d5f23f` | IDENTICAL |
| 660 | `methods/aris-vendor/skills/skills-codex/paper-write/templates/acm_mm2026.tex` | `c350a3f470e8f356f8697040f204fb28d168b671aed67465a71a938f844d1ce0` | `c350a3f470e8f356f8697040f204fb28d168b671aed67465a71a938f844d1ce0` | IDENTICAL |
| 661 | `methods/aris-vendor/skills/skills-codex/paper-write/templates/acmart.cls` | `560afeefdb1834d8b04556ec52e3abe60e7f23eed501b5b751c7b8215b626d34` | `560afeefdb1834d8b04556ec52e3abe60e7f23eed501b5b751c7b8215b626d34` | IDENTICAL |
| 662 | `methods/aris-vendor/skills/skills-codex/paper-write/templates/cvpr.bst` | `e38e6166bd7b1e6d23a1b79dcdb55c656e4fcdbe91bdf6b50d827e6b5d1aacfc` | `e38e6166bd7b1e6d23a1b79dcdb55c656e4fcdbe91bdf6b50d827e6b5d1aacfc` | IDENTICAL |
| 663 | `methods/aris-vendor/skills/skills-codex/paper-write/templates/cvpr.sty` | `2602473285d1a7df2a445ac89b76e1afa0acab78e056f0369d19770245190153` | `2602473285d1a7df2a445ac89b76e1afa0acab78e056f0369d19770245190153` | IDENTICAL |
| 664 | `methods/aris-vendor/skills/skills-codex/paper-write/templates/cvpr2026.tex` | `251329b8a7ea25f1ba0f5a769f652235e13bc1f43b3e8b1d892e16a005b361f0` | `251329b8a7ea25f1ba0f5a769f652235e13bc1f43b3e8b1d892e16a005b361f0` | IDENTICAL |
| 665 | `methods/aris-vendor/skills/skills-codex/paper-write/templates/iclr2026.tex` | `1e4c20b3c5b7445966194151d33c3e2023e828e621be8baf7ffb234b987cfc23` | `1e4c20b3c5b7445966194151d33c3e2023e828e621be8baf7ffb234b987cfc23` | IDENTICAL |
| 666 | `methods/aris-vendor/skills/skills-codex/paper-write/templates/iclr2026_conference.bst` | `2d67552db7ed38ccfccb5957b52f95656e25c249724761d3cf5f7922ad1844c5` | `2d67552db7ed38ccfccb5957b52f95656e25c249724761d3cf5f7922ad1844c5` | IDENTICAL |
| 667 | `methods/aris-vendor/skills/skills-codex/paper-write/templates/iclr2026_conference.sty` | `a4852f68e080d6c5245057ca2039100b409e31727898aa93c03d78ddb84374a3` | `a4852f68e080d6c5245057ca2039100b409e31727898aa93c03d78ddb84374a3` | IDENTICAL |
| 668 | `methods/aris-vendor/skills/skills-codex/paper-write/templates/icml2026.sty` | `7cdcf90f6a59c5219e7f15c88f7ed09fcaf598dad91e6cdddc4dc3cb0e397a95` | `7cdcf90f6a59c5219e7f15c88f7ed09fcaf598dad91e6cdddc4dc3cb0e397a95` | IDENTICAL |
| 669 | `methods/aris-vendor/skills/skills-codex/paper-write/templates/icml2026.tex` | `c2ca8140bf255d1ff77d1278eb3eefed4018b4b1e71065b8e1ccbc68b74c8acf` | `c2ca8140bf255d1ff77d1278eb3eefed4018b4b1e71065b8e1ccbc68b74c8acf` | IDENTICAL |
| 670 | `methods/aris-vendor/skills/skills-codex/paper-write/templates/ieee_conference.tex` | `a3dc3a175a7dd1512f4a2fdb844a0a482a9e919162e37dc27373d501fbafafbc` | `a3dc3a175a7dd1512f4a2fdb844a0a482a9e919162e37dc27373d501fbafafbc` | IDENTICAL |
| 671 | `methods/aris-vendor/skills/skills-codex/paper-write/templates/ieee_journal.tex` | `bdff7ff0aa376d8a46675bdb6e96c4dd715463360735706aa5fbaa5f834b7604` | `bdff7ff0aa376d8a46675bdb6e96c4dd715463360735706aa5fbaa5f834b7604` | IDENTICAL |
| 672 | `methods/aris-vendor/skills/skills-codex/paper-write/templates/math_commands.tex` | `3efe4556b2c33b4a93c1b6e86b99b9a3ecbd9c9565ccc06bf8a1f51293470dc6` | `3efe4556b2c33b4a93c1b6e86b99b9a3ecbd9c9565ccc06bf8a1f51293470dc6` | IDENTICAL |
| 673 | `methods/aris-vendor/skills/skills-codex/paper-write/templates/neurips2026.tex` | `d436d14ee70d6a1ee821f6239d2d45a544059fbd186d2431c69d0cbddcf0790d` | `d436d14ee70d6a1ee821f6239d2d45a544059fbd186d2431c69d0cbddcf0790d` | IDENTICAL |
| 674 | `methods/aris-vendor/skills/skills-codex/paper-write/templates/neurips_2026.sty` | `0c1ad36961fcd9198dcc2558cf2793e1df39973bde8264fd701f5e7970672757` | `0c1ad36961fcd9198dcc2558cf2793e1df39973bde8264fd701f5e7970672757` | IDENTICAL |
| 675 | `methods/aris-vendor/skills/skills-codex/paper-writing/SKILL.md` | `a07684e624255afe46a0a5752d9864bd07e18b2b6d9c0297b3d12c71c9f0b954` | `a07684e624255afe46a0a5752d9864bd07e18b2b6d9c0297b3d12c71c9f0b954` | IDENTICAL |
| 676 | `methods/aris-vendor/skills/skills-codex/patent-novelty-check/SKILL.md` | `66519de4c8c4bc84a0566127aacd05262e43e462ae1999b66c5c40fcccda2984` | `66519de4c8c4bc84a0566127aacd05262e43e462ae1999b66c5c40fcccda2984` | IDENTICAL |
| 677 | `methods/aris-vendor/skills/skills-codex/patent-pipeline/SKILL.md` | `2f499d528e626c4833f18bb766c36a0e573cad7e7d757ef75dbd5be83695e4af` | `2f499d528e626c4833f18bb766c36a0e573cad7e7d757ef75dbd5be83695e4af` | IDENTICAL |
| 678 | `methods/aris-vendor/skills/skills-codex/patent-review/SKILL.md` | `dd202a6d499f809cf286d24b54cddc3bf757bdbfb9fde6e9a080f21adb02950e` | `dd202a6d499f809cf286d24b54cddc3bf757bdbfb9fde6e9a080f21adb02950e` | IDENTICAL |
| 679 | `methods/aris-vendor/skills/skills-codex/pixel-art/SKILL.md` | `96ccea96d27140be68dd934e6af1d0d576450226152e1d20df6f9d3dc5b0ef23` | `96ccea96d27140be68dd934e6af1d0d576450226152e1d20df6f9d3dc5b0ef23` | IDENTICAL |
| 680 | `methods/aris-vendor/skills/skills-codex/prior-art-search/SKILL.md` | `8793fb26c522de4c44a64b68df81e5d12718a99866c639658261cea680bd58b2` | `8793fb26c522de4c44a64b68df81e5d12718a99866c639658261cea680bd58b2` | IDENTICAL |
| 681 | `methods/aris-vendor/skills/skills-codex/proof-checker/SKILL.md` | `3d3e5b22a0d3668243ab9d3c789b62dc2304fcefbf72cfe7d1cb831ffeec235a` | `3d3e5b22a0d3668243ab9d3c789b62dc2304fcefbf72cfe7d1cb831ffeec235a` | IDENTICAL |
| 682 | `methods/aris-vendor/skills/skills-codex/proof-orchestrator/SKILL.md` | `f29f1d6bc03130523ade30a64a8a6a966601e17eef77f27163373e874ce9f682` | `f29f1d6bc03130523ade30a64a8a6a966601e17eef77f27163373e874ce9f682` | IDENTICAL |
| 683 | `methods/aris-vendor/skills/skills-codex/proof-orchestrator/references/audit-output-contract.md` | `cff8da1ef42794c64aba244decb19895b97ae912651e023c5c0b54a110e3eb7e` | `cff8da1ef42794c64aba244decb19895b97ae912651e023c5c0b54a110e3eb7e` | IDENTICAL |
| 684 | `methods/aris-vendor/skills/skills-codex/proof-orchestrator/references/deepseek-routing.md` | `a1631bc28ba78adb79154c2f07b76c82c9204f8d307952b28056b0f215449753` | `a1631bc28ba78adb79154c2f07b76c82c9204f8d307952b28056b0f215449753` | IDENTICAL |
| 685 | `methods/aris-vendor/skills/skills-codex/proof-orchestrator/references/dispatch-prompts.md` | `21f0f279dd24f98cf9eaa5ce21754299f88cdc8eac77874c2bfe6b12a8f6c7eb` | `21f0f279dd24f98cf9eaa5ce21754299f88cdc8eac77874c2bfe6b12a8f6c7eb` | IDENTICAL |
| 686 | `methods/aris-vendor/skills/skills-codex/proof-orchestrator/references/notation-audit.md` | `8db3079a9209d9c71b977d448cff1abe33c5cf6414b1923735c813c9fc56e757` | `8db3079a9209d9c71b977d448cff1abe33c5cf6414b1923735c813c9fc56e757` | IDENTICAL |
| 687 | `methods/aris-vendor/skills/skills-codex/proof-orchestrator/references/proof-audit-rubric.md` | `fb962314da5291f5376da55f502f94a9337f380b481cf12208d6b586341b86bf` | `fb962314da5291f5376da55f502f94a9337f380b481cf12208d6b586341b86bf` | IDENTICAL |
| 688 | `methods/aris-vendor/skills/skills-codex/proof-orchestrator/references/stress-tests.md` | `93c4c054f14dfe6acce9f1d1f2d5a70a71a2b32ac96d1988f6136d557e01067a` | `93c4c054f14dfe6acce9f1d1f2d5a70a71a2b32ac96d1988f6136d557e01067a` | IDENTICAL |
| 689 | `methods/aris-vendor/skills/skills-codex/proof-writer/SKILL.md` | `bef68a5cb664e212f299667773f6367b90ad3447b68cacc399186655fb02f9f8` | `bef68a5cb664e212f299667773f6367b90ad3447b68cacc399186655fb02f9f8` | IDENTICAL |
| 690 | `methods/aris-vendor/skills/skills-codex/qzcli/SKILL.md` | `328953e6e4a21f8a38e979f9729818721af387724b799cb7cc96e072d0012d2f` | `328953e6e4a21f8a38e979f9729818721af387724b799cb7cc96e072d0012d2f` | IDENTICAL |
| 691 | `methods/aris-vendor/skills/skills-codex/rebuttal/SKILL.md` | `a3da910783e74fce6508d03d8a6b3a7f4dc859a0975daf2d5032fe8635cc3f08` | `a3da910783e74fce6508d03d8a6b3a7f4dc859a0975daf2d5032fe8635cc3f08` | IDENTICAL |
| 692 | `methods/aris-vendor/skills/skills-codex/render-html/SKILL.md` | `b75a1856c1227c8e5be1c98e4b6d0665e52f3320f4d2493d2065d1b1810bad8c` | `b75a1856c1227c8e5be1c98e4b6d0665e52f3320f4d2493d2065d1b1810bad8c` | IDENTICAL |
| 693 | `methods/aris-vendor/skills/skills-codex/render-html/scripts/render_html.py` | `25d04ffbb1c2d4de61c4016578390477080168275a093d3569a43e14758e5694` | `25d04ffbb1c2d4de61c4016578390477080168275a093d3569a43e14758e5694` | IDENTICAL |
| 694 | `methods/aris-vendor/skills/skills-codex/render-html/scripts/templates/academic.html` | `0ce224f68f320252e05696bc865050b3794d8e8c6f7163f17c663b4e6814a545` | `0ce224f68f320252e05696bc865050b3794d8e8c6f7163f17c663b4e6814a545` | IDENTICAL |
| 695 | `methods/aris-vendor/skills/skills-codex/render-html/scripts/templates/dashboard.html` | `156e0825a131279debe55d1b91d7aa7c5f85e755458414932110687c9c3b3779` | `156e0825a131279debe55d1b91d7aa7c5f85e755458414932110687c9c3b3779` | IDENTICAL |
| 696 | `methods/aris-vendor/skills/skills-codex/research-lit/SKILL.md` | `d6293c58a6d6319b7ae5075ee9a1587ae83368400fbe15ff89a338e52e549c61` | `d6293c58a6d6319b7ae5075ee9a1587ae83368400fbe15ff89a338e52e549c61` | IDENTICAL |
| 697 | `methods/aris-vendor/skills/skills-codex/research-pipeline/SKILL.md` | `4326acbb8888c24a2bd5fa6e57a991055285148bdf9c59b7f60165ea3de1d2f0` | `4326acbb8888c24a2bd5fa6e57a991055285148bdf9c59b7f60165ea3de1d2f0` | IDENTICAL |
| 698 | `methods/aris-vendor/skills/skills-codex/research-refine-pipeline/SKILL.md` | `a3276db7ff225b6316c61c49d403e80f80592102310c74c1d6deb3dc9e8ae696` | `a3276db7ff225b6316c61c49d403e80f80592102310c74c1d6deb3dc9e8ae696` | IDENTICAL |
| 699 | `methods/aris-vendor/skills/skills-codex/research-refine/SKILL.md` | `bb489173329fec7a6551c74c319e2103d83f722ea11fc11462a7c4ccacd00b09` | `bb489173329fec7a6551c74c319e2103d83f722ea11fc11462a7c4ccacd00b09` | IDENTICAL |
| 700 | `methods/aris-vendor/skills/skills-codex/research-review/SKILL.md` | `62ec6f53bfed6e83fbd4fedfd976833de9516fc5427c20a2a27143e8420136e2` | `62ec6f53bfed6e83fbd4fedfd976833de9516fc5427c20a2a27143e8420136e2` | IDENTICAL |
| 701 | `methods/aris-vendor/skills/skills-codex/research-wiki/SKILL.md` | `c3e9acaf94402cb7648763772ee6c2d41a4f76328595354fb658647d4b2f7ca9` | `c3e9acaf94402cb7648763772ee6c2d41a4f76328595354fb658647d4b2f7ca9` | IDENTICAL |
| 702 | `methods/aris-vendor/skills/skills-codex/resubmit-pipeline/SKILL.md` | `db81ed2531cbe08711ec9bc33eb3d9feb146727645fa7f36cfbcf858ff6b9e7c` | `db81ed2531cbe08711ec9bc33eb3d9feb146727645fa7f36cfbcf858ff6b9e7c` | IDENTICAL |
| 703 | `methods/aris-vendor/skills/skills-codex/result-to-claim/SKILL.md` | `d22f527aa7d8b28a2ab7e4b206de3a9c5cb7ec5790b836883d5a40a0dc730a26` | `d22f527aa7d8b28a2ab7e4b206de3a9c5cb7ec5790b836883d5a40a0dc730a26` | IDENTICAL |
| 704 | `methods/aris-vendor/skills/skills-codex/run-experiment/SKILL.md` | `8325128eab14c7f82213d44c8e78e98f44ca680baa9c78f3bee8766f8e9f464a` | `8325128eab14c7f82213d44c8e78e98f44ca680baa9c78f3bee8766f8e9f464a` | IDENTICAL |
| 705 | `methods/aris-vendor/skills/skills-codex/semantic-scholar/SKILL.md` | `7e91ddfecb979562dd49797d2244cd03f796049fb116a418d12dbad70dca34bb` | `7e91ddfecb979562dd49797d2244cd03f796049fb116a418d12dbad70dca34bb` | IDENTICAL |
| 706 | `methods/aris-vendor/skills/skills-codex/serverless-modal/SKILL.md` | `a57ba889e70f4108f1b1427e1b352ca892918f6216eb2678289b3d829a9d7325` | `a57ba889e70f4108f1b1427e1b352ca892918f6216eb2678289b3d829a9d7325` | IDENTICAL |
| 707 | `methods/aris-vendor/skills/skills-codex/shared-references/acceptance-gate.md` | `462726457f58e6317abf91fe409a5acb14227881041e30709be8f7e04eeaef8e` | `462726457f58e6317abf91fe409a5acb14227881041e30709be8f7e04eeaef8e` | IDENTICAL |
| 708 | `methods/aris-vendor/skills/skills-codex/shared-references/assurance-contract.md` | `1df4ab0f26a81b7b904fb7ba066e485a7c12cfe0333ec49017f097e922a59aed` | `1df4ab0f26a81b7b904fb7ba066e485a7c12cfe0333ec49017f097e922a59aed` | IDENTICAL |
| 709 | `methods/aris-vendor/skills/skills-codex/shared-references/capture-antipatterns.md` | `5cc25b4e70d6d4073fa260d70c40e3fcf7f9e0eb6f0c6fca0e4d388c399550f3` | `5cc25b4e70d6d4073fa260d70c40e3fcf7f9e0eb6f0c6fca0e4d388c399550f3` | IDENTICAL |
| 710 | `methods/aris-vendor/skills/skills-codex/shared-references/citation-discipline.md` | `1c51dc936bbc3dbb17580148767734e0c642ad59516a861d9503b9767ca7043c` | `1c51dc936bbc3dbb17580148767734e0c642ad59516a861d9503b9767ca7043c` | IDENTICAL |
| 711 | `methods/aris-vendor/skills/skills-codex/shared-references/compute-env-contract.md` | `27aee2eee75a705a7d3ed72086b05ae2aa499104489376596ecb5b683807eeb5` | `27aee2eee75a705a7d3ed72086b05ae2aa499104489376596ecb5b683807eeb5` | IDENTICAL |
| 712 | `methods/aris-vendor/skills/skills-codex/shared-references/effort-contract.md` | `d4a53faf13d19d5d7f844d279b46ad5528de6572b07531cee4d49f4f405873e5` | `d4a53faf13d19d5d7f844d279b46ad5528de6572b07531cee4d49f4f405873e5` | IDENTICAL |
| 713 | `methods/aris-vendor/skills/skills-codex/shared-references/evidence-precheck.md` | `3eee097fe24fead242cf82a7393b828bf4add0fe511703a2be828edf06bb4c0b` | `3eee097fe24fead242cf82a7393b828bf4add0fe511703a2be828edf06bb4c0b` | IDENTICAL |
| 714 | `methods/aris-vendor/skills/skills-codex/shared-references/experiment-integrity.md` | `22150fbdc5867e7790c88f968bccb367079c2db4c190ddce980709aea7e76f60` | `22150fbdc5867e7790c88f968bccb367079c2db4c190ddce980709aea7e76f60` | IDENTICAL |
| 715 | `methods/aris-vendor/skills/skills-codex/shared-references/external-cadence.md` | `f59faf54b865b0c46779cacba081f3d5e4d68a7f748915197f8de64c67a26507` | `f59faf54b865b0c46779cacba081f3d5e4d68a7f748915197f8de64c67a26507` | IDENTICAL |
| 716 | `methods/aris-vendor/skills/skills-codex/shared-references/fan-out-pattern.md` | `550eb36f8b807001fdbe4c5357ea2927b5efb88bda74223747d5c45ab28edca4` | `550eb36f8b807001fdbe4c5357ea2927b5efb88bda74223747d5c45ab28edca4` | IDENTICAL |
| 717 | `methods/aris-vendor/skills/skills-codex/shared-references/injection-hygiene.md` | `05fa5db4a0b0f72529715d78fe4e20247458404362e8b94e295c7fa65a58e4ed` | `05fa5db4a0b0f72529715d78fe4e20247458404362e8b94e295c7fa65a58e4ed` | IDENTICAL |
| 718 | `methods/aris-vendor/skills/skills-codex/shared-references/integration-contract.md` | `5d393c31b36e98ae99c17ab9cf5879853c0cb595bbd9f4973ffe7bcd6549f4e7` | `5d393c31b36e98ae99c17ab9cf5879853c0cb595bbd9f4973ffe7bcd6549f4e7` | IDENTICAL |
| 719 | `methods/aris-vendor/skills/skills-codex/shared-references/output-composition.md` | `79a72c7ea02102c460ae3ad55853c21a4054b9df93f377c29dd34555e6d3c3a7` | `79a72c7ea02102c460ae3ad55853c21a4054b9df93f377c29dd34555e6d3c3a7` | IDENTICAL |
| 720 | `methods/aris-vendor/skills/skills-codex/shared-references/output-language.md` | `0f1447579bd7a2195fd4a074be70ae6345b5c368f1a70d327e89748bf5a378f9` | `0f1447579bd7a2195fd4a074be70ae6345b5c368f1a70d327e89748bf5a378f9` | IDENTICAL |
| 721 | `methods/aris-vendor/skills/skills-codex/shared-references/output-manifest.md` | `e767083e0ef97a7adf7a4e8a574090067a59c0655d5aca422a3747cd32b6afde` | `e767083e0ef97a7adf7a4e8a574090067a59c0655d5aca422a3747cd32b6afde` | IDENTICAL |
| 722 | `methods/aris-vendor/skills/skills-codex/shared-references/output-versioning.md` | `de8e7ac23069de6c5d0c482d4cef117dd5a543e00b57e2dc6c62560a457290c5` | `de8e7ac23069de6c5d0c482d4cef117dd5a543e00b57e2dc6c62560a457290c5` | IDENTICAL |
| 723 | `methods/aris-vendor/skills/skills-codex/shared-references/patent-format-cn.md` | `e5be6c2c6fab3c84c795b53ca419198192b95f2c1ccd63833b5d0510a8f93c1f` | `e5be6c2c6fab3c84c795b53ca419198192b95f2c1ccd63833b5d0510a8f93c1f` | IDENTICAL |
| 724 | `methods/aris-vendor/skills/skills-codex/shared-references/patent-format-ep.md` | `8cf58ac775fe524c230cd7f371abd0ce25eb774029129bc336f884026c58ba23` | `8cf58ac775fe524c230cd7f371abd0ce25eb774029129bc336f884026c58ba23` | IDENTICAL |
| 725 | `methods/aris-vendor/skills/skills-codex/shared-references/patent-format-us.md` | `13f179cc70fc8664f356d5258bdaa52a4cc577496e385e5ac5cdd421a12f4f65` | `13f179cc70fc8664f356d5258bdaa52a4cc577496e385e5ac5cdd421a12f4f65` | IDENTICAL |
| 726 | `methods/aris-vendor/skills/skills-codex/shared-references/patent-writing-principles.md` | `8c8dc8250948bd0741b792d350e3afdc686ed194a1bf02359fb0e55b81468d1d` | `8c8dc8250948bd0741b792d350e3afdc686ed194a1bf02359fb0e55b81468d1d` | IDENTICAL |
| 727 | `methods/aris-vendor/skills/skills-codex/shared-references/prior-art-databases.md` | `8225843987fbabb5f11788c19ed8a739f10691319865485d5cb876e7bc2a3cb7` | `8225843987fbabb5f11788c19ed8a739f10691319865485d5cb876e7bc2a3cb7` | IDENTICAL |
| 728 | `methods/aris-vendor/skills/skills-codex/shared-references/resumable-runs.md` | `3925421bcf64c680cc1b32e9de9e18d3bde0783a662c934aeb979183e39c2402` | `3925421bcf64c680cc1b32e9de9e18d3bde0783a662c934aeb979183e39c2402` | IDENTICAL |
| 729 | `methods/aris-vendor/skills/skills-codex/shared-references/review-scope-limits.md` | `1636b6bb96a18683698faad7bc103122ad0da9dcf3218b899f8413533f366e2a` | `1636b6bb96a18683698faad7bc103122ad0da9dcf3218b899f8413533f366e2a` | IDENTICAL |
| 730 | `methods/aris-vendor/skills/skills-codex/shared-references/review-tracing.md` | `4f4936984391da87464b8e8bf6f7c984f3f186e8fdc42890d0ac999b5e2024dc` | `4f4936984391da87464b8e8bf6f7c984f3f186e8fdc42890d0ac999b5e2024dc` | IDENTICAL |
| 731 | `methods/aris-vendor/skills/skills-codex/shared-references/reviewer-independence.md` | `d66262e74d5f69b1614007bf744b9f2220aeb35d1f36ec66196dfe32b0438530` | `d66262e74d5f69b1614007bf744b9f2220aeb35d1f36ec66196dfe32b0438530` | IDENTICAL |
| 732 | `methods/aris-vendor/skills/skills-codex/shared-references/reviewer-routing.md` | `e1fc0841b342b64130aa1c8fc99b337b1ef9e994697f17a518ebf1bbca664c66` | `e1fc0841b342b64130aa1c8fc99b337b1ef9e994697f17a518ebf1bbca664c66` | IDENTICAL |
| 733 | `methods/aris-vendor/skills/skills-codex/shared-references/skill-governance.md` | `4accf540cbae33ea958dc01431222305cb5ccbe19d12d67aa92c4c90e3637786` | `4accf540cbae33ea958dc01431222305cb5ccbe19d12d67aa92c4c90e3637786` | IDENTICAL |
| 734 | `methods/aris-vendor/skills/skills-codex/shared-references/taste-calibration.md` | `ab5880c4989e2d05ab58212d46e4bd4e215b1cee87b430e7d94d31bc431b947d` | `ab5880c4989e2d05ab58212d46e4bd4e215b1cee87b430e7d94d31bc431b947d` | IDENTICAL |
| 735 | `methods/aris-vendor/skills/skills-codex/shared-references/venue-checklists.md` | `aef7a0c396078747a5723b93b289c379aa1dda3f08540eca6d2d321264ed0ec8` | `aef7a0c396078747a5723b93b289c379aa1dda3f08540eca6d2d321264ed0ec8` | IDENTICAL |
| 736 | `methods/aris-vendor/skills/skills-codex/shared-references/wiki-helper-resolution.md` | `c39a9712178b481aac6bc5d118cb9bc3dee7ea8abf4b95ae535ad28ef8cab84e` | `c39a9712178b481aac6bc5d118cb9bc3dee7ea8abf4b95ae535ad28ef8cab84e` | IDENTICAL |
| 737 | `methods/aris-vendor/skills/skills-codex/shared-references/writing-principles.md` | `25c71f6b76fad1a198b47b4eae9b1d101561578cc0a8767e91706957829f0abe` | `25c71f6b76fad1a198b47b4eae9b1d101561578cc0a8767e91706957829f0abe` | IDENTICAL |
| 738 | `methods/aris-vendor/skills/skills-codex/slides-polish/SKILL.md` | `6c61a3d9885916a2151a8c1b20df52c491d1b859d176f206f0392559b2b816f6` | `6c61a3d9885916a2151a8c1b20df52c491d1b859d176f206f0392559b2b816f6` | IDENTICAL |
| 739 | `methods/aris-vendor/skills/skills-codex/specification-writing/SKILL.md` | `357f5a3aa4936ef78eb568c884a910e098a0653ce6aaa428bef215e808184bae` | `357f5a3aa4936ef78eb568c884a910e098a0653ce6aaa428bef215e808184bae` | IDENTICAL |
| 740 | `methods/aris-vendor/skills/skills-codex/system-profile/SKILL.md` | `9d31e32d2a63cf2f27a843e171c652327596c3f9e911c265660618d4ba27c48e` | `9d31e32d2a63cf2f27a843e171c652327596c3f9e911c265660618d4ba27c48e` | IDENTICAL |
| 741 | `methods/aris-vendor/skills/skills-codex/training-check/SKILL.md` | `c48dc4b1e5bcfcb025d48c90a03de7caa6cd02908b6c2c5d0148c6ec394b391e` | `c48dc4b1e5bcfcb025d48c90a03de7caa6cd02908b6c2c5d0148c6ec394b391e` | IDENTICAL |
| 742 | `methods/aris-vendor/skills/skills-codex/vast-gpu/SKILL.md` | `38e0f7c622e85bc96978ffb945c3f07a779f4f8e931cac917e51f8be8e8624d4` | `38e0f7c622e85bc96978ffb945c3f07a779f4f8e931cac917e51f8be8e8624d4` | IDENTICAL |
| 743 | `methods/aris-vendor/skills/skills-codex/web-debug-search/SKILL.md` | `ffb5f3ccf61c45d90c41901c251263f945c67baba0f91cb300cc1d53dcd63d01` | `ffb5f3ccf61c45d90c41901c251263f945c67baba0f91cb300cc1d53dcd63d01` | IDENTICAL |
| 744 | `methods/aris-vendor/skills/skills-codex/wiki-enrich/SKILL.md` | `3c3748a4da25f4f5ef8bc92ee8c3f8ff4742a0b24ba3de0f4a5d835026e2cb1f` | `3c3748a4da25f4f5ef8bc92ee8c3f8ff4742a0b24ba3de0f4a5d835026e2cb1f` | IDENTICAL |
| 745 | `methods/aris-vendor/skills/skills-codex/writing-systems-papers/SKILL.md` | `14a79a6b44b8e0723be097f3c120f0d787bef1a9d0f16ff1e1511c6ec1e765f1` | `14a79a6b44b8e0723be097f3c120f0d787bef1a9d0f16ff1e1511c6ec1e765f1` | IDENTICAL |
| 746 | `methods/aris-vendor/skills/slides-polish/SKILL.md` | `8e4839ede2857ffa114e748a3378df699b0ab9515cab29ce1c13712122d1a9d0` | `8e4839ede2857ffa114e748a3378df699b0ab9515cab29ce1c13712122d1a9d0` | IDENTICAL |
| 747 | `methods/aris-vendor/skills/specification-writing/SKILL.md` | `5e6dadac5555974ffcd6d91f242a1c56e432f711ccdb2131c926e0ef236ad6c2` | `5e6dadac5555974ffcd6d91f242a1c56e432f711ccdb2131c926e0ef236ad6c2` | IDENTICAL |
| 748 | `methods/aris-vendor/skills/system-profile/SKILL.md` | `9d31e32d2a63cf2f27a843e171c652327596c3f9e911c265660618d4ba27c48e` | `9d31e32d2a63cf2f27a843e171c652327596c3f9e911c265660618d4ba27c48e` | IDENTICAL |
| 749 | `methods/aris-vendor/skills/training-check/SKILL.md` | `b912cc10a6227211bdce83c51ed0ba2f6143b108e6b733daaeca809f59588654` | `b912cc10a6227211bdce83c51ed0ba2f6143b108e6b733daaeca809f59588654` | IDENTICAL |
| 750 | `methods/aris-vendor/skills/vast-gpu/SKILL.md` | `69aabce36540fd6fce55bf47b6f043166fc118fd708d03efddb57d168a99f4e5` | `69aabce36540fd6fce55bf47b6f043166fc118fd708d03efddb57d168a99f4e5` | IDENTICAL |
| 751 | `methods/aris-vendor/skills/web-debug-search/SKILL.md` | `ffb5f3ccf61c45d90c41901c251263f945c67baba0f91cb300cc1d53dcd63d01` | `ffb5f3ccf61c45d90c41901c251263f945c67baba0f91cb300cc1d53dcd63d01` | IDENTICAL |
| 752 | `methods/aris-vendor/skills/wiki-enrich/SKILL.md` | `ef2636d24dedbf0824f4b0bec96dee8daf1aef3c4b72ebe772b87a2febe3ea39` | `ef2636d24dedbf0824f4b0bec96dee8daf1aef3c4b72ebe772b87a2febe3ea39` | IDENTICAL |
| 753 | `methods/aris-vendor/skills/writing-systems-papers/SKILL.md` | `385fcf41742514b4aa9ecf93a0582a1bfd3452cacd12a54c87cf5bd82adccf7f` | `385fcf41742514b4aa9ecf93a0582a1bfd3452cacd12a54c87cf5bd82adccf7f` | IDENTICAL |
| 754 | `methods/aris-vendor/templates/CLAUDE_MD_TEMPLATE.md` | `b0676223a52aa3c651ba31210615d9e110f4ea6670e638e27ab1c1b12c239880` | `b0676223a52aa3c651ba31210615d9e110f4ea6670e638e27ab1c1b12c239880` | IDENTICAL |
| 755 | `methods/aris-vendor/templates/EXPERIMENT_LOG_TEMPLATE.md` | `32126068df3cf2168d0a7d24f8658d7e97890df506155746dbe570302f12b59f` | `32126068df3cf2168d0a7d24f8658d7e97890df506155746dbe570302f12b59f` | IDENTICAL |
| 756 | `methods/aris-vendor/templates/EXPERIMENT_PLAN_TEMPLATE.md` | `a28f0795f4c8e203216be6b5d91b4d9def60f5af7cdbfcc7ed0a2ebf205abb67` | `a28f0795f4c8e203216be6b5d91b4d9def60f5af7cdbfcc7ed0a2ebf205abb67` | IDENTICAL |
| 757 | `methods/aris-vendor/templates/EXPERIMENT_PLAN_TEMPLATE_CN.md` | `bec2b65c78f95902040bc7a2f2a728be42c82a8d0242a9c265602400e29da34f` | `bec2b65c78f95902040bc7a2f2a728be42c82a8d0242a9c265602400e29da34f` | IDENTICAL |
| 758 | `methods/aris-vendor/templates/FINDINGS_TEMPLATE.md` | `c3d98f53f780a5c91988d785e6cbb118c9e2b6d1ac819db8943639e17d55255f` | `c3d98f53f780a5c91988d785e6cbb118c9e2b6d1ac819db8943639e17d55255f` | IDENTICAL |
| 759 | `methods/aris-vendor/templates/IDEA_CANDIDATES_TEMPLATE.md` | `832bf7ac924894982cf73fae8f2d026b76111cf952f14f6ca3e3b130ee14e984` | `832bf7ac924894982cf73fae8f2d026b76111cf952f14f6ca3e3b130ee14e984` | IDENTICAL |
| 760 | `methods/aris-vendor/templates/IDEA_CANDIDATES_TEMPLATE_CN.md` | `b57f0086f8fcbe9159aa611ad866c39fcc5faf3149d75529e02bc7cbd06a8fbf` | `b57f0086f8fcbe9159aa611ad866c39fcc5faf3149d75529e02bc7cbd06a8fbf` | IDENTICAL |
| 761 | `methods/aris-vendor/templates/INVENTION_BRIEF_TEMPLATE.md` | `9fd8c4ca0912bfd5e449dcb6b034196dfad05c11f44abe04e5c177de5d6357f9` | `9fd8c4ca0912bfd5e449dcb6b034196dfad05c11f44abe04e5c177de5d6357f9` | IDENTICAL |
| 762 | `methods/aris-vendor/templates/MANIFEST_TEMPLATE.md` | `513bc08b2744b20825bb00063e77e22d536293e428fb419ca0c7b0ed9f7ea6d2` | `513bc08b2744b20825bb00063e77e22d536293e428fb419ca0c7b0ed9f7ea6d2` | IDENTICAL |
| 763 | `methods/aris-vendor/templates/NARRATIVE_REPORT_TEMPLATE.md` | `108481c051e96976b432f038c3903968d89d9d3556cc6bbef45c3947198713b6` | `108481c051e96976b432f038c3903968d89d9d3556cc6bbef45c3947198713b6` | IDENTICAL |
| 764 | `methods/aris-vendor/templates/PAPER_PLAN_TEMPLATE.md` | `0c323fa0e65c0d9e13100e7de1d6d7ea9f4857706b9e32e81afe9d632adf981d` | `0c323fa0e65c0d9e13100e7de1d6d7ea9f4857706b9e32e81afe9d632adf981d` | IDENTICAL |
| 765 | `methods/aris-vendor/templates/PATENT_CLAIMS_TEMPLATE.md` | `cbcfcb9715e951087e6a1a5f0937db04f9f9f123048dc6d3f9edb9d87a2927b3` | `cbcfcb9715e951087e6a1a5f0937db04f9f9f123048dc6d3f9edb9d87a2927b3` | IDENTICAL |
| 766 | `methods/aris-vendor/templates/PATENT_SPECIFICATION_TEMPLATE.md` | `8a058790ac4b97ae0a9d95d2c65026eca76194be98841b1e16f8037a47849fa0` | `8a058790ac4b97ae0a9d95d2c65026eca76194be98841b1e16f8037a47849fa0` | IDENTICAL |
| 767 | `methods/aris-vendor/templates/README.md` | `334aac9654abd110dd1201f0e56915f11a3e1e47304079856ce0db66c25dc635` | `334aac9654abd110dd1201f0e56915f11a3e1e47304079856ce0db66c25dc635` | IDENTICAL |
| 768 | `methods/aris-vendor/templates/RESEARCH_BRIEF_TEMPLATE.md` | `f3aae6dcb26028a4115994aeb5a37b3fe408aa6cca18743bac693cfc1ad08688` | `f3aae6dcb26028a4115994aeb5a37b3fe408aa6cca18743bac693cfc1ad08688` | IDENTICAL |
| 769 | `methods/aris-vendor/templates/RESEARCH_BRIEF_TEMPLATE_CN.md` | `4e341cc84147061bc67a1fa15379b54ba3ea11e1ad0917150333471686b2d4dc` | `4e341cc84147061bc67a1fa15379b54ba3ea11e1ad0917150333471686b2d4dc` | IDENTICAL |
| 770 | `methods/aris-vendor/templates/RESEARCH_CONTRACT_TEMPLATE.md` | `e71ee594951a50aaa93b1644318c28a705d6fcf9780ca1f61030b1c1bb44696a` | `e71ee594951a50aaa93b1644318c28a705d6fcf9780ca1f61030b1c1bb44696a` | IDENTICAL |
| 771 | `methods/aris-vendor/templates/claude-hooks/corpus_write_guard.json` | `b32a2d9200be0d70a55ea3d14e199db04a42b0cc5aab243afeee354329ccc363` | `b32a2d9200be0d70a55ea3d14e199db04a42b0cc5aab243afeee354329ccc363` | IDENTICAL |
| 772 | `methods/aris-vendor/templates/claude-hooks/corpus_write_guard.py` | `9005bc1bc94378952237439096d9c2c05f1ff6243456878da5c9fc94efdd5893` | `9005bc1bc94378952237439096d9c2c05f1ff6243456878da5c9fc94efdd5893` | IDENTICAL |
| 773 | `methods/aris-vendor/templates/claude-hooks/meta_logging.json` | `4162f4d902e6ba6740a377b0a7d01d85f15f7a36bda2645b6181bb51636aa303` | `4162f4d902e6ba6740a377b0a7d01d85f15f7a36bda2645b6181bb51636aa303` | IDENTICAL |
| 774 | `methods/aris-vendor/templates/gitignore-trace.txt` | `9fbc968ad5c3f249200c96ddb115324ac95991ddaea9dbc2af493e7c2983166d` | `9fbc968ad5c3f249200c96ddb115324ac95991ddaea9dbc2af493e7c2983166d` | IDENTICAL |
| 775 | `methods/aris-vendor/tests/__init__.py` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | IDENTICAL |
| 776 | `methods/aris-vendor/tests/_feishu_bridge_helpers.py` | `1d4fec96e1542f3b1a5a5f00f99d48c7b1ebb8ddb9d4ed608e4bb8793a7749b7` | `1d4fec96e1542f3b1a5a5f00f99d48c7b1ebb8ddb9d4ed608e4bb8793a7749b7` | IDENTICAL |
| 777 | `methods/aris-vendor/tests/_llm_chat_helpers.py` | `01c6564d4e49f67960dc4aacb3f84b6425685d9cd7a32a5f5732c10a1aec80bc` | `01c6564d4e49f67960dc4aacb3f84b6425685d9cd7a32a5f5732c10a1aec80bc` | IDENTICAL |
| 778 | `methods/aris-vendor/tests/_minimax_helpers.py` | `c9533d8c54c7103c3f143952021caf1d7e43324fb6e9689c305b613c503fb375` | `c9533d8c54c7103c3f143952021caf1d7e43324fb6e9689c305b613c503fb375` | IDENTICAL |
| 779 | `methods/aris-vendor/tests/test_argument_hint_lint.py` | `036529c7a0b1d71bf9f018a4e289520154cb2351afd90591c8d0c5650b980b40` | `036529c7a0b1d71bf9f018a4e289520154cb2351afd90591c8d0c5650b980b40` | IDENTICAL |
| 780 | `methods/aris-vendor/tests/test_arxiv_fetch.py` | `eb2fe49d4fd0e9f6a100d36e0034679424e6c3903c283cafe3bc186c79ec2ce2` | `eb2fe49d4fd0e9f6a100d36e0034679424e6c3903c283cafe3bc186c79ec2ce2` | IDENTICAL |
| 781 | `methods/aris-vendor/tests/test_capture_filter.py` | `5f97b6f9660aec2f25cd60ad3058f4e158025adfb9c2830c50a4cf2316811a2d` | `5f97b6f9660aec2f25cd60ad3058f4e158025adfb9c2830c50a4cf2316811a2d` | IDENTICAL |
| 782 | `methods/aris-vendor/tests/test_claude_review_overlay.py` | `62cf7ea5d2492852fcefb89dac85c95f7d65ada1361cbc6155555ff588dae80f` | `62cf7ea5d2492852fcefb89dac85c95f7d65ada1361cbc6155555ff588dae80f` | IDENTICAL |
| 783 | `methods/aris-vendor/tests/test_claude_review_parse.py` | `ffa630d617af32e0a340868d2037ca7527f7d00780c192ed2a5545d65125a5cd` | `ffa630d617af32e0a340868d2037ca7527f7d00780c192ed2a5545d65125a5cd` | IDENTICAL |
| 784 | `methods/aris-vendor/tests/test_codex_image2_server.py` | `9499ddde8399d09fc15a66b50ae154567b3fe408fca6dfaa9f022bd43db84ede` | `9499ddde8399d09fc15a66b50ae154567b3fe408fca6dfaa9f022bd43db84ede` | IDENTICAL |
| 785 | `methods/aris-vendor/tests/test_codex_install_update.py` | `9ea83746b102a9f7f4f680f88ca1f475ed211c51a466f072c159c396e73880b1` | `9ea83746b102a9f7f4f680f88ca1f475ed211c51a466f072c159c396e73880b1` | IDENTICAL |
| 786 | `methods/aris-vendor/tests/test_codex_skill_mirror.py` | `588c6b26c12798cee3c9a96db4a9b9c2b2185ef7b2f6598ec8b1bb3612843133` | `588c6b26c12798cee3c9a96db4a9b9c2b2185ef7b2f6598ec8b1bb3612843133` | IDENTICAL |
| 787 | `methods/aris-vendor/tests/test_copilot_install.py` | `8959ee05ce99bc906d6026c321fd5a161da23c4e3ec97dba4ff468d6ff2e2bfc` | `8959ee05ce99bc906d6026c321fd5a161da23c4e3ec97dba4ff468d6ff2e2bfc` | IDENTICAL |
| 788 | `methods/aris-vendor/tests/test_copilot_native_evidence.py` | `32f615c22dc0483a544077af406e5868b73114424f4d8338f31e4bed4c33eef1` | `32f615c22dc0483a544077af406e5868b73114424f4d8338f31e4bed4c33eef1` | IDENTICAL |
| 789 | `methods/aris-vendor/tests/test_corpus_write_guard.py` | `dd889d1e480dc2e0b7f06182d685cd9249ce21e075aec4bc4e2be0b51f62ec46` | `dd889d1e480dc2e0b7f06182d685cd9249ce21e075aec4bc4e2be0b51f62ec46` | IDENTICAL |
| 790 | `methods/aris-vendor/tests/test_deepxiv_fetch.py` | `a5b177b234297cd9fb7cc7e5941c72bd40a24e2b2e68242688512595a9061066` | `a5b177b234297cd9fb7cc7e5941c72bd40a24e2b2e68242688512595a9061066` | IDENTICAL |
| 791 | `methods/aris-vendor/tests/test_evidence_check.py` | `cc182ce17a3b91b1a3ca6534aa05931cc4f9a14fa1eb6b6281a17b47201a832d` | `cc182ce17a3b91b1a3ca6534aa05931cc4f9a14fa1eb6b6281a17b47201a832d` | IDENTICAL |
| 792 | `methods/aris-vendor/tests/test_exa_search.py` | `601b5e2cba56fb53d32445bd31e737a484569e6955c9e2881db7213bb7738e88` | `601b5e2cba56fb53d32445bd31e737a484569e6955c9e2881db7213bb7738e88` | IDENTICAL |
| 793 | `methods/aris-vendor/tests/test_feishu_bridge_server.py` | `0c1fd55d68ae99566cde4e039f34991afc19394471b44c7b2204ab5e31dabb9e` | `0c1fd55d68ae99566cde4e039f34991afc19394471b44c7b2204ab5e31dabb9e` | IDENTICAL |
| 794 | `methods/aris-vendor/tests/test_forensics_gate.py` | `8b02c97a4169a87de2e7916e883018b6ecc4964b83c3ed73dfc03816020bf53f` | `8b02c97a4169a87de2e7916e883018b6ecc4964b83c3ed73dfc03816020bf53f` | IDENTICAL |
| 795 | `methods/aris-vendor/tests/test_idea_discovery_gate.py` | `9a56045066cef56ab9f828ec7ee3d940b6dbd6e4494ded3713729e01459f616e` | `9a56045066cef56ab9f828ec7ee3d940b6dbd6e4494ded3713729e01459f616e` | IDENTICAL |
| 796 | `methods/aris-vendor/tests/test_install_aris_ps1.py` | `1bd953a23d567f803c3f76fab56c26b630be17ceeb0ef8a6af3e1242d6151488` | `1bd953a23d567f803c3f76fab56c26b630be17ceeb0ef8a6af3e1242d6151488` | IDENTICAL |
| 797 | `methods/aris-vendor/tests/test_install_aris_replace_link.py` | `c3e5ec1ab3b8099bee70876e8ebf9933fa9ac6498c65d92c7470b68e69be4083` | `c3e5ec1ab3b8099bee70876e8ebf9933fa9ac6498c65d92c7470b68e69be4083` | IDENTICAL |
| 798 | `methods/aris-vendor/tests/test_install_aris_selective.py` | `699d3eccec8a966c404e4dcfc829e5d05627feb63be7cc02850a4df062f499c6` | `699d3eccec8a966c404e4dcfc829e5d05627feb63be7cc02850a4df062f499c6` | IDENTICAL |
| 799 | `methods/aris-vendor/tests/test_install_aris_tools_symlink.py` | `42a62f33c00b9dcbc6cdb2549e4bbea3d4fa17abc5133109c3c23dfa064f4d98` | `42a62f33c00b9dcbc6cdb2549e4bbea3d4fa17abc5133109c3c23dfa064f4d98` | IDENTICAL |
| 800 | `methods/aris-vendor/tests/test_iteration_log.py` | `8605261d4433a0511b9960301d70873659a13c9579dff1a4681eb4d77833c74f` | `8605261d4433a0511b9960301d70873659a13c9579dff1a4681eb4d77833c74f` | IDENTICAL |
| 801 | `methods/aris-vendor/tests/test_llm_chat_converter.py` | `7a95ddf18d566c15f6cc089c5830b2ac82c4445b51a089366f8e77fffc969e30` | `7a95ddf18d566c15f6cc089c5830b2ac82c4445b51a089366f8e77fffc969e30` | IDENTICAL |
| 802 | `methods/aris-vendor/tests/test_llm_chat_server.py` | `9a5b5c563eb1b5c2d3a4fe72737e466c50ec27b80c67fe29ebc38a3e78d075ba` | `9a5b5c563eb1b5c2d3a4fe72737e466c50ec27b80c67fe29ebc38a3e78d075ba` | IDENTICAL |
| 803 | `methods/aris-vendor/tests/test_mainline_large_payload_prompts.py` | `c177a59906b6443beaf591409de9eace68539bc598647acbe30c1993969a61eb` | `c177a59906b6443beaf591409de9eace68539bc598647acbe30c1993969a61eb` | IDENTICAL |
| 804 | `methods/aris-vendor/tests/test_manual_review.py` | `a58df111531815cb0949eab9bde42f98df6e9f0d7fc4b881c0d68f3019889159` | `a58df111531815cb0949eab9bde42f98df6e9f0d7fc4b881c0d68f3019889159` | IDENTICAL |
| 805 | `methods/aris-vendor/tests/test_manual_review_integration.py` | `14c5305a4c480ea7ec073b2094e81997a803f726a47dfce52ecc40d985bc7f8a` | `14c5305a4c480ea7ec073b2094e81997a803f726a47dfce52ecc40d985bc7f8a` | IDENTICAL |
| 806 | `methods/aris-vendor/tests/test_minimax_chat_server.py` | `9753dbf4651c6913a2a0708269460db1497fbbf766db2bd9f423f9470e6012ff` | `9753dbf4651c6913a2a0708269460db1497fbbf766db2bd9f423f9470e6012ff` | IDENTICAL |
| 807 | `methods/aris-vendor/tests/test_minimax_integration.py` | `c25e0fa359de04f71c4cabb8a3dd26402e17e173241e8120a2ada1eba7412ab8` | `c25e0fa359de04f71c4cabb8a3dd26402e17e173241e8120a2ada1eba7412ab8` | IDENTICAL |
| 808 | `methods/aris-vendor/tests/test_openalex_fetch.py` | `3cacf33173825fb0c3b5844e7ee7d421185a14f180b0bd782f143ddfc81106a5` | `3cacf33173825fb0c3b5844e7ee7d421185a14f180b0bd782f143ddfc81106a5` | IDENTICAL |
| 809 | `methods/aris-vendor/tests/test_proof_suite_integration.py` | `d622eb8ccf8b430755f8e8559424f37a77ffad93c9b143b68a81c60e814ffdcb` | `d622eb8ccf8b430755f8e8559424f37a77ffad93c9b143b68a81c60e814ffdcb` | IDENTICAL |
| 810 | `methods/aris-vendor/tests/test_provenance.py` | `4739e07ec078543a1d5da745f49226c28aab7f43da7a4c527c55cd4c25a8c4b2` | `4739e07ec078543a1d5da745f49226c28aab7f43da7a4c527c55cd4c25a8c4b2` | IDENTICAL |
| 811 | `methods/aris-vendor/tests/test_research_wiki_claims.py` | `7ff0301af6a717223f2ed2fe0003215ff6c3338cbb12e0758364ee05d275f825` | `7ff0301af6a717223f2ed2fe0003215ff6c3338cbb12e0758364ee05d275f825` | IDENTICAL |
| 812 | `methods/aris-vendor/tests/test_research_wiki_encoding.py` | `6353a57011964f5548dc541435be3ee50f4a178d76fda3b2bc1e5e215839de72` | `6353a57011964f5548dc541435be3ee50f4a178d76fda3b2bc1e5e215839de72` | IDENTICAL |
| 813 | `methods/aris-vendor/tests/test_research_wiki_experiments.py` | `2ebd24e15085d8949dfc07bf4ad8a5119e29a896312cfc0c6a8f09bde30fe2b6` | `2ebd24e15085d8949dfc07bf4ad8a5119e29a896312cfc0c6a8f09bde30fe2b6` | IDENTICAL |
| 814 | `methods/aris-vendor/tests/test_research_wiki_fetch_arxiv_metadata.py` | `e954ae41169a634f7de52d7a3cde1338ec4c89f97e37058ad3d584efe9683e47` | `e954ae41169a634f7de52d7a3cde1338ec4c89f97e37058ad3d584efe9683e47` | IDENTICAL |
| 815 | `methods/aris-vendor/tests/test_research_wiki_helper_resolution.py` | `91fd121539954758a215dba34e772c8e2431121d9d3631090075f4d0a615b31b` | `91fd121539954758a215dba34e772c8e2431121d9d3631090075f4d0a615b31b` | IDENTICAL |
| 816 | `methods/aris-vendor/tests/test_research_wiki_ideas.py` | `de40712d7d2a1bbecbff37e4117329597b80187b5a081b53c92070f2799ff365` | `de40712d7d2a1bbecbff37e4117329597b80187b5a081b53c92070f2799ff365` | IDENTICAL |
| 817 | `methods/aris-vendor/tests/test_review_gate.py` | `eb39d8181f3585885af22058b76b30e568caa78efacec75b54a15fdbd139be01` | `eb39d8181f3585885af22058b76b30e568caa78efacec75b54a15fdbd139be01` | IDENTICAL |
| 818 | `methods/aris-vendor/tests/test_reviewer_pins.py` | `3c8b1173e553641a16219afd22d25470f78a698bcdd9668e66790f5e04b7dca8` | `3c8b1173e553641a16219afd22d25470f78a698bcdd9668e66790f5e04b7dca8` | IDENTICAL |
| 819 | `methods/aris-vendor/tests/test_run_state.py` | `7375ce4a0b9c6ee2c364f3c2b1fbb460ad4308b613e505ea66c325e081d7a2f2` | `7375ce4a0b9c6ee2c364f3c2b1fbb460ad4308b613e505ea66c325e081d7a2f2` | IDENTICAL |
| 820 | `methods/aris-vendor/tests/test_skill_groups.py` | `9988232082ec54099acd5b7b39edfae48506cec9fca0684d3f089123203e4cef` | `9988232082ec54099acd5b7b39edfae48506cec9fca0684d3f089123203e4cef` | IDENTICAL |
| 821 | `methods/aris-vendor/tests/test_skill_picker.py` | `5aba46f5f34e34e694c65888c94f38667e989465f2029d1b1d862f9a32dc85ef` | `5aba46f5f34e34e694c65888c94f38667e989465f2029d1b1d862f9a32dc85ef` | IDENTICAL |
| 822 | `methods/aris-vendor/tests/test_threat_scan.py` | `32dadeab5eaba600791851da4c53d84c267c93bfdd254946dbf2964cbf7c61a7` | `32dadeab5eaba600791851da4c53d84c267c93bfdd254946dbf2964cbf7c61a7` | IDENTICAL |
| 823 | `methods/aris-vendor/tests/test_trigger_eval.py` | `442612a876f5378796f4f436a21487fe3ac9540ea7928e1a3459e1345640f2d7` | `442612a876f5378796f4f436a21487fe3ac9540ea7928e1a3459e1345640f2d7` | IDENTICAL |
| 824 | `methods/aris-vendor/tests/test_verify_paper_audits.py` | `b2ce2ed7b8fd37ab48a189668ba61155b41c5979cdddf5689261d5ffab93bdde` | `b2ce2ed7b8fd37ab48a189668ba61155b41c5979cdddf5689261d5ffab93bdde` | IDENTICAL |
| 825 | `methods/aris-vendor/tests/test_watchdog.py` | `c6448f08f2edbb75e69a20d3ce0d7aba0a4e38de733646c40f662f619f30ed3e` | `c6448f08f2edbb75e69a20d3ce0d7aba0a4e38de733646c40f662f619f30ed3e` | IDENTICAL |
| 826 | `methods/aris-vendor/tests/test_watchdog_loop.py` | `d1230c6edcc2019b9881d9c6ef1a32deb3a8b9348560b8bd579380e3a9e3d2d0` | `d1230c6edcc2019b9881d9c6ef1a32deb3a8b9348560b8bd579380e3a9e3d2d0` | IDENTICAL |
| 827 | `methods/aris-vendor/tests/test_web_debug_search.py` | `38fda5c9e1969c6559e19ccb98896869fb2a2424f21745158124088ac7502cc9` | `38fda5c9e1969c6559e19ccb98896869fb2a2424f21745158124088ac7502cc9` | IDENTICAL |
| 828 | `methods/aris-vendor/tools/arxiv_fetch.py` | `9f127cd05f054e5a55065dd5bba7ef1865d22b64f105525ac347b3435ef6703a` | `9f127cd05f054e5a55065dd5bba7ef1865d22b64f105525ac347b3435ef6703a` | IDENTICAL |
| 829 | `methods/aris-vendor/tools/capture_filter.py` | `04cf93f079612fa1454e424101cef3069bb29c79dad11488e659b40bb1c118d0` | `04cf93f079612fa1454e424101cef3069bb29c79dad11488e659b40bb1c118d0` | IDENTICAL |
| 830 | `methods/aris-vendor/tools/check_skills_inventory.py` | `fe50c1eb2fd10c1d61cc484183b6b047caeb65a70577f0685a46ca5248b2cb1b` | `fe50c1eb2fd10c1d61cc484183b6b047caeb65a70577f0685a46ca5248b2cb1b` | IDENTICAL |
| 831 | `methods/aris-vendor/tools/convert_skills_to_llm_chat.py` | `1e640536f77ac7b6f882e95c175db8e622eb4751efeda9f8b350f8429ab4a3f0` | `1e640536f77ac7b6f882e95c175db8e622eb4751efeda9f8b350f8429ab4a3f0` | IDENTICAL |
| 832 | `methods/aris-vendor/tools/copilot_native_evidence.py` | `f8137fccba9874b7d04e0ddbbee5755d2d036509415680da760910959d7aff02` | `f8137fccba9874b7d04e0ddbbee5755d2d036509415680da760910959d7aff02` | IDENTICAL |
| 833 | `methods/aris-vendor/tools/deepxiv_fetch.py` | `764ef7a4bb87a25df1e92c6fc51060d4b92615df7f1306df71faf0fb6020630f` | `764ef7a4bb87a25df1e92c6fc51060d4b92615df7f1306df71faf0fb6020630f` | IDENTICAL |
| 834 | `methods/aris-vendor/tools/evidence_check.py` | `2edbd901d760d22e7e43a14e8e88ab0e089303f489055cd9b5e9d1f4dce50382` | `2edbd901d760d22e7e43a14e8e88ab0e089303f489055cd9b5e9d1f4dce50382` | IDENTICAL |
| 835 | `methods/aris-vendor/tools/exa_search.py` | `f29f9950d476fdf66b1f7bf8ccdcd7a827ae069060c5980d86b3b6f580b437b1` | `f29f9950d476fdf66b1f7bf8ccdcd7a827ae069060c5980d86b3b6f580b437b1` | IDENTICAL |
| 836 | `methods/aris-vendor/tools/experiment_queue/README.md` | `df7757d1b2cec27a52fd655a233948c5a031b846ea93e2167811a668877924b3` | `df7757d1b2cec27a52fd655a233948c5a031b846ea93e2167811a668877924b3` | IDENTICAL |
| 837 | `methods/aris-vendor/tools/experiment_queue/build_manifest.py` | `e1daa4116e24a36f970e5fddf6d1493e6a7396933c4e21468c85593ca35d4a25` | `e1daa4116e24a36f970e5fddf6d1493e6a7396933c4e21468c85593ca35d4a25` | IDENTICAL |
| 838 | `methods/aris-vendor/tools/experiment_queue/queue_manager.py` | `eac75a1285c81eb1683906cc979486f14bbba612c7cf434c753dfacec1f79dda` | `eac75a1285c81eb1683906cc979486f14bbba612c7cf434c753dfacec1f79dda` | IDENTICAL |
| 839 | `methods/aris-vendor/tools/extract_paper_style.py` | `020baeed072f7ab8ac0f4bc0b341609b2498f82121b6dd6d4e3961f0669eb1f2` | `020baeed072f7ab8ac0f4bc0b341609b2498f82121b6dd6d4e3961f0669eb1f2` | IDENTICAL |
| 840 | `methods/aris-vendor/tools/figure_renderer.py` | `88f667eb398d491fc49f5f4d24c6ee06de27862d1e9187c2a23f8ff3079b165c` | `88f667eb398d491fc49f5f4d24c6ee06de27862d1e9187c2a23f8ff3079b165c` | IDENTICAL |
| 841 | `methods/aris-vendor/tools/forensics_gate.py` | `6b702cffb656aada0290b7d06f218a96c2cc47d2cef924838b4b53f79233f80b` | `6b702cffb656aada0290b7d06f218a96c2cc47d2cef924838b4b53f79233f80b` | IDENTICAL |
| 842 | `methods/aris-vendor/tools/generate_codex_claude_review_overrides.py` | `cdc80209e8d0b17162b74cf64efc2cdbcad73fd30e728db6ff2d959e8cc33f3a` | `cdc80209e8d0b17162b74cf64efc2cdbcad73fd30e728db6ff2d959e8cc33f3a` | IDENTICAL |
| 843 | `methods/aris-vendor/tools/idea_discovery_gate.py` | `685699547e1f22e39d73394356f960258160a0ced6c1a551a0f7b89c81cb7981` | `685699547e1f22e39d73394356f960258160a0ced6c1a551a0f7b89c81cb7981` | IDENTICAL |
| 844 | `methods/aris-vendor/tools/install_aris.ps1` | `4eebea14bb58019304bdb52e1f4073537e754e12c610971cf3038521960b93a4` | `4eebea14bb58019304bdb52e1f4073537e754e12c610971cf3038521960b93a4` | IDENTICAL |
| 845 | `methods/aris-vendor/tools/install_aris.sh` | `df2f8210e5724c5364fe6355d8ab187cf07bb0a157dd81ef55d5d39651226cb7` | `df2f8210e5724c5364fe6355d8ab187cf07bb0a157dd81ef55d5d39651226cb7` | IDENTICAL |
| 846 | `methods/aris-vendor/tools/install_aris_codex.sh` | `f9df60648bf057481c9b11ce59ab0943b678d77677a145f247484c92d24fa88a` | `f9df60648bf057481c9b11ce59ab0943b678d77677a145f247484c92d24fa88a` | IDENTICAL |
| 847 | `methods/aris-vendor/tools/install_aris_copilot.sh` | `2b9ff14c6143583625d4bbf1399d8622664965ddbc885c39425975535031f229` | `2b9ff14c6143583625d4bbf1399d8622664965ddbc885c39425975535031f229` | IDENTICAL |
| 848 | `methods/aris-vendor/tools/iteration_log.py` | `819c22ba20bb270e0a514edb2626e7e3a1c4bade36f809e3ee9571cc076f7cb0` | `819c22ba20bb270e0a514edb2626e7e3a1c4bade36f809e3ee9571cc076f7cb0` | IDENTICAL |
| 849 | `methods/aris-vendor/tools/lint_skills_helpers.sh` | `8ac51929052f4a930439c4479508f01763b03cd486337c9b2ad9af18202fc82a` | `8ac51929052f4a930439c4479508f01763b03cd486337c9b2ad9af18202fc82a` | IDENTICAL |
| 850 | `methods/aris-vendor/tools/meta_opt/check_ready.sh` | `6c581e592893db7fb288c91bb8b4a7f94c34c13bb8e4d5fe11f6f5205f841fc6` | `6c581e592893db7fb288c91bb8b4a7f94c34c13bb8e4d5fe11f6f5205f841fc6` | IDENTICAL |
| 851 | `methods/aris-vendor/tools/meta_opt/log_event.sh` | `9bf323361b0f0613e70c3d88d44600b8608f647433ca288cc8eda2411cdefce1` | `9bf323361b0f0613e70c3d88d44600b8608f647433ca288cc8eda2411cdefce1` | IDENTICAL |
| 852 | `methods/aris-vendor/tools/meta_opt/trigger_eval.py` | `ec0dfb8b08de96c97b751968dd9b8e08bf323828cbf727e757a8bf2fc2d6ed76` | `ec0dfb8b08de96c97b751968dd9b8e08bf323828cbf727e757a8bf2fc2d6ed76` | IDENTICAL |
| 853 | `methods/aris-vendor/tools/meta_opt/trigger_evals.sample.json` | `20db057ba06ac3c7d1cd89e1297b80449c38462c1bf010531e053f368139f7f7` | `20db057ba06ac3c7d1cd89e1297b80449c38462c1bf010531e053f368139f7f7` | IDENTICAL |
| 854 | `methods/aris-vendor/tools/openalex_fetch.py` | `7f9cbb14a987ab750d0bb51d1501c7c67837f1b8a7fbb32edbb672d770b7105a` | `7f9cbb14a987ab750d0bb51d1501c7c67837f1b8a7fbb32edbb672d770b7105a` | IDENTICAL |
| 855 | `methods/aris-vendor/tools/overleaf_audit.sh` | `2d4bcaa33d541a74166bd83bf2262f0d92ad9600c502b5f88c80190aa6ed9274` | `2d4bcaa33d541a74166bd83bf2262f0d92ad9600c502b5f88c80190aa6ed9274` | IDENTICAL |
| 856 | `methods/aris-vendor/tools/overleaf_setup.sh` | `f2274ad4da248d590ef9b861551886aa7175bff26a003b87362996a9e92a076f` | `f2274ad4da248d590ef9b861551886aa7175bff26a003b87362996a9e92a076f` | IDENTICAL |
| 857 | `methods/aris-vendor/tools/paper_illustration_image2.py` | `f7c6221f70d00b113646f1c3d481a37a1b04a5bcef2f0e055b3d9b22d8b9c01f` | `f7c6221f70d00b113646f1c3d481a37a1b04a5bcef2f0e055b3d9b22d8b9c01f` | IDENTICAL |
| 858 | `methods/aris-vendor/tools/provenance.py` | `e063b46fee48db692662f407848f20a486148e89bac67682ff79295884f7ec6d` | `e063b46fee48db692662f407848f20a486148e89bac67682ff79295884f7ec6d` | IDENTICAL |
| 859 | `methods/aris-vendor/tools/research_wiki.py` | `455bfe5f0a5d53d5a06bd729350dc44e81257100a681ff3405c7277bd6001c0b` | `455bfe5f0a5d53d5a06bd729350dc44e81257100a681ff3405c7277bd6001c0b` | IDENTICAL |
| 860 | `methods/aris-vendor/tools/review_gate.py` | `6fc05c43200bfcdb95972d6c9b52bb9cb812bcc1ab741446ad040d7d7799affa` | `6fc05c43200bfcdb95972d6c9b52bb9cb812bcc1ab741446ad040d7d7799affa` | IDENTICAL |
| 861 | `methods/aris-vendor/tools/run_state.py` | `2bdc017ad90c90107150c373cb2683bcc57e16688a775780bb147cd8b1a59547` | `2bdc017ad90c90107150c373cb2683bcc57e16688a775780bb147cd8b1a59547` | IDENTICAL |
| 862 | `methods/aris-vendor/tools/save_trace.sh` | `0bf7833edb08677434ed6a7dff286aaacda53db6c756e35eeb29c70f0b46d366` | `0bf7833edb08677434ed6a7dff286aaacda53db6c756e35eeb29c70f0b46d366` | IDENTICAL |
| 863 | `methods/aris-vendor/tools/semantic_scholar_fetch.py` | `2b8b2f5164b886eb0f9d73ea5495e43991e9b52fc84631de87e941bc3e3ccb7c` | `2b8b2f5164b886eb0f9d73ea5495e43991e9b52fc84631de87e941bc3e3ccb7c` | IDENTICAL |
| 864 | `methods/aris-vendor/tools/skill-groups.tsv` | `d6affde70bc8381b4d20ba27da6cf3e86b24d1da6593779f11cef908ac6a5b70` | `d6affde70bc8381b4d20ba27da6cf3e86b24d1da6593779f11cef908ac6a5b70` | IDENTICAL |
| 865 | `methods/aris-vendor/tools/skill_picker.py` | `3d08bbf141abfc65e5b348735f10c9fe56fa92afc33bdd6ae7edae85a17cac14` | `3d08bbf141abfc65e5b348735f10c9fe56fa92afc33bdd6ae7edae85a17cac14` | IDENTICAL |
| 866 | `methods/aris-vendor/tools/smart_update.ps1` | `16ed12f54305e23268a3ced533734c78ed39cf3ba1e7125c9919b861660f4590` | `16ed12f54305e23268a3ced533734c78ed39cf3ba1e7125c9919b861660f4590` | IDENTICAL |
| 867 | `methods/aris-vendor/tools/smart_update.sh` | `40ffbfba8b52ddafd87fb11642382877cbd0a4d93a3576fce7cae5fe5ab4ef87` | `40ffbfba8b52ddafd87fb11642382877cbd0a4d93a3576fce7cae5fe5ab4ef87` | IDENTICAL |
| 868 | `methods/aris-vendor/tools/smart_update_codex.sh` | `d8f659a7d453bea7816bbaa200a0bc9312853cec46551c156101730b80759d75` | `d8f659a7d453bea7816bbaa200a0bc9312853cec46551c156101730b80759d75` | IDENTICAL |
| 869 | `methods/aris-vendor/tools/smart_update_copilot.sh` | `586d6fae1202ac180c0d6a68c13ff798302e7fcad5a91aa4b709f8f8b5c9e955` | `586d6fae1202ac180c0d6a68c13ff798302e7fcad5a91aa4b709f8f8b5c9e955` | IDENTICAL |
| 870 | `methods/aris-vendor/tools/threat_scan.py` | `fe0f6d4ec38baa09b58a9dbdb4bde3039b9863a3e52dc79ada33d79f3c84e268` | `fe0f6d4ec38baa09b58a9dbdb4bde3039b9863a3e52dc79ada33d79f3c84e268` | IDENTICAL |
| 871 | `methods/aris-vendor/tools/verify_paper_audits.sh` | `7dd8c07a6e9458077a202c3075c4207985b2bba7a196b10687d286b9c9dd455d` | `7dd8c07a6e9458077a202c3075c4207985b2bba7a196b10687d286b9c9dd455d` | IDENTICAL |
| 872 | `methods/aris-vendor/tools/verify_papers.py` | `28e6a3b1276d08fff971b71b03360a00a279d5f3c2ccacfd14b78a76d7fef76e` | `28e6a3b1276d08fff971b71b03360a00a279d5f3c2ccacfd14b78a76d7fef76e` | IDENTICAL |
| 873 | `methods/aris-vendor/tools/verify_wiki_coverage.sh` | `cdc619caacc680fef77f25def48aa7e4ad72ca2e0cb7842da5dfdfa8cbb8a709` | `cdc619caacc680fef77f25def48aa7e4ad72ca2e0cb7842da5dfdfa8cbb8a709` | IDENTICAL |
| 874 | `methods/aris-vendor/tools/watchdog.py` | `f03e40799e855d1201fdb4428c4625311691d204e719ca9e32acc33e0d0377ae` | `f03e40799e855d1201fdb4428c4625311691d204e719ca9e32acc33e0d0377ae` | IDENTICAL |
| 875 | `methods/aris-vendor/xhs_post.md` | `0050c3118925b20c32b84fb919ea4acc940cfa6ac123217c3179eaaefa2e9032` | `0050c3118925b20c32b84fb919ea4acc940cfa6ac123217c3179eaaefa2e9032` | IDENTICAL |
| 876 | `research-product/RESEARCH_ARTIFACT_CONTRACTS.yaml` | `bb0c518044cb4326aa9957cdc1e520af62b764417f3109416bc4ca874ea15550` | `e02ab91ea47e13a1822bac8b5accd3c94f449f259c5a41879cb06450e0e7ec62` | CRLF_ONLY |
| 877 | `research-product/templates/CandidateKnowledge.yaml` | `bf735fd27e8160d8494add1fedeaf5e595d9921a02185e0b51c8410389b4639e` | `bf735fd27e8160d8494add1fedeaf5e595d9921a02185e0b51c8410389b4639e` | IDENTICAL |
| 878 | `research-product/templates/CandidateResearch.yaml` | `488ce427a0c6ee9e77be22cc2b55fa0aa0efd38f2b49338491670e36f0521efe` | `488ce427a0c6ee9e77be22cc2b55fa0aa0efd38f2b49338491670e36f0521efe` | IDENTICAL |
| 879 | `research-product/templates/ClaimLedger.tsv` | `7073af28c5266d93ebfc33417bac228bf2d61d62d34bc458a4c6300d3c043ec6` | `6f41198ffbcb5a134b8d0273e41fb932210a4a7030a58799112a4f31e10081ce` | CRLF_ONLY |
| 880 | `research-product/templates/ContradictionLedger.tsv` | `479056a2db9212151134f2bd1ce9a2a96daa91744b540ef7c3afc6564c9d74fb` | `479056a2db9212151134f2bd1ce9a2a96daa91744b540ef7c3afc6564c9d74fb` | IDENTICAL |
| 881 | `research-product/templates/DisagreementLedger.tsv` | `48df62a0095daecaa7389da5608ccc582e207beed82a700c4bebe1dd20b8f569` | `48df62a0095daecaa7389da5608ccc582e207beed82a700c4bebe1dd20b8f569` | IDENTICAL |
| 882 | `research-product/templates/ExperimentPlan.yaml` | `f15d38b3d8db8d7ba939225b4e13646f2e5fd5f8081d3d17616d919991a866fd` | `f15d38b3d8db8d7ba939225b4e13646f2e5fd5f8081d3d17616d919991a866fd` | IDENTICAL |
| 883 | `research-product/templates/ExperimentResult.yaml` | `857fadcdacc0229330a62fa7d6ae96620c31ed2307db9efbce7052dad7a7a5f4` | `857fadcdacc0229330a62fa7d6ae96620c31ed2307db9efbce7052dad7a7a5f4` | IDENTICAL |
| 884 | `research-product/templates/ExtractionLedger.jsonl` | `ff63718a0dd65934acb5a0b571f3f75f899b9fa49487f9c7ad3820232819b622` | `ff63718a0dd65934acb5a0b571f3f75f899b9fa49487f9c7ad3820232819b622` | IDENTICAL |
| 885 | `research-product/templates/FitGapLedger.tsv` | `c2d54b0752a5b724df8ba3bc054a52c4602a610db00660e93eea8f3f2a8e7dd8` | `c2d54b0752a5b724df8ba3bc054a52c4602a610db00660e93eea8f3f2a8e7dd8` | IDENTICAL |
| 886 | `research-product/templates/HypothesisLedger.tsv` | `2f1e89d5388452f9557713a01510ffe12d77d291c4162e1c06f529c38c927e3b` | `2f1e89d5388452f9557713a01510ffe12d77d291c4162e1c06f529c38c927e3b` | IDENTICAL |
| 887 | `research-product/templates/OpenQuestionLedger.tsv` | `0ac82441f16b5010ce07c3e1f8f55adb38b65d27f3e2c2791d714f72e258840e` | `0ac82441f16b5010ce07c3e1f8f55adb38b65d27f3e2c2791d714f72e258840e` | IDENTICAL |
| 888 | `research-product/templates/ProposedEvolution.yaml` | `b34d63731471e65978488f192b4d246f041ced372e8a6280605cf854644c9e08` | `b34d63731471e65978488f192b4d246f041ced372e8a6280605cf854644c9e08` | IDENTICAL |
| 889 | `research-product/templates/QueryLedger.tsv` | `589ea0e57ca9c2e05bdd67ddecc5e09583b233805a558acc7ec767ac9c9d9f4e` | `589ea0e57ca9c2e05bdd67ddecc5e09583b233805a558acc7ec767ac9c9d9f4e` | IDENTICAL |
| 890 | `research-product/templates/RejectedAlternativeLedger.tsv` | `e78871334cdf422a3fa8a86348b802b75f14bf1ea3ea11547e6ab009d64d2bf3` | `e78871334cdf422a3fa8a86348b802b75f14bf1ea3ea11547e6ab009d64d2bf3` | IDENTICAL |
| 891 | `research-product/templates/ResearchHandoff.yaml` | `856065799134d9faf615bbe45438b3f9f686586b787e964ba711939c36cf744b` | `856065799134d9faf615bbe45438b3f9f686586b787e964ba711939c36cf744b` | IDENTICAL |
| 892 | `research-product/templates/ResearchPlan.yaml` | `dcadff4e2d1af057965093275bf23e9989e34cf468a44c10ef7a3788dd76077f` | `3fa9f2f261df12d5f8a4ce5894d8709e4825fad64626c6ff78b3b367e0cd467e` | CRLF_ONLY |
| 893 | `research-product/templates/ResearchRequest.yaml` | `e198da23a26b36e2a9d19b0a22ba7cd4afb03aab0fec99fb97b723cec350691f` | `e198da23a26b36e2a9d19b0a22ba7cd4afb03aab0fec99fb97b723cec350691f` | IDENTICAL |
| 894 | `research-product/templates/ResearchRunReceipt.json` | `e3fb41db474ace01f1a27f5ed6962063d780a3db6fc300fde5a9dee76278c9d5` | `fbb8cffe28a0f4703153a4cf28b1caccd0d959f63f375df0022c8b1e77a67398` | CRLF_ONLY |
| 895 | `research-product/templates/ResearchSourceDenominator.tsv` | `a45c84b5c7838c30584627dfd33a6713c448f8e0c0d92ff92d2add386ebf8337` | `a45c84b5c7838c30584627dfd33a6713c448f8e0c0d92ff92d2add386ebf8337` | IDENTICAL |
| 896 | `research-product/templates/ResearchSynthesis.md` | `26832ca0afce5417d936f66c70f8f5a25c082c35bad522fea71bedee5a7ead57` | `72975d673816686a10acfeb65afd2f1b30e52d2c0ff2b8b00ed5c3910b126cd4` | CRLF_ONLY |
| 897 | `research-product/templates/SourceDispositionLedger.tsv` | `54a758e07def25ebf9cb551b0fc8a03a0d015a35b0949a466c28a34a1bac6152` | `54a758e07def25ebf9cb551b0fc8a03a0d015a35b0949a466c28a34a1bac6152` | IDENTICAL |
| 898 | `research-product/templates/SourceSnapshotLedger.tsv` | `ed9b79cae144095ff0c8ee9a06666cb7f7a546ad32a2c83241fe0e0c425c30b1` | `ed9b79cae144095ff0c8ee9a06666cb7f7a546ad32a2c83241fe0e0c425c30b1` | IDENTICAL |
| 899 | `tests/__init__.py` | `5b3fb56aa3b20c9165a694e980e39986aef3404fc10e2fbca4da4ce4856bc640` | `a849ee8dfb3a7dddc26c777437113f324712d434452568f0f0e27da8d1c20bc8` | CRLF_ONLY |
| 900 | `tests/test_far_hardening.py` | `99a21e8a4ad5be1be8f2708c9ffac25f7fce973111d117cae3b466737ebe6993` | `a97b823bd3aeb1ca43487d7b3cf648747bd1423e5bb09bf4615718b4d6593453` | CRLF_ONLY |
| 901 | `tests/test_far_retrieval.py` | `7dad36128a8f85581dbd757a1fdfc815c8354d57dd38d0c88a49c4e3e1a82f9d` | `aadbd3bd3680657014fce466443de13d68219d4ea0c51bce5ee215f91c9342f7` | CRLF_ONLY |
| 902 | `tests/test_far_router.py` | `58ca6e6cc79f07f5f07773db0be88dbc692fc58bd18d81a0cb6a2400ec19a44f` | `3874046de941fbfe12afb7772f0f119fc88c82495356005a84dbe31eb39db1ab` | CRLF_ONLY |
| 903 | `tests/test_far_source_security.py` | `6fa97b3e0b205cbab02718d2e900893ddc6fea3bd23a42904da15b44211a0d7f` | `c32e6bb67e3848ebe059054d962bd526aa72210ab205ad3fe6cf8e39f0239236` | CRLF_ONLY |
| 904 | `tests/test_far_trisource.py` | `b6976cbbf788e5c5e74619f14cc30a8fc61178b97514cf8fc111ee107f395df6` | `2c6a51a8359a90c992e982958dce786f05900fe9320f4e12c6d76765e22afd97` | CRLF_ONLY |
| 905 | `tests/test_far_watchdog.py` | `dbf3afc63bcbe7482a498d91d76a9d602348e1ea4e7c52539610b2c898a276d3` | `f863fcdcbdc8523c5ee202b0ecdad64814aaea13798142d6c65379b0eeb4d01d` | CRLF_ONLY |

## 5. 缺口清單（mirror 有，本地權威也有，但**未上傳**）

### 5.1 FDA：53 檔未上傳（bucket：`evidence`=14, `evidence/receipts`=39）

| # | path（相對 `fabric-desktop-automation/`） | local bytes | local sha256 |
|---|---|---|---|
| 1 | `evidence/FDA_DIRECTORY_TREE.txt` | 2046 | `c6d5647acba90379c5882018f6a024d3f7fcb27ecc4e91c8f89c3fd7e98a7110` |
| 2 | `evidence/FDA_EVIDENCE_MANIFEST.json` | 13479 | `b07d5d810d6ee2d4f18d6acaa93e0661cf43998b5987fbebf9296571aca804ea` |
| 3 | `evidence/FDA_EXTERNAL_FINAL_FOCUSED_REREVIEW_2026-08-14_r8.md` | 15891 | `19c74eeb83ac3e09b9d35d10ffccbe871dba877fd33b4e326f810d9efc7fd877` |
| 4 | `evidence/FDA_EXTERNAL_FINAL_SINGLE_EVIDENCE_RR6.md` | 51147 | `92207123f9698d1dc15f40ffaaec00e6e39ee8152c2e297f900a97278560bfa4` |
| 5 | `evidence/FDA_EXTERNAL_FINAL_SINGLE_EVIDENCE_RR7.md` | 45918 | `28b0c9f2c902d9ad080b9ebf098294c24e495e4c65f04a034da0bfb14cffb0d6` |
| 6 | `evidence/FDA_EXTERNAL_FINAL_SINGLE_EVIDENCE_RR8.md` | 69870 | `acbf7463119785537fdb0c2088d49f629fb09735990ccb07662dc9f795b1265c` |
| 7 | `evidence/FDA_EXTERNAL_FULL_EVIDENCE_20260814.md` | 28972 | `75078b2019d8efeff5ba14d9912178d944fb2ffbb0e8902991be39cd2140fee8` |
| 8 | `evidence/FDA_EXTERNAL_RE_REVIEW_EVIDENCE_20260814_r2.md` | 6996 | `e5f5dc0a1ae65cac9860c120b2abb3163eeba6a757ffaf93d796cb31695dad88` |
| 9 | `evidence/FDA_EXTERNAL_SINGLE_EVIDENCE_RR3.md` | 34299 | `2687e4d5f90019c865638da764dac7e7d48b261a994fd1b6f291c737b4cf28cc` |
| 10 | `evidence/FDA_FOLDER_REORGANIZATION_RECEIPT.json` | 777 | `00d690f94a05aabc644e9c9cafc4664fc98602eeaa5e28f54d17ae6ee7e58cbe` |
| 11 | `evidence/FDA_IMPLEMENTATION_EVIDENCE.md` | 12643 | `025bd73d1398686a439cfb2051155dca9783c0ad50ec4cc908d32fb3aae12eb4` |
| 12 | `evidence/FDA_MIRROR_READBACK_20260814_RR3.json` | 452 | `beb62f115a2466894d0f141f7bd6d841888f8259022607f1cc1e8a094a597621` |
| 13 | `evidence/FDA_RAW_EVIDENCE_SINGLE_MD_RR5.md` | 37356 | `41eb23c14bcaba0c9fcbee922d24a0bb0359d524cb4d7e84b99b9c5ed769db2c` |
| 14 | `evidence/FDA_USER_GUIDE.md` | 22327 | `21a3d22b26e499b1bad10dc7fb0235402b460c3138e0fd719e7791d120815ee5` |
| 15 | `evidence/receipts/FDA_BOUNDED_CONTROL_LIVE_PROBE.json` | 586 | `51559903556f3910d6286974a349b8515d8498a6870d727532cd7f5f016b623e` |
| 16 | `evidence/receipts/FDA_C0_READBACK_RECEIPT.json` | 5838 | `ca905aba1e02a8df4b1a6d2b41764df448bbd53353422c2a81b5b2750562b414` |
| 17 | `evidence/receipts/FDA_C2_CUA_QUALIFICATION_RECEIPT.json` | 3380 | `c181ef51b2066b1ffc9b185355b42653c00ee245048ebe84483fde2393c54362` |
| 18 | `evidence/receipts/FDA_C3_UFO2_EFFECTIVE_LOAD_RECEIPT.json` | 1811 | `1d7d149ac6cd1ed0616ab1fa25f804cc20f33808663d7d1d32b4040ab8d97781` |
| 19 | `evidence/receipts/FDA_C3_UFO2_QUALIFICATION_RECEIPT.json` | 1800 | `048b151f462384310eabb9018e7d5ecb012677473b47667be49be84c03492e6d` |
| 20 | `evidence/receipts/FDA_C4_XQ_QUALIFICATION_RECEIPT.json` | 3636 | `cf86b05f71c0cf734dcc2684cd0bb1542c82e151ea7edf1df5132236189b6543` |
| 21 | `evidence/receipts/FDA_C5_LEASE_CONCURRENCY_RECEIPT.json` | 825 | `357a9650a045d7485ff93270f98268946d740980da156d6f280e995b2364d0a8` |
| 22 | `evidence/receipts/FDA_CHECKER_179_RAW_RECEIPT_RR6.json` | 29901 | `d323854f8461887db077cbefba7c356e944bde42895884c169d7bea6c05ad5b9` |
| 23 | `evidence/receipts/FDA_CHECKER_FINAL_RR7.json` | 35395 | `1a02c45ef2af8a45215e5250befc4c1aa2705302ddf7abdb99ea47e8866b074e` |
| 24 | `evidence/receipts/FDA_CHECKER_RAW_RECEIPT_RR6.json` | 30120 | `8226f901bcda5333e2f68595bf9052204fb193164b9f63d5dba43dc486fadc3e` |
| 25 | `evidence/receipts/FDA_F01_CURRENT_260811_RECEIPT.json` | 4470 | `c27f6c5e690c922a9ac8d4d03552481fd965eea12c0241f9fc38dc356a041839` |
| 26 | `evidence/receipts/FDA_F01_LIVE_FIXTURE_RECEIPT.json` | 3912 | `36fff6f57cffa10bc8f6c753295147c644a1b000ea35c58de8f848a1dc8d8697` |
| 27 | `evidence/receipts/FDA_F03_LIVE_FIXTURE_RECEIPT.json` | 1337 | `cbf60ef9cd5cab761ce3e6ccdd13236d5107a4d41f3a52482dc396dae31b1055` |
| 28 | `evidence/receipts/FDA_F04_LIVE_FIXTURE_RECEIPT.json` | 1183 | `5d9bd84beae406f06206bc7d8b3bf1288ff38b2f54f34dcdf2947da3905647d8` |
| 29 | `evidence/receipts/FDA_F06_CLOSURE_V3_RECEIPT.json` | 1263 | `fe2d736f49865b9a7d2abfa3b28794764bae32c17d60d559623fe3a77a39980b` |
| 30 | `evidence/receipts/FDA_F06_CLOSURE_V4_RECEIPT.json` | 1125 | `e149fdeb258a422a7983722c2ae2315d4e77a32317574a2c9a2c61da79edd47b` |
| 31 | `evidence/receipts/FDA_F06_CLOSURE_V5_RECEIPT.json` | 1139 | `249c016a3a3a7b68a2439469cc5a31c24ace8d198e9f968177c9d89e3f018792` |
| 32 | `evidence/receipts/FDA_F06_CLOSURE_V6_RECEIPT.json` | 1558 | `0462d34b16705535b2c293bdecc2359ad910fae7b74986c9328c94efdaa6be47` |
| 33 | `evidence/receipts/FDA_F06_CLOSURE_V7_RECEIPT.json` | 1603 | `774454d0faeed6c0ae0af92f4c959378be87afa63a15a3e5b0cb952131ec0b6f` |
| 34 | `evidence/receipts/FDA_F06_CLOSURE_V8_RECEIPT.json` | 1352 | `a16a4bb3852ddb30460ba19e4979e32d1b5263ed66e946fc076c614e96ea72b7` |
| 35 | `evidence/receipts/FDA_F06_COMPILE_RECEIPT.json` | 1380 | `94cfccad36dabc5e91eb32eb4259f8232c160f674a018cbdb0a6ca14dadac569` |
| 36 | `evidence/receipts/FDA_F06_COMPILE_TOOLBAR_RECEIPT.json` | 972 | `7977c24d7fe9576b89e1edc2eab20bbba26397e5d9985edd4dfa9e007e92bdae` |
| 37 | `evidence/receipts/FDA_F06_EXPORT_RECEIPT.json` | 768 | `f03dd33cbca58b70d51c7c5a1425d830a59aeaf53fdbe21de457cffcac1aa083` |
| 38 | `evidence/receipts/FDA_F06_F07_LIVE_FIXTURE_RECEIPT.json` | 1460 | `353b639f2a789f6c6116b8225262af1325178adb9354be553670461f21273bef` |
| 39 | `evidence/receipts/FDA_F06_FRESH_10RUN_RECEIPT_RR6.json` | 3184 | `369187d9b4223c95bac6ab8d8be0a8322cf4ca17a5fdb7481487cbd0419d3408` |
| 40 | `evidence/receipts/FDA_F06_LIVE_FIXTURE_RECEIPT.json` | 1272 | `f10b9c5497fb763fdfafd7eb1659c93df4f3835f5a9026870fc4d75d11a27ade` |
| 41 | `evidence/receipts/FDA_F06_SYSTEM_PATH_RECEIPT.json` | 1257 | `7407a237fd1127474e692b5d564dc8420330ed58c7fdf0fa366d7cb53d93a345` |
| 42 | `evidence/receipts/FDA_F06_TEN_RUN_RECEIPT.json` | 2535 | `17353bfbbde9e9dd59f67d0be08e8075530b68d950a8a66d7ce70b5b00f5d97c` |
| 43 | `evidence/receipts/FDA_F09B_PAPER_RUNTIME_RECEIPT.json` | 2002 | `a57f730465c3d023145e2481fb274bddc87c62c6d5b6e1f576d2edd42fa41f78` |
| 44 | `evidence/receipts/FDA_F09_RADAR_RECEIPT.json` | 1089 | `0c9adabdbac434953007bd8dcba0bbf7c8aacd1b267343f02c6e1b4d721f1ee5` |
| 45 | `evidence/receipts/FDA_F10_F11_READBACK_RECEIPT.json` | 1373 | `7d471b12739d9e2f4dce9980cd8e8171c43bed3b0df723775ee380894eb2323b` |
| 46 | `evidence/receipts/FDA_XQ_BUILD_FINGERPRINT_RECEIPT.json` | 946 | `b23ddca238b99378988c731036b9fe01742a1a5fbbc0fd9ba3d8223eb484e9be` |
| 47 | `evidence/receipts/FDA_XQ_NATIVE_QUALIFICATION_RECEIPT.json` | 551 | `d676c68f05f9560af6f5aae31408cee66308adc9d18d50bda150dce6d7f8fa13` |
| 48 | `evidence/receipts/FDA_XQ_PAPER_10RUN_RECEIPT_RR6.json` | 3718 | `b003d3967d030d98953830fa1eac646ebed3e8f3862f399758f7528c1dc19fe2` |
| 49 | `evidence/receipts/FDA_XQ_PAPER_10RUN_RECEIPT_RR6_V2.json` | 9505 | `dc0a252df036a448237d414c230e7d83ec0deb38445ef295022a51514fb9b501` |
| 50 | `evidence/receipts/FDA_XQ_PAPER_10RUN_RECEIPT_RR6_V3.json` | 11241 | `89ca67f47fff342b83191a345f0c8b44c16fc419c61b259640329935a0f3129f` |
| 51 | `evidence/receipts/FDA_XQ_PAPER_RUNTIME_RECEIPT.json` | 4587 | `1730e4162c1f10b606af7e850c494df799cc96e3e2ef46c93a4466f8e3905a74` |
| 52 | `evidence/receipts/FDA_XQ_PAPER_STOP_10RUN_RECEIPT_RR7.json` | 8865 | `5700491f5e79a8243acc122f1536dd92a251146aa9c102d62383b990aef69346` |
| 53 | `evidence/receipts/FDA_XQ_PAPER_STOP_SEMANTICS_AUTHORITY_RR8.json` | 8417 | `65b0dfc4bd718eab53cd918c8802861587b63b08348b977d9cf765684531f5a5` |
（mirror-only：0 檔）

### 5.2 FAR：13 檔未上傳

| # | path（相對 `fabric-autonomous-research/`） | local bytes | local sha256 |
|---|---|---|---|
| 1 | `evidence/FAR_ARTIFACT_INDEX.json` | 15415 | `7b01df26d17505ec27b3c96d3b383e144c022b49f78ba6275b27442f66a6a755` |
| 2 | `evidence/FAR_EVIDENCE_MANIFEST.json` | 22951 | `14eed267e97602ef47002678059e4c66149c3fb6b6e8406f86ba48d8d1cc655b` |
| 3 | `evidence/FAR_EXTERNAL_REVIEW_PACKAGE_v3.zip` | 174640 | `bab2ecaead5393cf9dc7d3576c565466939fe0f5a0c9a0e9d8f4d2daccf8efb5` |
| 4 | `evidence/FAR_FINAL_ACCEPTANCE_EVIDENCE_post-activation_eff79b73.md` | 76780 | `eff79b73f281da4ead2bd01e6bb4697af57060eec0d23dba261dac33faf8c58f` |
| 5 | `evidence/FAR_FIRST_USE_EVIDENCE.md` | 6326 | `ddd6bc74588f007cdacbb29fdf0098605af60eb17400c27158ae2e11bed2f6d8` |
| 6 | `evidence/FAR_FIRST_USE_INDEX.json` | 18185 | `92a1523ec25e34f7271c5ba9205721a53df843dd623b4368a17529782728ae07` |
| 7 | `evidence/FAR_FIRST_USE_SUBJECT_MANIFEST.json` | 4236 | `08d3970dfc5666bf5d8e65883d2934277b13b2ebb4080c8a55ad84729f7e1b8c` |
| 8 | `evidence/FAR_IMPLEMENTATION_EVIDENCE.md` | 12199 | `8c708e5cffd41516f4dd1f5735c9d374e8fca8dd95ff69be0af1e381f43687f8` |
| 9 | `evidence/FAR_IMPLEMENTATION_EVIDENCE_v2.md` | 9125 | `249f71bab389207fda7a4194a1bbd1b617ac50bc4a8c7387eb084919a5c04871` |
| 10 | `evidence/FAR_IMPLEMENTATION_EVIDENCE_v3.md` | 10438 | `3f5efaf23edda8208d39b4cf9b9e13b5b1a948fa673c500a83cd30619212cc08` |
| 11 | `evidence/FAR_MVT_PLANNED_GATE1_RECEIPT.json` | 2828 | `2856bad29acaf47cd54ae07fe7cb2fefb69fc7b361779c039e79b3c4510ce06e` |
| 12 | `evidence/FAR_TRI_SOURCE_FOCUSED_HARDENING_EVIDENCE.md` | 42872 | `b7a696572aa960ba2f62d42462062af63193baa03c3350ed08db5130533d4c45` |
| 13 | `evidence/FAR_TRI_SOURCE_IMPLEMENTATION_EVIDENCE.md` | 31720 | `4793e16fa1b3f322bfde633d4dcbf5fc383de6aa942869ebcd533689b971bfde` |
（mirror-only：0 檔）

## 6. 未上傳造成的**具體**後果：mirror 內文件所引用但不存在的路徑（dangling refs）

- `lane_a_dangling_refs.json`（sha256 `77db07b8977ff00e28aeb03fc59c92055898fd63cd37eabab0e06c6d5fd0eced`）：`missing_refs` = 24 筆
    - `DOC/FDA_USER_GUIDE.md`
    - `FDA_C3_UFO2_EFFECTIVE_LOAD_RECEIPT.json`
    - `FDA_CHECKER_FINAL_RR7.json`
    - `FDA_CUA_0194_SHADOW_RECEIPT.json`
    - `FDA_EVIDENCE_MANIFEST.json`
    - `FDA_EXTERNAL_FINAL_FOCUSED_REREVIEW_2026-08-14_r9.md`
    - `FDA_EXTERNAL_FINAL_SINGLE_EVIDENCE_RR6.md`
    - `FDA_EXTERNAL_FINAL_SINGLE_EVIDENCE_RR8.md`
    - `FDA_EXTERNAL_RE_REVIEW_EVIDENCE_20260814_r2.md`
    - `FDA_F01_CURRENT_260811_RECEIPT.json`
    - `FDA_F01_LIVE_FIXTURE_RECEIPT.json`
    - `FDA_F06_FRESH_10RUN_RECEIPT_RR6.json`
    - `FDA_F06_TEN_RUN_RECEIPT.json`
    - `FDA_IMPLEMENTATION_EVIDENCE.md`
    - `FDA_RAW_EVIDENCE_SINGLE_MD_RR5.md`
    - `FDA_XQ_BUILD_FINGERPRINT_RECEIPT.json`
    - `FDA_XQ_NATIVE_QUALIFICATION_RECEIPT.json`
    - `FDA_XQ_PAPER_RUNTIME_RECEIPT.json`
    - `FDA_XQ_PAPER_STOP_10RUN_RECEIPT_RR7.json`
    - `FDA_XQ_PAPER_STOP_SEMANTICS_AUTHORITY_RR8.json`
    - `evidence/receipts/`
    - `var/fda/fda_run.py`
    - `var/fda/hgk_evidence_preflight.py`
    - `var/fda/screen_state_check.py`
- `lane_b_dangling_refs.json`（sha256 `6fdd2d78a70e70f39c915c23f0305a8b7766d161020ceec6320b2be0e7350187`）：`missing_from_mirror_list` = 66 筆
    - `1.md`
    - `CLAUDE.md`
    - `CLOSURE-EXT-FAR-001..010.json`
    - `CLOSURE_EXT-FAR-002.json`
    - `DOC\\fabric-autonomous-research\\CHANGE_INPUT_MANIFEST_TRI_SOURCE_2026-08-13.json`
    - `DOC\\fabric-autonomous-research\\FAR_TRI_SOURCE_IMPLEMENTATION_2026-08-13_r1.md`
    - `ExtractionLedger.json`
    - `FAR-root/FAR_EXTERNAL_REVIEW_PACKAGE_v3.zip`
    - `FAR-root/FAR_FINAL_ACCEPTANCE_EVIDENCE_post-activation_eff79b73.md`
    - `FAR-root/FAR_FIRST_USE_SUBJECT_MANIFEST.json`
    - `FAR-root/FAR_IMPLEMENTATION_EVIDENCE_v2.md`
    - `FAR-root/FAR_IMPLEMENTATION_EVIDENCE_v3.md`
    - `FAR/WO-FAR-008/FAR_RESEARCH_MAP.md`
    - `FAR\WO-FAR-008\FAR_RESEARCH_MAP.md`
    - `FAR\\WO-FAR-008\\FAR_RESEARCH_MAP.md`
    - `FAR_EVIDENCE_MANIFEST.json`
    - `FAR_EXTERNAL_REVIEW_PACKAGE_v3.zip`
    - `FAR_FINAL_ACCEPTANCE_EVIDENCE_post-activation_eff79b73.md`
    - `FAR_FINAL_EXTERNAL_ACCEPTANCE_REPORT_2026-08-13_r7_ALL_PASS.md`
    - `FAR_FIRST_USE_SUBJECT_MANIFEST.json`
    - `FAR_IMPLEMENTATION_EVIDENCE_v2.md`
    - `FAR_IMPLEMENTATION_EVIDENCE_v3.md`
    - `FAR_RESEARCH_MAP.md`
    - `FAR_TRI_SOURCE_FOCUSED_HARDENING_EVIDENCE.md`
    - `FAR_TRI_SOURCE_IMPLEMENTATION_2026-08-13_r1.md`
    - `FDA_IMPLEMENTATION_EVIDENCE.md`
    - `Fabric/fabric-autonomous-research/canary/FAR-20260813-001/ExtractionLedger.json`
    - `Fabric/fabric-autonomous-research/canary/FAR-20260813-002/ExtractionLedger.json`
    - `Fabric/fabric-autonomous-research/research-product/templates/ExtractionLedger.json`
    - `Fabric\\fabric-autonomous-research\\FAR_TRI_SOURCE_IMPLEMENTATION_EVIDENCE.md`
    - `Fabric\\fabric-autonomous-research\\canary\\FAR-20260813-001\\ExtractionLedger.json`
    - `Fabric\\fabric-autonomous-research\\canary\\FAR-20260813-002\\ExtractionLedger.json`
    - `Fabric\\fabric-autonomous-research\\research-product\\templates\\ExtractionLedger.json`
    - `HARDENING_CHANGE_INPUT_MANIFEST_2026-08-14.json`
    - `HG-KSEOS/var/far/capc/FAR_IMPLEMENTATION_2026-08-13_contract.json`
    - `HG-KSEOS_P0-CIP-PACK_v2026.08.05-r2.md`
    - `Projects\Agent_Workspace\HG-KSEOS\var\shared-spine\hg-kseos.db`
    - `Projects\\Agent_Workspace\\Fabric\\evidence\\review\\FAR_IMPLEMENTATION_EVIDENCE_v3.md`
    - `Projects\\Agent_Workspace\\Fabric\\fabric-autonomous-research\\FAR_IMPLEMENTATION_EVIDENCE_v3.md`
    - `Projects\\Agent_Workspace\\HG-KSEOS\\evidence\\review\\FAR_IMPLEMENTATION_EVIDENCE_v3.md`

## 7. 安全事件（HIGH）

- 檔案：`DESKTOP/docs-fda/XQ用戶登入資訊.txt`（**public repo**，`private=false`）
- sha256 = `bf8274bccfea979117988300c11c08262b26b8e6d8f2e45984b629f45a1ec913`，68 bytes；與本機附件 `~/AppData/Local/hermes/attachments/XQ用戶登入資訊.txt` **位元相同**（sha256 `bf8274bccfea979117988300c11c08262b26b8e6d8f2e45984b629f45a1ec913`）。
- 內容骨架（**數值一律遮罩，本 MD 不含任何憑證值**）：
```
  1: ##用戶登入資訊
  2: 
  3: 帳號：
  4: ######
  5: 
  6: 密碼：
  7: ##########
```
- 對照：mirror 根 `README.md` §2/§4 明文聲明 *"Credentials, tokens and connection strings are **never** mirrored."* → **聲明與事實相反**。
- 處置建議（未執行）：自 mirror 移除該檔並**輪替 XQ 憑證**。

### 7.1 憑證相鄰（MEDIUM-LOW）

- `DESKTOP/var-fda/probe_key.py`（sha256 `7baa4d75071e40db58871e16dec8dba19e3c8e87b2c9dc3a80afed01164905f6`，783 B）在上傳內容中**硬編碼了操作者本機憑證庫路徑**：
```python
Reads API key from Hermes auth.json credential_pool at runtime; NEVER writes it
auth = json.loads(Path(r"C:\Users\user\AppData\Local\hermes\auth.json").read_text(encoding="utf-8"))
cred = auth["credential_pool"]["opencode-go"][0]
API_KEY = cred.get("secret_value") or cred.get("api_key") or cred.get("key") or ""
```
- 判定：**未內嵌任何憑證值**（該腳本只讀 `key_len`/欄位名），但公開了本機 Hermes 憑證庫位置與讀取方式 → 建議改為 env-ref 或自 mirror 排除。

## 8. 讀寫面聲明 vs 事實（over-claim register）

**root README §2 排除清單**（`FABRIC` mirror `README.md`，原文節錄）

```text
## 2. Directory map

| Path | Subject | Notes |
|---|---|---|
| `FABRIC/` | Fabric governance | contract, policy, tooling |
| `HG-KSEOS/` | HG-KSEOS control plane | curated: `src/ tests/ docs/ schemas/ scripts/ config/ requirements/ tools/` |
| `FAR/` | FAR research deliverables | research request/plan, integrated findings, root-cause, challenge, proposed evolution |
| `DESKTOP/` | Desktop-effect plane | *pending authorization-token refresh — see Sec.5* |
| `INTEGRATION/` | This integration | manifest, binding statement, acceptance entry point |

**Deliberately excluded** (not part of the acceptance surface): `var/` (working data, SQLite DBs),
`worktrees/`, `evidence/` raw stores, `.venv/`, and any `API KEY/` directory. These are runtime
state or secrets, not governance artifacts.

## 3. What an external acceptance officer can verify here

1. **The binding is real, not prose** - HG-KSEOS
```
**root README §4 claim ceiling**（`FABRIC` mirror `README.md`，原文節錄）

```text
## 4. Claim ceiling of this mirror

`MIRROR_OF_GOVERNED_ARTIFACTS_FOR_EXTERNAL_ACCEPTANCE_ONLY`

- This repository does **not** claim external acceptance, merge, release, production, or any
  live-world effect.
- Neither SWOF W2 (external `PASS_CHALLENGE`) nor W3 dispatch is claimed here.
- Credentials, tokens and connection strings are **never** mirrored.

## 5. Desktop-effect plane slice

The desktop-effect plane artifact tree is mirrored at `DESKTOP/` (adapter, routing/preflight
guards, capability matrix, asset registry, verified action-class receipts, documentation).

Curation: third-party vendored material (a downloaded distribution archive and its extraction,
~133 MB) is **excluded** - it is not a governance artifact. The scripts that operate on it are
kept.

## 6. Provenance

Mirrored from the local governed workspace `C:\Projects\Agent_Workspace` at the state where:
- HG-KSEOS co
```
**root README §5 desktop slice**（`FABRIC` mirror `README.md`，原文節錄）

```text
## 5. Desktop-effect plane slice

The desktop-effect plane artifact tree is mirrored at `DESKTOP/` (adapter, routing/preflight
guards, capability matrix, asset registry, verified action-class receipts, documentation).

Curation: third-party vendored material (a downloaded distribution archive and its extraction,
~133 MB) is **excluded** - it is not a governance artifact. The scripts that operate on it are
kept.

## 6. Provenance

Mirrored from the local governed workspace `C:\Projects\Agent_Workspace` at the state where:
- HG-KSEOS commits `c0cb5cb` (canonical acceptance resolver) and `c12412e` (ordering oracle) are HEAD.
- FAR Gate 1 = `CONFIRMS_USEFUL`; Gate 2 = authorized; controls C1-C8 implemented with an
  independent-checker PASS.
```
**FDA 主體 `README.md` 開頭（原文節錄，宣稱 EXTERNAL ACCEPTANCE GRANTED / checker 194/194 / manifest sha a3496336）**

```text
# Fabric Desktop Automation (FDA)

> **Status: ✅ EXTERNAL ACCEPTANCE GRANTED** — r11 ALL PASS (2026-08-14)
> Fabric-governed bounded Windows desktop automation · LOCAL / PAPER / NO-LIVE-WRITE

Fabric Desktop Automation (FDA) 是在 HG-KSEOS 治理下，透過純消息/背景路徑自動化 **XQ (XQ全球贏家) 與 XS (XScript)** 桌面操作的能力層——用於策略雷達建立、PAPER 策略執行、編譯驗證、log readback 與外部驗收證據產生。**全程零滑鼠搶奪、零焦點竊取、零實單交易。**

## 🏆 驗收狀態

| 項目 | 狀態 |
|---|---|
| FDA blueprint / architecture / runtime / implementation | **PASS** |
| FDA_PROFILE_TEAM_ACTIVE | **PASS**（r11 2026-08-14）|
| XQ 3.20.02-260811 exact-build | PASS |
| F01 current-build 10/10 · F06 fresh compile 10x | PASS |
| UFO² v3.0.8 effective-load 7/7 | PASS |
| PAPER single-wash 10x + terminal readback | PASS |
| final checker 194/194（evaluator 9009713）| PASS |
| canonical manifest（63 entries, sha a3496336）| PASS |
| SQS_LIVE_TRADING | **NOT_AUTHORIZED** |

## 📁 核心資產

| 資產 | 用途 |
|---|---|
| `FDA_DESKTOP_CAPABILITY_MATRIX.yaml` | action class × backend × build firewall（canonical 能力矩陣）|
| `xq_native_adapter.py` | 純消息 adapter（find_window/invoke_button/set_edit_text/press_toolbar）|
|
```
**`FDA_DIRECTORY_TREE.txt`（mirror 內）開頭 — 它自己列出 `evidence/receipts/*`，但這些檔案不在 repo 內**

```text
fabric-desktop-automation/
  FDA_DESKTOP_CAPABILITY_MATRIX.yaml
  FDA_DIRECTORY_TREE.txt
  FDA_EXECUTION_BINDING.json
  FDA_IMPLEMENTATION_EVIDENCE.md
  FDA_USER_GUIDE.md
  TEAM.md
  WO_FDA_XQ_002.yaml
  fda_lease.py
  fda_router.py
  independent_checker.py
  test_xq_action_router.py
  test_xq_build_drift.py
  test_xq_native_adapter.py
  xq_native_adapter.py
  __pycache__/
    fda_lease.cpython-311.pyc
    fda_router.cpython-311.pyc
    xq_native_adapter.cpython-312.pyc
  evidence/
    receipts/
      FDA_BOUNDED_CONTROL_LIVE_PROBE.json
      FDA_C0_READBACK_RECEIPT.json
      FDA_C2_CUA_QUALIFICATION_RECEIPT.json
      FDA_C3_UFO2_EFFECTIVE_LOAD_RECEIPT.json
      FDA_C3_UFO2_QUALIFICATION_RECEIPT.json
```
**FDA `AGENTS.md` 引用為證的收據（原文節錄）**

```text
3. **REUSE-FIRST**：任何操作前查 `FDA_ASSET_REGISTRY.json`（adapter 函數 / matrix / receipts）— 有現成資產就 CALL，禁止重寫。
F01 current 260811 10/10        = PASS（receipt: FDA_F01_CURRENT_260811_RECEIPT.json）
F06 fresh compile 10x           = PASS（FDA_F06_FRESH_10RUN_RECEIPT_RR6.json）
PAPER single-wash 10x           = PASS（FDA_XQ_PAPER_STOP_10RUN_RECEIPT_RR7.json）
```
**FAR `AGENTS.md` 狀態行（原文節錄）**

```text
# AGENTS.md — fabric-autonomous-research（FAR）agent 導航契約

> Status: **ACTIVE**（FAR-R1 PASS; external r7 2026-08-13）｜ Blueprint: FABRIC-AUTONOMOUS-RESEARCH-BLUEPRINT-20260813-R2

本檔是進入本目錄的 agent 的第一份導航契約。**先讀本檔，再讀 TEAM.md 與使用說明手冊**，然後才動工。

## 身份與角色
```

## 9. 正向可驗事實（不能只列缺口）

- **FAR canonical 單一驗收 MD 已上傳且 hash 自洽**：`FABRIC/fabric-autonomous-research/FAR_FINAL_ACCEPTANCE_EVIDENCE.md` sha256 = `b0b21ced799face772327199e5b29ca1bf016b5177a06ffe9ee1832efa653d40`（78746 B），該值被 mirror 內 6 份文件宣告（`AGENTS.md`、`README.md`、`governance/FAR_ACTIVATION_RECEIPT.json`、`governance/FAR_R8_HISTORICAL_BASELINE.md`、`governance/FAR_TRI_SOURCE_CHALLENGE_CLOSURE.json`、`FAR_FINAL_HARDENING_ACCEPTANCE_EVIDENCE.md`）。
- FAR 契約面完整：`research-product/RESEARCH_ARTIFACT_CONTRACTS.yaml` + `research-product/templates/` 22 檔（= 手冊 §5 列名的 22 個模板逐一對得上）。
- FDA 契約面完整：`TEAM.md`、`FDA_DESKTOP_CAPABILITY_MATRIX.yaml`、`FDA_EXECUTION_BINDING.json`、`FDA_ASSET_REGISTRY.json`、`governance/`（4 yaml）、`fda_router.py`、`fda_lease.py`、`xq_native_adapter.py`、`independent_checker.py` 與 33 個測試檔。
- FDA 外部複驗全文可讀：`DESKTOP/docs-fda/外部驗收報告/` 11 份（r1、r2–r7、r9_CORRECTED、r10_FIXED_CONTRACT、r11_ALL_PASS）＋ 藍圖 ＋ 8 份設計討論 ＋ 升級方案。

## 10. 獨立通道（SWARM lanes + CODEX CLI）

### 10.1 lane A / lane B（sub-agent，獨立 context）

- **`lane_a_dangling_refs.json`** sha256=`77db07b8977ff00e28aeb03fc59c92055898fd63cd37eabab0e06c6d5fd0eced`
```json
{
 "authorization": "ROUTE-WO-FDA-001",
 "source_count": 14,
 "reference_count": 40,
 "exists_in_mirror_count": 16,
 "missing_from_mirror_count": 24,
 "missing_focus_count": 22
}
```
- **`lane_a_fda_gap.json`** sha256=`4358af0fd2c8ffd52922f651a0ba9e75af68ea63a7beba9d161cccbf64f5b422`
```json
{
 "authorization": "ROUTE-WO-FDA-001",
 "mirror_count": 25,
 "local_count": 88,
 "common_count": 25,
 "missing_from_mirror_count": 63,
 "mirror_only_count": 0
}
```
- **`lane_a_fda_inventory.json`** sha256=`973c5def5e18a3a7c0fecc3d4b7311c2a920744d270db7d110d3b727ced21e83`
```json
{
 "authorization": "ROUTE-WO-FDA-001",
 "subject_root_mirror": "C:/Users/user/AppData/Local/Temp/hgk-fabric-verify/mirror/FABRIC/fabric-desktop-automation",
 "file_count": 25
}
```
- **`lane_a_fda_sha_identity.json`** sha256=`8e09a8ee4fadcbed33b093a12399be64062264c1a7cd15c64b968edef4880869`
```json
{
 "authorization": "ROUTE-WO-FDA-001",
 "common_count": 25,
 "identical_count": 2,
 "crlf_only_count": 23,
 "real_content_diff_count": 0
}
```
- **`lane_a_report.json`** sha256=`1588eeb4470dc7b59ae3598065393c858c92e21926e07b57ee0704b6ff121703`
```json
{
 "authorization": "ROUTE-WO-FDA-001",
 "report": "lane_a -- FDA subject integration audit vs remote GitHub mirror",
 "mirror_head": "60ed68a68bc7d39385e65d1aa96dcf30b47acd30",
 "mirror_subject_root": "FABRIC/fabric-desktop-automation",
 "mirrored_file_count": 25,
 "local_file_count": 88,
 "common_file_count": 25,
 "crlf_only_differences": 23,
 "real_content_differences": 0,
 "missing_from_mirror_count": 63,
 "mirror_only_count": 0,
 "missing_from_mirror_top": [
  "evidence/receipts/FDA_F01_CURRENT_260811_RECEIPT.json",
  "evidence/receipts/FDA_F06_FRESH_10RUN_RECEIPT_RR6.json",
  "evidence/receipts/FDA_XQ_PAPER_STOP_10RUN_RECEIPT_RR7.json",
  "evidence/receipts/FDA_XQ_PAPER_STOP_SEMANTICS_AUTHORITY_RR8.json",
  "evidence/receipts/FDA_CHECKER_FINAL_RR7.json",
  "evidence/receipts/FDA_XQ_BUILD_FINGERPRINT_RECEIPT.json",
  "evidence/receipts/FDA_XQ_NATIVE_QUALIFICATION_RECEIPT.json",
  "evidence/receipts/FDA_XQ_PAPER_RUNTIME_RECEIPT.json",
  "evidence/FDA_IMPLEMENTATION_EVIDENCE.md",
  "evidence/FDA_EVIDENCE_MANIFEST.json",
  "evidence/FDA_EXTERNAL_FULL_EVIDENCE_20260814.md",
  "evidence/FDA_EXTERNAL_FINAL_SINGLE_EVIDENCE_RR6.md"
 ],
 "can_external_reviewer_verify": "PARTIAL_NO"
}
```
- **`lane_b_dangling_refs.json`** sha256=`6fdd2d78a70e70f39c915c23f0305a8b7766d161020ceec6320b2be0e7350187`
```json
{
 "source_doc_count": 80,
 "distinct_references": 496,
 "exists_in_mirror": 430,
 "missing_from_mirror_refs": 66
}
```
- **`lane_b_external_status.json`** sha256=`7c8f0d102a26596e08fb2a36f058eb85b17bcdda965d9da01d1a2c40f9d02ed0`
```json
{
 "question": "Any document in the mirror stating FAR's external acceptance status?",
 "answer": "YES - multiple mirrored docs state FAR-R1 = PASS at external r7/r8.",
 "hash_note": "Mirrored FAR_FINAL_ACCEPTANCE_EVIDENCE.md raw sha256 = b0b21ced799face7... = the declared canonical-current hash; the r7/r8 historical baseline 58de0815 (76,214B) is superseded and its bytes are NOT in the mirror."
}
```
- **`lane_b_far_gap.json`** sha256=`15e53ca71fb7f0b1f9a733a6b17e5d642bd9461f5f2d54f55f12fba9d8b8aa56`
```json
{
 "local_root": "C:/Projects/Agent_Workspace/Fabric/fabric-autonomous-research",
 "mirror_root": "C:/Users/user/AppData/Local/Temp/hgk-fabric-verify/mirror\\FABRIC\\fabric-autonomous-research",
 "local_file_count": 947,
 "mirror_file_count": 905,
 "missing_from_mirror_count": 42,
 "mirror_only_count": 0
}
```
- **`lane_b_far_inventory.json`** sha256=`d753fb76b86e0fd3ac3c45ed653eee575dedb10aa1f023f9dfa62c1268098816`
```json
{
 "subject": "FABRIC/fabric-autonomous-research",
 "mirror_head": "60ed68a68bc7d39385e65d1aa96dcf30b47acd30",
 "file_count": 905,
 "total_bytes": 38551710,
 "declared_r7_baseline_58de0815": "58de08155b2565c342a3df28cfa3c2f899bd5603f7047cf51e94f0c9860738f2"
}
```
- **`lane_b_hash_compare.json`** sha256=`da39522eb8ebe83dc528c6c80d39e4cf61f3c8346b87c9a8ad44154db1f7ba84`
```json
{
 "common_file_count": 905,
 "identical_raw": 841,
 "crlf_only_differences": 64,
 "real_content_differences": 0
}
```
- **`lane_b_mirror_all.json`** sha256=`d06f51b1efdd20b2ef6bad99dc9ed5850c61a964fc878878351243a48f259dac`
```json
{}
```
### 10.2 lane C — Codex CLI（唯讀獨立裁決，第三方實作）

- 通道身分：`CODEX_HOME=%LOCALAPPDATA%\HG-KSEOS\codex-hermes`、`OPENCODEX_HOME=%LOCALAPPDATA%\HG-KSEOS\opencodex-hermes`、執行檔 `...\HG-KSEOS\runtime\codex-0.147.0-alpha.6.5\codex.exe`、`--model deepseek-v4.1-flash --sandbox read-only -c approval_policy=never --cd <mirror> exec --skip-git-repo-check --ephemeral --json`
- relay：`http://127.0.0.1:10101/healthz` = **200**（啟動前為 DOWN，本輪以 `OPENCODEX_HOME` 隔離 home 啟動）
- provider 收據：`%LOCALAPPDATA%\HG-KSEOS\opencodex-hermes\usage.jsonl` → `provider=opencode-go model=deepseek-v4.1-flash status=200`（inboundProtocol=responses, admissionKind=loopback）
- 互動證據：NDJSON 事件 {'thread.started': 1, 'error': 1, 'turn.started': 1, 'agent_message': 16, 'item.started': 50, 'command_execution': 50, 'turn.completed': 1}（其中 `command_execution`=50 次＝真實工具呼叫，非純文字回覆）
- 原始 NDJSON：`codex_lane.ndjson` sha256 `4b9c7fba1fbd53ad793c2a78a47117d1ce0afef9c71215fbcc4146426a313004`

**Codex 最終裁決（原文，已還原遮蔽後之逐字內容；sha256 `6262d72e457e471fbe2847d7e1b3bdf74766edbee0956b585ca55aa006ab778e`）**

```text
Read-only review complete. Findings:

**Key evidence**
- `FABRIC/fabric-desktop-automation/` + `DESKTOP/` hold FDA; `FABRIC/fabric-autonomous-research/` + top-level `FAR/` hold FAR.
- `DESKTOP/docs-fda/XQ用戶登入資訊.txt` contains plaintext account <REDACTED> / password <REDACTED> Both `FDA_DIRECTORY_TREE.txt` and the FAR README map declare an `evidence/` directory; neither exists (only FAR's `evidence-bundle/`).

```json
{
'fda_integrated': true,
'fda_present_scope': 'Two trees. FABRIC/fabric-desktop-automation/: README.md, AGENTS.md, TEAM.md, FDA_DIRECTORY_TREE.txt, FDA_DESKTOP_CAPABILITY_MATRIX.yaml, FDA_ASSET_REGISTRY.json, FDA_EXECUTION_BINDING.json, xq_native_adapter.py, fda_router.py, fda_lease.py, independent_checker.py, tests/test_fda_*.py, test_xq_*.py, docs/FDA_USER_GUIDE.md, governance/*.yaml. DESKTOP/: README.md, docs-fda/ (blueprint v2026.08.13-r2, 外部驗收報告 r1-r11, 討論&設計原意 1-8, 升級方案), var-fda/ scripts. Also FAR/ at top level.',
'fda_not_verifiable': 'Its declared evidence/ dir is absent: no evidence/receipts/, so F01/F06 receipts (e.g. FDA_F06_CLOSURE_V8_RECEIPT.json, FDA_F01_LIVE_FIXTURE_RECEIPT.json), PAPER/STOP/checker receipts, canonical manifest sha a3496336 (63 entries), checker 194/194, F06 10x, UFO2 7/7 and r11 ALL PASS cannot be confirmed - only named in scripts/tree/matrix. docs/FDA_USER_GUIDE.md:526 cites Fabric/evidence/review/FDA_EXTERNAL_FULL_EVIDENCE_20260814.md, which is absent. Live XQ 3.20.02 runs are not reproducible here.',
'far_integrated': true,
'far_present_scope': 'FABRIC/fabric-autonomous-research/: README.md, AGENTS.md, TEAM.md, FAR_DIRECTORY_TREE.txt, FAR_FINAL_ACCEPTANCE_EVIDENCE.md, FAR_HARDENING_* files, far_router.py, far_watchdog.py, far_source_security.py, far_trisource.py, far_retrieval.py, FAR_ROUTE_CHECK.yaml, FAR_LONG_HORIZON_CONTRACT.yaml, research-product/ (contracts+templates), methods/aris-vendor/, canary/ (8 dirs, FAR-20260813-001..007, LH-CANARY-001), governance/ (~48 receipts incl FAR_CAPABILITY_MATRIX.yaml, FAR_EXECUTION_BINDING.json, FAR_SUBJECT_ROOT_MANIFEST.json), tests/ (7 test_far_*.py), docs/ manual. Top-level FAR/far-swof-kseos-rca-001/: ResearchRequest/Plan, IntegratedFindings, LaneD_RootCause, LaneE_Challenge, ProposedEvolution, Gate1_Receipt.json, InventoryRecord.yaml, FAR_DELIVERY_RECEIPT.json, impl/acceptance_integrity_checks.py + test.',
'far_not_verifiable': 'README dir-map declares an evidence/ dir (FAR_EVIDENCE_MANIFEST.json evidence root, review package) but only evidence-bundle/ exists - evidence/ absent. The claim that FAR_FINAL_ACCEPTANCE_EVIDENCE.md is byte-identical at four mirrors is uncheckable from one mirror; manifest digests partially unreadable.',
'evidence_dir_found': false,
'credential_file_found': true,
'overclaim_found': true,
'verdict_notes': 'Credential: DESKTOP/docs-fda/XQ用戶登入資訊.txt holds account <REDACTED> and password <REDACTED> in plaintext; DESKTOP/var-fda/probe_key.py also reads an external hermes auth.json secret at runtime. No exactly-named evidence/ or review/ directory anywhere in the repo; only FAR evidence-bundle/. Overclaim: FABRIC/fabric-desktop-automation/README.md line 31 lists evidence/receipts/ and line 19 a canonical 63-entry manifest as present, and FDA_DIRECTORY_TREE.txt enumerates 28 receipts - none exist; docs/FDA_USER_GUIDE.md:526 cites an absent review file; the FAR README dir-map also lists an absent evidence/ dir. Could not read: the .lnk shortcut target (DESKTOP/docs-fda/evidence - 捷徑.lnk, binary) and .git objects.'
}
```
```

### 10.3 lane 衛生事件（誠實揭露）

- **LANE-001（已修補）**：Codex lane 在其自身 transcript 中**逐字複印了 `DESKTOP/docs-fda/XQ用戶登入資訊.txt` 的帳號與密碼值**（不該如此；憑證衛生要求任何值不得進入工件）。處置：本 MD 產出前先對 `codex_lane.ndjson` / `codex_final.txt` 做字串抹除，複驗殘留命中 = **0**；本 MD 與本輪報告**不含任何憑證值**（僅含遮罩骨架與 sha256）。
- **LANE-002**：Codex 明示無法讀取 `DESKTOP/docs-fda/evidence - 捷徑.lnk`（binary）與 `.git` 物件——已於其 verdict 內聲明，屬正確的 fail-closed 聲明。
- lane A（FDA）自我報告：其命令因 FDA 授權閘 fail-closed 被擋，改走設計中的條件 2（已登記 ACTIVE route）完成唯讀稽核，未繞過閘門。

## 11. 建議（未執行，需授權）

1. **SEC-001（先做）**：自 mirror 刪除 `DESKTOP/docs-fda/XQ用戶登入資訊.txt`（含歷史 commit 掃描）並輪替 XQ 憑證；同時把 `~/AppData/Local/hermes/attachments/Fine-grained personal access tokens.txt` 一併輪替（本機明文 PAT）。
2. **DISC-001/002**：若外部驗收官要能複算 PASS，需在**受治理路徑**（而非 `evidence/` raw store）另行發佈收據集 + `FDA_EVIDENCE_MANIFEST.json` + 外部單一證據 MD；否則應把 README/`DESKTOP/README` 的「verified action-class receipts」與 §12 引用改為明示 `EXCLUDED_FROM_MIRROR`，使聲明與事實一致。
3. **DISC-003**：修掉 mirror 內指向 `evidence/`、`evidence/review/` 的 dangling 引用，並刪除 `DESKTOP/docs-fda/evidence - 捷徑.lnk`（Windows 捷徑對 GitHub-only reviewer 無效，且可能洩漏本機路徑）。
4. **FAR**：若要外部可複核 FAR-R1，需上傳外部 r7 報告與 `FAR_EXTERNAL_REVIEW_PACKAGE_v3.zip`（或其內容摘要 + 收據）。

## 12. 本 MD 之凍結與輸入登記

### 12.1 輸入工件 sha256

| 工件 | sha256 |
|---|---|
| `repo_meta.json` | `91d1e14790bc1482778db01ee58c892a37ae797bce05b23a1fe4c79a100d6084` |
| `tree.json` | `56e89d2df32b87543fe53fd0095db898208637ccc5d0c7b74f0d1371b6a26bfd` |
| `findings_core.json` | `140286eeb158117605a7e8dd39c43de734f77ddf77ca6abfe1e887120456a9f7` |
| `local_blobs.txt` | `27242c1901d10051b1f361e1814bad350634d5f1bcdb91c2d50fee3360bf4660` |
| `mirror_blobs.txt` | `2829335b78a17f88381d29061ca25ec709b9815107ec13c691b4a5ea6d34e7bb` |
| `codex_prompt.txt` | `305283348120dceab5bd47f06af58ad3bcb2942987ff66ca22f05b1f1f33e76f` |
| `lane_a_dangling_refs.json` | `77db07b8977ff00e28aeb03fc59c92055898fd63cd37eabab0e06c6d5fd0eced` |
| `lane_a_fda_gap.json` | `4358af0fd2c8ffd52922f651a0ba9e75af68ea63a7beba9d161cccbf64f5b422` |
| `lane_a_fda_inventory.json` | `973c5def5e18a3a7c0fecc3d4b7311c2a920744d270db7d110d3b727ced21e83` |
| `lane_a_fda_sha_identity.json` | `8e09a8ee4fadcbed33b093a12399be64062264c1a7cd15c64b968edef4880869` |
| `lane_a_report.json` | `1588eeb4470dc7b59ae3598065393c858c92e21926e07b57ee0704b6ff121703` |
| `lane_b_dangling_refs.json` | `6fdd2d78a70e70f39c915c23f0305a8b7766d161020ceec6320b2be0e7350187` |
| `lane_b_external_status.json` | `7c8f0d102a26596e08fb2a36f058eb85b17bcdda965d9da01d1a2c40f9d02ed0` |
| `lane_b_far_gap.json` | `15e53ca71fb7f0b1f9a733a6b17e5d642bd9461f5f2d54f55f12fba9d8b8aa56` |
| `lane_b_far_inventory.json` | `d753fb76b86e0fd3ac3c45ed653eee575dedb10aa1f023f9dfa62c1268098816` |
| `lane_b_hash_compare.json` | `da39522eb8ebe83dc528c6c80d39e4cf61f3c8346b87c9a8ad44154db1f7ba84` |
| `lane_b_mirror_all.json` | `d06f51b1efdd20b2ef6bad99dc9ed5850c61a964fc878878351243a48f259dac` |
### 12.2 本 MD 自身雜湊（可複驗語意）

```text
self_sha256_normalized = sha256( 本檔 bytes，先將 `self_sha256: <64hex>` 這一行的值以字面 `SELF_HASH_PLACEHOLDER` 取代 )
  複驗：python -c "import hashlib,re,sys;b=open(sys.argv[1],'rb').read();print(hashlib.sha256(re.sub(rb'self_sha256: [0-9a-f]{64}',b'self_sha256: 684b2ef2d5fba34613213fe20b4c2ad9b8c6ec6fa913375288e6fffc4c059a7b',b)).hexdigest())" <本檔>

self_sha256_as_delivered = sha256( 本檔 bytes，原樣 )
```

self_sha256: 684b2ef2d5fba34613213fe20b4c2ad9b8c6ec6fa913375288e6fffc4c059a7b
