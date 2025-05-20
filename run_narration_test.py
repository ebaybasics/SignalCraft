#!/usr/bin/env python3
"""
Test runner for SignalCraft narration functionality
"""

import argparse
import pandas as pd
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

from chatgpt.client import get_narration, DEFAULT_CONFIG

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Default data paths
DATA_DIR = Path("data/marketData")
OUTPUT_DIR = Path("data/narrations")

# === Load and combine market snapshot data ===
def load_market_data(timeframes=None):
    """Load market data for specified timeframes"""
    if timeframes is None:
        timeframes = ["5M", "1H", "1D"]
    
    data = {}
    
    # Always load summary data
    try:
        data["Indicator Summary"] = pd.read_csv("data/indicatorSummary.csv")
    except FileNotFoundError:
        logger.error("Could not find indicator summary file")
        raise
    
    # Load requested timeframes
    for tf in timeframes:
        try:
            data[tf] = pd.read_csv(DATA_DIR / f"goodEnough_{tf}.csv")
            logger.info(f"Loaded {tf} data")
        except FileNotFoundError:
            logger.warning(f"Could not load {tf} data, skipping")
    
    return data

# === Format each timeframe's data ===
def format_snapshot(df: pd.DataFrame, timeframe: str) -> str:
    """Format a dataframe for API consumption"""
    header = f"\n\n{'=' * 8} {timeframe.upper()} {'=' * 8}\n"
    text = df.to_csv(index=False)
    return header + text

# === Compose full input message for GPT ===
def build_input_message(data: dict, ordered_keys=None) -> str:
    """Build a formatted input message from multiple dataframes"""
    if ordered_keys is None:
        ordered_keys = ["Indicator Summary", "5M", "1H", "1D"]
    
    return "\n".join([format_snapshot(data[tf], tf) 
                      for tf in ordered_keys if tf in data])

def save_narration(narration: str, output_file: str = None) -> None:
    """Save narration to file"""
    if output_file is None:
        # Create output directory if it doesn't exist
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = OUTPUT_DIR / f"narration_{timestamp}.txt"
    
    with open(output_file, 'w') as f:
        f.write(narration)
    logger.info(f"Saved narration to {output_file}")

# === Run narration ===
def main():
    """Main entry point"""
    # Add command-line arguments
    parser = argparse.ArgumentParser(description='Generate market narration')
    parser.add_argument('-t', '--timeframes', nargs='+', default=["5M", "1H", "1D"],
                       help='Timeframes to include (default: 5M 1H 1D)')
    parser.add_argument('-m', '--model', default=DEFAULT_CONFIG["model"],
                       help=f'OpenAI model to use (default: {DEFAULT_CONFIG["model"]})')
    parser.add_argument('--temp', type=float, default=DEFAULT_CONFIG["temperature"],
                       help=f'Temperature parameter (default: {DEFAULT_CONFIG["temperature"]})')
    parser.add_argument('-o', '--output', help='Output file path')
    parser.add_argument('--no-save', action='store_true', help='Don\'t save output to file')
    parser.add_argument(
        '--prompt-type', '-p',
        type=str,
        default="market",
        choices=["market", "ticker", "sector"],
        help='Type of prompt to use (market, ticker, or sector)'
    )
    
    args = parser.parse_args()
    
    # Load and process data
    data = load_market_data(args.timeframes)
    input_text = build_input_message(data)
    
    # Generate narration
    logger.info(f"Generating narration using model {args.model}")
    narration = get_narration(
        csv_blob=input_text,
        model=args.model,
        temperature=args.temp,
        prompt_type=args.prompt_type
    )
    
    # Handle both string and error dict responses
    if isinstance(narration, dict) and 'error' in narration:
        logger.error(f"Narration failed: {narration['error']}")
        return 1
    
    # Print narration
    print("\n📈 SignalCraft Narration:\n")
    print(narration)
    
    # Save narration if requested
    if not args.no_save:
        save_narration(narration, args.output)
    
    return 0

if __name__ == "__main__":
    main()

# =====================================================
# EXAMPLE USAGE WITH DIFFERENT PROMPTS:
# =====================================================
# 
# # Default market analysis prompt (ANALYST_PROMPT)
# python run_narration_test.py
# 
# # Use ticker-focused analysis (TICKER_ANALYST_PROMPT)
# python run_narration_test.py -p ticker
# 
# # Combine with other options
# python run_narration_test.py -p ticker -m gpt-4o -t 1D
#
# # Ticker analysis with custom model and temperature
# python run_narration_test.py -p ticker -m claude-3-opus -t 1D 1WK --temp 0.8
# =====================================================
