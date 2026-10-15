# 《SQS-THC & TW-ICT_FSDT-Stack 使用說明文檔》

- 版本：2026-08-10 r1（REFERENCE PROJECT-001 local delivery）
- Reference Project ID：`HGK-REFERENCE-PROJECT-001`
- 最終裁決：`SQS-THC_TW-ICT_FSDT_STACK_LOCAL_DELIVERY_PASS`（canonical reducer 15/15，exit 0）
- Claim Ceiling：Production `NOT_CLAIMED`；Live Trading `NOT_AUTHORIZED`；Remote Deployment `NOT_CLAIMED`
- Canonical authority：`C:\Projects\Agent_Workspace\SQS-THC\SSOT`（P0-CIP PACK r2 為最高產品決策；原始檔為 authority）

---

## 1. 這是什麼

SQS-THC 是受治理的台灣 ICT 當沖／隔日沖量化研究與執行棧，TW-ICT_FSDT-Stack 是其金融契約與技術內核。本專案依 P0-CIP r2（36 章／27 MC／15 TaskSpec）在本地完成施工、驗收與交付，並以 HG-KSEOS Autonomous Project Lifecycle 全流程實證（REFERENCE PROJECT-001 / real external system dogfooding）。

## 2. 目前狀態

| 項目 | 狀態 | 證據 |
|---|---|---|
| Lifecycle | EXECUTING（15 WorkOrders admitted） | SQS-THC_WORKORDER_ADMISSION.json |
| Source Inventory | 161,099 files / 8.8GB 全量 sha256 | SQS-THC_SOURCE_INVENTORY.json |
| Knowledge Preload | 376 files → 354 docs promoted（22 quarantined 為 security 範例攔截，0 failed） | SQS-THC_KNOWLEDGE_PRELOAD.json |
| Engineering Base | 6 子系統全量 disposition（REUSE×2/ADAPT/PATCH/MIGRATE/QUARANTINE） | SQS-THC_ENGINEERING_BASE_DISPOSITION.json |
| Kanban | board `sqs-thc-ref-001`，15 cards，5 delivered(done) | SQS-THC_KANBAN_EVIDENCE.json |
| gstack | named-method router → plan-eng-review 真實執行（advisory） | SQS-THC_GSTACK_EVIDENCE.json |
| 施工 | 5 核心 kernels（FSDT/temporal/knowledge/harness/capability）37/37 tests | 5× INDEPENDENT_READBACK |
| 整合 suite | 5/5 suites INTEGRATED_GREEN | SQS-THC_INTEGRATED_SUITE_RESULT.json |
| Package | 7.7MB / 19 payload / SHA 470fed2e / 獨立 readback PASS | SQS-THC_LOCAL_PACKAGE_READBACK.json |
| Reducer | **15/15 PASS → LOCAL_DELIVERY_PASS（exit 0，兩次獨立 run）** | SQS-THC_REDUCER_DECISION.json |

## 3. 目錄結構

```
SQS-THC/
├── SSOT/                  # 產品權威源（P0-CIP PACK、RBWI_WP G01-G07、實作前開發文檔）
├── 技術資料庫/            # 工程開發文檔 DOC-00..12、專業技術文檔、設計開發、市場資料
├── 工程基座/              # PRIMARY_ENGINEERING_BASELINE（ICT-OBI、TriRAG、Spartoi 等 6 子系統）
├── 實作執行/
│   ├── worktrees/         # 5 個 kernel 施工 worktree（git repo，獨立 commit）
│   ├── SQS-THC_*.json     # 全部 evidence（inventory/preload/disposition/kanban/gstack/reducer）
│   ├── SQS-THC_LOCAL_DELIVERY_CANDIDATE.zip
│   └── SQS-THC_TW-ICT_FSDT-Stack使用說明文檔.md
└── sqs_thc/               # 施工產物（kernel packages；目前於 worktrees 內）
```

## 4. 快速開始（使用者旅程）

1. 查閱權威：`SSOT/SQS-THC_P0-CIP-PACK_v2026.08.06-r2.md`（36 章 / 27 MC / 15 TaskSpec）
2. 查閱交付包：`實作執行/SQS-THC_LOCAL_DELIVERY_CANDIDATE.zip`（19 payload，含 evidence + User Guide）
3. 執行任一 kernel 測試：`cd 實作執行/worktrees/ts-ref-0X && python -m unittest discover -s tests -t . -v`
4. 全文檢索知識庫（若有 Hermes runtime）：KnowledgeFactory search（354 docs，source-bound）

