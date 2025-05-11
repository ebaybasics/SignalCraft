# === analysis/summary.py ===

import pandas as pd
from config import SUMMARY_INDICATORS, SUMMARY_TOP_N, SUMMARY_INCLUDE_TOP_BOTTOM_ONLY

# === Summarize Top/Bottom ETFs Dynamically by Indicator ===
def summarize_top_bottom_indicators(
    snapshots: dict[str, pd.DataFrame]
) -> pd.DataFrame:
    def extract_sorted_lists(df, col, n):
        df_sorted = df.sort_values(by=col, ascending=False, na_position='last')
        return (
            df_sorted['Ticker'].head(n).tolist(),
            df_sorted['Ticker'].tail(n).tolist()[::-1]
        )

    summary = []

    for label, df in snapshots.items():
        snapshot_summary = {"Timeframe": label}

        for indicator in SUMMARY_INDICATORS:
            col_name = f"{indicator}_{label}"
            if col_name not in df.columns:
                print(f"⚠️ Missing: {col_name}")
                continue

            top, bottom = extract_sorted_lists(df, col_name, SUMMARY_TOP_N)
            snapshot_summary[f"{indicator}_Top"] = top
            snapshot_summary[f"{indicator}_Bottom"] = bottom

            # === Optional: Add context like Avg/Slope for the full set ===
            if not SUMMARY_INCLUDE_TOP_BOTTOM_ONLY:
                for suffix in ["Avg", "Slope"]:
                    context_col = f"{col_name}_{suffix}"
                    if context_col in df.columns:
                        snapshot_summary[f"{indicator}_{suffix}"] = (
                            df[context_col].mean(skipna=True).round(3)
                        )

        summary.append(snapshot_summary)

    return pd.DataFrame(summary)

