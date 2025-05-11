# indicators/fetch_data.py

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def fetch_ticker_data(ticker: str, interval: str = "1d", years: int = 5) -> pd.DataFrame:
    end_date = datetime.today()
    if interval in ["1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h"]:
        start_date = end_date - timedelta(days=59)
    else:
        start_date = end_date - timedelta(days=years * 365)

    df = yf.download(
        ticker,
        start=start_date,
        end=end_date,
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
    snapshot_rows = []

    for tf in timeframes:
        try:
            df = fetch_ticker_data(ticker, interval=tf, years=1)
            last_row = df.iloc[-1]  # Get most recent OHLCV
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