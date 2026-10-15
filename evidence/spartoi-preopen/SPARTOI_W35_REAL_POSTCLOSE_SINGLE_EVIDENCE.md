# Spartoi 週五盤後真實週級流程（W35）— 單一證據

- **對象**: Spartoi RUNBOOK&WI v2.0.0 / P1 v2.1.0
- **時序**: 2026-08-21（週五）收盤後 16:17 → 本週最後交易日收盤，依 RUNBOOK SF-01「每週五盤後」+ SF-13「13:30~」真實時窗
- **模式**: `REAL_POSTCLOSE`（真實資料層，非 SIM）
- **資料集**: `DSV-DAILY-2026-08-21-r2`（真實 8/21 TWSE 收盤，1425 new rows）
- **CAND**: `CAND-SPARTOI-W35-REAL-20260821`

## 1. 交付物

Primary home: `SQS-THC/evidence/spartoi-preopen/real_postclose/`

- **SF-01 週級包（真實）**: `SF-01_WEEKLY_PACK_W35_REAL.json`
  - bias_w = MIXED（mean_ret +0.24%, up 132 / dn 120）
  - W-DR/EQ50 market = 41.21；W-LQ 前五大流動性
  - weekly_list = 30 檔（含 eq50/w_ret%/liquidity/bias_tag）
  - four_cards（market bias / dealing range / liquidity / operation）
  - next_week_prep → W36（首日 2026-08-24）
- **SF-13 盤後復盤（真實）**: `SF-13_REVIEW_W35_REAL.json`

## 2. 誠實 claim ceiling

- **真實部分**：本週級分析用真實 8/21 收盤 OHLCV → `REAL_POSTCLOSE`（資料層真實，非模擬）。
- **非宣稱**：無 live 訂單/成交、無 broker 寫入；本週無真實盤中執行（此前為 SIM/qualification）。
- **盤中段限制**：SF-04..12（真實盤中 live）今天已收盤無法執行 → 下周首個交易日（08-24）開盤段，
  需 FDA 條件2 開 XQ + 建倉逐筆 HITL。本交付是**真實盤後準備下周開盤**，非 live 下單。
- **8/21 覆蓋**：95 symbols 具 8/21 真實列（部分標的因收據匹配被 skip）；週級分析基於可取得真實資料。

## 3. 對 FAR 兩問題的誠實結

1. **是否足以應付下周首個交易日開盤？** → 準備度部分成立（交付物骨架 + 真實 8/21 資料 + W36 週級包 + 下周盤前準備）
   已備妥；但**完整真實實跑**仍需下周開盤段 live 執行 + FDA + HITL。本交付完成「可為開盤做真實準備」。
2. **本週最後交易日收盤是否該做真實（非模擬）流程？** → **是**，且已執行真實盤後復盤 + 週級分析
   （非 SIM），為 W36 首個交易日（08-24）做真實準備。

## 4. STOP / 接續

- 不停 production/live。下周 08-24 開盤段 = 真實盤中實跑窗口（FDA 條件2 + 逐筆 HITL）。
- Resume: `RESUME:SPARTOI_W35_REAL_POSTCLOSE_FROZEN`（下周一 08:30 前做 SF-02/SF-03 真實盤前 + 開盤 live）。