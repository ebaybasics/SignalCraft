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
├── config.py                   # Settings and constants
├── data/                       # Output files (CSV)
├── indicators/                 # Indicator logic (fetch + compute)
├── analysis/                   # Summary and ranking logic
├── docs/                       # Documentation and usage guides
│   ├── ADDING_INDICATORS.md
│   └── RUNNING_SIGNALCRAFT.md
```

---

## 🚀 Getting Started

See [RUNNING_SIGNALCRAFT.md](docs/RUNNING_SIGNALCRAFT.md) for full instructions.

1. Install dependencies:
```bash
pip install yfinance pandas pandas_ta matplotlib
```

2. Run the script:
```bash
python main.py
```

3. Output: `data/marketData.csv` containing snapshot of ETF flows

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
