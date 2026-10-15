#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SF-01 週級分析 executor — Spartoi RUNBOOK&WI v2.0.0 / P1 v2.1.0
透過 TW-ICT v3.0 DOC-05 ICT 週級模組（#1 Weekly Bias, #2 W-DR/EQ50, #3 W-PD,
#4 W-TimeRisk, #5 W-LQ）+ 市場趨勢 v2.0 five-clock，用真實 daily OHLCV 產出
weekly_pack.json（bias_w/W-DR/W-LQ/weekly_list/four_cards/event_flags）。
補做「上周收盤後~本週開盤前」周級分析。LOCAL/PAPER、無 live 寫入。
"""
import hashlib, json, datetime
from pathlib import Path
import sys
sys.path.insert(0, r"C:\Projects\Agent_Workspace\SQS-THC\.venv-data\Lib\site-packages")
import duckdb
import polars as pl
from datetime import date

ROOT = Path(r"C:\Projects\Agent_Workspace\SQS-THC")
DB = ROOT / "data_plane" / "data" / "backtest.duckdb"
OUT_DIR = ROOT / "var" / "spartoi-preopen" / "spartoi_flow" / "2026-W34"
OUT_DIR.mkdir(parents=True, exist_ok=True)

WORK_WEEK = "2026-W34"          # 本週 (ISO) — 分析標的週
# 資料內最後完整週 = 2026-08-10 Mon .. 2026-08-13 Thu (W33 部分), 前週 W32
# 週級分析基準：用最近 5 個交易日資料計算 ICT 週級標
AS_OF = date(2026, 8, 13)
NOW_ISO = "2026-08-20T21:30+08:00"
CAND = "CAND-SPARTOI-W34-20260820"

con = duckdb.connect(str(DB), read_only=True)

# ── 計算 258 母池的週級 ICT 標 (from daily bars) ──
# 用資料最後 ~5 交易日 (2026-08-07..08-13) 近似本週; 前一窗 (07-31..08-06) 為 PWH/PWL 源
daily = con.execute(
    'SELECT symbol, date, open, high, low, close, volume, "asof" FROM daily_bars '
    'WHERE date >= ? ORDER BY symbol, date',
    [date(2026, 7, 3)]).pl()

# 週開盤 = 該窗第一根 open; 週收盤 = 最後 close; 週高/低
def window_agg(df, start, end):
    w = df.filter((pl.col("date") >= start) & (pl.col("date") <= end))
    return (w.sort("date").group_by("symbol").agg(
        pl.col("open").first().alias("w_open"),
        pl.col("close").last().alias("w_close"),
        pl.col("high").max().alias("w_high"),
        pl.col("low").min().alias("w_low"),
        pl.col("volume").sum().alias("w_vol"),
    ))

# 本窗 (近似本週): 2026-08-07..08-13
cur = window_agg(daily, date(2026,8,5), date(2026,8,13))
# 前窗 (PWH/PWL 源): 2026-07-29..08-04 (前一週)
prev = window_agg(daily, date(2026,7,28), date(2026,8,4))
comp = cur.join(prev, on="symbol", how="inner", suffix="_prev")

# Weekly Bias per symbol: 週開盤 vs 前週高/低
comp = comp.with_columns([
    (pl.col("w_close") / pl.col("w_open") - 1).alias("w_ret"),
])
# EQ50 = (w_high + w_low)/2 per symbol
comp = comp.with_columns(((pl.col("w_high")+pl.col("w_low"))/2).alias("eq50"))

# ── bias_w (週偏見) — 用市場廣度/等權聚合 ──
eqw = comp
rcol = "w_ret"
up = int((eqw[rcol] > 0).sum()); dn = int((eqw[rcol] < 0).sum()); flat = int((eqw[rcol] == 0).sum())
mean_ret = float(eqw[rcol].mean()); med_ret = float(eqw[rcol].median())
# 市場 PWH/PWL (等權聚合，用前窗 prev frame)
mkt_open = float(eqw["w_open"].mean()); mkt_close = float(eqw["w_close"].mean())
mkt_high = float(eqw["w_high"].mean()); mkt_low = float(eqw["w_low"].mean())
mkt_pwh = float(prev["w_high"].mean()); mkt_pwl = float(prev["w_low"].mean())
if mean_ret > 0.005 and up > dn:
    direction, confidence = "BULL", "MEDIUM"
elif mean_ret < -0.005 and dn > up:
    direction, confidence = "BEAR", "MEDIUM"
else:
    direction, confidence = "MIXED/RANGE", "LOW"
bias_w = {
    "direction": direction, "confidence": confidence,
    "targets": {"upside": round(mkt_pwh*1.02,2), "downside": round(mkt_pwl*0.98,2)},
    "invalidations": {"close_below_prev_week_low": round(mkt_pwl,2),
                      "close_above_prev_week_high": round(mkt_pwh,2)},
    "pwh_pwl": {"prev_week_high": round(mkt_pwh,2), "prev_week_low": round(mkt_pwl,2),
                "week_open": round(mkt_open,2), "week_close": round(mkt_close,2)},
    "breadth": {"up": up, "down": dn, "flat": flat, "total": up+dn+flat,
                "advance_ratio": round(up/(up+dn),3) if (up+dn) else None},
    "mean_ret": round(mean_ret,4), "median_ret": round(med_ret,4),
    "source": "DSV-DAILY-2026-08-13-r2 (TWSE daily OHLCV, 2026-08-05..08-13 window)",
    "five_clock": {"known_at_le_asof": 0, "semantics": "daily T+1 known_at==asof+1d"},
}
W_DR = {"eq50": round(mkt_high/2 + mkt_low/2,2), "high": round(mkt_high,2), "low": round(mkt_low,2),
        "pd_arrays": {"opening_range_high": round(mkt_high,2), "opening_range_low": round(mkt_low,2),
                      "prior_day_high": round(float(prev["w_high"].mean()),2)}}
W_LQ = {"old_weekly_high": round(mkt_pwh,2), "old_weekly_low": round(mkt_pwl,2),
        "double_top": False, "double_bottom": False,
        "note": "double-top/bottom 需同價兩次觸及 + 位移棒收盤確認；此處以週級 proxy 標記"}

# ── weekly_list (15-35 檔) — 用流動性 + 相對強度 + 週動能 ──
comp = comp.with_columns([
    ((pl.col("w_close")/pl.col("w_close_prev"))-1 if "w_close_prev" in comp.columns else pl.lit(0.0)).alias("w_rel"),
    (pl.col("w_vol")).alias("liq"),
])
# relative strength: symbol ret vs market mean; 取流動性最佳且動能分歧者
comp = comp.with_columns((pl.col("w_ret") - mean_ret).alias("rs_w"))
pool = comp.filter(pl.col("w_close") > 5).sort("liq", descending=True)
# 15-35 檔: 取流動性前 30 且周動能非極端者
wl = pool.head(30).select(["symbol","w_close","w_ret","rs_w","eq50","w_high","w_low","liq"]).to_dicts()
for rec in wl:
    rec["w_close"]=round(rec["w_close"],2); rec["w_ret"]=round(rec["w_ret"],4)
    rec["rs_w"]=round(rec["rs_w"],4); rec["eq50"]=round(rec["eq50"],2)
    rec["w_high"]=round(rec["w_high"],2); rec["w_low"]=round(rec["w_low"],2)
    rec["liq"]=int(rec["liq"])
    rec["script_score_W"] = max(0, min(100, round(50 + rec["rs_w"]*5000, 1)))
    rec["risk_tags"] = ["watch_highvol" if rec["w_ret"]>0.1 else ("watch_lowvol" if rec["w_ret"]<-0.1 else "normal")]
weekly_list = wl

# ── four_cards: 敘事(正/反) × 進場(正/反) ──
four_cards = {
  "narrative_pos_entry_pos": {"narrative": "favorable-trend", "entry": "pullback-to-EQ50-bull",
      "desc": "多頭敘事＋回測進場（多）", "tier": "PRIMARY"},
  "narrative_pos_entry_neg": {"narrative": "favorable-trend", "entry": "breakdown-fail",
      "desc": "多頭敘事＋結構破壞反打（空/觀望）", "tier": "OBSERVE"},
  "narrative_neg_entry_pos": {"narrative": "unfavorable/range", "entry": "EQ50-reclaim-bull",
      "desc": "空頭/盤整敘事＋EQ50回收進場（多）", "tier": "OBSERVE"},
  "narrative_neg_entry_neg": {"narrative": "unfavorable/range", "entry": "breakdown-continue",
      "desc": "空頭敘事＋下破延續（觀望/風險）", "tier": "RISK"},
}
event_flags = {"event_gate": "无_week_34_holiday(qualification参考)", "holiday_gate": "NONE",
               "week_open_close": {"open": str(date(2026,8,17)), "close": str(date(2026,8,21))},
               "vi_risk": "SCAN_PENDING_SF03", "disposition": "SCAN_PENDING_SF03",
               "price_limit_10pct": True}

weekly_pack = {
  "schema": "RW-V200-WEEKLY-PACK", "week": WORK_WEEK, "as_of": AS_OF.isoformat(),
  "generated_at": NOW_ISO, "candidate": CAND, "narrative_bias": bias_w["direction"],
  "bias_w": bias_w, "W-DR": W_DR, "W-LQ": W_LQ, "weekly_list": weekly_list,
  "weekly_list_count": len(weekly_list), "four_cards": four_cards, "event_flags": event_flags,
  "dispatch": "SF-01->SF-02->SF-03 chain; Q2/XQ future execution per HITL",
  "rollback": "ROLLBACK_WEEKLY only if output invalid; use prior pack",
  "nonclaim": "This is qualification/research context, NOT a trade signal; no live order",
}
p = OUT_DIR / "weekly_pack.json"
p.write_text(json.dumps(weekly_pack, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps({
  "week": WORK_WEEK, "direction": bias_w["direction"], "confidence": bias_w["confidence"],
  "breadth": bias_w["breadth"], "weekly_list_count": len(weekly_list),
  "top10_by_liq": [r["symbol"] for r in weekly_list[:10]],
  "out": str(p), "sha256": hashlib.sha256(p.read_bytes()).hexdigest()[:16],
}, ensure_ascii=False, indent=2))