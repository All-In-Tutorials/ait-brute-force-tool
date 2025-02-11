## 📌 Introduction

**AIT Brute Force Tool** is an open-source Python-based tool designed for security testing and password auditing.  
It automates brute-force attacks using **ChromeDriver**, making it useful for penetration testing and cybersecurity research.  

⚠️ **Disclaimer:** This tool is intended for **educational and security research purposes only**.  
Unauthorized use against systems you do not own is **illegal**. Proceed responsibly.  

---

## 🛠️ Requirements

### 1️⃣ ChromeDriver  
ChromeDriver is required for browser automation. Download the appropriate version based on your Chrome browser:  

- **Version 133 and later:** [Download here](https://googlechromelabs.github.io/chrome-for-testing/)  
- **Version 114 and earlier:** [Download here](https://sites.google.com/chromium.org/driver/downloads)  

📌 **Tip:** Ensure ChromeDriver is accessible in your system **PATH**.  

### 2️⃣ Python  
Install the latest **stable version** of Python:  

- 📥 [Download Python](https://www.python.org/downloads/)  

Verify installation with:

```sh
python --version
```
or

```sh
python3 --version
```

### 3️⃣ Selenium  
This tool relies on **Selenium** for browser automation. Install it via pip:  

```sh
pip install selenium
```

Verify installation with:

```sh
python -c "import selenium; print(selenium.__version__)"
```

---

## 🚀 Installation & Setup

### 1️⃣ Fork & Clone the Repository

```sh
git clone https://github.com/yourusername/ait-brute-force-tool.git
```

```sh
cd ait-brute-force-tool
```

### 2️⃣ Set Up ChromeDriver  

- Download the correct ChromeDriver version (based on your browser).  
- Extract it and move it to a directory in your system **PATH**.  

---

## 📌 Usage

### Running the Generator (generator.py)

- The generator creates possible (A-Z) and (1-9) combinations based on predefined rules.

```sh
python generator.py
```

- It will automatically generate possible combinations based on selected option (1-14).
- Option 15 will automatically execute all options from 1 to 14 (choose this option if you want to generate all).
- **This script also generates a `prefix.txt` file, which is required for testing.** Ensure this file **exists** and contains a **hardcoded value for the exact username prefix** after execution.

### Running the Brute Force Tool (main.py)

To start the tool, run:

```sh
python main.py
```
or

```sh
python3 main.py
```

### Running with CLI Arguments

- Run the tool with custom login/dashboard URLs:
  
  ```sh
  python main.py --login_url "http://example.com/login" --wrong_url "http://example.com/fail"
  ```

---

## 🔢 Mapping Rules

### Overview
This document outlines the mapping rules for username and password combinations. There are two levels of mapping: **Basic Level** and **Advanced Level**.

### Basic Level Mapping
In this level, each username maps to an identical password.

```
1  -> 1
2  -> 2
3  -> 3
...
14 -> 14
```

### Advanced Level Mapping
In this level, each username maps to multiple possible passwords, except for its identical match.

```
1  -> 2, 3, 4, 5, ..., 14
2  -> 1, 3, 4, 5, ..., 14
...
14 -> 1, 2, 3, 4, ..., 13
```

### How to Use
- **Basic Level Mapping**: Use when a direct one-to-one mapping is required.
- **Advanced Level Mapping**: Use when multiple mappings are needed for increased flexibility.

### Notes
- Ensure that the correct mapping level is selected before execution.
- Future updates may introduce additional mapping rules or customization options.

---

## 🔧 Troubleshooting  

### ❌ ChromeDriver Version Mismatch  
If you encounter an error like:  

> This version of ChromeDriver only supports Chrome version X  

Check that:  
- Your ChromeDriver version matches your **Chrome browser version**.  
- Your Chrome is up to date, or downgrade Chrome to match the driver.  

### ❌ Python Not Found  
If you see **"command not found"**, ensure **Python is installed and added to your system PATH**.  

### ❌ Selenium Import Error  
If you see **ModuleNotFoundError: No module named 'selenium'**, reinstall Selenium:  

```sh
pip install selenium --upgrade
```

---

## 📢 Changelog

See the latest updates and improvements in the [CHANGELOG.md](CHANGELOG.md).

---

## 📜 License 

This project is open-source and licensed under the **MIT License**.
