# 📊 SignalCraft

**SignalCraft** is a modular Python-based market analysis toolkit that blends technical indicators, macroeconomic context, and sector rotation logic to create actionable insights. Designed to help you see the market clearly, it functions as a personal market lens with potential to scale into a full research and advisory tool.

---

## 🔍 Features

- Fetch and analyze ETF data across multiple timeframes
- Compute key indicators like CMF and RSI (more coming: MACD, BBANDS, etc.)
- Modular structure: easily extend with your own logic
- Summarize top/bottom ETFs by money flow and momentum
- Fully configurable via `config.py`
- Clean output saved as `marketData.csv` for use in GPT prompts or dashboards

---

## 🗂 Folder Structure

```
signalcraft/
├── main.py                     # Main runner script
├── config.py                   # Settings and registry definitions
├── data/                       # Output files (CSV)
├── indicators/                 # Core market logic
│   ├── compute_indicators.py           # Pure TA indicator computation (pandas_ta)
│   ├── compute_passthroughs.py         # Handles VOLUME, REL_VOLUME, and raw source signals
│   ├── enhance_indicators.py           # Applies z-score, trend, smoothing, etc.
│   ├── post_indicator_proccessing_functions.py  # Raw enhancement function definitions
│   ├── fetch_data.py                   # OHLCV data downloading
├── analysis/                  # Summary and ranking logic
│   └── summary.py
├── docs/                      # Documentation and usage guides
│   ├── ADDING_INDICATORS.md
│   └── RUNNING_SIGNALCRAFT.md
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
