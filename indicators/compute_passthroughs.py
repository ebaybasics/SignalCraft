# === compute_passthroughs.py ===

import pandas as pd
from config.config import PASSTHROUGH_REGISTRY

def compute_passthroughs(df: pd.DataFrame, interval: str) -> pd.DataFrame:
    """
    Apply passthrough indicators (e.g., VOLUME, REL_VOLUME) based on column mappings.
    These are not TA indicators but derived directly from raw OHLCV data.
    """
    label = interval.upper()
    output = {}

    for name, meta in PASSTHROUGH_REGISTRY.items():
        source_col = meta["source"]
        base_col_name = f"{name}_{label}"

        if source_col not in df.columns:
            print(f"Skipping {name} — missing column: {source_col}")
            continue

        series = df[source_col]
        output[base_col_name] = series

        if meta.get("with_avg"):
            output[f"{base_col_name}_Avg"] = series.rolling(5).mean()

        if meta.get("with_slope"):
            output[f"{base_col_name}_Slope"] = series.diff()

    # Special case: REL_VOLUME depends on VOLUME and VOLUME_Avg
    vol_col = f"VOLUME_{label}"
    vol_avg_col = f"{vol_col}_Avg"
    relvol_col = f"REL_VOLUME_{label}"
    if vol_col in output and vol_avg_col in output:
        output[relvol_col] = output[vol_col] / output[vol_avg_col]

    return pd.DataFrame(output)
