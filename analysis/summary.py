# === analysis/summary.py ===

import pandas as pd
from config import SUMMARY_INDICATORS

# === Summarize Top/Bottom ETFs Dynamically by Indicator ===
def summarize_top_bottom_indicators(
    snapshots: dict[str, pd.DataFrame],
    top_n: int = 10
) -> pd.DataFrame:
    def extract_sorted_lists(df, col):
        df_sorted = df.sort_values(by=col, ascending=False, na_position='last')
        return (
            df_sorted['Ticker'].head(top_n).tolist(),
            df_sorted['Ticker'].tail(top_n).tolist()[::-1]
        )

    summary = []

    for label, df in snapshots.items():
        snapshot_summary = {"Timeframe": label}

        for indicator in SUMMARY_INDICATORS:
            col_name = f"{indicator}_{label}"
            if col_name not in df.columns:
                print(f"⚠️ Missing: {col_name}")
                continue

            top, bottom = extract_sorted_lists(df, col_name)
            snapshot_summary[f"{indicator}_Top"] = top
            snapshot_summary[f"{indicator}_Bottom"] = bottom

        summary.append(snapshot_summary)

    return pd.DataFrame(summary)
