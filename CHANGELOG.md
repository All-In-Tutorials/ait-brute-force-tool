# 📌 CHANGELOG

## [Unreleased]

### 🆕 Added
- CLI arguments support for custom login URLs (`--login_url`, `--wrong_url`).
- Dynamic credential loading for portability.
- `generator.py` file for dictionary file creation.
- `.gitignore` to exclude the Dictionary directory.
- Documentation updates in `README.md` (Usage & Requirements section).
- Option-based selection mechanism in `main.py` for better flexibility.

### 🛠️ Changed
- Renamed directory in `generator.py` to maintain uniformity.
- Refactored `main.py` to load generated directories for username and password.

### 🐛 Fixed
- Improved logging: Replaced `print()` with `logging.info()` for better debugging.
- Exception handling: Added `TimeoutException`, `NoSuchElementException`, and generic error handling for robustness.
- Optimized delays: Replaced `time.sleep()` with `wait.until(...)` for better performance.
- Wrong login page handling: Added detection to prevent unnecessary reloads.
