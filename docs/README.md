# 📊 SignalCraft

**SignalCraft** is a modular Python-based market analysis toolkit that blends technical indicators, macroeconomic context, and sector rotation logic to create actionable insights. Designed to help you see the market clearly, it functions as a personal market lens with potential to scale into a full research and advisory tool.

---

## 🔍 Features

- Fetch and analyze ETF data across multiple timeframes
- Compute key indicators like CMF, RSI, MACD, OBV — and passthroughs like Volume and Relative Volume
- Modular structure: easily extend with your own logic
- Summarize top/bottom ETFs by money flow and momentum
- Fully configurable via `config.py`
- Clean output saved as `marketData.csv` for use in GPT prompts or dashboards
- Plug-and-play data layer: swap out yFinance with another API easily

---

## 🗂 Folder Structure
```
```markdown
# 📊 SignalCraft

**SignalCraft** is a modular Python-based market analysis toolkit that blends technical indicators, macroeconomic context, and sector rotation logic to create actionable insights. Designed to help you see the market clearly, it functions as a personal market lens with potential to scale into a full research and advisory tool.

---

## 🔍 Features

- Fetch and analyze ETF data across multiple timeframes
- Compute key indicators like CMF, RSI, MACD, OBV — and passthroughs like Volume and Relative Volume
- Modular structure: easily extend with your own logic
- Summarize top/bottom ETFs by money flow and momentum
- Fully configurable via `config.py`
- Clean output saved as `marketData.csv` for use in GPT prompts or dashboards
- Plug-and-play data layer: swap out yFinance with another API easily

---

## 🗂 Folder Structure

```
signalcraft/
├── main.py                          # Main runner script
├── config/                          # Configuration files
│   ├── __init__.py                  # Settings and registry definitions
│   └── credentials.py               # API keys and sensitive information
├── indicators/                      # Core market logic
│   ├── build_snapshots.py           # Unified snapshot builder
│   ├── compute_indicators.py        # Pure TA indicator computation (pandas_ta)
│   ├── compute_passthroughs.py      # Handles VOLUME, REL_VOLUME, and raw signals
│   ├── enhance_indicators.py        # Applies z-score, trend, smoothing, etc.
│   ├── post_indicator_proccessing_functions.py  # Enhancement functions
│   └── fetch_data.py                # OHLCV data downloading (yFinance by default)
├── analysis/                        # Summary and ranking logic
│   └── summary.py                   # Summarizes indicators and creates rankings
├── chatgpt/                         # AI integration components
│   ├── client.py                    # OpenAI API client functions
│   └── prompts.py                   # System prompts for different analysis types
├── stockrover/                      # StockRover integration
│   └── extract_tickers.py           # PDF extraction utilities
├── data/                            # Output files (CSV)
│   ├── marketData/                  # Market snapshots and indicators
│   ├── priceVolume/                 # Raw OHLCV data for individual tickers
│   └── narrations/                  # AI-generated market analyses
├── docs/                            # Documentation and usage guides
└── run_narration_test.py            # Script for generating AI market analyses
```

---

## 🚀 Getting Started

To set up SignalCraft with the correct Python version and all required packages, use the included `bootstrap.sh` script.

### 📦 Install Prerequisites (Once)

> Make sure the following are installed on your system:

```bash
sudo pacman -S --needed git base-devel openssl zlib xz tk readline libffi
```

