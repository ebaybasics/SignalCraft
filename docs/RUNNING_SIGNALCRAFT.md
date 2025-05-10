# ▶️ How to Run SignalCraft

This guide explains how to install dependencies and run your market data engine.

---

## 1. Setup & Install Dependencies

From your root project directory, install required packages:

```bash
pip install yfinance pandas pandas_ta matplotlib
```

---

## 2. Folder Structure Overview

```
signalcraft/
├── main.py
├── config.py
├── data/
├── indicators/
│   ├── __init__.py
│   ├── fetch_data.py
│   └── compute_indicators.py
├── analysis/
│   ├── __init__.py
│   └── summary.py
├── docs/
│   └── RUNNING_SIGNALCRAFT.md
│   └── ADDING_INDICATORS.md
```

---

## 3. Run the Script

```bash
python main.py
```

You should see:

```
📈 Building indicator snapshots...
🧠 Summarizing top and bottom ETFs by CMF & RSI...
✅ Saved to data/marketData.csv
```

---

## 4. Output

- CSV file: `data/marketData.csv`
- Format:

```csv
Timeframe,Top_ETFs,Bottom_ETFs,RSI_Top,RSI_Bottom
5M,"['XLK', 'SMH', ...]","['XLC', 'XLP', ...]",...
...
```

---

## 5. Troubleshooting

- Ensure you have an internet connection
- Python version should be 3.9+ recommended
- If data appears missing, increase lookback period in `config.py`

---

Happy SignalCrafting 📊
