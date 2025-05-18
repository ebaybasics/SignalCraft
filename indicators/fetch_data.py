# === Alpaca Stock-data helpers ============================================
# pip install alpaca-py
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame, TimeFrameUnit
import pandas as pd, os, re
from datetime import datetime, timezone, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List
from config.credentials import ALPACA_SECRET, ALPACA_API_KEY

# ── 1)  Initialise the client (paper- or live-key both work) ──────────────

_data_client = StockHistoricalDataClient(
    api_key       = ALPACA_API_KEY,
    secret_key    = ALPACA_SECRET,
    # raw_data      = True             # ⇢ return a tidy pd.DataFrame
)

# ── 2)  yfinance-style interval → Alpaca TimeFrame mapping ────────────────
INTERVAL_MAP = {
    "1m" : TimeFrame.Minute,
    "5m" : TimeFrame(5 , TimeFrameUnit.Minute),
    "15m": TimeFrame(15, TimeFrameUnit.Minute),
    "30m": TimeFrame(30, TimeFrameUnit.Minute),
    "60m": TimeFrame.Hour,           # yfinance alias for 1-hour
    "1h" : TimeFrame.Hour,
    "1d" : TimeFrame.Day,
    "1wk": TimeFrame.Week,
    "1mo": TimeFrame.Month,
}

# ── 3)  Helper → convert “60d”, “1y”, “2mo” … to UTC start-date ───────────
_PERIOD_RE = re.compile(r"(?P<num>\d+)(?P<unit>[dmwy])")
_UNIT_TO_DAYS = {"d":1, "w":7, "m":30, "y":365}      # rough is fine for look-backs

def _period_to_start(period: str) -> datetime:
    m = _PERIOD_RE.fullmatch(period)
    if not m:
        raise ValueError(f"Unsupported period {period!r}")
    days = int(m["num"]) * _UNIT_TO_DAYS[m["unit"]]
    return datetime.now(timezone.utc) - timedelta(days=days)

# ── 4)  Core fetch function – same signature as before ────────────────────
def fetch_ticker_data(
    ticker: str,
    interval: str,
    period: str = "60d",
) -> pd.DataFrame:
    """Return OHLCV data in yfinance format via Alpaca."""
    tf = INTERVAL_MAP.get(interval)
    if tf is None:
        raise ValueError(f"Unsupported interval {interval}")

    request = StockBarsRequest(
        symbol_or_symbols = ticker,
        timeframe         = tf,
        start             = _period_to_start(period),
        end               = datetime.now(timezone.utc),
        adjustment        = "raw",        # ⇢ yfinance default is unadjusted
        feed              = "iex",        # free plan; use "sip" if you pay
    )

    bars = _data_client.get_stock_bars(request).df     # multi-index (symbol, time)
    if bars.empty:
        raise ValueError(f"No data for {ticker} at {interval}")

    # Flatten multi-index, rename to match yfinance, keep only needed cols
    bars = (
        bars.xs(ticker, level="symbol")   # drop symbol level
            .rename(
                columns={
                    "open"  : "Open",
                    "high"  : "High",
                    "low"   : "Low",
                    "close" : "Close",
                    "volume": "Volume",
                }
            )[["Open", "High", "Low", "Close", "Volume"]]
    )
    bars.index.name = "Date"
    return bars

# ── 5)  Multi-ticker fetch (unchanged API) ────────────────────────────────
def fetch_multiple_tickers(
    tickers: List[str],
    interval: str,
    period: str = "60d",
    max_workers: int = 5
) -> Dict[str, pd.DataFrame]:
    results = {}
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        fut_to_tkr = {
            pool.submit(fetch_ticker_data, tkr, interval, period): tkr
            for tkr in tickers
        }
        for fut in as_completed(fut_to_tkr):
            tkr = fut_to_tkr[fut]
            try:
                results[tkr] = fut.result()
                print(f"✅ {tkr} fetched")
            except Exception as e:
                print(f"❌ {tkr} failed: {e}")
    return results

# ── 6)  Snapshot helper – works exactly like your original ────────────────
def generate_ohlcv_snapshots(ticker: str, timeframes: list[str]) -> pd.DataFrame:
    snapshot_rows = []
    for tf in timeframes:
        try:
            df = fetch_ticker_data(ticker, interval=tf, period="1y")
            last = df.iloc[-1]
            snapshot_rows.append({
                "Ticker"   : ticker,
                "Timeframe": tf.upper(),
                "Open"     : last["Open"],
                "High"     : last["High"],
                "Low"      : last["Low"],
                "Close"    : last["Close"],
                "Volume"   : last["Volume"],
            })
        except Exception as e:
            print(f"⚠️ {ticker} {tf}: {e}")
    return pd.DataFrame(snapshot_rows)
