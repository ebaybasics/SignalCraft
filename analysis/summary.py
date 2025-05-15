import pandas as pd
from config.config import SUMMARY_INDICATORS, SUMMARY_TOP_N, SUMMARY_INCLUDE_TOP_BOTTOM_ONLY

# === Summarize Top/Bottom ETFs Dynamically by Indicator ===
def summarize_top_bottom_indicators(
    snapshots: dict[str, pd.DataFrame]
) -> pd.DataFrame:
    
    def extract_sorted_dicts(df, value_col, indicator_name, n):
        df_sorted = df.sort_values(by=value_col, ascending=False, na_position='last')
        top = [
            {
                "Ticker": row["Ticker"],
                "Indicator": indicator_name,
                "Value": round(row[value_col], 4)
            }
            for _, row in df_sorted.head(n).iterrows()
        ]
        bottom = [
            {
                "Ticker": row["Ticker"],
                "Indicator": indicator_name,
                "Value": round(row[value_col], 4)
            }
            for _, row in df_sorted.tail(n).iloc[::-1].iterrows()
        ]
        return top, bottom

    summary = []

    for label, df in snapshots.items():
        snapshot_summary = {"Timeframe": label}

        for indicator in SUMMARY_INDICATORS:
            col_name = f"{indicator}_{label}"
            if col_name not in df.columns:
                print(f"⚠️ Missing: {col_name}")
                continue

            try:
                top, bottom = extract_sorted_dicts(df, col_name, indicator, SUMMARY_TOP_N)
                snapshot_summary[f"{indicator}_Top"] = top
                snapshot_summary[f"{indicator}_Bottom"] = bottom
            except Exception as e:
                print(f"❌ Error summarizing {indicator} on {label}: {e}")
                continue

            if not SUMMARY_INCLUDE_TOP_BOTTOM_ONLY:
                for suffix in ["Avg", "Slope"]:
                    context_col = f"{col_name}_{suffix}"
                    if context_col in df.columns:
                        snapshot_summary[f"{indicator}_{suffix}"] = (
                            df[context_col].mean(skipna=True).round(3)
                        )

        summary.append(snapshot_summary)

    return pd.DataFrame(summary)
