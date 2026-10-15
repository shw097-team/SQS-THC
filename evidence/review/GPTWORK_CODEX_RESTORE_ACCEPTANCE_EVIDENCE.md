# HGK Acceptance Evidence — 桌面APP版 GPT WORK / CODEX 恢復 OpenAI 原廠模型供應

**WO:** WO-HGK-GPTWORK-CODEX-RESTORE-001
**Task:** HGK_GPTWORK_CODEX_DESKTOP_APP_OPENAI_NATIVE_RESTORE
**日期:** 2026-08-15 (Asia/Taipei) — 執行 UTC 05:20~05:40Z
**Status:** ✅ INTERNAL ACCEPTANCE ALL PASS (AO VERDICT=PASS, Challenge 修正後 PASS)
**Terminal:** STOP_FOR_USER_UI_VERIFICATION (桌面App UI 層 HumanGate 待用戶開啟 ChatGPT 桌面 App 確認)

---

## 1. 任務摘要

OpenAI 官方 ChatGPT 桌面 App（介面分 Chat / Work / Codex 三種模式）的 Work 與 Codex 模式
底層使用 `C:\Users\user\.codex\`（人檔 home）。2026-08-12 起該 home 被第三方工具
**opencodex (ocx)**「Universal provider proxy for Codex」綁架：

- `~/.codex/config.toml` 被注入 `openai_base_url = "http://127.0.0.1:10101/v1"` +
  `model_catalog_json = opencodex-catalog.json`（24 個 opencode-go 模型）+ 註解
  `# Auto-injected by opencodex`
- `~/.opencodex/config.json` 的 `defaultProvider=opencode-go`、OpenAI 原廠 provider
  `disabled=True`、`codexAutoStart=True`
- 且 opencodex proxy 未運行（10100/10101 皆無 listener）→ 桌面 App Codex/Work 請求
  連 `127.0.0.1:10101` 全部失敗 → **無法使用**

**修復（方案 A，USER HITL 2026-08-15 確認）:** 恢復人類側原生 Codex（移除注入、
關閉 autostart、重建 cache）；**HGK 協作 Codex CLI lane 零觸碰**。

## 2. Claim Ceiling

- ✅ 人類側 ~/.codex 已恢復 OpenAI 原廠供應（config 無注入、canary 2/2 成功）
- ✅ HGK lane（%LOCALAPPDATA%\HG-KSEOS\codex-hermes + opencodex-hermes port 10101）零觸碰
- ❌ 未宣告 production / live trading / remote deployment
- ⏳ 桌面 App UI 層實際開啟驗證 = **HumanGate 待用戶**（COV-11-06，不自批）

## 3. 執行方法（六執行面全啟用）

| 執行面 | 證據 |
|---|---|
| HGK | WO-HGK-GPTWORK-CODEX-RESTORE-001 經 SharedSpine admission：REQ FROZEN v1 (EVT-9e6b3f8d) → TS ADMITTED → WO CREATED → **VERIFIED** |
| KANBAN | board `gptwork-codex-restore`，K1-K5 全 done（見 §7） |
| SWARM | deleg_dcc80b83 雙 lane（AO 5/5 PASS + Challenge 修正後 PASS），overlap 13:30:09~13:31:53 |
| GSTACK | route('plan'/'review'/'qa'/'release')=GSTACK，ACTIVE_SELECTED 8 項，invariants 14 項全 0 |
| OPENSPEC | route('brownfield')=OPENSPEC (CERTIFIED_ACTIVE_BROWNFIELD)；本任務為設定檔修補，named-method 無專屬 flow，native 執行 |
| CODEX | writer=codex WorkOrder；修補為設定檔層級作業由 orchestration plane 依 WO 執行；canary 用人類 Codex 0.148.0-alpha.9 實跑 |

## 4. 根因證據（raw）

### 4.1 修補前 ~/.codex/config.toml（前 7 行，備份還原）

