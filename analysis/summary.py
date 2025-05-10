# analysis/summary.py

import pandas as pd

def summarize_top_bottom_cmf(
    cmf5Minute: pd.DataFrame,
    cmfHour: pd.DataFrame,
    cmfDay: pd.DataFrame,
    cmfWeek: pd.DataFrame,
    cmfMonth: pd.DataFrame,
    top_n: int = 10
) -> pd.DataFrame:
    def extract_sorted_lists(df, col):
        df_sorted = df.sort_values(by=col, ascending=False, na_position='last')
        return (
            df_sorted['Ticker'].head(top_n).tolist(),
            df_sorted['Ticker'].tail(top_n).tolist()[::-1]
        )

    summary = []
    snapshots = [
        ("5M", cmf5Minute, "CMF_5M", "RSI_5M"),
        ("1H", cmfHour, "CMF_1H", "RSI_1H"),
        ("1D", cmfDay, "CMF_1D", "RSI_1D"),
        ("1W", cmfWeek, "CMF_1WK", "RSI_1WK"),
        ("1M", cmfMonth, "CMF_1MO", "RSI_1MO")
    ]

    for label, df, cmf_col, rsi_col in snapshots:
        if cmf_col not in df.columns or rsi_col not in df.columns:
            raise ValueError(f"{label} missing: {cmf_col}, {rsi_col}")
        cmf_top, cmf_bottom = extract_sorted_lists(df, cmf_col)
        rsi_top, rsi_bottom = extract_sorted_lists(df, rsi_col)
        summary.append({
            "Timeframe": label,
            "Top_ETFs": cmf_top,
            "Bottom_ETFs": cmf_bottom,
            "RSI_Top": rsi_top,
            "RSI_Bottom": rsi_bottom
        })

    return pd.DataFrame(summary)
