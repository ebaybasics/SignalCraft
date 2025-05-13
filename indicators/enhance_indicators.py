from config import INDICATOR_ENHANCERS
from indicators.post_indicator_proccessing_functions import (
    z_score, true_trend, signal_noise, slope_diff, smooth_series, velocity_rank
)
import pandas as pd

# === FUNC_MAP ===
# This dictionary maps string names from INDICATOR_ENHANCERS to the actual function implementations.
# It is used in `apply_derived_features()` to dynamically apply enhancements to indicators.
# 
# IMPORTANT: If you define a new enhancement function (e.g., kurtosis_score, trend_stability),
# you MUST add it here using the same string key as used in INDICATOR_ENHANCERS.
# Otherwise, the enhancer will be ignored or raise a KeyError during enhancement.
#
# Convention:
# - Keys must match strings listed in INDICATOR_ENHANCERS
# - Values must be callables that accept a pandas Series and return a Series (or use .rolling().apply for windowed ops)

FUNC_MAP = {
    "z_score": z_score,
    "true_trend": lambda s: s.rolling(10).apply(true_trend, raw=False),
    "signal_noise": signal_noise,
    "slope_diff": slope_diff,
    "smooth_series": smooth_series,
    "velocity_rank": velocity_rank,
}

def apply_derived_features(df: pd.DataFrame, label: str) -> pd.DataFrame:
    for base_name, enhancers in INDICATOR_ENHANCERS.items():
        col_name = f"{base_name}_{label}"
        if col_name not in df.columns:
            continue

        for enhancer in enhancers:
            try:
                func = FUNC_MAP[enhancer]
                new_col = f"{col_name}_{enhancer.replace('true_trend', 'Trend').replace('slope_diff', 'Impulse').replace('smooth_series', 'Smoothed').replace('velocity_rank', 'Velocity').replace('signal_noise', 'Noise').replace('z_score', 'Z')}"
                df[new_col] = func(df[col_name])
            except Exception as e:
                print(f"❌ Error enhancing {col_name} with {enhancer}: {e}")
    return df
