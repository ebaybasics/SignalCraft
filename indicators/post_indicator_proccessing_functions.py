from scipy.stats import linregress
import pandas as pd
import numpy as np

# ========== Helper Functions for Indicator Analysis ==========

def slope_diff(series: pd.Series, n: int = 1) -> pd.Series:
    """Compute simple n-period difference (impulse)."""
    return series.diff(n)

def smooth_series(series: pd.Series, n: int = 3) -> pd.Series:
    """Smooth a series with a rolling mean."""
    return series.rolling(n).mean()

def true_trend(series: pd.Series, window: int = 10) -> float:
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