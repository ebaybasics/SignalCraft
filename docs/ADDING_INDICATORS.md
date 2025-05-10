# 🛠️ How to Add New Technical Indicators – SignalCraft

This guide explains how to add new indicators (like MACD, Bollinger Bands, etc.) to SignalCraft in a clean, modular way.

---

## 1. Edit `compute_indicators()`
**File:** `indicators/compute_indicators.py`

This function handles all indicator calculations. Add your new indicator logic here.

### ➕ Add your indicator calculation

Example for Bollinger Bands:
```python
bb = ta.bbands(df['Close'], length=20, std=2)
df["BB_Lower"] = bb["BBL_20_2.0"]
df["BB_Upper"] = bb["BBU_20_2.0"]
```

Example for MACD:
```python
macd = ta.macd(df['Close'])
df["MACD"] = macd["MACD_12_26_9"]
df["MACD_HISTO"] = macd["MACDh_12_26_9"]
```

### 🧼 Add new columns to the return:
Make sure to return the new indicator columns so they're included downstream:
```python
return df[[cmf_col, rsi_col, "BB_Lower", "BB_Upper", "MACD", "MACD_HISTO"]]
```

---

## 2. Edit `build_snapshot_with_indicators()`
**Also in:** `indicators/compute_indicators.py`

This function pulls the latest value for each indicator after it’s computed.

### 📦 Extract the last value for each new indicator:
```python
bb_lower = df["BB_Lower"].dropna().iloc[-1] if not df["BB_Lower"].dropna().empty else None
bb_upper = df["BB_Upper"].dropna().iloc[-1] if not df["BB_Upper"].dropna().empty else None
macd_val  = df["MACD"].dropna().iloc[-1] if not df["MACD"].dropna().empty else None
```

### 🔁 Add the new values to the results dictionary:
```python
results.append({
    "Ticker": ticker,
    cmf_label: cmf,
    rsi_label: rsi,
    "BB_Lower": bb_lower,
    "BB_Upper": bb_upper,
    "MACD": macd_val
})
```

---

## 3. Test It

Run the system:
```bash
python main.py
```

Then inspect `data/marketData.csv` to confirm that your new indicator values appear in the table.

---

## ✅ Optional: Add Toggles in `config.py`

To easily enable or disable indicators, use flags:
```python
ENABLED_INDICATORS = ["CMF", "RSI", "BBANDS", "MACD"]
```

Then wrap your indicator logic like:
```python
if "MACD" in ENABLED_INDICATORS:
    macd = ta.macd(df['Close'])
    df["MACD"] = macd["MACD_12_26_9"]
```

---

## 🔁 Summary

- All new indicators go into `compute_indicators()`
- Their final values get picked out in `build_snapshot_with_indicators()`
- You can toggle them in `config.py` if desired
- Final results show up in `marketData.csv`

---

Welcome to the craft.
