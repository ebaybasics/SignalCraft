# run_narration_test.py

import pandas as pd
from chatgpt.client import get_narration


# === Load and combine market snapshot data ===
def load_market_data():
    df_5m = pd.read_csv("data/marketData/marketData_5M.csv")
    df_1h = pd.read_csv("data/marketData/marketData_1H.csv")
    df_1d = pd.read_csv("data/marketData/marketData_1D.csv")
    df_1wk = pd.read_csv("data/marketData/marketData_1WK.csv")
    df_1mo = pd.read_csv("data/marketData/marketData_1MO.csv")
    df_summary = pd.read_csv("data/indicatorSummary.csv")
    
    return {
        "Indicator Summary": df_summary,
        "5M": df_5m,
        "1H": df_1h,
        "1D": df_1d,
        "1WK": df_1wk,
        "1MO": df_1mo
    }


# === Format each timeframe's data ===
def format_snapshot(df: pd.DataFrame, timeframe: str) -> str:
    header = f"\n\n{'=' * 8} {timeframe.upper()} {'=' * 8}\n"
    text = df.to_csv(index=False)
    return header + text


# === Compose full input message for GPT ===
def build_input_message(data: dict) -> str:
    ordered_keys = ["Indicator Summary", "5M", "1H", "1D", "1WK", "1MO"]
    return "\n".join([format_snapshot(data[tf], tf) for tf in ordered_keys if tf in data])


# === Run narration ===
def main():
    data = load_market_data()
    input_text = build_input_message(data)
    narration = get_narration(input_text)
    print("📈 SignalCraft Narration:\n")
    print(narration)

if __name__ == "__main__":
    main()
