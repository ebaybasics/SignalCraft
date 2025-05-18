# === build_snapshots.py ===

import pandas as pd
from indicators.compute_indicators import compute_indicators
from indicators.compute_passthroughs import compute_passthroughs
from config.config import INTERVAL_PERIOD_MAP


def build_full_snapshot(
    tickers: list[str],
    timeframes: list[str],
    fetch_function
) -> dict[str, pd.DataFrame]:
    """
    Builds a multi-timeframe snapshot for a list of tickers using the provided data fetch function.

    Args:
        tickers: List of ticker symbols.
        timeframes: List of timeframes (e.g., ["5m", "1h", "1d"]).
        fetch_function: Function(ticker: str, interval: str, period: str) -> pd.DataFrame

    Returns:
        Dictionary of snapshots keyed by timeframe label (e.g. "1H", "1D", etc.)
    """
    snapshots = {}

    for tf in timeframes:
        label = tf.upper()
        snapshot_rows = []

        print(f"📥 Building snapshot for {label}...")

        for ticker in tickers:
            try:
                # === Step 1: Determine historical range using INTERVAL_PERIOD_MAP ===
                period = INTERVAL_PERIOD_MAP.get(tf, "60d")

                # === Step 2: Fetch raw OHLCV data using the passed fetch_function ===
                raw_df = fetch_function(ticker, interval=tf, period=period)



                if raw_df.empty or len(raw_df) < 20:
                    print(f"⚠️ Skipping {ticker} {label} — not enough data")
                    continue

                # === Step 3: Compute TA indicators and passthroughs ===
                indicators_df = compute_indicators(raw_df.copy(), tf)
                passthrough_df = compute_passthroughs(raw_df.copy(), tf)

                # === Step 4: Combine both layers, tag metadata, and extract last row ===
                full_df = pd.concat([indicators_df, passthrough_df], axis=1)
                final_row = full_df.iloc[[-1]].copy()
                final_row["Ticker"] = ticker
                final_row["Timeframe"] = label

                # ----- ADD DATE & TIME COLUMNS ----------------------------------------
                ts   = raw_df.index[-1]                     # tz-aware UTC timestamp
                # If you prefer U.S. market time convert here:
                ts = ts.tz_convert("America/New_York")
                final_row["Date"] = ts.strftime("%m/%d/%y")
                final_row["Time"] = ts.strftime("%H:%M")
                # -----------------------------------------------------------------------

                final_row["Ticker"]    = ticker
                final_row["Timeframe"] = label

                # Re-order so Date / Time are the first two columns
                cols = (
                    ["Date", "Time", "Ticker", "Timeframe"]
                    + [c for c in final_row.columns if c not in ("Date","Time","Ticker","Timeframe")]
                )
                final_row = final_row[cols]

                

                # Reorder columns to place Ticker and Timeframe first
                cols = ["Ticker", "Timeframe"] + [col for col in final_row.columns if col not in ("Ticker", "Timeframe")]
                final_row = final_row[cols]

                snapshot_rows.append(final_row)

            except Exception as e:
                print(f"❌ {ticker} ({label}) error: {e}")
                snapshot_rows.append(pd.DataFrame([{"Ticker": ticker, "Timeframe": label}]))

        # === Step 5: Save combined snapshot per timeframe ===
        if snapshot_rows:
            snapshots[label] = pd.concat(snapshot_rows, ignore_index=True)
            print(f"✅ {label} snapshot built with {len(snapshots[label])} rows")
        else:
            print(f"⚠️ No usable data for {label}")

    return snapshots