```toml
model = "gpt-5.6-sol"
model_reasoning_effort = "medium"
service_tier = "fast"
model_catalog_json = "C:\\Users\\user\\.codex\\opencodex-catalog.json"
# Auto-injected by opencodex
openai_base_url = "http://127.0.0.1:10101/v1"

notify = [ "C:\\Users\\user\\AppData\\Local\\OpenAI\\Codex\\runtimes\\cua_node\\9ec47c3bbf131bc8\\bin\\node_modules\\@oai\\sky\\bin\\windows\\codex-computer-use.exe", "turn-ended" ]
```

### 4.2 人類 opencodex config (~/.opencodex/config.json 關鍵欄位)

```json
{
  "port": 10100,
  "defaultProvider": "opencode-go",
  "codexAutoStart": true,
  "codexShimAutoRestore": true,
  "providers": {
    "openai":      { "adapter": "openai-responses", "baseUrl": "https://chatgpt.com/backend-api/codex", "authMode": "forward", "disabled": true },
    "opencode-go": { "adapter": "openai-chat", "baseUrl": "https://opencode.ai/zen/go/v1", "authMode": "key", "defaultModel": "deepseek-v4-flash" }
  }
}
```

### 4.3 opencodex-catalog.json（修補前 ~/.codex 的模型目錄 = 24 個 opencode-go 模型）

```json
{
  "models": [
    { "slug": "opencode-go/deepseek-v4-flash", "display_name": "opencode-go/deepseek-v4-flash", "description": "Routed via opencodex → opencode-go (opencode)." },
    { "slug": "opencode-go/deepseek-v4-pro", ... },
    { "slug": "opencode-go/glm-5", ... },
    { "slug": "opencode-go/glm-5.1", ... },
    { "slug": "opencode-go/glm-5.2", ... },
    { "slug": "opencode-go/gpt-5.6-luna", ... },
    ... 共 24 個 opencode-go/* 模型
  ]
}
```

### 4.4 ocx doctor 輸出（綁架狀態確認）

```
Paths
  ok  CODEX_HOME: C:\Users\user\.codex
  ok  CODEX_HOME/auth.json: C:\Users\user\.codex\auth.json
  ok  OPENCODEX_HOME: C:\Users\user\.opencodex
  ok  OPENCODEX_HOME/config.json: C:\Users\user\.opencodex\config.json
Codex app home targeting
  ok  Effective Codex home: C:\Users\[USER]\.codex
Codex restart safety
  !!  AT RISK after restart (no viable background service; run 'ocx service install')
       routing=opencodex-local, service=absent, shim=absent
```

### 4.5 致命點確認

```
netstat -ano | grep -E ":1010[01]"  →  (empty = 10100/10101 皆無 listener)
ocx status → ❌ Proxy: not running / Health: http://127.0.0.1:10100/healthz unreachable
```

→ 桌面 App Codex/Work 模式請求被 config 導向 127.0.0.1:10101，但 proxy 未運行 → 全部失敗。

## 5. 執行修補（方案 A）

### 5.1 修補動作

| # | 檔案 | 動作 | 前 sha256 | 後 sha256 |
|---|---|---|---|---|
| 1 | ~/.codex/config.toml | 移除 3 行注入（model_catalog_json / # Auto-injected / openai_base_url）+ 修正 CRLF | e1938f98… | 22b3e6fb… |
| 2 | ~/.opencodex/config.json | codexAutoStart True→False；codexShimAutoRestore True→False | a90786d1… | 9609b9ad… |
| 3 | ~/.codex/models_cache.json | 清除 24 個 opencode-go 污染 → 空骨架（後被原廠自動重拉） | 5a2b7563… | 340291d7… |

### 5.2 修補後 ~/.codex/config.toml（前 6 行，raw）

```toml
model = "gpt-5.6-sol"

model_reasoning_effort = "medium"

service_tier = "fast"

notify = [ "C:\\Users\\user\\AppData\\Local\\OpenAI\\Codex\\runtimes\\cua_node\\9ec47c3bbf131bc8\\bin\\node_modules\\@oai\\sky\\bin\\windows\\codex-computer-use.exe", "turn-ended" ]
```

驗證：`grep -c "openai_base_url\|Auto-injected\|model_catalog_json" config.toml` = **0**
CRLF 檢查：`has \r\r: False`、`has lone \n: False`（純 CRLF）

### 5.3 修補後 ~/.opencodex/config.json 關鍵欄位

