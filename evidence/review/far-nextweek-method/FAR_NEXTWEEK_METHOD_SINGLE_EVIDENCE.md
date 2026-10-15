# FAR 下周當沖方法設計 — 單一 Evidence MD

**artifact_id:** `FAR_NEXTWEEK_METHOD_SINGLE_EVIDENCE`
**目標下週:** 2026-08-24..08-28（五交易日）· **主軸:** 台股當日沖銷 T0（非隔夜）
**建置:** 2026-08-21 · **治理:** HGK / Fabric · **工具:** KANBAN+SWARM+GSTACK/OPENSPEC+Codex CLI

## 0. Claim Ceiling
```
FAR_NEXTWEEK_METHOD_RESEARCH_COMPLETE
目標: 制定下周合理最高獲利機率/期望值/風險報酬之當沖方法
方法 = 設計提案 + 量化框架; 不保證獲利
需實測 + WF-09→10→11→08 + HITL 才可下周使用
Paper/live NOT_AUTHORIZED
```

## 1. 候選教訓（3 候選證偽分類 — 最重要軸 = gross pre-cost 正負）
| 候選 | 證偽根因 | 類別 |
|---|---|---|
| w34 overnight-pullback | gross -581,939, win43%<50% | **signal 無 edge**（成本放大 6.64x） |
| rf-overnight (real) | gross +36.18 vs baseline 22.0, edge **+14.18bp** | **有真 edge 但被 68.5bp 隔夜成本吃掉** |
| T0 open-auction-breakout | gross IS-240%/OOS-221%（成本前即負） | **純無 edge**（非成本）; 49 權值股代表性薄 |

**KEY INSIGHT（Codex + lane 一致）：** 唯一被實證的真 edge 來源 = **ML 跨截面/短時域分類**（rf +14.18bp vs baseline）。應**移入 T0 盤中**（5/15/30-min 分類）保 edge、共享 68.5bp 盤中成本。

## 2. 下周（8/24–28）方法設計（leading candidates）

- **C1 `OR-breakout-retest-continuation`**（實證結構最優）: 首 15-min OpeningRange 突破延展（OR_hi→day_hi 均值 +151bp），回踩後做多 ~+160bp；**需 vol filter + trailing + 僅 top-liquidity + 重估 slippage** 才可能轉正。此**取代**先前的 rf-intraday-momentum（其實測「首小時動能延續率僅 44.2%」→ FIRST-HOUR-MOMENTUM 剔除）。
- **C2 `VWAP-anchor-drift`**（高波動 regime 對照）。
- **誠實 default（lane2）**：因無候選能中立覆蓋 68.5bp 成本，**下周無可推薦方法 = 誠實期望結果（NO_TRADE default，非失敗）**。
- 通用參數: Universe top-49 權值股; cost 68.5bp; target gross 覆蓋成本 / RR≥1.5; 尾盤 13:20 平（T0 非隔夜）。

## 3. 量化框架（成功定義與防 overclaim）
- **成功 = IS AND OOS 皆 gross>0**（成本後），非僅 OOS；RR≥1.5、win≥40%。
- walk-forward / 參數穩健性；**禁止只挑 OOS 修參數**（overfit-rescue guard, DOC-20）。
- 決策樹: 候選 → IS/OOS 回測 → gross>0 both? 否=REJECTED(失敗是資產) / 是=成本後>0 → independent validation(另派 checker) → WF-09→10→11→08 RESEARCH_ONLY → 推薦下周 → Paper/Shadow(需 live/HITL)。

## 4. 執行與驗收
- KANBAN 4 卡 + SWARM 3 lane(FAR) + Codex CLI ANALYSIS(EXIT=0, opencode-go) + 驗收 lane。
- lane1 用真實 minute_bars 做了 duckdb 統計（gap/OR/動能行為）。
- KEY_INSIGHT 由既有 evidence 支持（rf real +14.18bp）。

## 5. Nonclaims / Stop
- 方法為**設計提案 + 量化框架**；**不保證獲利**；需實測/WF/HITL。
- Paper/live NOT_AUTHORIZED；下周若候選 gross 仍負→誠實 REJECTED 不留倉。
- STOP_NEXT: 依 C1 建 rf-intraday-momentum 實測(IS/OOS + cost) 才是落地。

