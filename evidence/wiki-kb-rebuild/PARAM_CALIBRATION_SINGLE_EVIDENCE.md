# SQS 策略參數回測校準（CALIBRATION_REQUIRED 定值）— 單一外部審查證據

- **WO**: `WO-SQS-WIKI-REBUILD-001` 延伸（board `sqs-wiki-param-calibration`, C1..C4 全 done）
- **日期**: 2026-08-21
- **Claim ceiling**: `RESEARCH_ONLY`；無 live/production/broker write 宣稱
- **資料**: `backtest.duckdb` `minute_bars`（49 權值股, 2,793,223 rows, 2025-08-11..2026-08-10）

---

## 1. 校準範圍（原 CALIBRATION_REQUIRED 6 項全部定值）

| 參數 | 校準值 | 校準標記 | 依據 |
|---|---|---|---|
| opening_range_window | 09:01-09:15 | EMPIRICAL_OR_WINDOW | 資料指南 OR 突破最強 edge |
| r_multiple_target | 1.0 | EMPIRICAL_2026_08_RMULT | R 分佈 p70≈1.0R（11848 symbol-day, med=0.67R/p90=2.0R） |
| stop_percent | 0.010 | EMPIRICAL_2026_08_STOP | stop 掃描 winR 最高(0.30) |
| risk_per_trade_budget | 0.005 | MANAGERIAL_NOMINAL_0.5PCT | approved_qty 公式輸入（資金管理, 非市場校準） |
| screening_thresholds | vol≥500/price... | EMPIRICAL_OR_PROXY_2026_08 | 權值股 Volume 分位 proxy |
| first_hour_momentum_continuation_rate | 0.442 | EMPIRICAL_2026_08_MOMB | 資料指南 44.2%（<50% 證偽） |

**0 項 active CALIBRATION_REQUIRED**（剩 2 處為保留的校準紀律註釋，非參數值）。

## 2. 誠實核心結論（不可偽造為正）

- **方法 A（OR 突破）**: 每 day 單次突破、49 權值股、68.5bp 成本 → **NET 期望全負**。
  - 較正成本後最佳（stop=0.010/cap=0.010）→ **-77.6bp**。
  - R-multiple: up/down med=0.67R, p15=0.22R, p70=1.0R, p90=2.0R → 定 1.0R 為「最不差退出點」。
  - OR 區間相對價格 median 144.8bp（> 建議 40-120bp）。
  - **結論: 此法在權值股宇宙不可行**；校準值僅為「負期望最小」研究基準。
- **方法 B（動能延續）**: 首小時動能延續率 44.2%（<50%）→ 獨立動能延續**基本證偽**；
  對稱基準複核 19-24% 強化之。僅可作輔助確認。

## 3. 自動檢測 / 自迭代修補（AO observation 閉合）

- **AO fresh-context（deleg_17ca82ef）驗收**: PASS-with-observation。
  複算證實 11848 symbol-day、R 分佈、-11.3bp 數字（成本 10x under-subtract）。
- **缺陷**: `calibrate_strategy.py` 成本 `-6.85`（錯）應 `-68.5`（0.00685 fraction ×10000）。
  已修 → NET 期望由 -15.9bp 校正為 **-77.6bp**（更負，方向不變，誠實修正幅度）。
  同步更新 params YAML + method query 頁。
- **閉合**: YAML parse OK; 每參數有 source+calibration; claim ceiling=RESEARCH_ONLY; 無 active CALIBRATION_REQUIRED。

## 4. Non-claims（honest 界線）

- `RESEARCH_ONLY`: 定值參數為「負期望最小」研究基準，**非可實盤獲利參數**。
- 無 live/production/paper/broker write/獲利宣稱。
- 方法 A 權值股負期望與方法 B 證偽均誠實標記，未偽造正值。

## 5. 證據

- 單一 evidence MD: `SQS-THC/evidence/wiki-kb-rebuild/PARAM_CALIBRATION_SINGLE_EVIDENCE.md`
- 校準腳本: `var/rbwi-fullrun/calibrate_params.py` / `calibrate_strategy.py` / `calibrate_methodB.py`（gitignored var/）
- 定值參數: `SQS-THC/strategies/sqs-wiki-derived-params.yaml`
- Mirror roots（byte-identical）: `HG-KSEOS|SQS-THC|Fabric/evidence/review/wiki-kb-rebuild/`

## 6. 接續

- 權值股宇宙方法 A 不可行 → 若要可操作策略：需換非權值股宇宙（中小股，但 Symbols 資料少）/ 加濾網 / 成本重估（降 slippage）/ 樣本外驗證。
- 下一階段（如需）: 非權值股代測或 forward-paper 前，需先擴充 symbol 宇宙資料。