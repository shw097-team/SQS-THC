# FAR 研究報告 — opencodex daemon「常駐」vs「需要時啟動」

**WO:** WO-HGK-GPTWORK-CODEX-RESTORE-001（K6 複檢延伸研究）
**研究日期:** 2026-08-15
**研究範圍:** 「daemon 常駐加進 HGK 開機流程」vs「保持現狀（需要時手動/launcher 啟動）」——
此屬 HG-KSEOS 上游藍圖規劃的正常狀況，或是需修補的狀況？

---

## 1. 結論（摘要）

**「需要時啟動（StartOpenCodex → Hermes，session 期間存活）」是上游藍圖與既有文件規劃的
正常狀況，不是缺陷，無需修補。**「daemon 常駐加進開機流程」反而是**偏離藍圖保守態度的
提案**（HGK 對 standalone daemon / Task Scheduler 常駐有明確限制），不建議採行。

---

## 2. 上游藍圖證據（知識庫）

### 2.1 《HG-KSEOS_多智能體協作系統_本地部屬藍圖_r2.md》§5.2 — ChatGPT Desktop 三泳道

```
| Step | GPT Work / ChatGPT Desktop | Codex Local | Human |
| Auth | 說明 OAuth 分離 | 開啟 hermes setup、codex login | 完成瀏覽器登入 |
| Test | 彙總 Evidence，不自評 final PASS | 執行 runner | 驗收／拒絕／開 TT |
GPT Work 不直接取得本機 shell 權限；Codex Local 不自行批准 UAC/OAuth/SE3+。
```
→ 藍圖把「GPT Work / ChatGPT Desktop」視為受治理的**泳道**（lane），與 Codex Local 分工；
opencodex transport 屬 Codex Local 泳道的模型供應機制，**未規劃常駐服務**。

### 2.2 同藍圖 §8.2 board-binding（L635）+ L1488 + L2052 — standalone daemon 禁令

```yaml
dispatcher:
  mode: gateway_embedded
  standalone_daemon: forbidden
```
L1488: `P0 manual startup；Windows Task Scheduler only after G4 durability and explicit
service account/HITL review。不得同時 standalone daemon。`
L2052: `Assert auto_decompose: false and no standalone daemon。`

→ 這三處禁令針對 **Kanban dispatcher**（第二 orchestrator 防線），非 opencodex transport；
但它反映 HGK 對「常駐 daemon」的整體保守原則：**P0 manual startup 是基準**，常駐需 G4
durability + service account + HITL review 才允許。把 opencodex daemon 加進開機流程
（Task Scheduler / 服務）將觸及同一條審查線，**在未達 G4 前屬越權**。

### 2.3 同藍圖 §30（升級 v0.20 文件）— 路線不變

> 「Codex CLI → OpenCodex → OpenCode Go → DeepSeek V4 Flash 仍是一條合理且已被你完整
> 驗收的路線。**升 Hermes ≠ 換 Codex/OpenCodex/provider architecture。**」

→ opencodex 是受治理的 Model Transport，**維持現狀即符合藍圖**。

## 3. 既有文件規範（HG-KSEOS 使用說明文檔.md L168-171）

```
- Hermes Codex CLI 只使用 %LOCALAPPDATA%\HG-KSEOS\codex-hermes 與 opencodex-hermes。
  由 scripts\start-hgk-hermes.ps1 對自己的 process tree 注入 CODEX_HOME / OPENCODEX_HOME；
  禁止 setx 或其他全域設定。
- 驗證：... -Action Verify
- 啟動：先以 -Action StartOpenCodex 啟動隔離 transport，再以 -Action Hermes 啟動
  canonical Hermes。缺少 credential、錯誤 home、OpenCodex health failure 都 fail closed，
  不得 fallback 到 OpenAI。
```

→ **啟動序列規範 = StartOpenCodex（啟動 transport）→ Hermes（healthz gate）**。daemon 的
預期生命週期 =「需要 Codex 執行時啟動、Hermes 作業期間存活」，不是「開機即常駐」。

## 4. 原始驗收證據（8/12）

`HGK_CODEX_PROVIDER_LANE_ISOLATION_RAW.json` restart_persistence：

```json
{
  "pre_restart_listener_count": 0,
  "codex_exit_code": 0,
  "provider": "opencode-go", "model": "deepseek-v4-flash", "provider_status": 200,
  "post_probe_listener_count": 0
}
```
外部審查 MD L75: `Post-probe listener count on port 10101: 0; the affected test proxy was
stopped.`

→ **驗收時即驗證「Probe 測試後 listener 歸零」= 測試模式設計**（啟動→驗證→關閉），
日常模式另由 StartOpenCodex/Hermes 啟動序列涵蓋。`config/hermes-codex-lane.json` 的
`scope: "launcher-process-tree-only"` 亦印證：lane 的生命週期綁 launcher process tree，
**非系統常駐**。

## 5. 本次複檢實測（K6）

| 狀態 | 結果 |
|---|---|
| 複檢時 10101 | 無 listener（daemon 未啟動）= **正常待命狀態**，非故障 |
| `StartOpenCodex` 啟動 | healthz=200（version 2.11.0, pid 424, LISTENING） |
| sealed lane canary | exit=0, agent_message=HGK_ROUTE_RECHECK_OK_20260815, cached_input_tokens=11904 |
| usage receipt | provider=opencode-go / model=deepseek-v4-flash / status=200 |
| Hermes action gate | 若 daemon 未啟動會 `ERR_ISOLATED_OPENCODEX_NOT_HEALTHY` **fail closed**（設計行為） |

## 6. 判定

| 選項 | 判定 | 理由 |
|---|---|---|
| A. 保持現狀（需要時 `StartOpenCodex` → `Hermes`） | ✅ **符合藍圖/文件/驗收的正常狀況** | §5.2 泳道、§30 路線、使用說明 L170 啟動序列、launcher-process-tree-only scope |
| B. daemon 常駐加進開機流程 | ⚠️ **偏離藍圖保守原則的提案** | standalone_daemon 禁令精神 + Task Scheduler 需 G4 durability/HITL；屬新 ChangeSet 需 FAR Gate 2 決策，不建議現在做 |
| C. 修補 launcher（Hermes action 自動確保 daemon） | 🔶 可選小增強（非缺陷） | 現行 fail-closed 已是安全設計；若要減少人為步驟可加「auto-start if not healthy」，但屬產品碼變更，需 Gate 2 |

## 7. 建議

1. **維持現狀（選項 A）**：HGK 作業需要 Codex 執行時，依序 `-Action StartOpenCodex` →
   `-Action Hermes`（或直接啟動後作業）。這與上游藍圖、使用說明、8/12 驗收全部一致。
2. 若您仍希望減少手動步驟，可考慮選項 C 的最小增強（Hermes action 在 healthz 失敗時
   自動 `Start-Process` opencodex 再重試一次，仍 fail closed）——但這會改動
   `scripts/start-hgk-hermes.ps1`（產品碼），需您 Gate 2 明確授權後另立 WO 執行。
3. 本報告不宣告任何 production / 常駐 / 系統服務狀態；daemon 現為作業期間存活模式。

---

**研究來源：** 知識庫《HG-KSEOS_多智能體協作系統_本地部屬藍圖_r2.md》§5.2/§8.2/§30、
《HG-KSEOS使用說明文檔.md》L168-171、《HG-KSEOS升級Hermes v0.20.md》§30、
HG-KSEOS evidence\review\HGK_CODEX_PROVIDER_LANE_ISOLATION_*（8/12 驗收）、
本次 K6 複檢實測。
