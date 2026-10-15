# 手動切換模型供應（軌道①）—— 指令文件

> WO-HGK-PFR-001 · UD-PFR-2026-08-23-001 · 2026-08-23
> 目的：解除「只能停留在 opencode-go」的困局。核心不是鎖，而是**憑證 + 指令**。
> 條件：目標 provider 必須已有憑證（例如在 `~/.hermes/.env` 設 `OPENROUTER_API_KEY`）方可啟用。

## 為何之前換不過去（簡述）

- `.env` 只有 `OPENCODE_GO_API_KEY`，其餘 provider 無憑證 → Hermes runtime/picker 不啟用無憑證 provider。
- `hermes model` 是**純互動式** picker，桌面/gateway 情境難非互動驅動。
- 每一 session 都吃 config 預設（`model.provider: opencode-go` / `model.default: deepseek-v4-flash`）。

## 非互動切換指令

```bash
# 切到 OpenRouter 免費模型並設為全域預設（下次 session 生效）
hermes model z-ai/glm-5.2:free --provider openrouter --global

# 僅本次 session 使用
hermes model z-ai/glm-5.2:free --provider openrouter

# 或以 config 直接設預設
hermes config set model.provider openrouter
hermes config set model.default z-ai/glm-5.2:free

# 查看現況
hermes model
hermes fallback list
```

### 語意重點（來自 hermes model_switch）
- Provider 切換**只用 `--provider` flag**；沒有 `provider:model` 冒號語法。
- `--global`：持久化到 config 為預設；`--provider` 無 `--global` → 僅 session。
- 切換後**影響下一 session**；執行中的 session 保留已釘模型（session 內用 `/model <m> --provider <p>`）。

## 現實上最自動的做法（根本解 ③）

無須手動切：`fallback_providers` 已含**跨 provider** OpenRouter 免費逃生線。
opencode-go 額度 / 5小時窗 / 429 / 5xx / 401 / 403 / 404 / 連線失敗時，Hermes
自動（且 reset-aware）切到 `z-ai/glm-5.2:free`（第二線 `nemotron-3.5-lightning:free`），
並依 `provider-failover-emergency-checkpoint` skill 對執行中任務做緊急存檔 + 中斷點，
下次可 `/resume` 續跑。

## 其他 provider 要能切

想用 Anthropic / DeepSeek / Google 等當 primary，就需在 `.env` 提供對應 key
（`ANTHROPIC_API_KEY`、`DEEPSEEK_API_KEY`、`GOOGLE_API_KEY`…），再用上面指令切換。