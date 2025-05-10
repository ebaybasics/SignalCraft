# config.py

# === ETF Ticker List ===
tickers = [
    "SPY", "QQQ", "DIA", "IWM", "VTI", "VOO", "IVV",
    "XLK", "XLF", "XLY", "XLP", "XLV", "XLE", "XLI", "XLRE", "XLU", "XLB", "XLC",
    "ARKK", "SMH", "TAN", "PBW", "FXI", "EEM", "EFA", "TLT", "HYG"
]

# === Indicator Parameters ===
DEFAULT_CMF_LENGTH = 20
DEFAULT_RSI_LENGTH = 14

# === Snapshot Timeframes & History Periods ===
INTERVAL_PERIOD_MAP = {
    "1m": "7d",
    "2m": "30d",
    "5m": "30d",
    "15m": "30d",
    "30m": "30d",
    "60m": "60d",
    "90m": "60d",
    "1h": "60d",
    "1d": "5y",
    "1wk": "10y",
    "1mo": "20y"
}


# === Indicator Registry ===
INDICATOR_REGISTRY = {
    "CMF": {
        "func": "ta.cmf",
        "columns": ["High", "Low", "Close", "Volume"],
        "params": {"length": 20}
    },
    "RSI": {
        "func": "ta.rsi",
        "columns": ["Close"],
        "params": {"length": 14}
    },
    "MACD": {
        "func": "ta.macd",
        "columns": ["Close"],
        "params": {}  # default fast=12, slow=26, signal=9
    },
    "BBANDS": {
        "func": "ta.bbands",
        "columns": ["Close"],
        "params": {"length": 20, "std": 2}
    },
    "EMA_21": {
        "func": "ta.ema",
        "columns": ["Close"],
        "params": {"length": 21}
    },
    "EMA_50": {
        "func": "ta.ema",
        "columns": ["Close"],
        "params": {"length": 50}
    },
    "ROC": {
        "func": "ta.roc",
        "columns": ["Close"],
        "params": {"length": 10}
    },
    "OBV": {
        "func": "ta.obv",
        "columns": ["Close", "Volume"],
        "params": {}
    }
}

# === Summary Output Indicators ===
SUMMARY_INDICATORS = ["CMF", "RSI"]
