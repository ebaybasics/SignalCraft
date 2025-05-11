# === main.py ===

import pandas as pd
import os
from config import tickers, SR_tickers
from indicators.compute_indicators import build_snapshot_with_indicators
from indicators.fetch_data import fetch_ticker_data
from analysis.summary import summarize_top_bottom_indicators

# === Create Output Directory ===
os.makedirs("data", exist_ok=True)

# === Generate Snapshots Dynamically ===
print("📈 Building indicator snapshots...")
snapshots = {
    "5M": build_snapshot_with_indicators(tickers, "5m"),
    "1H": build_snapshot_with_indicators(tickers, "1h"),
    "1D": build_snapshot_with_indicators(tickers, "1d"),
    "1WK": build_snapshot_with_indicators(tickers, "1wk"),
    "1MO": build_snapshot_with_indicators(tickers, "1mo"),
    "3MO": build_snapshot_with_indicators(tickers, "3mo")

}

# === Summary Output ===
print("🧠 Summarizing top and bottom ETFs by active indicators...")
summary_df = summarize_top_bottom_indicators(snapshots)

# === Save Outputs ===

# Create data folder if it doesn't exist
os.makedirs("data/marketData", exist_ok=True)

# Save each snapshot to a separate file in /data/marketData/
for label, df in snapshots.items():
    file_path = f"data/marketData/marketData_{label}.csv"
    df.to_csv(file_path, index=False)
    print(f"✅ Saved {label} snapshot to {file_path}")

# Save ranked summary
summary_df.to_csv("data/indicatorSummary.csv", index=False)

print("✅ Saved full market data to data/marketData.csv")
print("✅ Saved summary rankings to data/indicatorSummary.csv")

from indicators.fetch_data import generate_ohlcv_snapshots
import os

# === Save Ticker OHLCV Snapshots ===
os.makedirs("data/priceVolume", exist_ok=True)

timeframes = ["5m", "1h", "1d", "1wk", "1mo", "3mo"]

for ticker in SR_tickers:
    for tf in timeframes:
        try:
            df = fetch_ticker_data(ticker, interval=tf, years=1)
            if not df.empty:
                filepath = f"data/priceVolume/{ticker}_{tf.upper()}.csv"
                df.to_csv(filepath)
                print(f"✅ Saved: {filepath}")
            else:
                print(f"⚠️ No data for {ticker} {tf}")
        except Exception as e:
            print(f"❌ Error fetching {ticker} {tf}: {e}")
