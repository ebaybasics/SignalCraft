# === analysis/support_resistance.py ===

import pandas as pd

def get_support_resistance(df: pd.DataFrame, bins: int = 30) -> dict:
    """
    Estimate support and resistance using volume-weighted price bins.

    Parameters:
        df (pd.DataFrame): Must contain 'Close' and 'Volume'
        bins (int): Number of price levels to segment

    Returns:
        dict: Strong/weak support and resistance levels
    """
    if "Close" not in df.columns or "Volume" not in df.columns:
        raise ValueError("DataFrame must include 'Close' and 'Volume' columns")

    # Create volume-by-price profile
    min_price = df["Close"].min()
    max_price = df["Close"].max()
    price_range = max_price - min_price
    step = price_range / bins

    volume_profile = {}
    for i in range(bins):
        lower = min_price + i * step
        upper = lower + step
        mask = df["Close"].between(lower, upper)
        volume = df.loc[mask, "Volume"].sum()
        volume_profile[round((lower + upper) / 2, 2)] = volume

    # Sort by volume and pick top clusters
    sorted_levels = sorted(volume_profile.items(), key=lambda x: x[1], reverse=True)
    top_levels = [price for price, vol in sorted_levels[:5]]

    # Split into support and resistance based on current price
    current_price = df["Close"].iloc[-1]
    support = sorted([lvl for lvl in top_levels if lvl < current_price], reverse=True)
    resistance = sorted([lvl for lvl in top_levels if lvl > current_price])

    return {
        "strong_support": support[:2],
        "weak_support": support[2:],
        "strong_resistance": resistance[:2],
        "weak_resistance": resistance[2:]
    }
