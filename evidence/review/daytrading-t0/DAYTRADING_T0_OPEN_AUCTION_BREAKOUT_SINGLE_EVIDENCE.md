# 台股當日沖銷 T0 — Open-Auction Breakout 接入（單一 Evidence MD）

**artifact_id:** `DAYTRADING_T0_OPEN_AUCTION_BREAKOUT_SINGLE_EVIDENCE`
**主軸:** 台股當日沖銷 (T0, 盤中, **非隔夜**) · **建置:** 2026-08-21

## 0. Claim
```
m-t0-open-auction-breakout 接入 SQS method finalization 完成
ExperimentSpec(WF-09→10→11→08→RESEARCH_ONLY) + minute_bars 當日沖銷回測(非隔夜) 完成
實測: IS/OOS 皆 gross 負 (-240%/-221%, win11-13%) -> 訊號證偽
判 REJECTED / 失敗是資產 (DOC-20); Paper/live NOT_INITIATED
```

## 1. A/B 契約
- ExperimentSpec `EXPERIMENT_SPEC_open_auction_breakout_T0.json`: axis=DAYTRADING_T0_INTRADAY,
  09:00-09:15 OpeningRange→突破做多→停損/13:20退出→同日 FORCED_FLATTEN, cost 68.5bp。
- MethodSpec/WF `METHOD_SPEC_WF_t0_open_auction_breakout.json`: WF-09→10→11→08 → RESEARCH_ONLY, ceiling=RESEARCH_ONLY。

## 2. C 當日沖銷回測 (minute_bars, 非隔夜)
- 資料: minute_bars 49 權值股, 2025-08-11..2026-08-10, 09:00-13:30, 單一SHIOAJI。
- 實測: 5243 trades; IS gross -240.2%/net -1946%; OOS gross -221.1%/net -2106%; win 11-13%。
- **誠實根因: gross 即負 => 訊號本身無 edge(非成本; 對比隔夜 rf 是"有edge但成本吃掉")**。
- 資料代表性限制已標註(49 權值股/1y 不含中小).

## 3. 自動化檢測→自迭代修補→驗收
- Codex: PIT/T0/cost/honesty PASS, CONCERNS(cost標籤/FORCED_FLATTEN標籤/代表) -> 已修。
- SWARM lane0 VERIFIED_REPRODUCIBLE_AND_HONEST（重跑5243/hash一致）; lane1 PASS（T0 契約自洽）。
- 全程 244+ tests OK。

## 4. Evidence
- 收據 sha 01df1636…; 單一MD(本檔); 鏡像三 root byte-identical。

## 5. Nonclaims / Stop
- T0 當日沖銷為正確主軸; 本候選證偽但方法管線(WF/回測/驗收)完整跑通。
- Paper/live/production NOT_AUTHORIZED; gross負不進Paper(DOC-20/25)。
- STOP: 若要"有 edge"的當沖候選, 需換方法(如 PO3/OpeningRange-retest/高動能股)或擴大資料(含中小股/試撮深度);
  或先在現有 49 檔上改良 signal 再重測(Slow-Loop MethodChange, 非調參救)。
