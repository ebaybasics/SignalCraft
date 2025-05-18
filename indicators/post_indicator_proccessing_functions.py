from scipy.stats import linregress
import pandas as pd
import numpy as np
from config.config import INDICATOR_ENHANCERS  

# ========== Helper Functions for Indicator Analysis ==========

def slope_diff(series: pd.Series, n: int = 1) -> pd.Series:
    """Compute simple n-period difference (impulse)."""
    return series.diff(n)

def smooth_series(series: pd.Series, n: int = 3) -> pd.Series:
    """Smooth a series with a rolling mean."""
    return series.rolling(n).mean()

def true_trend(series: pd.Series, window: int = 20) -> float:
    """Calculate the slope of the linear regression line."""
    if len(series.dropna()) < window:
        return np.nan
    y = series.dropna().iloc[-window:]
    x = np.arange(len(y))
    slope, _, _, _, _ = linregress(x, y)
    return slope

def velocity_rank(series: pd.Series) -> pd.Series:
    """Measure percentage change as velocity ranking."""
    return series.pct_change()

def signal_noise(series: pd.Series, window: int = 5) -> pd.Series:
    """Measure standard deviation over a rolling window."""
    return series.rolling(window).std()

def z_score(series: pd.Series) -> pd.Series:
    """Compute the Z-score for cross-ticker comparison."""
    mean = series.mean()
    std = series.std()
    return (series - mean) / std

def vwap_distance_z_score(close: pd.Series, vwap: pd.Series, window: int = 20) -> pd.Series:
    """Z-score of the distance between Close and VWAP over a rolling window."""
    dist = close - vwap
    mean = dist.rolling(window).mean()
    std = dist.rolling(window).std()
    return (dist - mean) / std

def series_vwap(high, low, close, volume, window=20):
    """Rolling VWAP over the specified window (default 20)."""
    price = (high + low + close) / 3
    vwap = (price * volume).rolling(window=window).sum() / volume.rolling(window=window).sum()
    return vwap

def add_sumZZ(df: pd.DataFrame, label: str, out_col=None):
    """
    Dynamically sums all z-score columns for this timeframe, based on INDICATOR_ENHANCERS.
    Only includes indicators that have 'z_score' as an enhancer.
    """
    # Find all indicators with 'z_score' in their enhancer list
    features = [key for key, enh in INDICATOR_ENHANCERS.items() if "z_score" in enh]
    if out_col is None:
        out_col = f"sumZZ_{label}"
    zscore_cols = [f"{feat}_Z_{label}" for feat in features]
    # Only sum columns that exist (robust to missing)
    zscore_cols_exist = [col for col in zscore_cols if col in df.columns]
    df[out_col] = df[zscore_cols_exist].sum(axis=1, skipna=True)
    return df
