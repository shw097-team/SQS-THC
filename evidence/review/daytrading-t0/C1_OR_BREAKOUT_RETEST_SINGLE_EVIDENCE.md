# C1 OR-Breakout-Retest 強化版 — 單一 Evidence MD

**artifact_id:** `C1_OR_BREAKOUT_RETEST_SINGLE_EVIDENCE`
**主軸:** 台股當日沖銷 T0（非隔夜）· **目標:** 下周 2026-08-24..28 可推薦方法
**建置:** 2026-08-21 · **治理:** HGK/Fabric · **工具:** KANBAN+SWARM+GSTACK/OPENSPEC+Codex CLI

## 0. Claim Ceiling
```
C1_OR_BREAKOUT_RETEST_ENHANCED_TEST_EXECUTED
強化版(vol filter/trailing/top-liquid/低slip) 實測完成
結果: IS/OOS gross 皆負 (-10.39/-9.23bp avg) -> 未翻過 63.5bp 成本牆
判 HYPOTHESIS_NOT_ESTABLISHED_T0 / REJECTED
下周 NO_TRADE default (誠實); Paper/live NOT_AUTHORIZED
```

## 1. 強化版設計（依 FAR lane1 實證）
- 前提: lane1 實測 OR(09:01-09:15)→day_hi 均值 +151bp 為結構 edge。
- 強化: ① vol filter(開盤波動≥1%) ② trailing stop(新高-1%) ③ top-liquidity(開盤15分成交額≥2億, PIT-clean) ④ slippage 重估 2.5bp → round-trip **63.5bp**。

## 2. 實測結果（minute_bars 49 權值股, PIT-clean）
- 2296 trades(IS 819/OOS 1477)
- **IS gross avg -10.39bp / OOS -9.23bp**（成本後 -73.9/-72.7bp, win 13-15%）
- **gross 負 → 未翻過成本牆** => 判 REJECTED

## 3. 關鍵科學區分（誠實）
- lane1 的 **+151bp = OR_hi→day_hi potential（可達最大高點）**；
- 實際「突破追 + trailing」的**可交易進出場為負** → **paper edge ≠ tradable edge**。
- 此為重要教訓: 潛在最大延展不可直接視為可實採之期望值。

## 4. 自迭代修補（自動化檢測→修補）
- **Codex 抓出 top-liquidity gate 用了全日成交額 → 未來資訊 PIT leak** → 修為開盤15分成交額(PIT-clean)；修正後 gross 更負、結論更穩健。
- 成本 0.00635 decimal bug → 修。

## 5. 驗收
- Codex readback: CONCERNS(PIT leak)→已修; PIT/T0/cost/honesty 餘項 PASS。
- SWARM lane0: **PASS_CONSISTENT**(重跑 hash b9e5481d…一致, REJECTED 誠實穩健)。
- SWARM lane1: 未讀到 evidence 之 C1 receipt(因在 var 未先複製)→ 已補複製, 供其核對。

## 6. Nonclaims / Stop
- 方法為研究實測; **不保證獲利**; gross 負 → 不進 Paper。
- **下周 NO_TRADE 為誠實 default**; Paper/live NOT_AUTHORIZED。
- STOP_NEXT: 若要再找可交易 edge, 需(另行 Slow-Loop MethodChange) 換訊號源/擴資料(含中小股/試撮深度)、非對本候選調參救。


