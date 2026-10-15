# Corporate Action 政策｜DSV-DAILY-2026-08-13-r2

```yaml
artifact_id: CORPORATE_ACTION_POLICY_DAILY_2026-08-13
workorder: WO-RP2-DAILY-002
binding_finding: DA-EXT-003
state: RAW_UNADJUSTED_ONLY
owner: SQS-THC / TW-ICT FSDT-Stack owner
checker: independent acceptance officer
generated_at: 2026-08-13
```

## 1. 狀態宣告：RAW_UNADJUSTED_ONLY

本 DSV（DSV-DAILY-2026-08-13-r2）為 **TWSE 官方原始（未調整）EOD OHLCV**：

- 無除權息/分割調整因子；
- 無 CorporateActionEvent 串流；
- 無 AdjustmentMethodProfile（method/version/fixtures/replay evidence 皆無）；
- raw series 為官方原始值逐列保存（price 為官方原始報價，未做任何 continuity 調整）。

## 2. Typed BLOCK（調整相依 consumer 之硬性限制）

凡**相依於 total-return 或除權息/分割調整連續性**之回測/策略，**不得直接消費本 DSV**；於策略 admission gate 即 typed BLOCK，直到具來源與版本的治理路徑提供：

```text
CorporateActionEvent（source 綁定 + 版本 + hash）
+ AdjustmentMethodProfile（method + version + fixtures + replay evidence）
+ 獨立 checker 驗證
（依上游 TW-ICT DOC-06 Part 7）
```

BLOCK 為 typed 宣告：調整相依 consumer 若未經上述路徑即消費本 DSV 未調整序列 → **FAIL_CLOSED**（負例：split-adjusted 連續性回測直接吃 raw unadjusted 序列 = 缺陷候選）。

## 3. 保留與未來路徑

- raw series 不可變保存（11,352 artifacts，逐窗 sha256 receipts 綁定）→ 未來任何 adjusted series 可由 raw 重建，**不需重新下載**。
- 本政策不阻擋**價格變動率/報酬率**層級（以同序列 close 相除）的研究使用——只要該使用不宣稱除權息調整正確性；任何宣稱 total-return 正確性的分析必須先解除上述 BLOCK。
- 若後續建立 adjusted 層，將以新 DSV semantic version（r3+）發布並保留本 r2 原貌，**絕不原地改寫 sealed snapshot**（對應 DOC-06 revisions → new snapshot 規則）。

## 4. 驗證

- 檢查：本政策欄位齊全（state=RAW_UNADJUSTED_ONLY、BLOCK predicate 明確、raw 保留路徑、改版規則）＝ PASS。
- 負例：調整相依 backtest 直接消費 r2 而未經 CA 路徑 → FAIL_CLOSED。
