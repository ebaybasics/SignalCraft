# main.py

import pandas as pd
from config import tickers, INTERVAL_PERIOD_MAP
from indicators.compute_indicators import build_snapshot_with_indicators
from analysis.summary import summarize_top_bottom_cmf
import os

# ========== Create Output Directory ==========
os.makedirs("data", exist_ok=True)

# ========== Generate Snapshots ==========
print("📈 Building indicator snapshots...")
cmf5Minute = build_snapshot_with_indicators(tickers, "5m")
cmfHour    = build_snapshot_with_indicators(tickers, "1h")
cmfDay     = build_snapshot_with_indicators(tickers, "1d")
cmfWeek    = build_snapshot_with_indicators(tickers, "1wk")
cmfMonth   = build_snapshot_with_indicators(tickers, "1mo")

# ========== Summary Output ==========
print("🧠 Summarizing top and bottom ETFs by CMF & RSI...")
summary_df = summarize_top_bottom_cmf(
    cmf5Minute, cmfHour, cmfDay, cmfWeek, cmfMonth, top_n=8
)

# ========== Save to File ==========
output_path = "data/marketData.csv"
summary_df.to_csv(output_path, index=False)
print(f"✅ Saved to {output_path}")
