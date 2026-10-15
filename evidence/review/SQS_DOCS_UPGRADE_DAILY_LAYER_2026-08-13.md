# SQS Docs Upgrade 證據｜Daily OHLCV 資料層整合（WO-RP2-DOCS-002）

```yaml
artifact_id: SQS_DOCS_UPGRADE_DAILY_LAYER_2026-08-13
workorder: WO-RP2-DOCS-002
writer: codex（WO writer；執行 = Hermes-orchestrator 直寫 UTF-8, CODEX_EXECUTOR_FALLBACK=MOJIBAKE_DEFECT）
checker: independent AO lane（deleg_fc7004c6, VERIFY_ONLY, mutation=0）
basis: SQS_DAILY_LAYER_ACTIVATION_2026-08-13.md（d6f31949…）+ 外部 r4 GRANTED
generated_at: 2026-08-13
```

## 1. 變更內容（docs-only）

| 文件 | 變更 | SHA-256 |
|---|---|---|
| User Guide（使用說明文檔） | r5 → **r6**：header 更新、§16「Daily OHLCV 資料層」（16.1 資料集身分 / 16.2 驗收啟用 / 16.3 回測使用 / 16.4 每日自動更新 / 16.5 Claim 邊界）、211→231 tests currentness 修正 | `7bf87eb27c34dd74de72e177ef1243ae2f15e1650e93fcb4419612675166a064` |
| README.md | 新增 **§7.5 Daily OHLCV 資料層（ACTIVE）**：DSV r2 / 啟用 / 回測入口 / 每日 cron / 證據根 | `988f92954131405a9feb3d78e6bad10a07e0a1d49115c9fc1253a4ec25ac69c9` |
| AGENTS.md | v2026-08-13.1 → **.2**：§5 新增 daily-layer WO history（WO-RP2-DAILY-001..004）、**§8 Daily OHLCV Data Layer**（dataset/acceptance/backtest gate/每日更新/證據/邊界） | `768411ac981cd08d2cc729453416abb17748ba5b0b54cbebf6e5cccebaf5ecb6` |
| TEAM.md | **NO CHANGE**（評定：SQS-TEAM/1 role manifest，daily layer 為資料能力非角色/forbidden 變更；不新增欄位以保 schema） | `2b4226f4eff000d506d74e6461d5ba5b488b00c29036f573dff46fc001ca95a5` |

## 2. 品質驗證（Hermes 直寫補償控制）

- **UTF-8/CJK**：四檔 UTF-8 decode 全 PASS、0 U+FFFD；User Guide 586 CJK 字元、README 405 CJK 字元（無 mojibake——CODEX-MOJIBAKE-001 前例之補償控制）。
- **內容正確性**：DSV-DAILY-2026-08-13-r2 / 258 / 221,349 / TWSE-only / r4 GRANTED / STATUS_VECTOR_DAILY ACTIVE / backtest.duckdb / `known_at <= decision_time` / cron `d0d31ffedd07` / update_incremental 全部吻合 ground truth。
- **Docs-only delta**：porcelain 僅 User Guide（M）+ README/AGENTS（untracked, 前輪建立）；無 product/kernel 變更。

## 3. 獨立驗收（AO lane deleg_fc7004c6）

D1 User Guide r6 + §16 全要件（PASS）｜D2 README §7.5（PASS）｜D3 AGENTS .2 + §8 + WO history（PASS）｜D4 TEAM.md 維持 role manifest 原樣（PASS）｜D5 UTF-8/U+FFFD/CJK（PASS）｜D6 事實一致 + claim 紀律（PASS）→ **PASS 6/6**（read-only, mutation=0）。

## 4. Claim 邊界（不變）

```text
LOCAL/PAPER/NO-LIVE-WRITE；production NOT_CLAIMED；live trading NOT_AUTHORIZED；remote NOT_CLAIMED
daily layer = DAILY_OHLCV_LOCAL_BACKTEST_DATA_LAYER_PASS（EXTERNAL FINAL ACCEPTED, 文件反映）
```

## 5. 終止

```text
WO-RP2-DOCS-002 VERIFIED（writer=codex, checker=AO lane, mutation=0）
SQS_DOCS = CURRENT（UserGuide r6 / README §7.5 / AGENTS .2 §8 / TEAM 評定 no-change）
STOP
```
