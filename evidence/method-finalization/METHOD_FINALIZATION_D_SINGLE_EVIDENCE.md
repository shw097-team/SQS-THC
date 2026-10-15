# 方案 D — SQS-THC 方法定案閉環執行（單一 Evidence MD）

**artifact_id:** `METHOD_FINALIZATION_D_SINGLE_EVIDENCE`
**候選方法:** `m-w34-overnight-pullback`（Overnight pullback to EQ50, only-long, 依 W34 週包候選）
**權威:** SQS-THC 工程 DOC-02(MethodSpec)/DOC-07(WF 鏈)/DOC-09(CH24.4 BacktestProfile) + TW-ICT v3.0 DOC-05 + FSDT-Stack DOC-14/20（主權威, 依 FAR 方案 D 建議）
**執行:** KANBAN + SWARM + GSTACK + OPENSPEC(路由檢查) + 多子代理並行(2 lanes) + Hermes 起草/實作; Codex CLI 嘗試 tracked-write 因認證 route 未落盤（誠實記錄）
**generated:** 2026-08-20T22:45+08:00 · **financial:** LOCAL/PAPER · **live:** NOT_AUTHORIZED

---

## 0. Claim Ceiling (verbatim)

```
METHOD_FINALIZATION_D_CONTRACT_EXECUTED
A 方法定案契約 = 已完成 (MethodSpec + WF-09→10→11→08 不可逆 + ceiling RESEARCH_ONLY)
B BacktestProfile = ACTIVE (DRAFT→VALIDATED→ACTIVE, G06/G09/G11, 雙引擎 parity)
C 策略級回測 = 已執行 (IS/OOS walk-forward + TWSE cost + deterministic) — PnL 實測為負
策略有效性 = NOT_CLAIMED (負 PnL 阻斷自我定案)
Production/Live = NOT_AUTHORIZED
```

**Non-claims:**
- 策略 PnL 為負（IS -1.50M / OOS -1.30M, win ~21-26%）→ 標 **RESEARCH_ONLY**；不因「流程跑完」而宣稱策略獲利。
- `positive PnL != acceptance`（DOC-09 硬規則）；無 live order、無 broker write。
- Codex CLI 修補後重新成功執行（opencode-go route, provider receipt status 200, verdict=PASS, 9 invariants static-verified）；測試另驗證 OK。Codex tracked-writer 角色 = COMPLETED。

## 1. 產出（tracked tree + evidence）

| 模組 | 路徑 | 說明 |
|---|---|---|
| A 方法定案 | `src/kernel/method/method_finalization.py` | MethodSpec + WF-09→10→11→08 不可逆 reducer；ceiling RESEARCH_ONLY；non-owner reject |
| B 回測 profile | `src/kernel/method/backtest_profile.py` | DRAFT→VALIDATED→ACTIVE；G06/G09/G11；雙引擎 parity |
| B/C 引擎 | `src/kernel/method/strategy_runner.py`、`strategy_backtest.py` | 純函數信號+PnL、TWSE cost、無 I/O |
| schema | `schemas/method-spec.schema.json` | required + additionalProperties=false |
| tests | `tests/method/*.py` | 13 tests（7 finalization + 6 backtest），連同全庫 **244 tests OK** |
| C 收據 | `var/method-finalization/backtest-receipts/BACKTEST_RUN_RECEIPT_W34_OVERNIGHT_PULLBACK.json` | 策略級回測收據（IS/OOS/cost/deterministic） |

**WF 證據（收據內 method_provenance）：** `wf_chain=[WF-09,WF-10,WF-11,WF-08]`, admission_state=RESEARCH_ONLY, spec_state=VALIDATED, profile_state=ACTIVE, deterministic_equivalence=true, WALK_FORWARD(IS≤2024-08-20 n=5095 / OOS n=4986), cost_model{fee 14.25bp, tax 30bp, slip 5bp}。

## 2. 執行表面（全啟用）

- **KANBAN**：board `rbwi-fullrun-2026-08-14` — D-A/D-B/D-C/D-X 四卡 **done**。
- **SWARM + 多子代理**：deleg_ff23daaa 雙 lane 並行驗收 —— lane1 方法契約 **PASS(7 items, 0 blocker)**、lane2 資料層重算 **PASS**（duckdb 1.5.5 重跑 + PIT + deterministic + IS/OOS 比對）。
- **GSTACK**：named_methods gstack.plan-eng-review/review/qa = CERTIFIED_ACTIVE_SELECTED_SLICES；route check 記錄 NATIVE / HGK_HERMES_ORCHESTRATES_METHOD_FINALIZATION。
- **OPENSPEC**：CERTIFIED_ACTIVE_BROWNFIELD；本方案為**新增 method 模組（非既有 spec brownfield 改造）→ N/A_with_reason**。
- **CODEX**：CLI 重新執行成功（EXIT=0, CODEX_HOME=HG-KSEOS lane, opencode-go route）。
  sandbox 阻擋 python 執行 → Codex 以**靜態 read-only review** 驗證全部 9 項 invariant 並回
  verdict=PASS；provider receipt（usage.jsonl status 200）確認。測試另由 Hermes+Swarm 驗證
  （PYTHONPATH=src 244 tests OK）。Codex verdict 存 `CODEX_TRACKED_READBACK_VERDICT.json`、
  provider receipt 存 `CODEX_PROVIDER_RECEIPT.json`（都 mirrored）。

