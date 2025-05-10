# 📜 Changelog

All notable changes to this project will be documented in this file.

---

## [v0.2.0] - YYYY-MM-DD
### Added
- Modular indicator engine using `INDICATOR_REGISTRY`
- Dynamic indicator summary with `SUMMARY_INDICATORS`
- Snapshot generation across 5M, 1H, 1D, 1WK, 1MO timeframes
- Output folder structure: individual CSVs in `data/marketData/`
- Debug prints showing indicator computation and latest value
- Clean summary outputs ranked by CMF and RSI

### Changed
- `main.py` refactored to loop snapshots dynamically
- `summary.py` rebuilt to support indicator-based ranking

### Removed
- Hardcoded CMF/RSI logic from `summary.py`
