---
decision_id: UD-GPTWORK-CODEX-RESTORE-CONFIRM-2026-08-15-001
authority: USER
decided_at: 2026-08-15T14:00:00+08:00
status: CLOSED
supersedes: null
supersession_basis: null
bound_into: WO-HGK-GPTWORK-CODEX-RESTORE-001
---

# USER CONFIRMATION — 桌面APP版 GPT WORK / CODEX 恢復 OpenAI 原廠供應

## 用戶確認內容（HumanGate 通過）

> 用戶於 2026-08-15 實際開啟 OpenAI 官方 ChatGPT 桌面 App，切到 **Work 與 Codex 模式**發送訊息，
> **均可正常回覆**。整輪正式閉合。

## 綁定證據

| 項目 | 值 |
|---|---|
| WorkOrder | WO-HGK-GPTWORK-CODEX-RESTORE-001 (state=VERIFIED) |
| 接受證據 MD | GPTWORK_CODEX_RESTORE_ACCEPTANCE_EVIDENCE.md (sha256 1656620ef0d706260c52fa675c39ada5f4766b7dc490ef5061b773578e465e18) |
| 根因 | opencodex (ocx) 將人類 ~/.codex 綁架為 opencode-go 供應（注入 10101 base_url + 24 opencode 模型目錄 + openai provider disabled），且 proxy 未運行 → 桌面App無法使用 |
| 修補（方案A） | 移除 ~/.codex/config.toml 注入、關閉 ~/.opencodex/config.json codexAutoStart/codexShimAutoRestore、重建 models_cache（由 OpenAI 原廠自動重拉 8 個原廠模型）；HGK Codex CLI lane（%LOCALAPPDATA%\HG-KSEOS\codex-hermes + opencodex-hermes port 10101）零觸碰 |
| 驗證 | 原廠 canary 2/2 PASS（cached_input_tokens=9984 = OpenAI chatgpt 後端）；Swarm AO 5/5 PASS + Challenge 修正後 PASS（AO_PREDICATE_CORRECTION-001）；SharedSpine WO VERIFIED |

## 閉合狀態

- ✅ 內部驗收 ALL PASS
- ✅ HumanGate 用戶 UI 層驗證 PASS（本記錄）
- ✅ 證據 MD 4 份 byte-identical mirror（HGK/SQS/Fabric evidence\review + var\a3 主檔）
- ✅ HGK Codex CLI lane 保持 opencode-go 供應（零觸碰）

本輪 **CLOSED**。
