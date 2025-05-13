# === main.py ===

import pandas as pd
import os
from config import tickers, SR_tickers
# from indicators.compute_indicators import build_snapshot_with_indicators
from indicators.fetch_data import fetch_ticker_data
from indicators.post_indicator_proccessing_functions import *
from analysis.summary import summarize_top_bottom_indicators
from indicators.enhance_indicators import apply_derived_features
from indicators.compute_passthroughs import compute_passthroughs
from indicators.build_snapshots import build_full_snapshot


# === Create Output Directory ===
os.makedirs("data", exist_ok=True)


# === Flexible Snapshot Builder ===
# The following line generates snapshots for each timeframe by computing both technical indicators
# and passthrough values (e.g., VOLUME, REL_VOLUME) using raw OHLCV data.
#
# ✅ To change your data source in the future:
# Simply swap out `fetch_ticker_data` with another compatible data-fetching function,
# such as `fetch_from_csv`, `fetch_from_api`, or a custom database query.
#
# 🧠 Reminder:
# `fetch_ticker_data` is defined in `indicators/fetch_data.py` and follows this format:
#     def fetch_ticker_data(ticker: str, interval: str, years: int) -> pd.DataFrame
#
# As long as your custom fetch function returns a properly formatted OHLCV DataFrame,
# the rest of the pipeline will work without modification.
timeframes = ["5m", "1h", "1d", "1wk", "1mo"]
snapshots = build_full_snapshot(tickers, timeframes, fetch_ticker_data)

# === Compute Indicator Layers Separately ===
# We explicitly separate the calculation of pure technical indicators (via pandas_ta)
# from passthrough data transformations like raw Volume and derived REL_VOLUME.
#
# This preserves modularity and gives us flexibility to:
# - Swap out or extend passthrough logic independently
# - Reuse compute_indicators() in contexts where passthroughs aren’t needed
# - Add custom passthroughs (e.g., VWAP, average true range volume) later
#
# `compute_passthroughs()` pulls from PASSTHROUGH_REGISTRY in config.py
# and generates raw and derived signals like VOLUME_1H, VOLUME_1H_Avg, REL_VOLUME_1H, etc.
# === Add passthrough columns (like VOLUME, REL_VOLUME) to each snapshot ===
for label, df in snapshots.items():
    try:
        passthrough_df = compute_passthroughs(df, label)
        snapshots[label] = pd.concat([df, passthrough_df], axis=1)
    except Exception as e:
        print(f"❌ Error applying passthroughs to snapshot {label}: {e}")


# === Enhance each snapshot using configured indicator enhancers ===
for label, df in snapshots.items():
    snapshots[label] = apply_derived_features(df, label)



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

timeframes = ["5m", "1h", "1d", "1wk", "1mo"]

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
