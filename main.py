#!/usr/bin/env python3
"""
SignalCraft - Market Analysis and Indicator Processing Pipeline
"""

import pandas as pd
import os
import argparse
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional

# Import configuration
from config.config import tickers as default_tickers, SR_tickers, BASE_FEATURES
from indicators.fetch_data import fetch_ticker_data
from indicators.post_indicator_proccessing_functions import add_sumZZ, true_trend
from analysis.summary import summarize_top_bottom_indicators
from indicators.enhance_indicators import apply_derived_features
from indicators.compute_passthroughs import compute_passthroughs
from indicators.build_snapshots import build_full_snapshot
from stockrover.extract_tickers import extract_tickers_from_pdf

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ==== CONSTANTS ====
TIMEFRAMES = ["5m", "1h", "1d", "1wk", "1mo"]
TIMEFRAMES_UPPER = [tf.upper() for tf in TIMEFRAMES]
DATA_DIR = Path("data")
MARKET_DATA_DIR = DATA_DIR / "marketData"
PRICE_VOLUME_DIR = DATA_DIR / "priceVolume"
STOCKROVER_PDF_DIR = Path("stockrover/stockrover_downloads")
STOCKROVER_PDF = STOCKROVER_PDF_DIR / "Stock Rover Table.pdf"

# Mapping for trend windows
TREND_WINDOWS = {
    "1H": 24,   # one trading session of hourly bars
    "1D": 14,   # ~ three weeks of daily bars
    "1WK": 12,  # ~ three months of weekly bars
    "1MO": 6,   # ~ half-year of monthly bars
    "5M": 48,   # ~ one trading day of 5-minute bars
}