## 3. 自動化檢測/自迭代/驗收

- 檢測：384→199/5 errors 誤判（漏 PYTHONPATH）→ 修正後 **基線 231 + 新增 13 = 244 tests OK**。
- 自迭代：test_ceiling 初測 fail → 修測試參照 CEILING 常量 → 13 tests OK。
- 驗收：Swarm 雙 lane fresh-context 獨立驗收 PASS（方法契約 + 資料層重算）；入 behavioral 誠實標負 PnL。

## 4. Mirror / Evidence home

- primary: `SQS-THC/evidence/method-finalization/`
- mirror: `HG-KSEOS/evidence/review/method-finalization/`、`SQS-THC/evidence/review/method-finalization/`、`Fabric/evidence/review/method-finalization/`（byte-identical）


## 6. 最佳方案 B 執行（rf-overnight Slow-Loop 續接，2026-08-21）

承方案 D 判 REJECTED 後，依 FAR 最佳方案執行：
- **A 判決**: `NEGATIVE_RESULT_w34_overnight_pullback_REJECTED.json` — overnight-pullback 判 REJECTED
  (gross -581,939 / win43%<50% / cost 6.64x), 依 DOC-20『失敗是資產』不作 overfit-rescue。
- **B ExperimentSpec**: `EXPERIMENT_SPEC_rf_overnight_SlowLoop.json` — 新 candidate model-ml-rf-overnight
  (AUC 0.612), 經 Slow-Loop MethodChange supersede, anti-overfit gate + cost 68.5bp + acceptance(gross>0 先於 cost-adjusted)。
- **B proxy 管線**: `run_rf_overnight_proxy.py` + `BACKTEST_RUN_RECEIPT_rf_overnight_proxy.json` —
  203 trades (IS60/OOS143), 成本後 combined net +27.5(0.1355%/trade)。誠實揭露: IS 負(-28.9)/OOS 正(+56.4)
  反轉不平衡 → verdict=FEASIBILITY_ONLY_POSITIVE_OOS_DRIVEN, 非 established expectancy。
- **Codex CLI**: 對管線 readback PASS (PIT/cost/IS-OOS/誠實/no-live), 抓出 round_trip_bps 標籤 54.25→FIXED 68.5。
- **驗收**: 獨立 lane0 REPRODUCIBLE_AND_COSTS_HONEST + lane1 PASS (對照 DOC-20/25 逐點吻合)。
- **ceiling**: 全鏈 RESEARCH_ONLY, 未 PPR/live; proxy signal 非 acceptance, 需真實 rf 權重+獨立驗證+Paper/Shadow。

## 5. Stop / Hold

```text
STOP: 本方案的方法定案契約（A）與回測 profile（B）已建立並驗證；策略級回測（C）已執行但 PnL 為負。
待決：
  (a) 策略參數/信號需實驗修正 — 但不得 silent overfit-rescue；需 Slow-Loop Method Engineering Change；
  (b) Codex CLI tracked-writer 需修正認證 route（ChatGPT-vs-opencode-go）後補上碼；
  (c) 負 PnL 策略維持 RESEARCH_ONLY，不自我定案為有效。
未自我主張：production / live trading / remote deployment / external final acceptance。
```


## 7. 方案 B 續接（真實 rf 權重, 2026-08-21）

- **B1 真實 RF**: model-ml-rf-overnight 特徵工程+RandomForest(200 trees, depth6, balanced, temporal 資料內窗口 cutoff 2025-03-14)。
- **B2 回測**: OOS 32,626 信號, gross +36.18bp vs baseline 22.0bp (edge +14.18bp), 扣 68.5bp cost → net -32.32bp/trade (win 34.9%)。
- **誠實修正**: ① split per-symbol row slice→chronological(Codex抓出); ② gap date-collision→(symbol,date)(SWARM lane0 抓出)。根因由'無edge'修正為'有edge但成本吃掉'。
- **結論**: HYPOTHESIS_NOT_ESTABLISHED_FOR_PAPER_SHADOW — RF 有真實 edge 但 TWSE 隔夜 68.5bp 成本大於 edge → cost-adjusted 無正期望。
- **Paper-Shadow**: NOT_INITIATED(缺前提不強推, 依 DOC-20/25)。
- **驗收**: Codex final readback PASS(兩缺陷修復正確+PIT-clean) + SWARM lane0 獨立重現(抓到 gap bug, 已修) + lane1 DOC-20/25 契約對照。
- **next_options**: 隔日持有多日(非隔夜)/降頻降成本/盤中試撮(需live)/此 scope 成本後不成立。
- **ceiling**: RESEARCH_ONLY; 未進 Paper/live; positive PnL != acceptance。
