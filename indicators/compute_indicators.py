# indicators/compute_indicators.py

import pandas as pd
import pandas_ta as ta
from config import DEFAULT_CMF_LENGTH, DEFAULT_RSI_LENGTH, INTERVAL_PERIOD_MAP

def compute_indicators(df: pd.DataFrame, interval: str, cmf_len: int = DEFAULT_CMF_LENGTH, rsi_len: int = DEFAULT_RSI_LENGTH) -> pd.DataFrame:
    cmf_col = f"CMF_{interval.upper()}"
    rsi_col = f"RSI_{interval.upper()}"
    df[cmf_col] = ta.cmf(df['High'], df['Low'], df['Close'], df['Volume'], length=cmf_len)
    df[rsi_col] = ta.rsi(df['Close'], length=rsi_len)
    return df[[cmf_col, rsi_col]]

def build_snapshot_with_indicators(tickers: list[str], interval: str) -> pd.DataFrame:
    import yfinance as yf  # local import to avoid circular issues
    period = INTERVAL_PERIOD_MAP.get(interval, "60d")
    cmf_label = f"CMF_{interval.upper()}"
    rsi_label = f"RSI_{interval.upper()}"
    results = []

    for ticker in tickers:
        try:
            df = yf.download(ticker, period=period, interval=interval, auto_adjust=False, progress=False)
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = [col[0] for col in df.columns]
            if df.empty or df.shape[0] < 20:
                continue

            df = compute_indicators(df, interval)
            cmf = df[cmf_label].dropna().iloc[-1] if not df[cmf_label].dropna().empty else None
            rsi = df[rsi_label].dropna().iloc[-1] if not df[rsi_label].dropna().empty else None
            results.append({"Ticker": ticker, cmf_label: cmf, rsi_label: rsi})

        except Exception as e:
            print(f"{ticker} error: {e}")
            results.append({"Ticker": ticker, cmf_label: None, rsi_label: None})

    return pd.DataFrame(results)
