# 📌 CHANGELOG

## 🔥 Latest Improvements

### ✅ Better Logging
- Uses `logging.info()` instead of `print()`, making debugging easier.

### ✅ More Reliable Exception Handling
- Catches `TimeoutException`, `NoSuchElementException`, and generic errors for robustness.

### ✅ No Unnecessary Sleep Delays
- Uses `wait.until(...)` instead of `time.sleep()` for efficient execution.

### ✅ Handles Wrong Login Page More Efficiently
- Detects and avoids unnecessary page reloads when redirected to the wrong login page.

### ✅ CLI Arguments for Automation

- Run the tool with custom login URLs:
  
  ```sh
  python main.py --login_url "http://example.com/login" --wrong_url "http://example.com/fail"
  ```