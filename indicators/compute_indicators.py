# === compute_indicators.py ===

import pandas as pd
import pandas_ta as ta
import yfinance as yf
from config.config import INTERVAL_PERIOD_MAP, INDICATOR_REGISTRY


def compute_indicators(df: pd.DataFrame, interval: str) -> pd.DataFrame:
    """
    Compute all pure TA indicators listed in INDICATOR_REGISTRY.
    This function does not handle passthrough columns like VOLUME or derived columns like REL_VOLUME.
    """
    label = interval.upper()
    result_cols = []

    for name, meta in INDICATOR_REGISTRY.items():
        func_path = meta["func"]
        cols_needed = meta["columns"]
        params = meta["params"]

        # Ensure all required columns are present
        if not all(col in df.columns for col in cols_needed):
            print(f"Skipping {name} — missing required columns.")
            continue

        try:
            func = eval(func_path)  # or use getattr(ta, func_path)
            args = [df[col] for col in cols_needed]
            result = func(*args, **params)
            base_col_name = f"{name}_{label}"

            if isinstance(result, pd.Series):
                df[base_col_name] = result
                result_cols.append(base_col_name)

            elif isinstance(result, pd.DataFrame):
                for col in result.columns:
                    new_col = f"{col}_{label}" if not col.endswith(f"_{label}") else col
                    df[new_col] = result[col]
                    result_cols.append(new_col)

        except Exception as e:
            print(f"Error computing {name}: {e}")
            continue

    return df[result_cols]