def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='SignalCraft Market Analysis Pipeline')
    
    parser.add_argument(
        '--tickers', '-t',
        type=str,
        nargs='+',
        help='Override tickers list (e.g., -t AAPL MSFT GOOG)'
    )
    
    parser.add_argument(
        '--timeframes', '-tf',
        type=str,
        nargs='+',
        default=TIMEFRAMES,
        help=f'Timeframes to analyze (default: {" ".join(TIMEFRAMES)})'
    )
    
    parser.add_argument(
        '--output-dir', '-o',
        type=str,
        default=str(DATA_DIR),
        help=f'Output directory for data files (default: {DATA_DIR})'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    
    return parser.parse_args()

def setup_directories(data_dir: Path = DATA_DIR) -> None:
    """Create necessary directories if they don't exist"""
    market_dir = data_dir / "marketData"
    price_dir = data_dir / "priceVolume"
    
    for directory in [data_dir, market_dir, price_dir]:
        directory.mkdir(parents=True, exist_ok=True)
        logger.info(f"Ensured directory exists: {directory}")

def get_tickers(cli_tickers: Optional[List[str]] = None) -> List[str]:
    """
    Get tickers based on priority:
    1. Command-line arguments (if provided)
    2. StockRover PDF (if exists)
    3. Default tickers from config
    """
    if cli_tickers:
        logger.info(f"Using {len(cli_tickers)} tickers from command line: {', '.join(cli_tickers[:5])}...")
        return cli_tickers
    elif STOCKROVER_PDF.exists():
        logger.info(f"Using tickers extracted from: {STOCKROVER_PDF}")
        return extract_tickers_from_pdf(STOCKROVER_PDF)
    else:
        logger.info(f"Using {len(default_tickers)} default tickers from config")
        return default_tickers

def enhance_snapshot(df: pd.DataFrame, label: str) -> pd.DataFrame:
    """Apply post-processing to a snapshot dataframe"""
    try:
        # Apply derived features
        df = apply_derived_features(df, label)
        
        # Add sumZZ
        df = add_sumZZ(df, label)
        
        # Calculate trend slope
        sum_col = f"sumZZ_{label}"
        slope_col = f"slope_sumZZ_{label}"
        win = TREND_WINDOWS.get(label, 20)
        
        df[slope_col] = (
            df[sum_col]
            .rolling(win)
            .apply(lambda s: true_trend(s, window=win), raw=False)
        )
        
        return df
    except Exception as e:
        logger.error(f"Error enhancing snapshot {label}: {str(e)}")
        return df

def add_passthroughs(snapshots: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
    """Add passthrough columns to each snapshot"""
    enhanced_snapshots = {}
    
    for label, df in snapshots.items():
        try:
            passthrough_df = compute_passthroughs(df, label)
            enhanced_snapshots[label] = pd.concat([df, passthrough_df], axis=1)
            logger.info(f"Added passthroughs to {label} snapshot")
        except Exception as e:
            logger.error(f"Error applying passthroughs to {label}: {str(e)}")
            enhanced_snapshots[label] = df
            
    return enhanced_snapshots

def save_snapshots(snapshots: Dict[str, pd.DataFrame], output_dir: Path = MARKET_DATA_DIR) -> None:
    """Save all snapshot dataframes to CSV files"""
    for label, df in snapshots.items():
        file_path = output_dir / f"marketData_{label}.csv"
        df.to_csv(file_path, index=False)
        logger.info(f"Saved {label} snapshot to {file_path}")

def save_ticker_ohlcv(ticker_list: List[str], timeframes: List[str], output_dir: Path = PRICE_VOLUME_DIR) -> None:
    """Save OHLCV data for each ticker and timeframe"""
    for ticker in ticker_list:
        for tf in timeframes:
            try:
                df = fetch_ticker_data(ticker, interval=tf, years=1)
                if not df.empty:
                    filepath = output_dir / f"{ticker}_{tf.upper()}.csv"
                    df.to_csv(filepath)
                    logger.info(f"Saved: {filepath}")
                else:
                    logger.warning(f"No data for {ticker} {tf}")
            except Exception as e:
                logger.error(f"Error fetching {ticker} {tf}: {str(e)}")

def save_good_enough_columns(snapshots: Dict[str, pd.DataFrame], output_dir: Path = MARKET_DATA_DIR) -> None:
    """Save 'good enough' columns for LLM consumption"""
    good_enough_cols = BASE_FEATURES + ["Date", "Time"]
    
    for label, df in snapshots.items():
        keep_cols = ["Date", "Time", "Ticker", "Timeframe"]
        
        # Add columns with label suffix
        for col in good_enough_cols:
            if col in ["Ticker", "Timeframe", "CMF", "Date", "Time"]:
                # already added or non-suffix columns we always keep
                continue
            else:
                col_with_label = f"{col}_{label}"
                if col_with_label in df.columns:
                    keep_cols.append(col_with_label)
                else:
                    logger.warning(f"{col_with_label} missing in {label}")

        # Filter to existing columns only
        filtered_cols = [c for c in keep_cols if c in df.columns]
        good_df = df[filtered_cols].copy()

        # Save output
        out_path = output_dir / f"goodEnough_{label}.csv"
        good_df.to_csv(out_path, index=False)
        logger.info(f"Saved {label} good-enough CSV → {out_path}")

def main() -> None:
    """Main execution pipeline"""
    # Parse command line arguments
    args = parse_arguments()
    
    # Set logging level based on verbosity
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Setup directories
    data_dir = Path(args.output_dir)
    market_dir = data_dir / "marketData"
    price_dir = data_dir / "priceVolume"
    setup_directories(data_dir)
    
    # Get tickers (with priority: CLI args > PDF > config defaults)
    analysis_tickers = get_tickers(args.tickers)
    
    # Convert timeframes to lowercase for consistency
    timeframes = [tf.lower() for tf in args.timeframes]
    
    # Build initial snapshots
    logger.info(f"Building market snapshots for {len(analysis_tickers)} tickers across {len(timeframes)} timeframes...")
    snapshots = build_full_snapshot(analysis_tickers, timeframes, fetch_ticker_data)
    
    # Add passthrough columns
    logger.info("Adding passthroughs...")
    snapshots = add_passthroughs(snapshots)
    
    # Enhance snapshots with derived features
    logger.info("Enhancing snapshots with derived features...")
    for label, df in snapshots.items():
        snapshots[label] = enhance_snapshot(df, label)
    
    # Generate summary
    logger.info("Summarizing top and bottom ETFs by active indicators...")
    summary_df = summarize_top_bottom_indicators(snapshots)
    summary_df.to_csv(data_dir / "indicatorSummary.csv", index=False)
    logger.info("Saved summary rankings to data/indicatorSummary.csv")
    
    # Save snapshots
    logger.info("Saving snapshot files...")
    save_snapshots(snapshots, market_dir)
    
    # Save ticker OHLCV data
    logger.info("Saving individual ticker OHLCV data...")
    save_ticker_ohlcv(SR_tickers, timeframes, price_dir)
    
    # Save good enough columns for LLM
    logger.info("Saving LLM-friendly dataframes...")
    save_good_enough_columns(snapshots, market_dir)
    
    logger.info("✅ SignalCraft processing pipeline complete!")

if __name__ == "__main__":
    main()

# =====================================================
# USAGE EXAMPLES:
# =====================================================
#
# 1. Basic usage with default settings:
#    python main.py
#
# 2. Override tickers with a custom list:
#    python main.py -t SPY QQQ IWM AAPL MSFT
#
# 3. Analyze only specific timeframes:
#    python main.py -tf 1d 1wk
#    
# 4. Use small set of tickers with specific timeframes:
#    python main.py -t SPY QQQ IWM -tf 1d 1wk
#
# 5. Output to a custom directory:
#    python main.py -o /path/to/custom/data/dir
#
# 6. Enable verbose logging:
#    python main.py -v
#
# 7. Combine multiple options:
#    python main.py -t AAPL MSFT GOOG -tf 1d 1wk 1mo -o ./custom_data -v
#
# 8. Quick analysis of major ETFs (daily only):
#    python main.py -t SPY QQQ IWM XLF XLE XLK XLV -tf 1d
#
# 9. Focus on tech sector with fine-grained timeframes:
#    python main.py -t AAPL MSFT GOOG AMZN META NVDA AMD -tf 5m 1h 1d
# =====================================================

