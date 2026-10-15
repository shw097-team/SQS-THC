"""C-phase strategy runner — Overnight pullback to EQ50 (only-long, LOCAL/PAPER).
Pure signal + position reducer over daily bars; no I/O, no broker, no network.
Signal: price pulls back to prior-range EQ50 (internal liquidity) and structure holds
(trend not broken); entry next bar; exits at target/stop; PnL after TWSE cost model.
IS/OOS walk-forward split driven by caller. Deterministic (no RNG)."""
from __future__ import annotations
from dataclasses import dataclass, field

class SRError(Exception): pass

@dataclass
class StrategyResult:
    method_id: str
    trades: list = field(default_factory=list)
    is_metrics: dict = field(default_factory=dict)
    oos_metrics: dict = field(default_factory=dict)

    @property
    def total_pnl(self): 
        return sum(t["pnl"] for t in self.trades)
    @property
    def trade_count(self): return len(self.trades)

def _cost_adjust(entry, exit_, qty, fee_bps=14.25, tax_bps=30.0, slip_bps=5.0):
    """TWSE cost: 0.1425% fee, 0.3% tax on sell, 5bps slippage proxy."""
    entry_cost = entry*qty*(fee_bps/1e4) + entry*qty*(slip_bps/1e4)
    exit_cost = exit_*qty*(fee_bps/1e4) + exit_*qty*(tax_bps/1e4) + exit_*qty*(slip_bps/1e4)
    gross = (exit_ - entry)*qty
    return gross - entry_cost - exit_cost

def run_overnight_pullback(df, symbol_col="symbol", date_col="date", open_col="open",
                           high_col="high", low_col="low", close_col="close",
                           volume_col="volume", eq50_factor=1.0, stop_pct=0.03,
                           target_pct=0.03, qty=1000, fee_bps=14.25, tax_bps=30.0, slip_bps=5.0):
    """df: list of dict rows in date asc per symbol. 純函數."""
    trades = []
    for sym in {r[symbol_col] for r in df}:
        rows = sorted([r for r in df if r[symbol_col]==sym], key=lambda r: r[date_col])
        if len(rows) < 3: continue
        # 用前三根擬「prior range」EQ50 (local liquidity) 
        for i in range(2, len(rows)-1):
            prior_hi = max(rows[i-2][high_col], rows[i-1][high_col])
            prior_lo = min(rows[i-2][low_col], rows[i-1][low_col])
            eq50 = (prior_hi+prior_lo)/2
            entry_c = rows[i][close_col]
            # 信號: 收盤回踩到 EQ50 附近 (< +1.5%) 且非崩盤 (close> prior_lo*0.98)
            if eq50 <= 0: continue
            pullback = abs(entry_c - eq50)/eq50 < 0.015 and entry_c > prior_lo*0.98
            if not pullback: continue
            nxt_open = rows[i+1][open_col]; nxt_close = rows[i+1][close_col]
            nxt_hi = rows[i+1][high_col]; nxt_lo = rows[i+1][low_col]
            stop = nxt_open*(1-stop_pct)
            target = nxt_open*(1+target_pct)
            if nxt_hi >= target:
                exit_px = target
            elif nxt_lo <= stop:
                exit_px = stop
            else:
                exit_px = nxt_close
            pnl = _cost_adjust(nxt_open, exit_px, qty, fee_bps, tax_bps, slip_bps)
            trades.append({"symbol":sym,"date":str(rows[i+1][date_col]),"entry":round(nxt_open,2),
                           "exit":round(exit_px,2),"qty":qty,"pnl":round(pnl,2)})
    return trades

def compute_metrics(trades):
    if not trades: return {"n":0,"win_rate":0,"avg_pnl":0,"total_pnl":0,"sum_abs":0}
    wins = [t for t in trades if t["pnl"]>0]; total=sum(t["pnl"] for t in trades)
    return {"n":len(trades),"win_rate":round(len(wins)/len(trades),4),
            "avg_pnl":round(total/len(trades),2),"total_pnl":round(total,2),"sum_abs":round(sum(abs(t["pnl"]) for t in trades),2)}

def split_is_oos(trades, split_date):
    """walk-forward: trades with date<=split_date are IS, > are OOS."""
    is_= [t for t in trades if str(t["date"])<=split_date]
    oos= [t for t in trades if str(t["date"])> split_date]
    return is_, oos
