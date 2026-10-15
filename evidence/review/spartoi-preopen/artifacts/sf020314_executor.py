#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Spartoi 收盤後/開盤前 SF-02/03/13/14 executor — RUNBOOK&WI v2.0.0 / P1 v2.1.0
SF-02 盤前分析 -> daily_pack.json (bias_d_draft/final/D-DR/IL-EL/A_list/S1_candidates/story_card_final)
SF-03 盤前選股 -> S1_final_list.json / xs_watchlist.xs / preopen_risk_report.json (qualification proxy)
SF-13 盤後復盤 -> daily_report.json / weekly_report.json / feedback_to_method.json
SF-14 資料管理 -> version_manifest.json (版本化落盤)
LOCAL/PAPER; no live order; preopen live part marked pending Q2/XQ.
"""
import hashlib, json, datetime, csv
from pathlib import Path
import sys
sys.path.insert(0, r"C:\Projects\Agent_Workspace\SQS-THC\.venv-data\Lib\site-packages")
import duckdb
import polars as pl
from datetime import date

ROOT = Path(r"C:\Projects\Agent_Workspace\SQS-THC")
DB = ROOT / "data_plane" / "data" / "backtest.duckdb"
WEEK_OUT = ROOT / "var" / "spartoi-preopen" / "spartoi_flow" / "2026-W34"
DAY_OUT = ROOT / "var" / "spartoi-preopen" / "dayflow" / "2026-08-20"
ARC_OUT = ROOT / "var" / "spartoi-preopen" / "archive"
WEEK_OUT.mkdir(parents=True, exist_ok=True); DAY_OUT.mkdir(parents=True, exist_ok=True); ARC_OUT.mkdir(parents=True, exist_ok=True)

NOW = "2026-08-20T21:40+08:00"
WORK_DATE = "2026-08-20"; WORK_WEEK = "2026-W34"; CAND = "CAND-SPARTOI-W34-20260820"

con = duckdb.connect(str(DB), read_only=True)
# data last 30 bars per symbol for daily metrics
daily = con.execute('SELECT symbol, date, open, high, low, close, volume, "asof", "known_at" FROM daily_bars WHERE date >= ? ORDER BY symbol, date', [date(2026,7,1)]).pl()

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def emit(dirp, name, obj):
    p = dirp/name; p.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8"); return p

# load weekly_list from SF-01
weekly_pack_raw = json.loads((WEEK_OUT/"weekly_pack.json").read_text(encoding="utf-8"))
weekly_symbols = [r["symbol"] for r in weekly_pack_raw["weekly_list"]]
weekly_bias_dir = weekly_pack_raw["bias_w"]["direction"]

# ═══ SF-02 盤前分析 → daily_pack ═══
# 用週級股計算日級 ICT 標 (D-DR/EQ50, IL/EL proxy 從 daily OHLCV)
last = daily.filter(pl.col("date") == daily["date"].max())
d_dr_hi = float(last["high"].max()) if len(last) else 0.0
d_dr_lo = float(last["low"].min()) if len(last) else 0.0
eq50_d = round((d_dr_hi+d_dr_lo)/2, 2)
mean_dret = float(daily.group_by("symbol").agg((pl.col("close").last()/pl.col("close").first()-1).alias("r"))["r"].mean())
d_up = int((daily.group_by("symbol").agg((pl.col("close").last()/pl.col("close").first()-1).alias("r"))["r"]>0).sum())
d_dn = int((daily.group_by("symbol").agg((pl.col("close").last()/pl.col("close").first()-1).alias("r"))["r"]<0).sum())
if mean_dret > 0 and d_up > d_dn: d_dir = "BULL_MILD"
elif mean_dret < 0 and d_dn > d_up: d_dir = "BEAR_MILD"
else: d_dir = "MIXED"
bias_d_final = {"direction": d_dir, "three_scenarios": ["BASE", "BULL", "BEAR"],
                "confidence": "LOW_MEDIUM", "weekly_parent": weekly_bias_dir,
                "invalidations": {"D-DR-break-above": d_dr_hi, "D-DR-break-below": d_dr_lo}}
# A_list: 週級股中流動性/動能前 12 (≤16)
last_all = (daily.group_by("symbol").agg(
    pl.col("close").last().alias("c"), pl.col("volume").last().alias("v")))
A_list_df = last_all.join(pl.DataFrame({"symbol": weekly_symbols}), on="symbol", how="inner").sort("v", descending=True).head(12)
A_list = [{"symbol": r["symbol"], "px": round(r["c"],2), "liq": int(r["v"])} for r in A_list_df.to_dicts()]
# S1_candidates (6-10) — A_list 中 price OK 者
S1_candidates = [a for a in A_list if a["px"] > 5][:10]
story_card_final = {
  "market": "MIXED regime (weekly " + weekly_bias_dir + ")",
  "weekly_direction": weekly_bias_dir, "daily_direction": d_dir,
  "swings": ["base", "bull_reclaim", "bear_fail"],
  "entry_plan_ref": "pending-SF03/live preopen", "risk_ref": "risk/limits.yaml",
}
daily_pack = {
  "schema": "RW-V200-DAILY-PACK", "date": WORK_DATE, "week": WORK_WEEK, "generated_at": NOW,
  "candidate": CAND, "bias_d_draft": {"direction": d_dir, "state": "draft"},
  "bias_d_final": bias_d_final, "D-DR/EQ50": {"high": round(d_dr_hi,2), "low": round(d_dr_lo,2), "eq50": eq50_d},
  "IL/EL": {"internal_liquidity": "eq50-focus", "external_liquidity": "prev-range-h/l below/above", "proxy": "daily-OHLCV"},
  "A_list": A_list, "A_list_count": len(A_list), "S1_candidates": S1_candidates,
  "story_card_final": story_card_final,
  "mutation_flags": {"method": False, "risk": False, "wiki": False, "broker_write": False},
}
emit(DAY_OUT, "daily_pack.json", daily_pack)
print("[SF-02] daily_pack.json  A_list=%d S1_candidates=%d d_dir=%s" % (len(A_list), len(S1_candidates), d_dir))

# ═══ SF-03 盤前選股 → S1_final + xs_watchlist + preopen_risk (qualification proxy) ═══
# live preopen (平衡價/委比/量) 需 XQ/Q2 live window; 此處以 daily close 代理 + 標記
preopen_risk = {"vi_risk": ["SCAN_PENDING_LIVE_XQ"], "disposition": ["SCAN_PENDING_LIVE_XQ"],
                "price_limit_10pct": True, "live_preopen_note": "平衡價/委比需 Q2 XQ live window",
                "qualification": "daily-close-proxy"}
S1_final = S1_candidates[:8]  # 6-10 檔
emit(DAY_OUT, "S1_final_list.json", {"schema":"RW-V200-S1-FINAL","date":WORK_DATE,"S1_final":S1_final,"count":len(S1_final),
    "rollback":"ROLLBACK_S1->S1_candidates","hidden_if_empty":"KS-S1-EMPTY",
    "preopen_note":"候選經 daily-proxy；Q2/XQ live preopen 將覆核"})
# xs_watchlist.xs
xs_lines = ["// Spartoi S1 watchlist (qualification) " + WORK_DATE, "watchlist:"]
for s in S1_final:
    xs_lines.append("  - symbol: %s   // px=%.2f liq=%d" % (s["symbol"], s["px"], s["liq"]))
(DAY_OUT/"xs_watchlist.xs").write_text("\n".join(xs_lines), encoding="utf-8")
emit(DAY_OUT, "preopen_risk_report.json", preopen_risk)
print("[SF-03] S1_final_list.json S1=%d + xs_watchlist.xs + preopen_risk_report.json" % len(S1_final))

# ═══ SF-13 盤後復盤 (qualification: 本窗無實際trade → 結構性復盤) ═══
daily_report = {"schema":"RW-V200-DAILY-REPORT","date":WORK_DATE,"week":WORK_WEEK,"generated_at":NOW,
  "kpi":{"win_rate":"N_A_no_trades","expectancy":"N_A","r_multiple":"N_A","is_vwap_gap":"N_A",
         "mae_mfe":"N_A","hit_r":"N_A","main_vs_antitrend":"N_A"},
  "execution_vs_scenario":{"note":"qualification-run: 無實盤執行; 結構/契約層復盤"},
  "deviation_reason":["no_execution_today_qualification",
                      "data_window_asof_2026-08-13; today_2026-08-20 no_new_bars(NO_CHANGE)"],
  "deliverable":"STRUCTURAL (KPI uncomputable without live execution)"}
# 週五才出週報; 8/20 週四 -> weekly_report 以資料末週為週五分析
weekly_report = {"schema":"RW-V200-WEEKLY-REPORT","week_ref":"data-last-complete-week","generated_at":NOW,
  "weekly_bias": weekly_bias_dir, "advance_ratio": weekly_pack_raw["bias_w"]["breadth"]["advance_ratio"],
  "weekly_list_count": len(weekly_symbols),
  "note":"週五完整性週報需完整週資料; 本窗資料至 8/13(四)"}
emit(DAY_OUT, "daily_report.json", daily_report)
emit(WEEK_OUT, "weekly_report.json", weekly_report)
feedback_to_method = {"schema":"RW-V200-FEEDBACK","date":WORK_DATE,"items":[],
  "note":"無實盤執行→無方法回饋; 待 Q2/Q3/Q4 live 執行後生成"}
emit(DAY_OUT, "feedback_to_method.json", feedback_to_method)
print("[SF-13] daily_report.json + weekly_report.json + feedback_to_method.json")

# ═══ SF-14 資料管理 → version_manifest ═══
all_artifacts = []
for base in [WEEK_OUT, DAY_OUT]:
    for f in base.glob("*.*"):
        all_artifacts.append({"path": str(f.relative_to(ROOT/"var")), "sha256": sha(f), "bytes": f.stat().st_size})
version_manifest = {"schema":"RW-V200-VERSION-MANIFEST","date":WORK_DATE,"week":WORK_WEEK,
  "generated_at":NOW,"artifacts":all_artifacts,"count":len(all_artifacts),
  "replayable":"all evidence_ptr traceable; no compressed archive (small set)",
  "storage_note":"SQS-THC/var/spartoi-preopen (gitignored run area)"}
emit(ARC_OUT, "version_manifest.json", version_manifest)
print("[SF-14] version_manifest.json artifacts=%d" % len(all_artifacts))

# summary
print(json.dumps({"SF-02 A_list": len(A_list), "SF-02 S1_candidates": len(S1_candidates),
                  "SF-03 S1_final": len(S1_final), "SF-13 reports": ["daily","weekly","feedback"],
                  "SF-14 artifacts": len(all_artifacts), "candidate": CAND,
                  "dayflow_dir": str(DAY_OUT), "weekflow_dir": str(WEEK_OUT)}, ensure_ascii=False, indent=2))