## 5. 已交付 kernels（P0-CIP source binding）

| WorkOrder | 章節 | Kernel | Tests | 獨立 readback |
|---|---|---|---|---|
| WO-TS-REF-02 | CH04 | FSDT Financial Contract（FinancialContract/InstrumentIdentity/PriceQuantityValue、RAW→NORMALIZED→PIT_VALIDATED、ERR_CURRENCY_MISMATCH 等） | 8/8 | INDEPENDENT_CASE_PASS |
| WO-TS-REF-03 | CH06 | Temporal/Five Clocks/PIT/交易日曆（event≤availability≤decision≤execution、ERR_LOOKAHEAD 等） | 7/7 | INDEPENDENT_CASE_PASS |
| WO-TS-REF-04 | CH10 | Knowledge/RAG/Memory/Provenance（INGESTED→CHUNKED→INDEXED、ERR_BROAD_LOCATOR/ERR_CONTEXT_POISONING 等） | 7/7 | INDEPENDENT_CASE_PASS |
| WO-TS-REF-05 | CH15 | Harness/Loop/Handoff（DAG、iteration budget、ACK/NACK、HUMAN_REVIEWED merge） | 8/8 | INDEPENDENT_CASE_PASS |
| WO-TS-REF-06 | CH16 | Capability/Tool Lifecycle（CANDIDATE→DESIGNATED→QUALIFIED、ERR_PROVIDER_UNQUALIFIED 等） | 7/7 | INDEPENDENT_CASE_PASS |

## 6. 自動 vs HITL

- 自動：source scan、planning、routing、施工（Codex bounded）、測試、repair、evidence、checker、reducer
- HITL（本輪未觸發）：credential、admin/UAC、外部不可逆 side effect、authority conflict、production

## 7. 權威與治理

- A1 產品決策：SSOT P0-CIP r2 → A2 實作前開發文檔包 → A3 工程/技術文檔 → A4 RBWI_WP G01-G07 → A5 HG-KSEOS control corpus
- 原始檔為 canonical；Knowledge projection 可 rebuild/withdraw，不形成第二 SSOT
- Maker≠Checker：每 WorkOrder 有獨立 readback；package 有獨立 readback；reducer 兩次獨立 run

## 8. 驗收與 Release

- 每 WorkOrder：maker suite green + `INDEPENDENT_CASE_PASS`（fresh subprocess + frozen test hash 驗證）
- 整合：5/5 suites `INTEGRATED_GREEN`
- Package：zip + manifest + 獨立 readback（same SHA / exact set）
- Reducer：`SQS-THC_TW-ICT_FSDT_STACK_LOCAL_DELIVERY_PASS`（15/15，exit 0）
- `PRODUCTION = NOT_CLAIMED`；`LIVE_TRADING = NOT_AUTHORIZED`；`REMOTE_DEPLOYMENT = NOT_CLAIMED`

## 9. Rollback / Restore

- 每個 worktree 是獨立 git repo：`git reset --hard <pre-seed commit>` 可完整還原 pre-seed 骨架
- HG-KSEOS spine：rollback_pointer + compensating events（LGR 語意）
- Knowledge projection：`withdraw_source(source_id)` → `rebuild()` 可撤回並重建
- Package：pre-seed commits 保留於各 worktree git history（a31199c / ee4c12f / d0392a8 / 5b8b81b / eec0657）

## 10. 已知限制與 dogfooding gaps（已送 Governed Evolution）

1. **lifecycle.admit_workorders req_id collision**（EVO-SIG-32D2CAA8）：`REQ-{project尾段}` 與既有 `REQ-001` 碰撞；except 只捕 InvariantViolation 不捕 IntegrityError → 以 spine API workaround
2. **CLI project advance 未接 plan/admit**（EVO-SIG-509F4856 同源）：`_derive_tasks` 只認英文 keyword，中文 goal 只產生 2 generic tasks → 以 source-backed 15 TaskSpec 手動 admission 補足
3. **register_requirement FK 前置**：lifecycle start 未建 `projects` row → 需先 `create_project`
4. Windows Codex sandbox 在 gateway context 無法 spawn（CreateProcessAsUserW error 5）→ 使用 `--sandbox danger-full-access` + process boundary
5. 市場資料（台股價格歷史資料）與 1.2GB duckdb 不納入 delivery package（gstack advisory A1 已記錄）
