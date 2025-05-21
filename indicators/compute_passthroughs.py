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
    
    # First, normalize column names by checking for case-insensitive matches
    column_map = {}
    df_columns_lower = [col.lower() for col in df.columns]
    
    for expected_col in ['open', 'high', 'low', 'close', 'volume']:
        # Try exact match first
        if expected_col in df.columns:
            column_map[expected_col] = expected_col
        # Try case-insensitive match
        elif expected_col in df_columns_lower:
            idx = df_columns_lower.index(expected_col)
            actual_col = df.columns[idx]
            column_map[expected_col] = actual_col
        # Try capitalized version
        elif expected_col.capitalize() in df.columns:
            column_map[expected_col] = expected_col.capitalize()
        # Try uppercase version
        elif expected_col.upper() in df.columns:
            column_map[expected_col] = expected_col.upper()
    
    print(f"Column mapping: {column_map}")

    for name, meta in PASSTHROUGH_REGISTRY.items():
        source_col = meta["source"]
        base_col_name = f"{name}_{label}"
        
        # Skip PCT_GAIN here - we'll handle it separately
        if name == "PCT_GAIN":
            continue
        
        # Try to find the actual column name using our mapping
        actual_source_col = column_map.get(source_col.lower(), source_col)
            
        if actual_source_col not in df.columns:
            print(f"Skipping {name} — missing column: {source_col} (tried {actual_source_col})")
            continue

        series = df[actual_source_col]
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

    # Special case: PCT_GAIN - requires both open and close columns
    pct_gain_col = f"PCT_GAIN_{label}"
    
    # Get actual column names from our mapping
    open_col = column_map.get('open')
    close_col = column_map.get('close')
    
    # Check if both required columns exist
    if open_col and close_col and open_col in df.columns and close_col in df.columns:
        # Calculate percentage gain
        output[pct_gain_col] = ((df[close_col] - df[open_col]) / df[open_col]) * 100
        
        # Add moving average if configured
        if PASSTHROUGH_REGISTRY.get("PCT_GAIN", {}).get("with_avg", False):
            output[f"{pct_gain_col}_Avg"] = output[pct_gain_col].rolling(5).mean()
    else:
        print(f"Cannot calculate {pct_gain_col} - missing 'open' or 'close' columns")
        print(f"Available columns: {', '.join(df.columns)}")

    return pd.DataFrame(output)
