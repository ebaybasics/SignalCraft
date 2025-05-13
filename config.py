# config.py

# === ETF Ticker List ===
tickers = [
    "SPY", "QQQ", "DIA", "IWM", "VTI", "VOO", "IVV",
    "XLK", "XLF", "XLY", "XLP", "XLV", "XLE", "XLI", "XLRE", "XLU", "XLB", "XLC",
    "ARKK", "SMH", "TAN", "PBW", "FXI", "EEM", "EFA", "TLT", "HYG", "UUP", "SLV",
    "SIL", "GDX", "GLD", "VXX"
]

#=== Individual Ticker List ===
# tickers = [
#     "ENPH",   # Enphase Energy
#     "SEDG",   # SolarEdge Technologies
#     "FSLR",   # First Solar
#     "SPWR",   # SunPower Corporation
#     "RUN",    # Sunrun Inc.
#     "CSIQ",   # Canadian Solar
#     "SHLS",   # Shoals Technologies
#     "JKS",    # JinkoSolar
#     "DQ",     # Daqo New Energy
#     "MAXN",   # Maxeon Solar Technologies
#     "ARRY",   # Array Technologies
#     "NOVAR",  # NovaSource Power Services (if applicable)
#     "TAN"     # Invesco Solar ETF (good proxy for the whole group)
# ]



# === Tickers for Support Resistance Price Volume Data ===
SR_tickers = []

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
    "1mo": "20y",
    "3mo": "20y"

}


# === Indicator Registry ===
INDICATOR_REGISTRY = {
    "CMF": {"func": "ta.cmf", "columns": ["High", "Low", "Close", "Volume"], "params": {"length": 20}, "with_avg": True, "with_slope": True},
    "RSI": {"func": "ta.rsi", "columns": ["Close"], "params": {"length": 14}, "with_avg": True, "with_slope": True},
    "ROC": {"func": "ta.roc", "columns": ["Close"], "params": {"length": 10}},
    "MACD": {"func": "ta.macd", "columns": ["Close"], "params": {}},
    "EMA_50": {"func": "ta.ema", "columns": ["Close"], "params": {"length": 50}},
    "BBANDS": {"func": "ta.bbands", "columns": ["Close"], "params": {"length": 20, "std": 2}},
    "ADX": {"func": "ta.adx", "columns": ["High", "Low", "Close"], "params": {"length": 14}},  # optional but helpful
    "VOLUME": {"func": None, "columns": ["Volume"], "params": {}, "with_avg": True, "with_slope": True},
    "REL_VOLUME": {"func": None, "columns": ["Volume"], "params": {}, "with_avg": False, "with_slope": False}
    
}


# === Summary Output Indicators ===
SUMMARY_INDICATORS = ["CMF", "RSI", "REL_VOLUME"]
SUMMARY_TOP_N = 3
SUMMARY_INCLUDE_TOP_BOTTOM_ONLY = True