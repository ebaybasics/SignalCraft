# indicators/fetch_data.py

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def fetch_ticker_data(ticker: str, interval: str, period: str = "60d") -> pd.DataFrame:
    """
    Download historical OHLCV data for a given ticker and interval using yfinance.

    Args:
        ticker: Ticker symbol (e.g., "AAPL").
        interval: Data interval (e.g., "1d", "1wk", "5m").
        period: Lookback period or custom duration (e.g., "60d", "1y").

    Returns:
        A DataFrame with OHLCV data.
    """
    df = yf.download(
        ticker,
        period=period,
        interval=interval,
        auto_adjust=False,
        progress=False
    )

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [col[0] for col in df.columns]

    if df.empty:
        raise ValueError(f"No data for {ticker} at interval {interval}")

    return df


def generate_ohlcv_snapshots(ticker: str, timeframes: list[str]) -> pd.DataFrame:
    """
    Generate the most recent OHLCV row for multiple timeframes for a single ticker.

    Args:
        ticker: Ticker symbol.
        timeframes: List of timeframes (e.g., ["1d", "1wk", "1mo"]).

    Returns:
        DataFrame of latest OHLCV data for each timeframe.
    """
    snapshot_rows = []

    for tf in timeframes:
        try:
            df = fetch_ticker_data(ticker, interval=tf, period="1y")
            last_row = df.iloc[-1]
            snapshot_rows.append({
                "Ticker": ticker,
                "Timeframe": tf.upper(),
                "Open": last_row["Open"],
                "High": last_row["High"],
                "Low": last_row["Low"],
                "Close": last_row["Close"],
                "Volume": last_row["Volume"]
            })
        except Exception as e:
            print(f"⚠️ {ticker} {tf}: {e}")

    return pd.DataFrame(snapshot_rows)
