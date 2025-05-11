# === compute_indicators.py ===

import pandas as pd
import pandas_ta as ta
import yfinance as yf
from config import INTERVAL_PERIOD_MAP, INDICATOR_REGISTRY

# === Compute Technical Indicators ===
# === indicators/compute_indicators.py ===

import pandas as pd
from config import INDICATOR_REGISTRY

def compute_indicators(df: pd.DataFrame, interval: str) -> pd.DataFrame:
    """
    Compute all indicators listed in INDICATOR_REGISTRY and add optional average/slope columns.
    """
    label = interval.upper()
    result_cols = []

    for name, meta in INDICATOR_REGISTRY.items():
        func_path = meta["func"]
        cols_needed = meta["columns"]
        params = meta["params"]
        with_avg = meta.get("with_avg", False)
        with_slope = meta.get("with_slope", False)

        # Check that required columns exist
        if not all(col in df.columns for col in cols_needed):
            print(f"Skipping {name} — missing required columns.")
            continue

        try:
            func = eval(func_path)
            args = [df[col] for col in cols_needed]
            result = func(*args, **params)

            base_col_name = f"{name}_{label}"

            if isinstance(result, pd.Series):
                df[base_col_name] = result
                result_cols.append(base_col_name)

                if with_avg:
                    df[f"{base_col_name}_Avg"] = result.rolling(5).mean()
                    result_cols.append(f"{base_col_name}_Avg")

                if with_slope:
                    df[f"{base_col_name}_Slope"] = result.diff()
                    result_cols.append(f"{base_col_name}_Slope")

            elif isinstance(result, pd.DataFrame):
                for col in result.columns:
                    new_col = f"{col}_{label}" if not col.endswith(f"_{label}") else col
                    df[new_col] = result[col]
                    result_cols.append(new_col)

        except Exception as e:
            print(f"Error computing {name}: {e}")
            continue

    return df[result_cols]


# === Build Snapshot Across Tickers ===
def build_snapshot_with_indicators(tickers: list[str], interval: str) -> pd.DataFrame:
    period = INTERVAL_PERIOD_MAP.get(interval, "60d")
    label = interval.upper()
    results = []

    for ticker in tickers:
        try:
            df = yf.download(ticker, period=period, interval=interval, auto_adjust=False, progress=False)
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = [col[0] for col in df.columns]
            if df.empty or df.shape[0] < 20:
                continue

            df = compute_indicators(df, interval)

            result = {"Ticker": ticker}
            for col in df.columns:
                if not df[col].dropna().empty:
                    result[col] = df[col].dropna().iloc[-1]
                else:
                    result[col] = None

            results.append(result)

        except Exception as e:
            print(f"{ticker} error: {e}")
            results.append({"Ticker": ticker})

    return pd.DataFrame(results)