Then install [`pyenv`](https://github.com/pyenv/pyenv):

```bash
curl https://pyenv.run | bash
```

Add this to your shell config (`~/.bashrc`, `~/.zshrc`, etc.):

```bash
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv init -)"
```

Apply it:

```bash
exec "$SHELL"
```

---

### 🚀 Bootstrap the Project

```bash
./bootstrap.sh
```

This will:

- Install Python 3.11.9 (if needed)
- Create a .venv
- Install `numpy==1.24.4`, `scipy`, `yfinance`, `pandas_ta`, and dependencies
- Pin everything in requirements.txt

---

### 🧪 Run the System

1. Activate the environment:
```bash
source .venv/bin/activate
```

2. Run the script:
```bash
python main.py
```

3. Outputs:
- `data/marketData/*.csv` — indicator snapshots
- indicatorSummary.csv — top/bottom ETFs by indicator

---

## 📊 Advanced Usage

SignalCraft offers extensive customization through command-line arguments. Here's how to leverage these options for different scenarios:

### 🎯 Using Different Ticker Sets

By default, SignalCraft uses the tickers defined in __init__.py, but you can override these:

```bash
# Analyze only major index ETFs
python main.py -t SPY QQQ IWM

# Focus on tech sector
python main.py -t AAPL MSFT GOOG AMZN NVDA AMD INTC

# Analyze sectors with select stocks
python main.py -t XLF XLE XLK XLV JPM BAC C CVX XOM AAPL MSFT
```

### ⏱️ Working with Different Timeframes

Analyze specific timeframes to focus your analysis:

```bash
# Daily analysis only (faster execution)
python main.py -tf 1d

# Intraday analysis
python main.py -tf 5m 1h

# Long-term analysis
python main.py -tf 1d 1wk 1mo

# Combine with custom tickers
python main.py -t SPY QQQ IWM -tf 1d 1wk
```

### 📂 Custom Output Directories

Store results in a specific location:

```bash
# Output to custom directory
python main.py -o ./analysis_results

# Date-specific output
python main.py -o ./analysis_$(date +%Y%m%d)
```

### 🤖 AI Market Analysis

Use run_narration_test.py to generate AI-powered market analysis from your indicator data:

```bash
# Basic market analysis with default settings
python run_narration_test.py

# Save the narration to a specific file
python run_narration_test.py -o reports/daily_brief.txt

# Generate analysis without saving to file
python run_narration_test.py --no-save
```

### 🧠 Using Different AI Models

SignalCraft supports different AI models for market analysis:

```bash
# Use GPT-4o for higher quality analysis
python run_narration_test.py -m gpt-4o

# Use Claude model
python run_narration_test.py -m claude-3-sonnet-20240229

# Use smaller o3-mini model (faster)
python run_narration_test.py -m o3-mini

# Adjust temperature (creativity) of the model
python run_narration_test.py -m gpt-4o --temp 0.8
```

### 📝 Different Analysis Templates

Switch between different analysis prompt templates:

```bash
# Market-wide analysis (default)
python run_narration_test.py -p market

# Ticker-focused analysis for identifying trade candidates
python run_narration_test.py -p ticker

# Sector rotation analysis for identifying best sectors to trade
python run_narration_test.py -p sector

# Sector analysis with GPT-4o for higher quality analysis
python run_narration_test.py -p sector -m gpt-4o
```

### 🔄 Combining Options for Specific Scenarios

#### Daily Morning Briefing
```bash
# Generate a morning brief with major indices, daily timeframe only
python main.py -t SPY QQQ IWM -tf 1d
python run_narration_test.py -m gpt-4o -p market -o reports/morning_brief.txt
```

#### Sector Rotation Analysis
```bash
# Analyze sector ETFs across multiple timeframes
python main.py -t XLF XLE XLK XLV XLI XLU XLY XLP -tf 1d 1wk
python run_narration_test.py -m gpt-4o -t 1D 1WK -o reports/sector_rotation.txt
```

#### Focused Stock Watchlist
```bash
# Generate watchlist for specific stocks
python main.py -t AAPL MSFT GOOG AMZN META NVDA AMD INTC TSLA
python run_narration_test.py -p ticker -m gpt-4o -o watchlist.txt
```

#### Real-Time Market Update
```bash
# Quick intraday update of major indices
python main.py -t SPY QQQ IWM -tf 5m 1h
python run_narration_test.py -t 5M 1H --no-save
```

---

## 🔄 Swappable Data Sources

The snapshot builder in build_snapshots.py accepts a custom `fetch_function`.  
This allows you to replace `yfinance` with any API or internal source — no need to modify your core analysis logic.  
The default fetch function is defined in fetch_data.py.

---

## 🛠 Add Indicators

Want to add MACD, BBANDS, or others?  
See: ADDING_INDICATORS.md

---

## 🧠 Project Philosophy

This isn't just a tool. It's a craft.  
SignalCraft is designed to:
- Be human-readable and extensible
- Help you develop intuition through data
- Balance structure with flexibility

---

## 📬 Coming Soon

- Headline sentiment parser
- GPT-integrated strategy recommender
- Interactive dashboard
- API-fed economic indicators

---

Built for clarity. Built for curiosity.  
**Welcome to the craft.**


---

## 🚀 Getting Started

To set up SignalCraft with the correct Python version and all required packages, use the included `bootstrap.sh` script.

### 📦 Install Prerequisites (Once)

> Make sure the following are installed on your system:

```bash
sudo pacman -S --needed git base-devel openssl zlib xz tk readline libffi
```

Then install [`pyenv`](https://github.com/pyenv/pyenv):

```bash
curl https://pyenv.run | bash
```

Add this to your shell config (`~/.bashrc`, `~/.zshrc`, etc.):

```bash
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv init -)"
```

Apply it:

```bash
exec "$SHELL"
```

---

### 🚀 Bootstrap the Project

```bash
./bootstrap.sh
```

This will:

- Install Python 3.11.9 (if needed)
- Create a `.venv/`
- Install `numpy==1.24.4`, `scipy`, `yfinance`, `pandas_ta`, and dependencies
- Pin everything in `requirements.txt`

---

### 🧪 Run the System

1. Activate the environment:
```bash
source .venv/bin/activate
```

2. Run the script:
```bash
python main.py
```

3. Outputs:
- `data/marketData/*.csv` — indicator snapshots
- `data/indicatorSummary.csv` — top/bottom ETFs by indicator

---

## 🔄 Swappable Data Sources

The snapshot builder in `build_snapshots.py` accepts a custom `fetch_function`.  
This allows you to replace `yfinance` with any API or internal source — no need to modify your core analysis logic.  
The default fetch function is defined in `indicators/fetch_data.py`.

---

## 🛠 Add Indicators

Want to add MACD, BBANDS, or others?  
See: [ADDING_INDICATORS.md](docs/ADDING_INDICATORS.md)

---

## 🧠 Project Philosophy

This isn’t just a tool. It’s a craft.  
SignalCraft is designed to:
- Be human-readable and extensible
- Help you develop intuition through data
- Balance structure with flexibility

---

## 📬 Coming Soon

- Headline sentiment parser
- GPT-integrated strategy recommender
- Interactive dashboard
- API-fed economic indicators

---

Built for clarity. Built for curiosity.  
**Welcome to the craft.**