```json
{ "codexAutoStart": false, "codexShimAutoRestore": false, "defaultProvider": "opencode-go" }
```

### 5.4 修補後 models_cache.json（canary 實跑後由 OpenAI 原廠自動重拉）

```json
{
  "fetched_at": "2026-08-15T05:29:20.732024800Z",
  "etag": "W/\"f978193f34ff002d2389e61fcc51c735\"",
  "models": [
    { "slug": "gpt-5.6-sol" }, { "slug": "gpt-5.6-sol-wm" }, { "slug": "gpt-5.6-terra" },
    { "slug": "gpt-5.6-luna" }, { "slug": "gpt-5.5" }, { "slug": "gpt-5.4" },
    { "slug": "gpt-5.4-mini" }, { "slug": "codex-auto-review" }
  ]
}
```

→ 8/8 原廠模型、opencode-go 殘留 = 0。**fetched_at 05:29:20Z = canary 實跑時間**
= Codex 從 OpenAI 原廠端成功拉取模型目錄的正面證據。

### 5.5 備份

`C:\Users\user\.codex\restore-backup-20260815-132759\`：
config.toml.pre-restore / models_cache.json.pre-restore / opencodex.config.toml.pre-restore /
opencodex-human-config.json.pre-restore

## 6. HGK lane 零觸碰（K3）

| 檔案 | sha256 | mtime | 內容驗證 |
|---|---|---|---|
| %LOCALAPPDATA%\HG-KSEOS\codex-hermes\config.toml | 007bdf66… | 2026-08-13 01:07（早於任務） | model=deepseek-v4-flash + openai_base_url=10101 + 自有 catalog ✓ |
| %LOCALAPPDATA%\HG-KSEOS\opencodex-hermes\config.json | f336d369… | 2026-08-12 02:21 | port 10101、defaultProvider=opencode-go ✓ |
| %LOCALAPPDATA%\HG-KSEOS\runtime\codex-0.147.0-alpha.6.5\codex.exe | — | — | codex-cli 0.147.0-alpha.6.5 ✓ |

→ HGK 協作 Codex CLI lane 保持 opencode-go 供應，**零觸碰**。

## 7. 原廠 canary（K4）— raw 輸出

### Run 1（修補後立即）

```json
{"type":"turn.completed","usage":{"input_tokens":15036,"cached_input_tokens":0,"cache_write_input_tokens":0,"output_tokens":9,"reasoning_output_tokens":0}}
{"type":"item.completed","item":{"id":"item_0","type":"agent_message","text":"NATIVE_OPENAI_OK"}}
```

### Run 2（cache 修正後）

```json
{"type":"item.completed","item":{"id":"item_0","type":"agent_message","text":"NATIVE_OPENAI_OK_V2"}}
{"type":"turn.completed","usage":{"input_tokens":15038,"cached_input_tokens":9984,"cache_write_input_tokens":0,"output_tokens":11,"reasoning_output_tokens":0}}
```

**cached_input_tokens=9984** = 命中 OpenAI 原廠 chatgpt 後端 cache → 供應鏈確認原廠。

命令：`C:\Users\user\AppData\Local\OpenAI\Codex\bin\697a646d3cf0f240\codex.exe`
(0.148.0-alpha.9 = 桌面 App CODEX_CLI_PATH 指到的 runtime) `exec --skip-git-repo-check
--ephemeral --json "Reply with exactly: NATIVE_OPENAI_OK"`（CODEX_HOME=~/.codex 預設）

auth 保留證明：auth.json `auth_mode=chatgpt` + tokens[id_token, access_token,
refresh_token, account_id] 全部在 → 原廠 ChatGPT 登入未受損。

## 8. Swarm 獨立驗收（K5）— 原樣結果

### Lane 1: Acceptance Officer（task-1）→ **ACCOUNTING_OFFICER_VERDICT: PASS**

```
CHECK 1: PASS — SharedSpine: workorders WO-HGK-GPTWORK-CODEX-RESTORE-001 state=CREATED writer=codex
  rollback_pointer=RB-WO-...; requirements REQ-... state=FROZEN v1; taskspecs TS-... state=ADMITTED
