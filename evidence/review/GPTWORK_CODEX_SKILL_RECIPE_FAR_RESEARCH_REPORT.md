# FAR 研究報告 — 「桌面App Codex 恢復流程」是否需存成精簡 skill recipe？

**WO:** WO-HGK-GPTWORK-CODEX-RESTORE-001（K6 延伸研究 #2）
**研究日期:** 2026-08-15
**研究問題:** 「若日後又出現桌面 App Codex 無法使用…需要我把這次的完整流程存成更精簡的
skill recipe 供未來複用嗎？」— 是否真的需要？是否對之後有實質效率幫助？

---

## 1. 結論（摘要）

**不需要再新建任何 skill recipe——因為本次任務期間已經有 4 份重疊資產被寫入**
（1 份 codex skill pitfalls + 3 份 hgk skill references，皆由本任務的並行 session 各自
寫成）。這是 skill 已記錄的 **parallel-session skill-dir drift** 陷阱。真正需要的不是
「再建一份精簡 recipe」，而是**收斂去重**：選一份 canonical、合併 unique delta、刪除
重複、統一 SKILL.md 路由。

未來複用的**實質效率幫助：有**（復發情境真實存在），但**已由既有資產覆蓋**——收斂後
一份 canonical recipe 即可，無需新檔案。

---

## 2. 現況盤點：已存在的 4 份重疊資產（皆 2026-08-15 本任務期間寫入）

| # | 資產 | 位置 | 時間 | 內容 | 狀態 |
|---|---|---|---|---|---|
| 1 | codex skill「Pitfalls」區 | `skills/autonomous-ai-agents/codex/SKILL.md` L155-184 | 13:3x（本 session patch） | 精簡版：診斷 3 步 + 恢復 5 步 + 隔離鐵律 | ✅ 已存在 |
| 2 | `references/opencodex-codex-home-hijack.md` | hgk skill references | 13:22（並行 session） | 診斷 8 步 + **ocx CLI surface 完整表格** + restore 方案 A/B（PROPOSED 版） | ✅ 已存在，SKILL.md L1145 已路由 |
| 3 | `references/opencodex-human-home-hijack-restore.md` | hgk skill references | 13:42（並行 session） | **驗證版完整 recipe**（CRLF trap、fetched_at RFC3339、K6 route recheck、ERR_CODEX_ROUTE_EXIT_ 假警報、evidence shape） | ✅ 已存在，SKILL.md L848 已路由 |
| 4 | `references/gptwork-codex-desktop-restore.md` | hgk skill references | 13:50（並行 session） | **中文版最完整**（含 FAR daemon 判定 §L36-42、驗收模式、HumanGate） | ✅ 已存在，**SKILL.md 未路由** |

→ **4 份內容重疊率約 85%**，均涵蓋同一主題：opencodex 綁架人類 `~/.codex` → 診斷 →
恢復（方案A）→ HGK lane 零觸碰 → canary 驗證。

## 3. 評估：是否「真的需要」？

### 3.1 復發情境是否真實？→ 是
- `ocx` 工具**仍安裝**在系統（`%APPDATA%\npm\opencodex`），autostart 已關但 `ocx start` /
  `ocx ensure` / `ocx sync` 都可能**重新注入**人類 config（研究報告 §6 已確認）。
- 未來若再跑 `ocx start`、或重新安裝/更新 opencodex，綁架會復發 → **診斷+恢復流程有複用價值**。

### 3.2 既有資產是否已覆蓋？→ 是（已 4 倍覆蓋）
- 精簡層（codex skill pitfalls）：診斷/恢復/隔離三要點，適合「快速想起」。
- 完整層（references ×3）：含所有陷阱（CRLF、RFC3339、Probe 假警報、daemon 重啟）。
- **結論：再建第 5 份 = 負資產**（路由分裂、維護成本、與 skill 的 reuse-first / 去重原則衝突）。

### 3.3 對之後的實質效率幫助 → 有，但來自「收斂」而非「新建」
- 收斂後：未來 session 載入 1 份 canonical recipe（含全部陷阱）→ 診斷 10 分鐘內完成。
- 不收斂：4 份並存 → 未來 session 不知道該看哪份、SKILL.md 路由混亂、更新要改 4 處。

## 4. 建議方案（收斂，非新建）

依 skill 的 parallel-session drift 處理慣例（merge unique delta + delete duplicate，
reuse-first）：

| 步驟 | 動作 |
|---|---|
| 1 | 選 **canonical = `references/opencodex-human-home-hijack-restore.md`**（90 行驗證版，陷阱最全） |
| 2 | 從 #2 merge unique delta：**ocx CLI surface 完整表格**（restore/uninstall/stop/start/ensure/shim 語意） |
| 3 | 從 #4 merge unique delta：**FAR daemon 判定段落**（L36-42，藍圖§5.2/§8.2/§30 + 使用說明 L168-171 引證） |
| 4 | 刪除 #2、#4 兩份重複（內容已併入 canonical） |
| 5 | SKILL.md 路由統一指向 canonical 單一檔案（L848/L1145 合併為一處） |
| 6 | codex skill pitfalls 保留（精簡層，與 canonical reference 分層不衝突） |
| 7 | 驗證：canonical 檔 frontmatter/結構完整、SKILL.md 路由唯一、無殘留重複 |

**不建議**的選項：
- ❌ 新建「更精簡 skill recipe」（第 5 份重複）
- ❌ 刪除 codex skill pitfalls（它是精簡層，與完整 reference 分層是健康結構）

## 5. 判定

| 問題 | 答案 |
|---|---|
| 是否真的需要存成精簡 skill recipe？ | **不需要新建** — 4 份重疊資產已存在 |
| 是否對之後有實質效率幫助？ | **有**，但來自「收斂為 1 份 canonical」而非「新增」 |
| 建議動作 | 收斂去重（merge 3 份 → 1 份 canonical + 統一路由），零新增 |

---

**研究來源:** 本 session 實測（skill 目錄盤點、4 份資產內容比對、mtime 證據）、
hgk-governed-execution skill「parallel-session skill-dir drift」pitfall（L858-865 區）、
上一輪 FAR daemon 研究報告（復發情境 §6）。
