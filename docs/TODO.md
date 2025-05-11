# ✅ SignalCraft TODO List

This is the running checklist for building modularity, scalability, and flexibility into the SignalCraft engine.

---

## 🔁 Indicators

- [x ] Create an indicator registry in `config.py`
  - Format should include: name, function path, required columns, parameters
- [ x] Refactor `compute_indicators()` to loop through registry
  - Dynamically compute only enabled indicators
  - Automatically build result columns list

---

## 📊 Summary Engine

- [x ] Move indicator names used in summary to `config.py`
  - `SUMMARY_INDICATORS = ["CMF", "RSI", "MACD"]`
- [x ] Refactor `summarize_top_bottom_cmf()` to loop through indicators
  - Use the registry to find column names
  - Avoid hardcoding “CMF_1D”, etc.

---

## 🕐 Timeframes

- [ ] Move timeframe list to `config.py`
  - `ROTATION_TIMEFRAMES = ["5m", "1h", "1d", "1wk", "1mo"]`
- [ ] Refactor `main.py` to loop over timeframes dynamically

---

## 💾 Output Layer

- [ ] Create `output_writer.py` in a new `utils/` folder
  - Add `write_output(df, format="csv", path="...")`
- [ ] Optional: Add placeholder for `format="notion"` or `format="gpt"`

---

## 📡 Data Layer

- [ ] Create `fetch_data()` abstraction in `indicators/fetch_data.py`
  - Handles logic for yfinance or future data sources
- [ ] Replace `yfinance.download(...)` calls with this wrapper throughout

---

## 🧠 Strategy Logic (Optional)

- [ ] Create `strategies/` folder
  - Add simple `rotation_contrarian.py` with dummy logic
- [ ] Define interface: `generate_trade_ideas(df) -> list of ideas`

---

## 📁 Documentation Updates

- [ ] Update `README.md` to reflect new modular structure
- [ ] Add new doc: `docs/INDICATOR_REGISTRY.md` for format and usage

---

Let this grow with the project. Each part you modularize now makes future SignalCraft iterations simpler, cleaner, and more powerful.
