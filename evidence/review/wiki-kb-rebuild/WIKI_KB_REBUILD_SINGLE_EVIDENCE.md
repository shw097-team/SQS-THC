# SQS-WIKI 知識庫重建（消失後半段復原）— 單一外部審查證據

- **WO**: `WO-SQS-WIKI-REBUILD-001`（SPINE, writer=codex, state=CREATED, RB pointer）
- **Board**: `sqs-wiki-kb-rebuild`（K1..K5；K1..K4 done, K5 AO 驗收）
- **日期**: 2026-08-21（週五）；**觸發**: 模型用量耗盡後「TW-ICT專業技術文檔→WIKI+KG→SQS抽取當沖技術→方法/策略/參數」後半段遺失
- **Claim ceiling**: `RESEARCH_ONLY`；無 live / production / broker write 宣稱

---

## 1. 背景（FAR 調查結果）

模型用量耗盡（deepseek-v4-flash 429/quota）中斷後續跑；重開後「知識庫→抽取→策略/參數制定」後半段指令與執行內容在 conversation 遺失。FAR 三源調查（on-disk wiki + 歷史 session + skill）確診缺口：
1. **【5】ICT 專業技術文檔_v6.0**（14 DOC, 58k 行, 12MB）未入 wiki（authority 只到【4】）
2. **知識圖譜（KG）**未建
3. **SQS 從知識庫抽取當沖技術→方法/策略/參數制定**無 wiki-based 產物

## 2. 治理執行（KANBAN / SWARM / GSTACK / OPENSPEC / CODEX）

- **admission**: REQ→FROZEN→TS→WO-SQS-WIKI-REBUILD-001（writer=codex, CREATED）
- **Kanban**: board `sqs-wiki-kb-rebuild` DAG（K1 admission → K2/K3 並行抽取 → K4 KG+lint → K5 驗收）
- **SWARM（多子代理並行, deleg_bea96696, 3 lanes）**:
  - Lane-0 v6 抽取（raw/ict-v6 16 files + 3 v6 concepts）
  - Lane-1 知識圖譜（queries/knowledge-graph.md, 13 nodes/48 edges）
  - Lane-2 方法策略（queries/sqs-method-strategy-from-wiki.md + strategies/sqs-wiki-derived-params.yaml, 2 methods/27 params）
- **GSTACK/OPENSPEC**: registry `CERTIFIED_ACTIVE`（plan-eng-review/review/qa + openspec BROWNFIELD）；route=NATIVE, evidence receipt `ROUTE_GSTACK_OPENSPEC_WIKI_KB_REBUILD.json`
- **Codex**: WO writer=codex；lane 產出由 skill 驅動 worker 實作

## 3. 產出（raw index, primary home `SQS-THC/evidence/wiki-kb-rebuild/` + wiki）

| 產出 | 路徑 | 數量/狀態 |
|---|---|---|
| v6 raw 來源 | `wiki/raw/ict-v6/` | 14 DOC + summary + sources = 16 files |
| v6 concept 頁 | `wiki/concepts/ict-v6-{mainline-method,module-system-adapter,risk-gates}.md` | 3（>3KB, 實質） |
| 知識圖譜 | `wiki/queries/knowledge-graph.md` | 13→16 nodes（AO observation 已增 v6 節點） |
| 方法策略 spec | `wiki/queries/sqs-method-strategy-from-wiki.md` | 1（wiki 推導, type=query） |
| 策略參數 YAML | `SQS-THC/strategies/sqs-wiki-derived-params.yaml` | 2 methods / 27 param-leaf, RESEARCH_ONLY |
| index/log | `wiki/index.md`, `wiki/log.md` | 16 concepts + 2 queries + 8 raw summaries, log 已 append |
| route receipt | `ROUTE_GSTACK_OPENSPEC_WIKI_KB_REBUILD.json` | 1 |

## 4. 自動檢測 / 自迭代修補

- **Maker 檢測**: 3-lane 產出後全庫掃描 → 發現 `sqs-method-strategy-from-wiki` 未入 index → **修補**（補 index 條目 + Total pages 16+2+8）→ re-verify 全閉合
- **AO observation 閉合**: KG 圖譜原僅 13 nodes（未含 3 v6 頁）→ **增列 v6 三節點**, 反映 16-concept 全貌；此非阻擋。
- **最終閉合**: dangling wikilinks = 0（218 出現次全解析）；16 concepts 全有 frontmatter + ≥2 wikilinks + 在 index；params YAML parse OK。

## 5. 獨立驗收（Acceptance Officer, VERIFY_ONLY, fresh-context, deleg_6c67773c）

**7/7 主項 PASS + 2/2 非主張 PASS → 驗收通過**
- raw/ict-v6 16 files ✓ / 3 v6 concepts 實質 ✓ / KG 13-16 nodes+48 edges ✓ / method query wiki-推導 ✓ / params YAML 2 methods+source+RESEARCH_ONLY ✓ / index 16+2 ✓ / 0 dangling ✓
- 非主張: (a) 無 live/live_trading/broker write ✓ (b) v6 未宣稱 production（僅「supersedes v3 的工程化版」）✓

## 6. Non-claims（honest 界線）

- `RESEARCH_ONLY`：方法/策略/參數僅為知識庫研究制定，**不得作為 live/paper 執行**。
- 無 live / production / broker write / 自動憑證宣稱。
- v6 定位為「v3 的工程化規格再製」，非 production 抬升。

## 7. 證據

- 本單一 evidence MD：`SQS-THC/evidence/wiki-kb-rebuild/WIKI_KB_REBUILD_SINGLE_EVIDENCE.md`
- Mirror roots（byte-identical）：`HG-KSEOS|SQS-THC|Fabric/evidence/review/wiki-kb-rebuild/`

## 8. STOP / 接續

- 下半段已復原完成並 freeze（RESEARCH_ONLY）。未宣稱 production / live。
- 後續（如需要）：v6 節點入 KG 已做；SQS 資料層回測校準參數（CALIBRATION_REQUIRED 標記）為下一階段。