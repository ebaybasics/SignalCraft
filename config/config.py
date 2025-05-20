# config.py




# === ETF Ticker List ===
tickers = [
    # ─── U.S. Broad Equity Benchmarks ───
    "SPY",  # S&P 500
    "QQQ",  # Nasdaq-100
    "DIA",  # Dow 30
    "IWM",  # Russell 2000
    "VTI", "VOO",  # Total-market & alt S&P 500 wrappers

    # ─── U.S. Style & Factor Tilts ───
    "VUG",  # Growth
    "VTV",  # Value
    "MTUM", # Momentum
    "QUAL", # Quality
    "USMV", # Min-Vol

    # ─── U.S. Sector SPDRs (unchanged) ───
    "XLK","XLF","XLY","XLP","XLV","XLE","XLI","XLRE","XLU","XLB","XLC",

    # ─── Thematic / Innovation ───
    "ARKK", "SMH", "TAN", "PBW",

    # ─── Global & Regional Equity ───
    "EEM",  # EM broad
    "EFA",  # Developed ex-US
    "IEFA", # Cheaper developed ex-US core
    "FXI",  # China large-cap
    "INDA", # India
    "EWZ",  # Brazil
    "VEA",  # Developed Pacific & Europe

    # ─── Fixed-Income & Rates ───
    "TLT",  # 20-yr Treasury
    "IEF",  # 7-10 yr Treasury
    "SHY",  # 1-3 yr Treasury (front-end stress)
    "TIP",  # US TIPS (inflation breakevens)
    "BNDX", # Global AGG ex-US (hedged)
    "EMB",  # EM USD sovereigns
    "LQD",  # Invest-grade corporate
    "HYG",  # High-yield corporate

    # ─── Commodities ───
    "USO",  # WTI crude
    "BNO",  # Brent crude
    "UNG",  # Nat-gas
    "GLD", "GDX", "SLV", "SIL",  # Precious metals + miners
    "CPER", # Copper (Dr Copper = growth pulse)
    "DBA",  # Agriculture basket
    "DBC",  # Broad commodity basket

    # ─── Currencies / Dollar Smile ───
    "UUP",  # Long USD
    "FXE",  # Euro
    "FXY",  # Japanese Yen
    "CYB",  # Chinese Yuan (on-shore proxy)

    # ─── Real Assets & Alt-Inflation Hedges ───
    "VNQ",  # US REITs
    "REET", # Global REITs
    "INFL", # Real-asset / commodity equities sleeve

    # ─── Volatility & Tail Risk ───
    "VXX"   # Short-term VIX futures ETN
]

#=== Individual Ticker List ===
# tickers = [
#     "NXT",
#     "ENPH",
#     "EVRG",
#     "MSFT",
#     "QQQ",
#     "NVDA",
#     "ANET",
#     "AMZN",
#     "FSLR",
#     "SHLS"
# 
# ]

#Top Utilities
# tickers = [
#     'UGI',
#     'SWX',
#     'AVA',
#     'WEC',
#     'ATO',
#     'ED',
#     'AEE',
#     'XEL',
#     'DTE',
#     'EVRG'
# ]

#AI Hardware and Accelerators
# tickers = [
#     'NVDA',
#     'AMD',
#     'AVGO',
#     'MRVL',
#     'INTC',
#     'ACLS',
#     'AEHR',
#     'SMCI',
#     'LITE'
# ]

# AI Power Themed Utility AI Suggesstions
# tickers = [
#     "NEE",
#     "CEG",
#     "VST",
#     "NRG",
#     "DUK",
#     "SO",
#     "SRE",
#     "AEP",
#     "XEL",

# ]


# Individual
# tickers = [
#     'NVDA',
#     'AMD',
#     'AVGO',
# ]

# Top 5 XLV Holdings as of 5/20
# tickers = [
#     "LLY",
#     "JNJ",
#     "ABBV",
#     "UNH",
#     "ABT"
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
    # ─── Money-flow / Volume ───
    "CMF":  {"func": "ta.cmf",  "columns": ["High", "Low", "Close", "Volume"],
             "params": {"length": 20}, "with_avg": True, "with_slope": True},
    "OBV":  {"func": "ta.obv",  "columns": ["Close", "Volume"], "params": {},
             "with_avg": True, "with_slope": True},

    # ─── Momentum & Oscillators ───
    "RSI":  {"func": "ta.rsi",  "columns": ["Close"], "params": {"length": 14},
             "with_avg": True, "with_slope": True},
    "MACD": {"func": "ta.macd", "columns": ["Close"], "params": {}},

    # ─── Volatility / Range ───
    "ATR":  {"func": "ta.atr",  "columns": ["High", "Low", "Close"],
             "params": {"length": 14}, "with_avg": True, "with_slope": True},

    # ─── Price-positioning ───
    "VWAP": {"func": "series_vwap", "columns": ["High", "Low", "Close", "Volume"],
             "params": {"window": 20}},
    "BB_POS": {"func": "ta.bbands", "columns": ["Close"],
               "params": {"length": 20, "std": 2, "append": False}}
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
    "OBV":   ["z_score", "true_trend"],  # z_score for regime, optional: "velocity_rank" if you want unique flows
    "CMF":   ["z_score", "true_trend"],  # z_score for outlier accumulation/distribution
    "RSI":   ["z_score"],  # z_score for unusual momentum regime
    "MACDh_12_26_9":  ["z_score"],  # z_score for unusual MACD movement (optional)
    "VOLUME":   ["z_score"],  # z_score plus a percentile/spike check (see below)
    "VWAP":  ["z_score"],  # z_score for price stretch
    "ATR": ["z_score"]
}

# List of base features to include for LLM csv files, minus suffix (timeframe label)
BASE_FEATURES = [
    "RSI",
    "RSI_Z",
    "BBP_20_2.0",
    "MACDh_12_26_9_Z",
    "OBV_Z",
    "CMF",
    "CMF_Z",
    "VWAP_Z",
    "sumZZ",
    "slope_sumZZ",
    "ATR_Z"    
]

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
SUMMARY_INDICATORS = ["CMF", "RSI_Z", "CMF_Z", "OBV_Z", "MACDh_12_26_9_Z", "VWAP_Z", "sumZZ"]
SUMMARY_TOP_N = 2
SUMMARY_INCLUDE_TOP_BOTTOM_ONLY = True