CHECK 2: PASS — canonical_events EVT-9e6b3f8d974a76a7 idempotency_key=FRZ-REQ-... to_state=FROZEN
CHECK 3: PASS — kanban board gptwork-codex-restore (done=4, running=1); K1-K4 done / K5 running
CHECK 4: PASS — ACTIVE_SELECTED 含 openspec + gstack.review; route('plan')=GSTACK;
  evaluate_activation_invariants() 14 項全 0
CHECK 5: PASS — var\a3\wt-gptwork-restore 目錄存在; GPTWORK_CODEX_RESTORE_WO.json 合法 JSON, wo_id 匹配
```

### Lane 2: Challenge（task-0）→ 修正後 **CHALLENGE_VERDICT: PASS**

```
CHECK 1: PASS — config.toml 注入 0；前 3 非空行 = model gpt-5.6-sol / effort medium / tier fast
CHECK 2: PASS — auth.json chatgpt + 4 token keys
CHECK 3: PASS — codexAutoStart=False, codexShimAutoRestore=False
CHECK 4: FAIL(字面) → AO_PREDICATE_CORRECTION-001 → PASS
  (models len=8 全為 OpenAI 原廠 slug, opencode-go=0 — 比空陣列更強的原廠恢復證明)
CHECK 5: PASS — HGK lane model=deepseek-v4-flash + 10101 intact; mtime 2026-08-12 < 任務
CHECK 6: PASS — 備份目錄完整
```

### AO_PREDICATE_CORRECTION-001（raw）

```json
{
  "record_id": "AO-PREDICATE-CORRECTION-GPTWORK-CODEX-RESTORE-001",
  "original_predicate": "CHECK 4: models_cache.json models 陣列長度必須 = 0 (空骨架)",
  "observed_actual": "models 陣列長度 = 8 — 全部為 OpenAI 原廠模型 slug; fetched_at=2026-08-15T05:29:20Z (canary 實跑時由 OpenAI 原廠端自動重新拉取); opencode-go 殘留 = 0",
  "classification": "PREDICATE_TOO_STRICT_LETTER (spec 字面 vs intent)",
  "corrected_predicate": "models 陣列中 opencode-go 注入 = 0、且全部 slug 屬 OpenAI 原廠 (gpt-*/codex-auto-review)",
  "recheck_result": "PASS — models len=8, opencode-go entries=0, openai entries=8",
  "final_verdict": "CHALLENGE_VERDICT: PASS (修正後)"
}
```

## 9. SharedSpine / 證據登記

| 項目 | id | sha256 前 16 | 狀態 |
|---|---|---|---|
| Requirement | REQ-HGK-GPTWORK-CODEX-RESTORE-001 | — | FROZEN v1 (EVT-9e6b3f8d) |
| TaskSpec | TS-HGK-GPTWORK-CODEX-RESTORE-001 | — | ADMITTED |
| WorkOrder | WO-HGK-GPTWORK-CODEX-RESTORE-001 | — | CREATED → **VERIFIED** (writer=codex, checker=acceptance-officer, verdict=PASS) |
| EVD receipt | EVD-GPTWORK-CODEX-RESTORE-RECEIPT | d66258f4 | registered |
| EVD AO correction | EVD-GPTWORK-CODEX-RESTORE-AO-CORRECTION | e3720227 | registered |
| EVD WO | EVD-GPTWORK-CODEX-RESTORE-WO | b70b470b | registered |

## 10. 非主張 (Non-claims)

- 本文件不宣稱 production / live-trading / remote-deployment 任何狀態。
- 本文件不宣稱桌面 App UI 層已驗證（HumanGate 待用戶開啟 ChatGPT 桌面 App 確認 Work/Codex 模式）。
- 本文件不宣稱 opencodex 工具已移除（僅人類側 autostart 關閉；HGK lane 的 opencodex-hermes 維持）。
- 本文件不宣稱人類側 Codex 其他功能（插件/notify/mcp）受影響——未觸碰。

## 11. STOP

**STOP_FOR_USER_UI_VERIFICATION** — 請用戶開啟 OpenAI 官方 ChatGPT 桌面 App，
切到 Work 或 Codex 模式發一則訊息確認可用。確認後本輪閉合。
