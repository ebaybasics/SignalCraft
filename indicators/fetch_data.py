import yfinance as yf
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict
import threading


def fetch_ticker_data(ticker: str, interval: str, period: str = "60d") -> pd.DataFrame:

    df = yf.download(
        ticker,
        period=period,
        interval=interval,
        auto_adjust=False,
        progress=False,
        threads=False  # Important when using multithreading outside yfinance
    )

    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [col[0] for col in df.columns]

    if df.empty:
        raise ValueError(f"No data for {ticker} at interval {interval}")

    return df


def fetch_multiple_tickers(
    tickers: List[str],
    interval: str,
    period: str = "60d",
    max_workers: int = 5
) -> Dict[str, pd.DataFrame]:
    """
    Fetch OHLCV data for multiple tickers concurrently using up to 5 threads.

    Returns:
        A dictionary of {ticker: DataFrame}
    """
    results = {}

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_ticker = {
            executor.submit(fetch_ticker_data, ticker, interval, period): ticker
            for ticker in tickers
        }

        for future in as_completed(future_to_ticker):
            ticker = future_to_ticker[future]
            try:
                df = future.result()
                results[ticker] = df
                print(f"✅ {ticker} fetched")
            except Exception as e:
                print(f"❌ {ticker} failed: {e}")

    return results



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
