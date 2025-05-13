# config.py




# === ETF Ticker List ===
tickers = [
    "SPY", "QQQ", "DIA", "IWM", "VTI", "VOO", "IVV",
    "XLK", "XLF", "XLY", "XLP", "XLV", "XLE", "XLI", "XLRE", "XLU", "XLB", "XLC",
    "ARKK", "SMH", "TAN", "PBW", "FXI", "EEM", "EFA", "TLT", "HYG", "UUP", "SLV",
    "SIL", "GDX", "GLD", "VXX"
]

# #=== Individual Ticker List ===
# tickers = [
#     "ENPH",   # Enphase Energy
#     "SEDG",   # SolarEdge Technologies
#     "FSLR",   # First Solar

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


}


# === INDICATOR_REGISTRY ===
# This registry defines all base indicators used in the system and maps them to their corresponding
# technical analysis functions, parameter configurations, and input column requirements.
#
# These are **pure indicator definitions** — no enhancements or derived signals.
# Each `func` refers to a function from the `pandas_ta` library (e.g., `ta.rsi`, `ta.macd`), which is
# called inside `compute_indicators()` in `compute_indicators.py`.
#
# Fields:
# - "func": String path to the pandas_ta function (or None for passthroughs like VOLUME)
# - "columns": List of required OHLCV inputs
# - "params": Dict of parameters passed to the ta function
# - "with_avg": If True, appends a rolling average (e.g. RSI_1H_Avg)
# - "with_slope": If True, appends a simple diff-based slope (e.g. OBV_1D_Slope)
#
# IMPORTANT:
# - These functions are evaluated dynamically using `eval()` or `getattr()` in compute_indicators.py
# - This is the only place that defines which raw indicators are computed — enhancements come later
#
# If you're adding a new ta indicator, define it here first before building any enhancements.
INDICATOR_REGISTRY = {
    "CMF": {"func": "ta.cmf", "columns": ["High", "Low", "Close", "Volume"], "params": {"length": 20}, "with_avg": True, "with_slope": True},
    "RSI": {"func": "ta.rsi", "columns": ["Close"], "params": {"length": 14}, "with_avg": True, "with_slope": True},
    "ROC": {"func": "ta.roc", "columns": ["Close"], "params": {"length": 10}},
    "MACD": {"func": "ta.macd", "columns": ["Close"], "params": {}},
    "EMA_50": {"func": "ta.ema", "columns": ["Close"], "params": {"length": 50}},
    "BBANDS": {"func": "ta.bbands", "columns": ["Close"], "params": {"length": 20, "std": 2}},
    "ADX": {"func": "ta.adx", "columns": ["High", "Low", "Close"], "params": {"length": 14}},
    "OBV": {"func": "ta.obv", "columns": ["Close", "Volume"], "params": {}, "with_avg": True, "with_slope": True}
}


# === INDICATOR_ENHANCERS ===
# This dictionary defines which post-processing functions should be applied to each indicator
# after the base values are computed via `compute_indicators()`.
#
# The function names listed here must match the function names defined in `post_indicator_proccessing_functions.py`
# and must also be registered in the `FUNC_MAP` inside `enhance_indicators.py`.
#
# These enhancements are applied in `apply_derived_features()` and will mutate the final snapshot
# with columns like OBV_1H_Z, CMF_1D_Trend, etc.
#
# Only add functions here that are intended to be post-processing steps applied to the original indicator values.
INDICATOR_ENHANCERS = {
    "OBV": ["z_score", "true_trend", "signal_noise", "slope_diff", "smooth_series", "velocity_rank"],
    "CMF": ["z_score", "true_trend"],
    "RSI": ["slope_diff", "signal_noise", "z_score"],
    # Add more as needed
}

PASSTHROUGH_REGISTRY = {
    "VOLUME": {
        "source": "Volume",
        "with_avg": True,
        "with_slope": True
    },
    "REL_VOLUME": {
        "source": "Volume",  # still required for fallback
        "with_avg": False,
        "with_slope": False
    }
}


# === Summary Output Indicators ===
SUMMARY_INDICATORS = ["CMF", "RSI", "REL_VOLUME", "RSI_Z", "CMF_Z", "RSI_Noise", "OBV_Z"]
SUMMARY_TOP_N = 3
SUMMARY_INCLUDE_TOP_BOTTOM_ONLY = True