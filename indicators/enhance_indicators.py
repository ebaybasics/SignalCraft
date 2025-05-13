# === enhance_indicators.py ===

from config import INDICATOR_ENHANCERS
from indicators.post_indicator_proccessing_functions import (
    z_score, true_trend, signal_noise, slope_diff, smooth_series, velocity_rank
)
import pandas as pd

# === FUNC_MAP ===
# This dictionary maps enhancer names (as strings) to actual function implementations.
# It's used to dynamically apply feature engineering logic to base indicators.
#
# If you add a new enhancer function (e.g., kurtosis_score), make sure to:
#   - Define it in post_indicator_proccessing_functions.py
#   - Add it here with the same name used in INDICATOR_ENHANCERS
#   - Ensure it accepts a pd.Series and returns a pd.Series (or a scalar for rolling().apply)
#
# Naming conventions for output columns are enforced in apply_derived_features()

FUNC_MAP = {
    "z_score": z_score,
    "true_trend": lambda s: s.rolling(10).apply(true_trend, raw=False),
    "signal_noise": signal_noise,
    "slope_diff": slope_diff,
    "smooth_series": smooth_series,
    "velocity_rank": velocity_rank,
}

def apply_derived_features(df: pd.DataFrame, label: str) -> pd.DataFrame:
    """
    Applies configured post-indicator enhancements (like Z-score, Trend, Noise, etc.)
    to indicators listed in INDICATOR_ENHANCERS.

    Output column names follow the format: <Indicator>_<Enhancer>_<Label>
    e.g. "RSI_Z_1D", "OBV_Trend_1H"
    """
    for base_name, enhancers in INDICATOR_ENHANCERS.items():
        input_col = f"{base_name}_{label}"
        if input_col not in df.columns:
            continue

        for enhancer in enhancers:
            try:
                func = FUNC_MAP[enhancer]

                # Map enhancer names to suffix labels
                suffix = enhancer.replace("true_trend", "Trend") \
                                 .replace("slope_diff", "Impulse") \
                                 .replace("smooth_series", "Smoothed") \
                                 .replace("velocity_rank", "Velocity") \
                                 .replace("signal_noise", "Noise") \
                                 .replace("z_score", "Z")

                # Final output column: <Indicator>_<Enhancer>_<Label>
                output_col = f"{base_name}_{suffix}_{label}"
                df[output_col] = func(df[input_col])

            except Exception as e:
                print(f"❌ Error enhancing {input_col} with {enhancer}: {e}")

    return df
