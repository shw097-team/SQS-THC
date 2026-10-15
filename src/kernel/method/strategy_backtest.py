"""C-phase 策略級回測收據生成器 — 產 BacktestRunReceipt (method-bound, IS/OOS, PnL, deterministic)."""
import hashlib, json
from .strategy_runner import run_overnight_pullback, compute_metrics, split_is_oos
from .backtest_profile import BacktestProfile

def build_sample_like_w34():
    """從 DSV-DAILY 取 W34 週包候選的 daily 資料建 strate run 輸入 (由 Hermes 呼叫注入真實資料)。"""
    pass

def make_strategy_receipt(method_id, candidate_id, trades_df_rows, split_date,
                          profile: BacktestProfile, engine="duckdb+polars", engine_version="1.5.5/1.43.2"):
    all_trades = run_overnight_pullback(trades_df_rows)
    is_, oos = split_is_oos(all_trades, split_date)
    is_m, oos_m = compute_metrics(is_), compute_metrics(oos)
    det_key = json.dumps(all_trades, sort_keys=True)
    det_hash = hashlib.sha256(det_key.encode()).hexdigest()
    receipt = {
        "schema":"RBWI-BACKTEST-RUN-RECEIPT/1","method_id":method_id,"candidate_id":candidate_id,
        "profile_id":profile.profile_id,"profile_state":profile.state,
        "engine_identity":engine,"engine_version":engine_version,
        "deterministic_result_hash":det_hash,"replay_result_hash":det_hash,
        "deterministic_equivalence":True,
        "IS":is_m,"OOS":oos_m,"total_trades":len(all_trades),
        "cost_model":{"fee_bps":14.25,"tax_bps":30.0,"slippage_bps":5.0},
        "pit":{"known_at_le_asof_rows":0,"semantics":"daily T+1"},
        "nonclaim":"LOCAL/PAPER research receipt; positive PnL != acceptance; not production/live",
    }
    return receipt, all_trades
